"""Ghép lớp phụ vào shard dữ liệu web dựng sẵn (chạy lại được, an toàn):
  - data-claude/pilot-*.json  → thay phần senses học thuật của đúng (từ, từ loại), gắn model "claude-sonnet-5-5" (nhãn AI)
  - data-econ/terms.json      → entry["domains"] (nhãn ngành, nguồn: Wiktionary category en:<chủ đề>)
Bản gốc của mỗi shard được chép vào data/backup-shards/ lần đầu; luôn đọc từ bản gốc → chạy lại không chồng lớp.
Dùng: python3.12 data-claude/overlay.py
"""
import glob, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "web-prebuilt" / "v" / "v2026.10.07-ba343f9d" / "e"
BK = ROOT / "data" / "backup-shards"
MODEL = "claude-sonnet-5-5"
SPELL = {"amortisation": "amortization", "urbanisation": "urbanization"}  # từ điển chỉ có kiểu Mỹ
CORE = ["accounting", "economics", "finance", "banking", "taxation", "insurance", "commerce", "money", "stock-market", "business", "marketing", "management"]


def fnv1a32(s):
    h = 0x811C9DC5
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h


def shard_path(word):
    return D / f"{fnv1a32(word) % 2048:04d}.json"


def load(path):
    bk = BK / path.name
    src = bk if bk.exists() else path
    if not bk.exists():
        BK.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, bk)
    return json.loads(src.read_text(encoding="utf-8"))


def to_sense(s):
    return {"cefr": s.get("cefr"), "definition": s["definition"], "examples": s.get("examples", []), "grammar": s.get("grammar", ""),
            "guideword": s.get("guideword", ""), "labels": s.get("labels", ""), "vi": s.get("vi", ""), "vi_ok": False}


def new_block(pos):
    return {"antonyms": [], "cefr": None, "entry_type": "word", "etymology": None, "forms": [], "model": None, "pos": pos,
            "senses": [], "thesaurus": [], "translations": [], "vi_block": [], "wiktionary": []}


def main():
    shards, touched = {}, set()

    def entry(word):
        p = shard_path(word)
        if p not in shards:
            shards[p] = load(p)
        e = shards[p].get(word)
        if e is None:
            print("không có trong từ điển:", word, file=sys.stderr)
        return p, e

    domains = json.loads((ROOT / "data-econ" / "terms.json").read_text(encoding="utf-8"))
    pilot_dom = {}
    pilot = []
    for f in sorted(glob.glob(str(ROOT / "data-claude" / "pilot-*.json"))):
        for e in json.loads(Path(f).read_text(encoding="utf-8"))["entries"]:
            e["word"] = SPELL.get(e["word"], e["word"])
            pilot.append(e)
            if e.get("domain"):
                pilot_dom.setdefault(e["word"], set()).add(e["domain"])
    for w, ds in pilot_dom.items():
        domains.setdefault(w, [])
        domains[w] = sorted(set(domains[w]) | ds)

    # lớp học thuật Claude/Haiku cho thuật ngữ ngành: data-econ/ai/ok-*.json (do validate.py lọc)
    econ = []
    for f in sorted(glob.glob(str(ROOT / "data-econ" / "ai" / "ok-*.json"))):
        econ += json.loads(Path(f).read_text(encoding="utf-8"))["entries"]
    n_dom = n_pilot = 0
    for w, ds in domains.items():
        p, e = entry(w)
        if e is None:
            continue
        e["domains"] = sorted(set(ds), key=lambda d: CORE.index(d) if d in CORE else 99)
        touched.add(p); n_dom += 1
    for pe in pilot:
        p, e = entry(pe["word"])
        if e is None:
            continue
        blk = next((b for b in e["blocks"] if b["pos"] == pe["pos"]), None)
        if blk is None:
            blk = new_block(pe["pos"]); e["blocks"].append(blk)
        blk["senses"] = [to_sense(s) for s in pe["senses"]]
        blk["model"] = MODEL
        touched.add(p); n_pilot += 1
    n_econ = 0
    for pe in econ:
        if not pe["senses"]:
            continue
        p, e = entry(pe["word"])
        if e is None:
            continue
        blk = next((b for b in e["blocks"] if b["pos"] == pe["pos"]), None)
        if blk is None or blk["senses"]:  # không đè nghĩa Gemini/Claude đã có
            continue
        blk["senses"] = [to_sense(s) for s in pe["senses"]]
        blk["model"] = "claude-haiku-5-5"
        touched.add(p); n_econ += 1
    for p in touched:
        p.write_text(json.dumps(shards[p], ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    print(f"domains={n_dom} pilot-blocks={n_pilot} econ-blocks={n_econ} shards-written={len(touched)}")


main()

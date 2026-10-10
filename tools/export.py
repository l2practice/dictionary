"""Xuất dữ liệu từ điển cho repo Writing / Speaking (JSONL lồng + CSV phẳng).
Dùng: python3.12 data-claude/export.py [--set pilot|domains|both|all-ai]   (mặc định both)
  pilot   = 100 từ Claude soạn;  domains = thuật ngữ kinh tế–kế toán;  all-ai = mọi mục có lớp học thuật AI (lớn)
Ra: export/<tên>.jsonl, export/<tên>.csv  (UTF-8; CSV có BOM để Excel mở đúng tiếng Việt)
Mỗi dòng CSV = một nghĩa. source: claude | gemini | wiktionary. is_ai: 1 nếu do AI soạn.
"""
import csv, glob, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "web-prebuilt" / "v" / "v2026.10.07-ba343f9d" / "e"


def fnv1a32(s):
    h = 0x811C9DC5
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h


_cache = {}


def get(word):
    p = D / f"{fnv1a32(word) % 2048:04d}.json"
    if p not in _cache:
        _cache[p] = json.loads(p.read_text(encoding="utf-8"))
    return _cache[p].get(word)


def flat(e):
    rows = []
    for b in e["blocks"]:
        if b["senses"]:
            src = "claude" if (b.get("model") or "").startswith("claude") else "gemini"
            for i, s in enumerate(b["senses"], 1):
                ex = s.get("examples") or [{}]
                rows.append(dict(word=e["word"], pos=b["pos"], sense_no=i, domains=";".join(e.get("domains") or []),
                                 ipa_uk=(e["ipa"] or {}).get("uk") or "", cefr=s.get("cefr") or "", guideword=s.get("guideword") or "",
                                 grammar=s.get("grammar") or "", labels=s.get("labels") or "", definition_en=s["definition"],
                                 meaning_vi=s.get("vi") or "", example_en=ex[0].get("en", ""), example_vi=ex[0].get("vi", ""),
                                 example2_en=(ex[1].get("en", "") if len(ex) > 1 else ""), example2_vi=(ex[1].get("vi", "") if len(ex) > 1 else ""),
                                 source=src, model=b.get("model") or "", is_ai=1))
        else:
            for i, w in enumerate(b["wiktionary"][:3], 1):
                rows.append(dict(word=e["word"], pos=b["pos"], sense_no=i, domains=";".join(e.get("domains") or []),
                                 ipa_uk=(e["ipa"] or {}).get("uk") or "", cefr="", guideword="", grammar=w.get("grammar") or "",
                                 labels=w.get("labels") or "", definition_en=w["gloss"], meaning_vi=w.get("vi") or "",
                                 example_en=(w.get("examples") or [""])[0], example_vi="", example2_en="", example2_vi="",
                                 source="wiktionary", model="", is_ai=0))
    return rows


def words_for(which):
    out = []
    if which in ("pilot", "both"):
        for f in sorted(glob.glob(str(ROOT / "data-claude" / "pilot-*.json"))):
            for e in json.loads(Path(f).read_text(encoding="utf-8"))["entries"]:
                w = {"amortisation": "amortization", "urbanisation": "urbanization"}.get(e["word"], e["word"])
                if w not in out:
                    out.append(w)
    if which in ("domains", "both"):
        for w in json.loads((ROOT / "data-econ" / "terms.json").read_text(encoding="utf-8")):
            if w not in out:
                out.append(w)
    if which == "all-ai":
        for p in sorted(D.glob("*.json")):
            for w, e in json.loads(p.read_text(encoding="utf-8")).items():
                if any(b["senses"] for b in e["blocks"]):
                    out.append(w)
    return out


def main():
    which = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "both"
    out = ROOT / "export"; out.mkdir(exist_ok=True)
    rows, n = [], 0
    with open(out / f"dictionary-{which}.jsonl", "w", encoding="utf-8") as jf:
        for w in words_for(which):
            e = get(w)
            if not e:
                continue
            r = flat(e)
            if not r:
                continue
            n += 1; rows += r
            jf.write(json.dumps({"word": w, "domains": e.get("domains") or [], "ipa_uk": (e["ipa"] or {}).get("uk"), "senses": r}, ensure_ascii=False) + "\n")
    with open(out / f"dictionary-{which}.csv", "w", encoding="utf-8-sig", newline="") as cf:
        wr = csv.DictWriter(cf, fieldnames=list(rows[0]))
        wr.writeheader(); wr.writerows(rows)
    print(which, n, "từ", len(rows), "nghĩa →", out)


main()

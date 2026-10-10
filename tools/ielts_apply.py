"""Nhập từ vựng IELTS (Muse) vào bộ CEFR của Writing (artwrite/aw-cefr.js) và Speaking (fluentalk/cefr-dict.js).
Đọc  ~/Desktop/Ứng dụng/ielts-NN.json  (mỗi file {"topic","items":[{item,pos,cefr,register,use,band,definition,vi,collocations,
writing_example,writing_vi,speaking_example,speaking_vi,tip}]}).
Quy tắc: từ/cụm ĐÃ có trong CEFR_MAP thì bỏ qua (không đổi cấp cũ); chỉ thêm mục mới. Ghi thêm ielts-vocab.json (collocation, ví dụ, mẹo)
vào gốc hai repo. Không có --push thì chỉ ghi vào thư mục làm việc và in thống kê.
Dùng: python3.12 tools/ielts_apply.py [--src DIR] [--out DIR] [--push]"""
import argparse, glob, json, re, subprocess, sys
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument("--src", default=str(Path.home() / "Desktop" / "Ứng dụng"))
ap.add_argument("--out", default="/private/tmp/ielts-apply")
ap.add_argument("--push", action="store_true")
a = ap.parse_args()
LV = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
POS = {"noun": "n", "verb": "v", "adj": "j", "adv": "r", "prep": "p", "det": "d", "conj": "c", "pron": "o", "intj": "x", "num": "m", "phrase": "o"}
REQ = ["item", "pos", "cefr", "definition", "vi", "collocations", "writing_example", "speaking_example"]

items, bad, topics = {}, [], []
def load_topics():
    """Mỗi file là {topic, items} hoặc danh sách các {topic, items} (ielts-vocab-32-topics.json)."""
    for f in sorted(glob.glob(str(Path(a.src) / "ielts-*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            bad.append((Path(f).name, "JSON lỗi " + str(e)[:50])); continue
        for t in (d if isinstance(d, list) else [d]):
            yield f, t

for f, d in load_topics():
    topics.append(d.get("topic", Path(f).stem))
    for it in d.get("items", []):
        if any(not it.get(k) for k in REQ) or it["cefr"] not in LV:
            bad.append((Path(f).name, "thiếu/sai trường: " + str(it.get("item")))); continue
        key = it["item"].strip().lower()
        # bỏ collocation chỉ lặp lại mục (hoặc là một mảnh của cụm), giữ phần còn lại
        it["collocations"] = [c for c in dict.fromkeys(it["collocations"]) if c.strip().lower() not in key]
        if key in items:
            items[key]["topics"].append(d["topic"]); continue
        it["topics"] = [d["topic"]]; items[key] = it
print(f"{len(topics)} chủ đề, {len(items)} mục hợp lệ, {len(bad)} lỗi", bad[:5])

def code(it):
    return f'{LV[it["cefr"]]}{POS.get(it["pos"], "o")}'

def update(repo, fname, regex, prefix, suffix):
    d = Path(a.out) / repo
    if not d.exists():
        d.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["gh", "repo", "clone", f"l2practice/{repo}", str(d), "--", "-q", "--depth", "1"], check=True)
    p = d / fname
    s = p.read_text(encoding="utf-8")
    m = re.search(regex, s, re.S)
    cmap = json.loads(m.group(1))
    add = skip = 0
    for k, it in items.items():
        if " " in k: continue   # cụm nhiều từ: bộ phân tích chỉ tra từng từ, nên chỉ lưu trong ielts-vocab.json
        if k in cmap: skip += 1; continue
        cmap[k] = code(it); add += 1
    cmap = dict(sorted(cmap.items()))
    mj = json.dumps(cmap, ensure_ascii=False, separators=(",", ":"))
    s = s[:m.start()] + prefix + mj + suffix + s[m.end():]
    s = re.sub(r"(\d+) (từ|words)", lambda x: x.group(0), s)
    p.write_text(s, encoding="utf-8")
    vocab = {k: {kk: vv for kk, vv in it.items() if kk != "item"} for k, it in sorted(items.items())}
    (d / "ielts-vocab.json").write_text(json.dumps(vocab, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    Path(a.out, "ielts-vocab.json").write_text(json.dumps(vocab, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{repo}: +{add} mục mới, bỏ qua {skip} trùng; tổng CEFR_MAP {len(cmap)}")
    if a.push and add:
        subprocess.run(["git", "-C", str(d), "config", "user.name", "thanhtuduong"], check=True)
        subprocess.run(["git", "-C", str(d), "config", "user.email", "thanhtu.duong88@gmail.com"], check=True)
        subprocess.run(["git", "-C", str(d), "add", fname, "ielts-vocab.json"], check=True)
        subprocess.run(["git", "-C", str(d), "commit", "-q", "-m", f"CEFR wordlist: +{add} IELTS items (skipped {skip} existing); add ielts-vocab.json (collocations, examples)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"], check=True)
        subprocess.run(["git", "-C", str(d), "push", "-q", "origin", "HEAD:main"], check=True)
        print(repo, "đã push")

if items:
    update("artwrite", "aw-cefr.js", r"var CEFR_MAP = (\{.*?\});", "var CEFR_MAP = ", ";")
    update("fluentalk", "cefr-dict.js", r"const CEFR_MAP=(\{.*?\});", "const CEFR_MAP=", ";")

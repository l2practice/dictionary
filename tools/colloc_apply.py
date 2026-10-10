"""Nhập collocation (Muse) cho ~3.000 từ phổ biến.
Đọc ~/Desktop/Ứng dụng/colloc-NN.json ({"items":[{item,collocations[5],example,example_vi,note}]}), kiểm tra, gộp thành collocations.json
{từ: {c, e, v, n}}. Kiểm: từ phải nằm trong tools/colloc-selected.json; mỗi cụm phải chứa gốc của từ; 3–6 cụm; ví dụ ≤ 24 từ.
Dùng: python3.12 tools/colloc_apply.py [--src DIR] [--out data/collocations.json] [--push-repos]  (push-repos: thêm vào artwrite & fluentalk)"""
import argparse, glob, json, subprocess
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument("--src", default=str(Path.home() / "Desktop" / "Ứng dụng"))
ap.add_argument("--out", default="data/collocations.json")
ap.add_argument("--push-repos", action="store_true")
a = ap.parse_args()
H = Path(__file__).resolve().parent
sel = {x["item"] for x in json.load(open(H / "colloc-selected.json", encoding="utf-8"))}
out, bad = {}, []
def stem(w): return w[:-1] if w.endswith(("e", "y")) and len(w) > 4 else w
for f in sorted(glob.glob(str(Path(a.src) / "colloc-*.json"))):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception as e: bad.append((Path(f).name, "JSON lỗi")); continue
    for it in d.get("items", []):
        w = str(it.get("item", "")).strip().lower()
        if w not in sel: bad.append((w, "không có trong danh sách")); continue
        cs = [c.strip() for c in dict.fromkeys(it.get("collocations", [])) if isinstance(c, str) and c.strip()]
        cs = [c for c in cs if stem(w)[:max(3, len(stem(w)) - 1)] in c.lower()]
        if len(cs) < 3: bad.append((w, "dưới 3 cụm hợp lệ")); continue
        ex = str(it.get("example", "")).strip()
        if len(ex.split()) > 24: ex = ""
        out[w] = {"c": cs[:6], "e": ex, "v": str(it.get("example_vi", "")).strip() if ex else "", "n": str(it.get("note", "")).strip()}
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
json.dump(dict(sorted(out.items())), open(a.out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"{len(out)} từ hợp lệ; {len(bad)} lỗi/bỏ qua:", bad[:8])
if a.push_repos and out:
    for repo in ("artwrite", "fluentalk"):
        d = Path("/private/tmp/colloc-apply") / repo
        if not d.exists():
            d.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["gh", "repo", "clone", f"l2practice/{repo}", str(d), "--", "-q", "--depth", "1"], check=True)
        (d / "collocations.json").write_text(Path(a.out).read_text(encoding="utf-8"), encoding="utf-8")
        for k, v in (("user.name", "thanhtuduong"), ("user.email", "thanhtu.duong88@gmail.com")):
            subprocess.run(["git", "-C", str(d), "config", k, v], check=True)
        subprocess.run(["git", "-C", str(d), "add", "collocations.json"], check=True)
        subprocess.run(["git", "-C", str(d), "commit", "-q", "-m", f"Add collocations.json ({len(out)} words: collocations + example)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"], check=True)
        subprocess.run(["git", "-C", str(d), "push", "-q", "origin", "HEAD:main"], check=True)
        print(repo, "đã push")

"""Dựng data/domains.json cho tab "Chuyên ngành" của giao diện: {domain: [[từ, nghĩa Việt ngắn, CEFR, có AI?], ...]} (đã sắp A→Z).
Bỏ từ rất phổ thông (hạng tần suất ≤ 250: for, do, life…) vì chỉ có nghĩa chuyên ngành ở một vài khối nhỏ."""
import glob, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "web-prebuilt" / "v" / "v2026.10.07-ba343f9d" / "e"
terms = json.loads((ROOT / "data-econ" / "terms.json").read_text(encoding="utf-8"))
need = {}
for w in terms: need.setdefault(w, None)
for f in glob.glob(str(D / "*.json")):
    sh = json.load(open(f, encoding="utf-8"))
    for w in sh.keys() & terms.keys():
        e = sh[w]
        if e.get("rank") is not None and e["rank"] <= 250: continue
        vi = cefr = ""; ai = 0
        dom_lab = [d for d in terms[w]]
        best = None
        for b in e["blocks"]:
            for s in b["senses"]:
                if s.get("vi") and (best is None or any(d in (s.get("labels") or "") for d in ("accounting", "economics", "finance", "banking", "tax"))):
                    best = (s["vi"].split(";")[0].strip(), s.get("cefr") or b["cefr"] or "", 1)
                    if any(d in (s.get("labels") or "") for d in ("accounting", "economics", "finance", "banking", "tax")): break
            if best and best[2]: pass
        if best: vi, cefr, ai = best
        else:
            for b in e["blocks"]:
                if b["vi_block"]: vi = b["vi_block"][0].split(".")[0][:40]; break
        need[w] = [w, vi, cefr, ai]
out = {}
for w, row in need.items():
    if row is None: continue
    for d in terms[w]: out.setdefault(d, []).append(row)
for d in out: out[d].sort(key=lambda r: r[0].lower())
(ROOT / "data" / "web-prebuilt" / "domains.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print({d: len(v) for d, v in sorted(out.items(), key=lambda x: -len(x[1]))}, sum(1 for v in need.values() if v))

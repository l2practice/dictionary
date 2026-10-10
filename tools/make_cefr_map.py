"""Tạo bộ CEFR_MAP lớn hơn cho repo Writing (artwrite/aw-cefr.js) và Speaking (fluentalk/cefr-dict.js), cùng định dạng:
  {"word": "4v|5n"}  (chữ số = cấp 1..6 = A1..C2, chữ cái = loại từ n/v/j/r/p/d/c/o/x/m; nhiều mã cách nhau "|", cấp dễ trước)
Nguồn gộp (ưu tiên từ trên xuống): (1) 9.394 từ gốc của hai repo (giữ nguyên), (2) CEFR-J/Octanove trong từ điển này (block.cefr),
(3) cấp CEFR do AI ước lượng cho từng nghĩa (sense.cefr; lấy cấp THẤP nhất của từ loại đó, đánh dấu riêng trong cefr-source.json).
Dùng: python3.12 data-claude/make_cefr_map.py <aw-cefr.js gốc> <cefr-dict.js gốc>
Ra: export/writing-speaking/{cefr-map.json, cefr-source.json, aw-cefr.js, cefr-dict.js, glossary-vi.json}"""
import glob, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "web-prebuilt" / "v" / "v2026.10.07-ba343f9d" / "e"
OUT = ROOT / "export" / "writing-speaking"; OUT.mkdir(parents=True, exist_ok=True)
LV = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
POS = {"noun": "n", "verb": "v", "adj": "j", "adv": "r", "prep": "p", "det": "d", "conj": "c", "pron": "o", "intj": "x", "num": "m"}
aw_src = Path(sys.argv[1]).read_text(encoding="utf-8"); ck_src = Path(sys.argv[2]).read_text(encoding="utf-8")
base = json.loads(re.search(r"const CEFR_MAP=(\{.*?\});", ck_src, re.S).group(1))
codes = {w: v.split("|") for w, v in base.items()}
source = {w: "base" for w in base}
gloss = {}
OKW = re.compile(r"^[a-z][a-z' -]*$")
for f in glob.glob(str(D / "*.json")):
    for w, e in json.load(open(f, encoding="utf-8")).items():
        if not OKW.match(w): continue
        add = {}
        for b in e["blocks"]:
            p = POS.get(b["pos"])
            if not p: continue
            lv, src = (LV.get(b["cefr"]), "cefrj") if b["cefr"] else (None, None)
            if lv is None and b["senses"]:
                ls = [LV[s["cefr"]] for s in b["senses"] if s.get("cefr") in LV]
                if ls: lv, src = min(ls), "ai"
            if lv and p not in add: add[p] = (lv, src)
            if b["senses"] and w not in gloss:
                s = b["senses"][0]
                gloss[w] = {"p": b["pos"], "v": s.get("vi") or "", "d": s["definition"], "c": s.get("cefr") or b["cefr"] or "", **({"x": e["domains"]} if e.get("domains") else {})}
        if not add: continue
        if w in codes:
            have = {c[1] for c in codes[w]}
            new = [f"{l}{p}" for p, (l, s) in add.items() if p not in have]
            if new:
                codes[w] = codes[w] + sorted(new, key=lambda c: c[0])  # giữ nguyên thứ tự mã gốc: cấp đầu tiên của từ cũ không đổi
        else:
            codes[w] = sorted([f"{l}{p}" for p, (l, s) in add.items()], key=lambda c: c[0])
            source[w] = "cefrj" if any(s == "cefrj" for l, s in add.values()) else "ai"
cmap = {w: "|".join(c) for w, c in sorted(codes.items())}
json.dump(cmap, open(OUT / "cefr-map.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump({w: s for w, s in source.items() if s != "base"}, open(OUT / "cefr-source.json", "w", encoding="utf-8"), separators=(",", ":"))
json.dump(gloss, open(OUT / "glossary-vi.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
mj = json.dumps(cmap, ensure_ascii=False, separators=(",", ":"))
n = len(cmap)
ck = re.sub(r"const CEFR_MAP=\{.*?\};", lambda m: "const CEFR_MAP=" + mj + ";", ck_src, count=1, flags=re.S)
ck = re.sub(r"// 9394 từ[^\n]*", f"// {n} từ (9394 từ gốc + CEFR-J/Octanove + cấp do AI ước lượng, xem cefr-source.json). A1-C2 + loại từ. Mã: cấp(1=A1..6=C2) + loại(n/v/j/r/p/d/c/o/x/m)", ck, count=1)
aw = re.sub(r"var CEFR_MAP = \{.*?\};", lambda m: "var CEFR_MAP = " + mj + ";", aw_src, count=1, flags=re.S)
aw = aw.replace("The CEFR wordlist (9394 words,", f"The CEFR wordlist ({n} words,")
(OUT / "cefr-dict.js").write_text(ck, encoding="utf-8"); (OUT / "aw-cefr.js").write_text(aw, encoding="utf-8")
from collections import Counter
print(n, "từ trong CEFR_MAP;", dict(Counter(source.values())), "; glossary", len(gloss), "từ")

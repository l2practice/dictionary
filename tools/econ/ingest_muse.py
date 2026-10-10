"""Nhập kết quả từ Muse: lưu câu trả lời của mỗi lô vào data-econ/muse/out/<số lô>.txt (dán nguyên, có ```json cũng được).
Chạy: python3 data-econ/ingest_muse.py   → chuyển thành ai/out-<số lô>.json rồi chạy validate.py (in lỗi từng lô)."""
import json, re, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
def parse(txt):
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    a, b = txt.find("{"), txt.rfind("}")
    return json.loads(txt[a:b + 1])
done = bad = 0
for f in sorted((H / "muse" / "out").glob("*.txt")):
    n = f.stem.replace("prompt-", "").replace("out-", "")
    try:
        d = parse(f.read_text(encoding="utf-8"))
        assert isinstance(d.get("entries"), list)
        (H / "ai" / f"out-{n}.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8"); done += 1
    except Exception as e:
        bad += 1; print("lô", n, "JSON lỗi:", str(e)[:80])
print("nhập", done, "lô;", bad, "lỗi")
subprocess.run([sys.executable, "-I", str(H / "validate.py")])

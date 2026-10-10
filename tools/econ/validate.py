"""Kiểm kết quả AI: data-econ/ai/out-NNN.json so với batches/batch-NNN.json. In lỗi; ghi ai/ok-NNN.json (chỉ entry hợp lệ)."""
import json,sys,glob,re
from pathlib import Path
H=Path(__file__).resolve().parent
CEFR={"A1","A2","B1","B2","C1","C2"}
def check(inp,out):
    ok,errs=[],[]
    by={(e.get("word"),e.get("pos")):e for e in out.get("entries",[]) if isinstance(e,dict)}
    for b in inp:
        e=by.get((b["word"],b["pos"]))
        if not e: errs.append((b["word"],b["pos"],"thiếu entry"));continue
        n=len(b["glosses"]);good=[]
        for s in e.get("senses",[]):
            try:
                assert isinstance(s["definition"],str) and 3<len(s["definition"])<300
                assert isinstance(s["vi"],str) and s["vi"].strip()
                assert s["cefr"] in CEFR
                assert isinstance(s["src"],list) and s["src"] and all(isinstance(i,int) and 1<=i<=n for i in s["src"])
                ex=[x for x in s.get("examples",[]) if isinstance(x,dict) and x.get("en") and x.get("vi")]
                good.append(dict(src=s["src"],guideword=s.get("guideword") or "",grammar=s.get("grammar") or "",labels=s.get("labels") or "",definition=s["definition"].strip(),vi=s["vi"].strip(),cefr=s["cefr"],examples=ex[:2],vi_ok=bool(s.get("vi_ok"))))
            except Exception as x: errs.append((b["word"],b["pos"],"nghĩa lỗi "+repr(x)[:60]))
        ok.append(dict(word=b["word"],pos=b["pos"],senses=good))
    return ok,errs
if __name__=="__main__":
    tot=bad=sen=emp=0
    for f in sorted(glob.glob(str(H/"ai"/"out-*.json"))):
        i=re.search(r"out-(\d+)",f).group(1)
        try: out=json.load(open(f,encoding="utf-8"))
        except Exception as e: print(i,"JSON hỏng",e);continue
        ok,errs=check(json.load(open(H/"batches"/f"batch-{i}.json",encoding="utf-8")),out)
        json.dump({"entries":ok},open(H/"ai"/f"ok-{i}.json","w",encoding="utf-8"),ensure_ascii=False)
        tot+=len(ok);bad+=len(errs);sen+=sum(len(e["senses"]) for e in ok);emp+=sum(1 for e in ok if not e["senses"])
        for e in errs[:5]: print(i,e)
    print("entries",tot,"senses",sen,"empty",emp,"errors",bad)

import json,sys
root=sys.argv[1]
acc=set()
for i,l in enumerate(open(root+"/results/V3T/accepted.tsv")):
    f=l.rstrip("\n").split("\t")
    if i==0: continue
    if f[7]=="ACCEPTED": acc.add(f[0])
out=[];rt=0
for l in open("M.jsonl"):
    r=json.loads(l)
    assert json.dumps(r)+"\n"==l
    if r["case"] in acc: continue
    out.append(r)
for i,r in enumerate(out): r["idx"]=i
open("Mr.jsonl","w").write("".join(json.dumps(r)+"\n" for r in out))
print("accepted cases",len(acc),"removed",17989-len(out),"n",len(out),"cases",len({r["case"] for r in out}))

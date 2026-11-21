import json, hashlib, sys, os, re, gzip
REPO=sys.argv[1]; B34=REPO+"/archive/es7-2026-10-19/results/LO33N20261113/budget34"; AUD=B34+"/audit"
raw=open(B34+"/data/frozen-inputs/s20-v5/extra.json","rb").read()
v5=json.loads(raw)
for ind in (1,None):
    for tail in (b"", b"\n"):
        s=json.dumps(v5, indent=ind).encode()+tail
        print("s20-v5 format indent",ind,"tail",tail, hashlib.sha256(s).hexdigest()==hashlib.sha256(raw).hexdigest())
print("s20-v5 file sha", hashlib.sha256(raw).hexdigest()[:16], "cap rows", [ (len(r["support"]), r["rhs"], list(r.keys())) for r in v5[:2]])
# rebuild v169 in order (unsorted supports as given)
rows=[dict(r) for r in v5[2:]]
for k in range(6,14):
    rows += [{"support": json.loads(l)["support"], "rhs": json.loads(l)["rhs"]} for l in open(f"{AUD}/cuts-v{k}/replay.jsonl")]
for k in range(101,170):
    for d in sorted(d for d in os.listdir(AUD) if re.fullmatch(rf"cuts-v{k}([a-z][a-z0-9]*)?", d)):
        rows += [{"support": json.loads(l)["support"], "rhs": json.loads(l)["rhs"]} for l in open(f"{AUD}/{d}/replay.jsonl")]
cat=json.load(gzip.open(B34+"/data/frozen-inputs/source-2650.json.gz")); st=cat["states"]
F=[i for i in range(154) if st[i][0]>=5]; Lo=[i for i in range(154) if st[i][0]<=4]
for capF,capLo in ((v5[0]["support"],v5[1]["support"]),(F,Lo)):
    full=[{"support":capF,"rhs":20},{"support":capLo,"rhs":15}]+rows
    for ind in (1,None):
        for tail in (b"", b"\n"):
            h=hashlib.sha256(json.dumps(full, indent=ind).encode()+tail).hexdigest()
            print(ind, tail, h[:16], h.startswith("de4bcceb"))

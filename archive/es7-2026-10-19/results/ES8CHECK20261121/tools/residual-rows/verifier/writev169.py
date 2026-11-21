import json, sys, os, re
REPO=sys.argv[1]; B34=REPO+"/archive/es7-2026-10-19/results/LO33N20261113/budget34"; AUD=B34+"/audit"
v5=json.load(open(B34+"/data/frozen-inputs/s20-v5/extra.json"))
rows=[dict(r) for r in v5[2:]]
for k in range(6,14):
    rows += [{"support": json.loads(l)["support"], "rhs": json.loads(l)["rhs"]} for l in open(f"{AUD}/cuts-v{k}/replay.jsonl")]
for k in range(101,170):
    for d in sorted(d for d in os.listdir(AUD) if re.fullmatch(rf"cuts-v{k}([a-z][a-z0-9]*)?", d)):
        rows += [{"support": json.loads(l)["support"], "rhs": json.loads(l)["rhs"]} for l in open(f"{AUD}/{d}/replay.jsonl")]
full=[{"support":v5[0]["support"],"rhs":20},{"support":v5[1]["support"],"rhs":15}]+rows
open(sys.argv[2],"w").write(json.dumps(full, indent=1)+"\n")

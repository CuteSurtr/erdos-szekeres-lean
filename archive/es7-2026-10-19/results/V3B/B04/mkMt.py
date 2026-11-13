import json, os, glob, sys
ROOT = "/opt/in/cloud/es7-2026-10-19"
files = []
for d, _, fs in os.walk(ROOT + "/results/V3T"):
    files += [os.path.join(d, f) for f in fs if f.endswith(".jsonl")]
files += glob.glob(ROOT + "/results/V3A/*/out.jsonl") + glob.glob(ROOT + "/results/V3B/*/out.jsonl")
files.sort()
keys = set(); bad = 0
for p in files:
    for line in open(p):
        try: r = json.loads(line)
        except Exception: bad += 1; continue
        if isinstance(r, dict) and r.get("kind") == "leaf" and r.get("verdict") == "VERIFIED" and "lits" in r:
            keys.add((r["case"], json.dumps(r["lits"])))
out = []
for line in open("/opt/work/M.jsonl"):
    r = json.loads(line)
    if (r["case"], json.dumps(r["lits"])) in keys: continue
    out.append(r)
with open("/opt/work/Mt.jsonl", "w") as f:
    for i, r in enumerate(out):
        r["idx"] = i
        f.write(json.dumps(r) + "\n")
print("files", len(files), "unparsable lines", bad)
print("VERIFIED keys", len(keys), "n", len(out))

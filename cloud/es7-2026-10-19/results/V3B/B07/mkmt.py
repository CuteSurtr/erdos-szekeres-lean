import json, glob, os, sys
ROOT = "/opt/in/cloud/es7-2026-10-19"
files = sorted(glob.glob(ROOT + "/results/V3T/**/*.jsonl", recursive=True)) + sorted(glob.glob(ROOT + "/results/V3A/*/out.jsonl")) + sorted(glob.glob(ROOT + "/results/V3B/*/out.jsonl"))
keys = set(); bad = 0
for f in files:
    for line in open(f):
        line = line.strip()
        if not line: continue
        try: r = json.loads(line)
        except Exception: bad += 1; continue
        if isinstance(r, dict) and r.get("kind") == "leaf" and r.get("verdict") == "VERIFIED" and "lits" in r:
            keys.add((r["case"], json.dumps(r["lits"])))
out = []; removed = 0
for line in open("/opt/work/M.jsonl"):
    r = json.loads(line)
    if (r["case"], json.dumps(r["lits"])) in keys: removed += 1; continue
    out.append(r)
with open("/opt/work/Mt.jsonl", "w") as g:
    for i, r in enumerate(out):
        r["idx"] = i; g.write(json.dumps(r) + "\n")
print("files", len(files), "unparsable_lines", bad, "verified_keys", len(keys), "removed", removed, "n", len(out))

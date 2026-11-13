import json, collections
c = collections.Counter(); tops = {}; sat = 0; recs = []
for l in open('/opt/es7/out/leaves.jsonl'):
    d = json.loads(l); recs.append(d)
last = {}
for d in recs: last[d["key"]] = d
for d in last.values():
    c[(d["kind"], d["status"], d.get("lrat"))] += 1
for k, v in sorted(c.items(), key=str): print(k, v)
print("max solve_s", max(d.get("solve_s", 0) or 0 for d in last.values()))

#!/usr/bin/env python3
"""drop.py QUEUE.icnf OUT_QUEUE.icnf DROPPED.jsonl MYLEAVES.jsonl OTHERDIR...
Queue = the cubes F5 still has to close (its share, or the driver's current open frontier).
A queue cube c is dropped when the records of the other drivers (OTHERDIR/leaves.jsonl) prove it:
c, or a prefix of c, is a verified leaf (cake_lpr == `s VERIFIED UNSAT`), or c was split there
and every sub-cube is (recursively) proved.  Remaining cubes go to OUT_QUEUE in the same order;
dropped ones are appended to DROPPED.jsonl with the directory whose leaves cover them."""
import json, os, sys, time
q, outq, dj, mine, others = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
def cubes(p):
    cs = []
    for l in open(p):
        assert l.startswith("a ") and l.endswith(" 0\n"), l
        cs.append(tuple(map(int, l.split()[1:-1])))
    return cs
def recs(p):
    for l in open(p):
        if l.endswith("\n") and l.strip(): yield json.loads(l)
def covered_by(d):
    closed, split = set(), {}
    for r in recs(os.path.join(d, "leaves.jsonl")):
        if "cube" not in r: continue
        c = tuple(r["cube"])
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT": closed.add(c)
        elif r.get("status") == "SPLIT" and "subs" in r: split[c] = [tuple(s) for s in r["subs"]]
    memo = {}
    def cov(c):
        if c in memo: return memo[c]
        v = any(c[:i] in closed for i in range(len(c) + 1)) or (c in split and all(cov(c + s) for s in split[c]))
        memo[c] = v; return v
    return cov
covs = [(d, covered_by(d)) for d in others if os.path.exists(os.path.join(d, "leaves.jsonl"))]
keep, drop = [], []
for c in cubes(q):
    who = next((d for d, f in covs if f(c)), None)
    (keep if who is None else drop).append((c, who))
with open(outq + ".tmp", "w") as f:
    for c, _ in keep: f.write("a " + " ".join(map(str, c)) + " 0\n")
os.replace(outq + ".tmp", outq)
with open(dj, "a") as f:
    for c, who in drop:
        f.write(json.dumps({"cube": list(c), "covered_by": who, "time": time.strftime("%H:%M:%SZ", time.gmtime())}) + "\n")
print(f"queue {len(keep) + len(drop)} kept {len(keep)} dropped {len(drop)}")

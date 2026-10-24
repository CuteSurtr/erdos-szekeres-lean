#!/usr/bin/env python3
"""Canonical order-type fingerprints (chiro.canonical_form: relabelling + reflection, sha1[:16]) of
26-point sets.  Reference = F2's realized sets (results/F2/data/sets26/*.pts and
results/F2/s2/data/run1/sets26.jsonl).  usage: fingerprint26.py OUT.json new1.pts|new.jsonl ...
Prints, for each new set, its fingerprint and whether it equals a reference or an earlier new set."""
import sys, os, json, glob, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(R, "..", "tools", "realizer"))
from chiro import canonical_form, chirotope_of
def canon(P): return hashlib.sha1(canonical_form(chirotope_of(P), len(P)).encode()).hexdigest()[:16]
def load(path):
    if path.endswith(".jsonl"):
        return [(json.loads(l)["id"], [tuple(p) for p in json.loads(l)["points"]]) for l in open(path) if l.strip()]
    return [(os.path.splitext(os.path.basename(path))[0], [tuple(map(int, l.split())) for l in open(path) if l.strip()])]
ref = {}
for f in sorted(glob.glob(os.path.join(R, "F2/data/sets26/*.pts"))) + [os.path.join(R, "F2/s2/data/run1/sets26.jsonl")]:
    for name, P in load(f): ref.setdefault(canon(P), []).append("F2:" + name)
res = {"reference": {h: v for h, v in ref.items()}, "new": []}
seen = {}
for f in sys.argv[2:]:
    for name, P in load(f):
        h = canon(P)
        r = {"id": name, "fp": h, "dup_of_F2": ref.get(h, []), "dup_of_new": list(seen.get(h, []))}
        seen.setdefault(h, []).append(name); res["new"].append(r); print(json.dumps(r), flush=True)
res["n_new_sets"] = len(res["new"]); res["n_new_distinct_not_in_F2"] = len([h for h in seen if h not in ref])
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k.startswith("n_")}))

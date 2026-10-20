#!/usr/bin/env python3
"""Order-type novelty check: canonical forms (chiro.canonical_form: relabelling and reflection) of the
new 32-point sets versus all 8,537 pool sets (inputs/distinct_K7*.txt) and each other.
usage: novelty.py OUT.json new1.pts [new2.pts ...]"""
import glob, hashlib, json, multiprocessing as mp, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
from chiro import canonical_form, chirotope_of  # noqa
def canon(pts):
    return hashlib.sha1(canonical_form(chirotope_of(pts), len(pts)).encode()).hexdigest()
def pool_line(item):
    key, l = item
    t = l.split(); i = t.index("32"); v = list(map(int, t[i + 1:i + 65]))
    return key, canon([(v[2 * k], v[2 * k + 1]) for k in range(32)])
if __name__ == "__main__":
    out = sys.argv[1]
    new = {os.path.basename(f): canon([tuple(map(int, l.split())) for l in open(f) if l.strip()]) for f in sys.argv[2:]}
    lines = []
    for f in sorted(glob.glob(os.path.join(HERE, "..", "..", "..", "inputs", "distinct_K7*.txt"))):
        lines += [(f"{os.path.basename(f)}:{k + 1}", l) for k, l in enumerate(open(f)) if l.strip()]
    with mp.Pool(2) as P:
        pool = dict(P.map(pool_line, lines, chunksize=50))
    inv = {}
    for k, h in pool.items(): inv.setdefault(h, []).append(k)
    res = {"pool_sets": len(pool), "pool_distinct_order_types": len(inv), "new_sets": len(new),
           "new_distinct_order_types": len(set(new.values())),
           "new_matching_pool": {k: inv[h] for k, h in new.items() if h in inv}}
    json.dump(res, open(out, "w"), indent=1); print(json.dumps(res)[:1000])

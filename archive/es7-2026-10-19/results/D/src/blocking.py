#!/usr/bin/env python3
"""How many distinct (K-1)-gons block the m = 1 faces of a saturated set?

For each set: satcount sweep (EMIT=1), then the number of m = 1 faces, the
number of distinct blocking (K-1)-gons, and the share of m = 1 faces blocked by
the most frequent one.  Families:
  k6_null     - hexagon-free 16-point deletions of one-hexagon 17-point sets
                (gen near output files given with --k6 FILES)
  k7_walk     - a random sample of swept walk states (states_w*.txt)
  k7_baseline - a random sample of baseline (gen near) 32-point sets

usage: blocking.py RUNSDIR OUTJSON NSAMPLE [--k6 FILES...]
"""
import os, sys, json, glob, random, collections, statistics
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib, walk

runs, outp, nsamp = sys.argv[1], sys.argv[2], int(sys.argv[3])
k6files = sys.argv[sys.argv.index("--k6") + 1:] if "--k6" in sys.argv else []
NPROC = int(os.environ.get("NPROC", "8"))
rng = random.Random(3)
tmp = os.path.join(runs, "tmp_blocking"); os.makedirs(tmp, exist_ok=True)


def stat(args):
    i, P, K = args
    p = os.path.join(tmp, f"s{i}_{K}.txt"); fp = p + ".faces"
    dlib.write_pts(p, P)
    st = dlib.satcount_sweep(p, K, fp, 1, 3)
    F = [f for f in dlib.read_faces(fp) if f["m"] == 1]
    os.unlink(p); os.unlink(fp)
    c = collections.Counter(tuple(sorted(f["hex"])) for f in F)
    return {"m0": st["m0"], "m1": st["m1"], "distinct_blocking": len(c),
            "top_share": round(c.most_common(1)[0][1] / len(F), 4) if F else None}


def summ(L):
    d = lambda v: None if not v else {"min": min(v), "median": statistics.median(v), "mean": round(statistics.mean(v), 3), "max": max(v)}
    return {"n": len(L), "m0_total": sum(r["m0"] for r in L), "m1": d([r["m1"] for r in L]),
            "distinct_blocking": d([r["distinct_blocking"] for r in L]),
            "distinct_blocking_hist": dict(sorted(collections.Counter(r["distinct_blocking"] for r in L).items())),
            "top_share": d([r["top_share"] for r in L if r["top_share"] is not None])}


fam = {}
jobs = []
k6 = {}
for f in k6files:
    for line in open(f):
        fl = line.split()
        if not fl[0].startswith("ZERO"):
            k6.setdefault(fl[3], dlib.parse_line_pts(fl, 4))
jobs += [("k6_null", (i, P, 6)) for i, P in enumerate(k6.values())]
st = []
for f in glob.glob(os.path.join(runs, "walk", "states_w*.txt")):
    for line in open(f):
        fl = line.split()
        st.append(dlib.parse_line_pts(fl, 4))
rng.shuffle(st)
jobs += [("k7_walk", (100000 + i, P, 7)) for i, P in enumerate(st[:nsamp])]
bs = {}
for f in glob.glob(os.path.join(runs, "baseline", "baseline_b*.txt")):
    for line in open(f):
        fl = line.split()
        if not fl[0].startswith("ZERO"):
            bs.setdefault(fl[3], dlib.parse_line_pts(fl, 4))
bl = list(bs.values()); rng.shuffle(bl)
jobs += [("k7_baseline", (200000 + i, walk.normalize(P), 7)) for i, P in enumerate(bl[:nsamp])]
with ThreadPoolExecutor(NPROC) as ex:
    res = list(ex.map(stat, [j for _, j in jobs]))
out = {}
for name in ("k6_null", "k7_walk", "k7_baseline"):
    L = [r for (n, _), r in zip(jobs, res) if n == name]
    if L:
        out[name] = summ(L)
json.dump(out, open(outp, "w"), indent=1)
print(json.dumps(out, indent=1))

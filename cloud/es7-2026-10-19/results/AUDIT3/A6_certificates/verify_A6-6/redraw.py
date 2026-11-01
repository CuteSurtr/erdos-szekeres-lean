#!/usr/bin/env python3
"""A6-6 check: the procedure found by try_draw.py, written out plainly, plus variants for the extra sample.
Population per case and kind (H/Q): units with a certified record from a cloud machine (source not LOCAL*), one
record per unit (the first in sorted-path scan order), sorted by unit name. Main draw: random.Random(20261101), for
each case P1..P8 sample 2 H then 1 Q; print all H then all Q.
usage: redraw.py RESULTS_DIR"""
import glob, json, os, random, sys

RES = sys.argv[1]
first = {}
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split("/")[-3:-1])
    if "LOCAL" in src:
        continue
    for l in open(f):
        if l.strip():
            r = json.loads(l)
            if r.get("certified") and r["unit"] not in first:
                first[r["unit"]] = (src, r)
cases = [f"P{i}" for i in range(1, 9)]
pop = {(c, k): sorted(u for u, (s, r) in first.items() if r["case"] == c and r["kind"] == k)
       for c in cases for k in ("H", "Q")}
fmt = lambda u: f"{u}@{first[u][0]}"
print("population sizes:", {f"{c}{k}": len(v) for (c, k), v in pop.items()})

rng = random.Random(20261101)
H, Q = [], []
for c in cases:
    H += rng.sample(pop[(c, "H")], 2)
    Q += rng.sample(pop[(c, "Q")], 1)
main = [fmt(u) for u in H + Q]
target = [l.strip() for l in open(os.path.join(RES, "C2FINAL", "sample", "sample.txt")) if l.strip()]
print("main draw reproduces sample.txt exactly:", main == target)
# robustness: does any other small seed near it, or the string seed, give the same list? (it should not)
alt = 0
for sd in [20261100, 20261102, 20261031, "20261101", 1]:
    r2 = random.Random(sd); h, q = [], []
    for c in cases:
        h += r2.sample(pop[(c, "H")], 2); q += r2.sample(pop[(c, "Q")], 1)
    alt += ([fmt(u) for u in h + q] == target)
print("other seeds giving the same list:", alt)

target2 = [l.strip() for l in open(os.path.join(RES, "C2FINAL", "sample", "extra_sample.txt")) if l.strip()]
drawn = set(H + Q)
variants = {}
for excl in ("exclude_main", "no_exclude"):
    for meth in ("sample", "choice"):
        r2 = random.Random(20261102); E = []
        for c in cases:
            L = [u for u in pop[(c, "H")] if excl == "no_exclude" or u not in drawn]
            E += r2.sample(L, 1) if meth == "sample" else [r2.choice(L)]
        variants[(excl, meth)] = [fmt(u) for u in E]
for k, v in variants.items():
    print("extra draw", k, "reproduces extra_sample.txt:", v == target2, f"({sum(a == b for a, b in zip(v, target2))}/8 positional)")

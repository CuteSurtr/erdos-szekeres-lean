#!/usr/bin/env python3
"""Summarize out/w*.log and out/w*.sets; verify sets independently with out/vfy;
write best.txt and analysis.txt.  Usage: analyze.py"""
import collections, glob, os, random, re, subprocess, sys

D = os.path.dirname(os.path.abspath(__file__))
VFY = os.path.join(D, "out", "vfy")
TMP = os.environ.get("TMPDIR", "/tmp")

def vfy(points):
    fn = os.path.join(TMP, "lbs_vfy_%d.txt" % os.getpid())
    with open(fn, "w") as f:
        f.writelines("%d %d\n" % p for p in points)
    out = subprocess.run([VFY, fn], capture_output=True, text=True, check=True).stdout
    first = dict(kv.split("=") for kv in out.split("\n")[0].split())
    gons = [list(map(int, l.split()[1:])) for l in out.splitlines() if l.startswith("7gon:")]
    return {k: int(v) for k, v in first.items()}, gons

runs = []
for fn in sorted(glob.glob(os.path.join(D, "out", "w?.log"))):
    w = fn[-5]
    for line in open(fn):
        if line.startswith("run="):
            d = dict(kv.split("=", 1) for kv in line.split())
            d["worker"] = w
            runs.append(d)
sets = []
for fn in sorted(glob.glob(os.path.join(D, "out", "w?.sets"))):
    for line in open(fn):
        t = line.split()
        meta = dict(kv.split("=") for kv in t[:4])
        pts = [tuple(map(int, s.split(","))) for s in t[4:]]
        sets.append((int(meta["c7"]), int(meta["c6"]), meta["seed"], int(meta["run"]), pts))

out = []
P = out.append
P("runs: %d" % len(runs))
P("best c7 per run: %s" % sorted(collections.Counter(int(r["best"]) for r in runs).items()))
P("final c7 per run (state at end of annealing): %s" %
  sorted(collections.Counter(int(r["final"]) for r in runs).items()))
P("extension minimum (33rd point, 4000 candidates): %s" %
  sorted(collections.Counter(int(r["ext_min"]) for r in runs).items()))
by_walk = collections.defaultdict(list)
for r in runs:
    h = list(map(int, r["ext_hist"].split(",")))
    by_walk[int(r["walk"])].append(h[1] / max(1, int(r["ext_valid"])))
for wl in sorted(by_walk):
    v = by_walk[wl]
    P("walk %6d: %4d runs, mean fraction of valid candidates giving exactly 1 heptagon %.3f" %
      (wl, len(v), sum(v) / len(v)))
for mu in sorted({r["mu"] for r in runs}):
    rr = [r for r in runs if r["mu"] == mu]
    P("mu=%s: %d runs, final c7 = 1 in %d, mean final %.1f" % (
        mu, len(rr), sum(int(r["final"]) == 1 for r in rr),
        sum(int(r["final"]) for r in rr) / len(rr)))
c6s = sorted(s[1] for s in sets if s[0] == 1)
if c6s:
    P("c6 of saved best sets with c7=1: min %d, median %d, max %d (n=%d)" %
      (c6s[0], c6s[len(c6s) // 2], c6s[-1], len(c6s)))

# independent verification
sets.sort(key=lambda s: (s[0], s[1]))
rng = random.Random(1)
check = sets[:10] + rng.sample(sets, min(20, len(sets)))
bad = 0
for c7, c6, seed, run, pts in check:
    v, _ = vfy(pts)
    if v["general_position"] != 1 or v["c7"] != c7 or v["c6"] != c6 or v["n"] != 33:
        bad += 1
        P("MISMATCH seed=%s run=%d lbs c7=%d c6=%d vfy %s" % (seed, run, c7, c6, v))
P("independent check (vfy, brute force + monotone-chain hulls) of %d saved sets: %d mismatches"
  % (len(check), bad))

# near-miss structure of the best sets
P("")
P("ten best sets (fewest 7-gons, then fewest 6-gons):")
for c7, c6, seed, run, pts in sets[:10]:
    v, gons = vfy(pts)
    line = "seed=%s run=%d c5=%d c6=%d c7=%d" % (seed, run, v["c5"], v["c6"], v["c7"])
    for g in gons:
        line += " 7gon=%s contains_point32=%s" % (g, 32 in g)
        sub = [p for i, p in enumerate(pts) if i != g[0]]
        v2, _ = vfy(sub)
        line += " | delete vertex %d: c6=%d c7=%d" % (g[0], v2["c6"], v2["c7"])
    P(line)
c7, c6, seed, run, pts = sets[0]
with open(os.path.join(D, "best.txt"), "w") as f:
    f.write("# %d points, %d convex 7-gons, %d convex 6-gons (worker seed %s, run %s)\n"
            % (len(pts), c7, c6, seed, run))
    f.writelines("%d %d\n" % p for p in pts)
open(os.path.join(D, "analysis.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))

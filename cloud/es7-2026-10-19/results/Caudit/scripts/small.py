#!/usr/bin/env python3
"""Small-n soundness/equivalence test of the full mirror pipeline (gen_etv --mirror [--hull]
+ mirgen.py [--interior --yflip-unit | --hull]) for k = 5, 6, 7.

usage: small.py <bundle_root> <hornchk> <workdir> <N> <k> <nsets> <seed>
For each random mirror set (one axis point): truth = no convex k-gon (independent brute
force on the original coordinates); frame (ii) for interior sets, frame (i) for hull-vertex
sets; "SAT" = hornchk reports no violated clause (exact decision, the aux part is Horn).
Soundness requires truth => SAT for each CNF; we also report SAT => truth (completeness).
"""
import sys, os, json, random, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
from multiprocessing import Pool

root, hk, wd, N, k, n, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
os.makedirs(wd, exist_ok=True)
G = f"{root}/tools/etv/gen_etv.py"; MG = f"{root}/results/C/scripts/mirgen.py"
tag = f"N{N}k{k}"
def sh(*a): subprocess.run(a, check=True, capture_output=True)
c = lambda s: f"{wd}/{s}{tag}.cnf"
sh("python3", G, str(N), str(k), str(k), str(k), "--mirror", "-o", c("m"))
sh("python3", G, str(N), str(k), str(k), str(k), "--mirror", "--hull", "-o", c("hm"))
sh("python3", MG, c("m"), str(N), "--interior", "--yflip-unit", "-o", c("int.sub."))
sh("python3", MG, c("hm"), str(N), "--hull", "-o", c("h.sub."))
npairs = (N - 1) // 2
DIST = ["unif", "top", "bottom", "cluster", "small", "ties", "nearhull"]


def mk(rng, dist):
    R = 40 if dist == "small" else 10**5
    while True:
        if dist == "cluster":
            cs = [(rng.randrange(1, R), rng.randrange(-R, R)) for _ in range(2)]
            pts = [(max(1, cc[0] + rng.randrange(-R // 20, R // 20)), cc[1] + rng.randrange(-R // 20, R // 20)) for cc in (rng.choice(cs) for _ in range(npairs))]
        elif dist == "ties":
            xs = rng.sample(range(1, 100), (npairs + 1) // 2) * 2  # each |x| used at most twice
            pts = [(xs[i], rng.randrange(-R, R)) for i in range(npairs)]
        else:
            pts = [(rng.randrange(1, R), rng.randrange(-R, R)) for _ in range(npairs)]
        ys = [y for _, y in pts]; lo, hi = min(ys), max(ys)
        if dist == "top": y0 = hi + rng.randrange(1, R)
        elif dist == "bottom": y0 = lo - rng.randrange(1, R)
        elif dist == "nearhull": y0 = rng.choice([lo, hi]) + rng.randrange(-max(2, (hi - lo) // 10), max(2, (hi - lo) // 10))
        else: y0 = rng.randrange(lo - (hi - lo) // 3 - 1, hi + (hi - lo) // 3 + 1)
        P = [(x, y) for x, y in pts] + [(-x, y) for x, y in pts] + [(0, y0)]
        if len(set(P)) == len(P) and general_position(P): return P


def work(s):
    rng = random.Random(seed * 7919 + s)
    P = mk(rng, DIST[s % len(DIST)])
    o0 = orient_all(P)
    p = [q for q in P if q[0] == 0][0]
    vertex = P.index(p) in hull_vertices(P)
    for _ in range(6):
        ok = len(set(abs(x) for x, _ in P if x != 0)) == npairs
        if ok and vertex:
            try: frame_i(P)
            except AssertionError: ok = False
        if ok: break
        P2 = sym_perturb(P, rng); assert np.array_equal(orient_all(P2), o0); P = P2
    truth = not has_kgon_brute(P, k)
    if vertex: _, sg = frame_i(P)
    else: _, sg, _ = frame_ii(P)
    return s, vertex, truth, bits(sg), bits(orient_all(sorted(P))), P


with Pool(os.cpu_count()) as pool:
    res = pool.map(work, range(n), chunksize=16)
def chk(cnf, lines):
    if not lines: return {}
    r = subprocess.run([hk, cnf, str(math.comb(N, 3))], input="".join(f"{i} {b}\n" for i, b in lines), capture_output=True, text=True, check=True)
    return {int(l.split()[0]): ("xviol=0" in l.split() and "forbviol=0" in l.split()) for l in r.stdout.split("\n") if l.strip()}
I = [(s, b) for s, v, t, b, bx, P in res if not v]; V = [(s, b) for s, v, t, b, bx, P in res if v]
XS = [(s, bx) for s, v, t, b, bx, P in res]
truth = {s: t for s, v, t, b, bx, P in res}
out = {"N": N, "k": k, "sets": n, "interior": len(I), "vertex": len(V), "kgon_free": sum(truth.values())}
bad = []
for name, cnf, lines in [("int.sub", c("int.sub."), I), ("m(interior sets)", c("m"), [(s, b) for s, b in XS if s in dict(I)]),
                         ("h.sub", c("h.sub."), V), ("hm", c("hm"), V), ("m(all sets, plain x-sort)", c("m"), XS)]:
    r = chk(cnf, lines)
    sound_bad = [s for s in r if truth[s] and not r[s]]
    compl_bad = [s for s in r if r[s] and not truth[s]]
    out[name] = {"checked": len(r), "free": sum(truth[s] for s in r), "unsound(free but UNSAT)": len(sound_bad), "SAT_but_has_kgon": len(compl_bad)}
    bad += [(name, s) for s in sound_bad]
if bad:
    with open(f"{wd}/WITNESS_{tag}.txt", "w") as f:
        for name, s in bad: f.write(f"{name} {s} {res[s][5]}\n")
print(json.dumps(out))

#!/usr/bin/env python3
"""Check the point sets of this folder exactly: central symmetry, general position (no collinear triple), convex layers,
and the number of 7-point and 8-point subsets in convex position, counted by results/SYMMAX/brute.c (an independent
brute force over all subsets). usage: verify_sets.py BRUTE_BINARY FILE..."""
import itertools, subprocess, sys
brute, files = sys.argv[1], sys.argv[2:]
cr = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
def hull(P):
    P = sorted(set(P)); lo, hi = [], []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1] if len(P) > 2 else P
for f in files:
    P = [tuple(map(int, l.split())) for l in open(f) if l.strip() and not l.startswith("#")]
    n = len(P); sym = set(P) == {(-x, -y) for x, y in P}
    col = sum(1 for a, b, c in itertools.combinations(P, 3) if cr(a, b, c) == 0)
    R, lay = list(P), []
    while R:
        H = hull(R); lay.append(len(H)); R = [p for p in R if p not in set(H)]
    table = f"{n}\n" + "\n".join(" ".join(str((cr(P[a], P[b], P[c]) > 0) - (cr(P[a], P[b], P[c]) < 0)) for b in range(n) for c in range(n)) for a in range(n)) + "\n"
    cnt = {k: subprocess.run([brute, str(k)], input=table, capture_output=True, text=True).stdout.strip().split("convex=")[-1] for k in (7, 8)}
    print(f"{f.split('/')[-1]}: n={n} centrally_symmetric={sym} collinear_triples={col} layers={lay} convex_7={cnt[7]} convex_8={cnt[8]}")

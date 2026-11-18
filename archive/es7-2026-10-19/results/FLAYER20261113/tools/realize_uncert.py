"""Realization attempts for abstract no-split configurations that have NO bi-quadratic non-realizability
certificate (records with nonrealizable_certificate = null in <file>_bfp.jsonl).  A success is a REAL point set
in FL(5,5) without a strong split; it is re-verified exactly (orientations, class, brute-force split count).
usage: realize_uncert.py <file_bfp.jsonl> <attempts> <iters> <out.jsonl> [seed]"""
import sys, json, random, itertools
import numpy as np
import realize_small
from esgeo import Analysis
src, attempts, iters, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(int(sys.argv[5]) if len(sys.argv) > 5 else 17)
def count_splits(n, sig):
    T3 = list(itertools.combinations(range(n), 3)); T4 = list(itertools.combinations(range(n), 4))
    sg = {t: (1 if c == '+' else -1) for t, c in zip(T3, sig)}
    caps4 = [t for t in T4 if sg[t[0], t[1], t[2]] < 0 and sg[t[1], t[2], t[3]] < 0]
    cups4 = [t for t in T4 if sg[t[0], t[1], t[2]] > 0 and sg[t[1], t[2], t[3]] > 0]
    caps3 = [t for t in T3 if sg[t] < 0]; cups3 = [t for t in T3 if sg[t] > 0]
    m = lambda s: sum(1 << p for p in s)
    def gons(caps, cups):
        by = {}
        for c in cups: by.setdefault((c[0], c[-1]), []).append(c)
        return [m(set(c) | set(u)) for c in caps for u in by.get((c[0], c[-1]), [])]
    bad1 = set(m(c) for c in caps4) | set(gons(caps3, cups4)); bad2 = set(m(c) for c in cups4) | set(gons(caps4, cups3))
    ALL = np.arange(1 << n, dtype=np.int64); ok = np.ones(1 << n, dtype=bool)
    for x in bad1: ok &= (ALL & x) != x
    comp = ((1 << n) - 1) ^ ALL
    for x in bad2: ok &= (comp & x) != x
    return int(ok.sum())
tot = real = 0
for line in open(src):
    d = json.loads(line)
    if d['nonrealizable_certificate'] is not None: continue
    tot += 1; n, sig = d['n'], d['sig']; P = None
    for a_ in range(attempts):
        P = realize_small.realize(n, sig, rng, iters)
        if P: break
    if P is None: print(f'record {d["record"]}: not realized ({attempts} x {iters})', flush=True); continue
    P = sorted(P); T = list(itertools.combinations(range(n), 3))
    sig2 = ''.join('+' if (P[j][0]-P[i][0])*(P[k][1]-P[i][1]) - (P[j][1]-P[i][1])*(P[k][0]-P[i][0]) > 0 else '-' for i, j, k in T)
    A = Analysis(P); assert sig2 == sig and A.capB.max() <= 4 and A.cupB.max() <= 4 and not ((A.capB >= 4) & (A.cupB >= 4)).any()
    c = count_splits(n, sig2); real += 1
    print(f'record {d["record"]}: REALIZED by points; valid strong splits of the real set: {c}', flush=True)
    with open(out, 'a') as f: f.write(json.dumps({'record': d['record'], 'n': n, 'sig': sig, 'valid_splits': c, 'P': P}) + '\n')
print(f'{real} of {tot} configurations without certificate were realized', flush=True)

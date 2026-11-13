"""Probe a stuck vector with larger supports: greedy growth by forced-triple density (randomised) from face
unions, sizes lo..hi; CaDiCaL on the coupled CNF.  usage: probe_big.py <holes-json> <lo> <hi> <ncand> <procs> <secs>"""
import json, sys, time, random, itertools
from multiprocessing import Pool
import etv_common as ec, coupled5
from cyclists import masks, find_lists
H = json.loads(sys.argv[1]); lo, hi, ncand, procs, secs = map(int, sys.argv[2:7])
occ = [i for i in range(ec.N) if i not in H]
TT = ec.TT
F = (TT | TT.transpose(0, 2, 1))   # forced in some orientation
def dens(S, x):
    return sum(1 for a, b in itertools.combinations(S, 2) if F[a, b, x])
rng = random.Random(int(time.time()))
M = masks(TT)
faces = find_lists(M, occ, 7, limit=3000, rng=rng, per_start=200)
def grow(seed, size):
    S = list(seed)
    while len(S) < size:
        cand = [x for x in occ if x not in S]
        sc = [(dens(S, x) + rng.random() * 3, x) for x in cand]
        sc.sort(reverse=True)
        S.append(sc[rng.randrange(min(3, len(sc)))][1])
    return sorted(S)
cands = set()
while len(cands) < ncand:
    f = rng.choice(faces); g = rng.choice(faces)
    seed = sorted(set(f) | set(g))
    size = rng.randrange(lo, hi + 1)
    if len(seed) > size: seed = rng.sample(seed, size)
    cands.add(tuple(grow(seed, size)))
cands = [list(c) for c in cands]
def test(S):
    t = time.time(); r = coupled5.fast_solve(S, seconds=secs); return S, r, round(time.time() - t, 1)
found = []; stats = {'sat': 0, 'unsat': 0, 'unknown': 0}
with Pool(procs) as P:
    for S, r, t in P.imap_unordered(test, cands):
        stats[r] += 1
        if r == 'unsat':
            found.append(S); print(json.dumps({'event': 'unsat', 'size': len(S), 'support': S, 'secs': t}), flush=True)
print(json.dumps({'faces': len(faces), 'cands': len(cands), 'stats': stats}), flush=True)
json.dump(found, open(f'probe_big_{abs(hash(tuple(H))) % 10**8}.json', 'w'))

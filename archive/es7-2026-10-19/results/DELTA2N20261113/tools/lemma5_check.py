"""Exact check of Lemma 5 (saturated pairs, descent) on the real certificate sets of ETVTHY20261113 (C library esgeo
for capB/cupB; orientation tests in Python).  usage: lemma5_check.py n certfile.jsonl"""
import sys, json
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis, orient
W = '/home/jay/research/data/etvthy-20261113/'
n = int(sys.argv[1]); cache = {}; nsets = npairs = ndesc = nsatdesc = 0
for line in open(sys.argv[2]):
    rec = json.loads(line); fn = rec['file']
    if fn not in cache: cache[fn] = [json.load(open(W + fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(W + fn)]
    P = sorted(tuple(p) for p in cache[fn][rec['index']]); m = len(P); A = Analysis(P); nsets += 1
    # second points x of 4-caps starting at v
    second = {v: set() for v in range(m)}
    for v in range(m):
        for x in range(v + 1, m):
            if A.capS[v, x] >= 4: second[v].add(x)          # longest cap starting with the edge (v, x)
    for u in range(m):
        for v in range(u + 1, m):
            assert A.capB[u, v] + A.cupB[u, v] <= n + 1                                    # Lemma 5 (1)
            if A.capB[u, v] + A.cupB[u, v] != n + 1: continue
            npairs += 1; c = int(A.capB[u, v])
            for x in second[v]:
                ndesc += 1
                assert c >= 3, 'right end of an (n-1)-cup starts a 4-cap'
                assert A.cupB[u, x] >= n + 2 - c, 'the cup part does not extend'
                assert A.capB[u, x] <= c - 1
                if A.capB[u, x] == c - 1:
                    assert A.capB[u, x] + A.cupB[u, x] == n + 1; nsatdesc += 1
                if c == 3: assert A.cupB[u, x] == n - 1
print('%s n=%d: %d sets, %d saturated pairs, %d descents (v starts a 4-cap with second point x), %d of them to a saturated pair (u, x): Lemma 5 holds in all' % (sys.argv[2].split('/')[-1], n, nsets, npairs, ndesc, nsatdesc), flush=True)

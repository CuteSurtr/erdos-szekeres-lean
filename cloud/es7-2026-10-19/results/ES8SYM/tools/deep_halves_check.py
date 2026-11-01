"""For each of the m combinatorially distinct halves H of a centrally symmetric set S, test the 'deep halves' hypothesis:
for all a, b in H, the origin and every point of -H lie strictly on the same side of line ab. Reports, per half, the
number of pairs (a, b) violating it. (proofs/central.md, Lemma 3: if some half is deep, then |S| <= 56.)"""
import sys
from functools import cmp_to_key
from itertools import combinations
def orient(p, q, r): return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
S = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
n = len(S); m = n // 2; O = (0, 0)
hk = lambda p: 0 if (p[1] > 0 or (p[1] == 0 and p[0] > 0)) else 1
ang = sorted(range(n), key=cmp_to_key(lambda i, j: (hk(S[i]) - hk(S[j])) or (-1 if orient(O, S[i], S[j]) > 0 else 1)))
res = []
for start in range(m):
    H = [S[ang[(start + t) % n]] for t in range(m)]
    negH = [(-x, -y) for x, y in H]
    bad = 0
    for a, b in combinations(H, 2):
        so = orient(a, b, O) > 0
        if any((orient(a, b, q) > 0) != so for q in negH): bad += 1
    res.append(bad)
print("violating pairs per half:", res)
print("halves satisfying the deep hypothesis:", sum(1 for r in res if r == 0))

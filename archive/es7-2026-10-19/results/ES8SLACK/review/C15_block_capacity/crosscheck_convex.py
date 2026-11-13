"""Cross-check of convex-position counts with two independent characterizations.

(A) 4-point criterion: every 4-subset convex (no point inside the triangle of the other three,
    chirotope formulas), allowed sign patterns of (s(abc),s(abd),s(acd),s(bcd)) for a<b<c<d are
    ++++, ----, --++, ++-- (convex) ; the four other monotone patterns are non-convex.
(B) cap/cup split: x-sorted subset P = (p0..pk-1); interior points with s(p0,x,pk-1) negative go
    to the upper chain, positive to the lower chain; P is "convex" iff (p0, upper..., pk-1) is a cap
    (all triples negative) and (p0, lower..., pk-1) is a cup (all triples positive).
Counts for k = 4..8 are printed for both; also re-checks the signotope axiom by listing the
patterns of all 4-subsets. Usage: crosscheck_convex.py witness.json
"""
import sys, json, itertools, time
from collections import Counter

t0 = time.time()
w = json.load(open(sys.argv[1]))
n = w['n']
pos = set(map(tuple, w['orientation_positive']))
s = lambda i, j, k: (i, j, k) in pos
pat = Counter()
for q in itertools.combinations(range(n), 4):
    a, b, c, d = q
    pat[''.join('+' if x else '-' for x in (s(a, b, c), s(a, b, d), s(a, c, d), s(b, c, d)))] += 1
monotone = {'++++', '----', '-+++', '--++', '---+', '+---', '++--', '+++-'}
convex_pats = {'++++', '----', '--++', '++--'}
C4 = {}
for q in itertools.combinations(range(n), 4):
    a, b, c, d = q
    C4[q] = ''.join('+' if x else '-' for x in (s(a, b, c), s(a, b, d), s(a, c, d), s(b, c, d))) in convex_pats
def convA(P):
    return all(C4[q] for q in itertools.combinations(P, 4))
def convB(P):
    first, last = P[0], P[-1]
    up = [x for x in P[1:-1] if not s(first, x, last)]
    lo = [x for x in P[1:-1] if s(first, x, last)]
    U = [first] + up + [last]
    L = [first] + lo + [last]
    return all(not s(*t) for t in itertools.combinations(U, 3)) and all(s(*t) for t in itertools.combinations(L, 3))
out = {'patterns': dict(pat), 'all_patterns_monotone': set(pat) <= monotone}
for k in range(4, 9):
    ca = cb = disagree = 0
    for P in itertools.combinations(range(n), k):
        A = convA(P); B = convB(P)
        ca += A; cb += B; disagree += (A != B)
    out[f'k{k}'] = {'convexA': ca, 'convexB': cb, 'disagree': disagree}
out['seconds'] = round(time.time() - t0, 1)
print(json.dumps(out))

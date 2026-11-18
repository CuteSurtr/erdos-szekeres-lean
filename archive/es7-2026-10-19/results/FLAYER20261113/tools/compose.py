"""One-step compositions L (+) R (R to the right of and high above L): README Lemma 5.  Exact check of the
predicted invariants and hole patterns."""
import json, random
import fl, etvcon
from fl import *
from esgeo import quick
def pattern(P):
    S = Set66(P); assert S.ok
    holes = set(range(N)) - set(S.in_state)
    H1 = {i for i, f in enumerate(STATES) if f[0] == 4 and f[3] >= 1}
    H2 = {i for i, f in enumerate(STATES) if f[0] == 4 and f[1] <= 3}
    H3 = {i for i, f in enumerate(STATES) if f[3] == 1}
    nm = [k for k, H in (('H1', H1), ('H2', H2), ('H3', H3)) if H == holes]
    return S.n, (nm[0] if nm else sorted(holes))
out = []
L1 = etvcon.cupcap(4, 6); R1 = etvcon.cupcap(6, 5)     # L: no 4-cup, no 6-cap (15) ; R: no 6-cup, no 5-cap (35)
L2 = etvcon.cupcap(5, 6); R2 = etvcon.cupcap(6, 4)     # L: no 5-cup, no 6-cap (35) ; R: no 6-cup, no 4-cap (15)
print('pieces', len(L1), quick(L1), len(R1), quick(R1), len(L2), quick(L2), len(R2), quick(R2))
def variants(Q):
    yield 'as built', Q
    yield 'x-reversed', sorted((-x, y) for x, y in Q)
for nmL, L in variants(L1):
    for nmR, R in variants(R1):
        P = etvcon.place_high(sorted(L), sorted(R)); n, pat = pattern(P)
        print('type 1 (cup(L)<=3, cap(R)<=4):', nmL, '/', nmR, 'n', n, 'gon/cap/cup', quick(P), 'in-hole pattern', pat)
        out.append({'type': 1, 'L': nmL, 'R': nmR, 'P': sorted(P)})
for nmL, L in variants(L2):
    for nmR, R in variants(R2):
        P = etvcon.place_high(sorted(L), sorted(R)); n, pat = pattern(P)
        print('type 2 (cup(L)<=4, cap(R)<=3):', nmL, '/', nmR, 'n', n, 'gon/cap/cup', quick(P), 'in-hole pattern', pat)
        out.append({'type': 2, 'L': nmL, 'R': nmR, 'P': sorted(P)})
with open('pool_compose.jsonl', 'w') as f:
    for r in out: f.write(json.dumps(r) + '\n')

"""Count A_k = {f4 >= k} and A_k cap F on the pinned 154-state residual catalog; compare with ES / ETV numbers."""
import gzip, hashlib, json, sys
from math import comb
SRC = sys.argv[1]
raw = gzip.decompress(open(SRC, 'rb').read())
h = hashlib.sha256(raw).hexdigest()
print('catalog sha256(raw) =', h, 'pinned match:', h == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6')
CAT = json.loads(raw)
S = CAT['states']
print('states:', len(S), 'rows:', len(CAT['constraints']))
# independent enumeration of (2.1)
enum = []
for f1 in range(7):
    for f2 in range(f1 + 1):
        for f3 in range(f2 + 1):
            for f4 in range(f3 + 1):
                if f1 < 6 or f2 == 6:
                    enum.append((f1, f2, f3, f4))
cat4 = [tuple(s[:4]) for s in S]
print('catalog = enumeration of (2.1):', sorted(cat4) == sorted(enum), 'len enum', len(enum),
      'fifth coord all zero:', all(len(s) == 5 and s[4] == 0 for s in S))
F = {i for i, s in enumerate(cat4) if s[0] >= 5}
Lo = {i for i, s in enumerate(cat4) if s[0] <= 4}
print('|F| =', len(F), '|Lo| =', len(Lo), 'state 0 =', cat4[0])
def es(cup, cap):  # max size with no `cup`-cup and no `cap`-cap (Erdos-Szekeres, exact)
    return comb(cup + cap - 4, cup - 2)
def etv(a, b, n=8):  # ETV value for no a-cap, no b-cup, no n-gon
    return sum(comb(n - 2, i) for i in range(n - b, a - 1))
for k in range(1, 7):
    A = {i for i, s in enumerate(cat4) if s[3] >= k}
    AF = A & F
    cupfree = 8 - k  # owners have no (8-k)-cup
    print(f'k={k}: |A_k|={len(A):3d} (no {cupfree}-cup, no 6-cap: ES {es(cupfree,6):3d}, ETV {etv(6,cupfree):3d}) | '
          f'|A_k & F|={len(AF):3d} (no {cupfree}-cup, no 5-cap: ES {es(cupfree,5):3d}, ETV {etv(5,cupfree):3d}) | '
          f'|A_k & Lo|={len(A & Lo):3d}')

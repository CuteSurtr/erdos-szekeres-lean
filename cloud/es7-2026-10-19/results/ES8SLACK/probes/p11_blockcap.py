"""Probe 11: contextual capacity of a residual block row (abstract relaxation, CNF for CaDiCaL).

Question: can n owners occupy n distinct states of the support S of residual row K?
Variables / constraints (all are necessary conditions for owners in an actual residual configuration):
  * orientation s(i,j,k) for owner indices i<j<k in x-order (true = positive = cup turn), with the
    signotope (monotone 4-sequence) axioms, valid for real points in general position;
  * an injective state map owner -> S (owners have distinct incoming states, Lemma 2.1);
  * for i<j a pair label (a,b) in the residual grid {1..4}x{1..6} minus (1,6), with
    (a,b) in I(state j) \\ I(state i)  (Lemma 2.1, I(f) = {(a,b): b <= f_a});
  * growth: cap triple  => a(i,j) < a(j,k);  cup triple => b(i,j) < b(j,k)  (math.md 2.1);
  * no convex octagon: no cap and cup with common first and last point and 8 vertices in total
    (their union is in convex position for real points);  no 8-cup; no 6-cap.
UNSAT for n means: at most n-1 states of S are occupied in any residual configuration.
Usage: p11_blockcap.py row n out.cnf [--no-octagon]"""
import sys, itertools, json
from common import *

K, n, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
no_oct = '--no-octagon' not in sys.argv
states, rows = load(RES_2650)
S = [tuple(states[i][:4]) for i in rows[K][0]]
cells = [(a, b) for a in range(1, 5) for b in range(1, 7) if (a, b) != (1, 6)]
nv = 0
def new():
    global nv
    nv += 1
    return nv
cls = []
sig = {t: new() for t in itertools.combinations(range(n), 3)}
st = {(p, s): new() for p in range(n) for s in range(len(S))}
lab = {(p, q, c): new() for p, q in itertools.combinations(range(n), 2) for c in range(len(cells))}
A = {(p, q, a): new() for p, q in itertools.combinations(range(n), 2) for a in range(1, 5)}
B = {(p, q, b): new() for p, q in itertools.combinations(range(n), 2) for b in range(1, 7)}

def exactly_one(lits):
    cls.append(list(lits))
    for x, y in itertools.combinations(lits, 2):
        cls.append([-x, -y])

# signotope axioms: sequence s(ijk), s(ijl), s(ikl), s(jkl) monotone
for i, j, k, l in itertools.combinations(range(n), 4):
    seq = [sig[(i, j, k)], sig[(i, j, l)], sig[(i, k, l)], sig[(j, k, l)]]
    for x, y, z in itertools.combinations(range(4), 3):
        cls.append([-seq[x], seq[y], -seq[z]])
        cls.append([seq[x], -seq[y], seq[z]])
# states: exactly one per owner, injective
for p in range(n):
    exactly_one([st[(p, s)] for s in range(len(S))])
for s in range(len(S)):
    for p, q in itertools.combinations(range(n), 2):
        cls.append([-st[(p, s)], -st[(q, s)]])
# labels
for p, q in itertools.combinations(range(n), 2):
    exactly_one([lab[(p, q, c)] for c in range(len(cells))])
    for c, (a, b) in enumerate(cells):
        cls.append([-lab[(p, q, c)], A[(p, q, a)]])
        cls.append([-lab[(p, q, c)], B[(p, q, b)]])
        for s, f in enumerate(S):
            if f[a - 1] >= b:      # (a,b) in I(state p): forbidden
                cls.append([-lab[(p, q, c)], -st[(p, s)]])
            if f[a - 1] < b:       # (a,b) not in I(state q): forbidden
                cls.append([-lab[(p, q, c)], -st[(q, s)]])
    for a in range(1, 5):
        cls.append([-A[(p, q, a)]] + [lab[(p, q, c)] for c, (a2, b2) in enumerate(cells) if a2 == a])
    for b in range(1, 7):
        cls.append([-B[(p, q, b)]] + [lab[(p, q, c)] for c, (a2, b2) in enumerate(cells) if b2 == b])
# growth
for p, q, r in itertools.combinations(range(n), 3):
    s_ = sig[(p, q, r)]
    for a in range(1, 5):
        for a2 in range(1, a + 1):   # cap (s false) needs a(p,q) < a(q,r)
            cls.append([s_, -A[(p, q, a)], -A[(q, r, a2)]])
    for b in range(1, 7):
        for b2 in range(1, b + 1):   # cup (s true) needs b(p,q) < b(q,r)
            cls.append([-s_, -B[(p, q, b)], -B[(q, r, b2)]])
# chains: CP[i,m,j,k]: cap from i with last edge (m,j), length >= k (m=i encodes length 2)
if no_oct:
    CP, CU = {}, {}
    LMAX_CAP, LMAX_CUP = 6, 8
    for i in range(n):
        for j in range(i + 1, n):
            for m in range(i + 1, j):
                for k in range(3, LMAX_CAP + 1):
                    CP[(i, m, j, k)] = new()
                for k in range(3, LMAX_CUP + 1):
                    CU[(i, m, j, k)] = new()
    def cp(i, m, j, k):
        return None if k == 2 else CP.get((i, m, j, k))
    for i in range(n):
        for m in range(i + 1, n):
            for j in range(m + 1, n):
                # extend length-2 edge (i,m) by j
                cls.append([sig[(i, m, j)], CP[(i, m, j, 3)]])
                cls.append([-sig[(i, m, j)], CU[(i, m, j, 3)]])
                for l in range(i + 1, m):
                    for k in range(4, LMAX_CAP + 1):
                        cls.append([-CP[(i, l, m, k - 1)], sig[(l, m, j)], CP[(i, m, j, k)]])
                    for k in range(4, LMAX_CUP + 1):
                        cls.append([-CU[(i, l, m, k - 1)], -sig[(l, m, j)], CU[(i, m, j, k)]])
    CAPANY = {}; CUPANY = {}
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(3, LMAX_CAP + 1):
                CAPANY[(i, j, k)] = new()
                for m in range(i + 1, j):
                    cls.append([-CP[(i, m, j, k)], CAPANY[(i, j, k)]])
            for k in range(3, LMAX_CUP + 1):
                CUPANY[(i, j, k)] = new()
                for m in range(i + 1, j):
                    cls.append([-CU[(i, m, j, k)], CUPANY[(i, j, k)]])
            # octagon: cap length k + cup length k' = 10 (common endpoints); k=2 is the bare edge
            cls.append([-CUPANY[(i, j, 8)]])            # 8-cup (with the edge as cap)
            for k in range(3, LMAX_CAP + 1):
                kk = 10 - k
                if 3 <= kk <= LMAX_CUP:
                    cls.append([-CAPANY[(i, j, k)], -CUPANY[(i, j, kk)]])
            cls.append([-CAPANY[(i, j, 6)]])            # 6-cap (residual)
with open(out, 'w') as f:
    f.write(f'p cnf {nv} {len(cls)}\n')
    for c in cls:
        f.write(' '.join(map(str, c)) + ' 0\n')
print(json.dumps({'row': K, 'n': n, 'support': len(S), 'vars': nv, 'clauses': len(cls), 'octagon': no_oct}))

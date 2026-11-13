#!/usr/bin/env python3
"""Fan monotonicity ("tropical exactness") strengthening of the six-order check.

Exact labels are maxima over actual chains, so for p<q<r (chronological):
  E_+(p,r) >= E_+(p,q) and E_-(p,r) <= E_-(p,q)  if (p,q,r) is a cup,
  E_+(p,r) <= E_+(p,q) and E_-(p,r) >= E_-(p,q)  if (p,q,r) is a cap      (fan at p)
  F_-(p,r) <= F_-(q,r)                            if (p,q,r) is a cup,
  F_-(p,r) >= F_-(q,r)                            if (p,q,r) is a cap      (fan at r)
(proof: replace the last/first vertex of an attaining chain; 4-point transitivity).
Residual labels (a,b) = (6-F_-, E_+-1): cup needs b2>b1, b3>=b1, a3>=a2;
                                          cap needs a2>a1, b3<=b1, a3<=a2.
Balanced labels (a,b) = (E_--1, E_+-1):   cup needs b2>b1, b3>=b1, a3<=a1;
                                          cap needs a2>a1, b3<=b1, a3>=a1.
Here l1=d(p,q), l2=d(q,r), l3=d(p,r), each in its directed difference domain.
"""
import gzip, itertools, json, sys
import numpy as np

ROOT = '/home/jay/research/lean/erdos-szekeres-lean/'

def orset(it):
    m = 0
    for x in set(it):
        m |= x
    return m

def load(kind):
    if kind == 'res':
        d = json.load(gzip.open(ROOT + 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'))
        A, B = 4, 6
    else:
        d = json.load(open(ROOT + 'experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))
        A, B = 5, 5
    return d['states'], d['constraints'], A, B

def cells(s, A):
    return {(a + 1, y) for a in range(A) for y in range(1, s[a] + 1)}

def domains(S, A, B, kind, source_bound=False):
    n = len(S); C = [cells(s, A) for s in S]
    dom = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                dom[i][j] = []; continue
            d = C[j] - C[i]
            if kind == 'res':
                d.discard((1, 6))
            if source_bound:
                d = {z for z in d if z[1] <= S[i][0] + 1}
            dom[i][j] = sorted(d)
    return dom

def tables(S, A, B, kind, fan=True, source_bound=False):
    """cupP[p,q,r], capP[p,q,r]: orientation possible in chronological order p<q<r."""
    n = len(S); dom = domains(S, A, B, kind, source_bound)
    # bit index over (beta, alpha) grid: beta in 1..B (b-values), alpha in 1..A
    def bit(beta, alpha):
        return 1 << ((beta - 1) * A + (alpha - 1))
    full_alpha = lambda beta: orset(bit(beta, al) for al in range(1, A + 1))
    X1cup = np.zeros((n, n), np.int64); M2cup = np.zeros((n, n), np.int64); D3cup = np.zeros((n, n), np.int64)
    X1cap = np.zeros((n, n), np.int64); M2cap = np.zeros((n, n), np.int64); D3cap = np.zeros((n, n), np.int64)
    ne = np.zeros((n, n), bool)
    for i in range(n):
        for j in range(n):
            D = dom[i][j]
            if not D:
                continue
            ne[i, j] = True
            bset = {z[1] for z in D}; aset = {z[0] for z in D}
            if kind == 'res':
                # cup: l1 exact b1=beta; l2: a2=alpha, b2>beta; l3: b3>=beta, a3>=alpha
                X1cup[i, j] = orset(full_alpha(b) for b in bset)
                M2cup[i, j] = orset(bit(be, a) for (a, b) in D for be in range(1, B + 1) if b > be)
                D3cup[i, j] = orset(bit(be, al) for be in range(1, B + 1) for al in range(1, A + 1)
                                  if any(b >= be and a >= al for (a, b) in D)) if fan else (1 << (A * B)) - 1
                # cap: l1: a1<alpha, b1>=beta; l2: a2=alpha; l3: a3<=alpha, b3=beta
                X1cap[i, j] = orset(bit(be, al) for be in range(1, B + 1) for al in range(1, A + 1)
                                  if any(a < al and b >= be for (a, b) in D))
                M2cap[i, j] = orset(bit(be, a) for a in aset for be in range(1, B + 1))
                D3cap[i, j] = orset(bit(b, al) for (a, b) in D for al in range(1, A + 1) if a <= al) if fan else (1 << (A * B)) - 1
                if not fan:
                    X1cap[i, j] = orset(bit(be, al) for be in range(1, B + 1) for al in range(1, A + 1)
                                      if any(a < al for (a, b) in D))
            else:
                # balanced, grid over l1 exact (beta=b1, alpha=a1)
                X1cup[i, j] = orset(bit(b, a) for (a, b) in D)
                X1cap[i, j] = X1cup[i, j]
                M2cup[i, j] = orset(bit(be, al) for be in range(1, B + 1) for al in range(1, A + 1)
                                  if any(b > be for (a, b) in D))
                M2cap[i, j] = orset(bit(be, al) for be in range(1, B + 1) for al in range(1, A + 1)
                                  if any(a > al for (a, b) in D))
                D3cup[i, j] = orset(bit(be, al) for be in range(1, B + 1) for al in range(1, A + 1)
                                  if any(a <= al and b >= be for (a, b) in D)) if fan else (1 << (A * B)) - 1
                D3cap[i, j] = orset(bit(be, al) for be in range(1, B + 1) for al in range(1, A + 1)
                                  if any(a >= al and b <= be for (a, b) in D)) if fan else (1 << (A * B)) - 1
    order_ok = ne[:, :, None] & ne[None, :, :] & ne[:, None, :]
    cupP = ((X1cup[:, :, None] & M2cup[None, :, :] & D3cup[:, None, :]) != 0) & order_ok
    capP = ((X1cap[:, :, None] & M2cap[None, :, :] & D3cap[:, None, :]) != 0) & order_ok
    return cupP, capP, order_ok

def orset(it):
    m = 0
    for x in set(it):
        m |= x
    return m

def parity(q):
    return sum(q[i] > q[j] for i in range(3) for j in range(i + 1, 3)) % 2

def list_table(cupP, capP):
    """T[A,B,C]: list-order triple forced positive in every chronological order."""
    n = cupP.shape[0]
    T = np.ones((n, n, n), bool)
    idx = np.arange(n)
    for perm in itertools.permutations(range(3)):
        odd = parity(perm)
        # chronological (p,q,r) = (g[perm[0]], g[perm[1]], g[perm[2]]) with g=(A,B,C)
        # build arrays indexed [A,B,C]
        axes = [None, None, None]
        # cupP indexed [p,q,r]; transpose to [A,B,C]
        inv = [perm.index(k) for k in range(3)]  # position of list element k in chronological order
        cupT = np.transpose(cupP, inv)
        capT = np.transpose(capP, inv)
        bad = capT if not odd else cupT   # even: positive needed => cap must be impossible
        T &= ~bad
    T[idx, idx, :] = False; T[idx, :, idx] = False; T[:, idx, idx] = False
    return T

if __name__ == '__main__':
    kind = sys.argv[1]
    S, C, A, B = load(kind)
    res = {}
    for fan in [False, True]:
        cupP, capP, ok = tables(S, A, B, kind, fan=fan, source_bound=('sb' in sys.argv))
        T = list_table(cupP, capP)
        res[fan] = T
        print(kind, 'fan' if fan else 'base', 'forced list triples', int(T.sum()),
              'orient-forced chrono', int((ok & ~(cupP & capP)).sum()), 'impossible chrono', int((ok & ~cupP & ~capP).sum()), flush=True)
    np.save(f'T_{kind}_base.npy', res[False]); np.save(f'T_{kind}_fan.npy', res[True])

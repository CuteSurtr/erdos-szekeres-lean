#!/usr/bin/env python3
"""rows-search: capacity rows from the 'chain conditions' (own derivation, see notes in the final report).

Balanced H: no 7-cap, no 7-cup. States f (antitone {0..4}->{0..5}); R_k(f) = #{i : f(i) >= k} = f^T(k-1).

a-cap chain (q1..qa an a-cap of owners), for k = 1..a-1, with j_k = 5 - a + k:
   f_{q_k}(j_k) <= 4   and   f_{q_{k+1}}(k-1) >= f_{q_k}(j_k) + 1.
b-cup chain: the same with f replaced by its transpose f^T.
A class C with no a-cap chain and no b-cup chain (states may repeat in a chain: conservative) has owners with no
a-cap and no b-cup; capacity cap(a,b) = 55 for (6,6) (N66 <= 55, CERTIFIED), else the Erdos-Szekeres cup-cap
number C(a+b-4, a-2) (classical). Row: h(C) >= |C| - cap(a,b).
"""
import json, sys, itertools
from math import comb
import numpy as np, highspy

J = "<repo>/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json"
d = json.load(open(J))
S = [tuple(s) for s in d['states']]; N = len(S)
ROWS = [(r['support'], r['rhs']) for r in d['constraints']]
IDX = {s: i for i, s in enumerate(S)}
tr = lambda f: tuple(sum(1 for x in f if x > j) for j in range(5))
ST = [tr(s) for s in S]
assert S[0] == (0, 0, 0, 0, 0) and S[1] == (1, 0, 0, 0, 0)
Z = [i for i, f in enumerate(S) if f[0] <= 4 and f[4] == 0]
Zs = [i for i, f in enumerate(S) if f[0] == 5 and f[4] >= 1]
assert len(Z) == 70 and len(Zs) == 70


def chain_free_classes(a, F):
    """All maximal classes (as frozensets of state indices) with no a-chain, using vectors F[i] (f or f^T).
    Returns dict frozenset -> parameter tuple."""
    if a >= 7:
        return {frozenset(range(N)): ('all',)}
    out = {}
    jk = lambda k: 5 - a + k  # k = 1..a-1

    def feas(i, k, mprev):
        f = F[i]
        if k >= 2 and not (f[k - 2] >= mprev + 1):
            return False
        if k <= a - 1 and not (f[jk(k)] <= 4):
            return False
        return True

    for k0 in range(1, a + 1):
        for ms in itertools.product(range(5), repeat=k0 - 1):
            C = []
            for i in range(N):
                ok = True
                for k in range(1, k0):
                    mprev = ms[k - 2] if k >= 2 else None
                    if feas(i, k, mprev) and F[i][jk(k)] < ms[k - 1]:
                        ok = False; break
                if ok:
                    mprev = ms[k0 - 2] if k0 >= 2 else None
                    if feas(i, k0, mprev):
                        ok = False
                if ok:
                    C.append(i)
            fs = frozenset(C)
            if fs not in out:
                out[fs] = (k0,) + ms
    # keep only maximal ones (bitset subset test)
    L = sorted(out.items(), key=lambda t: -len(t[0]))
    maxi = []
    for fs, p in L:
        m = 0
        for i in fs: m |= 1 << i
        if not any((m & ~g) == 0 and m != g for g, _, _ in maxi):
            maxi.append((m, fs, p))
    return {fs: p for _, fs, p in maxi}


def lp(rows, fix0=True, obj=None):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    inf = highspy.kHighsInf
    c = np.ones(N) if obj is None else obj
    for j in range(N):
        ub = 0.0 if (fix0 and j in (0, 1)) else 1.0
        h.addVar(0.0, ub); h.changeColCost(j, float(c[j]))
    for sup, rhs in rows:
        idx = np.array(sorted(sup), dtype=np.int32)
        h.addRow(float(rhs), inf, len(idx), idx, np.ones(len(idx)))
    h.run()
    return h.getInfo().objective_function_value, np.array(h.getSolution().col_value)


if __name__ == '__main__':
    base = ROWS + [(Z, 15), (Zs, 15)]
    v0, x0 = lp(ROWS + [(Z, 15)])
    vb, xb = lp(base)
    print('LP catalog+Z (h0=h1=0): %.4f ; catalog+Z+Z*: %.4f' % (v0, vb), flush=True)
    vnf, _ = lp(base, fix0=False)
    print('LP catalog+Z+Z* without h0=h1=0: %.4f' % vnf, flush=True)
    capfam = {}
    for a in range(3, 8):
        capfam[('cap', a)] = chain_free_classes(a, S)
        capfam[('cup', a)] = chain_free_classes(a, ST)
        print('a=%d: %d maximal cap-chain-free classes (max size %d), %d cup-chain-free (max %d)' % (
            a, len(capfam[('cap', a)]), max(len(c) for c in capfam[('cap', a)]),
            len(capfam[('cup', a)]), max(len(c) for c in capfam[('cup', a)])), flush=True)
    # sanity: Z and Z* are 6-cap- and 6-cup-chain-free
    for name, cl in (('Z', Z), ('Z*', Zs)):
        sc = set(cl)
        print(name, 'inside some max 6-cap-free:', any(sc <= c for c in capfam[('cap', 6)]),
              '6-cup-free:', any(sc <= c for c in capfam[('cup', 6)]))
    fams = []
    for a in range(3, 8):
        for b in range(3, 8):
            if a == 7 and b == 7:
                continue
            cap = 55 if (a, b) == (6, 6) else comb(a + b - 4, a - 2)
            A = list(capfam[('cap', a)].items()); B = list(capfam[('cup', b)].items())
            MA = np.zeros((len(A), N)); MB = np.zeros((len(B), N))
            for i, (c, _) in enumerate(A): MA[i, list(c)] = 1
            for i, (c, _) in enumerate(B): MB[i, list(c)] = 1
            fams.append(((a, b), cap, A, B, MA, MB))
    rows = list(base); x = xb; v = vb; added = []
    SIZES = [MA @ MB.T for (ab, cap, A, B, MA, MB) in fams]
    for it in range(60):
        best = None
        for fi, (ab, cap, A, B, MA, MB) in enumerate(fams):
            size = SIZES[fi]
            wt = (MA * x) @ MB.T
            viol = size - cap - wt
            i, j = np.unravel_index(np.argmax(viol), viol.shape)
            if best is None or viol[i, j] > best[0]:
                best = (viol[i, j], ab, cap, A[i], B[j], int(size[i, j]))
        if best[0] <= 1e-7:
            print('no violated chain row; stop', flush=True); break
        vio, ab, cap, (ca, pa), (cb, pb), sz = best
        C = sorted(ca & cb)
        rows.append((C, sz - cap)); added.append({'ab': ab, 'cap': cap, 'size': sz, 'rhs': sz - cap,
                                                    'cap_params': pa, 'cup_params': pb, 'support': C})
        v, x = lp(rows)
        print('it %d: (a,b)=%s cap %d |C| %d rhs %d viol %.3f -> LP %.4f' % (it, ab, cap, sz, sz - cap, vio, v), flush=True)
    json.dump({'base_lp': vb, 'final_lp': v, 'added': added}, open(sys.argv[1], "w"))

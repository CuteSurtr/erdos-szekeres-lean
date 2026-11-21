#!/usr/bin/env python3
"""rows-search: iterated {0,1/2}-CG separation (pairs + triples of tight rows) at the root of catalog + Z + Z*
(h0 = h1 = 0). Every cut is rebuilt with exact integers from its parent rows and re-checked for validity form.
usage: sep_loop.py MAXIT MAXSEC OUT.json"""
import json, sys, time
import numpy as np, highspy
sys.path.insert(0, '<scratch>/agents/rows-search')
import chainrows as cr
N = cr.N
MAXIT, MAXSEC, OUT = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
t0 = time.time()
# rows as (coef dict, rhs): sum coef_s h_s >= rhs, integer data
rows = [({s: 1 for s in sup}, r) for sup, r in cr.ROWS] + [({s: 1 for s in cr.Z}, 15), ({s: 1 for s in cr.Zs}, 15)]
FIX = {0, 1}


def solve(rows):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    inf = highspy.kHighsInf
    for j in range(N):
        h.addVar(0.0, 0.0 if j in FIX else 1.0); h.changeColCost(j, 1.0)
    for co, r in rows:
        idx = np.array(sorted(co), dtype=np.int32); val = np.array([float(co[i]) for i in idx])
        h.addRow(float(r), inf, len(idx), idx, val)
    h.run()
    return h.getInfo().objective_function_value, np.array(h.getSolution().col_value)


def build_cut(parents, x):
    """exact {0,1/2}-CG cut from parent rows (each multiplier 1/2) and bounds; returns (coef, rhs) or None."""
    cov = {}
    B = 0
    for p in parents:
        co, r = rows[p]; B += r
        for s, c in co.items(): cov[s] = cov.get(s, 0) + c
    U = []; coef = {}
    oddS = [s for s, c in cov.items() if c % 2 == 1 and s not in FIX]
    for s, c in cov.items():
        if c % 2 == 0:
            coef[s] = c // 2
        elif s in FIX:
            coef[s] = (c - 1) // 2   # uses h_s <= 0: no rhs change
        elif (1 - x[s]) < x[s]:
            coef[s] = (c - 1) // 2; U.append(s)   # uses h_s <= 1
        else:
            coef[s] = (c + 1) // 2   # uses h_s >= 0
    tot = B - len(U)
    if tot % 2 == 0:
        # flip the cheapest odd state between the two bounds
        if not oddS: return None
        s = min(oddS, key=lambda s: abs(1 - 2 * x[s]))
        c = cov[s]
        if s in U:
            U.remove(s); coef[s] = (c + 1) // 2
        else:
            U.append(s); coef[s] = (c - 1) // 2
        tot = B - len(U)
    assert tot % 2 == 1
    rhs = (tot + 1) // 2
    coef = {s: c for s, c in coef.items() if c != 0}
    return coef, rhs


hist = []
v, x = solve(rows)
print('start LP %.6f' % v, flush=True)
for it in range(MAXIT):
    if time.time() - t0 > MAXSEC: print('time limit'); break
    A = np.zeros((len(rows), N)); b = np.array([r for _, r in rows], dtype=float)
    for i, (co, r) in enumerate(rows):
        for s, c in co.items(): A[i, s] = c
    slack = A @ x - b
    tight = np.where(slack < 1e-7)[0]
    Ai = (A[tight] % 2).astype(np.int16); bt = b[tight].astype(np.int64)
    lo = x.copy(); hi = 1 - x; fr = np.zeros(N, bool); fr[list(FIX)] = True
    found = []
    for ii in range(len(tight)):
        for jj in range(ii + 1, len(tight)):
            cov3 = (Ai[ii] + Ai[jj])[None, :] + Ai[jj + 1:]
            if cov3.shape[0] == 0: continue
            cov3 %= 2
            odd = (cov3 == 1) & ~fr[None, :]
            ch = odd & (hi < lo)[None, :]
            c = np.where(ch, hi[None, :], np.where(odd, lo[None, :], 0)).sum(axis=1)
            par = (bt[ii] + bt[jj] + bt[jj + 1:] + ch.sum(axis=1)) % 2
            flip = np.where(odd, np.abs(hi - lo)[None, :], 9).min(axis=1)
            c = c + np.where(par == 0, flip, 0)
            for k in np.where(c < 1 - 1e-6)[0]:
                found.append((float(c[k]), (int(tight[ii]), int(tight[jj]), int(tight[jj + 1 + k]))))
    if not found:
        print('it %d: no violated triple cut; stop' % it, flush=True); break
    found.sort()
    added = 0; seen = set()
    for c, par in found[:30]:
        cut = build_cut(par, x)
        if cut is None: continue
        co, r = cut
        lhs = sum(cv * x[s] for s, cv in co.items())
        key = (tuple(sorted(co.items())), r)
        if lhs < r - 1e-6 and key not in seen:
            seen.add(key); rows.append((co, r)); added += 1
            hist.append({'parents': par, 'rhs': r, 'coef': {str(s): cv for s, cv in co.items()}, 'viol': r - lhs})
    v, x = solve(rows)
    print('it %d: %d violated triples, added %d cuts -> LP %.6f (%.0fs)' % (it, len(found), added, v, time.time() - t0), flush=True)
json.dump({'final_lp': v, 'cuts': hist}, open(OUT, 'w'))

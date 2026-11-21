#!/usr/bin/env python3
"""rows-search: {0,1/2}-Chvatal-Gomory separation at the root LP optimum of catalog + Z + Z* (h0 = h1 = 0),
plus statistics of the (6,6) chain-free classes and a test of 'witness' implication rows.
A {0,1/2}-cut from rows R (h(S_r) >= b_r), bounds 0 <= h_s <= 1 (h_0 = h_1 = 0) is violated at x iff
 sum_r slack_r + sum_{s odd coverage} cost_s < 1 with odd total rhs parity (cost_s = x_s via h_s >= 0 or 1 - x_s via
 h_s <= 1, the latter flipping parity; states 0, 1 cost 0 without parity change)."""
import json, sys, itertools
import numpy as np
sys.path.insert(0, '<scratch>/agents/rows-search')
import chainrows as cr

N = cr.N; S = cr.S
base = cr.ROWS + [(cr.Z, 15), (cr.Zs, 15)]
v, x = cr.lp(base)
print('root LP %.6f; fractional %d; max x %.3f' % (v, int(((x > 1e-9) & (x < 1 - 1e-9)).sum()), x.max()), flush=True)
A = np.zeros((len(base), N), dtype=np.int8)
b = np.array([r for _, r in base])
for i, (sup, r) in enumerate(base):
    A[i, list(sup)] = 1
slack = A @ x - b
cost_lo = x.copy(); cost_hi = 1 - x
free = np.zeros(N, bool); free[[0, 1]] = True


def cut_violation(rows_idx):
    cov = A[list(rows_idx)].sum(axis=0) % 2
    odd = (cov == 1) & ~free
    par = int(b[list(rows_idx)].sum()) % 2
    c = slack[list(rows_idx)].sum()
    lo = cost_lo[odd]; hi = cost_hi[odd]
    choose_hi = hi < lo
    c += np.where(choose_hi, hi, lo).sum()
    par = (par + int(choose_hi.sum())) % 2
    if par == 0:
        if odd.sum() == 0:
            return None
        c += np.abs(hi - lo).min()
    return c

tight = np.where(slack < 1e-7)[0]
near = np.where(slack < 0.5)[0]
print('rows %d, tight %d, slack<0.5: %d' % (len(base), len(tight), len(near)), flush=True)
best = (9, None)
# singles (rounding of one row with bounds) and pairs among rows with slack < 0.5
for i in near:
    c = cut_violation([i])
    if c is not None and c < best[0]: best = (c, (i,))
W = np.where(A[near].astype(bool), 0, 0)
for ii, i in enumerate(near):
    for j in near[ii + 1:]:
        c = cut_violation([i, j])
        if c is not None and c < best[0]: best = (c, (i, j))
print('best single/pair {0,1/2} total slack %.4f (violated iff < 1) rows %s' % best, flush=True)
# triples among tight rows, vectorized over the third row
At = A[tight].astype(np.int16); bt = b[tight]
bestt = (9, None)
for ii in range(len(tight)):
    for jj in range(ii + 1, len(tight)):
        cov2 = (At[ii] + At[jj])
        cov3 = (cov2[None, :] + At[jj + 1:]) % 2
        if cov3.shape[0] == 0: continue
        odd = (cov3 == 1) & ~free[None, :]
        lo = np.where(odd, cost_lo[None, :], 0); hi = np.where(odd, cost_hi[None, :], 0)
        ch = odd & (cost_hi[None, :] < cost_lo[None, :])
        c = np.where(ch, hi, lo).sum(axis=1)
        par = (bt[ii] + bt[jj] + bt[jj + 1:] + ch.sum(axis=1)) % 2
        flip = np.where(odd, np.abs(cost_hi - cost_lo)[None, :], 9).min(axis=1)
        c = c + np.where(par == 0, flip, 0)
        k = int(np.argmin(c))
        if c[k] < bestt[0]: bestt = (float(c[k]), (tight[ii], tight[jj], tight[jj + 1 + k]))
print('best triple among tight rows: total slack %.4f rows %s' % bestt, flush=True)
json.dump({'lp': v, 'best_pair': [float(best[0]), [int(t) for t in best[1]]],
           'best_triple': [bestt[0], [int(t) for t in bestt[1]] if bestt[1] else None]},
          open(sys.argv[1], 'w'))

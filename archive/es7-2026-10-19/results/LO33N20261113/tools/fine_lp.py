"""Guide LP (floating point; not evidence).  Fine sub-slices of slice t by the nine Baek blocks B_1..B_9
(rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315; each F-state lies in exactly 3 of them, so
sum_j h(B_j) = 3 h(F) = 3t).  A fine sub-slice fixes k_j = h(B_j) >= 6 with sum k_j = 3t.
phi(k) = min h(Lo) s.t. rows, h(B_j) <= k_j (j = 1..9).   Dead at the root iff infeasible or phi > 33 - t."""
import sys, json, itertools, time
import numpy as np, highspy
from lo_common import *
t = int(sys.argv[1])
BL = [973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315]
cert = certified_supports()
h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
L = set(LO)
v = [h.addVariable(lb=0, ub=1, obj=(1.0 if i in L else 0.0)) for i in range(N)]
h.changeColBounds(0, 0, 0)
for j, r in enumerate(BL): h.addConstr(h.qsum(v[i] for i in ROWS[r][0]) <= 6)      # rows 0..8
for s, d in ROWS: h.addConstr(h.qsum(v[i] for i in s) >= d)
for s in cert: h.addConstr(h.qsum(v[i] for i in s) >= 1)
E = 3 * t - 54
def comps(e, parts):
    if parts == 1: yield (e,); return
    for a in range(e + 1):
        for rest in comps(e - a, parts - 1): yield (a,) + rest
res = []; t0 = time.time()
for ex in comps(E, 9):
    for j in range(9): h.changeRowBounds(j, -highspy.kHighsInf, 6.0 + ex[j])
    h.run(); st = h.getModelStatus()
    val = h.getObjectiveValue() if st == highspy.HighsModelStatus.kOptimal else None
    res.append((ex, val))
thr = 33 - t
live = [(ex, val) for ex, val in res if val is not None and val <= thr + 1e-7]
inf = sum(1 for ex, val in res if val is None)
print(json.dumps({'t': t, 'excess': E, 'subslices': len(res), 'infeasible': inf, 'dead_by_phi': len(res) - inf - len(live), 'live': len(live),
                  'seconds': round(time.time() - t0, 1)}))
import collections
hist = collections.Counter(int(np.floor(thr - val)) for ex, val in live)
print('live slack histogram (floor(thr - phi)):', sorted(hist.items()))
live.sort(key=lambda z: z[1])
print('lowest phi:', [(ex, round(val, 3)) for ex, val in live[:8]])
json.dump({'t': t, 'results': [[list(ex), val] for ex, val in res]}, open(f'fine_lp_t{t}.json', 'w'))

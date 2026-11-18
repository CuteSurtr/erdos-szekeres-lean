"""Knuth random-dive estimate for a slice t (rows h(F) >= t, h(Lo) >= 33 - t, budget 33) with a NON-DEGENERATE
branching score.  In a slice the standard LP (min sum h) sits at exactly 33 until the node is infeasible, so the
production strong-branching gains are all zero.  Here the score LP is one of
  lo : phi = min h(Lo)  s.t. rows, bounds, h(F) <= t          (node is dead iff infeasible or phi > 33 - t)
  f  : phi = min h(F)   s.t. rows, bounds, h(Lo) <= 33 - t    (dead iff infeasible or phi > t)
  s  : phi = min s      s.t. rows, bounds, h(F) - s <= t, h(Lo) - s <= 33 - t   (dead iff phi > 0)
All three are equivalent dead-tests to "standard LP > 33" (covering rows are monotone), up to the forced-row test.
Estimator only (HEURISTIC).  Usage: knuth2.py t mode dives seed out.json [K_TOP K_LOW D_TOP]"""
import json, math, os, random, sys, time
import numpy as np, highspy
from lo_common import *
t, mode, dives, seed, out = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
KTOP, KLOW, DTOP = (int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])) if len(sys.argv) > 8 else (16, 4, 8)
BUDGET = 33; rng = random.Random(seed)
cert = certified_supports()
rows = list(ROWS) + [(tuple(F), t), (tuple(LO), BUDGET - t)] + [(tuple(s), 1) for s in cert]
masks = [sum(1 << i for i in s) for s, _ in rows]; dem = [d for _, d in rows]
h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1); h.setOptionValue('presolve', 'off')
Fs, Ls = set(F), set(LO)
if mode == 'lo':
    v = [h.addVariable(lb=0, ub=1, obj=(1.0 if i in Ls else 0.0)) for i in range(N)]
    h.addConstr(h.qsum(v[i] for i in F) <= t); THR = BUDGET - t
elif mode == 'f':
    v = [h.addVariable(lb=0, ub=1, obj=(1.0 if i in Fs else 0.0)) for i in range(N)]
    h.addConstr(h.qsum(v[i] for i in LO) <= BUDGET - t); THR = t
else:
    v = [h.addVariable(lb=0, ub=1, obj=0.0) for i in range(N)]
    s_ = h.addVariable(lb=-100, ub=100, obj=1.0)
    h.addConstr(h.qsum(v[i] for i in F) - s_ <= t); h.addConstr(h.qsum(v[i] for i in LO) - s_ <= BUDGET - t); THR = 0
for s, d in ROWS: h.addConstr(h.qsum(v[i] for i in s) >= d)
for s in cert: h.addConstr(h.qsum(v[i] for i in s) >= 1)
idx = np.arange(N, dtype=np.int32)
OPT, INF = highspy.HighsModelStatus.kOptimal, highspy.HighsModelStatus.kInfeasible
nlp = [0]
def lpsolve(lo, hi):
    nlp[0] += 1
    h.changeColsBounds(N, idx, lo, hi); h.run(); st = h.getModelStatus()
    if st != OPT and st != INF:
        h.clearSolver(); h.run(); st = h.getModelStatus()
    if st == OPT: return h.getObjectiveValue(), np.array(h.getSolution().col_value)[:N]
    return math.inf, None
def expand(missing, occupied, depth):
    if missing.bit_count() > BUDGET: return 'leaf', None
    free = ((1 << N) - 1) ^ missing ^ occupied
    force = None
    for r, mk in enumerate(masks):
        rem = dem[r] - (mk & missing).bit_count(); av = (mk & free).bit_count()
        if rem > av: return 'leaf', None
        if rem and rem == av and force is None:
            a = mk & free; force = (a & -a).bit_length() - 1
    if force is not None: return 'branch', force
    lo = np.array([float(missing >> i & 1) for i in range(N)]); hi = np.array([float(not (occupied >> i & 1)) for i in range(N)])
    obj, x = lpsolve(lo, hi)
    if obj > THR + 1e-7: return 'leaf', None
    fr = [i for i in range(N) if free >> i & 1 and 1e-7 < x[i] < 1 - 1e-7]
    if not fr:
        holes = [i for i in range(N) if x[i] > 0.5]
        if len(holes) <= BUDGET and not check(holes, rows[:len(ROWS)] + rows[len(ROWS) + 2:]) and 0 not in holes: return 'witness', holes
        return 'branch', min(i for i in range(N) if free >> i & 1)
    K = KTOP if depth < DTOP else KLOW
    if K == 0: return 'branch', min(fr, key=lambda i: (abs(x[i] - 0.5), i))
    best = None
    for c in sorted(fr, key=lambda i: (abs(x[i] - 0.5), i))[:K]:
        g = []
        for bv in (0, 1):
            l2, h2 = lo.copy(), hi.copy(); l2[c] = bv; h2[c] = bv
            o2, _ = lpsolve(l2, h2); g.append(max(min(o2, THR + 1) - obj, 1e-3))
        if best is None or g[0] * g[1] > best[0]: best = (g[0] * g[1], c)
    return 'branch', best[1]
ests, depths, witnesses = [], [], []
t0 = time.time()
for dv in range(dives):
    m, o, d, tot, w = 0, 1, 0, 1.0, 1.0
    while True:
        kind, val = expand(m, o, d)
        if kind == 'witness': witnesses.append(val); break
        if kind == 'leaf': break
        if rng.random() < 0.5: o |= 1 << val
        else: m |= 1 << val
        d += 1; w *= 2; tot += w
    ests.append(tot); depths.append(d)
    mu = sum(ests) / len(ests)
    rec = {'slice': t, 'mode': mode, 'dives': dv + 1, 'log10_mean_nodes': round(math.log10(mu), 3),
           'median_depth': sorted(depths)[len(depths) // 2], 'max_depth': max(depths), 'witnesses': len(witnesses),
           'lps': nlp[0], 't': round(time.time() - t0)}
    print(json.dumps(rec), flush=True)
    json.dump({**rec, 'ests': ests, 'depths': depths, 'witness_vectors': witnesses}, open(out, 'w'))

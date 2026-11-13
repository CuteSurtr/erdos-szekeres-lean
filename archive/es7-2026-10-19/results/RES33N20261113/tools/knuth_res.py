"""Knuth random-dive estimate of the LP branch-and-bound tree for the residual budget question
(rule adapted from ES8SLACK/probes/p7_knuth.py, i.e. pbb_strong: forced-row branching, LP leaf test
obj > budget, strong branching on the K most fractional variables).  State 0 is fixed occupied.
Usage: knuth_res.py budget dives seed out.json rows(base|all) [K_TOP K_LOW D_TOP]
A dive that ends in a feasible integer vector reports it as a WITNESS."""
import os, sys, json, math, random, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, highspy
from common import N, ROWS, check
from hfind import load_rows
budget, dives, seed, out, which = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
KTOP, KLOW, DTOP = (int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])) if len(sys.argv) > 8 else (8, 0, 8)
rng = random.Random(seed)
rows = list(ROWS) if which == 'base' else load_rows()
masks = [sum(1 << i for i in s) for s, _ in rows]; dem = [d for _, d in rows]
h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
h.setOptionValue('presolve', 'off')
v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
for s, d in rows: h.addConstr(h.qsum(v[i] for i in s) >= d)
idx = np.arange(N, dtype=np.int32)
OPT, INF = highspy.HighsModelStatus.kOptimal, highspy.HighsModelStatus.kInfeasible
def lpsolve(lo, hi):
    h.changeColsBounds(N, idx, lo, hi); h.run(); st = h.getModelStatus()
    if st != OPT and st != INF:
        h.clearSolver(); h.run(); st = h.getModelStatus()
    if st == OPT: return h.getObjectiveValue(), np.array(h.getSolution().col_value)
    return math.inf, None
def expand(missing, occupied, depth):
    if missing.bit_count() > budget: return 'leaf', None
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
    if obj > budget + 1e-8: return 'leaf', None
    fr = [i for i in range(N) if free >> i & 1 and 1e-7 < x[i] < 1 - 1e-7]
    if not fr:
        holes = [i for i in range(N) if x[i] > 0.5]
        if len(holes) <= budget and not check(holes, rows) and 0 not in holes: return 'witness', holes
        return 'branch', min(i for i in range(N) if free >> i & 1)
    K = KTOP if depth < DTOP else KLOW
    if K == 0: return 'branch', min(fr, key=lambda i: (abs(x[i] - 0.5), i))
    best = None
    for c in sorted(fr, key=lambda i: (abs(x[i] - 0.5), i))[:K]:
        g = []
        for bv in (0, 1):
            l2, h2 = lo.copy(), hi.copy(); l2[c] = bv; h2[c] = bv
            o2, _ = lpsolve(l2, h2); g.append(max(min(o2, budget + 1) - obj, 1e-3))
        if best is None or g[0] * g[1] > best[0]: best = (g[0] * g[1], c)
    return 'branch', best[1]
ests, depths, witnesses = [], [], []
t0 = time.time()
for dv in range(dives):
    m, o, d, tot, w = 0, 1, 0, 1.0, 1.0   # bit 0 occupied (state 0)
    while True:
        kind, val = expand(m, o, d)
        if kind == 'witness': witnesses.append(val); break
        if kind == 'leaf': break
        if rng.random() < 0.5: o |= 1 << val
        else: m |= 1 << val
        d += 1; w *= 2; tot += w
    ests.append(tot); depths.append(d)
    mu = sum(ests) / len(ests)
    rec = {'budget': budget, 'rows': which, 'dives': dv + 1, 'log10_mean_nodes': round(math.log10(mu), 3),
           'median_depth': sorted(depths)[len(depths) // 2], 'max_depth': max(depths), 'witnesses': len(witnesses),
           't': round(time.time() - t0)}
    print(json.dumps(rec), flush=True)
    json.dump({**rec, 'ests': ests, 'depths': depths, 'witness_vectors': witnesses}, open(out, 'w'))

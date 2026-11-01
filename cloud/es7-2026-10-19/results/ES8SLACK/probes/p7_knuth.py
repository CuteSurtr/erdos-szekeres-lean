"""Probe 7: Knuth (random-dive) estimate of the size of the exact LP branch-and-bound tree used for the
311 certificate (rule of experiments/omission-final311-2026-10-14/search/pbb_strong.py: forced-row
branching, LP leaf test obj > budget, strong branching K_TOP=40 above depth 12, K_LOW=12 below).
E[sum_d 2^d] over random root-to-leaf dives is an unbiased estimate of the node count.
Usage: p7_knuth.py budget dives seed out.json [ktop klow dtop] [fix_occupied comma list]"""
import os, sys, json, math, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, highspy
from common import *

budget, dives, seed, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
KTOP, KLOW, DTOP = (int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else (40, 12, 12)
FIX = [int(x) for x in sys.argv[8].split(',')] if len(sys.argv) > 8 and sys.argv[8] else []
rng = random.Random(seed)
states, rows = load(BAL_V2)
N = len(states)
masks = [sum(1 << i for i in s) for s, _ in rows]
dem = [d for _, d in rows]
h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
h.setOptionValue('presolve', 'off')
v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
for s, d in rows:
    h.addConstr(h.qsum(v[i] for i in s) >= d)
import os
if os.environ.get('EARLY23'):
    h.addConstr(v[2] + v[3] <= 1)   # third vertex: one of states 2,3 occupied (balanced, n>=3)
idx = np.arange(N, dtype=np.int32)
OPT, INF = highspy.HighsModelStatus.kOptimal, highspy.HighsModelStatus.kInfeasible


def lpsolve(lo, hi):
    h.changeColsBounds(N, idx, lo, hi); h.run(); st = h.getModelStatus()
    if st != OPT and st != INF:
        h.clearSolver(); h.run(); st = h.getModelStatus()
    if st == OPT:
        return h.getObjectiveValue(), np.array(h.getSolution().col_value)
    return math.inf, None


def expand(missing, occupied, depth):
    """('leaf',None) | ('branch',var) | ('witness',holes)"""
    if missing.bit_count() > budget:
        return 'leaf', None
    free = ((1 << N) - 1) ^ missing ^ occupied
    force = None
    for r, mk in enumerate(masks):
        rem = dem[r] - (mk & missing).bit_count()
        av = (mk & free).bit_count()
        if rem > av:
            return 'leaf', None
        if rem and rem == av and force is None:
            a = mk & free; force = (a & -a).bit_length() - 1
    if force is not None:
        return 'branch', force
    lo = np.array([float(missing >> i & 1) for i in range(N)])
    hi = np.array([float(not (occupied >> i & 1)) for i in range(N)])
    obj, x = lpsolve(lo, hi)
    if obj > budget + 1e-8:
        return 'leaf', None
    fr = [i for i in range(N) if free >> i & 1 and 1e-7 < x[i] < 1 - 1e-7]
    if not fr:
        holes = [i for i in range(N) if x[i] > 0.5]
        if len(holes) <= budget and not check_exact(rows, holes) and not (os.environ.get('EARLY23') and 2 in holes and 3 in holes):
            return 'witness', holes
        return 'branch', min(i for i in range(N) if free >> i & 1)
    K = KTOP if depth < DTOP else KLOW
    if K == 0:
        return 'branch', min(fr, key=lambda i: (abs(x[i] - 0.5), i))
    cand = sorted(fr, key=lambda i: (abs(x[i] - 0.5), i))[:K]
    best = None
    for c in cand:
        g = []
        for bv in (0, 1):
            l2, h2 = lo.copy(), hi.copy(); l2[c] = bv; h2[c] = bv
            o2, _ = lpsolve(l2, h2)
            g.append(max(min(o2, budget + 1) - obj, 1e-3))
        key = g[0] * g[1]
        if best is None or key > best[0]:
            best = (key, c)
    return 'branch', best[1]


ests, depths = [], []
t0 = time.time()
occ0 = sum(1 << i for i in FIX)
for dv in range(dives):
    m, o, d, tot, w = 0, occ0, 0, 1.0, 1.0
    while True:
        kind, val = expand(m, o, d)
        if kind == 'witness':
            print(json.dumps({'WITNESS': val})); json.dump({'WITNESS': val}, open(out, 'w')); sys.exit(0)
        if kind == 'leaf':
            break
        if rng.random() < 0.5:
            o |= 1 << val
        else:
            m |= 1 << val
        d += 1; w *= 2; tot += w
    ests.append(tot); depths.append(d)
    if (dv + 1) % 10 == 0:
        mu = sum(ests) / len(ests)
        print(json.dumps({'budget': budget, 'dives': dv + 1, 'mean': round(mu), 'log10': round(math.log10(mu), 3),
                          'median_depth': sorted(depths)[len(depths) // 2], 'max_depth': max(depths),
                          't': round(time.time() - t0)}), flush=True)
mu = sum(ests) / len(ests)
sd = (sum((e - mu) ** 2 for e in ests) / max(1, len(ests) - 1)) ** 0.5
json.dump({'budget': budget, 'dives': len(ests), 'mean': mu, 'stderr': sd / len(ests) ** 0.5,
           'depths': depths, 'ests': ests, 'rule': [KTOP, KLOW, DTOP], 'fix_occupied': FIX,
           'seconds': time.time() - t0}, open(out, 'w'))

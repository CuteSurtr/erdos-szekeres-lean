"""Probe 12: can local rank-1 projection cuts (rounded cover cuts valid under a node's fixings) close
budget-64 B&B nodes earlier?  Sample nodes at a given depth on random most-fractional dives,
run a few rounds of local separation, report LP before/after vs the budget.
Usage: p12_localcuts.py budget depth nodes seed secs_per_node out.json"""
import os, sys, json, math, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, highspy
from common import *

budget, depth, nodes, seed, per, out = (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
                                        float(sys.argv[5]), sys.argv[6])
rng = random.Random(seed)
states, rows = load(BAL_V2)
N = len(states)
inc = [[] for _ in range(N)]
for k, (s, d) in enumerate(rows[:2685]):
    for i in s: inc[i].append(k)


def build():
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
    for s, d in rows:
        h.addConstr(h.qsum(v[i] for i in s) >= d)
    return h, v


h, v = build()
idx = np.arange(N, dtype=np.int32); ones = np.ones(N)


def lp(lo, hi, c=None):
    h.changeColsCost(N, idx, ones if c is None else c)
    h.changeColsBounds(N, idx, lo, hi); h.run()
    if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
        return math.inf, None
    return h.getObjectiveValue(), np.array(h.getSolution().col_value)


res = []
t0 = time.time()
while len(res) < nodes:
    lo = np.zeros(N); hi = np.ones(N); d = 0; ok = True
    while d < depth:
        obj, x = lp(lo, hi)
        if obj > budget + 1e-8 or lo.sum() > budget:
            ok = False; break
        fr = [i for i in range(N) if lo[i] != hi[i] and 1e-7 < x[i] < 1 - 1e-7]
        if not fr:
            ok = False; break
        i = min(fr, key=lambda i: abs(x[i] - .5))
        b = rng.randint(0, 1); lo[i] = b; hi[i] = b; d += 1
    if not ok:
        continue
    obj0, x = lp(lo, hi)
    if obj0 > budget:
        continue
    # local separation (cuts kept only in a fresh copy for this node)
    hn, vn = build()
    def lpn(c=None):
        hn.changeColsCost(N, idx, ones if c is None else c); hn.changeColsBounds(N, idx, lo, hi); hn.run()
        return hn.getObjectiveValue(), np.array(hn.getSolution().col_value)
    g, x = lpn(); ncut = 0; tn = time.time()
    while time.time() - tn < per and g <= budget + 1e-8:
        frac = [i for i in range(N) if lo[i] != hi[i] and 1e-6 < x[i] < 1 - 1e-6]
        found = []
        for _ in range(60):
            r = rng.random()
            if r < 0.5:
                i0 = rng.choice(frac) if frac else rng.randrange(N)
                ks = rng.sample(inc[i0], min(len(inc[i0]), rng.choice([2, 3, 4])))
                S = sorted(set().union(*[rows[k][0] for k in ks]))
            else:
                if len(frac) < 4: continue
                S = sorted(rng.sample(frac, rng.randint(4, min(40, len(frac)))))
            c = np.zeros(N); c[S] = 1
            val, _ = lpn(c); xs = x[S].sum(); k = math.ceil(val - 1e-7)
            if k > xs + 1e-6:
                found.append((k - xs, S, k))
        found.sort(key=lambda t: -t[0])
        for viol, S, k in found[:5]:
            hn.addConstr(hn.qsum(vn[i] for i in S) >= k); ncut += 1
        g, x = lpn()
        if not found:
            break
    res.append({'lp_before': round(obj0, 4), 'lp_after': round(g, 4), 'cuts': ncut, 'closed': g > budget + 1e-8,
                'fixed_missing': int(lo.sum()), 'secs': round(time.time() - tn, 1)})
    print(json.dumps(res[-1]), flush=True)
json.dump({'budget': budget, 'depth': depth, 'nodes': res, 'closed': sum(r['closed'] for r in res)}, open(out, 'w'))
print('closed', sum(r['closed'] for r in res), 'of', len(res), 'total secs', round(time.time() - t0))

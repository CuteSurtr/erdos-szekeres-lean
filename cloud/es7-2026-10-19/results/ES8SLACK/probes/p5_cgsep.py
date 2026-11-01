"""Probe 5: rank-1 projection-cut separation (= rounded cover cuts, math.md (3.2)) on the balanced V2 LP.
A cut h(T) >= ceil(min_LP h(T)) is valid for Boolean points and is exactly a rounded cover cut whose
weights are the LP duals of min h(T).  Question: does the global LP bound (55) move?
Usage: p5_cgsep.py seed seconds out.json"""
import os, sys, json, math, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, highspy
from common import *

seed, secs, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
rng = random.Random(seed)
states, rows = load(BAL_V2)
n = len(states)
h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(n)]
for s, d in rows:
    h.addConstr(h.qsum(v[i] for i in s) >= d)
idx = np.arange(n, dtype=np.int32)
ones = np.ones(n)


def glob():
    h.changeColsCost(n, idx, ones); h.run()
    return h.getObjectiveValue(), np.array(h.getSolution().col_value)


def vmin(S):
    c = np.zeros(n); c[S] = 1
    h.changeColsCost(n, idx, c); h.run()
    return h.getObjectiveValue()


rowsets = [s for s, _ in rows[:2685]]
inc = [[] for _ in range(n)]
for k, s in enumerate(rowsets):
    for i in s: inc[i].append(k)
cuts = []; t0 = time.time(); log = []
rd = 0
while time.time() - t0 < secs:
    g, x = glob()
    frac = [i for i in range(n) if 1e-6 < x[i] < 1 - 1e-6]
    found = []; tries = 0
    while tries < 300 and len(found) < 12 and time.time() - t0 < secs:
        tries += 1
        mode = rng.random()
        if mode < 0.35:  # union of 2-4 rows sharing a common state
            i0 = rng.randrange(n)
            if not inc[i0]: continue
            ks = rng.sample(inc[i0], min(len(inc[i0]), rng.choice([2, 3, 4])))
            S = sorted(set().union(*[rowsets[k] for k in ks]))
        elif mode < 0.6:  # star: all states of rows through one state
            i0 = rng.choice(frac) if frac else rng.randrange(n)
            S = sorted(set().union(*[rowsets[k] for k in inc[i0]]))
            if len(S) > 80: S = sorted(rng.sample(S, 80))
        elif mode < 0.8:  # low-x states
            m = rng.randint(10, 80)
            S = sorted(rng.sample(sorted(range(n), key=lambda i: x[i])[:120], m))
        else:  # random fractional subset
            if len(frac) < 6: continue
            S = sorted(rng.sample(frac, rng.randint(6, min(60, len(frac)))))
        if len(S) < 3: continue
        val = vmin(S); xs = x[S].sum(); k = math.ceil(val - 1e-7)
        if k > xs + 1e-6:
            found.append((k - xs, S, k))
    found.sort(key=lambda t: -t[0])
    for viol, S, k in found[:6]:
        cuts.append({'support': S, 'rhs': k}); h.addConstr(h.qsum(v[i] for i in S) >= k)
    g2, _ = glob()
    rec = {'round': rd, 'global_before': round(g, 5), 'global_after': round(g2, 5), 'found': len(found),
           'cuts': len(cuts), 't': round(time.time() - t0)}
    log.append(rec); print(json.dumps(rec), flush=True)
    rd += 1
json.dump({'log': log, 'cuts': cuts}, open(out, 'w'))

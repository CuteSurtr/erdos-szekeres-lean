"""Probe 6: large-neighbourhood search for low-hole Boolean assignments of a hole system.
Free a structured random subset of variables, keep the rest at the incumbent, re-optimise exactly
with HiGHS (scipy.milp).  Accept equal-or-better solutions (plateau moves).
Usage: p6_lns.py {bal|res} seconds start.json seed out.json [free_size]"""
import sys, time, json, random
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from common import *

which, secs, start, seed, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5]
K = int(sys.argv[6]) if len(sys.argv) > 6 else 90
rng = random.Random(seed)
states, rows = load(BAL_V2 if which == 'bal' else RES_2650)
n = len(states)
A, b = matrix(n, rows)
cons = LinearConstraint(A, b, np.inf)
cur = set(json.load(open(start))['holes'])
assert not check_exact(rows, sorted(cur))
inc = [[] for _ in range(n)]
for k, (s, d) in enumerate(rows):
    for i in s: inc[i].append(k)
best = sorted(cur); t0 = time.time(); it = 0; hist = []
fixed0 = [0] if which == 'res' else []
while time.time() - t0 < secs:
    it += 1
    # neighbourhood: a few random rows' supports + random holes + random states
    F = set()
    while len(F) < K:
        r = rng.random()
        if r < 0.5:
            s, _ = rows[rng.randrange(len(rows))]; F |= set(s)
        elif r < 0.8 and cur:
            F.add(rng.choice(sorted(cur)))
        else:
            F.add(rng.randrange(n))
    lb = np.zeros(n); ub = np.ones(n)
    for i in range(n):
        if i not in F:
            lb[i] = ub[i] = 1.0 if i in cur else 0.0
    for i in fixed0:
        ub[i] = 0.0
    res = milp(np.ones(n), integrality=np.ones(n), bounds=Bounds(lb, ub), constraints=[cons],
               options={'time_limit': 10, 'disp': False})
    if res.x is None:
        continue
    new = {i for i in range(n) if res.x[i] > 0.5}
    if len(new) <= len(cur) and not check_exact(rows, sorted(new)):
        if len(new) < len(cur):
            hist.append({'it': it, 't': round(time.time() - t0, 1), 'holes': len(new)})
            print(json.dumps(hist[-1]), flush=True)
        cur = new
        if len(cur) < len(best):
            best = sorted(cur)
json.dump({'which': which, 'best_holes': len(best), 'holes': best, 'iterations': it, 'history': hist,
           'violated_exact': check_exact(rows, best)}, open(out, 'w'))
print('best', len(best), 'iterations', it)

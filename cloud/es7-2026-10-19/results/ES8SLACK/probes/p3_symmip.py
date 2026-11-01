"""Probe 3: min holes over assignments invariant under a symmetry subgroup of the balanced catalog.
Any feasible invariant assignment is in particular feasible, so this gives upper bounds on min holes.
Usage: p3_symmip.py {G|T|C|TC} seconds"""
import sys, time, json
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
from common import *
from sym import perms

grp, secs = sys.argv[1], float(sys.argv[2])
states, rows = load(BAL_V2)
n = len(states)
T, C = perms(states)
TC = [C[T[i]] for i in range(n)]
gens = {'G': [T, C], 'T': [T], 'C': [C], 'TC': [TC]}[grp]
# orbits
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
for p in gens:
    for i in range(n):
        a, b = find(i), find(p[i])
        if a != b: parent[a] = b
reps = sorted({find(i) for i in range(n)})
oid = {r: k for k, r in enumerate(reps)}
m = len(reps)
size = np.zeros(m)
for i in range(n): size[oid[find(i)]] += 1
# rows in orbit variables (dedupe)
seen = {}
for s, d in rows:
    cnt = {}
    for i in s:
        o = oid[find(i)]; cnt[o] = cnt.get(o, 0) + 1
    key = tuple(sorted(cnt.items()))
    seen[key] = max(seen.get(key, 0), d)
data, ind, ptr, rhs = [], [], [0], []
for key, d in seen.items():
    for o, c in key:
        ind.append(o); data.append(float(c))
    ptr.append(len(ind)); rhs.append(d)
A = csr_matrix((data, ind, ptr), shape=(len(rhs), m))
t = time.time()
res = milp(size, integrality=np.ones(m), bounds=Bounds(np.zeros(m), np.ones(m)),
           constraints=[LinearConstraint(A, np.array(rhs, float), np.inf)],
           options={'time_limit': secs, 'disp': False, 'mip_rel_gap': 0})
out = {'group': grp, 'orbits': m, 'status': int(res.status), 'message': res.message,
       'seconds': round(time.time() - t, 1), 'dual_bound': getattr(res, 'mip_dual_bound', None)}
if res.x is not None:
    holes = sorted(i for i in range(n) if res.x[oid[find(i)]] > 0.5)
    out.update(num_holes=len(holes), holes=holes, violated_exact=check_exact(rows, holes),
               violated_exact_base=check_exact(rows[:2685], holes))
print(json.dumps(out))

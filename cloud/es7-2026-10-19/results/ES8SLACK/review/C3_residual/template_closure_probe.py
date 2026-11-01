#!/usr/bin/env python3
"""Exploratory probe (computational evidence only): enumerate instances of the existing coupled
templates over all 154 states (time-limited per template), add the new demand-one supports to the
2,650 catalog rows, and ask HiGHS (scipy.optimize.milp) for a 0/1 vector with h_0 = 0, at most 33
holes, satisfying the extended system.  Every returned vector is re-checked with exact integer
arithmetic.  A time-out decides nothing.
Usage: <python with numpy and scipy> -I template_closure_probe.py [seconds_per_template] [milp_seconds]
"""
import gzip, hashlib, json, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

sys.argv += []
T_LIMIT = float(sys.argv[1]) if len(sys.argv) > 1 else 90.0
M_LIMIT = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location('ti', HERE + '/template_search_lib.py')
ti = importlib.util.module_from_spec(spec); spec.loader.exec_module(ti)

cat = ti.cat
rows = [(frozenset(r['support']), int(r['rhs'])) for r in cat['constraints']]
catalog_supports = {s for s, d in rows if d >= 1}
out = {'templates': {}}
new_supports = set()
for name, (k, crit) in ti.TPL.items():
    res = ti.search(k, crit, list(range(154)), T_LIMIT, stop_after=None, keep_all=True)
    sups = {frozenset(s) for s in res['supports']}
    fresh = sups - catalog_supports
    # drop supports implied by a single demand-one catalog row contained in them
    new_supports |= fresh
    out['templates'][name] = {'complete': res['complete'], 'maps': res['maps'], 'distinct_supports': len(sups),
                              'not_in_catalog': len(fresh), 'seconds': res['seconds']}
    print(name, out['templates'][name], file=sys.stderr, flush=True)
out['new_supports_total'] = len(new_supports)
ext = rows + [(s, 1) for s in sorted(new_supports, key=sorted)]
W = json.load(open(TOP + '/witnesses.json'))['residual_2650_33_hole_witnesses_state0_occupied']
out['witnesses_violating_extended'] = [sum(1 for s, d in ext if len(s & set(h)) < d) for h in W]

# MIP feasibility: sum h <= 33, h0 = 0, rows
n = 154
A = lil_matrix((len(ext) + 1, n))
lo = np.zeros(len(ext) + 1); hi = np.full(len(ext) + 1, np.inf)
for r, (s, d) in enumerate(ext):
    for i in s:
        A[r, i] = 1
    lo[r] = d
A[len(ext), :] = 1
lo[len(ext)] = 0; hi[len(ext)] = 33
lb = np.zeros(n); ub = np.ones(n); ub[0] = 0
t0 = time.time()
res = milp(c=np.ones(n), constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(n),
           bounds=Bounds(lb, ub), options={'time_limit': M_LIMIT, 'disp': False})
out['milp'] = {'status': int(res.status), 'message': str(res.message), 'seconds': round(time.time() - t0, 1)}
if res.x is not None:
    h = [i for i in range(n) if res.x[i] > 0.5]
    ok = (0 not in h) and all(len(s & set(h)) >= d for s, d in ext)
    out['milp'].update({'holes': h, 'num_holes': len(h), 'exact_recheck_all_extended_rows': ok,
                        'objective_bound': getattr(res, 'mip_dual_bound', None)})
print(json.dumps(out, indent=1))
json.dump(out, open(HERE + '/template_closure_probe_out.json', 'w'), indent=1)

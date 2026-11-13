"""Final statistics + exact check that the last 18-hole vector satisfies every current row (so the minimum
over the final row set is exactly 18, given the certified lower bound)."""
import json, collections
import rowsio, etv_common as ec
rows = rowsio.load_all()
kinds = collections.Counter(k for d, k in rows.values())
V = [json.loads(l) for l in open('vectors.jsonl')]
cores = [json.loads(l) for l in open('cores.jsonl')]
tpl = sum(1 for _ in open('templates.jsonl'))
print(json.dumps({'rows': len(rows), 'kinds': kinds, 'vectors_probed': len(V), 'by_holes': collections.Counter(len(v['holes']) for v in V),
                  'cores': len(cores), 'core_sizes': collections.Counter(len(c['support']) for c in cores), 'templates': tpl}))
masks = [(sum(1 << i for i in s), d) for s, (d, k) in rows.items()]
for v in reversed(V):
    H = v['holes']; hm = sum(1 << i for i in H)
    viol = sum(1 for m, d in masks if (m & hm).bit_count() < d)
    if not viol and not (set(H) & set(ec.FIXED_OCC)):
        print(json.dumps({'last_unrefuted_vector': H, 'holes': len(H), 'violated_rows': 0, 'recorded_at': v['t']})); break
else:
    print('every recorded vector violates some row')
# fresh feasibility solve at 18 over the final rows (search only; the vector is re-checked exactly)
from ortools.sat.python import cp_model
m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(ec.N)]
for i in ec.FIXED_OCC: m.Add(h[i] == 0)
for s, (d, k) in rows.items(): m.Add(sum(h[i] for i in s) >= d)
m.Add(sum(h) <= 18)
so = cp_model.CpSolver(); so.parameters.num_workers = 4; so.parameters.max_time_in_seconds = 120
st = so.Solve(m)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    H = [i for i in range(ec.N) if so.Value(h[i])]; hm = sum(1 << i for i in H)
    viol = sum(1 for mm, d in masks if (mm & hm).bit_count() < d)
    print(json.dumps({'fresh_vector': H, 'holes': len(H), 'violated_rows_exact_check': viol, 'states': [ec.STATES[i] for i in H]}))
else:
    print(json.dumps({'fresh_solve_status': so.StatusName(st)}))

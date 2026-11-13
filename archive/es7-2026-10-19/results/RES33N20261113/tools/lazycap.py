"""Lazy row generation for: 2,650 rows + capacity h(F) >= 84 - c + h0 = 0 + sum h <= 33.
Repeatedly solve with HiGHS (first feasible point); add the new rows (templates + newrows, all valid)
that the point violates; stop when HiGHS proves infeasibility (=> with capacity c the valid rows force
>= 34 residual holes) or when a point satisfies every row (=> a genuine 33-hole vector for the loop)."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import highspy
from common import N, STATES, ROWS, check
from hfind import load_rows
c = int(sys.argv[1]); DL = float(sys.argv[2])
F = [i for i in range(N) if STATES[i][0] >= 5]
allrows = load_rows(); pool = allrows[len(ROWS):]
masks = [(sum(1 << i for i in s), d, s) for s, d in pool]
active = []
log = open(os.path.join(HERE, f'lazycap_{c}.jsonl'), 'a')
it = 0
while time.time() < DL - 30:
    it += 1
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    h.setOptionValue('time_limit', max(10.0, DL - time.time() - 20)); h.setOptionValue('mip_max_improving_sols', 1)
    v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
    h.changeColBounds(0, 0, 0)
    for i in range(N): h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
    for s, d in list(ROWS) + active: h.addConstr(h.qsum(v[i] for i in s) >= d)
    h.addConstr(h.qsum(v[i] for i in F) >= 84 - c)
    h.addConstr(h.qsum(v) <= 33)
    t = time.time(); h.run(); st = h.modelStatusToString(h.getModelStatus())
    rec = {'t': time.strftime('%H:%M:%S'), 'it': it, 'active': len(active), 'status': st, 'seconds': round(time.time() - t, 1)}
    x = h.getSolution().col_value
    H = [i for i in range(N) if x is not None and len(x) == N and x[i] > 0.5] if st != 'Infeasible' else []
    if H and len(H) <= 33 and not check(H, ROWS):
        hm = sum(1 << i for i in H)
        viol = [(s, d) for m, d, s in masks if (m & hm).bit_count() < d]
        rec.update(holes=H, F_occupied=len(set(F) - set(H)), violated=len(viol))
        if not viol:
            rec['GENUINE'] = True; log.write(json.dumps(rec) + '\n'); log.flush(); print(json.dumps(rec), flush=True); break
        active += viol[:400]
    log.write(json.dumps(rec) + '\n'); log.flush(); print(json.dumps(rec), flush=True)
    if st == 'Infeasible':
        break
    if not H and st != 'Infeasible':
        break

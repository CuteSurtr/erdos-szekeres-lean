"""Base 2,650 rows + capacity row h(F) >= 84 - c: find a 33-hole vector (HiGHS), then test it against the
new rows (templates + newrows).  Repeats with the vector excluded (no-good) to sample several."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import highspy
from common import N, STATES, ROWS, check
from hfind import load_rows
c = int(sys.argv[1]); k = int(sys.argv[2]); tl = float(sys.argv[3])
F = [i for i in range(N) if STATES[i][0] >= 5]
allrows = load_rows(); extra = allrows[len(ROWS):]
found = []
for it in range(k):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
    h.setOptionValue('time_limit', tl); h.setOptionValue('mip_max_improving_sols', 1)
    v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
    h.changeColBounds(0, 0, 0)
    for i in range(N): h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
    for s, d in ROWS: h.addConstr(h.qsum(v[i] for i in s) >= d)
    h.addConstr(h.qsum(v[i] for i in F) >= 84 - c)
    h.addConstr(h.qsum(v) <= 33)
    for H in found:  # no-good: not the same hole set
        h.addConstr(h.qsum(v[i] for i in H) <= len(H) - 1)
    t = time.time(); h.run(); st = h.modelStatusToString(h.getModelStatus())
    x = h.getSolution().col_value
    H = [i for i in range(N) if x is not None and len(x) == N and x[i] > 0.5]
    rec = {'it': it, 'status': st, 'seconds': round(time.time() - t, 1)}
    if H and len(H) <= 33 and not check(H, ROWS):
        found.append(H)
        rec.update(holes=H, F_occupied=len(set(F) - set(H)), violates_new_rows=len(check(H, extra)))
    print(json.dumps(rec), flush=True)
    with open('capvec.jsonl', 'a') as f: f.write(json.dumps(rec) + '\n')
    if not H: break

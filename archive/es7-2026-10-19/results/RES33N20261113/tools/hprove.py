"""One long HiGHS MIP run: is there a 0/1 vector, h0=0, sum<=33, satisfying catalog+templates+newrows?
Infeasible => (numerical, uncertified) residual budget 33 excluded over these rows."""
import json, os, sys, time, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import highspy
from common import N, check
from hfind import load_rows
rows = load_rows()
sig = hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest()[:16]
h = highspy.Highs()
h.setOptionValue('output_flag', True)
h.setOptionValue('log_to_console', False)
h.setOptionValue('log_file', 'hprove.log')
h.setOptionValue('threads', 1)
h.setOptionValue('time_limit', float(sys.argv[1]) - time.time())
h.setOptionValue('mip_max_improving_sols', 1)
v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
h.addConstr(h.qsum(v) <= 33)
h.changeColBounds(0, 0, 0)
for i in range(N): h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
for s, d in rows: h.addConstr(h.qsum(v[i] for i in s) >= d)
t = time.time(); h.run()
st = h.modelStatusToString(h.getModelStatus()); info = h.getInfo()
out = {'t': time.strftime('%H:%M:%S'), 'rows': len(rows), 'rows_sha': sig, 'status': st, 'seconds': round(time.time() - t, 1),
       'dual_bound': info.mip_dual_bound, 'nodes': info.mip_node_count}
x = h.getSolution().col_value
if x is not None and len(x) == N:
    H = [i for i in range(N) if x[i] > 0.5]
    if len(H) <= 33 and not check(H, rows) and 0 not in H: out['holes'] = H
json.dump(out, open('hprove_out.json', 'w')); print(json.dumps(out))

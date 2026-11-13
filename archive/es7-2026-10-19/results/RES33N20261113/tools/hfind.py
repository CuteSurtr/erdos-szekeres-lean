"""Global search for a 33-hole residual vector with HiGHS MIP (min sum h, objective bound 33.5).
Re-reads templates + newrows each round. Writes found vectors to hfound.jsonl. Discovery only."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import highspy
from common import N, ROWS, check

def load_rows():
    rows = list(ROWS); seen = {s for s, d in rows if d >= 1}
    for name, v in json.load(open(os.path.join(HERE, 'templates.json'))).items():
        for s in v['supports']:
            s = tuple(sorted(s))
            if s not in seen: seen.add(s); rows.append((s, 1))
    p = os.path.join(HERE, 'newrows.json')
    if os.path.exists(p):
        for r in json.load(open(p)):
            s = tuple(sorted(r['support']))
            if s not in seen: seen.add(s); rows.append((s, 1))
    return rows

def run(seconds, seed):
    rows = load_rows()
    h = highspy.Highs()
    h.setOptionValue('output_flag', False)
    h.setOptionValue('threads', 1)
    h.setOptionValue('time_limit', float(seconds))
    h.setOptionValue('random_seed', seed)
    h.setOptionValue('mip_max_improving_sols', 1)
    v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
    h.addConstr(h.qsum(v) <= 33)
    h.changeColBounds(0, 0, 0)
    for i in range(N): h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
    for s, d in rows: h.addConstr(h.qsum(v[i] for i in s) >= d)
    t = time.time(); h.run()
    st = h.modelStatusToString(h.getModelStatus())
    info = h.getInfo()
    out = {'t': time.strftime('%H:%M:%S'), 'rows': len(rows), 'status': st, 'seconds': round(time.time() - t, 1),
           'dual_bound': info.mip_dual_bound, 'nodes': info.mip_node_count}
    x = h.getSolution().col_value
    if x is not None and len(x) == N:
        H = [i for i in range(N) if x[i] > 0.5]
        if len(H) <= 33 and not check(H, rows) and 0 not in H:
            out['holes'] = H
    return out

if __name__ == '__main__':
    deadline = float(sys.argv[1]); per = float(sys.argv[2]) if len(sys.argv) > 2 else 900
    seed = 0
    while time.time() < deadline - 60:
        r = run(min(per, deadline - time.time() - 30), seed); seed += 1
        with open(os.path.join(HERE, 'hfound.jsonl'), 'a') as f: f.write(json.dumps(r) + '\n')
        print(json.dumps(r), flush=True)
        if 'holes' in r:
            # hand the vector to the CEGAR loop via vectors.json seeds
            vp = os.path.join(HERE, 'vectors.json')
            vs = json.load(open(vp)) if os.path.exists(vp) else []
            vs.append(r['holes']); json.dump(vs, open(vp + '.tmp', 'w')); os.replace(vp + '.tmp', vp)

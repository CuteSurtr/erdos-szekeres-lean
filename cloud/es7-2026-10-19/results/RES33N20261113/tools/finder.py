"""Continuous global CP-SAT search for 33-hole residual vectors; appends finds to vectors.json."""
import json, os, sys, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mip import load_rows
from cegar import cpsat
DL = float(sys.argv[1]); workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
vp = os.path.join(HERE, 'vectors.json')
while time.time() < DL - 120:
    rows, _, _ = load_rows()
    seed = random.randrange(10**6)
    t = time.time()
    st, H = cpsat(rows, seconds=min(900, DL - time.time() - 60), workers=workers, seed=seed)
    rec = {'t': time.strftime('%H:%M:%S'), 'status': st, 'rows': len(rows), 'seconds': round(time.time() - t), 'seed': seed}
    if H:
        vs = json.load(open(vp)) if os.path.exists(vp) else []
        if H not in vs:
            vs.append(H); json.dump(vs, open(vp + '.tmp', 'w')); os.replace(vp + '.tmp', vp)
        rec['holes'] = H
    with open(os.path.join(HERE, 'finder.jsonl'), 'a') as f: f.write(json.dumps(rec) + '\n')
    if st == 'INFEASIBLE':
        break

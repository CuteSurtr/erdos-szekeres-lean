"""Exact (CP-SAT, uncertified) neighbourhood statements: for each known 33-hole vector C and radius r,
is there a vector H with h0=0, |H|<=33, |H \\ C| <= r, satisfying all rows?  INFEASIBLE = none."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mip import load_rows
from cegar import cpsat, seeds
rows, a, b = load_rows()
out = []
for c in seeds():
    for r in (6, 10, 14):
        t = time.time(); st, H = cpsat(rows, center=c, radius=r, seconds=300, workers=2)
        rec = {'center_head': sorted(c)[:6], 'radius': r, 'status': st, 'seconds': round(time.time() - t, 1), 'rows': len(rows)}
        if H: rec['holes'] = H
        out.append(rec); print(json.dumps(rec), flush=True)
        json.dump(out, open(os.path.join(HERE, 'nbhd_proof.json'), 'w'), indent=0)
        if st != 'INFEASIBLE': break

"""Cube-driven CEGAR at budget 18 (discovery; result COMPUTED).  Cubes already UNSAT over an earlier row
snapshot stay UNSAT when rows are added (more constraints), so only the 7 open cubes are re-solved.
For a SAT cube: probe its vector with density-grown supports, minimise, transport, re-solve.
usage: cubecegar.py <deadline-epoch>"""
import sys, os, time, json, subprocess
DL = sys.argv[1]
sys.argv = ['loop12.py', DL, '5', '18', 'cc']
import loop12 as L
import etv_common as ec
from pbcnf5 import build
from multiprocessing import Pool
BR = [22, 37, 45, 53, 67]
OPEN = ['10111', '11010', '11011', '11100', '11101', '11110', '11111']
def solve_cube(args):
    tag, rows_list = args
    top, cls = build(rows_list, 18, ec.N, ec.FIXED_OCC)
    units = [[(s + 1) if b == '1' else -(s + 1)] for s, b in zip(BR, tag)]
    p = f'/home/jay/research/data/etv5-20261113/pbtest/cc_{tag}.cnf'
    with open(p, 'w') as f:
        f.write(f'p cnf {top} {len(cls) + len(units)}\n')
        for c in cls + units: f.write(' '.join(map(str, c)) + ' 0\n')
    t = time.time(); r = subprocess.run(['cadical', '-q', '-t', '420', p], capture_output=True, text=True); os.remove(p)
    st = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, 'UNKNOWN'); H = None
    if st == 'SAT':
        vals = set(int(x) for line in r.stdout.splitlines() if line.startswith('v') for x in line.split()[1:])
        H = [i for i in range(ec.N) if (i + 1) in vals]
    return tag, st, round(time.time() - t, 1), H
if __name__ == '__main__':
    deadline = float(DL); rnd = 0; status = {c: 'open' for c in OPEN}
    with Pool(5) as pool:
        while time.time() < deadline and any(v != 'UNSAT' for v in status.values()):
            rnd += 1; t0 = time.time()
            rows = L.load_rows(); rl = [(list(s), d) for s, d in rows.items()]
            todo = [c for c, v in status.items() if v != 'UNSAT']
            res = pool.map(solve_cube, [(c, rl) for c in todo])
            vecs = []
            for tag, st, secs, H in res:
                status[tag] = st
                L.log(event='cube', tag=tag, status=st, secs=secs, holes=H, rows=len(rows))
                if H: vecs.append(H)
            if not vecs: continue
            found = []
            for V in vecs[:5]:
                fv, stats, nf = L.probe_vector(pool, V, 6)
                L.log(event='probe', stats=stats, found=len(fv)); found += fv
            if found: L.process_found(pool, found, rnd, rows, t0)
    L.log(event='CUBES_FINAL', status=status)

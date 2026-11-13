"""Plain CaDiCaL on cubes (no proof) to gauge difficulty / find a vector.  usage: cube_probe.py <rows.json> <budget> <states> <secs> [procs]"""
import json, sys, subprocess, os, itertools, time
from multiprocessing import Pool
import etv_common as ec
from pbcnf5 import build
rows = json.load(open(sys.argv[1])); B = int(sys.argv[2]); br = [int(x) for x in sys.argv[3].split(',')]; secs = int(sys.argv[4])
procs = int(sys.argv[5]) if len(sys.argv) > 5 else 1
top, cls = build(rows, B, ec.N, ec.FIXED_OCC)
base = ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)
def run(bits):
    tag = ''.join(map(str, bits)); p = f'pbtest/cp_{tag}_{os.getpid()}.cnf'
    units = [[(s + 1) if b else -(s + 1)] for s, b in zip(br, bits)]
    with open(p, 'w') as f: f.write(f'p cnf {top} {len(cls) + len(units)}\n' + base + ''.join(f'{u[0]} 0\n' for u in units))
    t = time.time(); r = subprocess.run(['cadical', '-q', '-t', str(secs), p], capture_output=True, text=True); os.remove(p)
    st = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, 'UNKNOWN'); H = None
    if st == 'SAT':
        vals = set(int(x) for line in r.stdout.splitlines() if line.startswith('v') for x in line.split()[1:]); H = [i for i in range(ec.N) if (i + 1) in vals]
    return tag, st, round(time.time() - t, 1), H
cubes = list(itertools.product([0, 1], repeat=len(br)))
with Pool(procs) as P:
    for tag, st, t, H in P.imap_unordered(run, cubes):
        print(json.dumps({'cube': tag, 'status': st, 'secs': t, 'holes': H}), flush=True)

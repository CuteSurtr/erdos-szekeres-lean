"""Exact level probe with CaDiCaL on the PB CNF (no proof): is there a vector with <= budget holes over the
current rows?  Prints SAT + holes, UNSAT, or UNKNOWN.  usage: level_probe.py <budget> <seconds>"""
import json, sys, subprocess, os, time
import rowsio, etv_common as ec
from pbcnf5 import build
budget = int(sys.argv[1]); secs = int(sys.argv[2])
rows = rowsio.load_all()
top, cls = build([(list(s), d) for s, (d, k) in rows.items()], budget, ec.N, ec.FIXED_OCC)
p = f'pbtest/probe_{budget}_{os.getpid()}.cnf'
with open(p, 'w') as f:
    f.write(f'p cnf {top} {len(cls)}\n')
    for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
t = time.time()
r = subprocess.run(['cadical', '-q', '-t', str(secs), p], capture_output=True, text=True)
os.remove(p)
st = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, 'UNKNOWN')
H = None
if st == 'SAT':
    vals = set(int(x) for line in r.stdout.splitlines() if line.startswith('v') for x in line.split()[1:])
    H = [i for i in range(ec.N) if (i + 1) in vals]
print(json.dumps({'budget': budget, 'rows': len(rows), 'status': st, 'holes': H, 'seconds': round(time.time() - t, 1), 't': time.strftime('%H:%M:%S')}), flush=True)

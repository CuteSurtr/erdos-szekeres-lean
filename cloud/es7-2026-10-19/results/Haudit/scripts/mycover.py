#!/usr/bin/env python3
"""Own cover checker: cubes c_1..c_m cover all assignments  <=>  CNF {not c_i} is UNSAT.
The CNF is solved by CaDiCaL with LRAT output and the proof is checked by cake_lpr.
usage: mycover.py CUBES.icnf [WORKDIR]   (reads 'a l1 .. lk 0' lines)"""
import sys, os, subprocess
cubes = [list(map(int, l.split()[1:-1])) for l in open(sys.argv[1]) if l.startswith('a')]
w = sys.argv[2] if len(sys.argv) > 2 else '/tmp'
os.makedirs(w, exist_ok=True)
assert all(0 not in c for c in cubes)
if any(len(c) == 0 for c in cubes):
    print("s COVERED (empty cube present)", len(cubes)); sys.exit(0)
nv = max([abs(l) for c in cubes for l in c] + [1])
cnf = os.path.join(w, 'cov.cnf'); prf = os.path.join(w, 'cov.lrat')
with open(cnf, 'w') as f:
    f.write(f"p cnf {nv} {len(cubes)}\n")
    for c in cubes: f.write(" ".join(str(-l) for l in c) + " 0\n")
rc = subprocess.run(['/opt/bin/cadical', '-q', '--lrat', '--binary=false', cnf, prf], stdout=subprocess.DEVNULL).returncode
if rc == 10: print("s NOT COVERED (cadical found an uncovered assignment)", len(cubes)); sys.exit(1)
if rc != 20: print("s UNKNOWN rc", rc); sys.exit(2)
o = subprocess.run(['/opt/bin/cake_lpr', cnf, prf], capture_output=True, text=True).stdout
ok = any(l.strip() == 's VERIFIED UNSAT' for l in o.splitlines())
print("s COVERED (cake_lpr VERIFIED)" if ok else "s CHECK FAILED " + o[-200:], len(cubes)); sys.exit(0 if ok else 3)

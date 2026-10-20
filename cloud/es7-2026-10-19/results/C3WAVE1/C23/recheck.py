import sys, os, subprocess, time, json
sys.path.insert(0, '/opt/c3s/cloud/es7-2026-10-19/results/C3a'); sys.path.insert(0, '/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools')
import close_tree as ct
node = sys.argv[1]; d = '/opt/work/re'; os.makedirs(d, exist_ok=True); ct.WORK = d
from hullcase import layer_clauses, parse_layers
us = [c[0] for c in layer_clauses(11, parse_layers(node), ct.E.ccw, ct.E.sig)]
cnf, prf = f'{d}/{node}.cnf', f'{d}/{node}.lrat'
with open('/opt/work/base.cnf') as f, open(cnf, 'w') as g:
    h = f.readline().split(); g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n"); g.write(f.read()); g.write("".join(f"{u} 0\n" for u in us))
print('sha', ct.sha(cnf))
t = time.time(); r = subprocess.run(["cadical", "-q", "-t", "600", "--sat", "--lrat", "--binary=false", cnf, prf], capture_output=True, text=True)
print('cadical', [l for l in r.stdout.splitlines() if l.startswith('s ')], round(time.time()-t, 1), os.path.getsize(prf))
t = time.time(); a = subprocess.run(["lrat-check", cnf, prf], capture_output=True, text=True)
print('lrat-check rc', a.returncode, [l for l in a.stdout.splitlines() if 'VERIFIED' in l], round(time.time()-t, 1))
env = dict(os.environ, CML_HEAP_SIZE="12000", CML_STACK_SIZE="2000")
t = time.time(); b = subprocess.run(["/usr/bin/time", "-v", "cake_lpr", cnf, prf], capture_output=True, text=True, env=env)
print('cake rc', b.returncode, 'stdout', b.stdout.strip()[:300], round(time.time()-t, 1))
print('cake stderr', "\n".join(l for l in b.stderr.splitlines() if 'Maximum resident' in l or 'Exit' in l or 'rror' in l or 'xception' in l)[:1500])

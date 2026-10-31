import sys, os, time, subprocess, hashlib
os.chdir('/opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools')
sys.path.insert(0, '../../C3a'); sys.path.insert(0, '.')
from c3cnf import C3Enc
from hullcase import layer_clauses, parse_layers
from controls import dual
E = C3Enc(11, 7); node = sys.argv[1]; W = '/opt/work/recheck'
us = [c[0] for c in layer_clauses(11, parse_layers(node), E.ccw, E.sig)]
cnf, prf = f'{W}/{node}.cnf', f'{W}/{node}.lrat'
with open('/opt/work/base.cnf') as f, open(cnf, 'w') as g:
    h = f.readline().split(); g.write(f"p cnf {h[2]} {int(h[3]) + len(us)}\n"); g.write(f.read()); g.write(''.join(f'{u} 0\n' for u in us))
print('sha', hashlib.sha256(open(cnf,'rb').read()).hexdigest(), flush=True)
t=time.time(); r = subprocess.run(['cadical','-q','-t','600','--sat','--lrat','--binary=false',cnf,prf],capture_output=True,text=True).stdout
print([l for l in r.splitlines() if l.startswith('s ')], round(time.time()-t,1), os.path.getsize(prf), flush=True)
t=time.time(); print('dual', dual(cnf, prf), round(time.time()-t,1), flush=True)
env = dict(os.environ, CML_HEAP_SIZE="12000", CML_STACK_SIZE="2000")
p = subprocess.run(['cake_lpr',cnf,prf],capture_output=True,text=True,env=env)
print('cake rc', p.returncode, repr(p.stdout[:200]), [l.strip() for l in p.stderr.splitlines() if 'Maximum resident' in l or 'Exit status' in l], repr(p.stderr[:300]), flush=True)
os.remove(cnf); os.remove(prf)

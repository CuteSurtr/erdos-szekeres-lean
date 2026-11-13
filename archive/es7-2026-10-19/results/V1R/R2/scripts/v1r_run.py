#!/usr/bin/env python3
"""V1R: re-check sub-case (i) leaves i % 4 == J of verify/hull_leaves.icnf.
For each leaf: cubeCnf (hullCnf 33 7) c = header with NC+|c|, body of hm33k7.sub.cnf,
one unit clause per cube literal (file order). cadical --lrat=true --no-binary, then cake_lpr.
Usage: v1r_run.py SUBCNF LEAVES J OUT.jsonl CADICAL CAKE_LPR TMPDIR [PAR] [--only i,i,...]"""
import hashlib, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
import threading

sub, leaves, J, out, CAD, CAKE, TMP = sys.argv[1:8]
J = int(J); PAR = int(sys.argv[8]) if len(sys.argv) > 8 and not sys.argv[8].startswith('--') else 3
only = None
if '--only' in sys.argv:
    only = {int(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')}
data = open(sub, 'rb').read()
nl = data.index(b'\n')
hdr = data[:nl].split()
assert hdr[:2] == [b'p', b'cnf'] and len(hdr) == 4
NV, NC = int(hdr[2]), int(hdr[3])
body = data[nl + 1:]
assert body.endswith(b'\n')

cubes = []
for i, line in enumerate(open(leaves)):
    t = line.split()
    assert t[0] == 'a' and t[-1] == '0'
    cubes.append((i, [int(x) for x in t[1:-1]]))
done = set()
if os.path.exists(out) and only is None:
    for l in open(out):
        r = json.loads(l)
        if r['solver_exit'] == 20 and r['cake_lpr'] == 's VERIFIED UNSAT':
            done.add(r['i'])
todo = [(i, c) for i, c in cubes if i % 4 == J and i not in done and (only is None or i in only)]
lock = threading.Lock()

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()

def run(item):
    i, c = item
    f = os.path.join(TMP, f'leaf{i}.cnf'); p = os.path.join(TMP, f'leaf{i}.lrat')
    with open(f, 'wb') as fh:
        fh.write(b'p cnf %d %d\n' % (NV, NC + len(c)))
        fh.write(body)
        fh.write(b''.join(b'%d 0\n' % l for l in c))
    cnf_sha = sha(f)
    t0 = time.time()
    st = subprocess.run([CAD, '-q', '--lrat=true', '--no-binary', f, p],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
    t1 = time.time()
    pb = os.path.getsize(p) if os.path.exists(p) else 0
    psha = sha(p) if pb else None
    if st == 20:
        r = subprocess.run([CAKE, f, p], capture_output=True, text=True)
        lines = (r.stdout + r.stderr).splitlines()
        v = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in lines else ' | '.join(lines[-5:])
    else:
        v = f'not checked: solver exit {st}'
    t2 = time.time()
    for x in (f, p):
        if os.path.exists(x): os.remove(x)
    rec = dict(i=i, cube=c, cnf_sha256=cnf_sha, solver_exit=st, solve_s=round(t1 - t0, 2),
               proof_bytes=pb, proof_sha256=psha, cake_lpr=v, check_s=round(t2 - t1, 2))
    with lock:
        with open(out, 'a') as o:
            o.write(json.dumps(rec) + '\n')
    print(i, st, v, rec['solve_s'], rec['check_s'], flush=True)

with ThreadPoolExecutor(PAR) as ex:
    list(ex.map(run, todo))
print('ALLDONE', flush=True)

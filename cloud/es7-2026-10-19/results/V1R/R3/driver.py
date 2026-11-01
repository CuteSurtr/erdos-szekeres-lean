import hashlib, json, os, subprocess, sys, time, threading
from concurrent.futures import ThreadPoolExecutor
W = '/tmp/claude-0/w'
CAD = W + '/cadical/build/cadical'
CAKE = W + '/cake_lpr/cake_lpr'
LEAVES = sys.argv[1]; J = int(sys.argv[2]); OUT = sys.argv[3]
only = set(int(x) for x in sys.argv[4].split(',')) if len(sys.argv) > 4 else None
par = 1 if only else 3
body = open(W + '/hm33k7.sub.cnf', 'rb').read()
nl = body.index(b'\n')
hdr = body[:nl].split(); assert hdr[:2] == [b'p', b'cnf']
NV, NC = int(hdr[2]), int(hdr[3]); rest = body[nl+1:]
cubes = []
for i, line in enumerate(open(LEAVES)):
    t = line.split(); assert t[0] == 'a' and t[-1] == '0'
    cubes.append((i, [int(x) for x in t[1:-1]]))
mine = [(i, c) for i, c in cubes if i % 4 == J and (only is None or i in only)]
done = set()
if os.path.exists(OUT) and only is None:
    for l in open(OUT):
        r = json.loads(l)
        if r.get('ok'): done.add(r['i'])
lock = threading.Lock()
def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def run(ic):
    i, c = ic
    d = f'{W}/leaf{i}'; os.makedirs(d, exist_ok=True)
    cnf, prf = d + '/f.cnf', d + '/p.lrat'
    with open(cnf, 'wb') as f:
        f.write(b'p cnf %d %d\n' % (NV, NC + len(c))); f.write(rest)
        for l in c: f.write(b'%d 0\n' % l)
    cs = sha(cnf)
    t = time.time()
    p = subprocess.run([CAD, '--lrat=true', '--no-binary', '-q', cnf, prf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ss = round(time.time() - t, 2)
    pb = os.path.getsize(prf) if os.path.exists(prf) else 0
    ps = sha(prf) if pb else None
    t = time.time()
    if p.returncode == 20:
        q = subprocess.run([CAKE, cnf, prf], capture_output=True, text=True)
        lines = (q.stdout + q.stderr).splitlines()
        ver = 's VERIFIED UNSAT' in lines
        cl = 's VERIFIED UNSAT' if ver else ' | '.join(lines[-5:])
    else:
        ver, cl = False, 'not run'
    ck = round(time.time() - t, 2)
    r = dict(i=i, cube=c, cnf_sha256=cs, solver_exit=p.returncode, solve_s=ss, proof_bytes=pb,
             proof_sha256=ps, cake_lpr=cl, check_s=ck, ok=(p.returncode == 20 and ver))
    if only: r['rerun'] = True
    for x in (cnf, prf):
        if os.path.exists(x): os.remove(x)
    os.rmdir(d)
    with lock:
        with open(OUT, 'a') as f: f.write(json.dumps(r) + '\n')
    print(i, r['ok'], ss, ck, flush=True)
todo = [x for x in mine if x[0] not in done]
print('share', len(mine), 'todo', len(todo), flush=True)
with ThreadPoolExecutor(par) as ex: list(ex.map(run, todo))
print('ALL_DONE', flush=True)

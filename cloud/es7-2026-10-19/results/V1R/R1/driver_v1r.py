import sys, os, json, hashlib, subprocess, time, threading
from concurrent.futures import ThreadPoolExecutor
SUB, ICNF, OUT, WORK, J, DEADLINE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), float(sys.argv[6])
ONLY = [int(x) for x in sys.argv[7].split(',')] if len(sys.argv) > 7 else None
CAD = '/tmp/claude-0/w/cadical/build/cadical'; CAKE = '/tmp/claude-0/w/cake_lpr/cake_lpr'
raw = open(SUB, 'rb').read()
nl = raw.index(b'\n'); hdr = raw[:nl].split(); body = raw[nl+1:]
assert hdr[:2] == [b'p', b'cnf']; NV, NC = int(hdr[2]), int(hdr[3])
cubes = []
for i, line in enumerate(open(ICNF)):
    t = line.split(); assert t[0] == 'a' and t[-1] == '0'
    cubes.append((i, [int(x) for x in t[1:-1]]))
done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)['i'])
todo = [(i, c) for i, c in cubes if (i in ONLY if ONLY else i % 4 == J and i not in done)]
lock = threading.Lock()
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
def leaf(ic):
    i, c = ic
    if time.time() > DEADLINE: return
    cnf = f'{WORK}/l{i}.cnf'; prf = f'{WORK}/l{i}.lrat'
    with open(cnf, 'wb') as f:
        f.write(f'p cnf {NV} {NC+len(c)}\n'.encode()); f.write(body)
        for x in c: f.write(f'{x} 0\n'.encode())
    rec = {'i': i, 'cube': c, 'cnf_sha256': sha(cnf)}
    t = time.time()
    r = subprocess.run([CAD, '--lrat=true', '--no-binary', '-q', cnf, prf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rec['solver_exit'] = r.returncode; rec['solve_s'] = round(time.time() - t, 2)
    rec['proof_bytes'] = os.path.getsize(prf) if os.path.exists(prf) else 0
    rec['proof_sha256'] = sha(prf) if os.path.exists(prf) else None
    if r.returncode == 20:
        t = time.time()
        k = subprocess.run([CAKE, cnf, prf], capture_output=True, text=True)
        lines = (k.stdout + k.stderr).splitlines()
        rec['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in lines else '\n'.join(lines[-5:])
        rec['check_s'] = round(time.time() - t, 2)
    else:
        rec['cake_lpr'] = None; rec['check_s'] = None
    rec['verified'] = r.returncode == 20 and rec['cake_lpr'] == 's VERIFIED UNSAT'
    for p in (cnf, prf):
        if os.path.exists(p): os.remove(p)
    with lock:
        with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
    print(i, rec['verified'], rec['solve_s'], rec.get('check_s'), flush=True)
with ThreadPoolExecutor(3) as ex: list(ex.map(leaf, todo))
print('DONE', flush=True)

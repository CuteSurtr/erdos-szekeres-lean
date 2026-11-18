"""Certified first-layer instances (abstract signotope model): CaDiCaL 2.1.3 LRAT + cake_lpr.
usage: cert.py <a> <b> <n> <plain|inj> [timeout_s]
  plain: fls.FL(a,b,n)  (signotope axioms + exact chain definitions + no a-cap, no b-cup, no first-layer gon)
  inj  : witg.WitG(a,b,n, all points present) + 'at most one point per state'  (state separation, README 3.2)
Only cake_lpr's line 's VERIFIED UNSAT' certifies.  Appends to cert/certified.jsonl; the LRAT is deleted after hashing."""
import sys, os, json, time, hashlib, subprocess, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
a, b, n, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
to = int(sys.argv[5]) if len(sys.argv) > 5 else 0
if mode == 'plain':
    import fls
    w = fls.FL(a, b, n); txt = w.dimacs()
else:
    import witg
    w = witg.WitG(a, b, n, flags=False)
    cl = list(w.cl)
    for si in range(len(w.S)):
        vs = [w.st[p, si] for p in range(n) if (p, si) in w.st]
        for x, y in itertools.combinations(vs, 2): cl.append([-x, -y])
    # every point has a state (implied; kept as redundant clauses)
    for p in range(n):
        cl.append([w.st[p, si] for si in range(len(w.S)) if (p, si) in w.st])
    txt = 'p cnf %d %d\n' % (w.nv, len(cl)) + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cl)
h = hashlib.sha256(txt.encode()).hexdigest()
p = os.path.join(HERE, 'cert', f'fl_{a}_{b}_{n}_{mode}.cnf'); q = p[:-4] + '.lrat'
open(p, 'w').write(txt)
t0 = time.time()
cmd = ['/usr/bin/cadical', '-q', '--lrat=true', '--binary=false'] + (['-t', str(to)] if to else []) + [p, q]
r = subprocess.run(cmd, capture_output=True, text=True); t1 = time.time() - t0
res = {'a': a, 'b': b, 'n': n, 'mode': mode, 'cnf_sha256': h, 'vars': w.nv, 'cadical_exit': r.returncode, 'cadical_s': round(t1, 1)}
if r.returncode == 20:
    res['lrat_bytes'] = os.path.getsize(q)
    hh = hashlib.sha256()
    with open(q, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 24), b''): hh.update(chunk)
    res['lrat_sha256'] = hh.hexdigest()
    t0 = time.time(); c = subprocess.run([CAKE, p, q], capture_output=True, text=True)
    res['cake_s'] = round(time.time() - t0, 1)
    res['verdict'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else 'cake_lpr: ' + (c.stdout + c.stderr)[-200:]
else:
    res['verdict'] = 'SAT' if r.returncode == 10 else 'UNKNOWN'
if os.path.exists(q): os.remove(q)
with open(os.path.join(HERE, 'cert', 'certified.jsonl'), 'a') as f: f.write(json.dumps(res) + '\n')
print(res, flush=True)

"""Cube-and-conquer certificate for "no vector with <= budget holes" over a rows file.
The base CNF is pbcnf5.build (self-tested); cube c (a 0/1 assignment of the branching states) adds unit clauses.
The cubes cover all assignments of the branching states, so all cubes UNSAT => base CNF UNSAT.
Each cube: CaDiCaL 2.1.3 --lrat, cake_lpr; trace of the rows used.  LRATs deleted after hashing.
usage: cube_lrat.py <rows.json> <budget> <outdir> <procs> <state,state,...>"""
import json, os, sys, subprocess, hashlib, itertools, time
from multiprocessing import Pool
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
import etv_common as ec
from etv_common import N
rowsfile, budget, od, procs = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
branch = [int(x) for x in sys.argv[5].split(',')]
os.makedirs(od, exist_ok=True)
rows = [(s, d) for s, d in json.load(open(rowsfile))]
pool = IDPool(start_from=N + 1); var = lambda i: i + 1
clauses = []; owner = []
for i in ec.FIXED_OCC: clauses.append([-var(i)]); owner.append(-1)
for c in CardEnc.atmost(lits=[var(i) for i in range(N) if i not in ec.FIXED_OCC], bound=budget, vpool=pool, encoding=EncType.seqcounter).clauses:
    clauses.append(c); owner.append(-1)
for r, (s, d) in enumerate(rows):
    L = [var(i) for i in s if i not in ec.FIXED_OCC]
    if d == 1: clauses.append(L); owner.append(r)
    else:
        for c in CardEnc.atleast(lits=L, bound=d, vpool=pool, encoding=EncType.kmtotalizer).clauses:
            clauses.append(c); owner.append(r)
base = ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)
base_sha = hashlib.sha256((f'p cnf {pool.top} {len(clauses)}\n' + base).encode()).hexdigest()
def run(bits):
    tag = ''.join(map(str, bits))
    units = [[var(s) if b else -var(s)] for s, b in zip(branch, bits)]
    p = os.path.join(od, f'cube_{tag}.cnf'); q = p[:-4] + '.lrat'
    with open(p, 'w') as f:
        f.write(f'p cnf {pool.top} {len(clauses) + len(units)}\n' + base + ''.join(' '.join(map(str, u)) + ' 0\n' for u in units))
    cnf_sha = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    t = time.time()
    r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', p, q], capture_output=True, text=True)
    res = {'cube': tag, 'cnf_sha256': cnf_sha, 'cadical_exit': r.returncode, 'cadical_seconds': round(time.time() - t, 1)}
    if r.returncode != 20:
        os.remove(p)
        if os.path.exists(q): os.remove(q)
        return res, []
    h = hashlib.sha256()
    with open(q, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 24), b''): h.update(chunk)
    res['lrat_sha256'] = h.hexdigest(); res['lrat_bytes'] = os.path.getsize(q)
    t = time.time()
    c = subprocess.run([os.path.expanduser('~/.local/bin/cake_lpr'), p, q], capture_output=True, text=True)
    res['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else (c.stdout + c.stderr)[-200:]
    res['cake_seconds'] = round(time.time() - t, 1)
    m = len(clauses) + len(units); hints = {}; empty = None
    with open(q) as f:
        for line in f:
            tk = line.split()
            if len(tk) > 1 and tk[1] == 'd': continue
            cid = int(tk[0]); z = tk.index('0', 1)
            hints[cid] = [abs(int(x)) for x in tk[z + 1:-1]]
            if z == 1: empty = cid
    used = set(); stack = [empty]; seen = set()
    while stack:
        x = stack.pop()
        if x in seen: continue
        seen.add(x)
        if x <= m: used.add(x); continue
        stack.extend(hints.get(x, []))
    used_rows = sorted({owner[x - 1] for x in used if x <= len(clauses) and owner[x - 1] >= 0})
    os.remove(q); os.remove(p)
    return res, used_rows
if __name__ == '__main__':
    t0 = time.time()
    cubes = list(itertools.product([0, 1], repeat=len(branch)))
    allused = set(); out = []
    with Pool(procs) as P:
        for res, used in P.imap_unordered(run, cubes):
            out.append(res); allused.update(used)
            print(json.dumps(res), flush=True)
    ok = all(r.get('cake_lpr') == 's VERIFIED UNSAT' for r in out) and len(out) == len(cubes)
    json.dump([[list(rows[r][0]), rows[r][1]] for r in sorted(allused)], open(os.path.join(od, 'used_rows.json'), 'w'))
    info = {'rows_file': rowsfile, 'rows_sha256': hashlib.sha256(open(rowsfile, 'rb').read()).hexdigest(), 'budget': budget,
            'base_cnf_sha256': base_sha, 'branch_states': branch, 'cubes': out, 'all_verified': ok, 'used_rows': len(allused),
            'seconds': round(time.time() - t0, 1)}
    json.dump(info, open(os.path.join(od, 'info.json'), 'w'), indent=1)
    print(json.dumps({'all_verified': ok, 'cubes': len(out), 'used_rows': len(allused), 'seconds': info['seconds']}), flush=True)

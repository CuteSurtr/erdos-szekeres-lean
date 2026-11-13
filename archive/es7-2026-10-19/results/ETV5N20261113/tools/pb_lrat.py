"""PB CNF of a row file at a budget, CaDiCaL 2.1.3 LRAT, cake_lpr check, and trace of the rows used by the
refutation.  usage: pb_lrat.py <rows.json> <budget> <outdir>
Writes outdir/pb.cnf (+sha256), runs cadical --lrat --binary=false, cake_lpr, then parses the LRAT to find the
original clauses used and maps them to rows; writes outdir/used_rows.json ([[support, demand], ...]).
The LRAT file is deleted after cake_lpr's verdict and its hash are recorded."""
import json, os, sys, subprocess, hashlib, time
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
import etv_common as ec
from etv_common import N
rows = [(s, d) for s, d in json.load(open(sys.argv[1]))]; budget = int(sys.argv[2]); od = sys.argv[3]
os.makedirs(od, exist_ok=True)
pool = IDPool(start_from=N + 1); var = lambda i: i + 1
clauses = []; owner = []   # owner[c] = row index or -1 (fixed/cardinality)
for i in ec.FIXED_OCC: clauses.append([-var(i)]); owner.append(-1)
for c in CardEnc.atmost(lits=[var(i) for i in range(N) if i not in ec.FIXED_OCC], bound=budget, vpool=pool, encoding=EncType.seqcounter).clauses:
    clauses.append(c); owner.append(-1)
for r, (s, d) in enumerate(rows):
    L = [var(i) for i in s if i not in ec.FIXED_OCC]
    if d == 1: clauses.append(L); owner.append(r)
    else:
        for c in CardEnc.atleast(lits=L, bound=d, vpool=pool, encoding=EncType.kmtotalizer).clauses:
            clauses.append(c); owner.append(r)
cnf = os.path.join(od, 'pb.cnf'); lrat = os.path.join(od, 'pb.lrat')
with open(cnf, 'w') as f:
    f.write(f'p cnf {pool.top} {len(clauses)}\n')
    for c in clauses: f.write(' '.join(map(str, c)) + ' 0\n')
info = {'rows': len(rows), 'budget': budget, 'vars': pool.top, 'clauses': len(clauses),
        'cnf_sha256': hashlib.sha256(open(cnf, 'rb').read()).hexdigest(),
        'rows_sha256': hashlib.sha256(open(sys.argv[1], 'rb').read()).hexdigest()}
print(json.dumps(info), flush=True)
t = time.time()
r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', cnf, lrat], capture_output=True, text=True)
info['cadical_exit'] = r.returncode; info['cadical_seconds'] = round(time.time() - t, 1)
print(json.dumps({'cadical_exit': r.returncode, 'seconds': info['cadical_seconds']}), flush=True)
if r.returncode != 20:
    json.dump(info, open(os.path.join(od, 'info.json'), 'w')); sys.exit(1)
info['lrat_bytes'] = os.path.getsize(lrat)
h = hashlib.sha256()
with open(lrat, 'rb') as f:
    for chunk in iter(lambda: f.read(1 << 24), b''): h.update(chunk)
info['lrat_sha256'] = h.hexdigest()
t = time.time()
c = subprocess.run([os.path.expanduser('~/.local/bin/cake_lpr'), cnf, lrat], capture_output=True, text=True)
info['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else (c.stdout + c.stderr)[-300:]
info['cake_seconds'] = round(time.time() - t, 1)
print(json.dumps({'cake_lpr': info['cake_lpr'], 'seconds': info['cake_seconds']}), flush=True)
# trace used original clauses
m = len(clauses); hints = {}; empty = None
with open(lrat) as f:
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
used_rows = sorted({owner[x - 1] for x in used if owner[x - 1] >= 0})
info['used_original_clauses'] = len(used); info['used_rows'] = len(used_rows)
json.dump([[list(rows[r][0]), rows[r][1]] for r in used_rows], open(os.path.join(od, 'used_rows.json'), 'w'))
os.remove(lrat)
json.dump(info, open(os.path.join(od, 'info.json'), 'w'), indent=1)
print(json.dumps(info), flush=True)

# p2_batch_cube.py (15 Nov 2026): copy of p2_batch.py with --cube s:bit,... (bit 1 = occupied = +sel, 0 = hole); the only changes are this line, the --cube option, CUBE and line 39.
"""Phase 2 (20:50 KST): lazy monolithic search with fresh CaDiCaL 2.1.3 solves (the solver that refuted level 11 in
455 s), so that the final UNSAT run already is the certificate run.
Iteration: write the certificate CNF of the current activated set (p2_write.py: eager clauses, the 12 clauses of every
activated quadruple, units, rows, sequential counter "at most L holes") into <dir>/it<k>/, run CaDiCaL 2.1.3 with
LRAT;  SAT -> read the model, add the violated (quadruple, order) pairs of the occupied owners (at most --capq, random),
delete the proof, repeat;  UNSAT -> save the state as <out>_L<L>.json with 'certdir' = that iteration's directory and
run p2_cert.sh on it (trim, cake_lpr, rows, p2_verify, cert.json) in this same unit.
usage: p2_batch.py --out p2/s12/c.json --dir p2/b12 --L 12 --rows mono/rows_1832.json --warm a.json,b.json [--tauclose]
                   [--capq 60000] [--secs N] [--seed 3]"""
import argparse, itertools, json, os, sys, time, subprocess, shutil
import numpy as np
import etv_common as ec, lazymono
assert ec.A == 4 and ec.B == 4 and ec.N == 70
ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True); ap.add_argument('--dir', required=True); ap.add_argument('--L', type=int, required=True)
ap.add_argument('--rows', default='none'); ap.add_argument('--warm', default=''); ap.add_argument('--tauclose', action='store_true')
ap.add_argument('--sb', action='store_true'); ap.add_argument('--cadopts', default=''); ap.add_argument('--capq', type=int, default=60000); ap.add_argument('--secs', type=float, default=30000); ap.add_argument('--seed', type=int, default=3)
ap.add_argument('--cube', default='')
a = ap.parse_args()
CUBE = [[int(s), int(b)] for s, b in (x.split(':') for x in a.cube.split(',') if x)]
assert all(0 <= s < ec.N and b in (0, 1) for s, b in CUBE) and len({s for s, _ in CUBE}) == len(CUBE), CUBE
PY = sys.executable; W = list(range(ec.N)); L = a.L; t0 = time.time()
cellidx = {frozenset((x + 1, y) for x in range(4) for y in range(1, f[x] + 1)): i for i, f in enumerate(ec.STATES)}
TAU = [cellidx[frozenset((b, x) for x, b in c)] for c in (frozenset((x + 1, y) for x in range(4) for y in range(1, f[x] + 1)) for f in ec.STATES)]
E = lazymono.LazyMono(W, emit=lambda c: None)       # numbering, chain atoms, model check (clauses are written by p2_write.py)
del E.cnf
def okquad(q): return len(set(q)) == 4 and all(E.can[x][y] for x, y in itertools.combinations(q, 2))
act = set()
for fn in [x for x in a.warm.split(',') if x]:
    for q in json.load(open(fn))['activated']:
        q = tuple(int(x) for x in q); assert okquad(q); act.add(q)
if a.tauclose:
    for q in list(act): act.add(tuple(TAU[x] for x in q))
E.activated = act
rng = np.random.default_rng(a.seed)
SBP = None
if a.sb:
    import p2_sb; SBP = p2_sb.default_pairs()
def log(d):
    d['t'] = time.strftime('%H:%M:%S'); d['secs'] = round(time.time() - t0, 1); print(json.dumps(d), flush=True)
def save(path, status, extra=None):
    d = {'W': W, 'L': L, 'status': status, 'rows_file': a.rows, 'cube': CUBE, 'activated': sorted(act), 'seconds': round(time.time() - t0, 1),
         'warm': a.warm, 'tauclose': a.tauclose, 'engine': 'p2_batch.py (CaDiCaL 2.1.3, fresh solves)', 'cadical_options': a.cadopts}
    if a.sb: d['sb_pairs'] = SBP
    if extra: d.update(extra)
    json.dump(d, open(path + '.tmp', 'w')); os.replace(path + '.tmp', path)
log({'event': 'start', 'L': L, 'warm_quads': len(act)})
k = 0
while time.time() - t0 < a.secs:
    k += 1; d = os.path.join(a.dir, f'it{k}'); os.makedirs(d, exist_ok=True)
    save(a.out, f'iteration {k}')
    r = subprocess.run([PY, '-u', 'p2_write.py', a.out, d, 'keep' if a.rows != 'none' else 'none'], capture_output=True, text=True)
    if r.returncode: log({'event': 'write failed', 'err': r.stderr[-500:]}); break
    lay = json.load(open(os.path.join(d, 'layout.json')))
    ts = time.time()
    with open(os.path.join(d, 'cadical.log'), 'w') as g:
        rc = subprocess.run(['cadical'] + a.cadopts.split() + ['--lrat=true', '--binary=false', os.path.join(d, 'cert.cnf'), os.path.join(d, 'cert.lrat')], stdout=g, stderr=subprocess.STDOUT).returncode
    with open(os.path.join(d, 'cadical.log'), 'a') as g: g.write(f'exit {rc}\n')
    sol = round(time.time() - ts, 1)
    if rc == 20:
        log({'event': 'UNSAT', 'budget': L, 'iteration': k, 'activated': len(act), 'clauses': lay['clauses'], 'solve_secs': sol, 'certdir': d})
        save(a.out.replace('.json', f'_L{L}.json'), f'UNSAT at budget {L}', {'certdir': d})
        save(a.out, f'UNSAT at budget {L}', {'certdir': d})
        c = subprocess.run(['./p2_cert.sh', d], capture_output=True, text=True)
        log({'event': 'p2_cert.sh', 'exit': c.returncode, 'certdir': d})
        break
    if rc != 10:
        log({'event': 'cadical ended without verdict', 'exit': rc, 'solve_secs': sol}); break
    model = []
    for line in open(os.path.join(d, 'cadical.log')):
        if line.startswith('v '): model.extend(int(x) for x in line.split()[1:])
    model = [x for x in model if x != 0]
    vals = [0] * (E.top + 1)
    for x in model:
        if abs(x) <= E.top: vals[abs(x)] = x
    viol, holes, order = E.violated(vals[1:])
    new = [q for q in viol if q not in act]
    for f in ('cert.lrat', 'cert.cnf'):
        p = os.path.join(d, f)
        if os.path.exists(p): os.remove(p)
    if not new:
        log({'event': 'SAT_MODEL', 'budget': L, 'holes': holes, 'n_holes': len(holes), 'hole_states': [''.join(map(str, ec.STATES[h])) for h in holes],
             'x_order': [int(i) for i in order], 'iteration': k, 'activated': len(act)})
        save(a.out, f'SAT at budget {L}'); break
    if len(new) > a.capq:
        idx = rng.choice(len(new), a.capq, replace=False); new = [new[i] for i in idx]
    act.update(new)
    log({'event': 'iter', 'it': k, 'budget': L, 'solve_secs': sol, 'violated': len(viol), 'added': len(new), 'activated': len(act),
         'clauses': lay['clauses'], 'holes': sorted(holes)})
else:
    save(a.out, 'time limit')
log({'event': 'end', 'iterations': k, 'activated': len(act)})

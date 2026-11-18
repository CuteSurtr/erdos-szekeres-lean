"""Phase 2 (20:40 KST) version of lazymono.py: the same CNF (lazymono.LazyMono: eager pair/triple clauses of mono66,
lazily activated quadruple clauses, fixed states, optional cube units, optional demand-one row hints, a totalizer for
the number of holes), with
  * warm start: the activated (quadruple, order) pairs of earlier state files are added before the first solve
    (every quadruple's clauses belong to mono66's CNF, so any set of them may be added);
  * optional mirror closure of the activated set (tau maps the clauses of (a,b,c,d) onto those of (ta,tb,tc,td));
  * a log line per iteration and the state file rewritten after every iteration (activated set, status), so a stop
    loses at most the current solve call;
  * one budget L per run: on UNSAT the state is saved as <out>_L<L>.json (status 'UNSAT at budget L') and the run ends
    (the certificate is written from that file by p2_write.py; this run is discovery only).
usage: p2_lazymono.py --out S.json --L 12 [--rows mono/rows_1832.json] [--warm a.json,b.json] [--tauclose]
                      [--cube 32:0,37:1] [--seed 1] [--capq 30000] [--maxq 1500000] [--secs 30000]"""
import argparse, itertools, json, os, sys, time
import numpy as np
from pysat.solvers import Solver
from pysat.card import ITotalizer
import etv_common as ec, lazymono
assert ec.A == 4 and ec.B == 4 and ec.N == 70
ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True); ap.add_argument('--L', type=int, required=True)
ap.add_argument('--rows', default='none'); ap.add_argument('--warm', default='')
ap.add_argument('--tauclose', action='store_true'); ap.add_argument('--cube', default='')
ap.add_argument('--seed', type=int, default=1); ap.add_argument('--capq', type=int, default=30000)
ap.add_argument('--maxq', type=int, default=1500000); ap.add_argument('--secs', type=float, default=30000)
ap.add_argument('--solver', default='cadical195')
a = ap.parse_args()
cellidx = {frozenset((x + 1, y) for x in range(4) for y in range(1, f[x] + 1)): i for i, f in enumerate(ec.STATES)}
TAU = [cellidx[frozenset((b, x) for x, b in c)] for c in (frozenset((x + 1, y) for x in range(4) for y in range(1, f[x] + 1)) for f in ec.STATES)]
t0 = time.time(); L = a.L
W = list(range(ec.N))
s = Solver(name=a.solver); ncl = [0]
def emit(c): s.add_clause(c); ncl[0] += 1
E = lazymono.LazyMono(W, emit=emit)
for st in ec.FIXED_OCC: emit([E.sel[st]])
CUBE = [(int(x.split(':')[0]), int(x.split(':')[1])) for x in a.cube.split(',') if x]
for st_, bit in CUBE: emit([E.sel[st_] if bit else E.nsel[st_]])
nrows = 0
if a.rows != 'none':
    for supp, dd in json.load(open(a.rows)):
        if dd == 1: emit([E.nsel[x] for x in supp]); nrows += 1
tot = ITotalizer(lits=[E.nsel[i] for i in range(E.n) if W[i] not in ec.FIXED_OCC], ubound=L + 2, top_id=E.top)
for c in tot.cnf.clauses: emit(c)
def okquad(q):
    return all(E.can[x][y] for x, y in itertools.combinations(q, 2)) and len(set(q)) == 4
def activate(q):
    q = tuple(int(x) for x in q)
    if q in E.activated: return 0
    assert okquad(q), q
    E.activated.add(q)
    for c in E.quad_clauses(*q): emit(c)
    return 1
nwarm = 0
for fn in [x for x in a.warm.split(',') if x]:
    for q in json.load(open(fn))['activated']: nwarm += activate(q)
if a.tauclose:
    for q in list(E.activated): nwarm += activate(tuple(TAU[x] for x in q))
def log(d):
    d['t'] = time.strftime('%H:%M:%S'); d['secs'] = round(time.time() - t0, 1); print(json.dumps(d), flush=True)
log({'event': 'built', 'L': L, 'rows': nrows, 'cube': CUBE, 'warm_quads': nwarm, 'clauses': ncl[0], 'tauclose': a.tauclose, 'seed': a.seed})
it = 0; rng = np.random.default_rng(a.seed)
def save(status, path=None):
    path = path or a.out
    json.dump({'W': W, 'L': L, 'status': status, 'rows_file': a.rows, 'cube': CUBE, 'activated': sorted(E.activated), 'iterations': it,
               'seconds': round(time.time() - t0, 1), 'warm': a.warm, 'tauclose': a.tauclose, 'seed': a.seed}, open(path + '.tmp', 'w'))
    os.replace(path + '.tmp', path)
save('running')
while time.time() - t0 < a.secs:
    it += 1; ts = time.time()
    r = s.solve(assumptions=[-tot.rhs[L]])
    if not r:
        log({'event': 'UNSAT', 'budget': L, 'holes_at_least': L + 1, 'iterations': it, 'activated': len(E.activated), 'clauses': ncl[0],
             'solve_secs': round(time.time() - ts, 1)})
        save(f'UNSAT at budget {L}', a.out.replace('.json', f'_L{L}.json')); save(f'UNSAT at budget {L}')
        break
    viol, holes, order = E.violated(s.get_model())
    new = [q for q in viol if q not in E.activated]
    if not new:
        log({'event': 'SAT_MODEL', 'budget': L, 'holes': holes, 'n_holes': len(holes), 'hole_states': [''.join(map(str, ec.STATES[h])) for h in holes],
             'x_order': [W[int(i)] for i in order], 'iterations': it, 'activated': len(E.activated)})
        save(f'SAT at budget {L}'); break
    if len(new) > a.capq:
        sel_idx = rng.choice(len(new), a.capq, replace=False); new = [new[i] for i in sel_idx]
    for q in new: activate(q)
    log({'event': 'iter', 'it': it, 'budget': L, 'solve_secs': round(time.time() - ts, 1), 'violated': len(viol), 'added': len(new),
         'activated': len(E.activated), 'clauses': ncl[0], 'holes': sorted(holes)})
    save('running')
    if len(E.activated) > a.maxq:
        log({'event': 'STOP_MAXQ', 'activated': len(E.activated)}); save('stopped: MAXQ'); break
else:
    save('time limit')
log({'event': 'end', 'budget': L, 'iterations': it, 'activated': len(E.activated), 'clauses': ncl[0]})

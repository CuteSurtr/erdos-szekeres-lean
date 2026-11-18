#!/usr/bin/env python3
"""cegar.py CNF N [tlim] [mode] -- discovery tool (NOT a certificate): occupancy-level CEGAR on an
owner model.  Outer: SAT over occupancy with 'at least N occupied' + learned clauses.
Inner: the owner CNF under the candidate pattern as assumptions; UNSAT core -> learned clause."""
import sys, pickle, time, json
sys.path.insert(0, '.')
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
import cat_common
cnf = sys.argv[1]; N = int(sys.argv[2]); tlim = float(sys.argv[3]) if len(sys.argv) > 3 else 60
mode = sys.argv[4] if len(sys.argv) > 4 else 'exact'
meta = pickle.load(open(cnf + '.names.pkl', 'rb'))
names = meta['names']
states, cells, capH, cupH, D = cat_common.make(meta['CA'], meta['CB'])
NS = len(states)
occ = [names[('occ', s)] for s in range(NS)]
t0 = time.time()
inner = Solver(name='cadical153', bootstrap_with=CNF(from_file=cnf).clauses)
print('loaded', round(time.time() - t0, 1), flush=True)
outer = Solver(name='cadical153')
ov = list(range(1, NS + 1))
card = CardEnc.atleast(lits=ov, bound=N, top_id=NS, encoding=EncType.seqcounter)
for c in card.clauses: outer.add_clause(c)
e0 = states.index(tuple([0] * meta['CA'])); e1 = states.index(tuple([1] + [0] * (meta['CA'] - 1)))
outer.add_clause([ov[e0]]); outer.add_clause([ov[e1]])
it = 0; tin = 0; sizes = []; npos = []
learned = []
while True:
    if time.time() - t0 > tlim:
        print('TIMEOUT'); break
    if not outer.solve():
        print('OUTER UNSAT after', it, 'iterations'); break
    m = outer.get_model()
    pat = [m[s] > 0 for s in range(NS)]
    if mode == 'exact':
        ass = [occ[s] if pat[s] else -occ[s] for s in range(NS)]
    else:
        ass = [occ[s] for s in range(NS) if pat[s]]
    t1 = time.time()
    r = inner.solve(assumptions=ass)
    tin += time.time() - t1
    it += 1
    if r:
        print('INNER SAT: pattern realizable in the model', [states[s] for s in range(NS) if pat[s]]); break
    core = inner.get_core()
    o2s = {occ[s]: s for s in range(NS)}
    cl = [-(ov[o2s[abs(l)]]) if l > 0 else ov[o2s[abs(l)]] for l in core]
    outer.add_clause(cl)
    learned.append(cl)
    sizes.append(len(cl)); npos.append(sum(1 for l in cl if l > 0))
    if it % 500 == 0:
        print(it, 'iters', round(time.time() - t0, 1), 's inner', round(tin, 1), 'avg core', round(sum(sizes[-500:]) / 500, 1), 'avg pos lits', round(sum(npos[-500:]) / 500, 1), flush=True)
print(json.dumps({'iters': it, 'time': round(time.time() - t0, 1), 'inner': round(tin, 1), 'avg_core': round(sum(sizes) / max(1, len(sizes)), 2)}))
json.dump(learned, open(cnf + '.cegar_%s.json' % mode, 'w'))

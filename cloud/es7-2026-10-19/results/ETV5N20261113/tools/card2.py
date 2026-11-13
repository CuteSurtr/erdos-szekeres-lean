"""Experiment: demand-2 rows from the coupled CNF with optional owners.  For a support T, every clause is
guarded by the selectors of the owners it mentions (as in engine.minimize_fast), and at least |T|-1
selectors must be true.  UNSAT means: at most |T|-2 states of T are occupied (demand 2).
Candidates: unions of two known cores with large overlap.  usage: card2.py <max_pairs> <max_union>"""
import json, sys, time, itertools, random
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
import engine, coupled5
maxp, maxu = int(sys.argv[1]), int(sys.argv[2])
cores = [tuple(json.loads(l)['support']) for l in open('cores.jsonl')]
pairs = []
for a, b in itertools.combinations(range(len(cores)), 2):
    u = set(cores[a]) | set(cores[b])
    if len(u) <= maxu: pairs.append((len(u), a, b))
pairs.sort(); rng = random.Random(1)
def demand2(T):
    n = len(T); nv, stat, vown = engine.static_with_owners(n)
    dyn, d = engine.dyn_clauses(list(T))
    sel = [nv + 1 + i for i in range(n)]
    pool = IDPool(start_from=nv + n + 1)
    s = Solver(name='cadical195')
    for c, own in stat: s.add_clause(c + [-sel[o] for o in own])
    for c, t in dyn:
        own = set(t[1:4]) if t[0] == 'positive' else set(t[1:3])
        s.add_clause(c + [-sel[o] for o in own])
    for c in CardEnc.atleast(lits=sel, bound=n - 1, vpool=pool, encoding=EncType.seqcounter).clauses: s.add_clause(c)
    r = s.solve(); s.delete(); return not r
t0 = time.time(); tested = 0; found = []
for k, a, b in pairs[:maxp]:
    T = tuple(sorted(set(cores[a]) | set(cores[b])))
    tested += 1
    if demand2(T):
        found.append(T); print(json.dumps({'event': 'demand2', 'size': len(T), 'support': T}), flush=True)
print(json.dumps({'pairs_tested': tested, 'demand2_rows': len(found), 'seconds': round(time.time() - t0, 1), 'pair_union_sizes': sorted(set(p[0] for p in pairs[:maxp]))}))
json.dump(found, open('card2_found.json', 'w'))

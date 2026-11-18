import sys, pickle, random, time
sys.path.insert(0, '.')
from pysat.formula import CNF
from pysat.solvers import Solver
import cat_common
cnf = sys.argv[1]; Nocc = int(sys.argv[2]); trials = int(sys.argv[3]); mode = sys.argv[4]
meta = pickle.load(open(cnf + '.names.pkl', 'rb'))
names = meta['names']
states, cells, capH, cupH, D = cat_common.make(meta['CA'], meta['CB'])
NS = len(states)
occ = [names[('occ', s)] for s in range(NS)]
t0 = time.time()
S = Solver(name='cadical153', bootstrap_with=CNF(from_file=cnf).clauses)
print('loaded', round(time.time() - t0, 1), flush=True)
random.seed(1)
e0 = states.index(tuple([0] * meta['CA'])); e1 = states.index(tuple([1] + [0] * (meta['CA'] - 1)))
res = {'up_conflict': 0, 'sat': 0, 'unsat_search': 0}
tt = 0
for it in range(trials):
    rest = [s for s in range(NS) if s not in (e0, e1)]
    sub = set(random.sample(rest, Nocc - 2)) | {e0, e1}
    if mode == 'exact':
        ass = [occ[s] if s in sub else -occ[s] for s in range(NS)]
    else:
        ass = [occ[s] for s in sub]
    st, lits = S.propagate(assumptions=ass)
    if not st:
        res['up_conflict'] += 1
    else:
        t1 = time.time()
        r = S.solve(assumptions=ass)
        tt += time.time() - t1
        res['sat' if r else 'unsat_search'] += 1
print(res, 'search time', round(tt, 1))

"""Search for a REALIZABLE counterexample to a restricted statement: enumerate models of the restricted eager CNF
(pysat CaDiCaL, blocking clauses + random phase assumptions), re-check each exactly, try to realize it by points.
usage: find_real.py a n m weak|strong allow max_models [seed]"""
import sys, json, os, random, itertools, time
from eager_cert import Enc, exact_sets
from realize import realize
from pysat.solvers import Cadical153, Glucose4
comb = itertools.combinations
a, n, m, form, allow, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6])
seed = int(sys.argv[7]) if len(sys.argv) > 7 else 1
rnd = random.Random(seed); t0 = time.time()
E = Enc(a, n, m, form == 'strong'); E.restrict(allow)
sol = Cadical153(bootstrap_with=E.base + E.wit)
for D in E.pool(0, m): sol.add_clause(E.pool_clause(D))
tris = list(comb(range(m), 3)); name = 'restr_%s_%s_a%d_n%d_m%d' % (allow, form, a, n, m)
for it in range(N):
    vs = list(range(1, E.ntri + 1)); rnd.shuffle(vs)
    ass = [v if rnd.random() < 0.5 else -v for v in vs[:len(vs) // 20]]
    ok = sol.solve(assumptions=ass)
    if not ok: ok = sol.solve()
    if not ok: print('no more models', flush=True); break
    mod = sol.get_model(); o = {t: mod[E.tri[t] - 1] > 0 for t in tris}
    sol.add_clause([-mod[E.tri[t] - 1] for t in tris])
    s = ''.join('+' if o[t] else '-' for t in tris)
    P = realize(m, s, restarts=12, seed=seed * 100 + it)
    print(name, 'model', it, 'realized' if P else 'not realized', '%.0fs' % (time.time() - t0), flush=True)
    if P:
        json.dump({'name': name + '_real', 'a': a, 'n': n, 'm': m, 'kind': 'allow=' + allow, 'form': form, 'signs': s, 'realized': True, 'P': P},
                  open(os.path.join('cex', name + '_real.json'), 'w'))
        break

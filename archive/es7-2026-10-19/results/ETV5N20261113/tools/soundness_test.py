"""Soundness control: real point sets of the class; every clause of the coupled CNF must hold under
the exact geometric assignment, for random owner subsets in random index order."""
import random, sys, json, time
import etv_common as ec
from coupled5 import CNF
from geom import greedy_set, states, assignment, check_clauses, ok_class, max_convex
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
nsets = int(sys.argv[2]) if len(sys.argv) > 2 else 10
t0 = time.time(); total = 0; tot_cl = 0; sizes = []
for it in range(nsets):
    P = greedy_set(rng, tries=300, R=rng.choice([10**3, 10**6]), target=rng.randrange(14, 30))
    st, Em, Ep = states(P)
    assert len(set(st)) == len(st), 'state separation violated?!'
    assert st[0] == ec.FIXED_OCC[0] and (len(st) < 2 or st[1] == ec.FIXED_OCC[1])
    sizes.append(len(P))
    for rep in range(4):
        k = min(len(P), rng.randrange(8, 13))
        owners = rng.sample(range(len(P)), k)
        S = [st[o] for o in owners]
        cnf = CNF(S)
        val = assignment(cnf, P, owners)
        bad = check_clauses(cnf, val)
        total += 1; tot_cl += len(cnf.clauses)
        if bad:
            print('VIOLATION', P, owners, bad[:5]); sys.exit(1)
print(json.dumps({'sets': nsets, 'sizes': sizes, 'cnfs': total, 'clauses_checked': tot_cl, 'violations': 0,
                  'seconds': round(time.time() - t0, 1)}))

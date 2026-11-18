"""Controls for wit.py on real point sets (exact orientations fixed by unit clauses)."""
import sys, json, random, glob, os, itertools
os.environ['FL_TMP'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
import fl, wit
from fl import *
from esgeo import orient, quick
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
maxn = int(sys.argv[2]) if len(sys.argv) > 2 else 24
nsets = int(sys.argv[3]) if len(sys.argv) > 3 else 10
sets = []
for fn in sorted(glob.glob('pool_*.jsonl')) + sorted(glob.glob('sets_*.jsonl')):
    for rec in load_jsonl(fn):
        sets.append(sorted(tuple(p) for p in rec['P']))
rng.shuffle(sets)
stats = {'pos': 0, 'pos_pad': 0, 'neg_state': 0, 'neg_invalid': 0, 'bad': 0}
def units(w, P):
    return [[w.o[t] if orient(P[t[0]], P[t[1]], P[t[2]]) > 0 else -w.o[t]] for t in itertools.combinations(range(len(P)), 3)]
done = 0
for P0 in sets:
    if done >= nsets: break
    # random valid sub-configuration with at most maxn points (prefix-closed subsets keep validity)
    P = sorted(rng.sample(P0, min(len(P0), rng.randint(8, maxn))))
    S = Set66(P)
    if not S.ok: continue
    done += 1
    n = S.n; occ = sorted(set(S.in_state))
    # positive: random occupied states, last point's state included (last present point must be an owner)
    k = rng.randint(1, 4)
    T = list({S.in_state[n - 1]} | set(rng.sample(occ, min(k, len(occ)))))
    w = wit.Wit(n, T, flags=False)
    st, model = wit.solve_cnf(w.dimacs(units(w, P)))
    if st != 'SAT': stats['bad'] += 1; print('POSITIVE CONTROL FAILED', P, T)
    else:
        ok, det = wit.check_model(w, model)
        if not ok or det[4] != S.in_state: stats['bad'] += 1; print('DECODE MISMATCH', det)
        else: stats['pos'] += 1
    # positive with padding: n+2 points, flags on, o fixed only on the real triples
    w2 = wit.Wit(n + 2, T, flags=True)
    st, model = wit.solve_cnf(w2.dimacs(units(w2, P) + [[-w2.pres[n]]]))
    if st != 'SAT': stats['bad'] += 1; print('PAD CONTROL FAILED', P, T)
    else: stats['pos_pad'] += 1
    # negative: a state that is not occupied
    non = [i for i in range(N) if i not in occ]
    T2 = T + [rng.choice(non)]
    w3 = wit.Wit(n, T2, flags=False)
    st, model = wit.solve_cnf(w3.dimacs(units(w3, P)))
    if st != 'UNSAT': stats['bad'] += 1; print('NEGATIVE (state) CONTROL FAILED', P, T2)
    else: stats['neg_state'] += 1
    # negative: an invalid set (add a random point until the set is not (6,6;8)), states of the last point
    for _ in range(2000):
        x = (rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6))
        Q = sorted(P + [x])
        try:
            g, mc, mu = quick(Q)
        except Exception: continue
        if g < 0: continue
        if g >= 8 or mc >= 6 or mu >= 6:
            w4 = wit.Wit(len(Q), [], flags=False, last_owner=False)
            st, model = wit.solve_cnf(w4.dimacs(units(w4, Q)))
            if st != 'UNSAT': stats['bad'] += 1; print('NEGATIVE (invalid set) CONTROL FAILED', Q)
            else: stats['neg_invalid'] += 1
            break
print(stats)

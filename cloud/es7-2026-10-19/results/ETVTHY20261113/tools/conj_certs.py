"""Certificates for the Delta-reduction tests: for each set, a strong Delta (4-cap-free, no convex k-gon, meeting
every convex k-gon), found by CP-SAT and then re-verified by the independent pure-Python exact checker."""
import sys, json, random, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta_strong import delta_strong
from pyexact import chains

def py_check(P, D, k):
    """Pure-Python: Delta has no 4-cap and no convex k-gon; complement has no convex k-gon."""
    Ds = [P[i] for i in D]; R = [P[i] for i in range(len(P)) if i not in set(D)]
    ok = True
    if len(Ds) >= 2:
        _, _, capB, cupB = chains(Ds)
        if max(capB.values()) >= 4: ok = False
        if max(capB[x] + cupB[x] - 2 for x in capB) >= k: ok = False
    if len(R) >= 2:
        _, _, capB, cupB = chains(R)
        if max(capB[x] + cupB[x] - 2 for x in capB) >= k: ok = False
    return ok

if __name__ == '__main__':
    random.seed(1); k = int(sys.argv[1]); out = sys.argv[2]
    for fn in sys.argv[3:]:
        sets = [json.load(open(fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(fn)]
        for si, P in enumerate(sets):
            P = sorted(tuple(p) for p in P); t0 = time.time()
            D, st, rounds = delta_strong(P, k)
            ver = py_check(P, D, k) if D is not None else None
            with open(out, 'a') as f:
                f.write(json.dumps({'file': os.path.basename(fn), 'index': si, 'n': len(P), 'k': k, 'status': st,
                                    'Delta': D, 'py_verified': ver}) + '\n')
            print(fn, si, len(P), st, 'Delta', len(D) if D else None, 'pyverified', ver, '%.1fs' % (time.time()-t0), flush=True)

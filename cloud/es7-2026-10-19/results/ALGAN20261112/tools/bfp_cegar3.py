"""BFP-CEGAR, stage 3: stage 2 plus 5-layer subsets.
Solver input: gp_m4K8t14.work.cnf + added_clauses.cnf (stage 2) + added_clauses3.cnf (this stage, if present: resume).
Clauses are loaded and written with duplicate literals and duplicate clauses removed.
A 5-layer pattern is cut on every increasing 5-tuple of layers (as 4-layer patterns were in stage 2).
Certificates are made sparse first: a few reweighted-L1 LP rounds pick a support touching few rotation orbits
(heuristic choice only), then find_cert computes the exact integer certificate on that support and check_cert
re-checks it. Fewer orbits used means shorter, stronger cut clauses.
New clauses go to added_clauses3.cnf, certificates to certs3/."""
import sys, json, time, itertools, os
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, '.')
import bfp_cegar2 as B
from bfpcert import rows_for, find_cert, check_cert

E, t, ids = B.E, B.t, B.ids


def _brackets(r):
    a, b, c, d, e = r['rel']
    return {ids[tuple(sorted(x))] for x in ((a, b, c), (a, d, e), (a, b, d), (a, c, e), (a, b, e), (a, c, d))}


def sparse_support(R, rounds=6):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix, vstack
    vars_ = sorted({v for r in R for v in r['G'] + r['L']}); vi = {v: i for i, v in enumerate(vars_)}
    rr = []; cc = []; vv = []
    for i, r in enumerate(R):
        for v in r['G']: rr.append(vi[v]); cc.append(i); vv.append(1)
        for v in r['L']: rr.append(vi[v]); cc.append(i); vv.append(-1)
    M = coo_matrix((vv, (rr, cc)), shape=(len(vars_), len(R))).tocsr()
    A = vstack([M, np.ones((1, len(R)))]).tocsr(); b = np.zeros(len(vars_) + 1); b[-1] = 1
    BR = [_brackets(r) for r in R]; allv = set().union(*BR); w = dict.fromkeys(allv, 1.0)
    best = None; last = None
    for _ in range(rounds):
        res = linprog(np.array([sum(w[v] for v in br) for br in BR]), A_eq=A, b_eq=b,
                      bounds=[(0, None)] * len(R), method='highs')
        if res.status != 0:
            break
        supp = [i for i, x in enumerate(res.x) if x > 1e-9]
        nv = len(set().union(*(BR[i] for i in supp)))
        if best is None or nv < best[0]:
            best = (nv, supp)
        if nv == last:
            break
        last = nv; u = dict.fromkeys(allv, 0.0)
        for i in supp:
            for v in BR[i]: u[v] += res.x[i]
        w = {v: 1.0 / (1e-4 + u[v]) for v in allv}
    return None if best is None else best[1]


def _cert_sparse(L):
    chi = B.CHI
    Sx = [l * 4 + k for l in L for k in range(4)]
    R = rows_for(chi, Sx, ids)
    supp = sparse_support(R)
    cert = find_cert([R[i] for i in supp]) if supp else None
    how = 'sparse'
    if not isinstance(cert, list):
        cert = find_cert(R); how = 'dense'
    if not isinstance(cert, list):
        return L, None, 'extract failed %s' % cert
    ok, msg = check_cert(chi, cert, ids)
    if not ok:
        return L, None, 'check failed ' + msg
    pos = {L[p] * 4 + k: p * 4 + k for p in range(len(L)) for k in range(4)}
    used = {}
    for r, w in cert:
        a, b, c, d, e = r['rel']
        for x in ((a, b, c), (a, d, e), (a, b, d), (a, c, e), (a, b, e), (a, c, d)):
            used[tuple(pos[v] for v in x)] = int(chi[x[0], x[1], x[2]])
    return L, dict(cert=[dict(rel=r['rel'], j=r['j'], k=r['k'], w=w) for r, w in cert], used=sorted(used.items()),
                   how=how), 'ok'


def tuples_for(size):
    if size == 3:
        return itertools.permutations(range(t), 3)
    return itertools.combinations(range(t), size)


if __name__ == '__main__':
    from pysat.solvers import Cadical195
    TLIM = float(sys.argv[1]); NP = int(sys.argv[2]); T0 = time.time()
    log = open('bfp_cegar3.log', 'a'); os.makedirs('certs3', exist_ok=True)

    def P(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); log.write(s + '\n'); log.flush()

    S = Cadical195(); seen_cl = set(); nload = {}
    for fn in ('gp_m4K8t14.work.cnf', 'added_clauses.cnf', 'added_clauses3.cnf'):
        if not os.path.exists(fn):
            continue
        k = 0
        with open(fn) as f:
            for line in f:
                if line[0] in 'pc':
                    continue
                cl = tuple(sorted(set(map(int, line.split()[:-1]))))
                h = hash(cl)
                if not cl or h in seen_cl:
                    continue
                seen_cl.add(h); S.add_clause(list(cl)); k += 1
        nload[fn] = k
    add = open('added_clauses3.cnf', 'a')

    def ADD(cl):
        cl = tuple(sorted(set(cl))); h = hash(cl)
        if h in seen_cl:   # a hash collision could only drop a clause: weaker, never unsound
            return 0
        seen_cl.add(h); S.add_clause(list(cl)); add.write(' '.join(map(str, cl)) + ' 0\n')
        return 1

    def cut(used, size):
        c = 0
        for Lp in tuples_for(size):
            cl = []
            for (a, b, cc), s in used:
                A = Lp[a // 4] * 4 + a % 4; Bq = Lp[b // 4] * 4 + b % 4; C = Lp[cc // 4] * 4 + cc % 4
                l = E.o(A, Bq, C); cl.append(-l if s > 0 else l)
            c += ADD(cl)
        return c

    npat = {3: 0, 4: 0, 5: 0}
    for f in os.listdir('certs3'):
        npat[int(f[1])] += 1
    P('stage3 start: distinct clauses loaded', nload, 'existing stage-3 patterns', npat)
    it = 0
    while time.time() - T0 < TLIM:
        t1 = time.time(); ok = S.solve(); ts = time.time() - t1
        if not ok:
            P('iter', it, 'UNSAT (solve %.0fs)' % ts, 'patterns', npat, 'elapsed %.0fs' % (time.time() - T0)); break
        model = S.get_model(); chi = B.chi_of(model); gv = B.gp_viol(chi)
        if gv:
            na = 0
            for rel in gv:
                for cl in B.gp_clauses(E, *rel):
                    na += ADD(cl)
            P('iter', it, 'solve %.0fs' % ts, 'GP violations', len(gv), 'clauses', na); it += 1; continue
        found = False
        for size in (3, 4, 5):
            t2 = time.time()
            with Pool(NP, initializer=B._init, initargs=(chi,)) as pool:
                bad = [L for L, r in pool.imap_unordered(B._test, itertools.combinations(range(t), size), chunksize=4)
                       if r != 'FEAS']
                if not bad:
                    continue
                tt = time.time() - t2
                res = pool.map(_cert_sparse, bad, chunksize=1)
            newp = 0; ncl = 0
            for L, d, msg in res:
                if d is None:
                    P('  ', L, msg); continue
                newp += 1; npat[size] += 1
                json.dump(dict(size=size, layers=L, **d), open('certs3/s%d_%05d.json' % (size, npat[size]), 'w'))
                ncl += cut([(tuple(tr), s) for tr, s in d['used']], size)
            P('iter', it, 'solve %.0fs' % ts, 'size', size, 'bad subsets', len(bad), 'test %.0fs' % tt,
              'certs %.0fs' % (time.time() - t2 - tt), 'new patterns', newp, 'new clauses', ncl, 'patterns', npat,
              'elapsed %.0fs' % (time.time() - T0))
            found = True; break
        if not found:
            P('iter', it, 'model GP-consistent and BFP-clean on all 3-, 4- and 5-layer subsets -> saved')
            json.dump(sorted(x for x in model if x > 0), open('bfp5clean_model_%d.json' % it, 'w')); break
        it += 1
    else:
        P('time limit; patterns', npat, 'elapsed %.0fs' % (time.time() - T0))
    add.close()

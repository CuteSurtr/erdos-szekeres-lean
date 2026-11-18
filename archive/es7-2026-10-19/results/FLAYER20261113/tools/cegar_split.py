"""Complete test of the strong (Pascal) split for ALL abstract FL(a,b)-signotopes on n points (CEGAR).

Loop: (1) SAT: an FL(a,b)-signotope sigma for which none of the partitions collected so far is a valid split;
      (2) find a valid split (S1,S2) of sigma (split.py); if none exists, sigma is a counterexample;
      (3) add the clause "the partition (S1,S2) is not a valid split": some (a-1)-cap or ((a-2),(b-1))-gon
          inside S1, or some (b-1)-cup or ((a-1),(b-2))-gon inside S2 (auxiliary variables, one-directional).
UNSAT in (1) means: every FL(a,b)-signotope on n points has one of the collected partitions as a valid strong
split.  The final CNF is written for certification (CaDiCaL LRAT + cake_lpr, cert_cnf.py).
usage: cegar_split.py a b n [max_iters]"""
import sys, itertools, json, time, os
from pysat.solvers import Cadical153
import fls, split

def run(a, b, n, max_iters=10**6, log=sys.stdout, weak=False, time_limit=None, rss_limit_mb=None):
    w = fls.FL(a, b, n); so = Cadical153(bootstrap_with=w.cl)
    extra = []          # clauses added on top of w.cl (aux definitions and blocking clauses)
    aux = {}
    def add(c):
        extra.append(c); so.add_clause(c)
    def chainvar(sgn, idx):
        key = (sgn, idx)
        if key not in aux:
            v = w.new(); aux[key] = v
            for i in range(len(idx) - 2): add([-v, sgn * w.o[idx[i], idx[i + 1], idx[i + 2]]])
        return aux[key]
    def gonvar(capidx, cupidx):
        key = ('g', capidx, cupidx)
        if key not in aux:
            g = w.new(); aux[key] = g
            for (sgn, idx) in ((-1, capidx), (1, cupidx)):
                if len(idx) >= 3: add([-g, chainvar(sgn, idx)])
        return aux[key]
    def bad_structures(S, capL, gcap, gcup):
        """literals: S contains a chain of sign given below with capL points, or a (gcap-cap, gcup-cup)-gon"""
        lits = []
        return lits
    def block(S1, S2):
        lits = []
        # S1: an (a-1)-cap ; a ((a-2)-cap,(b-1)-cup)-gon
        for idx in itertools.combinations(S1, a - 1): lits.append(chainvar(-1, idx))
        lits += gons(S1, a - 2, b - 1)
        # S2: a (b-1)-cup ; an ((a-1)-cap,(b-2)-cup)-gon
        for idx in itertools.combinations(S2, b - 1): lits.append(chainvar(1, idx))
        if not weak: lits += gons(S2, a - 1, b - 2)
        add(lits)
    def gons(S, lc, lu):
        """all (lc-cap, lu-cup)-gons with vertices in S (index sets), lc, lu >= 2"""
        out = []
        ic, iu = lc - 2, lu - 2
        for ui in range(len(S)):
            for vi in range(ui + 1, len(S)):
                mid = S[ui + 1:vi]
                if len(mid) < ic + iu: continue
                for cs in itertools.combinations(mid, ic):
                    rest = [p for p in mid if p not in cs]
                    for us in itertools.combinations(rest, iu):
                        capidx = (S[ui],) + cs + (S[vi],); cupidx = (S[ui],) + us + (S[vi],)
                        if ic == 0 and iu == 0: continue
                        out.append(gonvar(capidx, cupidx))
        return out
    T = list(itertools.combinations(range(n), 3)); t0 = time.time(); parts = []
    import resource
    for it in range(max_iters):
        if time_limit and time.time() - t0 > time_limit: break
        if rss_limit_mb and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 > rss_limit_mb:
            print(f'  stopped by the internal memory limit ({rss_limit_mb} MB) after {it} iterations', file=log, flush=True); break
        if not so.solve():
            return 'ALL_SPLIT', parts, w, extra
        m = set(x for x in so.get_model() if x > 0)
        sg = {t: (1 if w.o[t] in m else -1) for t in T}
        f = lambda i, j, k: sg[i, j, k]
        ok, S1, ncl = split.split(n, f, a, b, weak=weak)
        if not ok:
            sig = ''.join('+' if sg[t] > 0 else '-' for t in T)
            return 'COUNTEREXAMPLE', sig, w, extra
        if not weak: assert split.check_split(n, f, a, b, S1)
        S1 = sorted(S1); S2 = [p for p in range(n) if p not in set(S1)]
        parts.append(S1); block(S1, S2)
        if (it + 1) % 200 == 0: print(f'  n={n} iteration {it+1}, aux {len(aux)}, {time.time()-t0:.0f}s', file=log, flush=True)
    return 'LIMIT', parts, w, extra

if __name__ == '__main__':
    a, b, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    mx = int(sys.argv[4]) if len(sys.argv) > 4 else 10**6
    weak = len(sys.argv) > 5 and sys.argv[5] == 'weak'
    tag = 'weak' if weak else 'split'
    tl = float(sys.argv[6]) if len(sys.argv) > 6 else None; rl = float(sys.argv[7]) if len(sys.argv) > 7 else None
    t0 = time.time(); st, info, w, extra = run(a, b, n, mx, weak=weak, time_limit=tl, rss_limit_mb=rl)
    if st == 'ALL_SPLIT':
        print(f'FL({a},{b}) n={n} [{tag}]: every signotope has a split of this kind; {len(info)} partitions used; {time.time()-t0:.0f}s', flush=True)
        cl = w.cl + extra
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cert', f'{tag}_{a}_{b}_{n}.cnf')
        with open(fn, 'w') as f:
            f.write('p cnf %d %d\n' % (w.nv, len(cl)))
            for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
        json.dump({'a': a, 'b': b, 'n': n, 'partitions_S1': info}, open(fn.replace('.cnf', '_partitions.json'), 'w'))
    elif st == 'COUNTEREXAMPLE':
        print(f'FL({a},{b}) n={n} [{tag}]: COUNTEREXAMPLE (no split of this kind): sig {info}', flush=True)
        json.dump({'a': a, 'b': b, 'n': n, 'sig': info}, open(f'{tag}_counterexample_{a}_{b}_{n}.json', 'w'))
    else: print(f'FL({a},{b}) n={n} [{tag}]: stopped by a limit after {len(info)} partitions, no counterexample found, {time.time()-t0:.0f}s', flush=True)

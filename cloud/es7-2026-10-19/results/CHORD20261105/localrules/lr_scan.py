#!/usr/bin/env python3
"""Driver: for every triple orbit and both signs, enumerate phase conditions (partial sign assignments on the
non-0 layer pairs), decide feasibility numerically, extract exact certificates for the minimal feasible ones.
Output: scan JSONL (one line per orbit) with the certificates found and numeric-only (uncertified) cases."""
import os, sys, json, itertools, time
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
from fractions import Fraction as F
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lr_core as C


def consistent(cond, L):
    """cond: dict pair -> sign (+1: theta_a < theta_b).  consistent with some total order of L with 0 least?"""
    for perm in itertools.permutations(L):
        if 0 in L and perm[0] != 0:
            continue
        pos = {x: r for r, x in enumerate(perm)}
        if all((pos[a] < pos[b]) == (sg == 1) for (a, b), sg in cond.items()):
            return True
    return False


def total_orders(L):
    out = []
    for perm in itertools.permutations(L):
        if 0 in L and perm[0] != 0:
            continue
        pos = {x: r for r, x in enumerate(perm)}
        out.append({(a, b): (1 if pos[a] < pos[b] else -1) for a, b in itertools.combinations(L, 2) if a != 0})
    return out


def build(t, s, cond, nest):
    L = sorted({x // 6 for x in t}); pos = {l: r for r, l in enumerate(L)}; n = 2 * len(L)
    trip = {'kind': 'triple', 'triple': list(t), 'var': C.E.tvar[t], 'sign': s}
    recs = []
    for a, b in itertools.combinations(L, 2):
        if a == 0:
            recs.append({'kind': 'phase_sign', 'pair': [a, b], 'sign': 1})
        elif (a, b) in cond:
            recs.append({'kind': 'phase_sign', 'pair': [a, b], 'sign': cond[(a, b)]})
        recs.append({'kind': 'phase_plus', 'pair': [a, b]}); recs.append({'kind': 'phase_minus', 'pair': [a, b]})
        recs.append({'kind': 'radius', 'pair': [a, b]})
    if nest:
        recs += C.nest_recs(L, C.E.tvar[t])
    S0F = C.rec_matrix(trip, pos, n); SsF = [C.rec_matrix(r, pos, n) for r in recs]
    return trip, recs, S0F, SsF


def attempt(t, s, cond):
    """returns ('cert', cert) | ('numeric', info) | ('infeasible', None)"""
    trip, recs, S0F, SsF = build(t, s, cond, True)
    st, lam = C.solve_sdp(C.tofloat(S0F), [C.tofloat(X) for X in SsF])
    if st not in ('Solved', 'AlmostSolved'):
        return 'infeasible', st
    tried = []
    for nest in (False, True):
        if nest:
            T = (trip, recs, S0F, SsF); l2 = lam
        else:
            T = build(t, s, cond, False)
            st2, l2 = C.solve_sdp(C.tofloat(T[2]), [C.tofloat(X) for X in T[3]])
            if st2 not in ('Solved', 'AlmostSolved'):
                continue
        w = C.exact_round(T[2], T[3], l2)
        if w is None:
            tried.append(nest); continue
        used = [(r, x) for r, x in zip(T[1], w) if x > 0]
        den = 1
        for _, x in used:
            den = den * x.denominator // np.gcd(den, x.denominator)
        tw = dict(T[0]); tw['weight'] = int(den)
        out = [tw]
        for r, x in used:
            rr = dict(r); rr['weight'] = int(x * den); out.append(rr)
        g = 0
        for r in out:
            g = int(np.gcd(g, r['weight']))
        for r in out:
            r['weight'] //= g
        lits = [C.lit_of(r) for r in out]
        clause = sorted({l for l in lits if l is not None}, key=abs)
        return 'cert', {'clause': clause, 'records': out}
    return 'numeric', {'status': st, 'lam': [float(x) for x in lam]}


def classify(t):
    L = sorted({x // 6 for x in t}); var = C.E.tvar[t]
    pairs = [(a, b) for a, b in itertools.combinations(L, 2) if a != 0]
    res = {'t': list(t), 'var': var, 'layers': L, 'signs': {}}
    for s in (1, -1):
        found = []; uncert = []; infeas_full = []
        r0 = attempt(t, s, {})
        if r0[0] == 'cert':
            found.append(({}, r0[1]))
        elif r0[0] == 'numeric':
            uncert.append(({}, r0[1]))
        if r0[0] == 'infeasible' and pairs:
            TO = total_orders(L)
            feas_to = []
            to_res = {}
            for o in TO:
                r = attempt(t, s, o); to_res[tuple(sorted(o.items()))] = r
                if r[0] != 'infeasible':
                    feas_to.append(o)
            # candidate partial conditions (nonempty, proper), size ascending
            cands = []
            for k in range(1, len(pairs)):
                for P in itertools.combinations(pairs, k):
                    for sg in itertools.product((1, -1), repeat=k):
                        cnd = dict(zip(P, sg))
                        if not consistent(cnd, L):
                            continue
                        ext = [o for o in TO if all(o[p] == v for p, v in cnd.items())]
                        if all(o in feas_to for o in ext):
                            cands.append(cnd)
            feas_partial = []
            for cnd in cands:
                if any(all(cnd.get(p) == v for p, v in f.items()) for f, _ in feas_partial):
                    continue   # superset of a feasible smaller condition
                r = attempt(t, s, cnd)
                if r[0] == 'cert':
                    feas_partial.append((cnd, r[1]))
                elif r[0] == 'numeric':
                    feas_partial.append((cnd, None)); uncert.append((cnd, r[1]))
            for cnd, cert in feas_partial:
                if cert is not None:
                    found.append((cnd, cert))
            for o in feas_to:
                if any(all(o.get(p) == v for p, v in f.items()) for f, _ in feas_partial):
                    continue
                r = to_res[tuple(sorted(o.items()))]
                if r[0] == 'cert':
                    found.append((o, r[1]))
                else:
                    uncert.append((o, r[1]))
        res['signs'][s] = {'found': [({'%d,%d' % k: v for k, v in c.items()}, cert) for c, cert in found],
                           'uncertified': [({'%d,%d' % k: v for k, v in c.items()}, info) for c, info in uncert]}
    return res


def main():
    out = sys.argv[1]; lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0; hi = int(sys.argv[3]) if len(sys.argv) > 3 else None
    ts = sorted(C.E.tvar, key=lambda T: C.E.tvar[T])[lo:hi]
    t0 = time.time(); n = 0
    with Pool(4) as P, open(out, 'w') as f:
        for r in P.imap_unordered(classify, ts, chunksize=4):
            f.write(json.dumps(r) + '\n'); n += 1
            if n % 200 == 0:
                f.flush(); print(n, round(time.time() - t0, 1), flush=True)
    print('done', n, round(time.time() - t0, 1))


if __name__ == '__main__':
    main()

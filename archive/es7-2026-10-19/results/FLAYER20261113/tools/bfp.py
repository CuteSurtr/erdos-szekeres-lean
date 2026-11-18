"""Non-realizability certificates for abstract configurations (signotopes) by bi-quadratic final polynomials
(Bokowski / Richter-Gebert), with EXACT verification.

Points p_i = (1, x_i, y_i), bracket [i j k] = det(p_i, p_j, p_k); for i < j < k its sign is the signotope sign
(positive = cup triple), and it is alternating in its arguments.

Three-term Grassmann-Pluecker relation, valid for any five points a, b, c, d, e of the plane:
        [a b c][a d e] - [a b d][a c e] + [a b e][a c d] = 0.
If the signs of the brackets are those of a realizable configuration in general position, the three signed
terms T1 = [abc][ade], T2 = -[abd][ace], T3 = [abe][acd] are nonzero and sum to 0, so one of them has the
sign opposite to the other two and the largest absolute value:  |T_odd| > |T_x| and |T_odd| > |T_y|.
With L_t = log |[t]| for the unordered triples t, each such statement is a strict linear inequality
        L_p + L_q - L_r - L_s > 0        (p, q the triples of T_odd; r, s the triples of the other term).
(If all three terms had the same sign the sign vector would not even be a chirotope.)
A certificate of non-realizability is a list of such inequalities with POSITIVE INTEGER multipliers whose
weighted sum is the zero linear form: it would give 0 > 0.

find_certificate : LP (scipy/HiGHS, floating point) proposes a support; the multipliers are then recomputed
                   EXACTLY (rational nullspace of the support) -- the floating-point answer is never trusted.
verify_certificate: independent exact check of a stored certificate against the signotope.
usage: bfp.py <file.json | file.jsonl with fields n (or m), sig> [max_records]
"""
import sys, json, itertools, random
from fractions import Fraction
from math import gcd

def chi_factory(n, sig):
    T = list(itertools.combinations(range(n), 3)); sg = {t: (1 if c == '+' else -1) for t, c in zip(T, sig)}
    def chi(a, b, c):
        """sign of [a b c] for distinct a, b, c in any order"""
        x = [a, b, c]; s = 1
        # bubble sort parity
        for i in range(3):
            for j in range(2 - i):
                if x[j] > x[j + 1]: x[j], x[j + 1] = x[j + 1], x[j]; s = -s
        return s * sg[x[0], x[1], x[2]]
    return chi

def tri(a, b, c): return tuple(sorted((a, b, c)))

def inequalities(n, chi):
    """all inequalities (p, q, r, s, tag): L_p + L_q - L_r - L_s > 0 ; tag = (a, b, c, d, e, odd, other)"""
    out = []
    for a in range(n):
        rest = [x for x in range(n) if x != a]
        for b, c, d, e in itertools.combinations(rest, 4):
            terms = [((a, b, c), (a, d, e), 1), ((a, b, d), (a, c, e), -1), ((a, b, e), (a, c, d), 1)]
            sgn = [coef * chi(*t1) * chi(*t2) for t1, t2, coef in terms]
            if sgn[0] == sgn[1] == sgn[2]:
                raise ValueError('not a chirotope: Grassmann-Pluecker sign condition violated at %s' % ((a, b, c, d, e),))
            odd = [i for i in range(3) if sgn[i] != sgn[(i + 1) % 3] and sgn[i] != sgn[(i + 2) % 3]][0]
            for other in range(3):
                if other == odd: continue
                p, q = tri(*terms[odd][0]), tri(*terms[odd][1]); r, s = tri(*terms[other][0]), tri(*terms[other][1])
                out.append((p, q, r, s, (a, b, c, d, e, odd, other)))
    return out

def exact_nullvector(cols, nrows_index):
    """cols: list of sparse integer columns {row: coef}.  Returns a nonzero rational vector y with sum_j y_j col_j = 0
    (exact Gaussian elimination on the columns), or None."""
    m = len(cols)
    # row-reduce the matrix M (rows = triples, columns = inequalities) keeping track of pivots
    rows = {}
    for j, col in enumerate(cols):
        for r, v in col.items(): rows.setdefault(r, {})[j] = Fraction(v)
    pivots = {}      # column -> row dict (normalized, pivot = 1)
    for r in list(rows):
        row = rows[r]
        # eliminate existing pivots
        for pc, prow in pivots.items():
            if pc in row:
                f = row[pc]
                for k, v in prow.items():
                    nv = row.get(k, 0) - f * v
                    if nv == 0: row.pop(k, None)
                    else: row[k] = nv
        if not row: continue
        pc = min(row); f = row[pc]
        row = {k: v / f for k, v in row.items()}
        # back-substitute into previous pivot rows
        for qc, qrow in pivots.items():
            if pc in qrow:
                g = qrow[pc]
                for k, v in row.items():
                    nv = qrow.get(k, 0) - g * v
                    if nv == 0: qrow.pop(k, None)
                    else: qrow[k] = nv
        pivots[pc] = row
    free = [j for j in range(m) if j not in pivots]
    if not free: return None
    # try every free column: nullspace basis vector with that free variable = 1, the others 0
    basis = []
    for fj in free:
        y = [Fraction(0)] * m; y[fj] = Fraction(1)
        for pc, prow in pivots.items():
            if fj in prow: y[pc] = -prow[fj]
        basis.append(y)
    return basis

def find_certificate(n, sig, seed=0):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    chi = chi_factory(n, sig); ineq = inequalities(n, chi)
    T = list(itertools.combinations(range(n), 3)); idx = {t: i for i, t in enumerate(T)}
    rows = []; cols = []; vals = []
    for j, (p, q, r, s, tag) in enumerate(ineq):
        for t, v in ((p, 1), (q, 1), (r, -1), (s, -1)):
            rows.append(idx[t]); cols.append(j); vals.append(v)
    m = len(ineq)
    A = coo_matrix((vals + [1.0] * m, (rows + [len(T)] * m, cols + list(range(m)))), shape=(len(T) + 1, m)).tocsr()
    b = np.zeros(len(T) + 1); b[-1] = 1.0
    rng = np.random.default_rng(seed)
    res = linprog(c=rng.uniform(1.0, 2.0, m), A_eq=A, b_eq=b, bounds=(0, None), method='highs-ds')   # dual simplex: a vertex
    if res.status != 0: return None, 'LP: no certificate proposed (status %d)' % res.status
    supp = [j for j in range(m) if res.x[j] > 1e-9]
    colsS = []
    for j in supp:
        p, q, r, s, tag = ineq[j]; col = {}
        for t, v in ((p, 1), (q, 1), (r, -1), (s, -1)): col[idx[t]] = col.get(idx[t], 0) + v
        colsS.append(col)
    basis = exact_nullvector(colsS, len(T))
    if not basis: return None, 'exact step: support has no dependency'
    # look for a nonnegative vector: a single basis vector, or the LP combination rationalized on the basis
    cand = None
    for y in basis:
        if all(v >= 0 for v in y) and any(v > 0 for v in y): cand = y; break
        if all(v <= 0 for v in y) and any(v < 0 for v in y): cand = [-v for v in y]; break
    if cand is None: return None, 'exact step: no nonnegative dependency found on the LP support (%d inequalities)' % len(supp)
    den = 1
    for v in cand: den = den * v.denominator // gcd(den, v.denominator)
    mult = [int(v * den) for v in cand]
    g = 0
    for v in mult: g = gcd(g, v)
    cert = [{'tag': list(ineq[supp[j]][4]), 'mult': mult[j] // g} for j in range(len(supp)) if mult[j] > 0]
    return cert, 'ok'

def verify_certificate(n, sig, cert):
    """independent exact check: every inequality is re-derived from the signotope, multipliers are positive
    integers, and the weighted sum of the linear forms is identically zero."""
    chi = chi_factory(n, sig); total = {}
    if not cert: return False
    for item in cert:
        a, b, c, d, e, odd, other = item['tag']; mult = item['mult']
        if not (isinstance(mult, int) and mult > 0): return False
        if len({a, b, c, d, e}) != 5 or odd == other or odd not in (0, 1, 2) or other not in (0, 1, 2): return False
        terms = [((a, b, c), (a, d, e), 1), ((a, b, d), (a, c, e), -1), ((a, b, e), (a, c, d), 1)]
        sgn = [coef * chi(*t1) * chi(*t2) for t1, t2, coef in terms]
        if not (sgn[odd] != sgn[(odd + 1) % 3] and sgn[odd] != sgn[(odd + 2) % 3]): return False
        for t in terms[odd][:2]: total[tri(*t)] = total.get(tri(*t), 0) + mult
        for t in terms[other][:2]: total[tri(*t)] = total.get(tri(*t), 0) - mult
    return all(v == 0 for v in total.values())

def selftest(seed=1):
    """the Grassmann-Pluecker identity on random integer points (exact), and: the inequalities hold on real points"""
    rng = random.Random(seed)
    P = sorted((rng.randint(-10**4, 10**4), rng.randint(-10**4, 10**4)) for _ in range(9))
    det = lambda a, b, c: (P[b][0] - P[a][0]) * (P[c][1] - P[a][1]) - (P[b][1] - P[a][1]) * (P[c][0] - P[a][0])
    n = len(P)
    for a, b, c, d, e in itertools.permutations(range(n), 5):
        if rng.random() < 0.02:
            assert det(a, b, c) * det(a, d, e) - det(a, b, d) * det(a, c, e) + det(a, b, e) * det(a, c, d) == 0
    T = list(itertools.combinations(range(n), 3)); sig = ''.join('+' if det(*t) > 0 else '-' for t in T)
    chi = chi_factory(n, sig)
    for t in itertools.permutations(range(n), 3):
        assert chi(*t) == (1 if det(*t) > 0 else -1)
    for p, q, r, s, tag in inequalities(n, chi):
        assert abs(det(*p) * det(*q)) > abs(det(*r) * det(*s))
    return True

if __name__ == '__main__':
    assert selftest(1) and selftest(2)
    fn = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
    recs = [json.loads(l) for l in open(fn)] if fn.endswith('.jsonl') else [json.load(open(fn))]
    ok = 0; out = fn.rsplit('.', 1)[0] + '_bfp.jsonl'
    for k, d in enumerate(recs[:mx]):
        n = d.get('n') or d.get('m'); sig = d['sig']
        cert, msg = find_certificate(n, sig)
        good = bool(cert) and verify_certificate(n, sig, cert)
        ok += good
        print(f'record {k}: n={n} certificate {"VERIFIED, %d inequalities, largest multiplier %d" % (len(cert), max(c["mult"] for c in cert)) if good else "not found (" + msg + ")"}', flush=True)
        with open(out, 'a') as f: f.write(json.dumps({'record': k, 'n': n, 'sig': sig, 'nonrealizable_certificate': cert if good else None}) + '\n')
    print(f'{ok} of {min(len(recs), mx)} configurations have an exactly verified non-realizability certificate', flush=True)

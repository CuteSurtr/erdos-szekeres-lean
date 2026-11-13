#!/usr/bin/env python3
"""Local forced-sign classification for Enc(6,8,10): independent SDP + exact rounding.

For a canonical triple t (layers L, |L| <= 3) and a sign s to refute, the rows are (all as quadratic forms in the
oblique seed coordinates z_l = a_l + b_l w, w = e^{i pi/3}, exactly as clausecert_check.py builds them):
  triple record s*Q_t (weight fixed to 1 before scaling),
  phase_sign(a,b) with the sign of the condition (pairs with layer 0: always +, no literal),
  phase_plus(a,b), phase_minus(a,b), radius(a,b) for a < b in L (always valid),
  nesting records orient((i,k),(i,k+1),(j,l)) = + for i < j in L (triple records; their clause literal is
  false in every valid model because the base CNF has it as a unit, rule (B)).
Feasibility: lambda >= 0 with S0 + sum lambda_k S_k negative semidefinite (zero objective, interior point =>
approximately a relative-interior point).  Exact step: kernel identification in rational oblique coordinates,
exact affine restriction, small-denominator rounding, exact LDL test (same algorithm as the checker)."""
import importlib.util, itertools, math, json
from fractions import Fraction as F
import numpy as np
import scipy.sparse as sp
import clarabel

R = '<results-dir>'
_s = importlib.util.spec_from_file_location('g', R + '/C7UPPER/gen.py'); G = importlib.util.module_from_spec(_s)
_s.loader.exec_module(G)
E = G.Enc(6, 8, 10)
NT = E.ntriplevars


def point(x, pos):
    """oblique linear forms (a,b) of point x, with layer local coordinate offset pos[layer]"""
    i, k = divmod(x, 6); p = pos[i]
    a = {2 * p: 1}; b = {2 * p + 1: 1}
    for _ in range(k):
        a, b = {j: -c for j, c in b.items()}, {j: a.get(j, 0) + b.get(j, 0) for j in set(a) | set(b)}
    return a, b


def add(S, f, g, c):
    for i, x in f.items():
        for j, y in g.items():
            S[i][j] += F(c) * x * y / 2; S[j][i] += F(c) * x * y / 2


def zero(n):
    return [[F(0)] * n for _ in range(n)]


def rec_matrix(r, pos, n):
    S = zero(n); k = r['kind']
    if k == 'triple':
        t = r['triple']; sg = r['sign']; P = [point(x, pos) for x in t]
        for p, q in zip(P, P[1:] + P[:1]):
            add(S, p[0], q[1], sg); add(S, p[1], q[0], -sg)
    elif k == 'phase_sign':
        i, j = r['pair']; sg = r['sign']; I, J = pos[i], pos[j]
        add(S, {2 * I: 1}, {2 * J + 1: 1}, F(sg, 2)); add(S, {2 * I + 1: 1}, {2 * J: 1}, F(-sg, 2))
    elif k in ('phase_plus', 'phase_minus'):
        i, j = r['pair']; e = 1 if k == 'phase_plus' else -1; I, J = pos[i], pos[j]
        a_i, b_i, a_j, b_j = {2 * I: 1}, {2 * I + 1: 1}, {2 * J: 1}, {2 * J + 1: 1}
        add(S, a_i, a_j, 1); add(S, a_i, b_j, F(1, 2)); add(S, b_i, a_j, F(1, 2)); add(S, b_i, b_j, 1)
        add(S, a_i, b_j, F(e, 2)); add(S, b_i, a_j, F(-e, 2))
    elif k == 'radius':
        a_, b_ = r['pair']
        for l, c in ((a_, 1), (b_, -1)):
            L = pos[l]; add(S, {2 * L: 1}, {2 * L: 1}, c); add(S, {2 * L: 1}, {2 * L + 1: 1}, c)
            add(S, {2 * L + 1: 1}, {2 * L + 1: 1}, c)
    else:
        raise ValueError(k)
    return S


def canon_rec(a, b, c):
    """triple record asserting orient(a,b,c) = + : canonical triple, var, sign"""
    lit = E.o(a, b, c); v = abs(lit)
    C = next(T for T, vv in E.tvar.items() if vv == v) if False else INV[v]
    return {'kind': 'triple', 'triple': list(C), 'var': v, 'sign': 1 if lit > 0 else -1}


INV = {v: T for T, v in E.tvar.items()}


def nest_recs(L, tvar):
    out = []
    for i, j in itertools.combinations(L, 2):
        for l in range(6):
            r = canon_rec(6 * i, 6 * i + 1, 6 * j + l)
            if r['var'] != tvar:
                out.append(r)
    # dedupe (same var+sign)
    seen = set(); res = []
    for r in out:
        key = (r['var'], r['sign'])
        if key not in seen:
            seen.add(key); res.append(r)
    return res


def lit_of(r):
    """clause literal contributed by a record (None if none)"""
    if r['kind'] == 'triple':
        return -r['sign'] * r['var']
    if r['kind'] == 'phase_sign':
        i, j = r['pair']
        if i == 0:
            return None
        y = E.Y[(i, j)]
        return -y if r['sign'] == 1 else y
    return None


def svec(M):
    n = M.shape[0]; out = []
    for j in range(n):
        for i in range(j + 1):
            out.append(M[i, j] * (1.0 if i == j else math.sqrt(2)))
    return np.array(out)


def ldl_nsd(S):
    """exact: is S (list of Fraction rows) negative semidefinite? (checker algorithm)"""
    n = len(S); A = [[-x for x in row] for row in S]; idx = list(range(n))
    while idx:
        for i in idx:
            if A[i][i] < 0 or (A[i][i] == 0 and any(A[i][j] for j in idx)):
                return False
        idx = [i for i in idx if A[i][i] != 0]
        if not idx:
            break
        p = idx.pop(0)
        for i in idx:
            f = A[i][p] / A[p][p]
            if f:
                for j in idx:
                    A[i][j] -= f * A[p][j]
    return True


def solve_sdp(S0, Ss, M=100.0):
    """numeric: find lam >= 0, lam <= M, S0 + sum lam_k Sk <= 0.  returns (status, lam)"""
    n = S0.shape[0]; m = len(Ss); d = n * (n + 1) // 2
    b1 = svec(-S0); A1 = np.column_stack([svec(Sk) for Sk in Ss]) if m else np.zeros((d, 0))
    A = np.vstack([A1, -np.eye(m), np.eye(m)]); b = np.concatenate([b1, np.zeros(m), M * np.ones(m)])
    P = sp.csc_matrix((m, m)); q = np.zeros(m)
    st = clarabel.DefaultSettings(); st.verbose = False; st.max_iter = 200
    cones = [clarabel.PSDTriangleConeT(n), clarabel.NonnegativeConeT(2 * m)]
    sol = clarabel.DefaultSolver(P, q, sp.csc_matrix(A), b, cones, st).solve()
    return str(sol.status), np.array(sol.x)


def tofloat(S):
    return np.array([[float(x) for x in row] for row in S])


def rref_rational(V, maxden=60):
    """V: n x k numeric basis (columns) of a subspace; return rational basis (list of Fraction vectors) from the
    RREF of V^T, or None"""
    Mt = V.T.copy(); k, n = Mt.shape; piv = []; r = 0
    for c in range(n):
        if r >= k:
            break
        p = r + int(np.argmax(np.abs(Mt[r:, c])))
        if abs(Mt[p, c]) < 1e-6:
            continue
        Mt[[r, p]] = Mt[[p, r]]; Mt[r] /= Mt[r, c]
        for rr in range(k):
            if rr != r:
                Mt[rr] -= Mt[rr, c] * Mt[r]
        piv.append(c); r += 1
    if r < k:
        return None
    out = []
    for rr in range(k):
        vec = [F(float(x)).limit_denominator(maxden) for x in Mt[rr]]
        if max(abs(float(v) - x) for v, x in zip(vec, Mt[rr])) > 1e-5:
            return None
        out.append(vec)
    return out


def mat_add(S, T, c):
    n = len(S)
    return [[S[i][j] + c * T[i][j] for j in range(n)] for i in range(n)]


def solve_affine(Aeq, beq, m):
    """exact rational solution space of Aeq lam = beq: returns (lam_p, N) or None (inconsistent)"""
    import flint
    if not Aeq:
        return [F(0)] * m, [[F(int(i == j)) for j in range(m)] for i in range(m)]
    rows = len(Aeq)
    Mx = [list(Aeq[r]) + [beq[r]] for r in range(rows)]
    # gaussian elimination with Fractions
    piv = []; r = 0
    for c in range(m):
        p = next((rr for rr in range(r, rows) if Mx[rr][c] != 0), None)
        if p is None:
            continue
        Mx[r], Mx[p] = Mx[p], Mx[r]; f = Mx[r][c]; Mx[r] = [x / f for x in Mx[r]]
        for rr in range(rows):
            if rr != r and Mx[rr][c] != 0:
                g = Mx[rr][c]; Mx[rr] = [x - g * y for x, y in zip(Mx[rr], Mx[r])]
        piv.append(c); r += 1
        if r == rows:
            break
    for rr in range(r, rows):
        if Mx[rr][m] != 0:
            return None
    free = [c for c in range(m) if c not in piv]
    lp = [F(0)] * m
    for rr, c in enumerate(piv):
        lp[c] = Mx[rr][m]
    N = []
    for fcol in free:
        v = [F(0)] * m; v[fcol] = F(1)
        for rr, c in enumerate(piv):
            v[c] = -Mx[rr][fcol]
        N.append(v)
    return lp, N


DENS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256, 512, 1024, 4096, 16384, 65536, 10 ** 6, 10 ** 8]


def exact_round(S0F, SsF, lam, tol_support=1e-7):
    """S0F, SsF: exact matrices; lam: numeric solution.  returns exact Fraction weights list or None"""
    m = len(SsF); n = len(S0F)
    S0 = tofloat(S0F); Ss = [tofloat(X) for X in SsF]
    lam = np.clip(lam, 0, None)
    Snum = S0 + sum(l * X for l, X in zip(lam, Ss)) if m else S0
    w, V = np.linalg.eigh(Snum)
    scale = max(1.0, np.abs(w).max())
    attempts = []
    # candidate kernel dims: by gaps in eigenvalues (largest eigenvalues are ~0)
    order = np.argsort(-w)          # descending: closest to 0 first
    ws = w[order]
    kdims = [0] + [k for k in range(1, n + 1) if ws[k - 1] > -1e-4 * scale]
    for kd in sorted(set(kdims), key=lambda k: (abs(k - sum(ws > -1e-6 * scale)), k)):
        for supp_tol in (tol_support, 1e-5, 1e-4):
            supp = [k for k in range(m) if lam[k] > supp_tol * max(1.0, lam.max())]
            if kd == 0:
                basis = []
            else:
                basis = rref_rational(V[:, order[:kd]])
                if basis is None:
                    continue
            # equations (S0 + sum_supp lam_k S_k) v = 0
            Aeq = []; beq = []
            for v in basis:
                for i in range(n):
                    row = [sum(SsF[k][i][j] * v[j] for j in range(n)) for k in supp]
                    rhs = -sum(S0F[i][j] * v[j] for j in range(n))
                    if any(row) or rhs:
                        Aeq.append(row); beq.append(rhs)
            res = solve_affine(Aeq, beq, len(supp))
            if res is None:
                continue
            lp, N = res
            ls = np.array([lam[k] for k in supp])
            lpf = np.array([float(x) for x in lp])
            if N:
                Nf = np.array([[float(x) for x in v] for v in N]).T
                mu = np.linalg.lstsq(Nf, ls - lpf, rcond=None)[0]
            else:
                mu = np.zeros(0)
            for den in DENS:
                muq = [F(round(x * den), den) for x in mu]
                lq = [lp[i] + sum(muq[r] * N[r][i] for r in range(len(N))) for i in range(len(supp))]
                if any(x <= 0 for x in lq):
                    continue
                S = S0F
                for k, x in zip(supp, lq):
                    S = mat_add(S, SsF[k], x)
                if ldl_nsd(S):
                    full = [F(0)] * m
                    for k, x in zip(supp, lq):
                        full[k] = x
                    return full
    return None

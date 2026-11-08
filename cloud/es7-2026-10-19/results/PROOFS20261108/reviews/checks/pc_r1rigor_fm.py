"""Rigor checks for section pc (phase patterns), round 1.

Part 1: every algebraic / trigonometric identity used in the written proofs (sympy).
Part 2: every linear-inequality step (lemma on empty arcs, arc12, alternation, exactly-one,
        runB, gap classification, exclusivity remarks, relabelling), checked as exact LP
        infeasibility of hypotheses + negated conclusion.  All these inequalities are
        homogeneous linear in (alpha, beta, delta, pi), so pi is scaled to 1.
"""
from sympy import (symbols, sin, cos, pi, expand_trig, simplify, sqrt, acos, Abs, Rational,
                   Integer, expand, trigsimp, S)
from sympy.solvers.simplex import lpmax, InfeasibleLPError

ok_all = True


def report(name, cond):
    global ok_all
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        ok_all = False


# ---------------------------------------------------------------- Part 1: identities
c0, c1, ra, rb, rd, al, be, de, r, th, ph = symbols('c0 c1 r_a r_b r_d alpha beta delta r theta phi', real=True)
x, y = symbols('x y', real=True)


def orient(a, b, d):
    return (b[0] - a[0]) * (d[1] - a[1]) - (b[1] - a[1]) * (d[0] - a[0])


def polar(c, rr, t):
    return (c[0] + rr * cos(t), c[1] + rr * sin(t))


C = (c0, c1)
A, B, D = polar(C, ra, al), polar(C, rb, be), polar(C, rd, de)
rhs_a = ra * rb * sin(be - al) + rb * rd * sin(de - be) + rd * ra * sin(al - de)
report("(a) polar orientation formula",
       simplify(expand(expand_trig(orient(A, B, D) - rhs_a))) == 0)

# bracket expansion [v-u,w-u] = [u,v]+[v,w]+[w,u]
u0, u1, v0, v1, w0, w1 = symbols('u0 u1 v0 v1 w0 w1', real=True)
br = lambda p, q: p[0] * q[1] - p[1] * q[0]
U, V, W = (u0, u1), (v0, v1), (w0, w1)
report("(a) bracket: [v-u,w-u] = [u,v]+[v,w]+[w,u]",
       expand(br((v0 - u0, v1 - u1), (w0 - u0, w1 - u1)) - (br(U, V) + br(V, W) + br(W, U))) == 0)
report("(a) orient(u,v,w) = [v-u,w-u]", expand(orient(U, V, W) - br((v0 - u0, v1 - u1), (w0 - u0, w1 - u1))) == 0)
report("(a) translation invariance", expand(orient((u0 + c0, u1 + c1), (v0 + c0, v1 + c1), (w0 + c0, w1 + c1)) - orient(U, V, W)) == 0)
uu = (ra * cos(al), ra * sin(al)); vv = (rb * cos(be), rb * sin(be)); ww = (rd * cos(de), rd * sin(de))
report("(a) [u,v] = ra rb sin(beta-alpha)", simplify(expand_trig(br(uu, vv) - ra * rb * sin(be - al))) == 0)
report("(a) [v,w] = rb rd sin(delta-beta)", simplify(expand_trig(br(vv, ww) - rb * rd * sin(de - be))) == 0)
report("(a) [w,u] = rd ra sin(alpha-delta)", simplify(expand_trig(br(ww, uu) - rd * ra * sin(al - de))) == 0)

# (b) centre form, directly and as (a) with r_d = 0
report("(b) orient(polar a, polar b, c) = ra rb sin(beta-alpha)",
       simplify(expand_trig(orient(A, B, C) - ra * rb * sin(be - al))) == 0)
report("(b) polar(c,0,t) = c", polar(C, 0, th) == C)
report("(b) = (a) at r_d = 0", simplify(rhs_a.subs(rd, 0) - ra * rb * sin(be - al)) == 0)

# (c) sin(alpha - delta) = sin(alpha - delta + 2 pi)
report("(c) sin(alpha-delta) = sin(alpha-delta+2pi)", simplify(sin(al - de) - sin(al - de + 2 * pi)) == 0)

# (d) sin x + sin y - sin(x+y) = sin x (1-cos y) + sin y (1-cos x)
report("(d) sin x + sin y - sin(x+y) identity",
       simplify(expand_trig(sin(x) + sin(y) - sin(x + y) - (sin(x) * (1 - cos(y)) + sin(y) * (1 - cos(x))))) == 0)

# (e) decomposition
O_e = ra * rb * sin(x) + rb * rd * sin(y) - rd * ra * sin(x + y)
dec = ra * (rb - rd) * sin(x) + rd * (rb - ra) * sin(y) + ra * rd * (sin(x) + sin(y) - sin(x + y))
report("(e) decomposition of O", expand(O_e - dec) == 0)
report("(e) alpha-delta = -(x+y) with x=b-a, y=d-b", expand((al - de) + ((be - al) + (de - be))) == 0)
report("(e) rhs_a at x,y equals O_e", simplify(expand_trig(rhs_a - O_e.subs({x: be - al, y: de - be}))) == 0)

# cyclic / swap invariance (used in rule-run (D),(A) and sign (ii))
P0, P1, P2 = (u0, u1), (v0, v1), (w0, w1)
report("orient cyclic: orient(b,d,a) = orient(a,b,d)", expand(orient(P1, P2, P0) - orient(P0, P1, P2)) == 0)
report("orient cyclic: orient(d,a,b) = orient(a,b,d)", expand(orient(P2, P0, P1) - orient(P0, P1, P2)) == 0)
report("orient swap: orient(a,d,b) = -orient(a,b,d)", expand(orient(P0, P2, P1) + orient(P0, P1, P2)) == 0)

# periodicity with integer k
k = symbols('k', integer=True)
report("periodic: cos(t+2 pi k) = cos t", simplify(cos(th + 2 * pi * k) - cos(th)) == 0)
report("periodic: sin(t+2 pi k) = sin t", simplify(sin(th + 2 * pi * k) - sin(th)) == 0)

# exists_polar via arccos
U0, U1 = symbols('U0 U1', real=True)
R = sqrt(U0 ** 2 + U1 ** 2)
t = U0 / R
report("exists_polar: 1 - t^2 = u1^2/r^2", simplify(1 - t ** 2 - U1 ** 2 / R ** 2) == 0)
report("exists_polar: cos(acos t) = t", simplify(cos(acos(t)) - t) == 0)
report("exists_polar: sin(acos t) = sqrt(1 - t^2)", simplify(sin(acos(t)) - sqrt(1 - t ** 2)) == 0)
# sign cases numerically at exact rationals
import random
random.seed(1)
ok_ep = True
for _ in range(300):
    a0 = Rational(random.randint(-50, 50), random.randint(1, 9))
    a1 = Rational(random.randint(-50, 50), random.randint(1, 9))
    if a0 == 0 and a1 == 0:
        continue
    RR = sqrt(a0 ** 2 + a1 ** 2)
    TT = acos(a0 / RR) if a1 >= 0 else -acos(a0 / RR)
    e0 = (RR * cos(TT) - a0).evalf(30)
    e1 = (RR * sin(TT) - a1).evalf(30)
    if abs(e0) > 1e-20 or abs(e1) > 1e-20:
        ok_ep = False
report("exists_polar: r cos(theta) = u0, r sin(theta) = u1 for both sign cases (300 exact-rational samples)", ok_ep)

# dist2_polar
report("dist2(c, polar(c,r,t)) = r^2",
       simplify((polar(C, r, th)[0] - c0) ** 2 + (polar(C, r, th)[1] - c1) ** 2 - r ** 2) == 0)

# halfplane identity
report("halfplane: r cos t cos phi + r sin t sin phi = r cos(t-phi)",
       simplify(expand_trig((polar(C, r, th)[0] - c0) * cos(ph) + (polar(C, r, th)[1] - c1) * sin(ph) - r * cos(th - ph))) == 0)

# elementary fact for radii
r1, r2 = symbols('r1 r2', real=True)
report("r^2 - r'^2 = (r - r')(r + r')", expand(r1 ** 2 - r2 ** 2 - (r1 - r2) * (r1 + r2)) == 0)

# ---------------------------------------------------------------- Part 2: linear implications
a, b, d = symbols('a b d', real=True)   # alpha, beta, delta in units of pi (pi := 1)
tt = symbols('tt', real=True)
tv = symbols('tv', real=True)
P = Integer(1)


def _lin(e):
    """sympy linear expression -> (dict var->Fraction, const Fraction)"""
    from fractions import Fraction
    e = expand(e)
    coeffs = {}
    for v_ in (a, b, d, tt, tv):
        cf = e.coeff(v_)
        if cf != 0:
            coeffs[v_] = Fraction(int(cf.p), int(cf.q))
    rest = expand(e - sum(cf_ * v_ for v_, cf_ in ((v_, e.coeff(v_)) for v_ in (a, b, d, tt, tv))))
    assert rest.free_symbols == set(), rest
    rest = S(rest)
    return coeffs, Fraction(int(rest.p), int(rest.q))


def feasible(cons):
    """Exact Fourier-Motzkin: cons list of (expr, rel), meaning expr rel 0, rel in '<','<=','=='."""
    from fractions import Fraction
    sys_ = []
    for e, rel in cons:
        cf, c_ = _lin(e)
        if rel == '<':
            sys_.append((cf, c_, True))
        elif rel == '<=':
            sys_.append((cf, c_, False))
        elif rel == '==':
            sys_.append((cf, c_, False))
            sys_.append(({k_: -v_ for k_, v_ in cf.items()}, -c_, False))
        else:
            raise ValueError(rel)
    for x_ in (a, b, d, tt, tv):
        pos = [s_ for s_ in sys_ if s_[0].get(x_, 0) > 0]
        negs = [s_ for s_ in sys_ if s_[0].get(x_, 0) < 0]
        zero = [s_ for s_ in sys_ if s_[0].get(x_, 0) == 0]
        new = list(zero)
        for p_ in pos:
            for n_ in negs:
                cp, cn = p_[0][x_], -n_[0][x_]
                cf = {}
                for k_ in set(p_[0]) | set(n_[0]):
                    val = p_[0].get(k_, 0) / cp + n_[0].get(k_, 0) / cn
                    if val != 0 and k_ != x_:
                        cf[k_] = val
                new.append((cf, p_[1] / cp + n_[1] / cn, p_[2] or n_[2]))
        sys_ = new
    for cf, c_, strict in sys_:
        assert not cf
        if strict and not (c_ < 0):
            return False
        if (not strict) and not (c_ <= 0):
            return False
    return True


def neg(c):
    e, rel = c
    if rel == '<':
        return [(-e, '<=')]
    if rel == '<=':
        return [(-e, '<')]
    raise ValueError


def implies(hyps, concl):
    return not feasible(hyps + neg(concl))


def lt(l, rr):
    return (l - rr, '<')


def le(l, rr):
    return (l - rr, '<=')


def eq(l, rr):
    return (l - rr, '==')


order = [lt(a, b), lt(b, d), lt(d, a + 2 * P)]


def not_in_arc_ok(hyps, s, g, theta, m):
    return implies(hyps, le(s + g, theta + 2 * P * m)) and implies(hyps, le(theta + 2 * P * m, s + 2 * P))


def in_arc_ok(hyps, s, g, theta, kk):
    return implies(hyps, lt(s, theta + 2 * P * kk)) and implies(hyps, lt(theta + 2 * P * kk, s + g))


A_, B_, D_ = a + P, b + P, d + P
arc1 = (a, b - a)
arc2 = (b, d - b)
arc3 = (d, a + 2 * P - d)
# Lemma pc:lem:empty, each part with the integers m as written
parts = {
    '(a) arc1_empty': ([lt(a, b), lt(b, d), le(d - a, P)], arc1, [0, 0, 0]),
    '(b) arc2_empty': ([lt(a, b), lt(b, d), le(d - a, P)], arc2, [0, 0, 0]),
    "(c) arc2_empty'": ([lt(b, d), lt(d, a + 2 * P), le(a + 2 * P - b, P)], arc2, [1, 0, 0]),
    '(d) arc3_empty': ([lt(b, d), lt(d, a + 2 * P), le(a + 2 * P - b, P)], arc3, [1, 0, 0]),
    "(e) arc3_empty'": ([lt(a, b), lt(d, a + 2 * P), le(b + 2 * P - d, P)], arc3, [1, 1, 0]),
    "(f) arc1_empty'": ([lt(a, b), lt(d, a + 2 * P), le(b + 2 * P - d, P)], arc1, [0, 0, -1]),
}
for nm, (hyps, (s, g), ms) in parts.items():
    res = all(not_in_arc_ok(hyps, s, g, th_, m_) for th_, m_ in zip([A_, B_, D_], ms))
    report("Lemma empty " + nm + " with m = " + str(ms), res)
# intermediate claims in Lemma empty proofs
report("empty (a): beta < alpha+pi and beta-alpha < pi", implies([lt(a, b), lt(b, d), le(d - a, P)], lt(b, a + P)) and implies([lt(a, b), lt(b, d), le(d - a, P)], lt(b - a, P)))
report("empty (b): delta-beta < pi", implies([lt(a, b), lt(b, d), le(d - a, P)], lt(d - b, P)))
report("empty (c): delta < beta+pi", implies([lt(b, d), lt(d, a + 2 * P), le(a + 2 * P - b, P)], lt(d, b + P)))
report("empty (d): alpha+pi < delta", implies([lt(b, d), lt(d, a + 2 * P), le(a + 2 * P - b, P)], lt(a + P, d)))
report("empty (e): alpha+pi < delta", implies([lt(a, b), lt(d, a + 2 * P), le(b + 2 * P - d, P)], lt(a + P, d)))
report("empty (f): beta < alpha+pi, beta+pi < alpha+2pi", implies([lt(a, b), lt(d, a + 2 * P), le(b + 2 * P - d, P)], lt(b, a + P)) and implies([lt(a, b), lt(d, a + 2 * P), le(b + 2 * P - d, P)], lt(b + P, a + 2 * P)))

# Lemma arc12, three cases
h12 = order + [lt(P, d - a)]
report("arc12 case b-a<pi: alpha+pi in arc2, k=0", in_arc_ok(h12 + [lt(b - a, P)], b, d - b, A_, 0))
report("arc12 case b-a>pi: alpha+pi in arc1, k=0", in_arc_ok(h12 + [lt(P, b - a)], a, b - a, A_, 0))
report("arc12 case b-a=pi: delta+pi in arc1, k=-1", in_arc_ok(h12 + [eq(b - a, P)], a, b - a, D_, -1))

# Theorem alternating
report("alt => : b-a>=pi gives a+2pi-b<=pi", implies(order + [le(P, b - a)], le(a + 2 * P - b, P)))
report("alt => : d-b>=pi gives b+2pi-d<=pi", implies(order + [le(P, d - b)], le(b + 2 * P - d, P)))
report("alt => : a+2pi-d>=pi gives d-a<=pi", implies(order + [le(P, a + 2 * P - d)], le(d - a, P)))
hg = order + [lt(b - a, P), lt(d - b, P), lt(a + 2 * P - d, P)]
report("alt <= : H1 via delta+pi k=-1", in_arc_ok(hg, a, b - a, D_, -1))
report("alt <= : H2 via alpha+pi k=0", in_arc_ok(hg, b, d - b, A_, 0))
report("alt <= : H3 via beta+pi k=0", in_arc_ok(hg, d, a + 2 * P - d, B_, 0))
# Proposition exactly-one, non-memberships
report("exactly-one arc1: alpha+pi m=0, beta+pi m=0", not_in_arc_ok(hg, a, b - a, A_, 0) and not_in_arc_ok(hg, a, b - a, B_, 0))
report("exactly-one arc2: beta+pi m=0, delta+pi m=0", not_in_arc_ok(hg, b, d - b, B_, 0) and not_in_arc_ok(hg, b, d - b, D_, 0))
report("exactly-one arc3: alpha+pi m=1, delta+pi m=0", not_in_arc_ok(hg, d, a + 2 * P - d, A_, 1) and not_in_arc_ok(hg, d, a + 2 * P - d, D_, 0))

# Theorem runB (=>): delta-alpha>=pi and a+2pi-d != pi gives pi<delta-alpha
report("runB =>: case a+2pi-d<pi", implies(order + [le(P, d - a), lt(a + 2 * P - d, P)], lt(P, d - a)))
report("runB =>: case a+2pi-d>pi infeasible with d-a>=pi", not feasible(order + [le(P, d - a), lt(P, a + 2 * P - d)]))

# Proposition gaps: 8 sign patterns, negated disjunction infeasible
g1, g2, g3 = b - a, d - b, a + 2 * P - d
negdisj_tail = [le(P, d - a), le(P, a + 2 * P - b), le(P, b + 2 * P - d)]
okg = True
import itertools
for pat in itertools.product(['<', '>'], repeat=3):
    cons = list(order)
    for gi, sgn in zip([g1, g2, g3], pat):
        cons.append(lt(gi, P) if sgn == '<' else lt(P, gi))
    if pat == ('<', '<', '<'):
        continue  # first disjunct holds
    if feasible(cons + negdisj_tail):
        okg = False
        print('   counterexample pattern', pat)
report("gap_classification: every sign pattern gives a disjunct", okg)
report("gaps: g3>pi gives d-a<pi", implies(order + [lt(P, g3)], lt(d - a, P)))
report("gaps: g1>pi gives a+2pi-b<pi", implies(order + [lt(P, g1)], lt(a + 2 * P - b, P)))
report("gaps: g2>pi gives b+2pi-d<pi", implies(order + [lt(P, g2)], lt(b + 2 * P - d, P)))
report("gaps: two gaps > pi impossible", all(not feasible(order + [lt(P, p_), lt(P, q_)]) for p_, q_ in [(g1, g2), (g1, g3), (g2, g3)]))
# Remark gaps (2): disjuncts pairwise exclusive
Dj = {'D1': [lt(g1, P), lt(g2, P), lt(g3, P)], 'D2': [lt(d - a, P)], 'D3': [lt(a + 2 * P - b, P)], 'D4': [lt(b + 2 * P - d, P)]}
report("remark gaps (2): disjuncts pairwise exclusive",
       all(not feasible(order + Dj[p_] + Dj[q_]) for p_, q_ in itertools.combinations(Dj, 2)))

# Remark runs: H1 or H2 or H3 under order, five cases
report("runs: a+pi<b gives H1 (alpha+pi, k=0)", in_arc_ok(order + [lt(a + P, b)], a, b - a, A_, 0))
report("runs: b<a+pi<d gives H2 (alpha+pi, k=0)", in_arc_ok(order + [lt(b, a + P), lt(a + P, d)], b, d - b, A_, 0))
report("runs: d<a+pi gives H3 (alpha+pi, k=0)", in_arc_ok(order + [lt(d, a + P)], d, a + 2 * P - d, A_, 0))
report("runs: a+pi=b gives H1 (delta+pi, k=-1)", in_arc_ok(order + [eq(a + P, b)], a, b - a, D_, -1))
report("runs: a+pi=d gives H3 (beta+pi, k=0)", in_arc_ok(order + [eq(a + P, d)], d, a + 2 * P - d, B_, 0))

# rule-run relabelling
ap, bp, dp = b, d, a + 2 * P
report("(D) relabel order", all(implies(order, c_) for c_ in [lt(ap, bp), lt(bp, dp), lt(dp, ap + 2 * P)]))
report("(D) alpha'+2pi-delta' = beta-alpha", expand(ap + 2 * P - dp - (b - a)) == 0)
ap, bp, dp = d, a + 2 * P, b + 2 * P
report("(A) relabel order", all(implies(order, c_) for c_ in [lt(ap, bp), lt(bp, dp), lt(dp, ap + 2 * P)]))
report("(A) alpha'+2pi-delta' = delta-beta", expand(ap + 2 * P - dp - (d - b)) == 0)

# halfplane: theta in [alpha, delta], phi=(alpha+delta)/2, delta-alpha<pi => |theta-phi|<pi/2
hh = [le(a, tv), le(tv, d), lt(d - a, P)]
phi_ = (a + d) / 2
report("halfplane |theta-phi| < pi/2", implies(hh, lt(tv - phi_, P / 2)) and implies(hh, lt(-P / 2, tv - phi_)))

print("\nALL OK" if ok_all else "\nSOME CHECK FAILED")

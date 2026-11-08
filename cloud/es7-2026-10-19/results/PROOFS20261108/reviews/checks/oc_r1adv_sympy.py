"""Adversarial checks for section oc (round 1). Symbolic identities (sympy) and exact-arithmetic attacks."""
import itertools, random
from fractions import Fraction as F
import sympy as sp

ok = 0; bad = []
def check(name, cond):
    global ok
    if cond: ok += 1
    else: bad.append(name)

def orient(a, b, d):
    return (b[0]-a[0])*(d[1]-a[1]) - (b[1]-a[1])*(d[0]-a[0])

# ---------- symbolic: rotations ----------
c0, c1, p0, p1, al, be, th, ph, r, rp, l = sp.symbols('c0 c1 p0 p1 alpha beta theta phi r rp l', real=True)
def R(c, t, p):
    return (c[0] + sp.cos(t)*(p[0]-c[0]) - sp.sin(t)*(p[1]-c[1]),
            c[1] + sp.sin(t)*(p[0]-c[0]) + sp.cos(t)*(p[1]-c[1]))
def polar(c, rr, t):
    return (c[0] + rr*sp.cos(t), c[1] + rr*sp.sin(t))
c = (c0, c1); p = (p0, p1)
lhs = R(c, al, R(c, be, p)); rhs = R(c, al+be, p)
check('rot-add(a)', all(sp.simplify(sp.expand_trig(lhs[i]-rhs[i])) == 0 for i in range(2)))
check('rot-add(b) R_pi', all(sp.simplify(R(c, sp.pi, p)[i] - (2*c[i]-p[i])) == 0 for i in range(2)))
check('rot-add(b) R_2pi', all(sp.simplify(R(c, 2*sp.pi, p)[i] - p[i]) == 0 for i in range(2)))
# rot-inv as polynomial identity in independent symbols C,S
C, S = sp.symbols('C S', real=True)
a = sp.symbols('a0 a1', real=True); b = sp.symbols('b0 b1', real=True); d = sp.symbols('d0 d1', real=True)
def Rpoly(p):
    return (c0 + C*(p[0]-c0) - S*(p[1]-c1), c1 + S*(p[0]-c0) + C*(p[1]-c1))
e = sp.expand(orient(Rpoly(a), Rpoly(b), Rpoly(d)) - orient(a, b, d) - orient(a, b, d)*(S**2 + C**2 - 1))
check('rot-inv linear_combination', e == 0)
# polar-rot (a)
lhs = R(c, ph, polar(c, r, th)); rhs = polar(c, r, th+ph)
check('rotAbout_polar', all(sp.simplify(sp.expand_trig(lhs[i]-rhs[i])) == 0 for i in range(2)))
# polar_add_int (b): n symbolic integer
n = sp.symbols('n', integer=True)
check('polar_add_int', all(sp.simplify(polar(c, r, th + n*2*sp.pi)[i] - polar(c, r, th)[i]) == 0 for i in range(2)))
# period: k*(2pi/(2k)) = pi ; m*(2pi/m) = 2pi
k, m = sp.symbols('k m', positive=True)
check('half-turn angle', sp.simplify(k*(2*sp.pi/(2*k)) - sp.pi) == 0)
check('full-turn angle', sp.simplify(m*(2*sp.pi/m) - 2*sp.pi) == 0)
# same-ray (iv): orient(x, c + l(x-c), 2c - x) = 0 ; (iii) y=q <=> (l+1)(x-c)=0
x = (p0, p1); y = (c0 + l*(p0-c0), c1 + l*(p1-c1)); q = (2*c0-p0, 2*c1-p1)
check('same-ray collinear', sp.expand(orient(x, y, q)) == 0)
check('same-ray y-x', all(sp.expand((y[i]-x[i]) - (l-1)*(x[i]-c[i])) == 0 for i in range(2)))
check('same-ray y=q', all(sp.expand((y[i]-q[i]) - (l+1)*(x[i]-c[i])) == 0 for i in range(2)))
# phase-nat: y-c = (r'/r)(z-c) with z = polar(c,r,beta), y = polar(c,r',beta)
z = polar(c, r, be); yy = polar(c, rp, be)
check('phase-nat ratio', all(sp.simplify((yy[i]-c[i]) - rp/r*(z[i]-c[i])) == 0 for i in range(2)))
# phase-int: k*(2pi/m) = j*(2pi/m) + q*2pi when k = j + m q
j_, q_, M = sp.symbols('j q M', positive=True)
check('phase-int split', sp.simplify((j_ + M*q_)*(2*sp.pi/M) - (j_*(2*sp.pi/M) + q_*2*sp.pi)) == 0)

# ---------- orient3 permutations, swaps, sign table ----------
T = [sp.symbols('t%d_0 t%d_1' % (i, i), real=True) for i in range(3)]
def o3(t): return sp.expand(orient(t[0], t[1], t[2]))
def swap(x_, y_):
    return tuple(y_ if i == x_ else x_ if i == y_ else i for i in range(3))
def mul(s, t):  # (s t)(i) = s(t(i))
    return tuple(s[t[i]] for i in range(3))
def inv(tau):
    return sum(1 for i in range(3) for j in range(i+1, 3) if tau[i] > tau[j])
def sgn_cycles(tau):  # independent of inversions: (-1)^(n - #cycles)
    seen = set(); cyc = 0
    for i in range(3):
        if i not in seen:
            cyc += 1; j = i
            while j not in seen:
                seen.add(j); j = tau[j]
    return (-1)**(3 - cyc)
for x_ in range(3):
    for y_ in range(3):
        if x_ != y_:
            s = swap(x_, y_)
            check('swap %d%d' % (x_, y_), sp.expand(o3([T[s[i]] for i in range(3)]) + o3(T)) == 0)
for tau in itertools.permutations(range(3)):
    check('perm %s' % (tau,), sp.expand(o3([T[tau[i]] for i in range(3)]) - sgn_cycles(tau)*o3(T)) == 0)
    check('inv=sgn %s' % (tau,), (-1)**inv(tau) == sgn_cycles(tau))
table = {(0,1,2): [], (1,0,2): [(0,1)], (0,2,1): [(1,2)], (2,1,0): [(0,2)], (1,2,0): [(0,1),(1,2)], (2,0,1): [(1,2),(0,1)]}
invs = {(0,1,2): 0, (1,0,2): 1, (0,2,1): 1, (2,1,0): 3, (1,2,0): 2, (2,0,1): 2}
for tau, sw in table.items():
    prod = (0, 1, 2)
    for (u_, v_) in sw:
        prod = mul(prod, swap(u_, v_))
    check('table product %s' % (tau,), prod == tau)
    check('table inv %s' % (tau,), inv(tau) == invs[tau])
    check('table sgn %s' % (tau,), (-1)**len(sw) == sgn_cycles(tau))

# ---------- encoder parity code vs sign of sorting permutation ----------
def sortpar(lst):  # verbatim logic of C7UPPER/gen.py:108
    a_ = list(lst); par = 1
    for i in range(len(a_)):
        for j in range(len(a_) - 1 - i):
            if a_[j] > a_[j + 1]:
                a_[j], a_[j + 1] = a_[j + 1], a_[j]; par = -par
    return tuple(a_), par
def perm_sign(seq):  # verbatim logic of C6UPPER/encb/gen_b2.py:56
    s = 1; a_ = list(seq)
    for x__ in range(len(a_)):
        for y__ in range(x__ + 1, len(a_)):
            if a_[x__] > a_[y__]: s = -s
    return s
for lst in itertools.permutations([(0, 5), (1, 2), (3, 0)]):
    sigma = tuple(sorted(range(3), key=lambda i: lst[i]))  # lst o sigma increasing
    check('sortpar=sgn(sigma) %s' % (lst,), sortpar(lst)[1] == sgn_cycles(sigma))
    check('perm_sign(order)=sgn(order) %s' % (lst,), perm_sign(list(sigma)) == sgn_cycles(sigma))

# ---------- Remark layers (3): exact counterexample ----------
h = F(1, 2)
outer = [(F(2), F(0)), (F(0), F(2)), (F(-2), F(0)), (F(0), F(-2))]
inner = [(h, h), (-h, h), (-h, -h), (h, -h)]
Sset = outer + inner
rot90 = lambda pt: (-pt[1], pt[0])
check('invariant', all(rot90(pt) in Sset for pt in Sset))
check('c not in S', (F(0), F(0)) not in Sset)
check('GP', all(orient(a_, b_, d_) != 0 for a_, b_, d_ in itertools.combinations(Sset, 3)))
def in_hull_of(pt, pts):  # exact: pt in conv(pts) for a convex polygon given ccw (here: test via triangles)
    for a_, b_, d_ in itertools.combinations(pts, 3):
        o = orient(a_, b_, d_)
        if o == 0: continue
        s1, s2, s3 = orient(a_, b_, pt), orient(b_, d_, pt), orient(d_, a_, pt)
        if (o > 0 and s1 >= 0 and s2 >= 0 and s3 >= 0) or (o < 0 and s1 <= 0 and s2 <= 0 and s3 <= 0):
            return True
    return False
def hull_verts(X):
    return [pt for pt in X if not in_hull_of(pt, [y_ for y_ in X if y_ != pt])]
check('hv(S)=outer', sorted(hull_verts(Sset)) == sorted(outer))
peel1 = [pt for pt in Sset if pt not in hull_verts(Sset)]
check('peel1=inner', sorted(peel1) == sorted(inner))
check('hv(peel1)=inner', sorted(hull_verts(peel1)) == sorted(inner))
check('S not convex position', len(hull_verts(Sset)) < len(Sset))
pp = polar((0, 0), sp.sqrt(2)/2, sp.pi/4)
check('polar(c,sqrt2/2,pi/4)=(1/2,1/2)', sp.simplify(pp[0] - sp.Rational(1, 2)) == 0 and sp.simplify(pp[1] - sp.Rational(1, 2)) == 0)

# ---------- key order: exact arithmetic in units where 2pi = N*u ----------
def toIcoMod(p_, a_, b_):  # Mathlib: b - n p with b - n p in [a, a+p)
    nn = (b_ - a_) // p_          # floor for Fractions
    v = b_ - nn * p_
    assert a_ <= v < a_ + p_
    return v
rnd = random.Random(7)
for _ in range(4000):
    N = rnd.randint(1, 9); u = F(rnd.randint(1, 7), rnd.randint(1, 5)); P2 = N * u  # plays 2pi
    J1, J2 = rnd.randint(-30, 30), rnd.randint(-30, 30)
    ps1 = u * F(rnd.randint(0, 9), 10) if rnd.random() < .7 else F(0)
    ps2 = u * F(rnd.randint(0, 9), 10) if rnd.random() < .7 else ps1
    # cell_lt_iff, cell_eq_iff
    check('cell_lt', (J1*u + ps1 < J2*u + ps2) == (J1 < J2 or (J1 == J2 and ps1 < ps2)))
    check('cell_eq', (J1*u + ps1 == J2*u + ps2) == (J1 == J2 and ps1 == ps2))
    # reduce_mod_two_pi (Python % is the Euclidean remainder for N > 0)
    check('reduce', toIcoMod(P2, F(0), J1*u + ps1) == (J1 % N)*u + ps1)
    # reduced_lt_iff_key with rank = strictly increasing map on phases
    rank = lambda v: int(v * 1000)
    lhs_ = toIcoMod(P2, F(0), J1*u + ps1) < toIcoMod(P2, F(0), J2*u + ps2)
    rhs_ = (J1 % N, rank(ps1)) < (J2 % N, rank(ps2))
    check('key', lhs_ == rhs_)
# boundary: psi = u breaks cell_lt_iff (Remark halfopen (1))
u = F(1)
check('halfopen(1) counterexample', not (0*u + u < 1*u + 0) and (0 < 1))
check('halfopen(2)', toIcoMod(5*u, F(0), 5*u) == 0)
# antipodes in exact units of pi: angle = q*pi, q rational; toIcoMod_{2pi}(0,.) in units of pi has period 2
for mm in range(1, 9):
    for J in range(-20, 21):
        for sfrac in [F(0), F(1, 3), F(9, 10)]:
            psi = sfrac / mm                      # psi in [0, pi/m), in units of pi
            lhs_ = toIcoMod(F(2), F(0), F(J, mm) + psi + 1)
            rhs_ = F((J + mm) % (2*mm), mm) + psi
            check('antipode_odd m=%d' % mm, lhs_ == rhs_)
            if mm % 2 == 0:
                psi2 = 2*sfrac / mm               # psi in [0, 2pi/m)
                lhs2 = toIcoMod(F(2), F(0), J*F(2, mm) + psi2 + 1)
                rhs2 = ((J + mm//2) % mm) * F(2, mm) + psi2
                check('antipode_even m=%d' % mm, lhs2 == rhs2)

# ---------- encoder_literal_sound, exact for m = 4 (and m = 2), non-injective P allowed ----------
def litVal(eps, Cpts):
    v = orient(*Cpts)
    return (0 < v) if eps == 1 else not (0 < v)
for trial in range(300):
    mm = rnd.choice([2, 4]); cc = (F(rnd.randint(-3, 3)), F(rnd.randint(-3, 3)))
    rho = (lambda pt: (cc[0] - (pt[1]-cc[1]), cc[1] + (pt[0]-cc[0]))) if mm == 4 else (lambda pt: (2*cc[0]-pt[0], 2*cc[1]-pt[1]))
    nl = rnd.randint(1, 3)  # layers; labels (i,k)
    base = [(F(rnd.randint(-9, 9), 2), F(rnd.randint(-9, 9), 2)) for _ in range(nl)]
    def Pl(lab):
        pt = base[lab[0]]
        for _ in range(lab[1] % mm): pt = rho(pt)
        return pt
    rl = lambda lab: (lab[0], (lab[1] + 1) % mm)
    labels = [(i, kk) for i in range(nl) for kk in range(mm)]
    Tt = tuple(rnd.choice(labels) for _ in range(3))
    s1 = rnd.choice(list(itertools.permutations(range(3)))); s2 = rnd.choice(list(itertools.permutations(range(3))))
    ss = rnd.randint(0, 9)
    T0 = tuple(Tt[s1[i]] for i in range(3))
    def rit(lab, t_):
        for _ in range(t_): lab = rl(lab)
        return lab
    Cl = tuple(rit(T0[s2[i]], ss) for i in range(3))
    PT = [Pl(lb) for lb in Tt]
    if orient(*PT) == 0: continue
    check('encoder_literal_sound', (0 < orient(*PT)) == litVal(sgn_cycles(s1)*sgn_cycles(s2), [Pl(lb) for lb in Cl]))

print('passed', ok, 'failed', len(bad))
for b_ in bad[:20]: print('FAIL', b_)

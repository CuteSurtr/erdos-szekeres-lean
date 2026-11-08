"""Rigor check (oc, round 1): verify every identity used in sections/oc.tex with sympy."""
import itertools
from sympy import (symbols, cos, sin, pi, simplify, expand, Matrix, Rational, sqrt,
                   trigsimp, expand_trig, Integer, floor, nsimplify)

ok = True
def check(name, expr):
    global ok
    e = simplify(expand_trig(expand(expr)))
    if e != 0:
        e = simplify(trigsimp(e))
    res = (e == 0)
    ok = ok and res
    print(("OK  " if res else "FAIL"), name, "" if res else e)

a0, a1, b0, b1, d0, d1, c0, c1, p0, p1 = symbols('a0 a1 b0 b1 d0 d1 c0 c1 p0 p1', real=True)
al, be, th, ph, r, rp, l = symbols('alpha beta theta phi r rp l', real=True)

def orient(a, b, d):
    return (b[0]-a[0])*(d[1]-a[1]) - (b[1]-a[1])*(d[0]-a[0])

def R(c, t, p):
    return (c[0] + cos(t)*(p[0]-c[0]) - sin(t)*(p[1]-c[1]),
            c[1] + sin(t)*(p[0]-c[0]) + cos(t)*(p[1]-c[1]))

def polar(c, rr, t):
    return (c[0] + rr*cos(t), c[1] + rr*sin(t))

c = (c0, c1); p = (p0, p1); A = (a0, a1); B = (b0, b1); D = (d0, d1)

# oc:lem:rot-add (a): R_alpha(R_beta p) = R_{alpha+beta} p
lhs = R(c, al, R(c, be, p)); rhs = R(c, al+be, p)
check("rot-add(a) x", lhs[0]-rhs[0]); check("rot-add(a) y", lhs[1]-rhs[1])
# the displayed coordinate formulas in the proof
v0, v1 = p0-c0, p1-c1
check("rot-add(a) display x", cos(al)*(cos(be)*v0 - sin(be)*v1) - sin(al)*(sin(be)*v0 + cos(be)*v1)
      - (cos(al+be)*v0 - sin(al+be)*v1))
check("rot-add(a) display y", sin(al)*(cos(be)*v0 - sin(be)*v1) + cos(al)*(sin(be)*v0 + cos(be)*v1)
      - (sin(al+be)*v0 + cos(al+be)*v1))
# (b)
for t, nm in [(0, "R_0"), (2*pi, "R_2pi")]:
    q = R(c, t, p); check(nm+" x", q[0]-p0); check(nm+" y", q[1]-p1)
q = R(c, pi, p); check("R_pi x", q[0]-(2*c0-p0)); check("R_pi y", q[1]-(2*c1-p1))

# oc:cor:period: m*(2pi/m) = 2pi, k*(2pi/(2k)) = pi
m, k = symbols('m k', positive=True, integer=True)
check("period m*(2pi/m)=2pi", m*(2*pi/m) - 2*pi)
check("half k*2pi/(2k)=pi", k*(2*pi/(k+k)) - pi)

# oc:lem:rot-inv: difference equals orient*(sin^2+cos^2-1) as a polynomial identity (no trig simplification)
s, co = symbols('s co', real=True)
def Rpoly(cc, pp):
    return (cc[0] + co*(pp[0]-cc[0]) - s*(pp[1]-cc[1]), cc[1] + s*(pp[0]-cc[0]) + co*(pp[1]-cc[1]))
diff = orient(Rpoly(c, A), Rpoly(c, B), Rpoly(c, D)) - orient(A, B, D)
res = expand(diff - orient(A, B, D)*(s**2 + co**2 - 1))
print(("OK  " if res == 0 else "FAIL"), "rot-inv polynomial identity", res if res != 0 else "")
ok = ok and res == 0
# det(M) = cos^2 + sin^2
M = Matrix([[cos(th), -sin(th)], [sin(th), cos(th)]])
check("det M = 1", M.det() - 1)
# orient(a,b,d) = det(b-a | d-a)
check("orient = det(b-a|d-a)", Matrix([[b0-a0, d0-a0], [b1-a1, d1-a1]]).det() - orient(A, B, D))

# oc:lem:swap: the three swaps
t0, t1, t2 = (symbols('x0 y0', real=True), symbols('x1 y1', real=True), symbols('x2 y2', real=True))
o = orient(t0, t1, t2)
check("swap(1,2)", orient(t0, t2, t1) + o)
check("swap(0,1)", orient(t1, t0, t2) + o)
check("swap(0,2)", orient(t2, t1, t0) + o)
check("cyclic rule used: orient(t1,t0,t2)=orient(t0,t2,t1)", orient(t1, t0, t2) - orient(t0, t2, t1))
check("cyclic rule used: orient(t2,t1,t0)=orient(t1,t0,t2)", orient(t2, t1, t0) - orient(t1, t0, t2))

# oc:lem:same-ray
x = (symbols('X0', real=True), symbols('X1', real=True))
y = (c0 + l*(x[0]-c0), c1 + l*(x[1]-c1))
q = (2*c0 - x[0], 2*c1 - x[1])
check("same-ray (iv) orient(x,y,q)=0", orient(x, y, q))
check("same-ray y-x=(l-1)(x-c) x", (y[0]-x[0]) - (l-1)*(x[0]-c0))
check("same-ray q-x=-2(x-c) x", (q[0]-x[0]) + 2*(x[0]-c0))
check("same-ray (iii) y-q = (l+1)(x-c) x", (y[0]-q[0]) - (l+1)*(x[0]-c0))
check("same-ray (iii) y-q = (l+1)(x-c) y", (y[1]-q[1]) - (l+1)*(x[1]-c1))
check("same-ray (ii) x-q = 2(x-c)", (x[0]-q[0]) - 2*(x[0]-c0))
# remark oc:rem:ray: y = 2c - x gives y - c = -(x - c)
check("rem ray antipode", (2*c0 - x[0] - c0) + (x[0]-c0))

# oc:lem:polar-rot (a), (b)
P = polar(c, r, th); RP = R(c, ph, P); Q = polar(c, r, th+ph)
check("rotAbout_polar x", RP[0]-Q[0]); check("rotAbout_polar y", RP[1]-Q[1])
n = symbols('n', integer=True)
check("polar_add_int x", polar(c, r, th + n*2*pi)[0] - P[0])
check("polar_add_int y", polar(c, r, th + n*2*pi)[1] - P[1])

# oc:lem:phase-nat: y - c = (r'/r)(z - c) with z = polar(c,r,beta), y = polar(c,r',beta)
z = polar(c, r, be); yy = polar(c, rp, be)
check("phase-nat x", (yy[0]-c0) - (rp/r)*(z[0]-c0))
check("phase-nat y", (yy[1]-c1) - (rp/r)*(z[1]-c1))
# R_{c, k(2pi/m)}(polar(c,r,alpha)) = polar(c,r,alpha+k(2pi/m)) -- instance of rotAbout_polar
kk = symbols('kk', integer=True, nonnegative=True)
RP2 = R(c, kk*(2*pi/m), polar(c, r, al)); Q2 = polar(c, r, al + kk*(2*pi/m))
check("phase-nat rotate x", RP2[0]-Q2[0]); check("phase-nat rotate y", RP2[1]-Q2[1])

# oc:lem:phase-int: k = j + m q  =>  k*(2pi/m) = j*(2pi/m) + q*2pi
j, qq = symbols('j qq', integer=True)
check("phase-int split", (j + m*qq)*(2*pi/m) - (j*(2*pi/m) + qq*2*pi))
# Euclidean division with positive divisor: Python // and % agree with Int.ediv/emod for m>0
bad = 0
for K in range(-40, 41):
    for MM in range(1, 13):
        Qp, Rp = K // MM, K % MM
        if not (0 <= Rp < MM and K == Rp + MM*Qp and Qp == floor(Rational(K, MM))):
            bad += 1
print(("OK  " if bad == 0 else "FAIL"), "euclidean division = floor division for m>0 (exhaustive small range)")
ok = ok and bad == 0

# oc:lem:cell: (J1u+psi1)-(J2u+psi2) = (J1-J2-1)u + psi1 + (u - psi2)
J1, J2, u, ps1, ps2 = symbols('J1 J2 u psi1 psi2', real=True)
check("cell only-if identity", (J1*u+ps1) - (J2*u+ps2) - ((J1-J2-1)*u + ps1 + (u-ps2)))
check("cell if: (J1+1)u = J1 u + u", (J1+1)*u - (J1*u + u))

# oc:lem:reduce
N, Rr, Qr, J, ps = symbols('N Rr Qr J psi', real=True)
# with N u = 2 pi: 2pi - (R u + psi) = (N-1-R) u + (u - psi)
check("reduce (ii)", (N*u) - (Rr*u + ps) - ((N-1-Rr)*u + (u-ps)))
check("reduce (iii)", (Rr + N*Qr)*u + ps - (Rr*u + ps + Qr*(N*u)))

# oc:lem:antipode-cell
JJ = symbols('JJ', integer=True)
check("antipode-odd rewrite", JJ*(pi/m) + ps + pi - ((JJ + m)*(pi/m) + ps))
check("antipode-odd Nu=2pi", (2*m)*(pi/m) - 2*pi)
check("antipode-even rewrite", JJ*(2*pi/(k+k)) + ps + pi - ((JJ + k)*(2*pi/(k+k)) + ps))
check("antipode-even Nu=2pi", (k+k)*(2*pi/(k+k)) - 2*pi)

# remark oc:rem:halfopen (1): J1=0, psi1=u, J2=1, psi2=0
check("halfopen (1)", (0*u + u) - (1*u + 0))

# oc:rem:layers (3) example (exact arithmetic)
half = Rational(1, 2)
outer = [(2, 0), (0, 2), (-2, 0), (0, -2)]
inner = [(half, half), (-half, half), (-half, -half), (half, -half)]
S = [(Integer(a), Integer(b)) for a, b in outer] + [(Rational(a), Rational(b)) for a, b in inner]
rot90 = lambda pt: (-pt[1], pt[0])  # rotation by pi/2 about the origin
img = set(rot90(pt) for pt in S)
print(("OK  " if img == set(S) else "FAIL"), "rotation by pi/2 maps S onto S")
ok = ok and img == set(S)
# general position: no three distinct collinear
col = [tr for tr in itertools.combinations(S, 3) if orient(*tr) == 0]
print(("OK  " if not col else "FAIL"), "S in general position (all", len(list(itertools.combinations(S, 3))), "triples)", col)
ok = ok and not col
# rotation used in the theorem is R_{c, 2pi/4} = rotation by pi/2
check("R_{0,2pi/4} is rot90 x", R((0, 0), 2*pi/4, p)[0] - (-p1))
check("R_{0,2pi/4} is rot90 y", R((0, 0), 2*pi/4, p)[1] - p0)
# inner points in conv(outer): explicit convex weights for (1/2,1/2) and symmetric images
w = [Rational(3, 8), Rational(3, 8), Rational(1, 8), Rational(1, 8)]
pt = (sum(wi*o_[0] for wi, o_ in zip(w, outer)), sum(wi*o_[1] for wi, o_ in zip(w, outer)))
print(("OK  " if pt == (half, half) else "FAIL"), "(1/2,1/2) is a convex combination of outer points", pt)
# |x|+|y| for inner points
print("OK  " if all(abs(a)+abs(b) < 2 for a, b in inner) else "FAIL", "inner points satisfy |x|+|y|<2")
# outer points: unique maximisers of +-x, +-y over S
for f, nm in [(lambda P_: P_[0], "x"), (lambda P_: -P_[0], "-x"), (lambda P_: P_[1], "y"), (lambda P_: -P_[1], "-y")]:
    vals = [f(P_) for P_ in S]; mx = max(vals)
    arg = [P_ for P_ in S if f(P_) == mx]
    print(("OK  " if len(arg) == 1 and arg[0] in [(Integer(a), Integer(b)) for a, b in outer] else "FAIL"),
          "unique maximiser of", nm, "over S:", arg)
# inner points: unique maximisers of +-x+-y over the inner points
I = [(Rational(a), Rational(b)) for a, b in inner]
for sx, sy in itertools.product([1, -1], [1, -1]):
    vals = [sx*P_[0] + sy*P_[1] for P_ in I]; mx = max(vals)
    arg = [P_ for P_ in I if sx*P_[0] + sy*P_[1] == mx]
    print(("OK  " if len(arg) == 1 else "FAIL"), "unique maximiser of", (sx, sy), "over inner:", arg)
# polar forms
pp = polar((0, 0), 2, 0); print("OK  " if (simplify(pp[0]-2), simplify(pp[1])) == (0, 0) else "FAIL", "(2,0)=polar(c,2,0)")
pp = polar((0, 0), sqrt(2)/2, pi/4)
print("OK  " if (simplify(pp[0]-half), simplify(pp[1]-half)) == (0, 0) else "FAIL", "(1/2,1/2)=polar(c,sqrt2/2,pi/4)")
check("beta-alpha = pi/4 = 1*pi/m for m=4", (pi/4 - 0) - 1*pi/4)
# is pi/4 a multiple of 2pi/4? (must not be, consistent with the theorem)
print("OK  " if (pi/4)/(2*pi/4) == half else "FAIL", "pi/4 = (1/2)*(2pi/4), not an integer multiple")

# oc:rem:parity table
def inv(tau):
    return sum(1 for i in range(3) for jj in range(i+1, 3) if tau[i] > tau[jj])
def compose(s_, t_):  # (s t)(i) = s(t(i))
    return tuple(s_[t_[i]] for i in range(3))
def swap(x_, y_):
    t_ = list(range(3)); t_[x_], t_[y_] = t_[y_], t_[x_]; return tuple(t_)
ident = (0, 1, 2)
table = {"012": (ident, 0, 1), "102": (swap(0, 1), 1, -1), "021": (swap(1, 2), 1, -1),
         "210": (swap(0, 2), 3, -1), "120": (compose(swap(0, 1), swap(1, 2)), 2, 1),
         "201": (compose(swap(1, 2), swap(0, 1)), 2, 1)}
for key, (tau, iv, sg) in table.items():
    good = ("".join(map(str, tau)) == key) and inv(tau) == iv and (-1)**inv(tau) == sg
    ok = ok and good
    print(("OK  " if good else "FAIL"), "parity table row", key, tau, inv(tau))
# inv(a) = inv(sigma^{-1}) when a o sigma is increasing (distinct labels)
bad = 0
for a_ in itertools.permutations([3, 7, 11]):
    sigma = tuple(sorted(range(3), key=lambda i: a_[i]))  # a o sigma increasing
    sinv = tuple(sigma.index(i) for i in range(3))
    if inv(a_) != inv(sinv):
        bad += 1
print(("OK  " if bad == 0 else "FAIL"), "inv(a) = inv(sigma^{-1}) for the sorting permutation (all 6 orders)")
ok = ok and bad == 0

# oc:def:keys(a): existence n = floor((b-a)/p): np <= b-a < np+p (spot checks with exact rationals)
bad = 0
for bnum in range(-30, 31):
    for pnum in [1, 2, 3, 7]:
        bb = Rational(bnum, 3); aa = Rational(-1, 5); pp_ = Rational(pnum, 2)
        nn = floor((bb-aa)/pp_)
        if not (aa <= bb - nn*pp_ < aa + pp_):
            bad += 1
print(("OK  " if bad == 0 else "FAIL"), "toIcoDiv existence via floor (spot checks)")
ok = ok and bad == 0

print("ALL OK" if ok else "SOME FAILURE")

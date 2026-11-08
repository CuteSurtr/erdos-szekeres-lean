"""Referee checks for section oc (polish round 1). Short symbolic and exact checks only."""
import itertools, math, random
from fractions import Fraction as Fr
import sympy as sp

ok = True
def check(name, cond):
    global ok
    print(("OK   " if cond else "FAIL ") + name)
    ok = ok and bool(cond)

a0,a1,b0,b1,d0,d1,c0,c1,p0,p1 = sp.symbols('a0 a1 b0 b1 d0 d1 c0 c1 p0 p1', real=True)
al, be, th, ph, r, rp, l = sp.symbols('alpha beta theta phi r rp l', real=True)
C, S = sp.symbols('C S', real=True)   # free cos, sin

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def rot(c, t, p):
    return (c[0] + sp.cos(t)*(p[0]-c[0]) - sp.sin(t)*(p[1]-c[1]),
            c[1] + sp.sin(t)*(p[0]-c[0]) + sp.cos(t)*(p[1]-c[1]))

def rotCS(c, p):
    return (c[0] + C*(p[0]-c[0]) - S*(p[1]-c[1]),
            c[1] + S*(p[0]-c[0]) + C*(p[1]-c[1]))

def polar(c, rr, t):
    return (c[0] + rr*sp.cos(t), c[1] + rr*sp.sin(t))

cc = (c0, c1); pp = (p0, p1); A = (a0, a1); B = (b0, b1); D = (d0, d1)

# oc:lem:rot-add (a) and (b)
lhs = rot(cc, al, rot(cc, be, pp)); rhs = rot(cc, al+be, pp)
check("rot-add (a)", all(sp.simplify(sp.expand_trig(lhs[i]-rhs[i])) == 0 for i in range(2)))
check("rot-add (b) R_pi = 2c-p", all(sp.simplify(rot(cc, sp.pi, pp)[i] - (2*cc[i]-pp[i])) == 0 for i in range(2)))
check("rot-add (b) R_2pi = id", all(sp.simplify(rot(cc, 2*sp.pi, pp)[i] - pp[i]) == 0 for i in range(2)))

# oc:lem:rot-inv: difference = orient*(S^2+C^2-1) as a polynomial identity in coordinates and C,S
diff = orient(rotCS(cc, A), rotCS(cc, B), rotCS(cc, D)) - orient(A, B, D)
check("rot-inv polynomial identity", sp.expand(diff - orient(A, B, D)*(S**2 + C**2 - 1)) == 0)

# oc:cor:period: k * (2pi/(2k)) = pi
k = sp.symbols('k', positive=True, integer=True)
check("period half-turn angle", sp.simplify(k*(2*sp.pi/(2*k)) - sp.pi) == 0)

# oc:lem:same-ray (iv)
x = (p0, p1)
y = (c0 + l*(p0-c0), c1 + l*(p1-c1))
q = (2*c0-p0, 2*c1-p1)
check("same-ray orient(x,y,q)=0", sp.expand(orient(x, y, q)) == 0)
check("same-ray y-x=(l-1)(x-c)", all(sp.expand(y[i]-x[i]-(l-1)*(x[i]-cc[i])) == 0 for i in range(2)))
check("same-ray (iii) y=q <=> (l+1)(x-c)=0", all(sp.expand((y[i]-q[i]) - (l+1)*(x[i]-cc[i])) == 0 for i in range(2)))

# oc:lem:polar-rot (a), (b)
lhs = rot(cc, ph, polar(cc, r, th)); rhs = polar(cc, r, th+ph)
check("polar-rot (a)", all(sp.simplify(sp.expand_trig(lhs[i]-rhs[i])) == 0 for i in range(2)))
n = sp.symbols('n', integer=True)
check("polar-rot (b)", all(sp.simplify(polar(cc, r, th+n*2*sp.pi)[i]-polar(cc, r, th)[i]) == 0 for i in range(2)))

# oc:lem:phase-nat: y - c = (r'/r)(z - c) where z = polar(c,r,beta), y = polar(c,r',beta)
z = polar(cc, r, be); yy = polar(cc, rp, be)
check("phase-nat ray identity", all(sp.simplify((yy[i]-cc[i]) - (rp/r)*(z[i]-cc[i])) == 0 for i in range(2)))

# oc:lem:phase-int: k*(2pi/m) = j*(2pi/m) + q*2pi when k = j + m q
m_, j_, q_ = sp.symbols('m j q', positive=True)
check("phase-int split", sp.simplify((j_+m_*q_)*(2*sp.pi/m_) - (j_*(2*sp.pi/m_) + q_*2*sp.pi)) == 0)

# oc:lem:swap: the three cases
t0 = (a0, a1); t1 = (b0, b1); t2 = (d0, d1)
o = orient(t0, t1, t2)
check("swap(1,2)", sp.expand(orient(t0, t2, t1) + o) == 0)
check("swap(0,1)", sp.expand(orient(t1, t0, t2) + o) == 0)
check("swap(0,2)", sp.expand(orient(t2, t1, t0) + o) == 0)
check("cyclic rule step (t1,t0,t2)->(t0,t2,t1)", sp.expand(orient(t1, t0, t2) - orient(t0, t2, t1)) == 0)
check("cyclic rule step (t2,t1,t0)->(t1,t0,t2)", sp.expand(orient(t2, t1, t0) - orient(t1, t0, t2)) == 0)

# oc:lem:cell: identities used
u, p1_, p2_, J1, J2, N_, R_, psi = sp.symbols('u psi1 psi2 J1 J2 N R psi')
check("cell only-if identity", sp.expand((J1*u+p1_)-(J2*u+p2_) - ((J1-J2-1)*u + p1_ + (u-p2_))) == 0)
check("reduce (ii) identity", sp.expand((N_*u - (R_*u+psi)) - ((N_-1-R_)*u + (u-psi))) == 0)
Q_ = sp.symbols('Q')
check("reduce (iii) identity", sp.expand(((R_+N_*Q_)*u+psi) - (R_*u+psi+Q_*(N_*u))) == 0)

# oc:lem:antipode-cell angle identities
J, mm = sp.symbols('J m', positive=True)
check("antipode_odd angle", sp.simplify(J*sp.pi/mm + psi + sp.pi - ((J+mm)*sp.pi/mm + psi)) == 0)
check("antipode_even angle", sp.simplify(J*2*sp.pi/(2*k) + psi + sp.pi - ((J+k)*2*sp.pi/(2*k) + psi)) == 0)

# numeric check of antipode_odd/even and reduce_mod_two_pi against a direct toIcoMod
def toIcoMod(b):  # representative of b mod 2pi in [0,2pi)
    return b - math.floor(b/(2*math.pi))*2*math.pi
rnd = random.Random(7); bad = 0
for _ in range(20000):
    m = rnd.randint(1, 12); Jv = rnd.randint(-50, 50)
    psiv = rnd.random()*math.pi/m*0.999
    lhs = toIcoMod(Jv*(math.pi/m) + psiv + math.pi); rhs = ((Jv+m) % (2*m))*(math.pi/m) + psiv
    if abs(lhs-rhs) > 1e-9: bad += 1
    if m % 2 == 0:
        psiv2 = rnd.random()*2*math.pi/m*0.999
        lhs = toIcoMod(Jv*(2*math.pi/m) + psiv2 + math.pi); rhs = ((Jv+m//2) % m)*(2*math.pi/m) + psiv2
        if abs(lhs-rhs) > 1e-9: bad += 1
check("antipode cells numeric (20000 samples; Python % is floor-mod = Int.emod for positive modulus)", bad == 0)

# oc:rem:layers example
pts = [(Fr(2),Fr(0)),(Fr(-2),Fr(0)),(Fr(0),Fr(2)),(Fr(0),Fr(-2))] + [(Fr(e1,2),Fr(e2,2)) for e1 in (1,-1) for e2 in (1,-1)]
gp = all(orient(a, b, c2) != 0 for a, b, c2 in itertools.combinations(pts, 3))
check("example: general position (all 56 triples)", gp)
comb_ok = True
for e1 in (1, -1):
    for e2 in (1, -1):
        v = [Fr(3,8)*2*e1 + Fr(1,8)*(-2*e1), Fr(3,8)*2*e2 + Fr(1,8)*(-2*e2)]
        comb_ok &= (v[0] == Fr(e1,2) and v[1] == Fr(e2,2))
check("example: convex combinations of the inner points", comb_ok)
rot90 = lambda p: (-p[1], p[0])
check("example: rotation by pi/2 maps S onto S", sorted(map(rot90, pts)) == sorted(pts))
check("example: polar(0, sqrt2/2, pi/4) = (1/2,1/2)", all(sp.simplify(polar((0,0), sp.sqrt(2)/2, sp.pi/4)[i] - sp.Rational(1,2)) == 0 for i in range(2)))
# outer points unique maximisers of +-x, +-y; inner points unique maximisers of +-x+-y among inner points
outer = pts[:4]; inner = pts[4:]
def uniq_max(P, f):
    vals = [f(p) for p in P]; mx = max(vals); return [p for p in P if f(p) == mx]
fs = [lambda p: p[0], lambda p: -p[0], lambda p: p[1], lambda p: -p[1]]
check("example: each outer point unique maximiser in S", sorted(sum((uniq_max(pts, f) for f in fs), [])) == sorted(outer))
gs = [lambda p, s=s, t=t: s*p[0]+t*p[1] for s in (1,-1) for t in (1,-1)]
check("example: each inner point unique maximiser in inner", sorted(sum((uniq_max(inner, g) for g in gs), [])) == sorted(inner))

# oc:rem:parity table: inversions vs sign via cycle structure, and inv(a) = inv(sigma^{-1})
def inv(lst): return sum(1 for i in range(len(lst)) for j in range(i+1, len(lst)) if lst[i] > lst[j])
def sign(perm):
    seen = set(); s = 1
    for i in range(len(perm)):
        if i in seen: continue
        L = 0; j = i
        while j not in seen:
            seen.add(j); j = perm[j]; L += 1
        s *= (-1)**(L-1)
    return s
tab_ok = all((-1)**inv(t) == sign(t) for t in itertools.permutations(range(3)))
check("parity table: (-1)^inv = sign for all 6 permutations", tab_ok)
inv_ok = True
for a in itertools.permutations([5, 11, 17]):
    sigma = sorted(range(3), key=lambda i: a[i])   # a o sigma increasing
    sinv = [sigma.index(i) for i in range(3)]
    inv_ok &= (inv(a) == inv(sinv)) and (sign(sigma) == sign(sinv))
check("inv(a) = inv(sigma^-1) when sigma sorts a; sgn sigma = sgn sigma^-1", inv_ok)
# gen_b2: order = sorted(range(3), key=rt) is the list sigma(0)sigma(1)sigma(2); perm_sign(order) = sgn sigma
gb_ok = all((-1)**inv(sorted(range(3), key=lambda i: a[i])) == sign(sorted(range(3), key=lambda i: a[i]))
            for a in itertools.permutations([2, 3, 9]))
check("gen_b2 perm_sign(order) = sgn(sigma)", gb_ok)

print("ALL OK" if ok else "SOME CHECK FAILED")

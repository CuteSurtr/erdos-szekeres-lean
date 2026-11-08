"""Symbolic checks of every algebraic/trigonometric identity used in section sr (rigor lens, round 1)."""
import sympy as sp

ok = True
def check(name, expr):
    global ok
    e = sp.simplify(sp.expand(expr))
    res = (e == 0)
    if not res:
        ok = False
    print(("OK   " if res else "FAIL ") + name + ("" if res else f"   residual: {e}"))

R = dict(real=True)
x, y, x1, y1, x2, y2 = sp.symbols('x y x1 y1 x2 y2', **R)
p0, p1, q0, q1, c0, c1, a0, a1, u0, u1, r0, r1, t, th = sp.symbols('p0 p1 q0 q1 c0 c1 a0 a1 u0 u1 r0 r1 t th', **R)
v0, v1, w0, w1, X0, X1 = sp.symbols('v0 v1 w0 w1 X0 X1', **R)
I = sp.I

def re(z): return sp.re(sp.expand(z))
def im(z): return sp.im(sp.expand(z))
def conj(z): return sp.conjugate(z)
def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
def edist2(p, q):
    return (p[0]-q[0])**2 + (p[1]-q[1])**2

# Conventions: <z,w> = Re(z conj w) = Re z Re w + Im z Im w
z = x1 + I*y1; w = x2 + I*y2
check("inner product Re(z wbar) = x1x2+y1y2", re(z*conj(w)) - (x1*x2 + y1*y2))
check("|z-w|^2 = |z|^2 - 2<z,w> + |w|^2", (x1-x2)**2+(y1-y2)**2 - ((x1**2+y1**2) - 2*(x1*x2+y1*y2) + (x2**2+y2**2)))

# Remark sup: rotation by 2pi/3 of c+(1,0)
cth, sth = sp.cos(2*sp.pi/3), sp.sin(2*sp.pi/3)
check("cos(2pi/3) = -1/2", cth + sp.Rational(1, 2))
check("sin(2pi/3) = sqrt3/2", sth - sp.sqrt(3)/2)
print("    sup dist after rotation:", sp.Max(sp.Abs(cth), sp.Abs(sth)), "(should be sqrt(3)/2 != 1)")
print("    sup dist (0,0)-(3,4):", max(3, 4))

# Lemma complex (d): eDist2 = normSq(toC p - toC q)
P = p0 + I*p1; Q = q0 + I*q1
check("eDist2 = normSq(p^-q^)", edist2((p0, p1), (q0, q1)) - re((P-Q)*conj(P-Q)))

# Lemma crot (c),(e),(g)
cc, ww, vv, zz = sp.symbols('cc ww vv zz')  # complex
check("crot_comp: c + w((c+v(z-c)) - c) = c + wv(z-c)", (cc + ww*((cc + vv*(zz-cc)) - cc)) - (cc + ww*vv*(zz-cc)))
check("crot_eq_self: c + w(z-c) - z = (w-1)(z-c)", (cc + ww*(zz-cc) - zz) - (ww-1)*(zz-cc))

# Lemma rot-half (a): exp(i th)(x+iy) = (x cos - y sin) + i(x sin + y cos)
lhs = sp.expand((sp.cos(th) + I*sp.sin(th))*(x + I*y))
check("rotAbout re part", re(lhs) - (x*sp.cos(th) - y*sp.sin(th)))
check("rotAbout im part", im(lhs) - (x*sp.sin(th) + y*sp.cos(th)))
# full rotAbout vs crot formula
C = c0 + I*c1
rot_p = (c0 + sp.cos(th)*(p0-c0) - sp.sin(th)*(p1-c1), c1 + sp.sin(th)*(p0-c0) + sp.cos(th)*(p1-c1))
crot_val = sp.expand(C + (sp.cos(th) + I*sp.sin(th))*(P - C))
check("rotAbout = crot (re)", re(crot_val) - rot_p[0])
check("rotAbout = crot (im)", im(crot_val) - rot_p[1])
# rot-half (b): halfTurn
ht = (2*c0 - p0, 2*c1 - p1)
hv = sp.expand(C + (-1)*(P - C))
check("halfTurn = crot(-1) (re)", re(hv) - ht[0])
check("halfTurn = crot(-1) (im)", im(hv) - ht[1])

# Lemma refl
def reflLine(a, u, p):
    d = (p[0]-a[0])*u[0] + (p[1]-a[1])*u[1]
    return (a[0] + 2*d*u[0] - (p[0]-a[0]), a[1] + 2*d*u[1] - (p[1]-a[1]))
A = (a0, a1); U = (u0, u1); Pp = (p0, p1)
X, Y = p0 - a0, p1 - a1
Uc = u0 + I*u1; Ac = a0 + I*a1
rl = reflLine(A, U, Pp)
# (a) expansions
exp_a = sp.expand(Uc**2*conj(X + I*Y))
check("refl(a): Re(u^2 conj(x+iy)) = (u0^2-u1^2)x + 2u0u1 y", re(exp_a) - ((u0**2-u1**2)*X + 2*u0*u1*Y))
check("refl(a): Im(u^2 conj(x+iy)) = 2u0u1 x - (u0^2-u1^2) y", im(exp_a) - (2*u0*u1*X - (u0**2-u1**2)*Y))
d = X*u0 + Y*u1
check("refl(a): 2du0 - x = (2u0^2-1)x + 2u0u1 y", (2*d*u0 - X) - ((2*u0**2-1)*X + 2*u0*u1*Y))
check("refl(a): 2du1 - y = 2u0u1 x + (2u1^2-1) y", (2*d*u1 - Y) - (2*u0*u1*X + (2*u1**2-1)*Y))
check("refl(a): re difference = x(u0^2+u1^2-1)", (2*d*u0 - X) - re(exp_a) - X*(u0**2+u1**2-1))
check("refl(a): im difference = y(u0^2+u1^2-1)", (2*d*u1 - Y) - im(exp_a) - Y*(u0**2+u1**2-1))
# (a) full statement under the constraint u1^2 = 1 - u0^2 (substitute)
full = sp.expand(Ac + Uc**2*conj(P - Ac))
sub = {u1**2: 1 - u0**2}
diff_re = sp.expand(rl[0] - re(full))
diff_im = sp.expand(rl[1] - im(full))
# reduce modulo u0^2+u1^2-1 using polynomial division
G = u0**2 + u1**2 - 1
_, rem_re = sp.reduced(diff_re, [G], u1, u0, a0, a1, p0, p1)
_, rem_im = sp.reduced(diff_im, [G], u1, u0, a0, a1, p0, p1)
check("refl(a) full statement modulo u0^2+u1^2=1 (re)", rem_re)
check("refl(a) full statement modulo u0^2+u1^2=1 (im)", rem_im)
# (b) involution modulo the unit constraint
rr = reflLine(A, U, rl)
_, rb0 = sp.reduced(sp.expand(rr[0] - p0), [G], u1, u0, a0, a1, p0, p1)
_, rb1 = sp.reduced(sp.expand(rr[1] - p1), [G], u1, u0, a0, a1, p0, p1)
check("refl(b) involution coordinate 0 (mod unit)", rb0)
check("refl(b) involution coordinate 1 (mod unit)", rb1)
# (b) complex: u^2 conj(u^2 conj(zeta)) = (u ubar)^2 zeta
zeta = sp.symbols('zeta')
check("refl(b) complex step", sp.expand(Uc**2*conj(Uc**2*conj(zeta))) - sp.expand((Uc*conj(Uc))**2*zeta))
# (c) fixed point equations: a0+2du0-x = a0+x  <=> du0 = x ; similarly; then x u1 - y u0 = 0
e0 = (rl[0] - p0)  # = 2du0 - 2x
e1 = (rl[1] - p1)
check("refl(c): rl0 - p0 = 2(d u0 - x)", e0 - 2*(d*u0 - X))
check("refl(c): rl1 - p1 = 2(d u1 - y)", e1 - 2*(d*u1 - Y))
# Lean's linear combination: (-(u1)/2)*h0 + (u0/2)*h1 where h0: rl0 = p0
check("refl(c): Lean combination gives cross", (-(u1)/2)*e0 + (u0/2)*e1 - ( (X)*u1 - (Y)*u0 ) * 1)
# Fixed points = mirror: p = a + t u => d = t |u|^2, reflLine(p) = p when |u|=1
pt = (a0 + t*u0, a1 + t*u1)
rlt = reflLine(A, U, pt)
_, f0 = sp.reduced(sp.expand(rlt[0] - pt[0]), [G], u1, u0, a0, a1, t)
_, f1 = sp.reduced(sp.expand(rlt[1] - pt[1]), [G], u1, u0, a0, a1, t)
check("classes remark: p=a+tu is fixed (coord 0, mod unit)", f0)
check("classes remark: p=a+tu is fixed (coord 1, mod unit)", f1)
check("classes remark: d = t(u0^2+u1^2) at p = a+tu", ((pt[0]-a0)*u0 + (pt[1]-a1)*u1) - t*(u0**2+u1**2))
# u = 0 gives the half-turn about a
rl0 = reflLine(A, (0, 0), Pp)
check("u=0: reflLine = halfTurn_a (0)", rl0[0] - (2*a0 - p0))
check("u=0: reflLine = halfTurn_a (1)", rl0[1] - (2*a1 - p1))
# (d) identity (v x w)(u0^2+u1^2) = (w.u)(v x u) - (v.u)(w x u)
cross = lambda a, b: a[0]*b[1] - a[1]*b[0]
dot = lambda a, b: a[0]*b[0] + a[1]*b[1]
V = (v0, v1); W = (w0, w1)
check("refl(d) identity", cross(V, W)*(u0**2+u1**2) - (dot(W, U)*cross(V, U) - dot(V, U)*cross(W, U)))
check("orient(p,q,r) = (q-p) x (r-p)", orient((p0, p1), (q0, q1), (r0, r1)) - cross((q0-p0, q1-p1), (r0-p0, r1-p1)))
check("(q-p) x u = (q-a) x u - (p-a) x u", cross((q0-p0, q1-p1), U) - (cross((q0-a0, q1-a1), U) - cross((p0-a0, p1-a1), U)))

# Theorem structure (a)
aa = sp.symbols('aa'); al, be = sp.symbols('alpha beta', real=True)
xi = sp.symbols('xi')
# <xi, ia> = Re(xi * conj(i a)) = Re(-i xi abar)
check("<xi,ia> = Re(-i xi abar)", sp.expand(xi*conj(I*aa)) - sp.expand(-I*xi*conj(aa)))
# with abar xi = alpha + i beta: Re(-i(alpha+i beta)) = beta
check("Re(-i(alpha + i beta)) = beta", re(-I*(al + I*be)) - be)
check("Re(alpha + i beta) = alpha", re(al + I*be) - al)
# <z,1> = x, <z,i> = y for z = x+iy
check("<z,1> = x", re((x + I*y)*conj(1)) - x)
check("<z,i> = y", re((x + I*y)*conj(I)) - y)
# x a + y (i a) = a z ; x a + y(-i a) = a conj(z)
check("xa + y(ia) = a(x+iy)", sp.expand(x*aa + y*(I*aa) - aa*(x + I*y)))
check("xa + y(-ia) = a(x-iy)", sp.expand(x*aa + y*(-I*aa) - aa*(x - I*y)))
# <xi,-ia>(-ia) = <xi,ia>(ia): bilinearity sign
check("<xi,e>e for e=-ia equals <xi,ia>ia", sp.expand(re(xi*conj(-I*aa))*(-I*aa) - re(xi*conj(I*aa))*(I*aa)))
# v = e abar with e = v a when |a|=1: e abar a = e |a|^2

# Theorem structure (b)
bb, pp_ = sp.symbols('bb pp')
cdef = bb/(1-aa)
check("case R: c + a(p - c) = a p + b with c=b/(1-a)", sp.simplify(cdef + aa*(pp_ - cdef) - (aa*pp_ + bb)))
# case C: g(g(p)) = a conj(a conj(p) + b) + b = a abar p + a bbar + b
gg = aa*conj(aa*conj(pp_) + bb) + bb
check("case C: g(g p) expansion", sp.expand(gg - (aa*conj(aa)*pp_ + aa*conj(bb) + bb)))
# reflection: b/2 + u^2 conj(p - b/2) with u^2 = a, a bbar = -b  gives a conj p + b
expr = bb/2 + aa*conj(pp_ - bb/2)
check("case C: b/2 + a conj(p - b/2) = a conj p + b/2 - a bbar/2", sp.expand(expr - (aa*conj(pp_) + bb/2 - aa*conj(bb)/2)))
# substitute a*conj(b) = -b
expr2 = sp.expand(aa*conj(pp_) + bb/2 - (-bb)/2)
check("case C: with a bbar = -b, equals a conj p + b", expr2 - (aa*conj(pp_) + bb))
# |u|^2 = |a| when u^2=a (numerical sanity skipped; follows from |u^2|=|u|^2)

# Lemma concyclic
Pc = (p0, p1); Cc = (c0, c1); Xc = (X0, X1)
qpt = (p0 - (p1 - c1), p1 + (p0 - c0))
o = orient(Pc, qpt, Xc)
check("concyclic: orient(p,q,x) = -[(p0-c0)(x0-p0)+(p1-c1)(x1-p1)]", o + ((p0-c0)*(X0-p0) + (p1-c1)*(X1-p1)))
check("concyclic: = 1/2(eDist2(x,p)+eDist2(p,c)-eDist2(x,c))", o - sp.Rational(1, 2)*(edist2(Xc, Pc) + edist2(Pc, Cc) - edist2(Xc, Cc)))
check("concyclic: |x-c|^2 = |x-p|^2 + 2<x-p,p-c> + |p-c|^2", edist2(Xc, Cc) - (edist2(Xc, Pc) + 2*((X0-p0)*(p0-c0) + (X1-p1)*(p1-c1)) + edist2(Pc, Cc)))

# Lemma supports: phi(x) = orient(p,q,x) is affine
lam = sp.symbols('lam', real=True)
qq = (q0, q1)
xa = (X0, X1); yb = (r0, r1)
comb = (lam*X0 + (1-lam)*r0, lam*X1 + (1-lam)*r1)
check("supports: orient(p,q,.) affine", orient(Pc, qq, comb) - (lam*orient(Pc, qq, xa) + (1-lam)*orient(Pc, qq, yb)))
check("supports: phi(p) = 0", orient(Pc, qq, Pc))

# Lemma center: orient(q, c, 2c - q) = 0
Qq = (q0, q1)
check("center: orient(q,c,2c-q) = 0", orient(Qq, Cc, (2*c0 - q0, 2*c1 - q1)))
check("center: explicit form", orient(Qq, Cc, (2*c0 - q0, 2*c1 - q1)) - ((c0-q0)*2*(c1-q1) - (c1-q1)*2*(c0-q0)))

# Lemma eDist2_crot_center: normSq(c + w(z-c) - c) = normSq(w) normSq(z-c)
check("crot center: c + w(z-c) - c = w(z-c)", sp.expand(cc + ww*(zz-cc) - cc - ww*(zz-cc)))

# (P) trivia: 2u0^2 - 1 = u0^2 - u1^2 mod unit
_, rr1 = sp.reduced(sp.expand((2*u0**2 - 1) - (u0**2 - u1**2)), [G], u1, u0)
check("2u0^2-1 = u0^2-u1^2 (mod unit)", rr1)
_, rr2 = sp.reduced(sp.expand((2*u1**2 - 1) + (u0**2 - u1**2)), [G], u1, u0)
check("2u1^2-1 = -(u0^2-u1^2) (mod unit)", rr2)

# Primitive root facts used: exp(2 pi i/4)^2 = -1, exp(2pi i/3), exp(2 pi i/5)
z4 = sp.exp(2*sp.pi*I/4)
check("exp(2pi i/4)^2 = -1", sp.simplify(z4**2 + 1))
for n in (3, 4, 5):
    zn = sp.exp(2*sp.pi*I/n)
    check(f"exp(2pi i/{n})^{n} = 1", sp.simplify(zn**n - 1))
    for l in range(1, n):
        val = sp.simplify(zn**l - 1)
        if val == 0:
            ok = False
            print(f"FAIL exp(2pi i/{n})^{l} = 1 unexpectedly")
print("    primitive: no smaller power equals 1 for n=3,4,5 (checked)")

# arithmetic used in case lemmas
def least_multiple_at_least(m, lo):
    k = -(-lo // m)
    return k*m
print("    3 | n >= 32 -> n >=", least_multiple_at_least(3, 32), "; 5 | n >= 32 -> n >=", least_multiple_at_least(5, 32),
      "; 2 | n >= 33 -> n >=", least_multiple_at_least(2, 33), "; 2 | n >= 31 -> n >=", least_multiple_at_least(2, 31),
      "; 4 | n >= 33 -> n >=", least_multiple_at_least(4, 33))
print("    32 mod 3 =", 32 % 3, "; 34 mod 5 =", 34 % 5)
print("ALL OK" if ok else "SOME CHECK FAILED")

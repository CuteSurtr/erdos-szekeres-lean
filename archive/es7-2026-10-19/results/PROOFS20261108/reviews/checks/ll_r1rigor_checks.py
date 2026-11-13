"""Symbolic checks of the identities used in section ll (round 1, rigor lens)."""
import itertools
import sympy as sp

ok = True
def check(name, expr_zero):
    global ok
    val = sp.simplify(sp.expand(expr_zero))
    res = (val == 0)
    ok = ok and res
    print(f"{'OK ' if res else 'FAIL'} {name}: residual = {val}")

th, al = sp.symbols('theta alpha', real=True)
p0, p1, c0, c1, v0, v1 = sp.symbols('p0 p1 c0 c1 v0 v1', real=True)
I = sp.I

def rho(c, t, p):
    return (c[0] + sp.cos(t)*(p[0]-c[0]) - sp.sin(t)*(p[1]-c[1]),
            c[1] + sp.sin(t)*(p[0]-c[0]) + sp.cos(t)*(p[1]-c[1]))

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

c = (c0, c1); p = (p0, p1); v = (v0, v1)

# Lemma rot (a): gamma + e^{i theta}(u - gamma) has Re/Im = coordinates of rho
u = p0 + I*p1; g = c0 + I*c1
w = sp.cos(th) + I*sp.sin(th)
z = sp.expand(g + w*(u - g))
r = rho(c, th, p)
check("rot(a) real part", sp.re(z) - r[0])
check("rot(a) imag part", sp.im(z) - r[1])
check("Euler e^{i theta} = cos + i sin", sp.exp(I*th).rewrite(sp.cos) - w)

# Lemma rot (b): rho(v+p) = A v + rho(p)
vp = (v0 + p0, v1 + p1)
Av = (sp.cos(th)*v0 - sp.sin(th)*v1, sp.sin(th)*v0 + sp.cos(th)*v1)
rvp = rho(c, th, vp)
check("rot(b) coord 0", rvp[0] - (Av[0] + r[0]))
check("rot(b) coord 1", rvp[1] - (Av[1] + r[1]))
# rho(p) = A(p-c) + c
Apc = (sp.cos(th)*(p0-c0) - sp.sin(th)*(p1-c1), sp.sin(th)*(p0-c0) + sp.cos(th)*(p1-c1))
check("rho(p) = A(p-c)+c coord 0", r[0] - (Apc[0] + c0))
check("rho(p) = A(p-c)+c coord 1", r[1] - (Apc[1] + c1))

# Lemma rot (d): (e^{i alpha})^j = e^{i j alpha}, j natural (check j = 0..6)
for j in range(0, 9):
    # exponential form (trig-form simplification stalls for j >= 5; see ll_r1rigor_demoivre.py)
    check(f"(e^(i a))^{j} = e^(i {j} a)", sp.powsimp(sp.exp(I*al)**j - sp.exp(I*j*al), force=True))

# Lemma complex (d): gamma + w((gamma + v(u-gamma)) - gamma) = gamma + w v (u - gamma)
W, V, G, U = sp.symbols('W V G U')
check("complex(d) crot_comp", G + W*((G + V*(U - G)) - G) - (G + W*V*(U - G)))
# Lemma complex (f): gamma + w(u-gamma) - u = (w-1)(u-gamma)
check("complex(f) crot_eq_self", (G + W*(U - G) - U) - (W - 1)*(U - G))
# Lemma complex (g): crot(p) - crot(q) = w (u - u')
U2 = sp.symbols('U2')
check("complex(g) crot_injective", (G + W*(U - G)) - (G + W*(U2 - G)) - W*(U - U2))

# Lemma minperiod: omega^m = 1, omega^k != 1 for 0<k<m (m = 1..12)
for m in range(1, 13):
    om = sp.exp(2*sp.pi*I/m)
    assert sp.simplify(om**m - 1) == 0, m
    for k in range(1, m):
        assert sp.cos(2*sp.pi*k/m) < 1, (m, k)
        assert sp.simplify(om**k - 1) != 0, (m, k)
print("OK  minperiod: omega^m = 1 and cos(2 pi k/m) < 1, omega^k != 1 for 0<k<m, m=1..12")

# Theorem sixfold step 2: 3 * (2 pi / 6) = pi; rho_{c,pi}(p) = 2c - p; orient(p, c, 2c - p) = 0
check("3*(2pi/6) = pi", 3*(2*sp.pi/6) - sp.pi)
rpi = rho(c, sp.pi, p)
check("rho_{c,pi}(p)_0 = 2c0 - p0", rpi[0] - (2*c0 - p0))
check("rho_{c,pi}(p)_1 = 2c1 - p1", rpi[1] - (2*c1 - p1))
q = (2*c0 - p0, 2*c1 - p1)
check("orient(p, c, 2c-p) = 0", orient(p, c, q))
check("displayed form (c0-p0)*2(c1-p1)-(c1-p1)*2(c0-p0)", orient(p, c, q) - ((c0-p0)*2*(c1-p1) - (c1-p1)*2*(c0-p0)))
# rotAbout_iterate for j = 3, alpha = 2pi/6 via the composition law (symbolic angle sum)
a1, a2 = sp.symbols('a1 a2', real=True)
comp = rho(c, a1, rho(c, a2, p))
r12 = rho(c, a1 + a2, p)
check("rho_a1 o rho_a2 = rho_(a1+a2) coord 0", sp.expand_trig(comp[0] - r12[0]))
check("rho_a1 o rho_a2 = rho_(a1+a2) coord 1", sp.expand_trig(comp[1] - r12[1]))

# Lemma hv (c) exchange step: z = sum alpha_a a + lam y, y = sum beta_a a + mu z
# => (1 - lam mu) z = sum (alpha_a + lam beta_a) a ; coefficient sum = 1 when sums are 1
lam, mu = sp.symbols('lambda mu')
n = 3
al_ = sp.symbols('al0:%d' % n); be_ = sp.symbols('be0:%d' % n)
A = sp.symbols('A0:%d' % n)
Z = sp.Symbol('Z')
Y = sum(be_[i]*A[i] for i in range(n)) + mu*Z
lhs = sum(al_[i]*A[i] for i in range(n)) + lam*Y  # = z
# z = lhs  =>  z - lam*mu*z = sum (al + lam be) a
check("hv(c) substitution", (lhs - lam*mu*Z) - sum((al_[i] + lam*be_[i])*A[i] for i in range(n)))
sa = sp.Symbol('sa'); sb = sp.Symbol('sb')  # sa = sum alpha = 1-lam, sb = sum beta = 1-mu
check("hv(c) coefficient sum", ((1 - lam) + lam*(1 - mu)) - (1 - lam*mu))

# (C5): f(sum l_i a_i) = sum l_i f(a_i) when sum l_i = 1, f(x) = L x + b (1-dim components suffice)
l1, l2, l3, L, b, x1, x2, x3 = sp.symbols('l1 l2 l3 L b x1 x2 x3')
expr = (L*(l1*x1 + l2*x2 + l3*x3) + b) - (l1*(L*x1 + b) + l2*(L*x2 + b) + l3*(L*x3 + b))
check("(C5) affine map preserves convex combinations (mod sum=1)", expr.subs(l3, 1 - l1 - l2))

# Lemma hv (b): x = lam_j s_j + (1-lam_j) y_j with y_j = sum_{i!=j} lam_i/(1-lam_j) s_i
ls = sp.symbols('ls0:4'); ss = sp.symbols('ss0:4')
j = 1
yj = sum(ls[i]/(1 - ls[j])*ss[i] for i in range(4) if i != j)
xx = sum(ls[i]*ss[i] for i in range(4))
check("hv(b) split x = l_j s_j + (1-l_j) y_j", sp.simplify(xx - (ls[j]*ss[j] + (1 - ls[j])*yj)))
check("hv(b) y_j coefficients sum to 1 (given sum l = 1)",
      sp.simplify(sum(ls[i]/(1 - ls[j]) for i in range(4) if i != j).subs(ls[3], 1 - ls[0] - ls[1] - ls[2]) - 1))

# Lemma orbit (e): 0<=i<j<=p-1  =>  1 <= p-j+i <= p-1  (brute force p <= 40)
for P in range(1, 41):
    for jj in range(P):
        for ii in range(jj):
            e = P - jj + ii
            assert 1 <= e <= P - 1, (P, ii, jj)
print("OK  orbit(e): 1 <= p-j+i <= p-1 for all 0<=i<j<=p-1, p<=40")

# card_peel / corollary / octagon arithmetic (natural subtraction)
def tsub(a, b): return max(a - b, 0)
assert 6 * tsub(11, 1) == 60 and 60 < 61
assert 7 * tsub(10, 1) == 63 and 65 - 1 == 64 and 63 < 64
assert 6 * 11 == 66 and 7 * 10 == 70 and 8 <= 12 and 8 <= 14
for m in range(1, 20):
    for t in range(1, 20):
        assert m * tsub(t, 1) == m*t - m < m*t
print("OK  octagon/corollary arithmetic")

print("ALL OK" if ok else "SOME CHECK FAILED")

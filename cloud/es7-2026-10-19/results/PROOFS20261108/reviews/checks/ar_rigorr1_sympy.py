"""Rigor check (round 1) of the identities used in section ar (affine symmetries)."""
import sympy as sp

ok = True
def check(name, expr):
    global ok
    r = sp.simplify(sp.expand(expr))
    good = (r == 0)
    ok = ok and good
    print(f"{'OK ' if good else 'FAIL'} {name}: residual = {r}")

A00, A01, A10, A11, z0, z1 = sp.symbols('A00 A01 A10 A11 z0 z1', real=True)
# Lemma ar:lem:mulvec + ar:lem:nsq-mulvec
Az0 = A00*z0 + A01*z1
Az1 = A10*z0 + A11*z1
gA = A00**2 + A10**2
gB = A00*A01 + A10*A11
gC = A01**2 + A11**2
check("nsq_mulVec", Az0**2 + Az1**2 - (gA*z0**2 + 2*gB*z0*z1 + gC*z1**2))

# Lemma ar:lem:avgq-pos (b), (c)
al, be, ga = sp.symbols('alpha beta gamma', real=True)
Q = lambda x0, x1: al*x0**2 + 2*be*x0*x1 + ga*x1**2
check("avgQ at (1,0) = alpha", Q(1, 0) - al)
check("nsq(-beta, alpha) = alpha^2+beta^2", (-be)**2 + al**2 - (al**2 + be**2))
check("avgQ at (-beta,alpha) = alpha(alpha gamma - beta^2)", Q(-be, al) - al*(al*ga - be**2))
check("middle expression alpha beta^2 + 2 beta(-beta) alpha + gamma alpha^2", al*be**2 + 2*be*(-be)*al + ga*al**2 - al*(al*ga - be**2))

# Lemma ar:lem:lin2 (b): orient scaling of lin2
a, b, c, d, u0, u1, w0, w1 = sp.symbols('a b c d u0 u1 w0 w1', real=True)
lhs = (a*u0 + b*u1)*(c*w0 + d*w1) - (c*u0 + d*u1)*(a*w0 + b*w1)
check("orient_lin2 core", lhs - (a*d - b*c)*(u0*w1 - u1*w0))
# full form with points x,y,z
x0, x1, y0, y1, zz0, zz1 = sp.symbols('x0 x1 y0 y1 zz0 zz1', real=True)
orient = lambda P, R, S: (R[0]-P[0])*(S[1]-P[1]) - (R[1]-P[1])*(S[0]-P[0])
lin = lambda P: (a*P[0] + b*P[1], c*P[0] + d*P[1])
X, Y, Z = (x0, x1), (y0, y1), (zz0, zz1)
check("orient_lin2 full", orient(lin(X), lin(Y), lin(Z)) - (a*d - b*c)*orient(X, Y, Z))

# Lemma ar:lem:orient-affine: orient(Lx+v, Ly+v, Lz+v) = det L * orient(x,y,z)
v0, v1 = sp.symbols('v0 v1', real=True)
aff = lambda P: (A00*P[0] + A01*P[1] + v0, A10*P[0] + A11*P[1] + v1)
check("orient_affine", orient(aff(X), aff(Y), aff(Z)) - (A00*A11 - A01*A10)*orient(X, Y, Z))

# Lemma ar:lem:chol
s, t, bt = sp.symbols('s t beta_', real=True, nonzero=True)
T = lambda P: (s*P[0] + (bt/s)*P[1], 0*P[0] + t*P[1])
Ti = lambda P: ((1/s)*P[0] + (-bt/(s**2*t))*P[1], 0*P[0] + (1/t)*P[1])
Zp = (z0, z1)
TZ = T(Zp)
check("nsq_lin2_chol", TZ[0]**2 + TZ[1]**2 - (s**2*z0**2 + 2*bt*z0*z1 + (bt**2/s**2 + t**2)*z1**2))
TiT = Ti(T(X))
check("chol_inv_left coord0", TiT[0] - x0)
check("chol_inv_left coord1", TiT[1] - x1)
TTi = T(Ti(X))
check("chol_inv_right coord0", TTi[0] - x0)
check("chol_inv_right coord1", TTi[1] - x1)
# the displayed intermediate steps of (b) and (c)
check("chol (b) step", (1/s)*(s*x0 + (bt/s)*x1) - (bt/(s**2*t))*t*x1 - x0)
check("chol (c) step", s*(x0/s - bt*x1/(s**2*t)) + (bt/s)*(x1/t) - x0)
check("chol (c) middle", s*(x0/s - bt*x1/(s**2*t)) + (bt/s)*(x1/t) - (x0 - bt*x1/(s*t) + bt*x1/(s*t)))
# orientation factor of T: ad - bc with (a,b,c,d) = (s, beta/s, 0, t)
check("det T = s t", s*t - (bt/s)*0 - s*t)

# Proposition ar:prop:averaging (b): beta^2/s^2 + t^2 = gamma when s^2 = alpha, t^2 = (alpha gamma - beta^2)/alpha
alp = sp.symbols('alp', positive=True)
check("beta^2/alpha + (alpha gamma - beta^2)/alpha = gamma", be**2/alp + (alp*ga - be**2)/alp - ga)
# Cholesky: T^T T equals the Gram matrix [[alpha, beta],[beta, gamma]] when s = sqrt(alpha), t = sqrt((alpha gamma - beta^2)/alpha)
sa = sp.sqrt(alp)
tt = sp.symbols('tt', positive=True)  # stands for t with t^2 = (alp*ga - be^2)/alp
Tm = sp.Matrix([[sa, be/sa], [0, tt]])
G = (Tm.T*Tm).subs(tt**2, (alp*ga - be**2)/alp)
G = sp.simplify(G)
check("T^T T [0,0] = alpha", G[0, 0] - alp)
check("T^T T [0,1] = beta", G[0, 1] - be)
check("T^T T [1,1] = gamma", sp.simplify(G[1, 1] - ga))

# Lemma ar:lem:fix: four polynomial identities
M00, M01, M10, M11 = sp.symbols('M00 M01 M10 M11', real=True)
delta = u0*w1 - u1*w0
E1 = M00*u0 + M01*u1 - u0
E2 = M10*u0 + M11*u1 - u1
E3 = M00*w0 + M01*w1 - w0
E4 = M10*w0 + M11*w1 - w1
check("fix e00", w1*E1 - u1*E3 - (M00 - 1)*delta)
check("fix e01", -w0*E1 + u0*E3 - M01*delta)
check("fix e10", w1*E2 - u1*E4 - M10*delta)
check("fix e11", -w0*E2 + u0*E4 - (M11 - 1)*delta)

# Lemma ar:lem:inj: Cramer elimination
L00, L01, L10, L11, p0, p1 = sp.symbols('L00 L01 L10 L11 p0 p1', real=True)
h0 = L00*p0 + L01*p1
h1 = L10*p0 + L11*p1
detL = L00*L11 - L01*L10
check("inj v0", L11*h0 - L01*h1 - detL*p0)
check("inj v1", L00*h1 - L10*h0 - detL*p1)

# Lemma ar:lem:cp-affine step 1: f((1-l)x + l y) = (1-l) f(x) + l f(y)
lam = sp.symbols('lam', real=True)
fx = aff((x0, x1)); fy = aff((y0, y1))
fm = aff(((1-lam)*x0 + lam*y0, (1-lam)*x1 + lam*y1))
check("affine combination coord0", fm[0] - ((1-lam)*fx[0] + lam*fy[0]))
check("affine combination coord1", fm[1] - ((1-lam)*fx[1] + lam*fy[1]))

# Prop (a): u0 w1 - u1 w0 with u = p1 - p0, w = p2 - p0 equals orient(p0,p1,p2)
q00, q01, q10, q11, q20, q21 = sp.symbols('q00 q01 q10 q11 q20 q21', real=True)
P0, P1, P2 = (q00, q01), (q10, q11), (q20, q21)
uu = (P1[0]-P0[0], P1[1]-P0[1]); ww = (P2[0]-P0[0], P2[1]-P0[1])
check("u0 w1 - u1 w0 = orient(p0,p1,p2)", uu[0]*ww[1] - uu[1]*ww[0] - orient(P0, P1, P2))

print("ALL_OK" if ok else "SOME_FAIL")

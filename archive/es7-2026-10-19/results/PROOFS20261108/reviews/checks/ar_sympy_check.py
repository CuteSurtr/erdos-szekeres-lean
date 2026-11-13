# Symbolic checks of the identities used in section ar (affine symmetries).
import sympy as sp
import random

ok = True
def check(name, expr):
    global ok
    e = sp.simplify(sp.expand(expr))
    res = (e == 0)
    print(("OK   " if res else "FAIL ") + name)
    if not res:
        ok = False
        print("     residual:", e)

A00, A01, A10, A11, z0, z1 = sp.symbols('A00 A01 A10 A11 z0 z1', real=True)

# mulVec / nsq_mulVec
Az0 = A00*z0 + A01*z1
Az1 = A10*z0 + A11*z1
gA = A00**2 + A10**2
gB = A00*A01 + A10*A11
gC = A01**2 + A11**2
check("nsq_mulVec", (Az0**2 + Az1**2) - (gA*z0**2 + 2*gB*z0*z1 + gC*z1**2))

# qdisc_pos: Q(-beta, alpha) = alpha*(alpha*gamma - beta^2); nsq(-beta, alpha) = alpha^2 + beta^2
al, be, ga = sp.symbols('alpha beta gamma', real=True)
Q = lambda w0, w1: al*w0**2 + 2*be*w0*w1 + ga*w1**2
check("Q(-beta,alpha) = alpha*(alpha*gamma-beta^2)", Q(-be, al) - al*(al*ga - be**2))
check("nsq(-beta,alpha) = alpha^2+beta^2", ((-be)**2 + al**2) - (al**2 + be**2))
# alpha*(alpha*gamma-beta^2) >= alpha^2+beta^2 and alpha>0 => disc>0 (logic, not identity)
# Q(1,0) = alpha
check("Q(1,0) = alpha", Q(1, 0) - al)

# orient
def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

x0, x1, y0, y1, w0, w1 = sp.symbols('x0 x1 y0 y1 w0 w1', real=True)
a, b, c, d, e, f = sp.symbols('a b c d e f', real=True)
L00, L01, L10, L11, b0, b1 = sp.symbols('L00 L01 L10 L11 b0 b1', real=True)
X = (x0, x1); Y = (y0, y1); Z = (w0, w1)

def lin2(a_, b_, c_, d_, p):
    return (a_*p[0] + b_*p[1], c_*p[0] + d_*p[1])

check("orient_lin2", orient(lin2(a,b,c,d,X), lin2(a,b,c,d,Y), lin2(a,b,c,d,Z)) - (a*d-b*c)*orient(X,Y,Z))

def aff(p):
    return (L00*p[0] + L01*p[1] + b0, L10*p[0] + L11*p[1] + b1)
detL = L00*L11 - L01*L10
check("orient_affine", orient(aff(X), aff(Y), aff(Z)) - detL*orient(X,Y,Z))

# 2x2 determinant identity used in orient_lin2 proof: (Mu)_0 (Mw)_1 - (Mu)_1 (Mw)_0 = det M (u0 w1 - u1 w0)
u0, u1 = sp.symbols('u0 u1', real=True)
check("det of images", (a*u0+b*u1)*(c*w0+d*w1) - (c*u0+d*u1)*(a*w0+b*w1) - (a*d-b*c)*(u0*w1-u1*w0))

# Cholesky factor
s, t = sp.symbols('s t', real=True, nonzero=True)
T = lambda p: lin2(s, be/s, 0, t, p)
Ti = lambda p: lin2(1/s, -be/(s**2*t), 0, 1/t, p)
TZ = T((z0, z1))
check("nsq_lin2_chol", (TZ[0]**2 + TZ[1]**2) - (s**2*z0**2 + 2*be*z0*z1 + (be**2/s**2 + t**2)*z1**2))
TiT = Ti(T((x0, x1)))
check("lin2_chol_inv_left coord 0", TiT[0] - x0)
check("lin2_chol_inv_left coord 1", TiT[1] - x1)
TTi = T(Ti((x0, x1)))
check("lin2_chol_inv_right coord 0", TTi[0] - x0)
check("lin2_chol_inv_right coord 1", TTi[1] - x1)
# det T = s*t - (beta/s)*0 = s t
check("det T", (s*t - (be/s)*0) - s*t)
# gamma identity: with s^2 = alpha, t^2 = (alpha*gamma - beta^2)/alpha: beta^2/s^2 + t^2 = gamma
alp = sp.symbols('alp', positive=True)
check("beta^2/alpha + (alpha*gamma-beta^2)/alpha = gamma", be**2/alp + (alp*ga - be**2)/alp - ga)
# explicit inverse entries of T: [[s, beta/s],[0,t]]^{-1} = [[1/s, -beta/(s^2 t)],[0, 1/t]]
Tm = sp.Matrix([[s, be/s], [0, t]])
Tim = sp.Matrix([[1/s, -be/(s**2*t)], [0, 1/t]])
check("T * Ti = I (entry sum)", sum(abs(sp.simplify(v)) for v in (Tm*Tim - sp.eye(2))))
check("Ti * T = I (entry sum)", sum(abs(sp.simplify(v)) for v in (Tim*Tm - sp.eye(2))))

# matrix_eq_one_of_fix: linear combinations
M00, M01, M10, M11 = sp.symbols('M00 M01 M10 M11', real=True)
hu0 = (M00*u0 + M01*u1) - u0   # (Mu)_0 - u_0 = 0
hu1 = (M10*u0 + M11*u1) - u1
hw0 = (M00*w0 + M01*w1) - w0
hw1 = (M10*w0 + M11*w1) - w1
delta = u0*w1 - u1*w0
check("e00", w1*hu0 - u1*hw0 - (M00 - 1)*delta)
check("e01", -w0*hu0 + u0*hw0 - M01*delta)
check("e10", w1*hu1 - u1*hw1 - M10*delta)
check("e11", -w0*hu1 + u0*hw1 - (M11 - 1)*delta)

# injective_of_affine: L v = 0 => det L * v = 0
v0, v1 = sp.symbols('v0 v1', real=True)
h0 = L00*v0 + L01*v1
h1 = L10*v0 + L11*v1
check("inj e0", L11*h0 - L01*h1 - detL*v0)
check("inj e1", L00*h1 - L10*h0 - detL*v1)

# orient(p0,p1,p2) = u0 w1 - u1 w0 with u = p1-p0, w = p2-p0
p00, p01, p10, p11, p20, p21 = sp.symbols('p00 p01 p10 p11 p20 p21', real=True)
check("orient = det(p1-p0, p2-p0)", orient((p00,p01),(p10,p11),(p20,p21)) - ((p10-p00)*(p21-p01) - (p11-p01)*(p20-p00)))

# coords form: g p = !![a,b;c,d] p + ![e,f]
P0, P1 = sp.symbols('P0 P1', real=True)
Mcd = sp.Matrix([[a, b], [c, d]])
gv = Mcd*sp.Matrix([P0, P1]) + sp.Matrix([e, f])
check("coords form coord 0", gv[0] - (a*P0 + b*P1 + e))
check("coords form coord 1", gv[1] - (c*P0 + d*P1 + f))
check("det !![a,b;c,d]", Mcd.det() - (a*d - b*c))

# affine maps preserve two-point convex combinations
lam = sp.symbols('lam', real=True)
comb = ((1-lam)*x0 + lam*y0, (1-lam)*x1 + lam*y1)
lhs = aff(comb)
rhs = tuple((1-lam)*aff(X)[i] + lam*aff(Y)[i] for i in range(2))
check("affine convex combination coord 0", lhs[0] - rhs[0])
check("affine convex combination coord 1", lhs[1] - rhs[1])

# iterate_sub_of_affine symbolically for k = 0..4 with generic L, b
Lm = sp.Matrix([[L00, L01], [L10, L11]])
bv = sp.Matrix([b0, b1])
pv = sp.Matrix([x0, x1]); qv = sp.Matrix([y0, y1])
gp, gq = pv, qv
for k in range(5):
    diff = (gp - gq) - (Lm**k)*(pv - qv)
    check(f"iterate_sub k={k}", sp.expand(diff[0])**2 + sp.expand(diff[1])**2)
    gp = Lm*gp + bv
    gq = Lm*gq + bv

# eDist2 = nsq(p - q)
check("eDist2_eq_nsq", ((x0-y0)**2 + (x1-y1)**2) - ((x0-y0)**2 + (x1-y1)**2))

# h^k = T g^k T^{-1}: check g^m = id from L^m = 1 and g^m(p0)=p0 is logic; numeric end-to-end check below.

print("ALL SYMBOLIC CHECKS PASSED" if ok else "SOME SYMBOLIC CHECK FAILED")

# ---- numeric end-to-end sanity check of the averaging construction ----
import math
random.seed(1)
def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def matvec(A, v):
    return [A[0][0]*v[0] + A[0][1]*v[1], A[1][0]*v[0] + A[1][1]*v[1]]
def inv2(A):
    dt = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    return [[A[1][1]/dt, -A[0][1]/dt], [-A[1][0]/dt, A[0][0]/dt]]
maxerr = 0.0
for trial in range(200):
    m = random.choice([2, 3, 4, 5, 6, 7, 8])
    j = random.choice([k for k in range(1, m) if math.gcd(k, m) == 1])
    refl = random.random() < 0.3
    th = 2*math.pi*j/m
    if refl:
        m = 2
        R = [[math.cos(th), math.sin(th)], [math.sin(th), -math.cos(th)]]
    else:
        R = [[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]]
    P = [[random.uniform(-2, 2) for _ in range(2)] for _ in range(2)]
    while abs(P[0][0]*P[1][1]-P[0][1]*P[1][0]) < 0.3:
        P = [[random.uniform(-2, 2) for _ in range(2)] for _ in range(2)]
    L = matmul(matmul(P, R), inv2(P))  # L^m = I
    bvec = [random.uniform(-3, 3), random.uniform(-3, 3)]
    # averaged form
    Lk = [[1.0, 0.0], [0.0, 1.0]]
    al_ = be_ = ga_ = 0.0
    for k in range(m):
        al_ += Lk[0][0]**2 + Lk[1][0]**2
        be_ += Lk[0][0]*Lk[0][1] + Lk[1][0]*Lk[1][1]
        ga_ += Lk[0][1]**2 + Lk[1][1]**2
        Lk = matmul(L, Lk)
    err_Lm = max(abs(Lk[i][jj] - (1.0 if i == jj else 0.0)) for i in range(2) for jj in range(2))
    assert err_Lm < 1e-9, err_Lm
    assert al_ >= 1 - 1e-12 and al_*ga_ - be_**2 > 0
    s_ = math.sqrt(al_); t_ = math.sqrt((al_*ga_ - be_**2)/al_)
    Tm_ = [[s_, be_/s_], [0.0, t_]]
    Ti_ = [[1/s_, -be_/(s_**2*t_)], [0.0, 1/t_]]
    def h(x):
        y = matvec(Ti_, x)
        gy = [matvec(L, y)[0] + bvec[0], matvec(L, y)[1] + bvec[1]]
        return matvec(Tm_, gy)
    for _ in range(20):
        x = [random.uniform(-5, 5), random.uniform(-5, 5)]
        y = [random.uniform(-5, 5), random.uniform(-5, 5)]
        hx, hy = h(x), h(y)
        d1 = (hx[0]-hy[0])**2 + (hx[1]-hy[1])**2
        d0 = (x[0]-y[0])**2 + (x[1]-y[1])**2
        maxerr = max(maxerr, abs(d1 - d0)/max(1.0, d0))
print("numeric isometry check: max relative error %.2e over 200 random finite-order affine maps" % maxerr)

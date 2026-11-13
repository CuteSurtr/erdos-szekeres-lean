import sympy as sp

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def pt(name):
    x, y = sp.symbols(name + '0 ' + name + '1', real=True)
    return (x, y)

a, b, c, d, v, p, q, r = (pt(n) for n in 'a b c d v p q r'.split())
results = []

def check(label, expr):
    ok = sp.simplify(sp.expand(expr)) == 0
    results.append((label, ok))

# fd:lem:orient
br = lambda x, y: x[0]*y[1] - x[1]*y[0]
check('orient = [a,b]+[b,c]+[c,a]', orient(a, b, c) - (br(a, b) + br(b, c) + br(c, a)))
check('(a) swap', orient(a, c, b) + orient(a, b, c))
check('(b) cycle', orient(b, c, a) - orient(a, b, c))
add = lambda x, y: (x[0]+y[0], x[1]+y[1])
check('(c) translate', orient(add(a, v), add(b, v), add(c, v)) - orient(a, b, c))
# (d) all six permutations
import itertools
P = [a, b, c]
for perm in itertools.permutations(range(3)):
    sgn = sp.Matrix(3, 3, lambda i, j: 1 if perm[i] == j else 0).det()
    check('(d) perm %s' % (perm,), orient(P[perm[0]], P[perm[1]], P[perm[2]]) - sgn*orient(a, b, c))
# (e) equal arguments
check('(e) a=b', orient(a, a, c)); check('(e) a=c', orient(a, b, a)); check('(e) b=c', orient(a, b, b))

# fd:lem:affine-orient
A = sp.Matrix(2, 2, sp.symbols('A00 A01 A10 A11', real=True))
vv = sp.Matrix(sp.symbols('v0 v1', real=True))
g = lambda x: tuple(A*sp.Matrix(x) + vv)
check('orient_affine', orient(g(a), g(b), g(c)) - A.det()*orient(a, b, c))

# rotations
th, al, be = sp.symbols('theta alpha beta', real=True)
R = lambda t: sp.Matrix([[sp.cos(t), -sp.sin(t)], [sp.sin(t), sp.cos(t)]])
def rot(cc, t, pp):
    return (cc[0] + sp.cos(t)*(pp[0]-cc[0]) - sp.sin(t)*(pp[1]-cc[1]),
            cc[1] + sp.sin(t)*(pp[0]-cc[0]) + sp.cos(t)*(pp[1]-cc[1]))
cm = sp.Matrix(c)
lhs = sp.Matrix(rot(c, th, p)); rhs1 = cm + R(th)*(sp.Matrix(p)-cm); rhs2 = R(th)*sp.Matrix(p) + (cm - R(th)*cm)
check('rot (b) c+R(p-c)', (lhs-rhs1).norm()**2)
check('rot (b) Rp+(c-Rc)', sum((lhs-rhs2)[i]**2 for i in range(2)))
pv = add(p, v)
check('rot (b) rho(p+v)=rho(p)+Rv', sum((sp.Matrix(rot(c, th, pv)) - sp.Matrix(rot(c, th, p)) - R(th)*sp.Matrix(v))[i]**2 for i in range(2)))
check('rot (b) rho(c)=c', sum((sp.Matrix(rot(c, th, c)) - cm)[i]**2 for i in range(2)))
# (a) complex form
z = p[0] + sp.I*p[1]; gam = c[0] + sp.I*c[1]
w = gam + (sp.cos(th) + sp.I*sp.sin(th))*(z - gam)
rp = rot(c, th, p)
check('rot (a) complex', sp.expand(rp[0] + sp.I*rp[1] - w))
# (c) composition
comp = (R(al)*R(be) - R(al+be)).applyfunc(lambda e: sp.expand(sp.expand_trig(e)))
check('rot (c) R_a R_b = R_{a+b}', sum(comp[i, j]**2 for i in range(2) for j in range(2)))
check('rot (c) R_0 = I', sum((R(0)-sp.eye(2))[i, j]**2 for i in range(2) for j in range(2)))
# (e) and (f)
check('rot (e)', sp.simplify(orient(c, p, rot(c, th, p)) - sp.sin(th)*((p[0]-c[0])**2 + (p[1]-c[1])**2)))
rp = rot(c, th, p)
check('rot (f)', sp.simplify((rp[0]-c[0])**2 + (rp[1]-c[1])**2 - ((p[0]-c[0])**2 + (p[1]-c[1])**2)))
check('det R = 1', sp.simplify(R(th).det() - 1))
# (i) rotation invariance
check('(i) orient_rotAbout_inv', sp.simplify(orient(rot(c, th, a), rot(c, th, b), rot(c, th, d)) - orient(a, b, d)))

# reflection (ii)
ph = sp.symbols('phi', real=True)
F = sp.Matrix([[sp.cos(2*ph), sp.sin(2*ph)], [sp.sin(2*ph), -sp.cos(2*ph)]])
u = sp.Matrix([sp.cos(ph), sp.sin(ph)]); up = sp.Matrix([-sp.sin(ph), sp.cos(ph)])
tr = lambda M: M.applyfunc(lambda e: sp.simplify(sp.expand_trig(e)))
check('(ii) det F = -1', sp.simplify(F.det() + 1))
check('(ii) F u = u', sum(tr(F*u - u)[i]**2 for i in range(2)))
check('(ii) F u_perp = -u_perp', sum(tr(F*up + up)[i]**2 for i in range(2)))
check('(ii) F u_perp = (sin, -cos)', sum(tr(F*up - sp.Matrix([sp.sin(ph), -sp.cos(ph)]))[i]**2 for i in range(2)))
o = pt('o'); om = sp.Matrix(o)
sig = lambda x: tuple(om + F*(sp.Matrix(x)-om))
check('(ii) orient reflection', sp.simplify(orient(sig(a), sig(b), sig(d)) + orient(a, b, d)))
check('(ii) cos2p cosp + sin2p sinp = cosp', sp.simplify(sp.expand_trig(sp.cos(2*ph)*sp.cos(ph)+sp.sin(2*ph)*sp.sin(ph)-sp.cos(ph))))
check('(ii) sin2p cosp - cos2p sinp = sinp', sp.simplify(sp.expand_trig(sp.sin(2*ph)*sp.cos(ph)-sp.cos(2*ph)*sp.sin(ph)-sp.sin(ph))))
# 2uu^T - I equals F (D3.orient_reflC comparison)
check('reflC matrix = F', sum(tr(2*u*u.T - sp.eye(2) - F)[i, j]**2 for i in range(2) for j in range(2)))
F0 = F.subs(ph, 0)
check('F_0 = diag(1,-1)', sum((F0 - sp.diag(1, -1))[i, j]**2 for i in range(2) for j in range(2)))

# collinear proof (a) step: r = w0/u0 gives r u1 = w1 when u0 w1 = u1 w0
u0, u1, w0, w1 = sp.symbols('u0 u1 w0 w1', real=True)
check('collinear r u1 = w1', sp.simplify((w0/u0)*u1 - w1).subs(w1, u1*w0/u0))

# fd:lem:affine-cp kernel vectors and adjugate
al_, be_, ga_, de_ = sp.symbols('alpha beta gamma delta', real=True)
M = sp.Matrix([[al_, be_], [ga_, de_]])
k1 = M*sp.Matrix([be_, -al_]); k2 = M.subs({al_: 0, be_: 0})*sp.Matrix([de_, -ga_])
check('kernel x=(beta,-alpha): first entry', k1[0])
check('kernel x=(beta,-alpha): second entry = -det', k1[1] + M.det())
check('kernel x=(delta,-gamma) when alpha=beta=0', k2[0]**2 + k2[1]**2)
Ls = sp.Matrix([[de_, -be_], [-ga_, al_]])
check('L# L = det L I', sum((Ls*M - M.det()*sp.eye(2))[i, j]**2 for i in range(2) for j in range(2)))
check('inverse A^{-1}', sum((M*(Ls/M.det()) - sp.eye(2))[i, j]**2 for i in range(2) for j in range(2)))
# (*) affine combination
lam, mu = sp.symbols('lambda mu', real=True)
X = sp.Matrix(a); Xp = sp.Matrix(b)
gx = lambda x: A*x + vv
check('(*) g(lx+mx\') = l g(x)+m g(x\') when l+m=1', sum(((gx(lam*X+mu*Xp) - lam*gx(X) - mu*gx(Xp)).subs(mu, 1-lam))[i]**2 for i in range(2)))

# fd:lem:halfplane (a) and the Lean certificate
uu, vvv = sp.symbols('u v', real=True)
comb = (uu*a[0] + vvv*b[0], uu*a[1] + vvv*b[1])
diff = orient(p, q, comb) - (uu*orient(p, q, a) + vvv*orient(p, q, b))
check('halfplane (a) with u+v=1', diff.subs(vvv, 1-uu))
check('halfplane certificate (p1 q0 - p0 q1)(u+v-1)', diff - (p[1]*q[0]-p[0]*q[1])*(uu+vvv-1))

# fd:lem:support-sum
pb_a = (p[0]+b[0]-a[0], p[1]+b[1]-a[1])
check('support sum', orient(p, pb_a, r) - (orient(a, p, r) + orient(p, b, r)))

# fd:lem:four-positive: the twelve values
oabc, oabd, oacd, obcd = orient(a, b, c), orient(a, b, d), orient(a, c, d), orient(b, c, d)
def qq(x, y, z):  # x + y - z
    return (x[0]+y[0]-z[0], x[1]+y[1]-z[1])
cases = [
    (a, qq(a, b, d), b, oabd), (a, qq(a, b, d), c, oacd + oabc), (a, qq(a, b, d), d, oabd),
    (b, qq(b, c, a), a, oabc), (b, qq(b, c, a), c, oabc), (b, qq(b, c, a), d, oabd + obcd),
    (c, qq(c, d, b), a, oabc + oacd), (c, qq(c, d, b), b, obcd), (c, qq(c, d, b), d, obcd),
    (d, qq(d, a, c), a, oacd), (d, qq(d, a, c), b, obcd + oabd), (d, qq(d, a, c), c, oacd),
]
for i, (pp, q_, rr, val) in enumerate(cases):
    check('four-positive case %d' % i, orient(pp, q_, rr) - val)

# separation expansion
W = sp.Matrix(sp.symbols('w0 w1', real=True)); Yq = sp.Matrix(sp.symbols('y0 y1', real=True))
t = sp.symbols('t', real=True)
n2 = lambda z: (z.T*z)[0]
check('separation expansion', n2(W - t*Yq) - (n2(W) - 2*t*(W.T*Yq)[0] + t**2*n2(Yq)))

# small (c): lambda tau(y) + (1-lambda) tau(z) = tau(x)
ty, tx, tz = sp.symbols('ty tx tz', real=True)
L_ = (tz - tx)/(tz - ty)
check('small(c) middle parameter', sp.simplify(L_*ty + (1-L_)*tz - tx))

bad = [l for l, ok in results if not ok]
print('checked', len(results), 'identities; failures:', bad)

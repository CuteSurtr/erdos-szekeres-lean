import sympy as sp

phi, th = sp.symbols('phi theta', real=True)
o0, o1, x0, x1, p0, p1, c0, c1, w0, w1 = sp.symbols('o0 o1 x0 x1 p0 p1 c0 c1 w0 w1', real=True)
a00, a01, a10, a11, v0, v1 = sp.symbols('a00 a01 a10 a11 v0 v1', real=True)
A_, B_, C_, q0, q1 = sp.symbols('A B C q0 q1', real=True)

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

ok = True
def check(name, expr):
    global ok
    r = sp.simplify(sp.expand_trig(sp.expand(expr)))
    print(name, 'OK' if r == 0 else 'FAIL: %s' % r)
    ok = ok and (r == 0)

# 1. D3.reflC c u p with u = (cos phi, sin phi) equals o + F_phi (p - o), o = c
u = (sp.cos(phi), sp.sin(phi))
d0, d1 = x0 - o0, x1 - o1
refl = (o0 + 2*(d0*u[0] + d1*u[1])*u[0] - d0, o1 + 2*(d0*u[0] + d1*u[1])*u[1] - d1)
F = sp.Matrix([[sp.cos(2*phi), sp.sin(2*phi)], [sp.sin(2*phi), -sp.cos(2*phi)]])
sig = sp.Matrix([o0, o1]) + F*sp.Matrix([d0, d1])
check('reflC_eq_sigma_0', refl[0] - sig[0])
check('reflC_eq_sigma_1', refl[1] - sig[1])
check('detF', F.det() + 1)

# 2. Review.orient_rotAbout: orient c p (rot c th p) = sin th * eDist2 p c  (fd:lem:rot(e))
rot = (c0 + sp.cos(th)*(p0-c0) - sp.sin(th)*(p1-c1), c1 + sp.sin(th)*(p0-c0) + sp.cos(th)*(p1-c1))
check('rot_e', orient((c0, c1), (p0, p1), rot) - sp.sin(th)*((p0-c0)**2 + (p1-c1)**2))
# rotAbout_center
rc = (c0 + sp.cos(th)*(c0-c0) - sp.sin(th)*(c1-c1), c1 + sp.sin(th)*(c0-c0) + sp.cos(th)*(c1-c1))
check('rot_center_0', rc[0] - c0)
check('rot_center_1', rc[1] - c1)

# 3. g(x) = A x + v satisfies g(w + p) = A w + g(p); p = 0 gives g(x) = A x + g(0)
A = sp.Matrix([[a00, a01], [a10, a11]])
g = lambda x: A*x + sp.Matrix([v0, v1])
W, P = sp.Matrix([w0, w1]), sp.Matrix([p0, p1])
diff = g(W + P) - (A*W + g(P))
check('affine_vadd_0', diff[0]); check('affine_vadd_1', diff[1])
diff0 = g(W) - (A*W + g(sp.Matrix([0, 0])))
check('affine_p0_0', diff0[0]); check('affine_p0_1', diff0[1])

# 4. exposed_not_in_hull as easy direction: l(z) = -(A z0 + B z1); l(p) - l(q) = aff(q) - aff(p)
aff = lambda z: A_*z[0] + B_*z[1] + C_
l = lambda z: -(A_*z[0] + B_*z[1])
check('exposed_l', (l((p0, p1)) - l((q0, q1))) - (aff((q0, q1)) - aff((p0, p1))))

print('ALL OK' if ok else 'SOME FAILED')

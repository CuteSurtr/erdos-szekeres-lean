"""Sympy checks of every identity used in section lg (round 1, rigor lens)."""
import sympy as sp

ok_all = True


def check(name, expr, assume_pythag=False, trig=False):
    global ok_all
    e = sp.expand(expr)
    if trig:
        e = sp.simplify(sp.expand_trig(e))
    res = sp.simplify(e) == 0
    print(f"{'OK ' if res else 'FAIL'} {name}")
    if not res:
        print("     residual:", sp.simplify(e))
        ok_all = False


# generic symbols
a0, a1, b0, b1, c0, c1, d0, d1, e0, e1, p0, p1, x0, x1, y0, y1, w0, w1 = sp.symbols(
    'a0 a1 b0 b1 c0 c1 d0 d1 e0 e1 p0 p1 x0 x1 y0 y1 w0 w1', real=True)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def det(X, Y):
    return X[0] * Y[1] - X[1] * Y[0]


def ip(X, Y):
    return X[0] * Y[0] + X[1] * Y[1]


def J(X):
    return (-X[1], X[0])


def lin(w, a, y):
    return w[0] * (y[0] - a[0]) + w[1] * (y[1] - a[1])


def sub(X, Y):
    return (X[0] - Y[0], X[1] - Y[1])


def rotAbout(c, cs, sn, p):
    # cs, sn are cos(theta), sin(theta) as free symbols or expressions
    return (c[0] + cs * (p[0] - c[0]) - sn * (p[1] - c[1]),
            c[1] + sn * (p[0] - c[0]) + cs * (p[1] - c[1]))


A = (a0, a1); B = (b0, b1); C = (c0, c1); D = (d0, d1); E = (e0, e1)
P = (p0, p1); X = (x0, x1); Y = (y0, y1); W = (w0, w1)

# ---- (lg:eq:J)
check("eq:J det(X,X)=0", det(X, X))
check("eq:J det(X,JX)=|X|^2", det(X, J(X)) - ip(X, X))
check("eq:J det(JX,X)=-|X|^2", det(J(X), X) + ip(X, X))
check("eq:J det(JX,JX)=0", det(J(X), J(X)))
check("eq:J <X,JX>=0", ip(X, J(X)))
check("det(X,Y)=<JX,Y>", det(X, Y) - ip(J(X), Y))

# ---- R_theta X = cos X + sin JX
ct, st = sp.symbols('ct st', real=True)
RX = (ct * x0 - st * x1, st * x0 + ct * x1)
check("R_theta X = cos X + sin JX (coord 0)", RX[0] - (ct * x0 + st * J(X)[0]))
check("R_theta X = cos X + sin JX (coord 1)", RX[1] - (ct * x1 + st * J(X)[1]))

# ---- rotfacts (b): R_alpha R_beta = R_{alpha+beta}
al, be, th, s, t = sp.symbols('alpha beta theta s t', real=True)
u0, u1 = sp.symbols('u0 u1', real=True)
Rb = (sp.cos(be) * u0 - sp.sin(be) * u1, sp.sin(be) * u0 + sp.cos(be) * u1)
RaRb = (sp.cos(al) * Rb[0] - sp.sin(al) * Rb[1], sp.sin(al) * Rb[0] + sp.cos(al) * Rb[1])
Rab = (sp.cos(al + be) * u0 - sp.sin(al + be) * u1, sp.sin(al + be) * u0 + sp.cos(al + be) * u1)
check("rotfacts(b) coord0", RaRb[0] - Rab[0], trig=True)
check("rotfacts(b) coord1", RaRb[1] - Rab[1], trig=True)
# rotAbout composition with full centre
r1 = rotAbout(C, sp.cos(be), sp.sin(be), P)
r2 = rotAbout(C, sp.cos(al), sp.sin(al), r1)
r3 = rotAbout(C, sp.cos(al + be), sp.sin(al + be), P)
check("rotfacts(b) rotAbout composition coord0", r2[0] - r3[0], trig=True)
check("rotfacts(b) rotAbout composition coord1", r2[1] - r3[1], trig=True)
# rotfacts (d)
Rt = (sp.cos(th) * u0 - sp.sin(th) * u1, sp.sin(th) * u0 + sp.cos(th) * u1)
check("rotfacts(d) |R u|^2 = |u|^2", ip(Rt, Rt) - (u0**2 + u1**2), trig=True)

# ---- orient_rotAbout (polynomial identity: cos/sin as free symbols)
ca, sa, cb, sb = sp.symbols('ca sa cb sb', real=True)
lhs = orient(X, rotAbout(C, ca, sa, X), rotAbout(C, cb, sb, X))
rhs = ((x0 - c0)**2 + (x1 - c1)**2) * ((ca - 1) * sb - sa * (cb - 1))
check("orient_rotAbout (polynomial, no Pythagoras)", lhs - rhs)
# also intermediate b - x = (cos a - 1) u + sin a J u
U = sub(X, C)
bx = sub(rotAbout(C, ca, sa, X), X)
check("b-x = (ca-1)u + sa Ju coord0", bx[0] - ((ca - 1) * U[0] + sa * J(U)[0]))
check("b-x = (ca-1)u + sa Ju coord1", bx[1] - ((ca - 1) * U[1] + sa * J(U)[1]))

# ---- trig_layer
lhs = (sp.cos(2 * t) - 1) * sp.sin(2 * s) - sp.sin(2 * t) * (sp.cos(2 * s) - 1)
rhs = 4 * sp.sin(t) * sp.sin(s) * sp.sin(s - t)
check("trig_layer", lhs - rhs, trig=True)
# the intermediate written step
mid = -4 * sp.sin(t)**2 * sp.sin(s) * sp.cos(s) + 4 * sp.sin(t) * sp.cos(t) * sp.sin(s)**2
check("trig_layer intermediate (double angle substitution)", lhs - mid, trig=True)
check("trig_layer intermediate factorisation",
      mid - 4 * sp.sin(t) * sp.sin(s) * (sp.sin(s) * sp.cos(t) - sp.cos(s) * sp.sin(t)))

# ---- orient_regular_nonneg remark: value = 4|x-c|^2 sin(pi/m) sin(j pi/m) sin((j-1)pi/m)
m, j = sp.symbols('m j', positive=True)
alpha = 2 * sp.pi / m
beta = j * (2 * sp.pi / m)
F = (sp.cos(alpha) - 1) * sp.sin(beta) - sp.sin(alpha) * (sp.cos(beta) - 1)
G = 4 * sp.sin(sp.pi / m) * sp.sin(j * sp.pi / m) * sp.sin((j - 1) * sp.pi / m)
check("regular: F = 4 sin(pi/m) sin(j pi/m) sin((j-1) pi/m)", F - G, trig=True)
# numeric spot check over m in 1..9 and j in 0..m (nonnegativity and zero set)
bad = []
for mm in range(1, 10):
    for jj in range(0, mm + 1):
        val = float(F.subs({m: mm, j: jj}))
        if val < -1e-12:
            bad.append((mm, jj, val))
print("OK " if not bad else "FAIL", "regular: F >= 0 for 1<=m<=9, 0<=j<=m", bad[:5])
zero_sets_ok = True
for mm in range(2, 10):
    zs = [jj for jj in range(1, mm + 1) if abs(float(F.subs({m: mm, j: jj}))) < 1e-12]
    if zs != sorted(set([1, mm])):
        zero_sets_ok = False
        print("   zero set mismatch m=", mm, zs)
print("OK " if zero_sets_ok else "FAIL", "remark: zero set is {1,m} for 2<=m<=9, 1<=j<=m")

# ---- orient_next_prev_pos: F with beta=(m-1)2pi/m equals 4 sin t sin(pi-t) sin(pi-2t), t=pi/m
tt = sp.pi / m
F2 = (sp.cos(2 * tt) - 1) * sp.sin((m - 1) * 2 * sp.pi / m) - sp.sin(2 * tt) * (sp.cos((m - 1) * 2 * sp.pi / m) - 1)
G2 = 4 * sp.sin(tt) * sp.sin(sp.pi - tt) * sp.sin(sp.pi - 2 * tt)
check("next_prev: F = 4 sin t sin(pi-t) sin(pi-2t)", F2 - G2, trig=True)
okpos = all(float(F2.subs(m, mm)) > 0 for mm in range(3, 30))
print("OK " if okpos else "FAIL", "next_prev: F > 0 for 3<=m<30")
print("info: next_prev F at m=2:", float(F2.subs(m, 2)), "(not claimed)")

# ---- lin_rotAbout (polynomial identity)
lhs = lin(sub(C, P), P, rotAbout(C, cb, sb, P))
rhs = ((p0 - c0)**2 + (p1 - c1)**2) * (1 - cb)
check("lin_rotAbout (polynomial, no Pythagoras)", lhs - rhs)

# ---- convex_orient_nonneg affine identity (u+v=1)
uu = sp.symbols('u', real=True)
vv = 1 - uu
Q1 = (sp.Symbol('q10'), sp.Symbol('q11')); Q2 = (sp.Symbol('q20'), sp.Symbol('q21'))
mix = (uu * Q1[0] + vv * Q2[0], uu * Q1[1] + vv * Q2[1])
check("O4 affinity of orient in 3rd arg", orient(A, B, mix) - (uu * orient(A, B, Q1) + vv * orient(A, B, Q2)))

# ---- convex_disk
Av = (sp.Symbol('A0'), sp.Symbol('A1')); Bv = (sp.Symbol('B0'), sp.Symbol('B1'))
uAvB = (uu * Av[0] + vv * Bv[0], uu * Av[1] + vv * Bv[1])
AmB = sub(Av, Bv)
check("convex_disk: u|A|^2+v|B|^2-|uA+vB|^2 = uv|A-B|^2",
      uu * ip(Av, Av) + vv * ip(Bv, Bv) - ip(uAvB, uAvB) - uu * vv * ip(AmB, AmB))
check("convex_disk: middle expression",
      uu * ip(Av, Av) + vv * ip(Bv, Bv) - ip(uAvB, uAvB)
      - (uu * (1 - uu) * ip(Av, Av) + vv * (1 - vv) * ip(Bv, Bv) - 2 * uu * vv * ip(Av, Bv)))
# (u y1 + v y2) - c = uA + vB
Y1 = (sp.Symbol('y10'), sp.Symbol('y11')); Y2 = (sp.Symbol('y20'), sp.Symbol('y21'))
mixy = (uu * Y1[0] + vv * Y2[0], uu * Y1[1] + vv * Y2[1])
lhsv = sub(mixy, C)
rhsv = (uu * (Y1[0] - c0) + vv * (Y2[0] - c0), uu * (Y1[1] - c1) + vv * (Y2[1] - c1))
check("convex_disk: (u y1+v y2)-c = uA+vB", lhsv[0] - rhsv[0] + lhsv[1] - rhsv[1])

# ---- centre_not_mem_of_even
q = rotAbout(C, sp.cos(sp.pi), sp.sin(sp.pi), P)
check("rotAbout(c,pi)(p) = 2c-p coord0", q[0] - (2 * c0 - p0))
check("rotAbout(c,pi)(p) = 2c-p coord1", q[1] - (2 * c1 - p1))
check("orient(p,c,2c-p)=0", orient(P, C, (2 * c0 - p0, 2 * c1 - p1)))
kk = sp.symbols('k', positive=True, integer=True)
check("2 pi k/(2k) = pi", 2 * sp.pi * kk / (2 * kk) - sp.pi)

# ---- Cramer identity
Xv = (sp.Symbol('X0'), sp.Symbol('X1')); Yv = (sp.Symbol('Y0'), sp.Symbol('Y1')); Zv = (sp.Symbol('Z0'), sp.Symbol('Z1'))
Vv = (sp.Symbol('V0'), sp.Symbol('V1'))
for k in (0, 1):
    check(f"Cramer coord {k}", det(Xv, Yv) * Zv[k] + det(Yv, Zv) * Xv[k] + det(Zv, Xv) * Yv[k])
    # the cofactor expansion as written
    M = sp.Matrix([[Xv[k], Yv[k], Zv[k]], [Xv[0], Yv[0], Zv[0]], [Xv[1], Yv[1], Zv[1]]])
    check(f"Cramer 3x3 det vanishes, k={k}", M.det())
    check(f"Cramer cofactor expansion as written, k={k}",
          M.det() - (Xv[k] * det(Yv, Zv) - Yv[k] * det(Xv, Zv) + Zv[k] * det(Xv, Yv)))
check("Cramer second identity",
      det(Xv, Yv) * ip(W, Zv) + det(Yv, Zv) * ip(W, Xv) + det(Zv, Xv) * ip(W, Yv))
check("Cramer third identity",
      det(Xv, Yv) * det(Vv, Zv) + det(Yv, Zv) * det(Vv, Xv) + det(Zv, Xv) * det(Vv, Yv))

# ---- orient_trans_halfplane key identity (lg:eq:trans)
lhs = orient(A, B, E) * lin(W, A, C)
rhs = orient(A, B, C) * lin(W, A, E) + orient(A, C, E) * lin(W, A, B)
check("orient_trans_halfplane identity (eq:trans)", lhs - rhs)
# the translation dictionary used in the proof
Bt, Ct, Et = sub(B, A), sub(C, A), sub(E, A)
check("trans: orient(a,b,c)=det(B,C)", orient(A, B, C) - det(Bt, Ct))
check("trans: orient(a,c,e)=det(C,E)", orient(A, C, E) - det(Ct, Et))
check("trans: orient(a,b,e)=det(B,E)", orient(A, B, E) - det(Bt, Et))

# ---- fan_step identity (lg:eq:fanstep)
lhs = orient(P, B, C) * orient(A, C, E)
rhs = orient(P, C, E) * orient(A, B, C) + orient(B, C, E) * orient(P, A, C)
check("fan_step identity (eq:fanstep)", lhs - rhs)
Pt, At, Bt2, Et2 = sub(P, C), sub(A, C), sub(B, C), sub(E, C)
check("fan_step: orient(p,b,c)=det(P,B)", orient(P, B, C) - det(Pt, Bt2))
check("fan_step: orient(a,b,c)=det(A,B)", orient(A, B, C) - det(At, Bt2))
check("fan_step: orient(p,a,c)=det(P,A)", orient(P, A, C) - det(Pt, At))
check("fan_step: orient(a,c,e)=det(E,A)", orient(A, C, E) - det(Et2, At))
check("fan_step: orient(p,c,e)=det(E,P)", orient(P, C, E) - det(Et2, Pt))
check("fan_step: orient(b,c,e)=det(E,B)", orient(B, C, E) - det(Et2, Bt2))
check("fan_step: third Cramer instance with (X,Y,Z,V)=(P,B,A,E)",
      det(Pt, Bt2) * det(Et2, At) + det(Bt2, At) * det(Et2, Pt) + det(At, Pt) * det(Et2, Bt2))

# ---- orient_eq_lin
wv = (-(X[1] - P[1]), X[0] - P[0])
check("orient_eq_lin", orient(P, X, Y) - lin(wv, X, Y))

# ---- lin_pos_of_peel key identity (lg:eq:key), arbitrary points p, rp (=rho p), pp (=p'), y, c
RP = (sp.Symbol('r0'), sp.Symbol('r1')); PP = (sp.Symbol('pp0'), sp.Symbol('pp1'))
w = sub(C, P)
lhs = orient(P, RP, PP) * lin(w, P, Y)
rhs = orient(PP, P, Y) * lin(w, P, RP) + orient(P, RP, Y) * lin(w, P, PP)
check("lin_pos_of_peel key identity (eq:key)", lhs - rhs)
check("key: orient(p',p,y) = det(E,C)", orient(PP, P, Y) - det(sub(Y, P), sub(PP, P)))
# also with arbitrary w (not just c-p)
lhs = orient(P, RP, PP) * lin(W, P, Y)
rhs = orient(PP, P, Y) * lin(W, P, RP) + orient(P, RP, Y) * lin(W, P, PP)
check("key identity with arbitrary w", lhs - rhs)

# ---- orient_polar
ra, rb, rd, de = sp.symbols('r_a r_b r_d delta', real=True)


def polar(c, r, th_):
    return (c[0] + r * sp.cos(th_), c[1] + r * sp.sin(th_))


lhs = orient(polar(C, ra, al), polar(C, rb, be), polar(C, rd, de))
rhs = ra * rb * sp.sin(be - al) + rb * rd * sp.sin(de - be) + rd * ra * sp.sin(al - de)
check("orient_polar", lhs - rhs, trig=True)
# intermediate det(B-A,D-A) = det(A,B)+det(B,D)+det(D,A)
check("polar: det(B-A,D-A) = det(A,B)+det(B,D)+det(D,A)",
      det(sub(B, A), sub(D, A)) - (det(A, B) + det(B, D) + det(D, A)))
check("polar: det(B-A,D-A) = det(B,D)-det(B,A)-det(A,D)+det(A,A)",
      det(sub(B, A), sub(D, A)) - (det(B, D) - det(B, A) - det(A, D) + det(A, A)))
r_, s_, ph, ps = sp.symbols('r s phi psi', real=True)
check("polar: det(r e(phi), s e(psi)) = r s sin(psi - phi)",
      det((r_ * sp.cos(ph), r_ * sp.sin(ph)), (s_ * sp.cos(ps), s_ * sp.sin(ps))) - r_ * s_ * sp.sin(ps - ph), trig=True)

# ---- rule A: sin(alpha - delta) = sin(alpha - delta + 2 pi)
check("ruleA: sin(z) = sin(z+2pi)", sp.sin(al - de) - sp.sin(al - de + 2 * sp.pi), trig=True)

# ---- sin_add_lt: sin(x+y) = sin x cos y + cos x sin y
xx, yy = sp.symbols('x y', real=True)
check("sin addition", sp.sin(xx + yy) - (sp.sin(xx) * sp.cos(yy) + sp.cos(xx) * sp.sin(yy)), trig=True)

# ---- rule B decomposition
sx, sy, sxy = sp.symbols('sx sy sxy', real=True)
lhs = ra * rb * sx + rb * rd * sy - rd * ra * sxy
rhs = ra * (rb - rd) * sx + rd * (rb - ra) * sy + ra * rd * (sx + sy - sxy)
check("ruleB decomposition", lhs - rhs)
# rule B: orient_polar with alpha-delta = -(x+y)
lhsB = (ra * rb * sp.sin(be - al) + rb * rd * sp.sin(de - be) + rd * ra * sp.sin(al - de)).subs({be: al + xx, de: al + xx + yy})
rhsB = ra * rb * sp.sin(xx) + rb * rd * sp.sin(yy) - rd * ra * sp.sin(xx + yy)
check("ruleB: orient_polar specialised", lhsB - rhsB, trig=True)

print()
print("ALL OK" if ok_all else "SOME CHECK FAILED")

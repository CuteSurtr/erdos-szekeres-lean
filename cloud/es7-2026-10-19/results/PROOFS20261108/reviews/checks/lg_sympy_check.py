"""Symbolic checks of every identity used in section lg (layer geometry)."""
import sympy as sp

c0, c1, p0, p1, x0, x1, y0, y1 = sp.symbols('c0 c1 p0 p1 x0 x1 y0 y1', real=True)
a0, a1, b0, b1, e0, e1, w0, w1, d0, d1 = sp.symbols('a0 a1 b0 b1 e0 e1 w0 w1 d0 d1', real=True)
q10, q11, q20, q21, P0, P1 = sp.symbols('q10 q11 q20 q21 P0 P1', real=True)
al, be, de, th, s, t, u, v, R = sp.symbols('alpha beta delta theta s t u v R', real=True)
ra, rb, rd = sp.symbols('r_a r_b r_d', real=True)
ca, sa, cb, sb = sp.symbols('ca sa cb sb', real=True)

ok = True
def check(name, expr):
    global ok
    z = sp.simplify(sp.expand(expr))
    res = (z == 0)
    if not res:
        ok = False
    print(f"{'OK ' if res else 'FAIL'} {name}: residual = {z}")

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def det(X, Y):
    return X[0]*Y[1] - X[1]*Y[0]

def ip(X, Y):
    return X[0]*Y[0] + X[1]*Y[1]

def rot(c, th, p):
    return (c[0] + sp.cos(th)*(p[0]-c[0]) - sp.sin(th)*(p[1]-c[1]),
            c[1] + sp.sin(th)*(p[0]-c[0]) + sp.cos(th)*(p[1]-c[1]))

def rot_cs(c, C, S, p):  # rotation with cos, sin as free symbols
    return (c[0] + C*(p[0]-c[0]) - S*(p[1]-c[1]),
            c[1] + S*(p[0]-c[0]) + C*(p[1]-c[1]))

def lin(w, a, y):
    return w[0]*(y[0]-a[0]) + w[1]*(y[1]-a[1])

def dist2(c, y):
    return (y[0]-c[0])**2 + (y[1]-c[1])**2

def polar(c, r, th):
    return (c[0] + r*sp.cos(th), c[1] + r*sp.sin(th))

c = (c0, c1); p = (p0, p1); x = (x0, x1); y = (y0, y1)
a = (a0, a1); b = (b0, b1); e = (e0, e1); w = (w0, w1); d = (d0, d1)

# --- rotAbout_iterate: rot(c,0) = id; rot(c,al) o rot(c,be) = rot(c, al+be)
r0 = rot(c, 0, p)
check("rotAbout c 0 = id (coord 0)", r0[0] - p0)
check("rotAbout c 0 = id (coord 1)", r0[1] - p1)
comp = rot(c, al, rot(c, be, p)); direct = rot(c, al + be, p)
check("composition coord 0", sp.expand_trig(comp[0] - direct[0]))
check("composition coord 1", sp.expand_trig(comp[1] - direct[1]))
# complex form: c + e^{i th}(z - c)
z = p0 + sp.I*p1; gam = c0 + sp.I*c1
cf = gam + (sp.cos(th) + sp.I*sp.sin(th))*(z - gam)
rr = rot(c, th, p)
check("complex form re", sp.re(sp.expand(cf)) - rr[0])
check("complex form im", sp.im(sp.expand(cf)) - rr[1])

# --- orient_rotAbout: pure polynomial identity with cos/sin as free symbols
lhs = orient(x, rot_cs(c, ca, sa, x), rot_cs(c, cb, sb, x))
rhs = ((x0-c0)**2 + (x1-c1)**2) * ((ca - 1)*sb - sa*(cb - 1))
check("orient_rotAbout (free cos/sin symbols)", lhs - rhs)
lhs_t = orient(x, rot(c, al, x), rot(c, be, x))
rhs_t = ((x0-c0)**2 + (x1-c1)**2) * ((sp.cos(al) - 1)*sp.sin(be) - sp.sin(al)*(sp.cos(be) - 1))
check("orient_rotAbout (trig)", lhs_t - rhs_t)
# complex-number derivation: det(z,w) = Im(conj(z) w)
U0, U1 = sp.symbols('U0 U1', real=True)
zz = (ca - 1 + sp.I*sa)*(U0 + sp.I*U1); ww = (cb - 1 + sp.I*sb)*(U0 + sp.I*U1)
zz = sp.expand(zz); ww = sp.expand(ww)
detzw = sp.re(zz)*sp.im(ww) - sp.im(zz)*sp.re(ww)
check("det((A-1)u,(B-1)u) = |u|^2((ca-1)sb - sa(cb-1))", detzw - (U0**2+U1**2)*((ca-1)*sb - sa*(cb-1)))

# --- trig_layer
tl = (sp.cos(2*t) - 1)*sp.sin(2*s) - sp.sin(2*t)*(sp.cos(2*s) - 1) - 4*sp.sin(t)*sp.sin(s)*sp.sin(s - t)
check("trig_layer", sp.expand_trig(tl))
# written derivation steps
check("cos2t-1 = -2 sin^2 t", sp.expand_trig(sp.cos(2*t) - 1 + 2*sp.sin(t)**2))
step = -4*sp.sin(t)**2*sp.sin(s)*sp.cos(s) + 4*sp.sin(t)*sp.cos(t)*sp.sin(s)**2 \
       - 4*sp.sin(t)*sp.sin(s)*(sp.sin(s)*sp.cos(t) - sp.cos(s)*sp.sin(t))
check("trig_layer factorisation step", step)
check("sin(s-t) = sin s cos t - cos s sin t", sp.expand_trig(sp.sin(s - t) - (sp.sin(s)*sp.cos(t) - sp.cos(s)*sp.sin(t))))
# j = 0 case
check("j=0 factor vanishes", (sp.cos(al) - 1)*sp.sin(0) - sp.sin(al)*(sp.cos(0) - 1))

# --- orient_regular_nonneg / orient_next_prev_pos: angle bookkeeping
m, j, k = sp.symbols('m j k', positive=True)
tt = sp.pi/m
check("2*pi/m = 2t", 2*sp.pi/m - 2*tt)
check("j*(2*pi/m) = 2*(j*t)", j*(2*sp.pi/m) - 2*(j*tt))
check("(m-1)*(2*pi/m) = 2*((m-1)*t)", (m - 1)*(2*sp.pi/m) - 2*((m - 1)*tt))
check("(m-1)t - t = (m-2)t", (m-1)*tt - tt - (m-2)*tt)
check("(m-1)t = pi - t", (m-1)*tt - (sp.pi - tt))
check("(m-2)t = pi - 2t", (m-2)*tt - (sp.pi - 2*tt))
check("j t - t = (j-1) t", j*tt - tt - (j-1)*tt)

# --- convex_orient_nonneg: affine in q with u+v=1
q1 = (q10, q11); q2 = (q20, q21)
mix = (u*q10 + (1-u)*q20, u*q11 + (1-u)*q21)
check("orient affine in last argument", orient(a, b, mix) - (u*orient(a, b, q1) + (1-u)*orient(a, b, q2)))

# --- centre_not_mem_of_even
rpi = rot(c, sp.pi, p)
check("rotAbout c pi p = 2c - p (coord 0)", rpi[0] - (2*c0 - p0))
check("rotAbout c pi p = 2c - p (coord 1)", rpi[1] - (2*c1 - p1))
check("orient(p, c, 2c-p) = 0", orient(p, c, (2*c0 - p0, 2*c1 - p1)))
check("k*(2pi/(k+k)) = pi", k*(2*sp.pi/(k + k)) - sp.pi)

# --- dist2 rotation invariance and convex_disk
check("dist2(c, rot x) = dist2(c, x)", sp.trigsimp(sp.expand(dist2(c, rot(c, th, x)) - dist2(c, x))))
A = (q10 - c0, q11 - c1); B = (q20 - c0, q21 - c1)
mixd = (u*q10 + (1-u)*q20, u*q11 + (1-u)*q21)
check("convex_disk: u|A|^2+v|B|^2-|mix-c|^2 = uv|A-B|^2 (v=1-u)",
      u*ip(A, A) + (1-u)*ip(B, B) - dist2(c, mixd) - u*(1-u)*ip((A[0]-B[0], A[1]-B[1]), (A[0]-B[0], A[1]-B[1])))

# --- vector identity det(X,Y)Z + det(Y,Z)X + det(Z,X)Y = 0
X = (a0, a1); Y = (b0, b1); Z = (e0, e1)
for i in range(2):
    check(f"vector identity coord {i}", det(X, Y)*Z[i] + det(Y, Z)*X[i] + det(Z, X)*Y[i])

# --- orient = det(b-a, c-a)
check("orient(a,b,c) = det(b-a,c-a)", orient(a, b, d) - det((b0-a0, b1-a1), (d0-a0, d1-a1)))

# --- orient_trans_halfplane identity (c renamed d here: generic point)
cc = d
key1 = orient(a, b, e)*lin(w, a, cc) - (orient(a, b, cc)*lin(w, a, e) + orient(a, cc, e)*lin(w, a, b))
check("orient_trans_halfplane identity", key1)

# --- fan_step identity
pp = (P0, P1)
key2 = orient(pp, b, cc)*orient(a, cc, e) - (orient(pp, cc, e)*orient(a, b, cc) + orient(b, cc, e)*orient(pp, a, cc))
check("fan_step identity", key2)
# translation to c as origin: orient(p,b,c) = det(P,B) etc.
Pv = (P0-d0, P1-d1); Av = (a0-d0, a1-d1); Bv = (b0-d0, b1-d1); Ev = (e0-d0, e1-d1)
check("orient(p,b,c)=det(P,B)", orient(pp, b, cc) - det(Pv, Bv))
check("orient(a,c,e)=det(E,A)", orient(a, cc, e) - det(Ev, Av))
check("orient(p,c,e)=det(E,P)", orient(pp, cc, e) - det(Ev, Pv))
check("orient(a,b,c)=det(A,B)", orient(a, b, cc) - det(Av, Bv))
check("orient(b,c,e)=det(E,B)", orient(b, cc, e) - det(Ev, Bv))
check("orient(p,a,c)=det(P,A)", orient(pp, a, cc) - det(Pv, Av))
check("Pluecker: det(P,B)det(E,A) = det(E,P)det(A,B) + det(E,B)det(P,A)",
      det(Pv, Bv)*det(Ev, Av) - (det(Ev, Pv)*det(Av, Bv) + det(Ev, Bv)*det(Pv, Av)))
# derivation: det(E, det(P,B)A + det(B,A)P + det(A,P)B) = 0
vec = tuple(det(Pv, Bv)*Av[i] + det(Bv, Av)*Pv[i] + det(Av, Pv)*Bv[i] for i in range(2))
check("vector identity instance (P,B,A)", vec[0]); check("vector identity instance (P,B,A) coord1", vec[1])

# --- orient_eq_lin
check("orient_eq_lin", orient(pp, x, y) - lin((-(x1 - P1), x0 - P0), x, y))

# --- degenerate orientations
check("orient(a,a,c)=0", orient(a, a, d))
check("orient(a,b,a)=0", orient(a, b, a))
check("orient(a,b,b)=0", orient(a, b, b))
check("orient cycle orient(b,c,a)=orient(a,b,c)", orient(b, d, a) - orient(a, b, d))

# --- lin_rotAbout
wcp = (c0 - p0, c1 - p1)
check("lin_rotAbout", lin(wcp, p, rot(c, be, p)) - ((p0-c0)**2 + (p1-c1)**2)*(1 - sp.cos(be)))
check("<u, R u> = cos |u|^2", ip((U0, U1), (sp.cos(be)*U0 - sp.sin(be)*U1, sp.sin(be)*U0 + sp.cos(be)*U1)) - sp.cos(be)*(U0**2 + U1**2))
check("lin(w,a,y) = <w, y-a>", lin(w, a, y) - ip(w, (y0-a0, y1-a1)))
check("lin(w,a,a) = 0", lin(w, a, a))

# --- key identity in lin_pos_of_peel: generic points p, rp (=rho p), pp' (=p'), y and centre c
rp = (b0, b1); ppr = (e0, e1)
key3 = orient(p, rp, ppr)*lin(wcp, p, y) - (orient(ppr, p, y)*lin(wcp, p, rp) + orient(p, rp, y)*lin(wcp, p, ppr))
check("lin_pos_of_peel key identity", key3)
check("orient(p',p,y) = orient(p,y,p')", orient(ppr, p, y) - orient(p, y, ppr))
# rho^m = id: m * (2 pi / m) = 2 pi and rot by 2 pi is identity
check("m*(2pi/m) = 2pi", m*(2*sp.pi/m) - 2*sp.pi)
r2 = rot(c, 2*sp.pi, p)
check("rot 2pi = id coord0", r2[0] - p0); check("rot 2pi = id coord1", r2[1] - p1)

# --- orient_polar
P_a = polar(c, ra, al); P_b = polar(c, rb, be); P_d = polar(c, rd, de)
op = orient(P_a, P_b, P_d) - (ra*rb*sp.sin(be - al) + rb*rd*sp.sin(de - be) + rd*ra*sp.sin(al - de))
check("orient_polar", sp.expand_trig(op))
# det(r e(al), s e(be)) = r s sin(be-al)
check("det(r e(a), s e(b)) = r s sin(b-a)",
      sp.expand_trig(det((ra*sp.cos(al), ra*sp.sin(al)), (rb*sp.cos(be), rb*sp.sin(be))) - ra*rb*sp.sin(be - al)))
# orient(a,b,d) = det(a,b)+det(b,d)+det(d,a) for vectors relative to the origin
check("orient = det(a,b)+det(b,d)+det(d,a)", orient(a, b, d) - (det(a, b) + det(b, d) + det(d, a)))

# --- rule A: sin(al - de) = sin(al - de + 2 pi)
check("sin periodic", sp.expand_trig(sp.sin(al - de + 2*sp.pi) - sp.sin(al - de)))

# --- sin_add_lt: expansion; alternative product identity
xx, yy = sp.symbols('x y', real=True)
check("sin(x+y) expansion", sp.expand_trig(sp.sin(xx + yy) - (sp.sin(xx)*sp.cos(yy) + sp.cos(xx)*sp.sin(yy))))
check("sin x + sin y - sin(x+y) = sin x (1-cos y) + sin y (1-cos x)",
      sp.expand_trig(sp.sin(xx) + sp.sin(yy) - sp.sin(xx + yy) - (sp.sin(xx)*(1 - sp.cos(yy)) + sp.sin(yy)*(1 - sp.cos(xx)))))

# --- rule B decomposition: with x = be-al, y = de-be
xb = be - al; yb = de - be
orient_B = ra*rb*sp.sin(xb) + rb*rd*sp.sin(yb) + rd*ra*sp.sin(al - de)
check("al - de = -(x+y)", (al - de) + (xb + yb))
decomp = ra*(rb - rd)*sp.sin(xb) + rd*(rb - ra)*sp.sin(yb) + ra*rd*(sp.sin(xb) + sp.sin(yb) - sp.sin(xb + yb))
check("rule B decomposition", sp.expand_trig(orient_B - decomp))

print("ALL OK" if ok else "SOME CHECK FAILED")

# --- extra checks for statements in the text
ok2 = True
def check2(name, expr):
    global ok2
    z = sp.simplify(sp.expand(expr)); r = (z == 0)
    ok2 = ok2 and r
    print(f"{'OK ' if r else 'FAIL'} {name}: residual = {z}")
Xv = (a0, a1); Yv = (b0, b1)
JX = (-a1, a0)
check2("det(X,Y) = <JX,Y>", det(Xv, Yv) - ip(JX, Yv))
check2("det(X,JX) = |X|^2", det(Xv, JX) - ip(Xv, Xv))
check2("det(JX,X) = -|X|^2", det(JX, Xv) + ip(Xv, Xv))
check2("det(JX,JX) = 0", det(JX, JX))
check2("<X,JX> = 0", ip(Xv, JX))
check2("R_theta X = cos X + sin JX (0)", (sp.cos(th)*a0 - sp.sin(th)*a1) - (sp.cos(th)*a0 + sp.sin(th)*JX[0]))
check2("R_theta X = cos X + sin JX (1)", (sp.sin(th)*a0 + sp.cos(th)*a1) - (sp.cos(th)*a1 + sp.sin(th)*JX[1]))
# matrix product R_a R_b = R_{a+b}
Ra = sp.Matrix([[sp.cos(al), -sp.sin(al)], [sp.sin(al), sp.cos(al)]])
Rb = sp.Matrix([[sp.cos(be), -sp.sin(be)], [sp.sin(be), sp.cos(be)]])
Rab = sp.Matrix([[sp.cos(al+be), -sp.sin(al+be)], [sp.sin(al+be), sp.cos(al+be)]])
D = (Ra*Rb - Rab).applyfunc(lambda z: sp.expand_trig(z))
check2("R_a R_b = R_{a+b}", sum(abs(sp.simplify(z)) for z in D))
# orient_eq_lin derivation: det(x-p, y-p) = det(x-p, y-x)
check2("det(x-p,y-p) = det(x-p,y-x)", det((x0-P0, x1-P1), (y0-P0, y1-P1)) - det((x0-P0, x1-P1), (y0-x0, y1-x1)))
# centre: q - p = 2c - 2p; orient(p,c,q) = det(c-p, 2c-2p)
qq = (2*c0 - p0, 2*c1 - p1)
check2("orient(p,c,q) = det(c-p, q-p)", orient(p, c, qq) - det((c0-p0, c1-p1), (qq[0]-p0, qq[1]-p1)))
# m = 2 remark: orient(x, z, (1-l)x + l z) = 0
lam = sp.symbols('lam', real=True)
zz2 = (e0, e1)
check2("orient(x,z,(1-l)x+l z) = 0", orient(x, zz2, ((1-lam)*x0 + lam*e0, (1-lam)*x1 + lam*e1)))
# trans identity via Cramer: det(B,C)<w,E> + det(C,E)<w,B> + det(E,B)<w,C> = 0
Bv2 = (b0-a0, b1-a1); Cv2 = (d0-a0, d1-a1); Ev2 = (e0-a0, e1-a1)
check2("Cramer second form instance", det(Bv2, Cv2)*ip(w, Ev2) + det(Cv2, Ev2)*ip(w, Bv2) + det(Ev2, Bv2)*ip(w, Cv2))
# generic Cramer forms with V
V = (q10, q11)
check2("Cramer third form generic", det(Xv, Yv)*det(V, (e0, e1)) + det(Yv, (e0, e1))*det(V, Xv) + det((e0, e1), Xv)*det(V, Yv))
# rule B: x<pi and y<pi from x,y>0 and x+y<pi is linear; sin(-(x+y)) = -sin(x+y)
check2("sin odd", sp.sin(-(xx+yy)) + sp.sin(xx+yy))
print("EXTRA ALL OK" if ok2 else "EXTRA SOME CHECK FAILED")

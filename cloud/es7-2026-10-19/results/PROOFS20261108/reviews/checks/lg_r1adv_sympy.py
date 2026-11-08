# Independent sympy checks for section lg (adversarial verifier, round 1).
import sympy as sp

ok_all = True
def check(name, expr):
    global ok_all
    e = sp.simplify(sp.expand(expr))
    if e != 0:
        e2 = sp.simplify(sp.expand_trig(sp.expand(expr)))
        if e2 != 0:
            e3 = sp.simplify(sp.trigsimp(sp.expand(sp.expand_trig(expr))))
            ok = (e3 == 0)
        else:
            ok = True
    else:
        ok = True
    print(("OK  " if ok else "FAIL"), name)
    if not ok:
        ok_all = False

def orient(a, b, d):
    return (b[0]-a[0])*(d[1]-a[1]) - (b[1]-a[1])*(d[0]-a[0])

def lin(w, a, y):
    return w[0]*(y[0]-a[0]) + w[1]*(y[1]-a[1])

def det(X, Y):
    return X[0]*Y[1] - X[1]*Y[0]

def ip(X, Y):
    return X[0]*Y[0] + X[1]*Y[1]

def J(X):
    return (-X[1], X[0])

def vsub(X, Y):
    return (X[0]-Y[0], X[1]-Y[1])

def P(name):
    return sp.symbols(name + '0 ' + name + '1', real=True)

c = P('c'); x = P('x'); p = P('p'); y = P('y'); a = P('a'); b = P('b'); e = P('e'); w = P('w'); d = P('d')
A_, B_, C_, D_, E_, V_, X_, Y_, Z_ = (P(n) for n in ['A', 'B', 'C', 'D', 'E', 'V', 'X', 'Y', 'Z'])
al, be, th, s, t, de = sp.symbols('alpha beta theta s t delta', real=True)

def rot(cc, theta, pp):  # rotAbout, LayerLemma.lean:298
    return (cc[0] + sp.cos(theta)*(pp[0]-cc[0]) - sp.sin(theta)*(pp[1]-cc[1]),
            cc[1] + sp.sin(theta)*(pp[0]-cc[0]) + sp.cos(theta)*(pp[1]-cc[1]))

# rotfacts (a),(c),(d) and (b)
r0 = rot(c, 0, p); check('rotfacts(a) coord0', r0[0]-p[0]); check('rotfacts(a) coord1', r0[1]-p[1])
r2 = rot(c, 2*sp.pi, p); check('rotfacts(c) coord0', r2[0]-p[0]); check('rotfacts(c) coord1', r2[1]-p[1])
rc = rot(c, al, rot(c, be, p)); rs = rot(c, al+be, p)
check('rotfacts(b) coord0', sp.expand_trig(rs[0]) - rc[0]); check('rotfacts(b) coord1', sp.expand_trig(rs[1]) - rc[1])
rd = rot(c, th, p)
check('rotfacts(d)', (rd[0]-c[0])**2 + (rd[1]-c[1])**2 - ((p[0]-c[0])**2 + (p[1]-c[1])**2))

# R_theta X = cos X + sin JX ; J identities (lg:eq:J)
check('R_theta = cos X + sin JX (0)', (sp.cos(th)*X_[0]-sp.sin(th)*X_[1]) - (sp.cos(th)*X_[0] + sp.sin(th)*J(X_)[0]))
check('R_theta = cos X + sin JX (1)', (sp.sin(th)*X_[0]+sp.cos(th)*X_[1]) - (sp.cos(th)*X_[1] + sp.sin(th)*J(X_)[1]))
check('det(X,Y)=<JX,Y>', det(X_, Y_) - ip(J(X_), Y_))
check('det(X,JX)=|X|^2', det(X_, J(X_)) - ip(X_, X_))
check('det(JX,X)=-|X|^2', det(J(X_), X_) + ip(X_, X_))
check('det(JX,JX)=0', det(J(X_), J(X_)))
check('<X,JX>=0', ip(X_, J(X_)))

# orient_rotAbout (LayerLemma.lean:472) -- as polynomial identity in independent ca,sa,cb,sb
ca, sa, cb, sb = sp.symbols('ca sa cb sb', real=True)
def rotp(cc, cs, sn, pp):
    return (cc[0] + cs*(pp[0]-cc[0]) - sn*(pp[1]-cc[1]), cc[1] + sn*(pp[0]-cc[0]) + cs*(pp[1]-cc[1]))
lhs = orient(x, rotp(c, ca, sa, x), rotp(c, cb, sb, x))
rhs = ((x[0]-c[0])**2 + (x[1]-c[1])**2) * ((ca-1)*sb - sa*(cb-1))
check('orient_rotAbout (polynomial, no Pythagoras)', lhs - rhs)

# trig_layer (LayerLemma.lean:480)
check('trig_layer', (sp.cos(2*t)-1)*sp.sin(2*s) - sp.sin(2*t)*(sp.cos(2*s)-1) - 4*sp.sin(t)*sp.sin(s)*sp.sin(s-t))
# written proof's intermediate step
check('trig_layer intermediate', -4*sp.sin(t)**2*sp.sin(s)*sp.cos(s) + 4*sp.sin(t)*sp.cos(t)*sp.sin(s)**2
      - 4*sp.sin(t)*sp.sin(s)*(sp.sin(s)*sp.cos(t) - sp.cos(s)*sp.sin(t)))

# orient_regular_nonneg remark: orient(x, rho x, rho^j x) = 4|x-c|^2 sin(pi/m) sin(j pi/m) sin((j-1) pi/m)
m_, j_ = sp.symbols('m j', positive=True)
alpha = 2*sp.pi/m_; beta = j_*alpha
F = (sp.cos(alpha)-1)*sp.sin(beta) - sp.sin(alpha)*(sp.cos(beta)-1)
check('regular remark formula F = 4 sin t sin jt sin (j-1)t', F - 4*sp.sin(sp.pi/m_)*sp.sin(j_*sp.pi/m_)*sp.sin((j_-1)*sp.pi/m_))
# orient_next_prev: s=(m-1)t, t = pi/m, so (m-1)t = pi - t and (m-1)t - t = pi - 2t
tt = sp.pi/m_
check('next-prev: (m-1)t = pi - t', (m_-1)*tt - (sp.pi - tt))
check('next-prev: (m-1)t - t = pi - 2t', (m_-1)*tt - tt - (sp.pi - 2*tt))
check('next-prev: beta=(m-1)(2pi/m)=2((m-1)t)', (m_-1)*(2*sp.pi/m_) - 2*((m_-1)*tt))

# lin_rotAbout (LayerLemma.lean:794) -- polynomial in cb, sb
cp = (c[0]-p[0], c[1]-p[1])
check('lin_rotAbout (polynomial)', lin(cp, p, rotp(c, cb, sb, p)) - ((p[0]-c[0])**2 + (p[1]-c[1])**2)*(1-cb))

# convex_orient_nonneg affinity (O4)
u, v = sp.symbols('u v', real=True)
q1 = P('q1_'); q2 = P('q2_')
mix = (u*q1[0] + v*q2[0], u*q1[1] + v*q2[1])
check('(O4) affinity with u+v=1', (orient(a, b, mix) - u*orient(a, b, q1) - v*orient(a, b, q2)).subs(v, 1-u))

# convex_disk identity
Avec = (y[0]-c[0], y[1]-c[1]); Bvec = (d[0]-c[0], d[1]-c[1])
uAvB = (u*Avec[0] + v*Bvec[0], u*Avec[1] + v*Bvec[1])
expr = (u*ip(Avec, Avec) + v*ip(Bvec, Bvec) - ip(uAvB, uAvB)) - u*v*ip(vsub(Avec, Bvec), vsub(Avec, Bvec))
check('convex_disk identity (u+v=1)', expr.subs(v, 1-u))
mixpt = (u*y[0] + v*d[0], u*y[1] + v*d[1])
check('convex_disk: (u y1 + v y2) - c = uA + vB (u+v=1)', (mixpt[0]-c[0] - uAvB[0]).subs(v, 1-u))

# Cramer identities (lg:lem:cramer)
for k in (0, 1):
    check('Cramer vector identity coord %d' % k, det(X_, Y_)*Z_[k] + det(Y_, Z_)*X_[k] + det(Z_, X_)*Y_[k])
check('Cramer <w,.> form', det(X_, Y_)*ip(w, Z_) + det(Y_, Z_)*ip(w, X_) + det(Z_, X_)*ip(w, Y_))
check('Cramer det(V,.) form', det(X_, Y_)*det(V_, Z_) + det(Y_, Z_)*det(V_, X_) + det(Z_, X_)*det(V_, Y_))
# 3x3 determinant expansion claim
M = sp.Matrix([[X_[0], Y_[0], Z_[0]], [X_[0], Y_[0], Z_[0]], [X_[1], Y_[1], Z_[1]]])
check('3x3 expansion (k=0)', M.det())
expansion = X_[0]*det(Y_, Z_) - Y_[0]*det(X_, Z_) + Z_[0]*det(X_, Y_)
check('3x3 expansion equals stated form (k=0)', expansion)

# orient_trans_halfplane key identity (LayerLemma.lean:632)
cc_ = P('cc')  # generic point named c in Lean
key1 = orient(a, b, e)*lin(w, a, cc_) - (orient(a, b, cc_)*lin(w, a, e) + orient(a, cc_, e)*lin(w, a, b))
check('orient_trans_halfplane key identity', key1)

# fan_step key identity (LayerLemma.lean:644)
key2 = orient(p, b, cc_)*orient(a, cc_, e) - (orient(p, cc_, e)*orient(a, b, cc_) + orient(b, cc_, e)*orient(p, a, cc_))
check('fan_step key identity', key2)
# the det rewrites used in the fan_step proof
Pv = vsub(p, cc_); Av = vsub(a, cc_); Bv = vsub(b, cc_); Ev = vsub(e, cc_)
check('fan_step: orient(p,b,c)=det(P,B)', orient(p, b, cc_) - det(Pv, Bv))
check('fan_step: orient(a,b,c)=det(A,B)', orient(a, b, cc_) - det(Av, Bv))
check('fan_step: orient(p,a,c)=det(P,A)', orient(p, a, cc_) - det(Pv, Av))
check('fan_step: orient(a,c,e)=det(E,A)', orient(a, cc_, e) - det(Ev, Av))
check('fan_step: orient(p,c,e)=det(E,P)', orient(p, cc_, e) - det(Ev, Pv))
check('fan_step: orient(b,c,e)=det(E,B)', orient(b, cc_, e) - det(Ev, Bv))
check('fan_step: displayed Cramer instance', det(Pv, Bv)*det(Ev, Av) + det(Bv, Av)*det(Ev, Pv) + det(Av, Pv)*det(Ev, Bv))

# orient_eq_lin (LayerLemma.lean:653)
check('orient_eq_lin', orient(p, x, y) - lin((-(x[1]-p[1]), x[0]-p[0]), x, y))

# lin_pos_of_peel key identity (LayerLemma.lean:901), arbitrary points p, rp, pp, y, c
rp = P('rp'); pp = P('pp')
key3 = orient(p, rp, pp)*lin(cp, p, y) - (orient(pp, p, y)*lin(cp, p, rp) + orient(p, rp, y)*lin(cp, p, pp))
check('lin_pos_of_peel key identity (arbitrary points)', key3)
Bv2 = vsub(rp, p); Cv2 = vsub(pp, p); Ev2 = vsub(y, p)
check('halfplane: orient(p,rp,pp)=det(B,C)', orient(p, rp, pp) - det(Bv2, Cv2))
check('halfplane: orient(p,rp,y)=det(B,E)', orient(p, rp, y) - det(Bv2, Ev2))
check('halfplane: orient(pp,p,y)=det(E,C)', orient(pp, p, y) - det(Ev2, Cv2))

# centre_not_mem_of_even: rot by pi gives 2c - p, orient(p,c,2c-p)=0
rpi = rot(c, sp.pi, p)
check('rot pi coord0 = 2c0 - p0', rpi[0] - (2*c[0]-p[0])); check('rot pi coord1 = 2c1 - p1', rpi[1] - (2*c[1]-p[1]))
check('orient(p,c,2c-p)=0', orient(p, c, (2*c[0]-p[0], 2*c[1]-p[1])))
kk = sp.symbols('k', positive=True)
check('k*(2pi/(2k)) = pi', kk*(2*sp.pi/(2*kk)) - sp.pi)

# orient_polar (LayerLemma.lean:935)
ra, rb, rd = sp.symbols('r_a r_b r_d', real=True)
def polar(cc, r, theta):
    return (cc[0] + r*sp.cos(theta), cc[1] + r*sp.sin(theta))
lhsP = orient(polar(c, ra, al), polar(c, rb, be), polar(c, rd, de))
rhsP = ra*rb*sp.sin(be-al) + rb*rd*sp.sin(de-be) + rd*ra*sp.sin(al-de)
check('orient_polar', sp.expand_trig(lhsP - rhsP))
# intermediate: det(B-A, D-A) = det(A,B)+det(B,D)+det(D,A)
check('det(B-A,D-A)=det(A,B)+det(B,D)+det(D,A)', det(vsub(B_, A_), vsub(D_, A_)) - (det(A_, B_) + det(B_, D_) + det(D_, A_)))
r_, s_, ph, ps = sp.symbols('r s phi psi', real=True)
check('det(r e(phi), s e(psi)) = rs sin(psi-phi)', sp.expand_trig(det((r_*sp.cos(ph), r_*sp.sin(ph)), (s_*sp.cos(ps), s_*sp.sin(ps))) - r_*s_*sp.sin(ps-ph)))

# rule A: sin(alpha-delta) = sin(alpha-delta+2pi)
check('sin(z+2pi)=sin z', sp.sin(al-de+2*sp.pi) - sp.sin(al-de))

# rule B decomposition
xx, yy = sp.symbols('x y', real=True)
orientB = ra*rb*sp.sin(xx) + rb*rd*sp.sin(yy) - rd*ra*sp.sin(xx+yy)
decomp = ra*(rb-rd)*sp.sin(xx) + rd*(rb-ra)*sp.sin(yy) + ra*rd*(sp.sin(xx)+sp.sin(yy)-sp.sin(xx+yy))
check('rule B decomposition', orientB - decomp)
# orient_polar specialised: alpha-delta = -(x+y)
check('rule B: orient_polar specialisation', (rhsP.subs({be: al+xx, de: al+xx+yy})) - orientB)

# sin_add_lt expansion
check('sin(x+y) = sin x cos y + cos x sin y', sp.expand_trig(sp.sin(xx+yy)) - (sp.sin(xx)*sp.cos(yy)+sp.cos(xx)*sp.sin(yy)))

print('ALL OK' if ok_all else 'SOME FAILED')

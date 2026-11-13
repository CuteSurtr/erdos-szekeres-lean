import sympy as sp

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def det(X, Y):
    return X[0]*Y[1] - X[1]*Y[0]

def ip(X, Y):
    return X[0]*Y[0] + X[1]*Y[1]

def lin(w, a, y):
    return w[0]*(y[0]-a[0]) + w[1]*(y[1]-a[1])

def J(X):
    return (-X[1], X[0])

def sub(X, Y):
    return (X[0]-Y[0], X[1]-Y[1])

def add(X, Y):
    return (X[0]+Y[0], X[1]+Y[1])

def smul(s, X):
    return (s*X[0], s*X[1])

def rotAbout(c, th, p):
    return (c[0] + sp.cos(th)*(p[0]-c[0]) - sp.sin(th)*(p[1]-c[1]),
            c[1] + sp.sin(th)*(p[0]-c[0]) + sp.cos(th)*(p[1]-c[1]))

def polar(c, r, th):
    return (c[0] + r*sp.cos(th), c[1] + r*sp.sin(th))

def pt(name):
    return sp.symbols(f'{name}0 {name}1', real=True)

results = []
def check(name, expr):
    e = sp.simplify(sp.expand_trig(sp.expand(expr)))
    ok = (e == 0)
    if not ok:
        e2 = sp.simplify(sp.trigsimp(sp.expand(sp.expand_trig(expr))))
        ok = (e2 == 0)
        e = e2
    results.append((name, ok, e))

al, be, th, de, s, t = sp.symbols('alpha beta theta delta s t', real=True)
c, x, p, a, b, e, w, y, q, V = pt('c'), pt('x'), pt('p'), pt('a'), pt('b'), pt('e'), pt('w'), pt('y'), pt('q'), pt('V')
X, Y, Z = pt('X'), pt('Y'), pt('Z')

# eq (lg:eq:J)
check('J: det(X,JX)=|X|^2', det(X, J(X)) - ip(X, X))
check('J: det(JX,X)=-|X|^2', det(J(X), X) + ip(X, X))
check('J: det(JX,JX)=0', det(J(X), J(X)))
check('J: <X,JX>=0', ip(X, J(X)))
check('J: det(X,Y)=<JX,Y>', det(X, Y) - ip(J(X), Y))
# R_theta X = cos X + sin JX
RX = (sp.cos(th)*X[0]-sp.sin(th)*X[1], sp.sin(th)*X[0]+sp.cos(th)*X[1])
check('R X = cos X + sin JX (0)', RX[0] - (sp.cos(th)*X[0] + sp.sin(th)*J(X)[0]))
check('R X = cos X + sin JX (1)', RX[1] - (sp.cos(th)*X[1] + sp.sin(th)*J(X)[1]))
# O1
check('O1', orient(a, b, e) - det(sub(b, a), sub(e, a)))
# O2
check('O2', orient(a, b, x) - det(sub(a, x), sub(b, x)))
# O4 affine
u_, v_ = sp.symbols('u v', real=True)
q1, q2 = pt('q1'), pt('q2')
check('O4', (orient(a, b, add(smul(u_, q1), smul(v_, q2))) - u_*orient(a, b, q1) - v_*orient(a, b, q2)).subs(v_, 1-u_))
# rotfacts (b) composition
comp = rotAbout(c, al, rotAbout(c, be, p))
tgt = rotAbout(c, al+be, p)
check('rotfacts(b) 0', comp[0]-tgt[0])
check('rotfacts(b) 1', comp[1]-tgt[1])
# rotfacts (d)
r = rotAbout(c, th, p)
check('rotfacts(d)', ip(sub(r, c), sub(r, c)) - ip(sub(p, c), sub(p, c)))
# rotfacts (a),(c)
for ang, nm in [(0, '(a)'), (2*sp.pi, '(c)')]:
    rr = rotAbout(c, ang, p)
    check('rotfacts'+nm+' 0', rr[0]-p[0]); check('rotfacts'+nm+' 1', rr[1]-p[1])
# orient_rotAbout
lhs = orient(x, rotAbout(c, al, x), rotAbout(c, be, x))
rhs = ((x[0]-c[0])**2 + (x[1]-c[1])**2)*((sp.cos(al)-1)*sp.sin(be) - sp.sin(al)*(sp.cos(be)-1))
check('orient_rotAbout (polynomial, no trig relation)', sp.expand(lhs - rhs))
# trig_layer
check('trig_layer', (sp.cos(2*t)-1)*sp.sin(2*s) - sp.sin(2*t)*(sp.cos(2*s)-1) - 4*sp.sin(t)*sp.sin(s)*sp.sin(s-t))
# lin_rotAbout
check('lin_rotAbout', lin(sub(c, p), p, rotAbout(c, be, p)) - ((p[0]-c[0])**2 + (p[1]-c[1])**2)*(1-sp.cos(be)))
# Cramer identities
cr = add(add(smul(det(X, Y), Z), smul(det(Y, Z), X)), smul(det(Z, X), Y))
check('Cramer 0', cr[0]); check('Cramer 1', cr[1])
check('Cramer ip', det(X, Y)*ip(w, Z) + det(Y, Z)*ip(w, X) + det(Z, X)*ip(w, Y))
check('Cramer det', det(X, Y)*det(V, Z) + det(Y, Z)*det(V, X) + det(Z, X)*det(V, Y))
# Cramer proof: 3x3 expansion
for k in (0, 1):
    M = sp.Matrix([[X[k], Y[k], Z[k]], [X[0], Y[0], Z[0]], [X[1], Y[1], Z[1]]])
    check(f'Cramer expansion k={k}', M.det())
    check(f'Cramer expansion formula k={k}', X[k]*det(Y, Z) - Y[k]*det(X, Z) + Z[k]*det(X, Y))
# orient_trans_halfplane key (c here is arbitrary point 'q')
cc = q
check('trans key', orient(a, b, e)*lin(w, a, cc) - (orient(a, b, cc)*lin(w, a, e) + orient(a, cc, e)*lin(w, a, b)))
# fan_step key
check('fan_step key', orient(p, b, cc)*orient(a, cc, e) - (orient(p, cc, e)*orient(a, b, cc) + orient(b, cc, e)*orient(p, a, cc)))
# fan_step translations
P_, A_, B_, E_ = sub(p, cc), sub(a, cc), sub(b, cc), sub(e, cc)
check('fan_step: orient(p,b,c)=det(P,B)', orient(p, b, cc) - det(P_, B_))
check('fan_step: orient(a,b,c)=det(A,B)', orient(a, b, cc) - det(A_, B_))
check('fan_step: orient(p,a,c)=det(P,A)', orient(p, a, cc) - det(P_, A_))
check('fan_step: orient(a,c,e)=det(E,A)', orient(a, cc, e) - det(E_, A_))
check('fan_step: orient(p,c,e)=det(E,P)', orient(p, cc, e) - det(E_, P_))
check('fan_step: orient(b,c,e)=det(E,B)', orient(b, cc, e) - det(E_, B_))
# orient_eq_lin
check('orient_eq_lin', orient(p, x, y) - lin((-(x[1]-p[1]), x[0]-p[0]), x, y))
# lin_pos_of_peel key for arbitrary points: rp = rho(p), pp = p'
rp, pp = pt('r'), pt('pp')
check('lin_pos_of_peel key', orient(p, rp, pp)*lin(sub(c, p), p, y) - (orient(pp, p, y)*lin(sub(c, p), p, rp) + orient(p, rp, y)*lin(sub(c, p), p, pp)))
check('lin_pos: orient(p\',p,y)=det(E,C)', orient(pp, p, y) - det(sub(y, p), sub(pp, p)))
# orient_polar
ra, rb, rd = sp.symbols('r_a r_b r_d', real=True)
check('orient_polar', orient(polar(c, ra, al), polar(c, rb, be), polar(c, rd, de)) - (ra*rb*sp.sin(be-al) + rb*rd*sp.sin(de-be) + rd*ra*sp.sin(al-de)))
check('orient_polar det(A,B)+det(B,D)+det(D,A)', det(sub(polar(c, rb, be), polar(c, ra, al)), sub(polar(c, rd, de), polar(c, ra, al)))
      - (det(polar((0, 0), ra, al), polar((0, 0), rb, be)) + det(polar((0, 0), rb, be), polar((0, 0), rd, de)) + det(polar((0, 0), rd, de), polar((0, 0), ra, al))))
# rule B decomposition
xx, yy = sp.symbols('x y', real=True)
check('ruleB decomposition', (ra*rb*sp.sin(xx) + rb*rd*sp.sin(yy) - rd*ra*sp.sin(xx+yy))
      - (ra*(rb-rd)*sp.sin(xx) + rd*(rb-ra)*sp.sin(yy) + ra*rd*(sp.sin(xx)+sp.sin(yy)-sp.sin(xx+yy))))
# convex_disk identity with u+v=1
A, B = pt('A'), pt('B')
uv = u_*A[0]+(1-u_)*B[0], u_*A[1]+(1-u_)*B[1]
check('convex_disk', u_*ip(A, A) + (1-u_)*ip(B, B) - ip(uv, uv) - u_*(1-u_)*ip(sub(A, B), sub(A, B)))
# centre: rotAbout(c, pi)(p) = 2c - p, orient(p,c,2c-p) = 0
rr = rotAbout(c, sp.pi, p)
check('centre q0', rr[0] - (2*c[0]-p[0])); check('centre q1', rr[1] - (2*c[1]-p[1]))
check('centre orient', orient(p, c, (2*c[0]-p[0], 2*c[1]-p[1])))
# next_prev: with t = pi/m, (m-1) t = pi - t
m = sp.symbols('m', positive=True)
tt = sp.pi/m
check('next_prev (m-1)t = pi - t', (m-1)*tt - (sp.pi - tt))
check('next_prev sin((m-1)t - t) = sin(pi - 2t)', sp.sin((m-1)*tt - tt) - sp.sin(sp.pi - 2*tt))
# regular remark: F = 4 sin t sin jt sin (j-1) t for beta = j*2pi/m
j = sp.symbols('j', positive=True)
F = (sp.cos(2*sp.pi/m)-1)*sp.sin(j*2*sp.pi/m) - sp.sin(2*sp.pi/m)*(sp.cos(j*2*sp.pi/m)-1)
check('regular remark formula', F - 4*sp.sin(sp.pi/m)*sp.sin(j*sp.pi/m)*sp.sin((j-1)*sp.pi/m))
# sin_add expansion
check('sin(x+y) expansion', sp.sin(xx+yy) - (sp.sin(xx)*sp.cos(yy) + sp.cos(xx)*sp.sin(yy)))
# det(r e(phi), s e(psi)) = r s sin(psi - phi)
r1, s1, ph, ps = sp.symbols('r1 s1 phi psi', real=True)
check('det polar', det((r1*sp.cos(ph), r1*sp.sin(ph)), (s1*sp.cos(ps), s1*sp.sin(ps))) - r1*s1*sp.sin(ps-ph))

for name, ok, val in results:
    print(('OK  ' if ok else 'FAIL') + '  ' + name + ('' if ok else '   residual: ' + str(val)))
print('all ok' if all(ok for _, ok, _ in results) else 'SOME FAILED')

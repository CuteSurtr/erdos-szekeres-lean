"""Sympy checks of every algebraic identity in sections/mm.tex (rigor review, round 1)."""
import sympy as sp

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def mir(p):
    return (p[0], -p[1])

a0, a1, b0, b1, d0, d1, p0, p1, q0, q1 = sp.symbols('a0 a1 b0 b1 d0 d1 p0 p1 q0 q1', real=True)
n0, n1, c = sp.symbols('n0 n1 c', real=True)
a, b, d, p, q = (a0, a1), (b0, b1), (d0, d1), (p0, p1), (q0, q1)
results = []

def check(name, expr):
    ok = sp.simplify(sp.expand(expr)) == 0
    results.append((name, ok))
    print(('OK  ' if ok else 'FAIL'), name)

# Lemma mm:lem:orient-mir
check('(b) orient(mir a,mir b,mir d) = -orient(a,b,d)', orient(mir(a), mir(b), mir(d)) + orient(a, b, d))
check('(b) displayed middle expression', orient(mir(a), mir(b), mir(d)) - ((b0-a0)*(-d1+a1) - (-b1+a1)*(d0-a0)))
check('(c) orient(mir a,mir b,d) = -orient(a,b,mir d)', orient(mir(a), mir(b), d) + orient(a, b, mir(d)))
check('(d1) orient(a,b,d) = orient(b,d,a)', orient(a, b, d) - orient(b, d, a))
check('(d2) orient(a,b,d) = -orient(b,a,d)', orient(a, b, d) + orient(b, a, d))
check('(d3) orient(a,b,d) = -orient(d,b,a)', orient(a, b, d) + orient(d, b, a))
check('(e) orient(a,b,mir d) = orient(a,b,d) - 2 d1 (b0-a0)', orient(a, b, mir(d)) - (orient(a, b, d) - 2*d1*(b0-a0)))
check('(e) displayed middle expression', orient(a, b, mir(d)) - ((b0-a0)*(-d1-a1) - (b1-a1)*(d0-a0)))

# Lemma mm:lem:slope (a), case i<l<j
xi, yi, xj, yj, xl, yl = sp.symbols('xi yi xj yj xl yl', real=True)
ci, cj, cl = (xi, yi), (xj, yj), (xl, yl)
check('slope(a) (*)', orient(ci, cj, mir(cl)) - (orient(ci, cj, cl) - 2*yl*(xj-xi)))
check('slope(a) case i<l<j expansion', orient(ci, cj, mir(cl)) - (-(xj-xi)*yl - yi*(xj-xl) - yj*(xl-xi)))
check('slope(a) case l<i: orient(ci,cj,cl)=orient(cl,ci,cj)', orient(ci, cj, cl) - orient(cl, ci, cj))
check('slope(a) case l=i: orient(ci,cj,ci)=0', orient(ci, cj, ci))
check('slope(a) case l=j: orient(ci,cj,cj)=0', orient(ci, cj, cj))

# Lemma mm:lem:slope (b): a1 = 0
A = (sp.Symbol('A0', real=True), 0)
check('slope(b) first form', orient(p, A, q) - ((A[0]-p0)*(q1-p1) + p1*(q0-p0)))
check('slope(b) second form', orient(p, A, q) - ((A[0]-p0)*q1 + p1*(q0-A[0])))

# Theorem mirror-polygon, Case 3 chain; axis (a) Case 3a; axis (b) Case 3a; Case 4
check('Case 3: orient(mir cr, cu2, cu) = orient(cu2, cu, mir cr)', orient(mir(a), b, d) - orient(b, d, mir(a)))
check('Case 3: orient(cu2, cu, mir cr) = -orient(cu, cu2, mir cr)', orient(b, d, mir(a)) + orient(d, b, mir(a)))
check('axis(a) 3a: orient(c0,cu2,cu) = -orient(c0,cu,cu2)', orient(a, b, d) + orient(a, d, b))
check('axis(b) 3a: orient(cm1,cu2,cu) = -orient(cu,cu2,cm1)', orient(a, b, d) + orient(d, b, a))
# mir(a) = a when a1 = 0
check('mir(a)=a on axis (coord 1)', mir(A)[1] - A[1])

# Lemma mm:lem:count (b): three axis points
check('count(b): orient of 3 axis points', orient((a0, 0), (b0, 0), (d0, 0)))

# Lemma mm:lem:injx: orient(p,q,mir p) with q0 = p0
expr = orient(p, (p0, q1), mir(p))
check('injx: orient(p,q,mir p)=0 when q0=p0', expr)
check('injx displayed expression', orient(p, q, mir(p)) - ((q0-p0)*(-p1-p1) - (q1-p1)*(p0-p0)))

# Definition/Lemma frame
s = n0**2 + n1**2
def lineRefl(pt):
    lam = n0*pt[0] + n1*pt[1] - c
    return (pt[0] - 2*lam*n0, pt[1] - 2*lam*n1)
def frame(pt):
    return (n1*(pt[0]-c*n0) - n0*(pt[1]-c*n1), n0*(pt[0]-c*n0) + n1*(pt[1]-c*n1))
def unframe(pt):
    return (n1*pt[0] + n0*pt[1] + c*n0, -n0*pt[0] + n1*pt[1] + c*n1)

fp = frame(p)
check('frame(p)_0 = n1 p0 - n0 p1', fp[0] - (n1*p0 - n0*p1))
check('frame(p)_1 = n0 p0 + n1 p1 - c s', fp[1] - (n0*p0 + n1*p1 - c*s))
uf = unframe(fp)
check('unframe(frame p)_0 = s p0 - c s n0 + c n0', uf[0] - (s*p0 - c*s*n0 + c*n0))
check('unframe(frame p)_0 = p0 + (s-1)(p0 - c n0)', uf[0] - (p0 + (s-1)*(p0 - c*n0)))
check('unframe(frame p)_1 = s p1 - c s n1 + c n1', uf[1] - (s*p1 - c*s*n1 + c*n1))
check('unframe(frame p)_1 = p1 + (s-1)(p1 - c n1)', uf[1] - (p1 + (s-1)*(p1 - c*n1)))
fu = frame(unframe(q))
X = n1*q0 + n0*q1 + c*n0
Y = -n0*q0 + n1*q1 + c*n1
check('frame(unframe q) = (n1 X - n0 Y, n0 X + n1 Y - cs) [0]', fu[0] - (n1*X - n0*Y))
check('frame(unframe q) = (n1 X - n0 Y, n0 X + n1 Y - cs) [1]', fu[1] - (n0*X + n1*Y - c*s))
check('frame(unframe q)_0 = s q0', fu[0] - s*q0)
check('frame(unframe q)_1 = s q1 (= s q1 + cs - cs)', fu[1] - s*q1)
lam = n0*p0 + n1*p1 - c
lr = lineRefl(p)
check('lineRefl(p) = p - 2 lam n [0]', lr[0] - (p0 - 2*lam*n0))
check('lineRefl(p) = p - 2 lam n [1]', lr[1] - (p1 - 2*lam*n1))
check('R n = (0, s) [0]', n1*n0 - n0*n1)
check('R n = (0, s) [1]', n0*n0 + n1*n1 - s)
flr = frame(lr)
check('frame(lineRefl p) = frame(p) - 2 lam (0,s) [0]', flr[0] - fp[0])
check('frame(lineRefl p) = frame(p) - 2 lam (0,s) [1]', flr[1] - (fp[1] - 2*lam*s))
mfp = mir(fp)
check('frame(lineRefl p)_0 - mir(frame p)_0 = 0 (ring)', flr[0] - mfp[0])
check('2nd coord difference = 2(n0p0+n1p1-cs) - 2 lam s', flr[1] - mfp[1] - (2*(n0*p0+n1*p1-c*s) - 2*lam*s))
check('2nd coord difference = -2(s-1)(n0p0+n1p1)', flr[1] - mfp[1] - (-2*(s-1)*(n0*p0+n1*p1)))
check('orient_frame: orient(frame a, frame b, frame d) = s orient(a,b,d)',
      orient(frame(a), frame(b), frame(d)) - s*orient(a, b, d))
# Lean linear_combination certificates: LHS - RHS = coeff * (s - 1)
check('cert unframe_frame[0] coeff p0 - c n0', (uf[0] - p0) - (p0 - c*n0)*(s-1))
check('cert unframe_frame[1] coeff p1 - c n1', (uf[1] - p1) - (p1 - c*n1)*(s-1))
check('cert frame_unframe[0] coeff q0', (fu[0] - q0) - q0*(s-1))
check('cert frame_unframe[1] coeff q1', (fu[1] - q1) - q1*(s-1))
check('cert frame_lineRefl[1] coeff -2(n0p0+n1p1)', (flr[1] - mfp[1]) - (-2*(n0*p0+n1*p1))*(s-1))
check('cert orient_frame coeff orient(a,b,d)', (orient(frame(a), frame(b), frame(d)) - orient(a, b, d)) - orient(a, b, d)*(s-1))

# Remark after Definition frame (with s = 1 substituted via n1^2 = 1 - n0^2 is awkward; check general forms)
lam_lr = n0*lr[0] + n1*lr[1] - c
check('remark: lam(lineRefl p) = lam - 2 lam s  (so = -lam when s = 1)', lam_lr - (lam - 2*lam*s))
check('remark: n1 x - n0 y unchanged by lineRefl', (n1*lr[0] - n0*lr[1]) - (n1*p0 - n0*p1))
check('remark: frame(p)_1 = lam(p) + c(1-s)', fp[1] - (lam + c*(1-s)))
check('det R = s', sp.Matrix([[n1, -n0], [n0, n1]]).det() - s)

print()
print('ALL OK' if all(ok for _, ok in results) else 'SOME FAILED', len(results), 'checks')

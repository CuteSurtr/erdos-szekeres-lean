#!/usr/bin/env python
# Independent recheck of the claims about refl and isoT (MirrorA.lean, l. 705-712)
# made in the Coverage paragraph of sections/mm.tex, final pass round 1.
import sympy as sp

p00, p01, u1, u2, t, s, x, y = sp.symbols('p00 p01 u1 u2 t s x y', real=True)

def refl(p0, u, p):
    d = (p[0] - p0[0]) * u[0] + (p[1] - p0[1]) * u[1]
    return (p0[0] + 2 * d * u[0] - (p[0] - p0[0]),
            p0[1] + 2 * d * u[1] - (p[1] - p0[1]))

def isoT(p0, u, p):
    return (u[0] * (p[0] - p0[0]) + u[1] * (p[1] - p0[1]),
            -u[1] * (p[0] - p0[0]) + u[0] * (p[1] - p0[1]))

p0 = (p00, p01)
u = (u1, u2)
unit = {u2**2: 1 - u1**2}  # impose u1^2 + u2^2 = 1

GENS = (u2, u1, p00, p01, t, s, x, y)

def red(e):
    # normal form modulo the ideal (u1^2 + u2^2 - 1); a single polynomial is a Groebner basis,
    # and with u2 first in lex order the remainder has degree <= 1 in u2 (canonical).
    e = sp.expand(e)
    if e == 0:
        return sp.Integer(0)
    _, r = sp.reduced(e, [u1**2 + u2**2 - 1], *GENS, order='lex')
    return sp.expand(r)

ok = True

# (1) isoT maps the point p0 + t u of the line to (t, 0): the line goes onto the x-axis.
img = isoT(p0, u, (p00 + t * u1, p01 + t * u2))
c1 = (red(img[0] - t), red(img[1]))
print("isoT(p0 + t u) - (t, 0) =", c1)
ok &= c1 == (0, 0)

# (2) isoT is a rigid motion: isoT(p) = A (p - p0) with A orthogonal of determinant 1.
A = sp.Matrix([[u1, u2], [-u2, u1]])
q = sp.Matrix([x - p00, y - p01])
lin = A * q
c2 = (sp.expand(lin[0] - isoT(p0, u, (x, y))[0]), sp.expand(lin[1] - isoT(p0, u, (x, y))[1]))
print("isoT(p) - A(p - p0) =", c2)
ok &= c2 == (0, 0)
AtA = (A.T * A).applyfunc(red)
detA = red(A.det())
print("A^T A =", AtA.tolist(), " det A =", detA)
ok &= AtA == sp.eye(2) and detA == 1

# (3) refl fixes the line pointwise and negates the normal (-u2, u1): orthogonal reflection.
fix = refl(p0, u, (p00 + t * u1, p01 + t * u2))
c3 = (red(fix[0] - (p00 + t * u1)), red(fix[1] - (p01 + t * u2)))
print("refl(p0 + t u) - (p0 + t u) =", c3)
ok &= c3 == (0, 0)
nrm = refl(p0, u, (p00 - s * u2, p01 + s * u1))
c4 = (sp.expand(nrm[0] - (p00 + s * u2)), sp.expand(nrm[1] - (p01 - s * u1)))
print("refl(p0 + s n) - (p0 - s n) =", c4)
ok &= c4 == (0, 0)

# (4) isoT_refl: isoT (refl p) = mu (isoT p), mu(a, b) = (a, -b).
lhs = isoT(p0, u, refl(p0, u, (x, y)))
rhs = isoT(p0, u, (x, y))
c5 = (red(lhs[0] - rhs[0]), red(lhs[1] + rhs[1]))
print("isoT(refl p) - mu(isoT p) =", c5)
ok &= c5 == (0, 0)

# (5) without the unit condition isoT is not an isometry (so 'rigid motion' needs |u| = 1).
print("det A without unit condition =", sp.expand(A.det()))

print("ALL OK" if ok else "FAILURE")

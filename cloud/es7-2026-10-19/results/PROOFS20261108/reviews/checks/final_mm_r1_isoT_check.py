import sympy as sp
p01, p02, u1, u2, t, s, x, y = sp.symbols('p01 p02 u1 u2 t s x y', real=True)
def refl(p):
    d = (p[0]-p01)*u1 + (p[1]-p02)*u2
    return (p01 + 2*d*u1 - (p[0]-p01), p02 + 2*d*u2 - (p[1]-p02))
def isoT(p):
    return (u1*(p[0]-p01) + u2*(p[1]-p02), -u2*(p[0]-p01) + u1*(p[1]-p02))
unit = {u2**2: 1 - u1**2}
line_pt = (p01 + t*u1, p02 + t*u2)
img = isoT(line_pt)
print("isoT(p0 + t u) =", [sp.simplify(sp.expand(c).subs(unit)) for c in img])
nrm_pt = (p01 - s*u2, p02 + s*u1)
print("refl fixes line:", [sp.simplify(sp.expand(a - b).subs(unit)) for a, b in zip(refl(line_pt), line_pt)])
print("refl on normal :", [sp.simplify(sp.expand(a - b)) for a, b in zip(refl(nrm_pt), (p01 + s*u2, p02 - s*u1))])
# isoT is a rigid motion: linear part [[u1,u2],[-u2,u1]] has det u1^2+u2^2 = 1 and is orthogonal
M = sp.Matrix([[u1, u2], [-u2, u1]])
print("det:", sp.expand(M.det()), " M^T M - I:", sp.simplify((M.T*M - sp.eye(2)).subs(unit)))

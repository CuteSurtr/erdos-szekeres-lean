from sympy import symbols, Matrix, simplify, expand
# Identities behind the reworded hunks of ar.tex (polish round 1):
# (1) proof of ar:lem:orient-affine: orient(g x, g y, g z) = det(L) orient(x, y, z) for g(p) = Lp + b;
# (2) proof of ar:prop:averaging(b): the factor of lin2(s, beta/s, 0, t) is s t - (beta/s) 0 = s t;
# (3) conventions (AffineEquiv.ext): f_lin(v) = f(v) - f(0) for f(p) = Lp + b.
L00, L01, L10, L11, b0, b1, s, t, be = symbols('L00 L01 L10 L11 b0 b1 s t beta', real=True)
x0, x1, y0, y1, z0, z1, v0, v1 = symbols('x0 x1 y0 y1 z0 z1 v0 v1', real=True)
def orient(a, b, c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
L = Matrix([[L00, L01], [L10, L11]]); bb = Matrix([b0, b1])
g = lambda p: L*Matrix(p)+bb
X, Y, Z = (x0, x1), (y0, y1), (z0, z1)
ok1 = expand(orient(g(X), g(Y), g(Z)) - L.det()*orient(X, Y, Z)) == 0
T = Matrix([[s, be/s], [0, t]])
ok2 = simplify(T.det() - (s*t - (be/s)*0)) == 0 and simplify(s*t-(be/s)*0 - s*t) == 0
flin = lambda v: L*Matrix(v)
ok3 = simplify(g((v0, v1)) - g((0, 0)) - flin((v0, v1))) == Matrix([0, 0])
print('orient_affine factor det L:', ok1)
print('lin2(s,beta/s,0,t) factor st:', ok2)
print('f_lin(v)=f(v)-f(0):', ok3)

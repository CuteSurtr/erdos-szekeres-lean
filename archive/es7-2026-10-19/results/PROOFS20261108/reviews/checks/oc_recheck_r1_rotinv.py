import sympy as sp
c0,c1,a0,a1,b0,b1,d0,d1,C,S=sp.symbols('c0 c1 a0 a1 b0 b1 d0 d1 C S')
def orient(a,b,d): return (b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0])
def R(p): return (c0+C*(p[0]-c0)-S*(p[1]-c1), c1+S*(p[0]-c0)+C*(p[1]-c1))
a,b,d=(a0,a1),(b0,b1),(d0,d1)
M=sp.Matrix([[C,-S],[S,C]])
# Def oc:def:basic(b): R(p) = c + M (p - c)
v=sp.Matrix([a0-c0,a1-c1]); w=M*v
print('matrix form ok:', sp.expand(R(a)[0]-(c0+w[0]))==0 and sp.expand(R(a)[1]-(c1+w[1]))==0)
# Lean linear_combination: LHS - RHS - orient(a,b,d)*(S^2+C^2-1) == 0
print('linear_combination identity ok:', sp.expand(orient(R(a),R(b),R(d))-orient(a,b,d)-orient(a,b,d)*(S**2+C**2-1))==0)
print('det M =', sp.expand(M.det()))

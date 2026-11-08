import sympy as sp
ca, sa, cb, sb = sp.symbols('ca sa cb sb')
c0, c1, x0, x1 = sp.symbols('c0 c1 x0 x1')
def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
def rot(C, S, p):
    return (c0 + C*(p[0]-c0) - S*(p[1]-c1), c1 + S*(p[0]-c0) + C*(p[1]-c1))
x = (x0, x1)
lhs = orient(x, rot(ca, sa, x), rot(cb, sb, x))
rhs = ((x0-c0)**2 + (x1-c1)**2)*((ca-1)*sb - sa*(cb-1))
print('orient_rotAbout pure polynomial:', sp.expand(lhs - rhs) == 0)
# lin_rotAbout as pure polynomial
cbe, sbe = sp.symbols('cbe sbe')
p0, p1 = x0, x1
r = rot(cbe, sbe, (p0, p1))
linv = (c0-p0)*(r[0]-p0) + (c1-p1)*(r[1]-p1)
print('lin_rotAbout pure polynomial:', sp.expand(linv - ((p0-c0)**2+(p1-c1)**2)*(1-cbe)) == 0)

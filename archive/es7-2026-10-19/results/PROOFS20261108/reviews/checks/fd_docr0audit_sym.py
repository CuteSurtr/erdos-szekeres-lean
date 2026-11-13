import sympy as sp
th,c0,c1,p0,p1,v0,v1=sp.symbols('theta c0 c1 p0 p1 v0 v1', real=True)
R=sp.Matrix([[sp.cos(th),-sp.sin(th)],[sp.sin(th),sp.cos(th)]])
c=sp.Matrix([c0,c1]); p=sp.Matrix([p0,p1]); v=sp.Matrix([v0,v1])
def rho(q):
    return sp.Matrix([c0+sp.cos(th)*(q[0]-c0)-sp.sin(th)*(q[1]-c1), c1+sp.sin(th)*(q[0]-c0)+sp.cos(th)*(q[1]-c1)])
checks={
 'rho(p) = c + R(p-c)': rho(p)-(c+R*(p-c)),
 'c + R(p-c) = R p + (c - R c)': (c+R*(p-c))-(R*p+(c-R*c)),
 'map_vadd: rho(v+p) = R v + rho(p)': rho(v+p)-(R*v+rho(p)),
 'rho(c) = c': rho(c)-c,
}
for k,e in checks.items():
    print(k, all(sp.simplify(x)==0 for x in e))

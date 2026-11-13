import sympy as sp
al = sp.symbols('alpha', real=True)
p0, p1, c0, c1 = sp.symbols('p0 p1 c0 c1', real=True)
def rot(c, t, p):
    return (c[0] + sp.cos(t)*(p[0]-c[0]) - sp.sin(t)*(p[1]-c[1]),
            c[1] + sp.sin(t)*(p[0]-c[0]) + sp.cos(t)*(p[1]-c[1]))
c = (c0, c1); p = (p0, p1)
ok = True
for jj in range(0, 7):
    q = p
    for _ in range(jj):
        q = rot(c, al, q)
    r = rot(c, jj*al, p)
    for i in range(2):
        d = (q[i] - r[i]).rewrite(sp.exp)
        d = sp.simplify(sp.expand(d))
        print(jj, i, d == 0)
        ok = ok and d == 0
print('rot(d) j<=6:', ok)

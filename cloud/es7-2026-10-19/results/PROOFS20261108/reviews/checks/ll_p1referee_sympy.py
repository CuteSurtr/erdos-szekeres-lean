import sympy as sp

th, al = sp.symbols('theta alpha', real=True)
p0, p1, c0, c1, v0, v1 = sp.symbols('p0 p1 c0 c1 v0 v1', real=True)
lam, mu = sp.symbols('lam mu', real=True)
j = sp.symbols('j', integer=True, nonnegative=True)

def rot(c, t, p):
    return (c[0] + sp.cos(t)*(p[0]-c[0]) - sp.sin(t)*(p[1]-c[1]),
            c[1] + sp.sin(t)*(p[0]-c[0]) + sp.cos(t)*(p[1]-c[1]))

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

c = (c0, c1); p = (p0, p1); v = (v0, v1)
res = {}

# Lemma rot(a): gamma + e^{i theta}(u - gamma), real and imaginary parts
u = p0 + sp.I*p1; g = c0 + sp.I*c1
z = sp.expand(g + (sp.cos(th) + sp.I*sp.sin(th))*(u - g))
rp = rot(c, th, p)
res['rot(a) re'] = sp.simplify(sp.re(z) - rp[0]) == 0
res['rot(a) im'] = sp.simplify(sp.im(z) - rp[1]) == 0

# Lemma rot(b): rho(v+p) = A v + rho(p)
lhs = rot(c, th, (v0+p0, v1+p1))
Av = (sp.cos(th)*v0 - sp.sin(th)*v1, sp.sin(th)*v0 + sp.cos(th)*v1)
res['rot(b) 0'] = sp.simplify(lhs[0] - (Av[0] + rp[0])) == 0
res['rot(b) 1'] = sp.simplify(lhs[1] - (Av[1] + rp[1])) == 0

# rho(c) = c
rc = rot(c, th, c)
res['rho(c)=c'] = sp.simplify(rc[0]-c0) == 0 and sp.simplify(rc[1]-c1) == 0

# Lemma rot(d) for j = 0..6 symbolically: iterate rot by alpha j times equals rot by j*alpha
ok = True
for jj in range(0, 7):
    q = p
    for _ in range(jj):
        q = rot(c, al, q)
    r = rot(c, jj*al, p)
    d0 = sp.simplify(sp.expand_trig(sp.expand(q[0] - r[0])))
    d1 = sp.simplify(sp.expand_trig(sp.expand(q[1] - r[1])))
    ok = ok and d0 == 0 and d1 == 0
res['rot(d) j<=6'] = ok

# rho_{c,3*2pi/6} = rho_{c,pi}; rho_{c,pi}(p) = 2c - p
res['3*(2pi/6)=pi'] = sp.simplify(3*(2*sp.pi/6) - sp.pi) == 0
rpi = rot(c, sp.pi, p)
res['rho_pi(p)=2c-p'] = sp.simplify(rpi[0] - (2*c0-p0)) == 0 and sp.simplify(rpi[1] - (2*c1-p1)) == 0

# orient(p, c, 2c-p) = 0
res['orient(p,c,2c-p)=0'] = sp.expand(orient(p, c, (2*c0-p0, 2*c1-p1))) == 0
# the displayed intermediate expression
disp = (c0-p0)*2*(c1-p1) - (c1-p1)*2*(c0-p0)
res['orient display'] = sp.expand(orient(p, c, (2*c0-p0, 2*c1-p1)) - disp) == 0

# Lemma hv(c): coefficient sum ((1-lam)+lam(1-mu))/(1-lam mu) = 1
res['hv(c) sum'] = sp.simplify(((1-lam) + lam*(1-mu))/(1-lam*mu) - 1) == 0

# Lemma complex (d), (f), (g)
U, G, W, V, Q = sp.symbols('U G W V Q')
res['complex(d)'] = sp.expand(G + W*((G + V*(U-G)) - G) - (G + W*V*(U-G))) == 0
res['complex(f)'] = sp.expand((G + W*(U-G) - U) - (W-1)*(U-G)) == 0
res['complex(g)'] = sp.expand((G + W*(U-G)) - (G + W*(Q-G)) - W*(U-Q)) == 0

# Lemma minperiod: omega^m = 1 and omega^k != 1 for 0<k<m, small m
ok = True
for m in range(1, 13):
    w = sp.exp(2*sp.pi*sp.I/m)
    ok = ok and sp.simplify(w**m - 1) == 0
    for k in range(1, m):
        # Re(omega^k) = cos(2 pi k/m) < 1 exactly
        ok = ok and sp.simplify(sp.cos(2*sp.pi*k/m) - 1) != 0 and sp.N(sp.cos(2*sp.pi*k/m)) < 1
res['primitive root m<=12'] = ok

# Arithmetic of the octagon theorems
res['6*(11-1)=60<61'] = 6*(11-1) == 60 and 60 < 61
res['7*(10-1)=63<64'] = 7*(10-1) == 63 and 63 < 64
res['6*11=66, 7*10=70'] = 6*11 == 66 and 7*10 == 70
res['8<=12, 8<=14'] = 8 <= 2*6 and 8 <= 2*7

for k_, v_ in res.items():
    print(f'{k_}: {v_}')
print('ALL OK' if all(res.values()) else 'SOME FAILED')

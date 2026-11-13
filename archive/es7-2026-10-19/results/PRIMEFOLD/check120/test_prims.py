import sys, random, cmath, math
sys.path.insert(0, sys.argv[1])
from exact_geom import *
random.seed(12345)
z = cmath.exp(2j*math.pi/8)
def cval(w): return sum(w[j]*z**j for j in range(8))
bad = 0; tested = 0; skipped = 0
for trial in range(20000):
    ws = [tuple(random.randint(-50,50) for _ in range(8)) for _ in range(3)]
    P = [coords(w) for w in ws]; Q = [red4(w) for w in ws]
    # check coords
    for w,(X,Y) in zip(ws,P):
        c = cval(w)
        xf = (X[0]+X[1]*math.sqrt(2))/2; yf=(Y[0]+Y[1]*math.sqrt(2))/2
        assert abs(xf-c.real)<1e-9 and abs(yf-c.imag)<1e-9, (w, xf, c)
    p,q,r = [cval(w) for w in ws]
    d = ((q-p).conjugate()*(r-p)).imag
    s1,_ = orient_M1(P,0,1,2); s2 = orient_M2(Q,0,1,2)
    if abs(d) < 1e-6: skipped += 1; continue
    tested += 1
    sf = 1 if d>0 else -1
    if s1 != sf or s2 != sf: bad += 1
# rotation check
for trial in range(2000):
    w = tuple(random.randint(-50,50) for _ in range(8))
    X,Y = coords(w); Xr,Yr = rot_zeta_exact(X,Y)
    assert (Xr,Yr) == coords(rot_zeta_coeffs(w))
    c = cval(w)*z
    assert abs((Xr[0]+Xr[1]*math.sqrt(2))/2 - c.real) < 1e-9
# sign_ab exhaustive small
for A in range(-30,31):
    for B in range(-30,31):
        v = A + B*math.sqrt(2)
        s = sign_ab(A,B)
        assert s == (0 if v==0 else (1 if v>0 else -1)), (A,B)
# collinear exact zero test: p, 2p, 3p collinear with origin-free combos
w = (3,1,4,1,5,9,2,6); w2 = tuple(2*x for x in w); w3 = tuple(3*x for x in w)
P=[coords(x) for x in (w,w2,w3)]; Q=[red4(x) for x in (w,w2,w3)]
print("collinear test M1,M2:", orient_M1(P,0,1,2)[0], orient_M2(Q,0,1,2))
print("tested", tested, "skipped", skipped, "bad", bad)

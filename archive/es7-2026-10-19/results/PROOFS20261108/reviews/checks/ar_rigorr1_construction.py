"""Exact sanity check of Proposition ar:prop:averaging on non-orthogonal finite-order linear parts."""
import sympy as sp

z0, z1, x0, x1, y0, y1 = sp.symbols('z0 z1 x0 x1 y0 y1', real=True)
b0, b1 = sp.Rational(3, 7), sp.Rational(-5, 2)  # arbitrary translation part

def nsq(v):
    return v[0]**2 + v[1]**2

cases = {
    "order 3 [[0,-1],[1,-1]]": sp.Matrix([[0, -1], [1, -1]]),
    "order 6 [[1,-1],[1,0]]": sp.Matrix([[1, -1], [1, 0]]),
    "order 4 [[1,-2],[1,-1]]": sp.Matrix([[1, -2], [1, -1]]),
    "order 2 det -1 [[1,1],[0,-1]]": sp.Matrix([[1, 1], [0, -1]]),
    "order 2 det +1 (-I)": sp.Matrix([[-1, 0], [0, -1]]),
}
allok = True
for name, L in cases.items():
    # order of L
    m = next(k for k in range(1, 13) if L**k == sp.eye(2))
    al = sum(((L**k)[0, 0]**2 + (L**k)[1, 0]**2) for k in range(m))
    be = sum(((L**k)[0, 0]*(L**k)[0, 1] + (L**k)[1, 0]*(L**k)[1, 1]) for k in range(m))
    ga = sum(((L**k)[0, 1]**2 + (L**k)[1, 1]**2) for k in range(m))
    s = sp.sqrt(al)
    t = sp.sqrt((al*ga - be**2)/al)
    T = sp.Matrix([[s, be/s], [0, t]])
    Ti = sp.Matrix([[1/s, -be/(s**2*t)], [0, 1/t]])
    z = sp.Matrix([z0, z1])
    avg = sum(nsq(L**k*z) for k in range(m))
    c1 = sp.simplify(sp.expand(nsq(T*z) - avg)) == 0
    c2 = sp.simplify(sp.expand(sum(nsq(L**k*(L*z)) for k in range(m)) - avg)) == 0
    c3 = sp.simplify(T*Ti - sp.eye(2)) == sp.zeros(2) and sp.simplify(Ti*T - sp.eye(2)) == sp.zeros(2)
    cc = sp.Matrix([b0, b1]); bvec = (sp.eye(2) - L)*cc  # g fixes cc
    g = lambda p: L*p + bvec
    h = lambda p: T*g(Ti*p)
    X = sp.Matrix([x0, x1]); Y = sp.Matrix([y0, y1])
    c4 = sp.simplify(sp.expand(nsq(h(X) - h(Y)) - nsq(X - Y))) == 0
    # order of h equals order of g: h^k = T g^k Ti
    def iterate(f, k, p):
        for _ in range(k):
            p = f(p)
        return p
    ordg = next(k for k in range(1, 13) if sp.simplify(iterate(g, k, X) - X) == sp.zeros(2, 1))
    ordh = next(k for k in range(1, 13) if sp.simplify(iterate(h, k, X) - X) == sp.zeros(2, 1))
    c5 = (ordg == ordh == m)
    detT = sp.simplify(T.det())
    c6 = sp.simplify(detT - s*t) == 0 and detT.is_positive
    ok = c1 and c2 and c3 and c4 and c5 and c6
    allok = allok and ok
    print(f"{name}: m={m} alpha={al} beta={be} gamma={ga} disc={sp.simplify(al*ga-be**2)} "
          f"nsq(Tz)=avgQ:{c1} invariance:{c2} inverse:{c3} isometry:{c4} ord g={ordg} ord h={ordh} det T>0:{c6}")
print("ALL_OK" if allok else "SOME_FAIL")

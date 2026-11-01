"""Exact symbolic verification of the polynomial identities used in proof.md.

A polynomial is a dict {monomial: integer coefficient}, a monomial a sorted tuple of variable names (with repetition).
Each identity is expanded completely and must reduce to the zero polynomial.
"""
from collections import defaultdict


def var(name):
    return {(name,): 1}


def const(c):
    return {(): c} if c else {}


def add(*ps):
    r = defaultdict(int)
    for p in ps:
        for m, c in p.items():
            r[m] += c
    return {m: c for m, c in r.items() if c}


def neg(p):
    return {m: -c for m, c in p.items()}


def mul(p, q):
    r = defaultdict(int)
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            r[tuple(sorted(m1 + m2))] += c1 * c2
    return {m: c for m, c in r.items() if c}


def scal(k, p):
    return {m: k * c for m, c in p.items() if k * c}


def det3(u, v, w):
    """u, v, w: lists of 3 polynomials"""
    return add(mul(u[0], add(mul(v[1], w[2]), neg(mul(v[2], w[1])))),
               neg(mul(u[1], add(mul(v[0], w[2]), neg(mul(v[2], w[0]))))),
               mul(u[2], add(mul(v[0], w[1]), neg(mul(v[1], w[0])))))


def vec(name, affine=True):
    """homogeneous vector (1, x, y) if affine, else (w, x, y)"""
    return [const(1) if affine else var(name + "w"), var(name + "x"), var(name + "y")]


def report(label, p):
    ok = (p == {})
    print(f"{'OK  ' if ok else 'FAIL'} {label}" + ("" if ok else f"  residual has {len(p)} terms"))
    return ok


def main():
    allok = True
    # (GP) three-term Grassmann-Pluecker relation, arbitrary vectors of R^3 (15 indeterminates)
    x, a, b, c, d = (vec(n, affine=False) for n in "xabcd")
    D = det3
    gp = add(mul(D(x, a, b), D(x, c, d)), neg(mul(D(x, a, c), D(x, b, d))), mul(D(x, a, d), D(x, b, c)))
    allok &= report("GP: [xab][xcd] - [xac][xbd] + [xad][xbc] = 0 for all x,a,b,c,d in R^3", gp)
    # the same relation with the code's index pattern: y0..y3 sorted, coefficients (+1, -1, +1)
    # (identical to the line above with a,b,c,d = y0,y1,y2,y3)

    # (A4) interiority identity, all first coordinates 1
    p, q, r, t = (vec(n) for n in "pqrt")
    a4 = add(D(p, q, r), neg(D(t, q, r)), neg(D(p, t, r)), neg(D(p, q, t)))
    allok &= report("A4: D(p,q,r) = D(t,q,r) + D(p,t,r) + D(p,q,t) when all first coordinates are 1", a4)
    # weighted version (first coordinates w_*): w_t D(p,q,r) = w_p D(t,q,r) + w_q D(p,t,r) + w_r D(p,q,t)
    p, q, r, t = (vec(n, affine=False) for n in "pqrt")
    a4w = add(mul(p_w := var("tw"), D(p, q, r)), neg(mul(var("pw"), D(t, q, r))), neg(mul(var("qw"), D(p, t, r))),
              neg(mul(var("rw"), D(p, q, t))))
    allok &= report("A4 (weighted): w_t D(p,q,r) = w_p D(t,q,r) + w_q D(p,t,r) + w_r D(p,q,t)", a4w)

    # (CENTRE) v_c = (v_p + v_hp)/2 with hp = 2c - p: 2 D(c,p,q) = D(hp,p,q)
    c = vec("c")
    p, q = vec("p"), vec("q")
    hp = [const(1), add(scal(2, c[1]), neg(p[1])), add(scal(2, c[2]), neg(p[2]))]
    cen = add(scal(2, D(c, p, q)), neg(D(hp, p, q)))
    allok &= report("CENTRE: 2 D(c,p,q) = D(h(p),p,q) where h(p) = 2c - p", cen)
    # midpoint as vectors: v_p + v_hp - 2 v_c = 0 coordinatewise
    mid = [add(p[i], hp[i], scal(-2, c[i])) for i in range(3)]
    allok &= report("CENTRE: v_p + v_h(p) = 2 v_c (coordinatewise)", {k: v for m in mid for k, v in m.items()})

    # (ZERO) D(c, p, h(p)) = 0
    allok &= report("ZERO: D(c, p, h(p)) = 0", D(c, p, hp))

    # (GROUP) half-turn invariance D(h a, h b, h d) = D(a, b, d), including triples with c (h(c) = c)
    a, b, d = vec("a"), vec("b"), vec("d")

    def h(v):
        return [const(1), add(scal(2, c[1]), neg(v[1])), add(scal(2, c[2]), neg(v[2]))]
    allok &= report("GROUP: D(h a, h b, h d) = D(a, b, d)", add(D(h(a), h(b), h(d)), neg(D(a, b, d))))
    allok &= report("GROUP: h(c) = c", {k: v for i in range(3) for k, v in add(h(c)[i], neg(c[i])).items()})
    allok &= report("GROUP: D(c, h a, h b) = D(c, a, b)", add(D(c, h(a), h(b)), neg(D(c, a, b))))

    # (HULL) barycentric identity for 'q inside triangle abd': D(a,b,d) = D(a,b,q) + D(b,d,q) + D(d,a,q)
    qq = vec("q")
    allok &= report("HULL: D(a,b,d) = D(a,b,q) + D(b,d,q) + D(d,a,q)",
                    add(D(a, b, d), neg(D(a, b, qq)), neg(D(b, d, qq)), neg(D(d, a, qq))))

    # (ORIENT) D((1,a),(1,b),(1,d)) equals ErdosSzekeres.orient a b d = (b0-a0)(d1-a1) - (b1-a1)(d0-a0)
    o = add(mul(add(b[1], neg(a[1])), add(d[2], neg(a[2]))), neg(mul(add(b[2], neg(a[2])), add(d[1], neg(a[1])))))
    allok &= report("ORIENT: det(v_a, v_b, v_d) = orient(a, b, d)", add(D(a, b, d), neg(o)))

    # (ANTI) D(c, p, h(q)) = -D(c, p, q): the two points of a pair lie on opposite sides of every line through c
    hq = h(q)
    allok &= report("ANTI: D(c, p, h q) = -D(c, p, q)", add(D(c, p, hq), D(c, p, q)))
    print("ALL IDENTITIES VERIFIED" if allok else "SOME IDENTITY FAILED")

    # negative controls: each of these is false and must leave a nonzero residual
    print("-- negative controls (each must FAIL) --")
    ctrl = []
    x, a, b, c4, d4 = (vec(n, affine=False) for n in "xabcd")
    ctrl.append(report("control GP with middle sign +", add(mul(D(x, a, b), D(x, c4, d4)), mul(D(x, a, c4), D(x, b, d4)),
                                                           mul(D(x, a, d4), D(x, b, c4)))))
    p, q, r, t = (vec(n, affine=False) for n in "pqrt")
    ctrl.append(report("control A4 unweighted on arbitrary vectors (needs first coordinates 1)",
                       add(D(p, q, r), neg(D(t, q, r)), neg(D(p, t, r)), neg(D(p, q, t)))))
    c = vec("c")
    p, q = vec("p"), vec("q")
    hp = [const(1), add(scal(2, c[1]), neg(p[1])), add(scal(2, c[2]), neg(p[2]))]
    ctrl.append(report("control CENTRE with the wrong sign: 2 D(c,p,q) = -D(h(p),p,q)", add(scal(2, D(c, p, q)), D(hp, p, q))))
    refl = [const(1), neg(p[1]), p[2]]       # a reflection x -> -x has det -1
    a, b, d = vec("a"), vec("b"), vec("d")

    def m(v):
        return [const(1), neg(v[1]), v[2]]
    ctrl.append(report("control GROUP for a reflection (det -1)", add(D(m(a), m(b), m(d)), neg(D(a, b, d)))))
    print("CONTROLS BEHAVE" if not any(ctrl) else "A CONTROL WRONGLY PASSED")


if __name__ == "__main__":
    main()

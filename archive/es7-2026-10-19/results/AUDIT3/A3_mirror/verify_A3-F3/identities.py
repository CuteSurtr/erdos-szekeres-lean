#!/usr/bin/env python3
"""A3-F3 (c), (d) background: exact symbolic checks of the two determinant identities the mirror soundness proof uses.

1. Cramer 4-term identity in R^3 (generic vectors p, q, r, t; 12 indeterminates):
       det(q,r,t) p - det(p,r,t) q + det(p,q,t) r - det(p,q,r) t = 0
   and its rewriting in the literal order used by zcnf.add_a4:
       det(t,q,r) p + det(p,t,r) q + det(p,q,t) r - det(p,q,r) t = 0.
2. Three-term Grassmann-Pluecker relation with the sign convention of zcnf.add_gp (k = +1, -1, +1):
       [x y0 y1][x y2 y3] - [x y0 y2][x y1 y3] + [x y0 y3][x y1 y2] = 0   (15 indeterminates).

Polynomials are dicts {exponent tuple: integer coefficient}; the check is an exact expansion, not random evaluation."""
import itertools


class Poly:
    def __init__(self, nvars, terms=None):
        self.n = nvars
        self.t = {k: v for k, v in (terms or {}).items() if v != 0}

    @staticmethod
    def var(n, i):
        e = [0] * n
        e[i] = 1
        return Poly(n, {tuple(e): 1})

    def __add__(self, o):
        r = dict(self.t)
        for k, v in o.t.items():
            r[k] = r.get(k, 0) + v
        return Poly(self.n, r)

    def __neg__(self):
        return Poly(self.n, {k: -v for k, v in self.t.items()})

    def __sub__(self, o):
        return self + (-o)

    def __mul__(self, o):
        r = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                r[k] = r.get(k, 0) + v1 * v2
        return Poly(self.n, r)

    def is_zero(self):
        return not self.t


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def vecs(n_vec):
    n = 3 * n_vec
    return [[Poly.var(n, 3 * i + j) for j in range(3)] for i in range(n_vec)]


def main():
    ok = True
    # 1. Cramer
    p, q, r, t = vecs(4)
    for j in range(3):
        e1 = det3(q, r, t) * p[j] - det3(p, r, t) * q[j] + det3(p, q, t) * r[j] - det3(p, q, r) * t[j]
        e2 = det3(t, q, r) * p[j] + det3(p, t, r) * q[j] + det3(p, q, t) * r[j] - det3(p, q, r) * t[j]
        print(f"Cramer coordinate {j}: form1 zero={e1.is_zero()}  zcnf-literal form zero={e2.is_zero()}")
        ok &= e1.is_zero() and e2.is_zero()
    # orientation facts used in the rewriting
    ok &= (det3(t, q, r) - det3(q, r, t)).is_zero() and (det3(p, t, r) + det3(p, r, t)).is_zero()
    # 2. Grassmann-Pluecker, code convention
    x, y0, y1, y2, y3 = vecs(5)
    gp = det3(x, y0, y1) * det3(x, y2, y3) - det3(x, y0, y2) * det3(x, y1, y3) + det3(x, y0, y3) * det3(x, y1, y2)
    print(f"GP 3-term (k = +1,-1,+1) zero={gp.is_zero()}")
    ok &= gp.is_zero()
    # a wrong sign convention must NOT vanish (sanity of the checker)
    bad = det3(x, y0, y1) * det3(x, y2, y3) + det3(x, y0, y2) * det3(x, y1, y3) + det3(x, y0, y3) * det3(x, y1, y2)
    print(f"GP with k = +1,+1,+1 (control, must be nonzero) zero={bad.is_zero()}")
    ok &= not bad.is_zero()
    print("RESULT", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()

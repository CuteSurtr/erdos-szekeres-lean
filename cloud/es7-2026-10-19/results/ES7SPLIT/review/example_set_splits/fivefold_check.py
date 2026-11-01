#!/usr/bin/env python3
"""One-sidedness enumeration for the 5-fold example sets (not part of the claim; checks the broader phrase of the original
summary, "the symmetric extremal sets have none").

Point c0 + c1 w + c2 w^2 + c3 w^3, w = exp(2 pi i / 5).  With cos72 = (r5 - 1)/4, cos144 = cos216 = -(r5 + 1)/4,
sin144 / sin72 = (r5 - 1)/2 and sin216 = -sin144:
   Re = c0 + c1 (r5 - 1)/4 - (c2 + c3)(r5 + 1)/4,     Im = sin72 * ( c1 + (c2 - c3)(r5 - 1)/2 ).
Scaling the y-axis by sin72 > 0 keeps orientation signs, so orientations are computed exactly in Q(r5) on
(Re, Im / sin72).  Cross-checked against the repository's verify5.py formula on all triples.
"""
import sys, itertools
from fractions import Fraction as F


class Q5:
    __slots__ = ("a", "b")  # a + b*sqrt5

    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(s, o):
        return Q5(s.a + o.a, s.b + o.b)

    def __sub__(s, o):
        return Q5(s.a - o.a, s.b - o.b)

    def __mul__(s, o):
        return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)

    def sign(s):
        a, b = s.a, s.b
        if a >= 0 and b >= 0:
            return int(a > 0 or b > 0)
        if a <= 0 and b <= 0:
            return -int(a < 0 or b < 0)
        # opposite signs: compare a^2 with 5 b^2
        d = a * a - 5 * b * b
        return (1 if d > 0 else -1 if d < 0 else 0) * (1 if a > 0 else -1)


def to_xy(c):
    c0, c1, c2, c3 = c
    X = Q5(c0) + Q5(F(-1, 4), F(1, 4)) * Q5(c1) - Q5(F(1, 4), F(1, 4)) * Q5(c2 + c3)
    Y = Q5(c1) + Q5(F(-1, 2), F(1, 2)) * Q5(c2 - c3)
    return X, Y


def orient_q5(p, q, r):
    return ((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])).sign()


# repository formula (verify5.py), re-typed for the cross-check
def sgn5(A, B):
    if A >= 0 and B >= 0: return int(A > 0 or B > 0)
    if A <= 0 and B <= 0: return -int(A < 0 or B < 0)
    a2, b2 = A * A, 5 * B * B
    return (1 if a2 > b2 else -1 if a2 < b2 else 0) * (1 if A > 0 else -1)


def norm(c):
    c = list(c) + [0] * (5 - len(c)); return tuple(x - c[4] for x in c[:4]) + (0,)


def mul(u, v):
    w = [0] * 5
    for a in range(5):
        for b in range(5): w[(a + b) % 5] += u[a] * v[b]
    return w


def conj(u): return [u[(-j) % 5] for j in range(5)]


def orient_repo(p, q, r):
    u = [q[t] - p[t] for t in range(5)]; v = [r[t] - p[t] for t in range(5)]
    w = mul(conj(u), v)
    return sgn5(2 * (w[1] - w[4]) - (w[2] - w[3]), w[2] - w[3])


def main():
    for fn in sys.argv[1:]:
        C = [tuple(int(t) for t in l.split()[:4]) for l in open(fn) if l.strip() and not l.startswith(("FOUND", "#"))]
        XY = [to_xy(c) for c in C]
        N5 = [norm(list(c)) for c in C]
        n = len(C)
        S = [[[0] * n for _ in range(n)] for _ in range(n)]
        mism = 0
        for i, j, k in itertools.permutations(range(n), 3):
            s = orient_q5(XY[i], XY[j], XY[k])
            S[i][j][k] = s
            if i < j < k and s != orient_repo(N5[i], N5[j], N5[k]):
                mism += 1
        gp = all(S[i][j][k] != 0 for i, j, k in itertools.combinations(range(n), 3))
        # backtracking enumeration of one-sided partitions (same logic as backtrack_onesided.py)
        side = [None] * n
        sols = []

        def consistent(m):
            X = [i for i in range(m + 1) if side[i] == side[m]]
            Y = [i for i in range(m + 1) if side[i] != side[m]]
            for x in X:
                if x == m:
                    continue
                ss = {S[m][x][y] for y in Y}
                if 0 in ss or len(ss) > 1:
                    return False
            for y, y2 in itertools.combinations(Y, 2):
                ss = {S[y][y2][x] for x in X}
                if 0 in ss or len(ss) > 1:
                    return False
            return True

        def rec(m):
            if m == n:
                a = sum(1 for s in side if s)
                if a >= 2 and n - a >= 2:
                    sols.append(sorted(i for i in range(n) if side[i]))
                return
            for val in (True, False):
                side[m] = val
                if consistent(m):
                    rec(m + 1)
                side[m] = None

        rec(0)
        print(f"{fn.rsplit('/', 1)[-1]}: n={n} general_position={gp} "
              f"orientation mismatches vs verify5 formula={mism} one-sided partitions (|A|,|B|>=2)={len(sols)}")
        for A in sols:
            print("    A =", A)


if __name__ == "__main__":
    main()

"""Exact arithmetic in Q(sqrt3): x = a + b*sqrt3 with a, b Fractions (reviewer code)."""
from fractions import Fraction as F


class Q3:
    __slots__ = ('a', 'b')

    def __init__(self, a=0, b=0):
        self.a = F(a)
        self.b = F(b)

    def __add__(s, o):
        o = q(o); return Q3(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __neg__(s):
        return Q3(-s.a, -s.b)

    def __sub__(s, o):
        o = q(o); return Q3(s.a - o.a, s.b - o.b)

    def __rsub__(s, o):
        return q(o) - s

    def __mul__(s, o):
        o = q(o); return Q3(s.a * o.a + 3 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - 3 * s.b * s.b      # nonzero for nonzero s (sqrt3 irrational)
        if n == 0:
            raise ZeroDivisionError
        return Q3(s.a / n, -s.b / n)

    def __truediv__(s, o):
        return s * q(o).inv()

    def sign(s):
        a, b = s.a, s.b
        sa = (a > 0) - (a < 0)
        sb = (b > 0) - (b < 0)
        if sa == 0:
            return sb
        if sb == 0 or sa == sb:
            return sa
        # opposite signs: compare a^2 with 3 b^2
        d = a * a - 3 * b * b
        return sa if d > 0 else -sa      # d != 0 since sqrt3 is irrational

    def iszero(s):
        return s.a == 0 and s.b == 0

    def __eq__(s, o):
        o = q(o); return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __float__(s):
        return float(s.a) + float(s.b) * 3 ** 0.5

    def __repr__(s):
        return 'Q3(%s,%s)' % (s.a, s.b)


def q(x):
    return x if isinstance(x, Q3) else Q3(x, 0)


SQ3 = Q3(0, 1)
HALF = Q3(F(1, 2), 0)


def cos30(k):
    """cos(30 k degrees) exactly"""
    k %= 12
    tab = [Q3(1), Q3(0, F(1, 2)), Q3(F(1, 2)), Q3(0), Q3(F(-1, 2)), Q3(0, F(-1, 2)),
           Q3(-1), Q3(0, F(-1, 2)), Q3(F(-1, 2)), Q3(0), Q3(F(1, 2)), Q3(0, F(1, 2))]
    return tab[k]


def sin30(k):
    return cos30(k - 3)


def _selftest():
    import math, random
    for k in range(-24, 25):
        assert abs(float(cos30(k)) - math.cos(math.radians(30 * k))) < 1e-12
        assert abs(float(sin30(k)) - math.sin(math.radians(30 * k))) < 1e-12
    random.seed(1)
    for _ in range(20000):
        a = F(random.randint(-50, 50), random.randint(1, 9)); b = F(random.randint(-50, 50), random.randint(1, 9))
        x = Q3(a, b); v = float(a) + float(b) * math.sqrt(3)
        if abs(v) > 1e-9:
            assert x.sign() == (1 if v > 0 else -1), (a, b)
        elif not x.iszero():
            raise AssertionError
    return True


if __name__ == '__main__':
    print('q3 selftest', _selftest())

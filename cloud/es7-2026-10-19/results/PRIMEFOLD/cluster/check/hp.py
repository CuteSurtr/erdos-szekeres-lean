"""Tiny high-precision helpers (Decimal), written for the TE verification: cos/sin of rational multiples of pi.
Error of the series is far below 10^-70 at the working precision of 90 digits; callers check margins >= 10^-40."""
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

getcontext().prec = 90
PI = Decimal('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651')


def _sincos(x):
    # reduce to |x| <= pi
    twopi = 2 * PI
    x = x % twopi
    if x > PI:
        x -= twopi
    s = Decimal(0)
    c = Decimal(0)
    term = Decimal(1)   # x^k / k!
    k = 0
    while True:
        if k % 4 == 0:
            c += term
        elif k % 4 == 1:
            s += term
        elif k % 4 == 2:
            c -= term
        else:
            s -= term
        k += 1
        term = term * x / k
        if abs(term) < Decimal(10) ** -100 and k > 5:
            break
    return s, c


def unit_at_pi_multiple(q):
    """(cos(q*pi), sin(q*pi)) as Decimals, q a Fraction."""
    s, c = _sincos(PI * Decimal(q.numerator) / Decimal(q.denominator))
    return c, s


def dec(x):
    """Fraction or int -> Decimal."""
    if isinstance(x, Fr):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)

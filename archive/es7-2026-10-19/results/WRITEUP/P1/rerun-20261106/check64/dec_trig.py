"""High-precision cos/sin(2 pi j/7) with the decimal module (independent of the algebraic bracket)."""
from decimal import Decimal, getcontext

def setup(dps=110):
    getcontext().prec = dps + 10

def arctan_inv(x):
    # arctan(1/x) for integer x > 1 by Taylor series
    x = Decimal(x); x2 = x * x
    term = 1 / x; s = term; k = 1
    eps = Decimal(10) ** (-(getcontext().prec + 2))
    while True:
        term = -term / x2
        k += 2
        d = term / k
        if abs(d) < eps:
            break
        s += d
    return s

def pi():
    # Machin: pi/4 = 4 arctan(1/5) - arctan(1/239)
    return 4 * (4 * arctan_inv(5) - arctan_inv(239))

def cos_sin(a):
    eps = Decimal(10) ** (-(getcontext().prec + 2))
    # Taylor series (a is at most ~6.3; fine at this precision)
    c = Decimal(0); s = Decimal(0)
    term = Decimal(1); k = 0
    while True:
        if k % 4 == 0: c += term
        elif k % 4 == 1: s += term
        elif k % 4 == 2: c -= term
        else: s -= term
        k += 1
        term = term * a / k
        if abs(term) < eps and k > 10:
            break
    return c, s

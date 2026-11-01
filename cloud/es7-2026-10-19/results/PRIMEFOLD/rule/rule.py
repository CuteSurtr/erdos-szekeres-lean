"""Explicit rule (recursive max/min construction in the simplified classes model) -> tree with numeric angles.
Angles are exact Fractions (units pi/p measured from the tangent direction at X_0)."""
import sys, functools
from fractions import Fraction as F
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from recdp import solve
def build(desc, A, B):
    """desc: 'o' or ('max'|'min', k, Ldesc, Rdesc); (A, B): open interval of allowed angles. Returns nested (L, R, angle)."""
    if desc == 'o': return None
    kind, k, Ld, Rd = desc
    lo, hi = max(A, F(k)), min(B, F(k + 1))
    assert lo < hi, (desc, A, B)
    if kind == 'max':
        th = hi - (hi - lo) / 4
        return (build(Ld, A, th), build(Rd, A, th), th)
    else:
        th = lo + (hi - lo) / 4
        return (build(Ld, th, B), build(Rd, th, B), th)
def rule_tree(h):
    v, desc = solve(h)
    T = build(desc, F(1), F(2 * h + 1, 2))    # classes 1..h; last class only up to the radial direction (angle p/2 = h + 1/2)
    return v, desc, T
def fmt(T):
    if T is None: return 'o'
    return '(' + fmt(T[0]) + ' ' + fmt(T[1]) + ' %.15f)' % float(T[2])
def leaves(T): return 1 if T is None else leaves(T[0]) + leaves(T[1])
if __name__ == '__main__':
    h = int(sys.argv[1])
    v, desc, T = rule_tree(h)
    print('h=%d size %d leaves %d' % (h, v, leaves(T)))
    print(fmt(T))

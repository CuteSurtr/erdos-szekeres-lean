#!/usr/bin/env python3
"""CATALAN20261110: checks of the count (Python standard library only; imports PRIMEFOLD/rule/recdp.py unchanged).
 1. The recursion F(h,a) = F(h,a-1) + F(h-1,min(a,h)), F(h,1) = F(1,a) = 1, equals the value of the classes-model DP
    of recdp.py at the state (u0, w0 with w1 = a, [1,h]) for every h <= 5 and 1 <= a <= h+1.
 2. F(h,h+1) equals recdp.solve(h) for h <= 6.
 3. F(h,a) = C(h+a-2,a-1) - C(h+a-2,a-4) for h <= 200, 1 <= a <= h+1 (proved for all h in the README).
 4. F(h,h+1) = Cat(h+1) - Cat(h) = C(2h,h-1) - C(2h,h-2) for h < 300.
 5. Whether recdp's own optimal tree is the F-tree (it is not for h >= 2: other tie-breaking, same size)."""
import os, sys, functools
from math import comb
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'PRIMEFOLD', 'rule'))
from recdp import solve
sys.setrecursionlimit(10000)
def C(n, k): return comb(n, k) if 0 <= k <= n else 0
def cat(n): return comb(2 * n, n) // (n + 1)
@functools.lru_cache(None)
def F(h, a): return 1 if h == 1 or a == 1 else F(h, a - 1) + F(h - 1, min(a, h))
def dp_value(h, a):
    """recdp.N, copied verbatim except that the start state has w1 = a"""
    @functools.lru_cache(maxsize=None)
    def N(u, w, lo, hi):
        if min(u) < 1 or min(w) < 1: return 0
        best = 1
        for k in range(lo, hi + 1):
            if any(u[e - 2] < 2 for e in range(k + 1, h + 2)) or any(w[s - 1] < 2 for s in range(1, k + 1)): continue
            uk = tuple(u[e - 2] - (1 if e > k else 0) for e in range(2, h + 2))
            wk = tuple(w[s - 1] - (1 if s <= k else 0) for s in range(1, h + 1))
            x, y = N(uk, w, lo, k), N(u, wk, lo, k)
            if x and y: best = max(best, x + y)
            x, y = N(u, wk, k, hi), N(uk, w, k, hi)
            if x and y: best = max(best, x + y)
        return best
    u0 = tuple(min(e, h) for e in range(2, h + 2)); w0 = (a,) + tuple(h + 2 - s for s in range(2, h + 1))
    return N(u0, w0, 1, h)
def ftree(h, a, c):
    if h == 1 or a == 1: return 'o'
    return ('min', c, ftree(h, a - 1, c), ftree(h - 1, min(a, h), c + 1))
ok = True
r1 = all(dp_value(h, a) == F(h, a) for h in range(1, 6) for a in range(1, h + 2)); ok &= r1
print('1. recursion == DP value for h <= 5, 1 <= a <= h+1:', r1)
r2 = all(solve(h)[0] == F(h, h + 1) for h in range(1, 7)); ok &= r2
print('2. F(h,h+1) == recdp.solve(h) for h <= 6:', r2)
r3 = all(F(h, a) == C(h + a - 2, a - 1) - C(h + a - 2, a - 4) for h in range(1, 201) for a in range(1, h + 2)); ok &= r3
print('3. closed form C(h+a-2,a-1) - C(h+a-2,a-4) for h <= 200:', r3)
r4 = all(F(h, h + 1) == cat(h + 1) - cat(h) == C(2 * h, h - 1) - C(2 * h, h - 2) for h in range(1, 300)); ok &= r4
print('4. F(h,h+1) == Cat(h+1)-Cat(h) == C(2h,h-1)-C(2h,h-2) for h < 300:', r4)
print('5. recdp optimal tree is the F-tree:', {h: solve(h)[1] == ftree(h, h + 1, 1) for h in range(1, 7)})
for h in range(1, 9): print('   F(%d, 1..%d) =' % (h, h + 1), [F(h, a) for a in range(1, h + 2)])
print('   m*B(h)+1 vs 2^(m-1):', [(2 * h + 1, (2 * h + 1) * F(h, h + 1) + 1, 2 ** (2 * h)) for h in range(1, 9)])
print('ALL OK' if ok else 'FAIL'); sys.exit(0 if ok else 1)

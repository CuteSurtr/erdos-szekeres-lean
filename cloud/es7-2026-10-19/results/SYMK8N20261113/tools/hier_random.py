#!/usr/bin/env python3
"""Random check of Theorem H: s generic scale-separated squares (random directions), largest convex subset vs s + 2."""
import sys, os, random, ctypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import double_exact as DE
DE.LIB = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libpolyeval2.so'))
DE.LIB.poly_eval.restype = ctypes.c_int
DE.LIB.poly_eval.argtypes = [ctypes.c_int] + [ctypes.c_void_p] * 5 + [ctypes.c_int, ctypes.c_void_p]
from double_exact import peval
random.seed(5)
for s in range(2, 11):
    hist = {}
    for _ in range(300 if s <= 8 else 100):
        pts = []
        for j in range(s):
            x, y = random.randint(-10**6, 10**6), random.randint(-10**6, 10**6)
            q = (x, y)
            for _ in range(4):
                pts.append([(j, q[0], q[1])]); q = (-q[1], q[0])
        ml, cnt, nz = peval(pts, 3)
        if nz:
            continue
        hist[ml] = hist.get(ml, 0) + 1
    print('s=%d: largest convex subset histogram %s (Theorem H bound s+2 = %d)' % (s, dict(sorted(hist.items())), s + 2), flush=True)

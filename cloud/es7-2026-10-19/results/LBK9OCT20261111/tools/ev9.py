"""ctypes wrapper: count convex K-gons of an 8-fold layered float configuration (search only)."""
import ctypes, os, math
import numpy as np
_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libcnt9.so'))
_lib.countk.restype = ctypes.c_longlong
_lib.countk.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int,
                        ctypes.POINTER(ctypes.c_double)]
def points(lr, th, m=8):
    X = []; Y = []
    for a, b in zip(lr, th):
        r = math.exp(a)
        for k in range(m):
            X.append(r * math.cos(b + 2 * math.pi * k / m)); Y.append(r * math.sin(b + 2 * math.pi * k / m))
    return np.array(X), np.array(Y)
def count(X, Y, K=9):
    X = np.ascontiguousarray(X, dtype=np.float64); Y = np.ascontiguousarray(Y, dtype=np.float64)
    md = ctypes.c_double(0)
    c = _lib.countk(len(X), X.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), Y.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), K, ctypes.byref(md))
    return c, md.value
def count_cfg(lr, th, K=9):
    X, Y = points(lr, th); return count(X, Y, K)

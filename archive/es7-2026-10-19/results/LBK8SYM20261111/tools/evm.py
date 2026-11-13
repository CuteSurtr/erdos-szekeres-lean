"""ctypes wrapper of src/libcvxm.so (float evaluator for m-fold configurations; evidence only)."""
import ctypes, os, numpy as np
_here = os.path.dirname(os.path.abspath(__file__))
_lib = ctypes.CDLL(os.path.join(_here, '..', 'src', 'libcvxm.so'))
_dp = ctypes.POINTER(ctypes.c_double)
_up = ctypes.POINTER(ctypes.c_ulonglong)
_lib.cvx_count.argtypes = [ctypes.c_int, _dp, _dp, _up, ctypes.c_ulonglong]
_lib.cvx_evalm.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, _dp, _dp, _up, ctypes.c_ulonglong]
_lib.m_points.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, _dp, _dp, _dp, _dp]
_lib.min_sine.argtypes = [ctypes.c_int, _dp, _dp]
_lib.min_sine.restype = ctypes.c_double
KMAX = 8


def count_xy(x, y, abort=0):
    x = np.ascontiguousarray(x, dtype=np.float64); y = np.ascontiguousarray(y, dtype=np.float64)
    c = (ctypes.c_ulonglong * (KMAX + 1))()
    r = _lib.cvx_count(len(x), x.ctypes.data_as(_dp), y.ctypes.data_as(_dp), c, abort)
    return list(c), r


def countm(m, lr, th, centre=0, abort=0):
    lr = np.ascontiguousarray(lr, dtype=np.float64); th = np.ascontiguousarray(th, dtype=np.float64)
    c = (ctypes.c_ulonglong * (KMAX + 1))()
    r = _lib.cvx_evalm(m, len(lr), int(centre), lr.ctypes.data_as(_dp), th.ctypes.data_as(_dp), c, abort)
    return list(c), r


def pointsm(m, lr, th, centre=0):
    lr = np.ascontiguousarray(lr, dtype=np.float64); th = np.ascontiguousarray(th, dtype=np.float64)
    n = m * len(lr) + int(centre)
    x = np.zeros(n); y = np.zeros(n)
    _lib.m_points(m, len(lr), int(centre), lr.ctypes.data_as(_dp), th.ctypes.data_as(_dp),
                  x.ctypes.data_as(_dp), y.ctypes.data_as(_dp))
    return x, y


def min_sine(x, y):
    x = np.ascontiguousarray(x, dtype=np.float64); y = np.ascontiguousarray(y, dtype=np.float64)
    return _lib.min_sine(len(x), x.ctypes.data_as(_dp), y.ctypes.data_as(_dp))


_le = ctypes.CDLL(os.path.join(_here, '..', 'src', 'libenumk.so'))
_ip = ctypes.POINTER(ctypes.c_int)
_le.enum_k.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_int, _ip, ctypes.c_int]


def enum_k(x, y, K=8, maxout=200000):
    x = np.ascontiguousarray(x, dtype=np.float64); y = np.ascontiguousarray(y, dtype=np.float64)
    out = np.zeros(maxout * K, dtype=np.int32)
    tot = _le.enum_k(len(x), x.ctypes.data_as(_dp), y.ctypes.data_as(_dp), K, out.ctypes.data_as(_ip), maxout)
    return tot, out[:min(tot, maxout) * K].reshape(-1, K)

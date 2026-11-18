"""Fast exact in-state computation (numpy) for annealing."""
import numpy as np
import fl
from esgeo import Analysis
POW = np.array([1, 5, 25, 125])
CODE2IDX = {sum(f[i] * 5**i for i in range(4)): k for k, f in enumerate(fl.STATES)}
def instates(P):
    """returns None if invalid (not general position / 6-cap / 6-cup / octagon); else (list of state idx, Analysis)."""
    try:
        A = Analysis(P)
    except ValueError:
        return None
    n = A.n
    if n < 2: return ([0] * n, A)
    if A.capB.max() > 5 or A.cupB.max() > 5 or (A.capB + A.cupB).max() - 2 > 7: return None
    code = np.zeros(n, dtype=np.int64)
    cm1 = A.cupE - 1
    for a in range(1, 5):
        fa = np.where(A.capE >= a + 1, cm1, 0).max(axis=0)
        code += fa * 5**(a - 1)
    return ([CODE2IDX[int(c)] for c in code], A)

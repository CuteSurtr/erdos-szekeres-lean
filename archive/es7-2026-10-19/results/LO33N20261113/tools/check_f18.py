"""Exact check of the identity behind h(F) >= 18 (RES33N Result 2): nine Baek block rows, each with 28 states
inside F and demand 6, cover every F-state exactly 3 times.  Hence 3 h(F) = sum of the nine rows >= 54."""
from lo_common import *
idx = [973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315]
cov = {i: 0 for i in F}
for r in idx:
    s, d = ROWS[r]; assert d == 6 and len(s) == 28 and set(s) <= set(F), (r, d, len(s))
    for i in s: cov[i] += 1
assert set(cov.values()) == {3}
print('OK: nine rows', idx, 'demand 6 each, every F-state covered exactly 3 times => 3 h(F) >= 54, h(F) >= 18')

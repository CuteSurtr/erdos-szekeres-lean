#!/usr/bin/env python3
"""Mutation control: weaken R(i,m) by dropping the edge-line condition at a (or at b) and confirm that
the U1 check of universal_test.py then reports violations (so the test is not vacuous)."""
import sys, importlib.util
spec = importlib.util.spec_from_file_location("ut", sys.argv[1])
ut = importlib.util.module_from_spec(spec); spec.loader.exec_module(ut)
which = sys.argv[2]
orient = ut.orient
def region_pred(H, i, m):
    a, b = H[i], H[(i + m + 1) % 6]
    hm1, hb1 = H[(i - 1) % 6], H[(i + m + 2) % 6]
    if which == "drop_a":
        return a, b, (lambda p: orient(a, b, p) < 0 and orient(b, hb1, p) > 0)
    if which == "drop_b":
        return a, b, (lambda p: orient(a, b, p) < 0 and orient(hm1, a, p) > 0)
    raise SystemExit("bad mode")
ut.region_pred = region_pred
sys.argv = [sys.argv[0], "5", "3000"]
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    ut.main()
lines = buf.getvalue().splitlines()
print(which, "violation lines:", sum(1 for l in lines if l.startswith("U1 VIOLATION")), "|", lines[-1][:200])

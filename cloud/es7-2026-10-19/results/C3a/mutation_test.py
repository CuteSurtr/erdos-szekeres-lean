#!/usr/bin/env python3
"""Sensitivity check of validate.py: deliberately broken variants of c3cnf must FAIL validation."""
import json
import sys
import c3cnf
import validate

orig_init, orig_sig, orig_ccw, orig_build = c3cnf.C3Enc.__init__, c3cnf.C3Enc.sig, c3cnf.C3Enc.ccw, c3cnf.C3Enc.build


def wrong_eps(self, m, k, sb=True):
    n = 3 * m
    old = c3cnf.C3Enc._orbits
    c3cnf.C3Enc._orbits = lambda s, trip, f: old(s, trip, lambda t, Rt: 1)
    try:
        orig_init(self, m, k, sb)
    finally:
        c3cnf.C3Enc._orbits = old


def wrong_sigma(self, i):
    return self.s[i % self.m]


def off_by_one(self, m, k, sb=True):  # forbids (k+1)-gons instead of k-gons
    orig_init(self, m, k + 1, sb)


MUT = {"wrong_eps": ("__init__", wrong_eps), "wrong_sigma": ("sig", wrong_sigma), "off_by_one": ("__init__", off_by_one)}
name, M, K, NS, seed = sys.argv[1], *map(int, sys.argv[2:6])
attr, f = MUT[name]
setattr(c3cnf.C3Enc, attr, f)
validate.C3Enc = c3cnf.C3Enc
sys.argv = ["validate.py", str(M), str(K), str(NS), str(seed)]
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    try:
        validate.main()
        out = json.loads(buf.getvalue())
        res = {"mutation": name, "m": M, "k": K, "sets": out["sets"], "failed_sets": len(out["fail"])}
    except AssertionError as ex:
        res = {"mutation": name, "m": M, "k": K, "assertion_failed": str(ex)[:80]}
print(json.dumps(res))

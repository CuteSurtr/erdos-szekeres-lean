#!/usr/bin/env python3
"""Per-case projected model sets of C3a and C3b must be identical.
Projection: (chi_S on every sorted triple, sigma_0..sigma_{m-1}); all projected models are
enumerated with blocking clauses (pysat cadical195).  usage: projcount.py m k [MAXMODELS]"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pysat.solvers import Solver  # noqa: E402
from gen_case import build  # noqa: E402
from hullcase import cases, case_name  # noqa: E402


def models(e, enc, m, cap):
    cls = e.clauses if enc == "c3a" else e.cls
    n = 3 * m
    trip = list(itertools.combinations(range(n), 3))
    if enc == "c3a":
        proj = [e.ccw(*t) for t in trip] + [e.s[r] for r in range(m)]
    else:
        proj = [e.chis(*t) for t in trip] + [e.s[r] for r in range(m)]
    keyvars = sorted({abs(l) for l in proj})
    out = set()
    with Solver(name="cadical195", bootstrap_with=cls) as S:
        while S.solve():
            md = S.get_model()
            val = {abs(x): x > 0 for x in md}
            key = tuple((val[abs(l)] if l > 0 else not val[abs(l)]) for l in proj)
            out.add(key)
            S.add_clause([-v if val[v] else v for v in keyvars])
            if len(out) >= cap:
                return out, False
    return out, True


def main():
    m, k = int(sys.argv[1]), int(sys.argv[2])
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 200000
    for c in ["none"] + [case_name(x) for x in cases(m, k)]:
        A, ca = models(build(m, k, c, "c3a"), "c3a", m, cap)
        B, cb = models(build(m, k, c, "c3b"), "c3b", m, cap)
        print(json.dumps({"m": m, "k": k, "case": c, "c3a_models": len(A), "c3b_models": len(B), "complete": ca and cb,
                          "identical": A == B}), flush=True)


if __name__ == "__main__":
    main()

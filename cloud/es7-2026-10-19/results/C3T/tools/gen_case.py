#!/usr/bin/env python3
"""C3-S case CNF: the C3a (default) or C3b encoding plus the hull-case clauses of hullcase.py.
usage: gen_case.py m k CASE -o out.cnf [--enc c3a|c3b] [--gon chain|conv]   (CASE: H3, H6a<a>s<s>, a layer name such as 0s0_3s0-7s1, or none)"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3b", "tools"))
sys.path.insert(0, HERE)
from hullcase import hull_clauses, parse_case, layer_clauses, parse_layers  # noqa: E402


def case_clauses(m, case, ccw, sig_true):
    if case == "H3" or case.startswith("H6"):
        return hull_clauses(m, parse_case(case), ccw, sig_true)
    return layer_clauses(m, parse_layers(case), ccw, sig_true)


def build(m, k, case, enc="c3a", gon="chain"):
    if enc == "c3a":
        from c3cnf import C3Enc
        e = C3Enc(m, k, gon=gon)
        e.build()
        if case != "none":
            st = len(e.clauses)
            for c in case_clauses(m, case, e.ccw, e.sig):
                e.add(c)
            e.section("hull", st)
    else:
        assert gon == "chain"
        from gen_c3b import Enc
        e = Enc(m, k)
        e.build()
        if case != "none":
            def sig_true(i):
                v, f = e.sig(i)
                return -v if f else v
            a = len(e.cls)
            for c in case_clauses(m, case, e.chis, sig_true):
                e.add(c)
            e.groups.append(("HULL", a, len(e.cls) - a))
    return e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("k", type=int)
    ap.add_argument("case")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--map")
    ap.add_argument("--enc", choices=["c3a", "c3b"], default="c3a")
    ap.add_argument("--gon", choices=["chain", "conv"], default="chain")
    a = ap.parse_args()
    e = build(a.m, a.k, a.case, a.enc, a.gon)
    info = e.write(a.out, a.map)
    info["case"], info["enc"] = a.case, a.enc
    print(json.dumps({k: v for k, v in info.items() if k not in ("sections", "groups", "patterns")}))


if __name__ == "__main__":
    main()

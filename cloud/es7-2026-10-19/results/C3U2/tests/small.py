#!/usr/bin/env python3
"""Run close_tree.py or compose.py of results/C3U/tools on a small instance (m, k) instead of the
hard-coded (11, 7).  Like results/C3T/tests/small.py: the tool is imported unchanged and only its
module-level (m, k) bindings are rebound: C3Enc, layer_clauses, tree_children, E (as C3T), plus the
C3U constants M, KC of close_tree and M, K of compose; for compose also BASE_SHA := sha256 of the
small BASE given on the command line (the m = 11 base is pinned in the tool).
usage: small.py TOOLSDIR m k close_tree BASE OUT.jsonl ROOT [close_tree options]
       small.py TOOLSDIR m k compose BASE RESULTS.jsonl [...] [compose options]"""
import hashlib, importlib, os, sys

tools, m, k, which = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, os.path.join(tools, "..", "..", "C3a"))
sys.path.insert(0, tools)
import hullcase  # noqa: E402
from c3cnf import C3Enc  # noqa: E402

mod = importlib.import_module(which)
mod.C3Enc = lambda _m, _k, **kw: C3Enc(m, k, **kw)
mod.layer_clauses = lambda _m, L, ccw, sig: hullcase.layer_clauses(m, L, ccw, sig)
if hasattr(mod, "tree_children"):
    mod.tree_children = lambda _m, _k, L, **kw: hullcase.tree_children(m, k, L, **kw)
if hasattr(mod, "E"):
    mod.E = C3Enc(m, k)
if which == "close_tree" and hasattr(mod, "KC"):
    mod.M, mod.KC = m, k
    mod.WORK = os.environ.get("C3U_WORK", "/opt/work/small_ct")  # apart from the m = 11 runs
if which == "compose":
    mod.M, mod.K = m, k
    mod.BASE_SHA = hashlib.sha256(open(sys.argv[5], "rb").read()).hexdigest()
sys.argv = [which + ".py"] + sys.argv[5:]
mod.main()

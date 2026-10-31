#!/usr/bin/env python3
"""Run close_node.py / close_tree.py of a tools directory (old results/C3-S/tools or new
results/C3T/tools) on a small instance (m, k) instead of the hard-coded (11, 7).

The tools hard-code m = 11, k = 7 (C3Enc(11, 7), layer_clauses(11, ...), tree_children(11, 7, ...)).
This wrapper imports the tool unchanged and rebinds only those three names in the tool's module
to the same functions with (m, k) fixed; nothing else of the tool is touched.  close_tree's
ProcessPoolExecutor forks, so the workers inherit the rebinding.
usage: small.py TOOLSDIR m k close_node BASE OUT.jsonl CAP NODE [NODE ...]
       small.py TOOLSDIR m k close_tree BASE OUT.jsonl ROOT [close_tree options]"""
import importlib, os, sys

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
sys.argv = [which + ".py"] + sys.argv[5:]
mod.main()

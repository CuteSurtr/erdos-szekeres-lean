"""C3AUDIT4: close_tree.py restart / childless tests with a fake solver (no CaDiCaL): close_tree is imported
unchanged at (m, k) = (5, 6) with its module bindings rebound as C3U2/tests/small.py does, and its `solve` is
replaced by a stub that answers UNSATISFIABLE + certified for names in CERT (a predicate) and UNKNOWN otherwise.
usage: ct_test.py TOOLSDIR SCENARIO OUT.jsonl"""
import hashlib, importlib, json, os, sys
tools, scen, out = sys.argv[1], sys.argv[2], sys.argv[3]
m, k = 5, 6
sys.path.insert(0, os.path.join(tools, "..", "..", "C3a")); sys.path.insert(0, tools)
import hullcase  # noqa
from c3cnf import C3Enc  # noqa
ct = importlib.import_module("close_tree")
ct.C3Enc = lambda _m, _k, **kw: C3Enc(m, k, **kw)
ct.layer_clauses = lambda _m, L, ccw, sig: hullcase.layer_clauses(m, L, ccw, sig)
ct.tree_children = lambda _m, _k, L, **kw: hullcase.tree_children(m, k, L, **kw)
ct.E = C3Enc(m, k); ct.M, ct.KC = m, k
ct.WORK = os.path.join(os.path.dirname(out), "wk")
BASE = "/tmp/claude-0/-home-user-erdos-szekeres-lean/a2372e58-e319-59b7-94d3-805904fed989/scratchpad/base/b56.cnf"
P = "0s0_1s0-2s0"
CERTP = {
    # T1: P itself times out; every proper descendant closes
    "T1": lambda n: n != P,
    # T2: nothing closes above 4 layers; fully layered (4+ layers here) nodes time out too
    "T2": lambda n: False,
    # T3: everything closes
    "T3": lambda n: True,
}[scen]


def fake(args):
    base, node, cap, modeldir, opts = args
    if CERTP(node):
        return {"node": node, "status": "UNSATISFIABLE", "certified": True, "lrat_check": "c VERIFIED",
                "cake_lpr": "s VERIFIED UNSAT", "cnf_sha256": "stub", "solve_s": 0}
    return {"node": node, "status": "UNKNOWN", "solve_s": 0}


ct.solve = fake
pre = {
    "T1": [{"node": P, "cube": {"3": 0}, "certified": True, "status": "UNSATISFIABLE", "lrat_check": "c VERIFIED",
            "cake_lpr": "s VERIFIED UNSAT", "cnf_sha256": "stub"}],
    "T2": [],
    "T3": [{"node": "0s0_1s0-2s0_3_4", "split": True, "children": 0}],
}[scen]
open(out, "w").write("".join(json.dumps(r) + "\n" for r in pre))
root = {"T1": P, "T2": P, "T3": "0s0_1s0-2s0_3_4"}[scen]
sys.argv = ["close_tree.py", BASE, out, root, "--jobs", "1", "--caps", "1"]
ct.main()

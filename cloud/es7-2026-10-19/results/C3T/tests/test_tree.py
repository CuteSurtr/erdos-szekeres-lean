#!/usr/bin/env python3
"""Structural tests of results/C3T/tools/hullcase.py and compose.py against results/C3-S/tools.
1. mirror_h6 off (default): tree_children equals the old one on every node up to depth 2 and on
   a sample of depth-3 nodes, for (m, k) in (7, 7), (9, 7), (11, 7), (6, 6); layer_clauses equal
   on all those nodes (same functions, checked anyway).
2. mirror_h6 on, m = 11: for every H6(a, s): phi is an involution on the 153 layer-2 options,
   maps options to options, equals phi of results/C3PLAN/scripts/validate_mirror_h6.py, and
   81 options are kept (5 one-orbit, 9 self-mirror), as PLAN.md 3a says; H3 and deeper nodes are
   unchanged.  Also m = 7, 9.
3. compose.node_sha_cached equals compose.node_sha on 300 random nodes (m = 11 base)."""
import hashlib, importlib.util, os, random, sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
R = os.path.join(R, "es7-2026-10-19") if not os.path.isdir(os.path.join(R, "results")) else R


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


old = load(os.path.join(R, "results/C3-S/tools/hullcase.py"), "hull_old")
new = load(os.path.join(R, "results/C3T/tools/hullcase.py"), "hull_new")
sys.path.insert(0, os.path.join(R, "results/C3a"))
from c3cnf import C3Enc  # noqa: E402

fails = 0
rng = random.Random(1)
for m, k in ((7, 7), (9, 7), (11, 7), (6, 6)):
    E = C3Enc(m, k)
    nodes, cnt = [[]], 0
    lvl = [[]]
    for d in range(3):
        nxt = []
        for L in lvl:
            a, b = old.tree_children(m, k, L), new.tree_children(m, k, L)
            b2 = new.tree_children(m, k, L, mirror=True, mirror_h6=False)
            cnt += 1
            if a != b or a != b2:
                fails += 1
                print("DIFF", m, k, L)
            nxt += a
        lvl = nxt if d < 1 else rng.sample(nxt, min(400, len(nxt)))
        nodes += lvl
    ncl = 0
    for L in rng.sample(nodes[1:], min(300, len(nodes) - 1)):
        if old.layer_clauses(m, L, E.ccw, E.sig) != new.layer_clauses(m, L, E.ccw, E.sig):
            fails += 1
            print("CLAUSE DIFF", m, k, L)
        ncl += 1
    print(f"off: m={m} k={k}: tree_children compared on {cnt} nodes, layer_clauses on {ncl} nodes")

# validate_mirror_h6.py imports geometry helpers at module level; take its phi source text only
src = open(os.path.join(R, "results/C3PLAN/scripts/validate_mirror_h6.py")).read()
i = src.index("def phi(")
ns = {}
exec(src[i:src.index("\ndef ", i + 1)], ns)
plan_phi = ns["phi"]
key = lambda L: tuple((r, -1 if s is None else s) for r, s in sorted(L, key=lambda x: (x[0], -1 if x[1] is None else x[1])))
for m in (7, 9, 11):
    for a in range(1, m // 2 + 1):
        for s in (0, 1):
            top = [[(0, 0), (a, s)]]
            opts = new.layer2_options(m, top[0])
            oset = {key(o) for o in opts}
            ok_inv = all(key(new.h6_phi(m, a, s, new.h6_phi(m, a, s, o))) == key(o) for o in opts)
            ok_map = all(key(new.h6_phi(m, a, s, o)) in oset for o in opts)
            ok_plan = all(key(new.h6_phi(m, a, s, o)) == key(plan_phi(m, a, s, o)) for o in opts)
            kept = new.tree_children(m, 7, top, mirror_h6=True)
            ch_off = new.tree_children(m, 7, top)
            kk = [c[-1] for c in kept]
            selfm = sum(key(new.h6_phi(m, a, s, o)) == key(o) for o in opts)
            # cover: every option is kept or its image is kept
            kset = {key(o) for o in kk}
            ok_cov = all(key(o) in kset or key(new.h6_phi(m, a, s, o)) in kset for o in opts)
            line = (f"on: m={m} H6({a},{s}): options {len(opts)} kept {len(kk)} one-orbit {sum(len(o) == 1 for o in kk)} "
                    f"self-mirror {selfm} involution {ok_inv} maps-to-options {ok_map} equals-PLAN-phi {ok_plan} cover {ok_cov} "
                    f"off-children {len(ch_off)}")
            if not (ok_inv and ok_map and ok_plan and ok_cov and len(ch_off) == len(opts)) or (m == 11 and (len(kk), selfm) != (81, 9)):
                fails += 1
                line = "FAIL " + line
            if m == 11 or line.startswith("FAIL"):
                print(line)
    # H3 and a deeper node unchanged with mirror_h6 on
    for L in ([], [[(0, 0)]], [[(0, 0), (1, 1)], [(3, None)]], [[(0, 0)], [(2, 0), (5, 1)]]):
        if new.tree_children(m, 7, L, mirror_h6=True) != old.tree_children(m, 7, L):
            fails += 1
            print("FAIL on: changed", m, L)

comp = load(os.path.join(R, "results/C3T/tools/compose.py"), "comp_new")
base = sys.argv[1] if len(sys.argv) > 1 else "/opt/work/base11.cnf"
if os.path.exists(base):
    E = C3Enc(11, 7)
    with open(base, "rb") as f:
        header = f.readline().decode().split()
        body = f.read()
    lvl, allL = [[]], []
    for d in range(4):
        lvl = [c for L in rng.sample(lvl, min(30, len(lvl))) for c in new.tree_children(11, 7, L)]
        allL += lvl
    n = 0
    for L in rng.sample(allL, 300):
        us = [c[0] for c in new.layer_clauses(11, L, E.ccw, E.sig)]
        if comp.node_sha(body, header, us) != comp.node_sha_cached(body, header, us):
            fails += 1
            print("FAIL node_sha_cached", L)
        n += 1
    print(f"node_sha_cached == node_sha on {n} random nodes (depth 1-4)")
print("FAILURES", fails)

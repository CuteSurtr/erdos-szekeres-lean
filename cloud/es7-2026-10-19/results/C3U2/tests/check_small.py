#!/usr/bin/env python3
"""Check a small close_tree run with --sigma-split (tests/run_small.sh, sig_* runs).
usage: check_small.py TOOLSDIR m k BASE OUT.jsonl
1. Statistics: sigma splits, nested sigma splits (split of a node that already has |C| > 0),
   layer splits of cube nodes and how many tree_children options rule 3 dropped there.
2. compose.py of TOOLSDIR on OUT (via tests/small.py, full sha check): must say class_covered.
3. Brute force, independent of compose.py and of the split records: every configuration
   (maximal path Q of the layer tree hullcase.tree_children(m, k, .), sigma in {0,1}^{1..m-1}
   consistent with the explicit sigmas of Q) must be matched by a certified leaf L__C, i.e. L is a
   prefix of Q and sigma agrees with C.  Walk the tree; at prefix P keep the set U of sigma vectors
   consistent with P not yet matched by a leaf on a prefix of P; remove those matched by the leaves
   with layers P; a maximal P with U non-empty is a hole."""
import collections, itertools, json, os, subprocess, sys

tools, m, k, base, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
sys.path.insert(0, tools)
import hullcase as h  # noqa: E402

R = [json.loads(l) for l in open(out)]
st = collections.Counter()
dropped = 0
fails = []
for r in R:
    L, C = h.parse_node(r["node"])
    if r.get("split") and "sigma_bits" in r:
        st["sigma_splits"] += 1
        K = len(r["sigma_bits"])
        st[f"sigma_splits_K{K}"] += 1
        if C:
            st["nested_sigma_splits"] += 1
        if set(r) != {"node", "split", "sigma_bits", "children"} or r["children"] != 2 ** K:
            fails.append(f"bad sigma split record {r}")
        st["max_C_after_sigma_split"] = max(st["max_C_after_sigma_split"], len(C) + K)
    elif r.get("split"):
        st["layer_splits"] += 1
        if C:
            st["layer_splits_of_cube_nodes"] += 1
            full = len(h.tree_children(m, k, L))
            dropped += full - r["children"]
    else:
        st[f"solve_{r['status']}{'_cube' if C else ''}"] += 1
st["rule3_dropped_options"] = dropped
leaves = [h.parse_node(r["node"]) for r in R if r.get("certified") and r.get("lrat_check") == "c VERIFIED"
          and r.get("cake_lpr") == "s VERIFIED UNSAT"]
st["certified_leaves"] = len(leaves)
st["certified_cube_leaves"] = sum(1 for _, C in leaves if C)

# compose.py
here = os.path.dirname(os.path.abspath(__file__))
p = subprocess.run([sys.executable, os.path.join(here, "small.py"), tools, str(m), str(k), "compose", base, out],
                   capture_output=True, text=True)
try:
    comp = json.loads(p.stdout.strip().splitlines()[-1])
except Exception:
    comp = {"raw": p.stdout + p.stderr}
if p.returncode != 0 or not comp.get("class_covered"):
    fails.append(f"compose rc {p.returncode}: {comp}")

# brute force
byL = collections.defaultdict(list)
for L, C in leaves:
    byL[h.layers_name(L)].append(C)
res = list(range(1, m))
ALL = list(itertools.product((0, 1), repeat=m - 1))
holes = []
nconf = [0]




def dfs(P, U):
    if P:
        matched = set()
        for C in byL.get(h.layers_name(P), []):
            matched |= {s for s in U if all(s[r - 1] == v for r, v in C)}
        U = [s for s in U if s not in matched]
    if not U:
        return
    ch = h.tree_children(m, k, P)
    if not ch:
        holes.append((h.layers_name(P), len(U)))
        return
    for c in ch:
        new = c[-1]
        nconf[0] += 1
        dfs(c, [s for s in U if all(sg is None or r == 0 or s[r - 1] == sg for r, sg in new)])


dfs([], ALL)
if holes:
    fails.append(f"brute force: {len(holes)} uncovered maximal paths, e.g. {holes[:3]}")
print(json.dumps({"run": os.path.basename(out), "stats": dict(st), "compose": {x: comp.get(x) for x in
      ("class_covered", "certified_nodes", "certified_cube_nodes", "sigma_splits_used", "uncovered_frontier_nodes",
       "sha_checked")}, "brute_force": {"tree_edges_walked": nconf[0], "holes": len(holes)},
      "result": "OK" if not fails else "FAIL", "fails": fails[:5]}))
sys.exit(1 if fails else 0)

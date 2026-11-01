#!/usr/bin/env python3
"""Differential test: the Lean definitions (prelude of C3Cover.lean, evaluated by Lean's #eval) against hullcase.py.

usage:
  python3 -I -B difftest.py gen  RESULTS_DIR PRELUDE OUT.lean SAMPLES.json [N] [SEED]
  python3 -I -B difftest.py cmp  RESULTS_DIR SAMPLES.json LEAN_OUTPUT.log

gen: random depth>=2 nodes (random walks from the 910 roots by layer and sigma splits, plus edge cases) and a Lean
     file that prints, for each node, layerChildren, free, sigmaChildren K (1 <= K <= min(3, |free|)); plus
     `roots` and `topCases.map keptOptions`.
cmp: compares the printed values with hullcase.cube_layer_children (mirror, mirror_h6), free_residues,
     sigma_children, tree_children (roots) - as lists, in order.
"""
import ast
import json
import os
import random
import sys

mode, R = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(R, "C3U2", "tools"))
import hullcase as H  # noqa: E402


def to_lean_layers(layers):
    return [[(r, 2 if s is None else s) for r, s in L] for L in layers]


def node_lit(layers, C):
    ls = ", ".join("[" + ", ".join(f"({r}, {s})" for r, s in L) + "]" for L in to_lean_layers(layers))
    cs = ", ".join(f"({r}, {v})" for r, v in C)
    return f"⟨[{ls}], [{cs}]⟩"


def canon(layers, C):
    return (tuple(tuple((r, 2 if s is None else s) for r, s in L) for L in layers), tuple((r, v) for r, v in C))


def roots_h():
    out = []
    for top in H.tree_children(11, 7, [], mirror=True, mirror_h6=True):
        for ch in H.tree_children(11, 7, top, mirror=True, mirror_h6=True):
            out.append(ch)
    return out


if mode == "gen":
    PRELUDE, OUT, SJ = sys.argv[3:6]
    N = int(sys.argv[6]) if len(sys.argv) > 6 else 300
    rnd = random.Random(int(sys.argv[7]) if len(sys.argv) > 7 else 20261101)
    rts = roots_h()
    samples = []
    seen = set()
    while len(samples) < N:
        lay, C = [list(L) for L in rnd.choice(rts)], []
        for step in range(rnd.randint(0, 6)):
            fr = H.free_residues(11, lay, C)
            if rnd.random() < 0.5 and fr:
                K = rnd.randint(1, min(3, len(fr)))
                lay, C = rnd.choice(H.sigma_children(11, lay, C, K)[1])
            else:
                ch = H.cube_layer_children(11, 7, lay, C, mirror=True, mirror_h6=True)
                if not ch:
                    break
                lay, C = rnd.choice(ch)
            key = H.node_name(lay, C)
            if key not in seen:
                seen.add(key)
                samples.append((lay, list(C)))
    # edge cases: all residues used (no layer children); no free residues but cube residues unused; cube residue in layer
    edge = [
        ([[(0, 0)], [(1, None)], [(2, None)], [(3, None)], [(4, None)], [(5, None)], [(6, None)], [(7, None)],
          [(8, None)], [(9, None)], [(10, None)]], []),
        ([[(0, 0)], [(1, 0), (2, 1)]], [(r, r % 2) for r in range(3, 11)]),
        ([[(0, 0), (5, 1)], [(3, None)], [(4, 1), (6, 0)]], [(1, 1), (2, 0), (7, 1), (8, 0), (9, 1), (10, 0)]),
        ([[(0, 0)], [(10, 1), (1, 0)]], [(1, 1)]),  # (not a tree node: unsorted pair; just exercises the functions)
    ]
    samples += edge
    json.dump(samples, open(SJ, "w"))
    pre = open(PRELUDE, encoding="utf-8").read()
    L = [pre, "",
         "def encN (n : Node) : String := toString n.layers ++ \"|\" ++ toString n.cube",
         "def samples : List Node := [" + ",\n  ".join(node_lit(l, c) for l, c in samples) + "]",
         "def line (n : Node) : String :=",
         "  let ks := (List.range 4).filter (fun K => 0 < K && K ≤ n.free.length)",
         "  encN n ++ \" || \" ++ String.intercalate \";\" (n.layerChildren.map encN) ++ \" || \" ++ toString n.free ++",
         "    \" || \" ++ String.intercalate \"#\" (ks.map fun K => String.intercalate \";\" ((n.sigmaChildren K).map encN))",
         "#eval do",
         "  for n in samples do",
         "    IO.println (\"N \" ++ line n)",
         "  for n in roots do",
         "    IO.println (\"R \" ++ encN n)",
         "  for t in topCases do",
         "    IO.println (\"K \" ++ toString t ++ \" || \" ++ toString (keptOptions t))",
         "end C3Cover", ""]
    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print(json.dumps({"samples": len(samples)}))
    sys.exit(0)

# ---------------------------------------------------------------- cmp
SJ, LOG = sys.argv[3:5]
samples = json.load(open(SJ))


def parse_node(s):
    a, b = s.split("|")
    return (tuple(tuple(tuple(t) for t in L) for L in ast.literal_eval(a)), tuple(tuple(t) for t in ast.literal_eval(b)))


lines = [l.rstrip("\n") for l in open(LOG, encoding="utf-8")]
N_lines = [l[2:] for l in lines if l.startswith("N ")]
R_lines = [l[2:] for l in lines if l.startswith("R ")]
K_lines = [l[2:] for l in lines if l.startswith("K ")]
bad = []
assert len(N_lines) == len(samples), (len(N_lines), len(samples))
cmp_layer = cmp_sigma = 0
for (lay, C), l in zip(samples, N_lines):
    lay = [[(r, s) for r, s in L] for L in lay]
    C = [tuple(x) for x in C]
    parts = l.split(" || ")
    node = parse_node(parts[0])
    if node != canon(lay, C):
        bad.append(("node", parts[0]))
    lc = [parse_node(x) for x in parts[1].split(";")] if parts[1] else []
    if len(lay) >= 2:
        want = [canon(a, b) for a, b in H.cube_layer_children(11, 7, lay, C, mirror=True, mirror_h6=True)]
        cmp_layer += 1
        if lc != want:
            bad.append(("layer", H.node_name(lay, C)))
    fr = ast.literal_eval(parts[2])
    if fr != H.free_residues(11, lay, C):
        bad.append(("free", H.node_name(lay, C)))
    sg = parts[3].split("#") if parts[3] else []
    for K, s in zip(range(1, 4), sg):
        got = [parse_node(x) for x in s.split(";")]
        want = [canon(a, b) for a, b in H.sigma_children(11, lay, C, K)[1]]
        cmp_sigma += 1
        if got != want:
            bad.append(("sigma", H.node_name(lay, C), K))
    if len(sg) != min(3, len(fr)):
        bad.append(("sigma-count", H.node_name(lay, C)))
rts = [canon(r, []) for r in roots_h()]
got_r = [parse_node(x) for x in R_lines]
if got_r != rts:
    bad.append(("roots", len(got_r), len(rts)))
for l in K_lines:
    t, kept = l.split(" || ")
    t = [tuple(x) for x in ast.literal_eval(t)]
    kept = [[tuple(x) for x in L] for L in ast.literal_eval(kept)]
    top = [(r, s) for r, s in t]
    if top == [(0, 0)]:
        want = H.h3_layer2_kept(11)
    else:
        want = H.h6_layer2_kept(11, top[1][0], top[1][1])
    want = [[(r, 2 if s is None else s) for r, s in L] for L in want]
    if kept != want:
        bad.append(("kept", t))
print(json.dumps({"samples": len(samples), "layer_compared": cmp_layer, "sigma_compared": cmp_sigma,
                  "roots_compared": len(got_r), "kept_compared": len(K_lines), "mismatches": len(bad), "sample": bad[:5]}))

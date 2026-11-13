#!/usr/bin/env python3
"""Read the C3FINAL record files and rebuild, for each of the 910 depth-2 roots of the reduced cut, the cover tree
that results/C3U2/tools/compose.py --mirror-h6 (covered2) finds.  Only records that compose.py accepts as certified
(certified true, lrat_check "c VERIFIED", cake_lpr "s VERIFIED UNSAT") are leaves; compose.py re-derives the CNF
sha256 of every one of them from the base formula and exits 1 on any mismatch (C3FINAL: all 116,883 matched).

load(R) -> dict with cert (canonical name -> list of (file, line, cnf_sha256)), ssplit, lsplit, prefixes.
tree(root, D) -> decision tree:  ("C",) | ("S", K, [subtrees]) | ("L", [subtrees])  (children in c3tree order)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c3tree as T  # noqa: E402


def canon(nm):
    return T.node_name(*T.parse_node(nm))


def load(R, files=None):
    if files is None:
        files = [l.strip() for l in open(os.path.join(R, "C3FINAL", "compose_files.txt")) if l.strip()]
    cert, ssplit, lsplit, cubes = {}, {}, set(), {}
    nrec = ncert_rec = 0
    BASE_SHA = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"
    for f in files:
        for i, l in enumerate(open(os.path.join(R, f))):
            r = json.loads(l)
            nrec += 1
            if "base_sha256" in r and r["base_sha256"] != BASE_SHA:
                raise SystemExit(f"{f}:{i + 1}: foreign base_sha256")
            if "node" not in r:
                continue
            if "cube" in r:
                parent = canon(r["node"])
                C = sorted((int(x), v) for x, v in r["cube"].items())
                if T.parse_node(parent)[1] or not C or any(v not in (0, 1) for _, v in C):
                    raise SystemExit(f"{f}:{i + 1}: bad sigma_cubes record")
                name = T.node_name(T.parse_node(parent)[0], C)
            else:
                name = canon(r["node"])
            if r.get("split") and "sigma_bits" in r:
                ssplit.setdefault(name, []).append(r["sigma_bits"])
            elif r.get("split") and T.parse_node(name)[1]:
                lsplit.add(name)
            if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                ncert_rec += 1
                cert.setdefault(name, []).append((f, i + 1, r.get("cnf_sha256")))
                if "cube" in r:
                    cubes.setdefault((parent, tuple(sorted(int(x) for x in r["cube"]))), set()).add(name)
    # sigma split records must name the K smallest free residues of a node with >= 2 layers (compose.py exits else)
    for name, L in ssplit.items():
        lay, C = T.parse_node(name)
        fr = T.free_residues(lay, C)
        for bits in L:
            nb = len(bits) if isinstance(bits, list) else 0
            if nb == 0 or len(lay) < 2 or bits != fr[:nb] or len(fr) < nb:
                raise SystemExit(f"bad sigma split record {name} {bits}")
    # implied sigma splits (all 2^K sigma_cubes cubes on the K smallest free residues certified)
    for (parent, res), got in cubes.items():
        lay, C = T.parse_node(parent)
        nb = len(res)
        fr = T.free_residues(lay, C)
        if len(lay) >= 2 and list(res) == fr[:nb] and len(fr) >= nb:
            want = {T.node_name(*c) for c in T.sigma_children(lay, C, nb)[1]}
            if nb > 0 and len(want) == 2 ** nb and got == want:
                ssplit.setdefault(parent, []).append(list(res))
    prefixes = set()
    for name in cert:
        L, C = T.parse_node(name)
        for j in range(1, len(L) + (1 if C else 0)):
            prefixes.add(T.layers_name(L[:j]))
    for name in list(ssplit) + list(lsplit):
        L = T.parse_node(name)[0]
        for j in range(1, len(L) + 1):
            prefixes.add(T.layers_name(L[:j]))
    return dict(cert=cert, ssplit=ssplit, lsplit=lsplit, prefixes=prefixes, nrec=nrec, ncert_rec=ncert_rec)


def tree(layers, C, D, stats=None):
    """compose.py covered2 (C3U2, --mirror-h6) below a node with >= 2 layers; returns the decision tree or None."""
    name = T.node_name(layers, C)
    if name in D["cert"]:
        return ("C",)
    for bits in D["ssplit"].get(name, []):
        K = len(bits)
        bb, sch = T.sigma_children(layers, C, K)
        assert bb == bits and len(sch) == 2 ** K > 0
        subs = [tree(cl, cc, D, stats) for cl, cc in sch]
        if all(s is not None for s in subs):
            return ("S", K, subs)
    if C:
        ch = T.layer_children(layers, C)
        if name not in D["lsplit"] or not ch:
            return None
        subs = [tree(cl, cc, D, stats) for cl, cc in ch]
        return ("L", subs) if all(s is not None for s in subs) else None
    if T.layers_name(layers) not in D["prefixes"]:
        return None
    ch = T.layer_children(layers, C)
    if not ch:
        return None
    subs = [tree(cl, cc, D, stats) for cl, cc in ch]
    return ("L", subs) if all(s is not None for s in subs) else None


def walk(t, layers, C):
    """yield (node, decision) in DFS (pre-)order."""
    yield (layers, C), t
    if t[0] == "S":
        for (cl, cc), s in zip(T.sigma_children(layers, C, t[1])[1], t[2]):
            yield from walk(s, cl, cc)
    elif t[0] == "L":
        for (cl, cc), s in zip(T.layer_children(layers, C), t[1]):
            yield from walk(s, cl, cc)

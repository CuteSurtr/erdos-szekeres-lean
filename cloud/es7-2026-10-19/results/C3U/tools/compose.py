#!/usr/bin/env python3
"""Compose per-node results into one claim (or report what is missing).

Input: jsonl files of node records {"node": NAME, "certified": true, "cnf_sha256": ...} (from
close_node.py; every record must have been checked by BOTH lrat-check (E2 patch) and cake_lpr).
The class (m = 11, k = 7) is covered when the root of the layer tree is covered, where a node is
covered iff it is certified, or it has children and all of them are covered (children: hullcase.tree_children with the
H3 mirror reduction).  The script also re-derives
each certified node's CNF sha256 from BASE + the node's units and compares it with the record.
usage: compose.py BASE RESULTS.jsonl [...] [--no-sha] [--mirror-h6]

C3T (FIX1) changes:
- BASE must have sha256 BASE_SHA (gen_case.py 11 7 none), and every record that has a
  "base_sha256" must carry BASE_SHA; otherwise the script prints the reason and exits 1.
- Every check that guards correctness is an explicit test that prints the reason and exits 1
  (no bare assert, so python3 -O cannot skip it).  The CNF sha256 is re-derived for EVERY
  certified record (not only the last record per node); the hash of header + BASE body is cached
  per unit count (node_sha_cached: the same bytes as node_sha, tested equal in C3T/tests).
- The output also reports "certified_with_proof_sha256" (certified records, and distinct certified
  nodes, carrying a proof_sha256) and "sha_checked".
- --mirror-h6 (default off): children of H6(a, s) nodes reduced by Lemma H6M (hullcase.py,
  results/C3PLAN/PLAN.md 3a).  Off, the tree is exactly that of C3-S compose.py.  No task may use
  it before results/C3AUDIT2 accepts the lemma.

C3U changes (results/C3U/TASK.md rule 5, results/C3U/sigma_split.md):
- Node names may be sigma-cube names "L__C" (hullcase.parse_node); a certified record's CNF sha256
  is re-derived from its name (layer units of L, then the units of C).
- Records of results/C3PLAN/scripts/sigma_cubes.py ("node" = parent N, "cube" = {r: v}) are read as
  records of the node N__C, C = the cube sorted by residue.
- A node is covered if it is certified, or if one of its splits has all its children covered:
  * sigma split: a split record with "sigma_bits", or, for a node N whose 2^K sigma_cubes.py cubes
    on the same K residues are all certified, an implied one.  The bits must be exactly the K
    smallest free residues of the node (hullcase.free_residues) and the node must have at least 2
    layers; a split record that fails this makes the script exit 1 (an implied one is just not
    used).  Children: all 2^K cube nodes.
  * layer split: as in C3T for plain layer nodes (always available, explored below nodes that
    have a certified or split descendant); for a cube node L__C only when it has a layer split
    record, with children L'__C for L' in tree_children(L) not contradicting C
    (hullcase.cube_layer_children).
- New output fields: "certified_cube_nodes", "sigma_splits_used" (nodes covered through a sigma
  split), "sigma_split_nodes_sample" (the first 50 of them)."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from c3cnf import C3Enc  # noqa: E402
from hullcase import tree_children, layer_clauses, layers_name, parse_layers  # noqa: E402
from hullcase import cube_layer_children, free_residues, node_name, node_units, parse_node, sigma_children  # noqa: E402

M, K = 11, 7
BASE_SHA = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"
MIRROR_H6 = False


def fail(msg):
    print(json.dumps({"error": msg}), flush=True)
    sys.exit(1)


def children(layers):
    return tree_children(M, K, layers, mirror=True, mirror_h6=MIRROR_H6)


def file_sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def node_sha(base_bytes, header, units):
    h = hashlib.sha256()
    h.update(f"p cnf {header[2]} {int(header[3]) + len(units)}\n".encode())
    h.update(base_bytes)
    h.update("".join(f"{u} 0\n" for u in units).encode())
    return h.hexdigest()


_hcache = {}


def node_sha_cached(base_bytes, header, units):
    """same bytes and digest as node_sha; the hash of header + BASE body is cached per unit count."""
    n = len(units)
    if n not in _hcache:
        h = hashlib.sha256()
        h.update(f"p cnf {header[2]} {int(header[3]) + n}\n".encode())
        h.update(base_bytes)
        _hcache[n] = h
    h = _hcache[n].copy()
    h.update("".join(f"{u} 0\n" for u in units).encode())
    return h.hexdigest()


def main():
    global MIRROR_H6
    unknown = [a for a in sys.argv[1:] if a.startswith("--") and a not in ("--no-sha", "--mirror-h6")]
    if unknown:
        fail(f"unknown option {unknown[0]}")
    MIRROR_H6 = "--mirror-h6" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        fail("usage: compose.py BASE RESULTS.jsonl [...] [--no-sha] [--mirror-h6]")
    base, files = args[0], args[1:]
    bs = file_sha(base)
    if bs != BASE_SHA:
        fail(f"BASE {base} has sha256 {bs}, not {BASE_SHA}")
    cert = {}
    allcert = []
    ssplit = {}  # node -> list of (sigma_bits, where): sigma split records
    lsplit = set()  # cube nodes with a layer split record
    cubes = {}  # sigma_cubes.py records: (parent, residues) -> set of certified cube names

    def canon(f, i, nm):
        try:
            return node_name(*parse_node(nm))
        except ValueError as e:
            fail(f"{f} line {i}: bad node name: {e}")

    for f in files:
        for i, l in enumerate(open(f)):
            r = json.loads(l)
            if "base_sha256" in r and r["base_sha256"] != BASE_SHA:
                fail(f"{f} line {i + 1}: base_sha256 {r['base_sha256']} is not {BASE_SHA}")
            if "node" not in r:
                continue  # e.g. sigma_cubes runner "meta" records
            if "cube" in r:
                parent = canon(f, i + 1, r["node"])
                C = sorted((int(x), v) for x, v in r["cube"].items())
                if parse_node(parent)[1] or not C or any(v not in (0, 1) for _, v in C):
                    fail(f"{f} line {i + 1}: bad sigma_cubes record")
                name = node_name(parse_node(parent)[0], C)
            else:
                name = canon(f, i + 1, r["node"])
            if r.get("split") and "sigma_bits" in r:
                ssplit.setdefault(name, []).append((r["sigma_bits"], f"{f} line {i + 1}"))
            elif r.get("split") and parse_node(name)[1]:
                lsplit.add(name)
            if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                cert[name] = r
                allcert.append((f, i + 1, r, name))
                if "cube" in r:
                    cubes.setdefault((parent, tuple(sorted(int(x) for x in r["cube"]))), set()).add(name)
    # sigma split records must name the K smallest free residues of a node with >= 2 layers
    for name, L in ssplit.items():
        lay, C = parse_node(name)
        for bits, where in L:
            nb = len(bits) if isinstance(bits, list) else 0
            if nb == 0 or len(lay) < 2 or bits != free_residues(M, lay, C)[:nb] or len(free_residues(M, lay, C)) < nb:
                fail(f"{where}: node {name} ({len(lay)} layers): sigma_bits {bits} refused: a sigma split needs a "
                     f"node with >= 2 layers and the {nb} smallest free residues {free_residues(M, lay, C)[:nb]}")
    # implied sigma splits: all 2^K sigma_cubes.py cubes of a node on its K smallest free residues certified
    for (parent, res), got in cubes.items():
        lay, C = parse_node(parent)
        nb = len(res)
        if len(lay) >= 2 and list(res) == free_residues(M, lay, C)[:nb] and len(free_residues(M, lay, C)) >= nb:
            if got == {node_name(*c) for c in sigma_children(M, lay, C, nb)[1]}:
                ssplit.setdefault(parent, []).append((list(res), "implied by sigma_cubes records"))
    if "--no-sha" not in sys.argv:
        E = C3Enc(M, K)
        with open(base, "rb") as f:
            header = f.readline().decode().split()
            body = f.read()
        if header[:2] != ["p", "cnf"] or len(header) != 4:
            fail("BASE header is not 'p cnf V C'")
        shas = {}
        for f, i, r, name in allcert:
            if name not in shas:
                us = node_units(M, name, E.ccw, E.sig)
                shas[name] = node_sha_cached(body, header, us)
            if shas[name] != r.get("cnf_sha256"):
                fail(f"{f} line {i}: node {name}: cnf_sha256 {r.get('cnf_sha256')} is not the re-derived {shas[name]}")
    memo = {}
    missing = []

    def covered(layers, depth_left):
        name = layers_name(layers) if layers else "ROOT"
        if name in cert:
            return True
        ch = children(layers)
        if not ch or depth_left == 0:
            missing.append(name)
            return False
        ok = True
        for c in ch:
            ok &= covered(c, depth_left - 1)
        return ok

    # only expand below nodes that have a certified descendant, to keep the report small
    # (C3U: also the layer prefixes of cube nodes, including L itself, and of sigma-split nodes)
    prefixes = set()
    for name in cert:
        L, C = parse_node(name)
        for j in range(1, len(L) + (1 if C else 0)):
            prefixes.add(layers_name(L[:j]))
    for name in list(ssplit) + list(lsplit):
        L = parse_node(name)[0]
        for j in range(1, len(L) + 1):
            prefixes.add(layers_name(L[:j]))
    sig_used = set()

    def covered2(layers, C=()):
        C = list(C)
        name = (node_name(layers, C) if layers else "ROOT")
        if name in memo:
            return memo[name]
        memo[name] = False  # no cycles: every split adds a layer or a sigma bit
        if name in cert:
            memo[name] = True
            return True
        for bits, _ in ssplit.get(name, []):
            # sigma split (checked above: bits = the K smallest free residues): all 2^K cubes
            res = True
            for cl, cc in sigma_children(M, layers, C, len(bits))[1]:
                res = covered2(cl, cc) and res
            if res:
                sig_used.add(name)
                memo[name] = True
                return True
        if C:
            ch = cube_layer_children(M, K, layers, C, mirror=True, mirror_h6=MIRROR_H6)
            if name not in lsplit or not ch:  # no children (all residues used): never vacuously covered
                missing.append(name)
                return False
            res = True
            for cl, cc in ch:
                res = covered2(cl, cc) and res
            memo[name] = res
            return res
        if layers and name not in prefixes:
            missing.append(name)
            return False
        ok = True
        for c in children(layers):
            ok = covered2(c) and ok
        memo[name] = ok
        return ok

    ok = covered2([])
    print(json.dumps({"certified_nodes": len(cert), "class_covered": ok, "uncovered_frontier_nodes": len(missing),
                      "uncovered_sample": missing[:10],
                      "certified_records": len(allcert),
                      "certified_with_proof_sha256": {"records": sum(1 for _, _, r, _ in allcert if r.get("proof_sha256")),
                                                      "nodes": sum(1 for r in cert.values() if r.get("proof_sha256"))},
                      "sha_checked": "--no-sha" not in sys.argv, "mirror_h6": MIRROR_H6,
                      "certified_cube_nodes": sum(1 for n in cert if "__" in n), "sigma_splits_used": len(sig_used),
                      "sigma_split_nodes_sample": sorted(sig_used)[:50]}))


if __name__ == "__main__":
    main()

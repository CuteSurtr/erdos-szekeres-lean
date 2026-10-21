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
  it before results/C3AUDIT2 accepts the lemma."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from c3cnf import C3Enc  # noqa: E402
from hullcase import tree_children, layer_clauses, layers_name, parse_layers  # noqa: E402

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
    for f in files:
        for i, l in enumerate(open(f)):
            r = json.loads(l)
            if "base_sha256" in r and r["base_sha256"] != BASE_SHA:
                fail(f"{f} line {i + 1}: base_sha256 {r['base_sha256']} is not {BASE_SHA}")
            if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                cert[layers_name(parse_layers(r["node"]))] = r
                allcert.append((f, i + 1, r))
    if "--no-sha" not in sys.argv:
        E = C3Enc(M, K)
        with open(base, "rb") as f:
            header = f.readline().decode().split()
            body = f.read()
        if header[:2] != ["p", "cnf"] or len(header) != 4:
            fail("BASE header is not 'p cnf V C'")
        shas = {}
        for f, i, r in allcert:
            name = layers_name(parse_layers(r["node"]))
            if name not in shas:
                us = [c[0] for c in layer_clauses(M, parse_layers(name), E.ccw, E.sig)]
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
    prefixes = set()
    for name in cert:
        L = parse_layers(name)
        for j in range(1, len(L)):
            prefixes.add(layers_name(L[:j]))

    def covered2(layers):
        name = layers_name(layers) if layers else "ROOT"
        if name in cert:
            return True
        if layers and name not in prefixes:
            missing.append(name)
            return False
        ok = True
        for c in children(layers):
            ok = covered2(c) and ok
        return ok

    ok = covered2([])
    print(json.dumps({"certified_nodes": len(cert), "class_covered": ok, "uncovered_frontier_nodes": len(missing),
                      "uncovered_sample": missing[:10],
                      "certified_records": len(allcert),
                      "certified_with_proof_sha256": {"records": sum(1 for _, _, r in allcert if r.get("proof_sha256")),
                                                      "nodes": sum(1 for r in cert.values() if r.get("proof_sha256"))},
                      "sha_checked": "--no-sha" not in sys.argv, "mirror_h6": MIRROR_H6}))


if __name__ == "__main__":
    main()

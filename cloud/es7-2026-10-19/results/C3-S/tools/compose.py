#!/usr/bin/env python3
"""Compose per-node results into one claim (or report what is missing).

Input: jsonl files of node records {"node": NAME, "certified": true, "cnf_sha256": ...} (from
close_node.py; every record must have been checked by BOTH lrat-check (E2 patch) and cake_lpr).
The class (m = 11, k = 7) is covered when the root of the layer tree is covered, where a node is
covered iff it is certified, or it has children and all of them are covered (children as in
knuth_pruned.children: the 11 top cases, then hullcase.layer2_options).  The script also re-derives
each certified node's CNF sha256 from BASE + the node's units and compares it with the record.
usage: compose.py BASE RESULTS.jsonl [...] [--no-sha]"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3a"))
sys.path.insert(0, HERE)
from c3cnf import C3Enc  # noqa: E402
from hullcase import cases, legacy_to_layers, layer2_options, layer_clauses, layers_name, parse_layers  # noqa: E402

M, K = 11, 7


def children(layers):
    if not layers:
        return [legacy_to_layers(c) for c in cases(M, K)]
    used = [r for L in layers for r, _ in L]
    return [layers + [o] for o in layer2_options(M, [(r, None) for r in used])]


def node_sha(base_bytes, header, units):
    h = hashlib.sha256()
    h.update(f"p cnf {header[2]} {int(header[3]) + len(units)}\n".encode())
    h.update(base_bytes)
    h.update("".join(f"{u} 0\n" for u in units).encode())
    return h.hexdigest()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base, files = args[0], args[1:]
    cert = {}
    for f in files:
        for l in open(f):
            r = json.loads(l)
            if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                cert[layers_name(parse_layers(r["node"]))] = r
    if "--no-sha" not in sys.argv:
        E = C3Enc(M, K)
        with open(base, "rb") as f:
            header = f.readline().decode().split()
            body = f.read()
        for name, r in cert.items():
            us = [c[0] for c in layer_clauses(M, parse_layers(name), E.ccw, E.sig)]
            assert node_sha(body, header, us) == r["cnf_sha256"], ("sha mismatch", name)
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
                      "uncovered_sample": missing[:10]}))


if __name__ == "__main__":
    main()

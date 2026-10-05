#!/usr/bin/env python3
"""Independent exact replay of weighted omission trees (no geometric transfer).

Every leaf either exceeds the hole budget or has a strict weighted-capacity
margin. The underlying capacity inequality is proved in OmissionCertificates.lean;
this JSON parser, branch traversal, and concrete data are not yet Lean-certified.
"""
import argparse
import json
from pathlib import Path

from omission_row_probe import read_rows


def natural(value):
    return type(value) is int and value >= 0


def leaf_margin(n, rows, budget, missing, occupied, node):
    capacity = node.get("capacity")
    weights = node.get("weights")
    if not natural(capacity) or not isinstance(weights, list):
        raise ValueError("Invalid weighted leaf")
    loads = [0] * n
    lower = 0
    seen_rows = set()
    for pair in weights:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("Invalid row multiplier")
        r, weight = pair
        if not natural(r) or r >= len(rows) or r in seen_rows or not natural(weight):
            raise ValueError("Invalid row multiplier")
        seen_rows.add(r)
        support, demand = rows[r]
        lower += weight * max(0, demand - len(set(support) & missing))
        for i in support:
            loads[i] += weight
    excess = sum(max(0, loads[i] - capacity) for i in range(n)
                 if i not in missing and i not in occupied)
    return lower - capacity * (budget - len(missing)) - excess


def contexts(n, nodes, root):
    """Validate an entire binary tree and return every leaf with its context."""
    seen = set()
    stack = [(root, frozenset(), frozenset())]
    leaves = []
    while stack:
        index, missing, occupied = stack.pop()
        if not natural(index) or index >= len(nodes) or index in seen:
            raise ValueError("Repeated or invalid tree node")
        seen.add(index)
        node = nodes[index]
        if not isinstance(node, dict):
            raise ValueError("Invalid node")
        if node.get("type") == "branch":
            i = node.get("vertex")
            if not natural(i) or i >= n or i in missing or i in occupied:
                raise ValueError("Repeated or invalid branch variable")
            stack.extend([(node.get("zero"), missing, occupied | {i}),
                          (node.get("one"), missing | {i}, occupied)])
        else:
            leaves.append((index, missing, occupied))
    if len(seen) != len(nodes):
        raise ValueError("Unreachable tree nodes")
    return leaves


def check_tree(n, rows, budget, nodes, root, allow_pending=False):
    read_rows({"states": [None] * n, "constraints": [
        {"support": support, "rhs": demand} for support, demand in rows]})
    if not natural(budget) or budget > n:
        raise ValueError("Invalid budget")
    leaves = contexts(n, nodes, root)
    pending = 0
    margins = []
    for index, missing, occupied in leaves:
        node = nodes[index]
        if node.get("type") == "weighted":
            margin = leaf_margin(n, rows, budget, missing, occupied, node)
            if margin <= 0:
                raise ValueError(f"Nonpositive leaf margin at node {index}")
            margins.append(margin)
        elif node.get("type") == "over_budget":
            if len(missing) <= budget:
                raise ValueError("Unjustified over-budget leaf")
        elif node.get("type") == "pending" and allow_pending:
            pending += 1
        else:
            raise ValueError("Uncertified leaf")
    return {"nodes": len(nodes), "leaves": len(leaves), "pending": pending,
            "complete": pending == 0, "minimum_margin": min(margins, default=None)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--tree", type=Path)
    args = parser.parse_args()
    data = json.loads(args.source.read_text())
    tree = json.loads(args.tree.read_text()) if args.tree else data
    n, rows = read_rows(data)
    if args.tree:
        from omission_opb import sha256
        if tree.get("source_sha256") != sha256(args.source):
            raise ValueError("Tree and source hashes differ")
    print(json.dumps(check_tree(n, rows, tree["hole_budget"], tree["nodes"], tree["root"])))

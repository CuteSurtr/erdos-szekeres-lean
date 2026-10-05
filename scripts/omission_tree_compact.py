#!/usr/bin/env python3
"""Reduce certificate multipliers, accepting changes only after exact checks."""
import argparse
import copy
from functools import reduce
import json
from math import gcd
from pathlib import Path

from omission_opb import sha256
from omission_row_probe import read_rows
from omission_tree import check_tree, contexts, leaf_margin


def primitive(node):
    divisor = reduce(gcd, [node["capacity"]] + [w for _, w in node["weights"]])
    if divisor <= 1:
        return node
    return {"type": "weighted", "capacity": node["capacity"] // divisor,
            "weights": [[r, w // divisor] for r, w in node["weights"]]}


def compact_leaf(n, rows, budget, missing, occupied, node):
    if leaf_margin(n, rows, budget, missing, occupied, node) <= 0:
        raise ValueError("Cannot compact an invalid leaf")
    result = primitive(node)
    capacity = node["capacity"]
    if capacity:
        for scale in (1, 10, 100, 1000, 10000, 100000):
            if scale >= capacity:
                break
            # Nearest integer, with ties upward; no floating-point arithmetic.
            weights = [[r, (2 * w * scale + capacity) // (2 * capacity)]
                       for r, w in node["weights"]]
            candidate = {"type": "weighted", "capacity": scale,
                         "weights": [[r, w] for r, w in weights if w]}
            if leaf_margin(n, rows, budget, missing, occupied, candidate) > 0:
                result = primitive(candidate)
                break
    if leaf_margin(n, rows, budget, missing, occupied, result) <= 0:
        raise AssertionError("Compaction invalidated a leaf")
    return result


def run(source, tree, output):
    if output.exists():
        raise FileExistsError(output)
    data, original = json.loads(source.read_text()), json.loads(tree.read_text())
    if original["source_sha256"] != sha256(source):
        raise ValueError("Tree and source hashes differ")
    n, rows = read_rows(data)
    budget, root = original["hole_budget"], original["root"]
    nodes = copy.deepcopy(original["nodes"])
    before = check_tree(n, rows, budget, nodes, root)
    changed = 0
    for i, missing, occupied in contexts(n, nodes, root):
        if nodes[i]["type"] == "weighted":
            compacted = compact_leaf(n, rows, budget, missing, occupied, nodes[i])
            changed += compacted != nodes[i]
            nodes[i] = compacted
    after = check_tree(n, rows, budget, nodes, root)
    result = {"scope": original["scope"], "source": str(source),
              "source_sha256": sha256(source), "parent_tree": str(tree),
              "parent_tree_sha256": sha256(tree), "script_sha256": sha256(Path(__file__)),
              "checker_sha256": sha256(Path(__file__).with_name("omission_tree.py")),
              "hole_budget": budget, "root": root, "nodes": nodes,
              "status": "unsat", "before": before, "checked": after,
              "changed_leaves": changed}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "nodes"}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("tree", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.tree, args.output)

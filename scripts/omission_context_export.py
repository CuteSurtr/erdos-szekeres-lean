#!/usr/bin/env python3
"""Export one complete subtree of an omission tree whose other branches may be pending.

This wraps `omission_fused_export` without changing it. The whole tree is
replayed with pending leaves allowed, and the selected subtree must then be
complete: every leaf under it is an exact weighted or over-budget leaf. The
exported root theorem `node<k>` carries the subtree's inherited context, for
example "state 0 occupied" when the tree first branches on state 0.
"""
import argparse
import json
from pathlib import Path

import omission_fused_export as fused
import omission_lean_export as original
from omission_tree import check_tree as full_check


def subtree_check(subtree):
    def check(n, rows, budget, nodes, root, allow_pending=False):
        result = full_check(n, rows, budget, nodes, root, allow_pending=True)
        stack = [subtree]
        while stack:
            node = nodes[stack.pop()]
            if node["type"] == "branch":
                stack += [node["zero"], node["one"]]
            elif node["type"] not in ("weighted", "over_budget"):
                raise ValueError("The exported subtree contains an unfinished leaf")
        return result
    return check


def export(source, tree, output, namespace, leaf_limit, subtree, module_prefix):
    if subtree is None:
        raise ValueError("Use omission_fused_export.py for complete trees")
    original.check_tree = subtree_check(subtree)
    report = fused.export(source, tree, output, namespace, leaf_limit, subtree, module_prefix)
    report["context_exporter_sha256"] = original.sha256(Path(__file__))
    report["exported_subtree"] = subtree
    (output / "export.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("tree", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--namespace", default="OmissionContextExport")
    parser.add_argument("--leaf-limit", type=int, default=64)
    parser.add_argument("--subtree", type=int, required=True)
    parser.add_argument("--module-prefix", default="")
    args = parser.parse_args()
    result = export(args.source, args.tree, args.output, args.namespace, args.leaf_limit,
                    args.subtree, args.module_prefix)
    print(json.dumps({key: result.get(key) for key in ["states", "rows", "budget", "base",
                     "exported_leaves", "exported_parts", "proof_style", "exported_subtree"]}))

#!/usr/bin/env python3
"""Lift stored exact duals to ancestors, compact multipliers, replay outputs.

All work is confined to this new bundle; archived input trees are unchanged.
"""
import copy
import gzip
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parent.parent
INPUT = ROOT / "experiments/omission-residual32-resume-2026-10-10"
CONTEXTS = [485514, 485512, 485506, 485509, 492350, 485503, 492346, 492344, 11, 9]
sys.path.insert(0, str(ROOT / "scripts"))
from omission_row_probe import read_rows
from omission_lean_export import inspect_tree, normalize_leaf
from omission_tree_compact import compact_leaf


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    src = ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz"
    raw = gzip.decompress(src.read_bytes())
    source_hash = hashlib.sha256(raw).hexdigest()
    assert source_hash == "f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909"
    n, rows = read_rows(json.loads(raw))
    frozen_path = ROOT / "experiments/omission-residual32-research-2026-10-10/pending-contexts.json"
    frozen = {c["node"]: c for c in json.loads(frozen_path.read_text())["contexts"]}
    spec = importlib.util.spec_from_file_location("remaining_replay", INPUT / "check.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    report = {"scope": "Exact arithmetic tree compression only; Lean validation is separate",
              "source_sha256": source_hash, "prepare_sha256": sha(Path(__file__)),
              "source_archive_sha256": sha(src), "frozen_contexts_sha256": sha(frozen_path),
              "checker_sha256": sha(INPUT / "check.py"),
              "compactor_sha256": sha(ROOT / "scripts/omission_tree_compact.py"), "contexts": []}
    for original in CONTEXTS:
        start = time.monotonic()
        path = INPUT / f"closed-context-{original}.json.gz"
        tree = json.loads(gzip.decompress(path.read_bytes()))
        assert tree["source_sha256"] == source_hash and tree["original_node"] == original
        before = checker.replay(tree, rows, n, frozen[original])
        nodes = tree["nodes"]
        preorder, postorder, local, counts = inspect_tree(nodes, tree["root"])
        contexts = {i: (tree["missing"] + m, tree["occupied"] + o) for i, (m, o) in local.items()}
        parent = {}
        for i, node in enumerate(nodes):
            if node["type"] == "branch":
                parent[node["zero"]] = (i, node["vertex"], False)
                parent[node["one"]] = (i, node["vertex"], True)
        replacement, lifted = {}, 0
        for i, node in enumerate(nodes):
            if node["type"] != "weighted":
                continue
            missing, occupied = contexts[i]
            entries, columns = normalize_leaf(n, rows, node, missing)
            normalized = {"type": "weighted", "capacity": node["capacity"],
                          "weights": [list(entry) for entry in entries]}
            cap = node["capacity"]
            hole_bonus = [max(cap - c, 0) for c in columns]
            occupied_bonus = [max(c - cap, 0) for c in columns]
            margin = sum(w * rows[r][1] for r, w in entries) - cap * 32 - sum(occupied_bonus)
            margin += sum(hole_bonus[j] for j in missing) + sum(occupied_bonus[j] for j in occupied)
            assert margin > 0
            replacement[i] = normalized
            current = i
            while current in parent:
                ancestor, variable, missing_value = parent[current]
                margin -= hole_bonus[variable] if missing_value else occupied_bonus[variable]
                if margin <= 0:
                    break
                old = replacement.get(ancestor)
                if old is None or sum(w for _, w in entries) < sum(w for _, w in old["weights"]):
                    replacement[ancestor] = normalized
                lifted += 1
                current = ancestor
        reduced, changed = [], 0

        def visit(index):
            nonlocal changed
            new = len(reduced)
            reduced.append(None)
            if index in replacement:
                candidate = copy.deepcopy(replacement[index])
                compacted = compact_leaf(n, rows, 32, *map(set, contexts[index]), candidate)
                changed += compacted != candidate
                reduced[new] = compacted
            else:
                node = nodes[index]
                assert node["type"] == "branch"
                zero, one = visit(node["zero"]), visit(node["one"])
                reduced[new] = {"type": "branch", "vertex": node["vertex"], "zero": zero, "one": one}
            return new

        root = visit(tree["root"])
        result = {"scope": "Complete conditional arithmetic subtree after exact ancestor lifting and multiplier compaction; Lean check separate",
                  "source_sha256": source_hash, "hole_budget": 32, "original_node": original,
                  "missing": tree["missing"], "occupied": tree["occupied"], "root": root, "nodes": reduced}
        after = checker.replay(result, rows, n, frozen[original])
        result["independent_check"] = after
        out = BUNDLE / f"compressed-context-{original}.json.gz"
        out.write_bytes(gzip.compress(json.dumps(result, separators=(",", ":")).encode(), mtime=0))
        sizes = [sum(w for _, w in node["weights"]) for node in reduced if node["type"] == "weighted"]
        item = {"original_node": original, "input": str(path.relative_to(ROOT)), "input_sha256": sha(path),
                "output": out.name, "output_sha256": sha(out), "before": before, "after": after,
                "lifted_ancestor_checks": lifted, "compacted_retained_leaves": changed,
                "largest_multiplier_total": max(sizes), "above_catalog_base": sum(x >= 131072 for x in sizes),
                "seconds": round(time.monotonic() - start, 3)}
        report["contexts"].append(item)
        (BUNDLE / "compression.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(item), flush=True)


if __name__ == "__main__":
    main()

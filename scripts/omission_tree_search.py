#!/usr/bin/env python3
"""Use numerical LP only to discover exact weighted omission-tree leaves.

No numerical bound closes a branch: integer arithmetic must show a strict
margin. Unfinished branches remain explicit and can be resumed with --seed-tree.
Requires the optional highspy and numpy packages.
"""
import argparse
import copy
import json
import math
from pathlib import Path
import time

from omission_opb import sha256
from omission_row_probe import read_rows, valid_holes
from omission_tree import check_tree, contexts, leaf_margin


def run(source, output, budget=None, seconds=300, max_nodes=20000, seed_tree=None):
    import highspy
    import numpy as np
    if output.exists():
        raise FileExistsError(output)
    if seconds < 1 or max_nodes < 1:
        raise ValueError("Invalid search limits")
    data = json.loads(source.read_text())
    n, rows = read_rows(data)
    if budget is None:
        budget = data["hole_budget"] + 1
    if type(budget) is not int or not 0 <= budget <= n:
        raise ValueError("Invalid hole budget")
    seed = json.loads(seed_tree.read_text()) if seed_tree else data
    if seed_tree and seed.get("source_sha256") != sha256(source):
        raise ValueError("Seed tree and source hashes differ")
    nodes, root = copy.deepcopy(seed["nodes"]), seed["root"]
    pending = []
    for index, missing, occupied in contexts(n, nodes, root):
        node = nodes[index]
        if len(missing) > budget:
            nodes[index] = {"type": "over_budget"}
        elif node.get("type") == "weighted" and leaf_margin(n, rows, budget, missing, occupied, node) > 0:
            pass
        elif node.get("type") in ("weighted", "pending", "over_budget"):
            nodes[index] = {"type": "pending"}
            pending.append((index, missing, occupied))
        else:
            raise ValueError("Invalid seed leaf")
    initial = check_tree(n, rows, budget, nodes, root, allow_pending=True)
    model = highspy.Highs()
    model.setOptionValue("output_flag", False)
    model.setOptionValue("threads", 1)
    model.setOptionValue("solver", "simplex")
    variables = [model.addVariable(lb=0, ub=1, obj=1) for _ in range(n)]
    for support, demand in rows:
        model.addConstr(model.qsum(variables[i] for i in support) >= demand)
    indices = np.arange(n, dtype=np.int32)
    started = time.monotonic()
    processed = 0
    exact_leaves = 0
    witness = None
    stop_reason = "complete"
    while pending:
        remaining = seconds - (time.monotonic() - started)
        if remaining <= 0 or processed >= max_nodes:
            stop_reason = "time_limit" if remaining <= 0 else "node_limit"
            break
        index, missing, occupied = pending.pop()
        if len(missing) > budget:
            nodes[index] = {"type": "over_budget"}
            exact_leaves += 1
            continue
        impossible_row = next((r for r, (support, demand) in enumerate(rows)
                               if demand > len(set(support) - occupied)), None)
        if impossible_row is not None:
            leaf = {"type": "weighted", "capacity": 0, "weights": [[impossible_row, 1]]}
            if leaf_margin(n, rows, budget, missing, occupied, leaf) <= 0:
                raise AssertionError("Invalid direct row contradiction")
            nodes[index] = leaf
            exact_leaves += 1
            continue
        lower = np.array([float(i in missing) for i in range(n)])
        upper = np.array([float(i not in occupied) for i in range(n)])
        model.changeColsBounds(n, indices, lower, upper)
        # HiGHS measures this limit cumulatively across repeated run() calls.
        model.setOptionValue("time_limit", model.getRunTime() + min(remaining, 20.0))
        model.run()
        processed += 1
        if model.getModelStatus() != highspy.HighsModelStatus.kOptimal:
            # Numerical infeasibility, a timeout, or an error is never a certificate.
            pending.append((index, missing, occupied))
            stop_reason = str(model.getModelStatus())
            break
        solution = model.getSolution()
        if not solution.value_valid or not solution.dual_valid:
            raise ValueError("LP returned invalid primal or dual data")
        dual = solution.row_dual
        if not all(math.isfinite(x) for x in dual + solution.col_value):
            raise ValueError("Nonfinite LP values")
        certified = False
        for scale in (10**6, 10**9, 10**12):
            weights = [[r, max(0, round(scale * value))] for r, value in enumerate(dual)]
            leaf = {"type": "weighted", "capacity": scale,
                    "weights": [[r, weight] for r, weight in weights if weight]}
            if leaf_margin(n, rows, budget, missing, occupied, leaf) > 0:
                nodes[index] = leaf
                exact_leaves += 1
                certified = True
                break
        if certified:
            continue
        candidate = [i for i, x in enumerate(solution.col_value) if x > 0.5]
        if valid_holes(n, rows, budget, candidate):
            witness = candidate
            pending.append((index, missing, occupied))
            stop_reason = "exact_row_assignment"
            break
        available = [i for i in range(n) if i not in missing and i not in occupied]
        if not available:
            raise ValueError("Unresolved complete assignment")
        variable = min(available, key=lambda i: (abs(solution.col_value[i] - 0.5), i))
        zero, one = len(nodes), len(nodes) + 1
        nodes.extend([{"type": "pending"}, {"type": "pending"}])
        nodes[index] = {"type": "branch", "vertex": variable, "zero": zero, "one": one}
        pending.extend([(zero, missing, occupied | {variable}),
                        (one, missing | {variable}, occupied)])
    checked = check_tree(n, rows, budget, nodes, root, allow_pending=True)
    record = {
        "scope": "Exact finite omission-row tree; JSON traversal and geometric transfer are not Lean-certified",
        "source": str(source), "source_sha256": sha256(source),
        "script_sha256": sha256(Path(__file__)), "checker_sha256": sha256(Path(__file__).with_name("omission_tree.py")),
        "seed_tree": str(seed_tree) if seed_tree else None,
        "seed_tree_sha256": sha256(seed_tree) if seed_tree else None,
        "solver": "HiGHS " + model.version(), "hole_budget": budget,
        "seconds_limit": seconds, "node_limit": max_nodes,
        "seconds": time.monotonic() - started, "processed_lp_nodes": processed,
        "new_exact_leaves": exact_leaves, "initial": initial, "checked": checked,
        "stop_reason": stop_reason, "status": "unsat" if checked["complete"] else
            "sat" if witness is not None else "unknown",
        "holes": witness, "nodes": nodes, "root": root}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "nodes"}), flush=True)
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--holes", type=int)
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--max-nodes", type=int, default=20000)
    parser.add_argument("--seed-tree", type=Path)
    args = parser.parse_args()
    run(args.source, args.output, args.holes, args.seconds, args.max_nodes, args.seed_tree)

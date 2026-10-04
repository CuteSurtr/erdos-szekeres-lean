#!/usr/bin/env python3
"""Search the entire plane for one-point extensions of a fixed configuration.

The fixed set is checked first. A convex (k-1)-gon and a general-position new
point form a convex k-gon exactly when one polygon edge is visible from the
new point. Counterexample-guided linear arithmetic adds these forbidden regions
in batches. UNSAT concerns this fixed configuration only, not all configurations.
All candidate geometry is independently checked with exact integer arithmetic.
"""
import argparse
import hashlib
from fractions import Fraction
from itertools import combinations
import json
from math import comb, lcm
from pathlib import Path
import time

from search import convex_subset, general_position, hull, largest_convex_subset


def line(a, b):
    return (a[1] - b[1], b[0] - a[0], a[0] * b[1] - a[1] * b[0])


def evaluate(coefficients, x, y, denominator=1):
    a, b, c = coefficients
    return a * x + b * y + c * denominator


def exactly_one_visible(polygon, point):
    return sum(evaluate(line(a, polygon[(i + 1) % len(polygon)]), *point) < 0
               for i, a in enumerate(polygon)) == 1


def run(source, output, seconds=300, batch_size=128, replace_index=None, fast=False):
    import z3
    if output.exists():
        raise FileExistsError(output)
    if seconds < 1 or batch_size < 1:
        raise ValueError("Positive time and batch size required")
    data = json.loads(source.read_text())
    points = [tuple(p) for p in data["coordinates"]]
    source_count = len(points)
    k = data["gon"]
    if not all(isinstance(c, int) for p in points for c in p):
        raise ValueError("Integer input coordinates required")
    started = time.monotonic()
    if not general_position(points) or (len(largest_convex_subset(points)) >= k if fast else
                                       convex_subset(points, k) is not None):
        raise ValueError("Input must be in general position with no forbidden polygon")
    print(f"Verified input: {len(points)} points; method={'exact DP' if fast else 'all subsets'}", flush=True)
    removed = None
    if replace_index is not None:
        if not 0 <= replace_index < len(points):
            raise ValueError("Replacement index out of range")
        removed = points.pop(replace_index)
    lines = {line(a, b) for a, b in combinations(points, 2)}
    polygons = []
    for subset in combinations(points, k - 1):
        polygon = hull(subset)
        if len(polygon) == k - 1:
            edges = [line(a, polygon[(i + 1) % len(polygon)]) for i, a in enumerate(polygon)]
            polygons.append(edges)
    print(f"Found {len(polygons)} convex {k-1}-gons; starting full-plane extension search", flush=True)
    x, y = z3.Reals("new_x new_y")
    solver = z3.SolverFor("QF_LRA")
    for coefficients in lines:
        solver.add(evaluate(coefficients, x, y) != 0)
    if removed is not None:
        # Force a change of orientation pattern, not a tiny move within the old cell.
        solver.add(z3.Or([evaluate(edge, x, y) < 0 if evaluate(edge, *removed) > 0 else
                          evaluate(edge, x, y) > 0 for edge in lines]))
    constraints, rounds = set(), 0
    result = {"scope": ("replace one point outside its old order-type cell; remaining points fixed"
                        if removed is not None else
                        "one new real point; original coordinates fixed; no grid restriction"),
              "source": str(source), "source_points": source_count, "fixed_points": len(points), "gon": k,
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "replaced_index": replace_index,
              "input_general_position_verified": True, "input_avoids_gon_verified": True,
              "input_subsets_checked": None if fast else comb(source_count, k),
              "input_check": "exact dynamic program" if fast else "exhaustive subsets",
              "convex_predecessor_polygons": len(polygons),
              "verification": "exact Python integers plus Z3; not Lean-certified",
              "z3_version": z3.get_version_string(), "status": "unknown"}
    search_started = time.monotonic()
    all_lines = {coefficients for edges in polygons for coefficients in edges}
    while time.monotonic() - search_started < seconds:
        remaining = seconds - (time.monotonic() - search_started)
        solver.set(timeout=max(1, int(remaining * 1000)))
        status = solver.check()
        rounds += 1
        if status != z3.sat:
            result["status"] = str(status)
            if status == z3.unknown:
                result["reason"] = solver.reason_unknown()
            break
        model = solver.model()
        qx, qy = (Fraction(model.eval(v).as_fraction()) for v in (x, y))
        denominator = lcm(qx.denominator, qy.denominator)
        qxn, qyn = int(qx * denominator), int(qy * denominator)
        visible = {edge: evaluate(edge, qxn, qyn, denominator) < 0 for edge in all_lines}
        violations = [i for i, edges in enumerate(polygons)
                      if sum(visible[edge] for edge in edges) == 1][:batch_size]
        if not violations:
            candidate = [(a * denominator, b * denominator) for a, b in points] + [(qxn, qyn)]
            exhaustive = not fast or len(candidate) > 2 ** (k - 2)
            forbidden = (convex_subset(candidate, k) is not None if exhaustive else
                         len(largest_convex_subset(candidate)) >= k)
            if not general_position(candidate) or forbidden:
                raise AssertionError("Extension criterion disagrees with exact hull verification")
            result.update(status="sat", coordinates=candidate,
                          candidate_check="exhaustive subsets" if exhaustive else "exact dynamic program",
                          candidate_general_position_verified=True, candidate_avoids_gon_verified=True)
            break
        if any(i in constraints for i in violations):
            raise AssertionError("Solver candidate violates an already asserted cut")
        for i in violations:
            solver.add(z3.Not(z3.PbEq([(evaluate(edge, x, y) < 0, 1) for edge in polygons[i]], 1)))
            constraints.add(i)
        if rounds % 10 == 0:
            print(f"{rounds} rounds, {len(constraints)} polygon cuts", flush=True)
    else:
        result["reason"] = "time budget exhausted"
    formula_path = output.with_suffix(".smt2")
    # This formula can be replayed independently; it is not itself an UNSAT proof.
    formula_path.write_text(solver.to_smt2())
    result.update(rounds=rounds, polygon_cuts=len(constraints),
                  cut_indices=sorted(constraints), seconds=time.monotonic() - started,
                  smt_formula=str(formula_path),
                  smt_sha256=hashlib.sha256(formula_path.read_bytes()).hexdigest())
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Extension verdict: {result['status']}; {len(constraints)} cuts", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--replace-index", type=int)
    parser.add_argument("--fast", action="store_true", help="Use exact DP for below-threshold fixtures")
    args = parser.parse_args()
    run(args.source, args.output, args.seconds, args.batch_size, args.replace_index, args.fast)

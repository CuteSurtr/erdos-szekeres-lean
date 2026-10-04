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
from math import comb, gcd, lcm
from pathlib import Path
import time

from search import convex_subset, general_position, hull, largest_convex_subset


def line(a, b):
    return (a[1] - b[1], b[0] - a[0], a[0] * b[1] - a[1] * b[0])


def primitive_line(a, b):
    coefficients = line(a, b)
    divisor = gcd(*coefficients)
    if not divisor:
        raise ValueError("Distinct endpoints required")
    return tuple(c // divisor for c in coefficients)


def evaluate(coefficients, x, y, denominator=1):
    a, b, c = coefficients
    return a * x + b * y + c * denominator


def exactly_one_visible(polygon, point):
    return sum(evaluate(line(a, polygon[(i + 1) % len(polygon)]), *point) < 0
               for i, a in enumerate(polygon)) == 1


def run(source, output, seconds=300, batch_size=128, replace_index=None, fast=False,
        integer_move=False, allowed_gons=0):
    import z3
    if output.exists():
        raise FileExistsError(output)
    if seconds < 1 or batch_size < 1:
        raise ValueError("Positive time and batch size required")
    if integer_move and replace_index is None:
        raise ValueError("Integer moves are only supported for point replacement")
    if allowed_gons < 0 or (allowed_gons and replace_index is not None):
        raise ValueError("A nonnegative polygon allowance is supported only for extension")
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
    lines = {primitive_line(a, b) for a, b in combinations(points, 2)}
    polygons = []
    for subset in combinations(points, k - 1):
        polygon = hull(subset)
        if len(polygon) == k - 1:
            edges = [primitive_line(a, polygon[(i + 1) % len(polygon)]) for i, a in enumerate(polygon)]
            polygons.append(edges)
    print(f"Found {len(polygons)} convex {k-1}-gons; starting full-plane extension search", flush=True)
    x, y = (z3.Ints if integer_move else z3.Reals)("new_x new_y")
    solver = z3.SolverFor("QF_LIA" if integer_move else "QF_LRA")
    for coefficients in lines:
        solver.add(evaluate(coefficients, x, y) != 0)
    if removed is not None:
        # Force a change of orientation pattern, not a tiny move within the old cell.
        solver.add(z3.Or([evaluate(edge, x, y) < 0 if evaluate(edge, *removed) > 0 else
                          evaluate(edge, x, y) > 0 for edge in lines]))
    constraints, rounds, observed_violations = set(), 0, []
    result = {"scope": ("replace one point outside its old order-type cell; remaining points fixed"
                        if removed is not None else
                        "one new real point; original coordinates fixed; no grid restriction"),
              "source": str(source), "source_points": source_count, "fixed_points": len(points), "gon": k,
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "replaced_index": replace_index,
              "new_point_domain": "integer lattice" if integer_move else "real plane",
              "allowed_convex_gons": allowed_gons,
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
        qx, qy = (Fraction(model.eval(v).as_long()) if integer_move else
                  Fraction(model.eval(v).as_fraction()) for v in (x, y))
        denominator = lcm(qx.denominator, qy.denominator)
        qxn, qyn = int(qx * denominator), int(qy * denominator)
        visible = {edge: evaluate(edge, qxn, qyn, denominator) < 0 for edge in all_lines}
        violations = [i for i, edges in enumerate(polygons)
                      if sum(visible[edge] for edge in edges) == 1]
        if len(violations) <= allowed_gons:
            candidate = [(a * denominator, b * denominator) for a, b in points] + [(qxn, qyn)]
            exhaustive = bool(allowed_gons) or not fast or len(candidate) > 2 ** (k - 2)
            actual_count = None
            if allowed_gons:
                actual_count = sum(len(hull(subset)) == k for subset in combinations(candidate, k))
                forbidden = actual_count != len(violations)
            else:
                forbidden = (convex_subset(candidate, k) is not None if exhaustive else
                             len(largest_convex_subset(candidate)) >= k)
            if not general_position(candidate) or forbidden:
                raise AssertionError("Extension criterion disagrees with exact hull verification")
            result.update(status="near_miss" if violations else "sat", coordinates=candidate,
                          convex_gons_count=actual_count if allowed_gons else 0,
                          candidate_check="exhaustive subsets" if exhaustive else "exact dynamic program",
                          candidate_subsets_checked=comb(len(candidate), k) if exhaustive else None,
                          candidate_general_position_verified=True,
                          candidate_avoids_gon_verified=not violations)
            break
        if sum(i in constraints for i in violations) > allowed_gons:
            raise AssertionError("Solver candidate violates an already asserted cut")
        new_violations = [i for i in violations if i not in constraints][:batch_size]
        for i in new_violations:
            predicate = z3.PbEq([(evaluate(edge, x, y) < 0, 1) for edge in polygons[i]], 1)
            if allowed_gons:
                observed_violations.append(predicate)
            else:
                solver.add(z3.Not(predicate))
            constraints.add(i)
        if allowed_gons:
            solver.add(z3.AtMost(*observed_violations, allowed_gons))
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
    parser.add_argument("--integer-move", action="store_true")
    parser.add_argument("--allowed-gons", type=int, default=0,
                        help="Near-miss benchmark only; nonzero is not a counterexample")
    args = parser.parse_args()
    run(args.source, args.output, args.seconds, args.batch_size, args.replace_index, args.fast,
        args.integer_move, args.allowed_gons)

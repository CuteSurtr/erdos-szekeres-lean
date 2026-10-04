#!/usr/bin/env python3
"""Search simultaneous vertical moves with exact linear-arithmetic cuts.

All x coordinates and unselected y coordinates stay fixed. Each cut forbids
one cyclic ordering of a convex k-gon: its increasing triples cannot all have
positive orientation in a k-gon-free configuration. A final candidate is checked
independently by exhaustive hull tests. UNSAT is restricted to the chosen moves.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from math import comb, gcd, lcm
from pathlib import Path
import time

from search import convex_subset, general_position, hull, largest_convex_subset


def orientation_coefficients(points, moving, triple):
    """Coefficients of the moving y values, then the constant, divided by gcd."""
    a, b, c = triple
    weights = ((a, points[c][0] - points[b][0]),
               (b, points[a][0] - points[c][0]),
               (c, points[b][0] - points[a][0]))
    index = {vertex: i for i, vertex in enumerate(moving)}
    coefficients = [0] * (len(moving) + 1)
    for vertex, weight in weights:
        if vertex in index:
            coefficients[index[vertex]] += weight
        else:
            coefficients[-1] += weight * points[vertex][1]
    divisor = gcd(*coefficients)
    return tuple(x // divisor for x in coefficients) if divisor else tuple(coefficients)


def run(source, output, moving, seconds=120, batch_size=32):
    import z3
    if output.exists():
        raise FileExistsError(output)
    if seconds <= 0 or batch_size <= 0:
        raise ValueError("Positive time and batch size required")
    data = json.loads(source.read_text())
    points, k = list(map(tuple, data["coordinates"])), data["gon"]
    moving = tuple(sorted(moving))
    if not moving or len(set(moving)) != len(moving) or not all(0 <= i < len(points) for i in moving):
        raise ValueError("Distinct valid moving-point indices required")
    if not all(isinstance(c, int) for p in points for c in p) or not general_position(points):
        raise ValueError("Integer, general-position input required")
    started = time.monotonic()
    variables = [z3.Real(f"y_{i}") for i in moving]
    solver = z3.SolverFor("QF_LRA")
    expressions = {}
    for triple in combinations(range(len(points)), 3):
        coefficients = orientation_coefficients(points, moving, triple)
        expression = sum(a * v for a, v in zip(coefficients, variables) if a) + coefficients[-1]
        expressions[triple] = expression
        solver.add(expression != 0)

    def signed_expression(triple):
        parity = sum(triple[i] > triple[j] for i in range(3) for j in range(i + 1, 3)) % 2
        value = expressions[tuple(sorted(triple))]
        return -value if parity else value

    cuts, seen, rounds = [], set(), 0
    result = {"scope": "simultaneous y moves only; all x and other y coordinates fixed",
              "source": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "gon": k, "points": len(points), "moving_indices": moving,
              "seconds_limit": seconds, "z3_version": z3.get_version_string(),
              "verification": "exact integer geometry plus Z3; not Lean-certified", "status": "unknown"}
    while time.monotonic() - started < seconds:
        solver.set(timeout=max(1, int((seconds - (time.monotonic() - started)) * 1000)))
        verdict = solver.check()
        rounds += 1
        if verdict != z3.sat:
            result["status"] = str(verdict)
            if verdict == z3.unknown:
                result["reason"] = solver.reason_unknown()
            break
        model = solver.model()
        values = [Fraction(model.eval(v, model_completion=True).as_fraction()) for v in variables]
        denominator = lcm(*(v.denominator for v in values))
        candidate = [(x * denominator, y * denominator) for x, y in points]
        for i, y in zip(moving, values):
            candidate[i] = (points[i][0] * denominator, int(y * denominator))
        if not general_position(candidate):
            raise AssertionError("Solver model violates general position")
        witness = largest_convex_subset(candidate)
        if len(witness) < k:
            if convex_subset(candidate, k) is not None:
                raise AssertionError("DP candidate disagrees with exhaustive hull check")
            result.update(status="sat", coordinates=candidate,
                          candidate_general_position_verified=True, candidate_avoids_gon_verified=True,
                          candidate_subsets_checked=comb(len(points), k))
            break
        labels = {point: i for i, point in enumerate(candidate)}
        cycle = [labels[p] for p in hull(witness)]
        added = 0
        for selection in combinations(cycle, k):
            # Rotate to a canonical starting label; retain the CCW direction.
            offset = selection.index(min(selection))
            selection = selection[offset:] + selection[:offset]
            if selection in seen:
                raise AssertionError("Solver repeated a forbidden convex cycle")
            solver.add(z3.Or([signed_expression(triple) <= 0 for triple in combinations(selection, 3)]))
            seen.add(selection)
            cuts.append(selection)
            added += 1
            if added == batch_size:
                break
        if rounds % 25 == 0:
            print(f"{moving}: {rounds} rounds, {len(cuts)} convex-cycle cuts", flush=True)
    else:
        result["reason"] = "time budget exhausted"
    formula = output.with_suffix(".smt2")
    formula.write_text(solver.to_smt2())
    result.update(rounds=rounds, cuts=cuts, seconds=time.monotonic() - started,
                  smt_formula=str(formula), smt_sha256=hashlib.sha256(formula.read_bytes()).hexdigest())
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"{moving}: {result['status']}, {len(cuts)} cuts", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--move", type=int, nargs="+", required=True)
    parser.add_argument("--seconds", type=int, default=120)
    args = parser.parse_args()
    run(args.source, args.output, args.move, args.seconds)

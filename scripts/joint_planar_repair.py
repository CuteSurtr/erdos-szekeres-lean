#!/usr/bin/env python3
"""Joint point repair with both coordinates free and exact polynomial cuts.

Unlike joint_vertical_repair.py, this uses nonlinear real arithmetic. The
unselected points stay fixed. SAT candidates are converted to integer points
with the same orientation signs and checked exhaustively. An UNSAT result is
restricted to these selected moves; neither UNSAT nor a timeout resolves ES(7).
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from math import comb, gcd, lcm, prod
from pathlib import Path
import time

from search import convex_subset, general_position, hull, largest_convex_subset, orient


def orientation_terms(points, moving, triple):
    """Sparse degree-two polynomial, normalized by a positive coefficient gcd.

    Variable order is x_i, y_i for each selected vertex, in moving order.
    A monomial is a tuple of variable indices; () denotes the constant.
    """
    index = {(vertex, axis): 2 * j + axis
             for j, vertex in enumerate(moving) for axis in (0, 1)}

    def coordinate(vertex, axis):
        if (vertex, axis) in index:
            return {(index[vertex, axis],): 1}
        return {(): points[vertex][axis]}

    def subtract(p, q):
        out = p.copy()
        for term, coefficient in q.items():
            out[term] = out.get(term, 0) - coefficient
        return {term: coefficient for term, coefficient in out.items() if coefficient}

    def multiply(p, q):
        out = {}
        for left, a in p.items():
            for right, b in q.items():
                term = tuple(sorted(left + right))
                out[term] = out.get(term, 0) + a * b
        return out

    a, b, c = triple
    bx = subtract(coordinate(b, 0), coordinate(a, 0))
    by = subtract(coordinate(b, 1), coordinate(a, 1))
    cx = subtract(coordinate(c, 0), coordinate(a, 0))
    cy = subtract(coordinate(c, 1), coordinate(a, 1))
    terms = subtract(multiply(bx, cy), multiply(by, cx))
    divisor = gcd(*terms.values())
    return {term: coefficient // divisor for term, coefficient in terms.items()} if divisor else {}


def integer_model(points, moving, variables, model, expressions):
    """Round algebraic coordinates only after checking every orientation sign.

    General-position solutions have an open neighborhood with constant signs.
    Rational approximations are therefore suitable, but each returned witness
    is explicitly verified; finite precision alone is never accepted.
    """
    import z3
    exact = [model.eval(v, model_completion=True) for v in variables]
    positive = {triple: z3.is_true(model.eval(value > 0, model_completion=True))
                for triple, value in expressions.items()}
    algebraic = any(z3.is_algebraic_value(value) for value in exact)
    for precision in (16, 32, 64, 128, 256, 512, 1024):
        values = []
        for value in exact:
            if z3.is_rational_value(value):
                values.append(Fraction(value.as_fraction()))
            elif z3.is_algebraic_value(value):
                values.append(Fraction(value.approx(precision).as_fraction()))
            else:
                raise ValueError(f"Unexpected real model value: {value}")
        denominator = lcm(*(value.denominator for value in values))
        candidate = [(x * denominator, y * denominator) for x, y in points]
        for j, i in enumerate(moving):
            candidate[i] = (int(values[2 * j] * denominator),
                            int(values[2 * j + 1] * denominator))
        if all((area := orient(*(candidate[i] for i in triple))) != 0 and
               (area > 0) == sign for triple, sign in positive.items()):
            if not general_position(candidate):
                raise AssertionError("Orientation-verified model is not in general position")
            return candidate, {"algebraic_model": algebraic,
                               "coordinate_scale": denominator,
                               "rationalization_precision": precision if algebraic else None}
    raise ValueError("No rational approximation preserved all orientation signs within the precision limit")


def run(source, output, moving, seconds=120, batch_size=32, seed=0, resume=None, seed_cuts=()):
    import z3
    if output.exists() or output.with_suffix(".smt2").exists():
        raise FileExistsError(output)
    if seconds <= 0 or batch_size <= 0:
        raise ValueError("Positive time and batch size required")
    data = json.loads(source.read_text())
    points, k = list(map(tuple, data["coordinates"])), data["gon"]
    moving = tuple(sorted(moving))
    if not moving or len(set(moving)) != len(moving) or not all(0 <= i < len(points) for i in moving):
        raise ValueError("Distinct valid moving-point indices required")
    if not 3 <= k <= len(points):
        raise ValueError("Require 3 <= gon <= number of points")
    if not all(len(p) == 2 and all(isinstance(c, int) for c in p) for p in points) or not general_position(points):
        raise ValueError("Integer, general-position input required")
    started = time.monotonic()
    variables = [z3.Real(f"{axis}_{i}") for i in moving for axis in ("x", "y")]
    solver = z3.SolverFor("QF_NRA")
    solver.set(random_seed=seed)
    expressions = {}
    for triple in combinations(range(len(points)), 3):
        terms = orientation_terms(points, moving, triple)
        expression = z3.Sum([z3.RealVal(coefficient) * prod(variables[j] for j in monomial)
                             for monomial, coefficient in terms.items()])
        expressions[triple] = expression
        solver.add(expression != 0)

    def signed_expression(triple):
        parity = sum(triple[i] > triple[j] for i in range(3) for j in range(i + 1, 3)) % 2
        value = expressions[tuple(sorted(triple))]
        return -value if parity else value

    cuts, seen, rounds = [], set(), 0
    moving_set = set(moving)

    def add_cycle(selection):
        if (len(selection) != k or len(set(selection)) != k or
                not all(isinstance(i, int) and 0 <= i < len(points) for i in selection)):
            raise ValueError("A convex-cycle cut must contain exactly k distinct valid labels")
        offset = selection.index(min(selection))
        selection = tuple(selection[offset:]) + tuple(selection[:offset])
        if selection in seen:
            return False
        if any(moving_set.isdisjoint(triple) and orient(*(points[i] for i in triple)) <= 0
               for triple in combinations(selection, 3)):
            return False  # A fixed nonpositive triple already satisfies this clause.
        # This is valid for any ordering of k distinct labels: if all its
        # ordered triples are positive, these vertices form a convex k-gon.
        solver.add(z3.Or([signed_expression(triple) <= 0 for triple in combinations(selection, 3)]))
        seen.add(selection)
        cuts.append(selection)
        return True

    previous = None
    if resume is not None:
        previous = json.loads(resume.read_text())
        if (previous.get("source_sha256") != hashlib.sha256(source.read_bytes()).hexdigest() or
                previous.get("moving_indices") != list(moving) or previous.get("gon") != k or
                previous.get("logic") != "QF_NRA" or previous.get("status") != "unknown"):
            raise ValueError("Resume requires a matching inconclusive planar search")
        # Reconstruct validated cuts instead of trusting arbitrary SMT assertions.
        for selection in previous["cuts"]:
            add_cycle(selection)
    inherited_cuts = len(cuts)
    seed_sources = []
    for path in seed_cuts:
        data = json.loads(path.read_text())
        records = data["attempts"] if "attempts" in data else [data]
        supplied = added = 0
        for record in records:
            if record.get("gon") != k or record.get("points") != len(points):
                raise ValueError("Seed cuts must use the same number of point labels and polygon size")
            for selection in record["cuts"]:
                supplied += 1
                added += add_cycle(selection)
        seed_sources.append({"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                             "supplied_cuts": supplied, "retained_new_cuts": added})

    def exclude_witness(candidate, witness, allow_existing=False):
        labels = {point: i for i, point in enumerate(candidate)}
        cycle = [labels[p] for p in hull(witness)]
        for added, selection in enumerate(combinations(cycle, k), 1):
            if not add_cycle(selection) and not allow_existing:
                raise AssertionError("Solver repeated a forbidden convex cycle")
            if added == batch_size:
                break

    # The original forbidden polygon supplies a useful cut before the first solve.
    initial = largest_convex_subset(points)
    if len(initial) >= k:
        exclude_witness(points, initial, allow_existing=True)
    result = {"scope": "both coordinates of selected points range over the real plane; other points fixed",
              "source": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "gon": k, "points": len(points), "moving_indices": moving,
              "seconds_limit": seconds, "seed": seed, "logic": "QF_NRA",
              "z3_version": z3.get_version_string(),
              "seed_cut_sources": seed_sources,
              "verification": "exact integer geometry plus Z3; not Lean-certified", "status": "unknown"}
    if resume is not None:
        result.update(resumed_from=str(resume),
                      resumed_sha256=hashlib.sha256(resume.read_bytes()).hexdigest(),
                      inherited_cuts=inherited_cuts)
    algebraic_models = 0
    while time.monotonic() - started < seconds:
        solver.set(timeout=max(1, int((seconds - (time.monotonic() - started)) * 1000)))
        verdict = solver.check()
        rounds += 1
        if verdict != z3.sat:
            result["status"] = str(verdict)
            if verdict == z3.unknown:
                result["reason"] = solver.reason_unknown()
            break
        try:
            candidate, metadata = integer_model(points, moving, variables, solver.model(), expressions)
        except ValueError as error:
            result["reason"] = str(error)
            break
        algebraic_models += metadata["algebraic_model"]
        witness = largest_convex_subset(candidate)
        if len(witness) < k:
            if convex_subset(candidate, k) is not None:
                raise AssertionError("Dynamic program disagrees with exhaustive hull verification")
            result.update(status="sat", coordinates=candidate,
                          candidate_general_position_verified=True, candidate_avoids_gon_verified=True,
                          candidate_subsets_checked=comb(len(points), k), **metadata)
            break
        exclude_witness(candidate, witness)
        if rounds % 10 == 0:
            print(f"{moving}: {rounds} rounds, {len(cuts)} convex-cycle cuts", flush=True)
    else:
        result["reason"] = "time budget exhausted"
    formula = output.with_suffix(".smt2")
    formula.write_text(solver.to_smt2())
    result.update(rounds=rounds, cuts=cuts, algebraic_models_rounded=algebraic_models,
                  seconds=time.monotonic() - started,
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
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--resume", type=Path, help="Reuse validated cuts from a matching unknown result")
    parser.add_argument("--seed-cuts", type=Path, nargs="+", default=[],
                        help="Reuse universally valid cycle cuts from other searches on N labels")
    args = parser.parse_args()
    run(args.source, args.output, args.move, args.seconds, seed=args.seed,
        resume=args.resume, seed_cuts=args.seed_cuts)

#!/usr/bin/env python3
"""Final validation of the existing lift model, not a new lift search.

Independent exact geometry reconstructs the input, checks the linear
obstruction, and evaluates encoder variables on explicitly built integer
clusters. The builder is imported only for the formula under test.
"""

import hashlib
import itertools
import json
import math
import resource
import time
from fractions import Fraction
from pathlib import Path

from independent_audit import build as independent_geometry, determinant
from lift_cluster_cnf import build as formula_under_test


ROOT = Path(__file__).resolve().parent


def boundary(points, vertices):
    order = sorted(vertices, key=lambda p: points[p][0])
    lower, upper = [], []
    for acc, seq in ((lower, order), (upper, reversed(order))):
        for p in seq:
            while len(acc) > 1 and determinant(points, (*acc[-2:], p)) < 0:
                acc.pop()
            acc.append(p)
    return lower[:-1] + upper[:-1], lower


def concrete_assignment(points, target, cnf, metadata, states):
    chosen = [metadata["point_choices"][p][j] for p, j in enumerate(states)]
    slopes = [None if row["slope"] is None else Fraction(row["slope"]) for row in chosen]
    denominator = math.lcm(*(s.denominator for s in slopes if s is not None))
    eps_den = 2**256
    scale = denominator * eps_den**2
    clusters, actual = [], []
    for (x, y), t in zip(points, slopes):
        ids = []
        for a in range(1 if t is None else target - 5):
            ids.append(len(actual))
            actual.append((x * scale + a * denominator * eps_den,
                           y * scale + (0 if t is None else t.numerator * (denominator // t.denominator) * a * eps_den)
                           + a * a * denominator))
        clusters.append(ids)
    assert all(determinant(actual, t) for t in itertools.combinations(range(len(actual)), 3))
    projection = {q: p for p, ids in enumerate(clusters) for q in ids}
    # Distinct-cluster orientation preservation, checked on every representative choice.
    for triple in itertools.combinations(range(len(points)), 3):
        sign = determinant(points, triple) > 0
        for selected in itertools.product(*(clusters[p] for p in triple)):
            assert (determinant(actual, selected) > 0) == sign
    true = {row["variable"] for row in chosen}
    for (chain, p, kind), var in cnf.event_map.items():
        if len(clusters[p]) == 1:
            continue
        expanded = []
        for q in chain:
            if q == p:
                expanded.extend(clusters[q] if kind == "cup" else [clusters[q][0], clusters[q][-1]])
            else:
                expanded.append(clusters[q][0])
        signs = [determinant(actual, expanded[j:j + 3]) for j in range(len(expanded) - 2)]
        if all(s > 0 for s in signs) if kind == "cup" else all(s < 0 for s in signs):
            true.add(var)
    checked = 0
    for h in metadata["polygons"]:
        ids = [q for p in h["vertices"] for q in clusters[p]]
        hull, lower = boundary(actual, ids)
        predicted = len(h["vertices"])
        predicted += (target - 6) * sum(cnf.event_map[(tuple(h["lower"]), p, "cup")] in true for p in h["lower"])
        predicted += sum(cnf.event_map[(tuple(h["upper"]), p, "cap")] in true for p in h["upper"])
        assert len(hull) == predicted
        assert set(projection[q] for q in lower) == set(h["lower"])
        if len(hull) >= target - 1:
            true.add(h["full_variable"])
        checked += 1
    false = [c for c in cnf.clauses if not any((v > 0 and v in true) or (v < 0 and -v not in true) for v in c)]
    return {"cluster_points": len(actual), "hull_capacities_checked": checked,
            "false_clause_count": len(false)}, false


def main():
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
    start = time.monotonic()
    probe = json.loads((ROOT / "lift_probe.json").read_text())
    points = probe["P"]
    caps, gons = independent_geometry(points, 6)
    lower = set(gons.values())
    assert (len(caps), len(gons), len(lower)) == (80, 216, 103)
    for carrier in probe["carriers"]:
        assert gons[frozenset(carrier["gon"])] == frozenset(carrier["lower"])
    coefficients = [Fraction(0) for _ in points]
    rhs = Fraction(0)
    for term in probe["rational_inconsistency"]:
        assert frozenset(term["lower"]) in lower
        c = Fraction(term["coefficient"])
        rhs += c
        for p in term["lower"]:
            coefficients[p] += c
    assert not any(coefficients) and rhs == 1
    controls, original_checks = [], []
    for target, name in ((7, "binary"), (8, "ternary")):
        cnf, meta = formula_under_test(points, target)
        text = f"p cnf {cnf.variables} {len(cnf.clauses)}\n" + "".join(
            " ".join(map(str, c)) + " 0\n" for c in sorted(cnf.clauses))
        assert text.encode() == (ROOT / f"lift_{name}.cnf").read_bytes()
        assert (ROOT / f"lift_{name}.cake.out").read_text().splitlines() == ["s VERIFIED UNSAT"]
        # Fixed coordinate controls, not a search over point sets or models.
        single, failures = concrete_assignment(points, target, cnf, meta, [0] * len(points))
        full_vars = {h["full_variable"] for h in meta["polygons"]}
        assert failures and all(c and set(c) <= full_vars for c in failures)
        mixed, _ = concrete_assignment(points, target, cnf, meta,
                                        [0 if p % 3 == 0 else 1 + (3 * p) % (len(meta["point_choices"][p]) - 1)
                                         for p in range(len(points))])
        original_checks.append({"target": target, "all_single": single, "fixed_mixed": mixed})
        parabola = [(i, i * i) for i in range(5)]
        control, info = formula_under_test(parabola, target)
        states = [0] * 5
        states[2] = next(i for i, row in enumerate(info["point_choices"][2]) if row["slope"] == "4")
        report, failures = concrete_assignment(parabola, target, control, info, states)
        assert not failures, "Known real lift rejected by encoder"
        controls.append({"target": target, "original_points": parabola, "duplicated_point": 2, **report})
    result = {"label": "COMPUTED", "original_geometry": {"cap4": len(caps), "pentagons": len(gons), "lower": len(lower)},
              "linear_certificate": "verified exact rational 0 = 1", "positive_controls": controls,
              "coordinate_capacity_controls": original_checks, "cnfs_regenerated_byte_identically": True,
              "cake_lines_exact": True, "elapsed_seconds": time.monotonic() - start,
              "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT / "lift_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

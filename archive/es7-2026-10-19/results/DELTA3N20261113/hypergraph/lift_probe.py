#!/usr/bin/env python3
"""Bounded, deterministic local-duplication tests; no random search or optimizer."""

import argparse
import hashlib
import itertools
import json
import resource
import time
from fractions import Fraction
from pathlib import Path

from obstruction_check import bits, geometry


def exact_one_core(m, lower):
    candidates = set(range(1 << m))
    used = []
    for edge in lower:
        candidates = {t for t in candidates if (t & edge).bit_count() == 1}
        used.append(edge)
        if not candidates:
            break
    if candidates:
        return {"solutions": [bits(t) for t in sorted(candidates)], "core": []}
    # Delete constraints while preserving inconsistency. This is a finite
    # 2^15 exact-one check, not minimum-transversal optimization.
    def models(edges):
        return [t for t in range(1 << m) if all((t & e).bit_count() == 1 for e in edges)]
    for e in list(used):
        trial = [f for f in used if f != e]
        if not models(trial):
            used = trial
    return {"solutions": [], "core": [bits(e) for e in used],
            "core_deletion_witnesses": [bits(models([f for f in used if f != e])[0]) for e in used]}


def rational_inconsistency(m, lower):
    """Return an exact linear combination of sum_{p in C} x_p = 1 giving 0=1, if present."""
    basis = {}
    for j, edge in enumerate(lower):
        row = [Fraction(bool(edge & (1 << p))) for p in range(m)] + [Fraction(1)]
        combination = {j: Fraction(1)}
        for pivot, (base, coefficients) in sorted(basis.items()):
            scale = row[pivot]
            if scale:
                row = [a - scale * b for a, b in zip(row, base)]
                for k, v in coefficients.items():
                    combination[k] = combination.get(k, Fraction(0)) - scale * v
                combination = {k: v for k, v in combination.items() if v}
        pivot = next((p for p in range(m) if row[p]), None)
        if pivot is None:
            if row[-1]:
                norm = row[-1]
                return [{"lower": bits(lower[k]), "coefficient": str(v / norm)}
                        for k, v in sorted(combination.items())]
        else:
            norm = row[pivot]
            basis[pivot] = ([x / norm for x in row], {k: v / norm for k, v in combination.items()})
    return None


def slope(points, i, j):
    return Fraction(points[j][1] - points[i][1], points[j][0] - points[i][0])


def tangent_intervals(points, lower, carriers, caps):
    answer = []
    for p in range(len(points)):
        lower_bounds, upper_bounds = [], []
        for e in lower:
            chain = bits(e)
            if p not in chain:
                continue
            j = chain.index(p)
            if j:
                lower_bounds.append((slope(points, chain[j - 1], p), chain))
            if j + 1 < len(chain):
                upper_bounds.append((slope(points, p, chain[j + 1]), chain))
        low = max(lower_bounds, default=None, key=lambda item: item[0])
        high = min(upper_bounds, default=None, key=lambda item: item[0])
        possible = low is None or high is None or low[0] < high[0]
        entry = {"p": p, "cup_interval_nonempty": possible,
                 "lower_bound": None if low is None else str(low[0]),
                 "upper_bound": None if high is None else str(high[0]),
                 "lower_witness": None if low is None else low[1],
                 "upper_witness": None if high is None else high[1]}
        cuts = sorted(set(slope(points, q, p) for q in range(len(points)) if q != p))
        samples = [cuts[0] - 1] + [(a + b) / 2 for a, b in zip(cuts, cuts[1:])] + [cuts[-1] + 1]
        feasible = []
        for t in samples:
            if low is not None and t <= low[0] or high is not None and t >= high[0]:
                continue
            creates_cap5 = False
            for k in caps:
                chain = bits(k)
                if p not in chain:
                    continue
                j = chain.index(p)
                incoming = None if j == 0 else slope(points, chain[j - 1], p)
                outgoing = None if j == len(chain) - 1 else slope(points, p, chain[j + 1])
                if (incoming is None or t < incoming) and (outgoing is None or t > outgoing):
                    creates_cap5 = True
                    break
            if not creates_cap5:
                feasible.append(str(t))
        entry["all_cup_chains_and_no_single_cap4_extension_slopes"] = feasible
        answer.append(entry)
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
    start = time.monotonic()
    raw = args.input.read_bytes()
    source = json.loads(raw)
    points = source["P"]
    assert len(points) == 15 and source["n"] == 6
    caps, gons, triples = geometry(points, 6)
    carriers = {}
    for g, lo, up in gons:
        carriers.setdefault(lo, {"gon": bits(g), "upper": bits(up)})
    lower = sorted(carriers)
    exact_one = exact_one_core(len(points), lower)
    linear = rational_inconsistency(len(points), lower)
    output = {"label": "COMPUTED", "source": str(args.input),
              "source_sha256": hashlib.sha256(raw).hexdigest(), "P": points,
              "cap4_count": len(caps), "pentagon_count": len(gons), "lower_count": len(lower),
              "exact_one": exact_one, "rational_inconsistency": linear,
              "tangents": tangent_intervals(points, lower, carriers, caps),
              "carriers": [{"lower": bits(e), **carriers[e]} for e in lower],
              "elapsed_seconds": time.monotonic() - start,
              "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k not in ("P", "carriers", "tangents")}, indent=2))
    print(json.dumps({"cup_interval_nonempty": [r["p"] for r in output["tangents"] if r["cup_interval_nonempty"]],
                      "cup_and_cap4_compatible": [r["p"] for r in output["tangents"]
                        if r["all_cup_chains_and_no_single_cap4_extension_slopes"]]}))


if __name__ == "__main__":
    main()

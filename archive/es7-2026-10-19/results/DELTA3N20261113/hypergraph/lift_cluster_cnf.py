#!/usr/bin/env python3
"""Exact finite model for infinitesimal cup-cluster lifts of a fixed real set.

Each point stays single or becomes r=target-5 nearby cup points with a generic
tangent slope. Emits CNF only; this program does not launch a solver.
Coverage may use ANY original convex 3/4/5-set whose lower chain is contained
in the old target chain, not only that chain's original pentagon carriers.
"""

import argparse
import hashlib
import itertools
import json
import resource
import time
from fractions import Fraction
from pathlib import Path

from obstruction_check import bits, geometry, hull, mask, orient


class CNF:
    def __init__(self):
        self.variables = 0
        self.clauses = set()

    def variable(self):
        self.variables += 1
        return self.variables

    def add(self, clause):
        clause = frozenset(clause)
        if not any(-v in clause for v in clause):
            self.clauses.add(tuple(sorted(clause)))

    def at_most(self, literals, bound):
        if bound < 0:
            self.add([])
        elif bound < len(literals):
            for subset in itertools.combinations(literals, bound + 1):
                self.add([-v for v in subset])

    def implies_at_least(self, indicator, literals, bound):
        if bound > len(literals):
            self.add([-indicator])
        elif bound > 0:
            for subset in itertools.combinations(literals, len(literals) - bound + 1):
                self.add([-indicator, *subset])


def build(points, target):
    r = target - 5
    assert r in (2, 3)
    caps, pentagons, _ = geometry(points, 6)
    old_lower = sorted(set(lo for _, lo, _ in pentagons))
    m = len(points)

    def slope(i, j):
        return Fraction(points[j][1] - points[i][1], points[j][0] - points[i][0])

    cnf = CNF()
    choices = []
    for p in range(m):
        cuts = sorted(set(slope(p, q) for q in range(m) if q != p))
        slopes = [cuts[0] - 1] + [(a + b) / 2 for a, b in zip(cuts, cuts[1:])] + [cuts[-1] + 1]
        row = [(cnf.variable(), None)] + [(cnf.variable(), s) for s in slopes]
        choices.append(row)
        cnf.add(v for v, _ in row)
        cnf.at_most([v for v, _ in row], 1)
    events = {}

    def visible(chain, p, kind):
        key = (tuple(chain), p, kind)
        if key in events:
            return events[key]
        j = chain.index(p)
        incoming = None if j == 0 else slope(chain[j - 1], p)
        outgoing = None if j == len(chain) - 1 else slope(p, chain[j + 1])
        selected = []
        for var, t in choices[p]:
            if t is None:
                continue
            if kind == "cup":
                good = (incoming is None or incoming < t) and (outgoing is None or t < outgoing)
            else:
                good = (incoming is None or incoming > t) and (outgoing is None or t > outgoing)
            if good:
                selected.append(var)
        v = cnf.variable()
        for choice in selected:
            cnf.add([-choice, v])
        cnf.add([-v, *selected])
        events[key] = v
        return v

    # A cup cluster contributes at most two points to a cap, for either r.
    for k in caps:
        chain = bits(k)
        for p in chain:
            cnf.add([-visible(chain, p, "cap")])
    cap3_count = 0
    for chain in itertools.combinations(range(m), 3):
        if orient(points, *chain) < 0:
            cap3_count += 1
            cnf.at_most([visible(chain, p, "cap") for p in chain], 1)

    polygons = []
    for size in (3, 4, 5):
        for vertices in itertools.combinations(range(m), size):
            boundary, lower, upper = hull(points, vertices)
            if len(boundary) != size:
                continue
            weighted = []
            for p in lower:
                weighted.extend([visible(lower, p, "cup")] * (r - 1))
            for p in upper:
                weighted.append(visible(upper, p, "cap"))
            bound = target - 1 - size
            cnf.at_most(weighted, bound)
            full = cnf.variable()
            cnf.implies_at_least(full, weighted, bound)
            polygons.append({"vertices": list(vertices), "lower": lower,
                             "upper": upper, "full_variable": full})

    for old in old_lower:
        candidates = [h["full_variable"] for h in polygons if mask(h["lower"]) & old == mask(h["lower"])]
        assert candidates
        cnf.add(candidates)
    metadata = {"target_n": target, "cluster_size": r, "m": m,
                "variables": cnf.variables, "clauses": len(cnf.clauses),
                "old_fourcaps": len(caps), "old_cap3": cap3_count,
                "old_pentagons": len(pentagons), "old_lower_chains": len(old_lower),
                "projection_polygons": len(polygons),
                "point_choices": [[{"variable": v, "slope": None if s is None else str(s)}
                                   for v, s in row] for row in choices],
                "polygons": polygons}
    cnf.event_map = events  # Used only by the exact-coordinate positive controls.
    return cnf, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--target", type=int, choices=(7, 8), required=True)
    parser.add_argument("--prefix", type=Path, required=True)
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
    start = time.monotonic()
    raw = args.input.read_bytes()
    source = json.loads(raw)
    cnf, metadata = build(source["P"], args.target)
    path = args.prefix.with_suffix(".cnf")
    with path.open("w") as f:
        f.write(f"p cnf {cnf.variables} {len(cnf.clauses)}\n")
        for clause in sorted(cnf.clauses):
            f.write(" ".join(map(str, clause)) + " 0\n")
    metadata.update({"label": "COMPUTED", "source": str(args.input),
                     "source_sha256": hashlib.sha256(raw).hexdigest(), "P": source["P"],
                     "cnf_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                     "elapsed_seconds": time.monotonic() - start,
                     "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    args.prefix.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps({k: v for k, v in metadata.items() if k not in ("P", "point_choices", "polygons")}, indent=2))


if __name__ == "__main__":
    main()

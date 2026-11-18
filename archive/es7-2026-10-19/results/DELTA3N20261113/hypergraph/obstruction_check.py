#!/usr/bin/env python3
"""Exact, bounded checks for mixed cap/gon coloring; Python standard library only.

No SAT solver or UNSAT certificate is used. All reported enumeration is COMPUTED.
The CLI checks explicitly supplied coordinate fixtures, not a search queue.
"""

import argparse
import itertools
import json
import resource
import time
from collections import deque
from pathlib import Path


def bits(mask):
    return [i for i in range(mask.bit_length()) if mask & (1 << i)]


def mask(vertices):
    return sum(1 << i for i in vertices)


def orient(points, i, j, k):
    a, b, c = (points[t] for t in (i, j, k))
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def hull(points, vertices):
    vertices = sorted(vertices)
    lower, upper = [], []
    for target, order in ((lower, vertices), (upper, reversed(vertices))):
        for i in order:
            while len(target) >= 2 and orient(points, target[-2], target[-1], i) <= 0:
                target.pop()
            target.append(i)
    return lower[:-1] + upper[:-1], lower, list(reversed(upper))


def geometry(points, n):
    assert all(isinstance(z, int) for p in points for z in p)
    assert all(points[i][0] < points[i + 1][0] for i in range(len(points) - 1))
    triples = {t: orient(points, *t) for t in itertools.combinations(range(len(points)), 3)}
    assert all(triples.values()), "Not in general position"
    caps = {}
    for k in (4, 5):
        caps[k] = [mask(t) for t in itertools.combinations(range(len(points)), k)
                   if all(triples[u] < 0 for u in itertools.combinations(t, 3))]
    gons, forbidden = [], []
    for k in (n - 1, n):
        for t in itertools.combinations(range(len(points)), k):
            boundary, lower, upper = hull(points, t)
            if len(boundary) == k:
                if k == n:
                    forbidden.append(mask(t))
                else:
                    gons.append((mask(t), mask(lower), mask(upper)))
    assert not caps[5] and not forbidden, "Fixture is not (5,n)-valid"
    return caps[4], gons, triples


def works(red, caps, positive):
    return not any(red & c == c for c in caps) and all(red & e for e in positive)


def peel(caps, positive):
    """Blocked-clause elimination via singleton intersections; reconstruct if empty."""
    edges = [sorted(set(caps)), sorted(set(positive))]
    active = [(1 << len(side)) - 1 for side in edges]
    occurrence = []
    for side in edges:
        occ = {}
        for j, edge in enumerate(side):
            for p in bits(edge):
                occ[p] = occ.get(p, 0) | (1 << j)
        occurrence.append(occ)
    neighbors = [[], []]
    for side in (0, 1):
        for edge in edges[side]:
            incidence = {}
            for p in bits(edge):
                opposite = occurrence[1 - side].get(p, 0)
                for q in bits(edge & ~(1 << p)):
                    opposite &= ~occurrence[1 - side].get(q, 0)
                incidence[p] = opposite
            neighbors[side].append(incidence)

    def free_pivot(side, j):
        return next((p for p, others in neighbors[side][j].items()
                     if not others & active[1 - side]), None)

    queue = deque((side, j) for side in (0, 1) for j in range(len(edges[side]))
                  if free_pivot(side, j) is not None)
    trace = []
    while queue:
        side, j = queue.popleft()
        if not active[side] & (1 << j):
            continue
        p = free_pivot(side, j)
        assert p is not None
        active[side] &= ~(1 << j)
        trace.append((side, edges[side][j], p))
        affected = 0
        for others in neighbors[side][j].values():
            affected |= others
        affected &= active[1 - side]
        while affected:
            bit = affected & -affected
            k = bit.bit_length() - 1
            affected ^= bit
            if free_pivot(1 - side, k) is not None:
                queue.append((1 - side, k))
    remaining = [{edges[side][j] for j in bits(active[side])} for side in (0, 1)]
    red = None
    if not any(remaining):
        red = 0
        for side, edge, p in reversed(trace):
            if side == 0 and red & edge == edge:
                red &= ~(1 << p)
            if side == 1 and not red & edge:
                red |= 1 << p
        assert works(red, caps, positive)
    report = {"deleted_clauses": len(trace), "remaining_caps": len(remaining[0]),
              "remaining_positive": len(remaining[1]),
              "reconstructed_red": None if red is None else bits(red)}
    if any(remaining):
        assert all(any(edge & other == 1 << p for other in remaining[1 - side])
                   for side in (0, 1) for edge in remaining[side] for p in bits(edge))
        root = min(remaining[0])
        report["root_cap"] = bits(root)
        report["singleton_partners"] = [bits(min(e for e in remaining[1] if e & root == 1 << p))
                                        for p in bits(root)]
    return report, remaining


def one_recolor_obstruction(m, caps, gons, mode):
    """Disprove universal extension with at most one change to an old color.

    Deletion instances use full gon supports, including for cup-side edges.
    Enumerates all full colorings once, then each one-point deletion.
    """
    positive = sorted(set(g if mode == "weak" else lo for g, lo, _ in gons))
    full = [r for r in range(1 << m) if works(r, caps, positive)]
    assert full, "No full coloring found: investigate; not certified UNSAT"
    for p in range(m):
        bit = 1 << p
        projection = {r & ~bit for r in full}
        distance_at_most_one = set(projection)
        for r in projection:
            distance_at_most_one.update(r ^ (1 << q) for q in range(m) if q != p)
        subcaps = [c for c in caps if not c & bit]
        subpositive = sorted(set(g if mode == "weak" else lo
                                for g, lo, _ in gons if not g & bit))
        for r in range(1 << m):
            if r & bit or r in distance_at_most_one or not works(r, subcaps, subpositive):
                continue
            nearest = min(full, key=lambda s: ((s & ~bit) ^ r).bit_count())
            dist = ((nearest & ~bit) ^ r).bit_count()
            negative_blockers = [c for c in caps if c & (r | bit) == c]
            positive_blockers = [e for e in positive if not r & e]
            # Every one-recolor extension is accompanied by an explicit violated clause.
            failures = []
            for q in [None] + [q for q in range(m) if q != p]:
                for new_p in (0, 1):
                    candidate = r if q is None else r ^ (1 << q)
                    if new_p:
                        candidate |= bit
                    badcap = next((c for c in caps if candidate & c == c), None)
                    badpositive = next((e for e in positive if not candidate & e), None)
                    assert badcap is not None or badpositive is not None
                    failures.append({"flip_old": q, "hole_red": bool(new_p),
                                     "violated_type": "cap" if badcap is not None else mode,
                                     "violated_edge": bits(badcap if badcap is not None else badpositive)})
            return {"hole": p, "red": bits(r), "blue": bits(((1 << m) - 1) & ~(r | bit)),
                    "minimum_old_recolorings": dist, "nearest_full_red": bits(nearest),
                    "red_blockers": [bits(c) for c in negative_blockers],
                    "blue_blockers": [bits(e) for e in positive_blockers],
                    "all_one_recolor_failures": failures,
                    "full_colorings": len(full)}
    return {"found": False, "full_colorings": len(full)}


def analyze(path, peel_only=False):
    source = json.loads(path.read_text())
    if isinstance(source, list):
        raise ValueError("Use an object with integer P and polygon parameter n")
    points, n = source["P"], source["n"]
    caps, gons, triples = geometry(points, n)
    output = {"label": "COMPUTED", "source": str(path), "P": points, "n": n,
              "point_count": len(points), "cap4_count": len(caps), "gon_count": len(gons),
              "cap5_count": 0, "gon_n_count": 0,
              "minimum_absolute_orientation": min(map(abs, triples.values())), "modes": {}}
    for mode in ("weak", "cup"):
        positive = sorted(set(g if mode == "weak" else lo for g, lo, _ in gons))
        report, _ = peel(caps, positive)
        output["modes"][mode] = {"positive_edges": len(positive), "peeling": report}
        if not peel_only:
            assert len(points) <= 16, "Full-coloring enumeration is restricted to at most 16 points"
            output["modes"][mode]["one_recolor"] = one_recolor_obstruction(len(points), caps, gons, mode)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--peel-only", action="store_true", help="Skip all-coloring enumeration")
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
    start = time.monotonic()
    results = [analyze(path, args.peel_only) for path in args.input]
    args.output.write_text(json.dumps({"label": "COMPUTED", "results": results}, indent=2) + "\n")
    for result in results:
        print(json.dumps({k: v for k, v in result.items() if k not in ("P", "modes")}))
        for mode, report in result["modes"].items():
            small = {k: v for k, v in report.get("one_recolor", {}).items()
                     if k not in ("red_blockers", "blue_blockers", "all_one_recolor_failures")}
            print(json.dumps({"mode": mode, "peeling": report["peeling"], "one_recolor": small}))
    print(json.dumps({"elapsed_seconds": time.monotonic() - start,
                      "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()

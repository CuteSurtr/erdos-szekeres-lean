#!/usr/bin/env python3
"""Independent exact audit: no imports from the extraction/search programs.

Convexity uses point-in-triangle tests on four-subsets, not a hull routine.
Caps use consecutive determinants, not all-triple tests. No SAT or optimizer.
"""

import itertools
import json
import resource
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def determinant(points, triple):
    a, b, c = [points[i] for i in triple]
    return a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])


def build(points, n):
    m = len(points)
    assert all(points[i][0] < points[i + 1][0] for i in range(m - 1))
    assert all(determinant(points, t) != 0 for t in itertools.combinations(range(m), 3))

    def cap(t):
        return all(determinant(points, t[i:i + 3]) < 0 for i in range(len(t) - 2))

    caps = [frozenset(t) for t in itertools.combinations(range(m), 4) if cap(t)]
    assert not any(cap(t) for t in itertools.combinations(range(m), 5))
    bad4 = set()
    for t in itertools.combinations(range(m), 4):
        for p in t:
            a, b, c = [q for q in t if q != p]
            signs = [determinant(points, (a, b, p)), determinant(points, (b, c, p)),
                     determinant(points, (c, a, p))]
            if all(s > 0 for s in signs) or all(s < 0 for s in signs):
                bad4.add(t)
                break

    def convex(t):
        return all(q not in bad4 for q in itertools.combinations(t, 4))

    assert not any(convex(t) for t in itertools.combinations(range(m), n))
    gons = {}
    for t in itertools.combinations(range(m), n - 1):
        if convex(t):
            lo = frozenset((t[0], t[-1])) | frozenset(
                p for p in t[1:-1] if determinant(points, (t[0], p, t[-1])) > 0)
            up = frozenset(t) - lo | frozenset((t[0], t[-1]))
            assert all(determinant(points, q) > 0 for q in itertools.combinations(sorted(lo), 3))
            assert all(determinant(points, q) < 0 for q in itertools.combinations(sorted(up), 3))
            gons[frozenset(t)] = lo
    return caps, gons


def good(red, caps, positive):
    return not any(c <= red for c in caps) and all(e & red for e in positive)


def audit_four_state(path):
    data = json.loads(path.read_text())
    points, n, target = data["P"], data["n"], frozenset(data["T"])
    caps, gons = build(points, n)
    lower = set(gons.values())
    assert len(caps) == data["cap4_count"]
    assert len(gons) == data["gon_count"]
    assert len(lower) == data["lower_count"]
    assert target in caps and all(target & e for e in lower)
    universe = frozenset(range(len(points)))
    for fan in data["fans"]:
        p = fan["pivot"]
        common = universe
        for witness in fan["witnesses"]:
            e, h = frozenset(witness["lower"]), frozenset(witness["gon"])
            assert gons[h] == e and e & target == {p}
            common &= e
        assert common == {p}

    # Directly check every proposed extension and every one-hole move.
    transitions = []
    for p in target:
        red = target - {p}
        assert not any(c <= red for c in caps)
        assert all(e & red or p in e for e in lower)
        assert not good(red, caps, lower) and not good(target, caps, lower)
        allowed = []
        for q in universe - {p}:
            new_red = red - {q} | {p} if q in red else red
            proper = not any(c <= new_red for c in caps) and all(e & new_red or q in e for e in lower)
            assert proper == (q in target)
            if proper:
                allowed.append(q)
        transitions.append({"hole": p, "allowed_next_holes": sorted(allowed)})
    if "known_cap_free_transversal" in data:
        assert good(frozenset(data["known_cap_free_transversal"]), caps, lower)
    elif "larger_cap_free_transversal" in data:
        assert good(frozenset(data["larger_cap_free_transversal"]), caps, lower)
    compatible = data.get("compatible_four_point_red")
    if compatible is not None:
        assert len(compatible) == 4 and good(frozenset(compatible), caps, lower)
    return {"file": path.name, "m": len(points), "cap4_count": len(caps),
            "gon_count": len(gons), "lower_count": len(lower),
            "fan_count": sum(len(f["witnesses"]) for f in data["fans"]),
            "closed_component": transitions, "compatible_four_point_red": compatible}


def audit_one_recolor():
    results = []
    for data in json.loads((ROOT / "one_recolor_obstructions.json").read_text())["results"]:
        points, n = data["P"], data["n"]
        m = len(points)
        caps, gons = build(points, n)
        assert len(caps) == data["cap4_count"] and len(gons) == data["gon_count"]
        for mode, details in data["modes"].items():
            example = details["one_recolor"]
            p, red = example["hole"], frozenset(example["red"])
            positive = set(gons if mode == "weak" else gons.values())
            subcaps = [c for c in caps if p not in c]
            subpositive = [h if mode == "weak" else e for h, e in gons.items() if p not in h]
            assert p not in red and good(red, subcaps, subpositive)
            for q in [None] + [q for q in range(m) if q != p]:
                old = red if q is None else red ^ {q}
                assert not good(old, caps, positive)
                assert not good(old | {p}, caps, positive)
            nearest = frozenset(example["nearest_full_red"])
            assert good(nearest, caps, positive)
            assert len((nearest - {p}) ^ red) == 2
            results.append({"n": n, "m": m, "mode": mode,
                            "minimum_old_recolorings": 2, "hole": p})
    return results


def main():
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
    start = time.monotonic()
    output = {"label": "COMPUTED", "geometry_method": "four-subset point-in-triangle",
              "four_state": [audit_four_state(ROOT / name) for name in
                             ("four_state_obstruction.json", "four_state_obstruction_small.json")],
              "one_recolor": audit_one_recolor(),
              "elapsed_seconds": time.monotonic() - start,
              "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT / "independent_audit.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

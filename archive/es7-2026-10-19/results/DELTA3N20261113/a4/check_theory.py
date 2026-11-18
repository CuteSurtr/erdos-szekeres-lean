#!/usr/bin/env python3
"""Bounded exact controls for theory.md; standard library, one thread, no SAT.

Reads the old records without importing their code. Enumerates subsets directly;
real-point convexity is checked by an independent monotone-chain hull. The
default inputs are 662 recorded small signotopes and the real a=4 counterexamples.
The time budget is a guard, not a request to run a long search.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import time


TRIMMING_POINTS = [
    [-500, -530], [10, 0], [20, 10], [30, 40],
    [40, 90], [100, 162], [110, 405],
]
TRIMMING_SIGNS = "-+++++++++++++++++++-+-+++-+-++--++"


def det(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def point_signs(points):
    assert all(points[i][0] < points[i + 1][0] for i in range(len(points) - 1))
    out = {}
    for t in combinations(range(len(points)), 3):
        d = det(*(points[i] for i in t))
        assert d != 0, ("collinear", t)
        out[t] = d > 0
    return out


def hull(points, ids):
    """Return the vertex set and the lower chain, both from exact determinants."""
    ids = tuple(sorted(ids))
    if len(ids) < 2:
        return frozenset(ids), ids
    lo, hi = [], []
    for sequence, stack in ((ids, lo), (tuple(reversed(ids)), hi)):
        for p in sequence:
            while len(stack) > 1 and det(points[stack[-2]], points[stack[-1]], points[p]) <= 0:
                stack.pop()
            stack.append(p)
    return frozenset(lo + hi), tuple(lo)


class Config:
    def __init__(self, name, m, n, signs, points=None):
        self.name, self.m, self.n = name, m, n
        self.o, self.points = signs, points
        assert len(signs) == comb(m, 3)
        for a, b, c, d in combinations(range(m), 4):
            row = [signs[a, b, c], signs[a, b, d], signs[a, c, d], signs[b, c, d]]
            assert sum(row[i] != row[i + 1] for i in range(3)) <= 1
        self.cups = []
        for size in range(1, m + 1):
            for C in combinations(range(m), size):
                # All-triples and consecutive-turn definitions are cross-checked.
                all_triples = all(signs[t] for t in combinations(C, 3))
                consecutive = all(signs[C[i], C[i + 1], C[i + 2]] for i in range(size - 2))
                assert all_triples == consecutive
                if all_triples:
                    self.cups.append(C)
        self.gon_cache = {}

    def cup(self, C):
        return all(self.o[t] for t in combinations(sorted(C), 3))

    def cap4_free(self):
        return all(any(self.o[t] for t in combinations(C, 3))
                   for C in combinations(range(self.m), 4))

    def polygons(self, size):
        if size in self.gon_cache:
            return self.gon_cache[size]
        answer = []
        for G in combinations(range(self.m), size):
            four_test = all(
                self.o[a, b, c] == self.o[a, b, d]
                and self.o[a, c, d] == self.o[b, c, d]
                for a, b, c, d in combinations(G, 4)
            )
            if self.points is not None:
                vertices, lower = hull(self.points, G)
                geometric = len(vertices) == size
                assert geometric == four_test, (self.name, G)
            else:
                geometric = four_test
            if geometric:
                u, v = G[0], G[-1]
                sign_lower = (u,) + tuple(p for p in G[1:-1] if self.o[u, p, v]) + (v,)
                if self.points is not None:
                    assert lower == sign_lower
                answer.append((G, sign_lower))
        self.gon_cache[size] = answer
        return answer

    def reflected(self):
        if self.points is not None:
            pts = [[-x, y] for x, y in reversed(self.points)]
            signs = point_signs(pts)
        else:
            pts = None
            signs = {t: self.o[tuple(self.m - 1 - i for i in reversed(t))]
                     for t in combinations(range(self.m), 3)}
        return Config(self.name + ":reflected", self.m, self.n, signs, pts)


def check_terminal(f, U, k, targets, counts):
    U = frozenset(U)
    if any(len(C) == k and set(C) <= U for C in f.cups):
        return None
    eligible = [(G, C) for G, C in targets if set(G) <= U]
    E = frozenset(G[-1] for G, C in eligible)
    assert f.cup(E), ("terminal cup", f.name, sorted(E))
    assert len(E) <= k - 2, ("terminal size", f.name, sorted(E))
    assert all(E.intersection(C) for G, C in eligible)
    assert all(len(C) == k - 1 for G, C in eligible)
    for e in E:
        assert any(not f.o[a, b, e] for a, b in combinations(sorted(p for p in U if p < e), 2))
    counts["terminal_lemma_instances"] += 1
    return E


def check_one(f, counts, sizes):
    assert f.cap4_free(), ("invalid 4-cap hypothesis", f.name)
    counts["configurations_checked_including_reflections"] += 1
    if f.points is not None:
        counts["real_configurations_including_reflections"] += 1
    k, r = f.n - 1, f.m - 1
    targets = f.polygons(k)
    counts["target_polygons_examined"] += len(targets)
    check_terminal(f, range(f.m), k, targets, counts)
    E = check_terminal(f, range(r), k, targets, counts)
    if E is not None:
        D = E | {r}
        assert f.cup(D), ("extreme theorem cup", f.name, sorted(D))
        assert len(D) <= k - 1, ("extreme theorem size", f.name, sorted(D))
        assert all(D.intersection(C) for G, C in targets), ("extreme theorem hit", f.name)
        assert all(f.o[p, q, z] for p in D
                   for q, z in combinations(range(p + 1, f.m), 2)), ("conditional Q localization", f.name)
        counts["extreme_point_theorem_instances"] += 1
        if any(len(C) == k for C in f.cups):
            counts["extreme_theorem_instances_with_k_cups_present"] += 1
        if f.polygons(k + 1):
            counts["extreme_theorem_instances_with_convex_k_plus_1_gon"] += 1
        sizes[f"k={k},size={len(D)}"] += 1

    if f.polygons(k + 1):
        return  # The boundary localization has the extra polygon hypothesis.
    assert max(map(len, f.cups), default=0) <= k
    lab = {(x, y): 2 if any(not f.o[x, y, z] for z in range(y + 1, f.m)) else 1
           for x, y in combinations(range(f.m), 2)}
    for a, b, c in combinations(range(f.m), 3):
        if not f.o[a, b, c]:
            assert (lab[a, b], lab[b, c]) == (2, 1)
    alpha, beta = [1] * f.m, [1] * f.m
    for C in f.cups:
        beta[C[-1]] = max(beta[C[-1]], len(C))
        if len(C) >= 2 and lab[C[-2], C[-1]] == 1:
            alpha[C[-1]] = max(alpha[C[-1]], len(C))
    R = frozenset(p for p in range(f.m) if beta[p] == k)
    assert f.cup(R) and len(R) <= k - 1
    assert all(R.intersection(C) for C in f.cups if len(C) == k)
    counts["boundary_localization_instances"] += 1
    for G, C in targets:
        if not R.intersection(C):
            assert len(C) == k - 1
            assert beta[C[-1]] == k - 1 and alpha[C[0]] == 1
            assert all(alpha[p] <= i for i, p in enumerate(C, 1))
            counts["missed_lower_chains_localized_with_multiplicity"] += 1


def trimming_control():
    f = Config("new-seven-point-trimming-obstruction", 7, 5,
               point_signs(TRIMMING_POINTS), TRIMMING_POINTS)
    sign_string = "".join("+" if f.o[t] else "-" for t in combinations(range(7), 3))
    assert sign_string == TRIMMING_SIGNS
    assert f.cap4_free() and not f.polygons(5)
    targets = f.polygons(4)
    C = frozenset((1, 2, 3, 4))
    assert f.cup(C) and all(C.intersection(L) for G, L in targets)
    private = []
    for p in sorted(C):
        W = (0, p, 5, 6)
        assert f.cup(W) and C.intersection(W) == {p}
        assert not all((C - {p}).intersection(L) for G, L in targets)
        private.append(W)
    smaller = next(D for D in f.cups if len(D) <= 3
                   and all(set(D).intersection(L) for G, L in targets))
    return f, {
        "label": "COMPUTED (exact integer arithmetic and exhaustive subsets)",
        "points": TRIMMING_POINTS,
        "signs": sign_string,
        "negative_triples": [t for t in combinations(range(7), 3) if not f.o[t]],
        "convex_quadrilaterals": len(targets),
        "convex_pentagons": len(f.polygons(5)),
        "four_caps": 0,
        "inclusion_minimal_cup_side_transversal": sorted(C),
        "private_four_cups": private,
        "alternative_smaller_cup_side_transversal": smaller,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path,
                        default=Path(__file__).resolve().parents[2] / "DELTA2N20261113" / "data")
    args = parser.parse_args()
    started = time.monotonic()
    counts, sizes, source_hashes = Counter(), Counter(), {}
    expected = {5: 35, 6: 170, 7: 457}

    def run(f):
        if time.monotonic() - started > 17:
            raise RuntimeError("short-test budget reached; run is INCOMPLETE")
        check_one(f, counts, sizes)
        check_one(f.reflected(), counts, sizes)

    for m, expected_count in expected.items():
        path = args.data / f"enum_a4_n5_m{m}_strong.jsonl"
        data = path.read_bytes()
        source_hashes[path.name] = sha256(data).hexdigest()
        records = [json.loads(line) for line in data.splitlines() if line.strip()]
        assert len(records) == expected_count
        for i, rec in enumerate(records):
            assert len(rec["s"]) == comb(m, 3)
            signs = {t: c == "+" for t, c in zip(combinations(range(m), 3), rec["s"])}
            run(Config(f"{path.name}:{i + 1}", m, 5, signs))
        counts["recorded_abstract_inputs"] += len(records)

    for path in sorted((args.data / "cex").glob("*a4*.json")):
        data = path.read_bytes()
        rec = json.loads(data)
        if not rec.get("P"):
            continue
        points = rec["P"]
        assert len(points) == rec["m"] <= 11
        signs = point_signs(points)
        actual = "".join("+" if signs[t] else "-" for t in combinations(range(len(points)), 3))
        assert actual == rec["signs"]
        source_hashes[f"cex/{path.name}"] = sha256(data).hexdigest()
        run(Config(path.name, len(points), rec["n"], signs, points))
        counts["old_real_inputs"] += 1

    trimming, obstruction = trimming_control()
    run(trimming)
    # The main theorem deliberately has no (k+1)-gon-free hypothesis.
    points = [[0, 0], [1, -1], [2, 2], [3, -1], [4, 0]]
    broader = Config("convex-pentagon-control", 5, 5, point_signs(points), points)
    assert len(broader.polygons(5)) == 1
    run(broader)

    # Nonvacuous original-hypothesis examples for every n=4,...,8:
    # the extra point is above the old endpoint chord but below the new one.
    for k in range(3, 8):
        points = sorted([[2 * i, (2 * i) ** 2] for i in range(k)] + [[1, 2 * k - 3]])
        f = Config(f"parabolic-extension-k{k}", k + 1, k + 1, point_signs(points), points)
        assert f.polygons(k) and not f.polygons(k + 1)
        assert not any(len(C) == k and C[-1] < f.m - 1 for C in f.cups)
        run(f)
        counts["parabolic_extension_inputs"] += 1

    result = {
        "status": "PASS",
        "label": "COMPUTED; bounded controls, not a universal or UNSAT certificate",
        "method": "direct subset enumeration; exact hulls for real inputs; no old code imported",
        "counts": dict(sorted(counts.items())),
        "extreme_theorem_delta_sizes": dict(sorted(sizes.items())),
        "trimming_obstruction": obstruction,
        "input_sha256": source_hashes,
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

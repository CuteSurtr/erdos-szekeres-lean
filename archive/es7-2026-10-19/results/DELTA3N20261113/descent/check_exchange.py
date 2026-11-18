#!/usr/bin/env python3
"""Exact, bounded exchange audit for a supplied small integer point set.

Pure Python, one thread, no SAT solver. Reads old data without modifying it.
All indices are zero based in increasing x order. Intended for m <= 16.
"""
import argparse
import itertools
import json
import time
from pathlib import Path


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def mask(xs):
    return sum(1 << x for x in xs)


def vertices(bits):
    return [i for i in range(bits.bit_length()) if bits >> i & 1]


def hull_parts(points, ids):
    lo, hi = [], []
    for i in ids:
        while len(lo) >= 2 and orient(points[lo[-2]], points[lo[-1]], points[i]) <= 0:
            lo.pop()
        lo.append(i)
        while len(hi) >= 2 and orient(points[hi[-2]], points[hi[-1]], points[i]) >= 0:
            hi.pop()
        hi.append(i)
    return lo, hi


def analyze(points, n, require_starter=True, stop_at_first_trap=False):
    points = sorted(map(tuple, points))
    m = len(points)
    assert m <= 16, "bounded small-set audit only"
    assert len({p[0] for p in points}) == m
    signs = {t: orient(*(points[i] for i in t)) for t in itertools.combinations(range(m), 3)}
    assert all(signs.values()), "not general position"
    cap = lambda ids: all(signs[t] < 0 for t in zip(ids, ids[1:], ids[2:]))
    caps4 = [tuple(ids) for ids in itertools.combinations(range(m), 4) if cap(ids)]
    caps5 = [tuple(ids) for ids in itertools.combinations(range(m), 5) if cap(ids)]
    assert not caps5, "has a 5-cap"
    gons = []
    for ids in itertools.combinations(range(m), n):
        lo, hi = hull_parts(points, ids)
        if len(lo) + len(hi) - 2 == n:
            gons.append(ids)
    assert not gons, "has a convex n-gon"
    family = {}
    for ids in itertools.combinations(range(m), n - 1):
        lo, hi = hull_parts(points, ids)
        if len(lo) + len(hi) - 2 == n - 1:
            family[mask(lo)] = {"cup": lo, "cap_type": len(hi), "cap": hi}
    family = sorted(family.items())
    all_hit = (1 << len(family)) - 1
    incidence = [sum(1 << j for j, (d, _) in enumerate(family) if d >> i & 1) for i in range(m)]
    type_masks = {c: sum(1 << j for j, (_, rec) in enumerate(family) if rec["cap_type"] == c) for c in (2, 3, 4)}
    capmasks = [mask(c) for c in caps4]
    good = [False] * (1 << m)
    hit = [0] * (1 << m)
    good[0] = True
    for a in range(1, 1 << m):
        b = a & -a
        hit[a] = hit[a ^ b] | incidence[b.bit_length() - 1]
        good[a] = good[a ^ b] and not any(k & a == k for k in capmasks if k & b)
    full = [a for a in range(1 << m) if good[a] and hit[a] == all_hit]
    result = {"label": "COMPUTED", "n": n, "m": m, "points": points,
              "caps4": caps4, "family": [r for _, r in family],
              "type_counts": {c: t.bit_count() for c, t in type_masks.items()},
              "full_transversals": len(full)}
    result["require_right_starter"] = require_starter
    start_caps = {}
    for k in caps4:
        start_caps.setdefault(k[0], []).append(k)
    Q = set(range(m)) - set(start_caps)
    result["Q"] = sorted(Q)
    result["extendible_cups"] = [rec for _, rec in family if rec["cup"][-1] in start_caps]
    traps = []
    candidate_count = 0
    candidate_by_type = {3: 0, 4: 0}
    for a in range(1 << m):
        if not good[a] or hit[a] == all_hit or hit[a] & type_masks[2] != type_masks[2]:
            continue
        missed = [j for j, (d, _) in enumerate(family) if not a & d]
        candidates = [j for j in missed if family[j][1]["cap_type"] in (3, 4)
                      and (not require_starter or family[j][1]["cup"][-1] in start_caps)]
        for j in candidates:
            candidate_count += 1
            d, rec = family[j]
            candidate_by_type[rec["cap_type"]] += 1
            moves = []
            for p in vertices(d):
                for r in [None] + vertices(a):
                    new = (a | (1 << p)) if r is None else ((a ^ (1 << r)) | (1 << p))
                    if good[new] and hit[new] & hit[a] == hit[a]:
                        moves.append((p, r))
            if not moves:
                captype = rec["cap_type"]
                near = sorted(full, key=lambda b: ((b ^ a).bit_count(), b))
                best = near[0]
                trap = {"A": vertices(a), "A_subset_Q": set(vertices(a)) <= Q,
                        "D": rec, "missed": [family[z][1] for z in missed],
                        "right_start_caps": start_caps.get(rec["cup"][-1], []),
                        "nearest_full": vertices(best), "nearest_distance": (best ^ a).bit_count()}
                # One concise witness per cap type and per Q-localization status.
                key = (captype, trap["A_subset_Q"])
                if not any((t["D"]["cap_type"], t["A_subset_Q"]) == key for t in traps):
                    traps.append(trap)
        if len(traps) == 4 or (stop_at_first_trap and traps):
            break
    result["monotone_one_exchange_traps"] = traps
    result["candidate_pairs_checked"] = candidate_count
    result["candidate_pairs_by_type"] = candidate_by_type
    result["stopped_after_witness"] = bool(stop_at_first_trap and traps)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--n", type=int)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    begin = time.monotonic()
    data = json.loads(Path(args.input).read_text())
    result = analyze(data["P"], args.n or data["n"])
    result["source"] = str(Path(args.input))
    result["seconds"] = time.monotonic() - begin
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("n", "m", "type_counts", "full_transversals", "monotone_one_exchange_traps", "seconds")}))


if __name__ == "__main__":
    main()

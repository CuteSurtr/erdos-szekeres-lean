#!/usr/bin/env python3
"""Search threshold-compatible rank-two blocks inside a fixed Boolean witness.

This is a candidate search, not a geometric or Lean proof. Pairwise interval
compatibility on each threshold row prevents discarding valid subsets merely
because a larger unconstrained maximal clique has no threshold realization.
"""
import argparse
import gzip
import hashlib
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
HOLES = [7,12,33,39,44,47,50,51,52,54,55,56,69,71,73,75,76,77,78,90,97,99,101,109,115,117,118,119,124,127,132,133]


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def search(mode):
    source = ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz"
    raw = gzip.decompress(source.read_bytes())
    data = json.loads(raw)
    states = data["states"]
    cells = [(x, y) for x in range(1, 5) for y in range(1, 7)]
    masks = [sum(1 << i for i, (x, y) in enumerate(cells) if y <= state[x-1]) for state in states]
    occupied = [i for i in range(len(states)) if i not in HOLES]
    intervals = eligible = calls = 0
    best = []
    started = time.monotonic()
    found = None
    for lower, L in enumerate(masks):
        for upper, U in enumerate(masks):
            if L & ~U:
                continue
            intervals += 1
            inside = [i for i in occupied if not (L & ~masks[i] or masks[i] & ~U)]
            if len(inside) < 23:
                continue
            active = U & ~L
            ac = list(bits(active))
            bounds = []
            valid = []
            for s in inside:
                present, absent = masks[s] & active, active & ~masks[s]
                largest_absent = max((cells[i][0] for i in bits(absent)), default=0)
                smallest_present = min((cells[i][0] for i in bits(present)), default=5)
                lo, hi = [0]*6, [4]*6
                ones = twos = 0
                for i in bits(present):
                    x, y = cells[i]
                    if x < largest_absent:
                        lo[y-1] = max(lo[y-1], x)
                        ones |= 1 << i
                for i in bits(absent):
                    x, y = cells[i]
                    if smallest_present < x:
                        hi[y-1] = min(hi[y-1], x-1)
                        twos |= 1 << i
                if (all(a <= b for a, b in zip(lo, hi)) if mode == "threshold" else not (ones & twos)):
                    valid.append(s)
                    bounds.append((lo, hi, ones, twos))
            if len(valid) < 23:
                continue
            eligible += 1
            adjacency = []
            for a, (lo, hi, ones, twos) in enumerate(bounds):
                mask = 0
                for b, (lb, hb, ob, tb) in enumerate(bounds):
                    compatible = (all(x <= y and z <= w for x, y, z, w in zip(lo, hb, lb, hi))
                                  if mode == "threshold" else not (ones & tb or ob & twos))
                    if a != b and compatible:
                        mask |= 1 << b
                adjacency.append(mask)

            def visit(chosen, possible, excluded):
                nonlocal calls, found, best
                calls += 1
                if len(chosen) > len(best):
                    best = [valid[i] for i in chosen]
                if len(chosen) >= 23:
                    thresholds = [max(bounds[i][0][y] for i in chosen) for y in range(6)]
                    support = sorted(valid[i] for i in chosen)
                    active_cells = [cells[i] for i in ac]
                    ones = 0
                    for i in chosen:
                        ones |= bounds[i][2]
                    rank_one = [cells[i] for i in bits(ones)]
                    rank = (lambda z: 1 if z[0] <= thresholds[z[1]-1] else 2) if mode == "threshold" else (lambda z: 1 if z in rank_one else 2)
                    assert all(rank(z) < rank(w) for s in support for z in active_cells for w in active_cells
                               if z[1] <= states[s][z[0]-1] and w[1] > states[s][w[0]-1] and z[0] < w[0])
                    assert all(not ((masks[b] & ~masks[a]) & ~active) for a in support for b in support)
                    found = {"support": support, "thresholds": thresholds if mode == "threshold" else None,
                             "rank_one_cells": rank_one,
                             "active": active_cells, "lower": lower, "upper": upper,
                             "demand": len(support)-22, "holes_in_support": sorted(set(support) & set(HOLES))}
                    return True
                if len(chosen) + possible.bit_count() < 23:
                    return False
                pivot = max(bits(possible | excluded), key=lambda v: (possible & adjacency[v]).bit_count(), default=None)
                candidates = possible if pivot is None else possible & ~adjacency[pivot]
                for v in list(bits(candidates)):
                    if visit(chosen + [v], possible & adjacency[v], excluded & adjacency[v]):
                        return True
                    possible &= ~(1 << v)
                    excluded |= 1 << v
                return False

            if visit([], (1 << len(valid))-1, 0):
                break
        if found:
            break
    report = {"scope": "Computational rank-two compression candidate search; no Lean proof yet", "mode": mode,
              "source_archive_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "source_uncompressed_sha256": hashlib.sha256(raw).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "holes": HOLES, "occupied_count": len(occupied), "intervals": intervals,
              "eligible_intervals": eligible, "recursive_calls": calls,
              "largest_clique_visited": best, "candidate": found,
              "all_intervals_exhausted": found is None, "seconds": round(time.monotonic()-started, 3)}
    (HERE / ("search-" + mode + ".json")).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["threshold", "cell"], default="threshold")
    search(parser.parse_args().mode)

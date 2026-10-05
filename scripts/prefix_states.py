#!/usr/bin/env python3
"""Enumerate short incoming-rank prefixes under necessary four-point signs.

The orientation patterns are a relaxation: realizability is not asserted.
Every four-packet in lexicographic triple order has at most one sign change.
This finite Python enumeration is not a Lean-certified coverage computation.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time

ALLOWED_PACKETS = frozenset((0, 1, 3, 7, 8, 12, 14, 15))


def signotope_masks(n):
    if type(n) is not int or not 1 <= n <= 6:
        raise ValueError("Exhaustive enumeration is limited to one through six vertices")
    triples = list(combinations(range(n), 3))
    index = {triple: i for i, triple in enumerate(triples)}
    packets = [tuple(index[t] for t in combinations(q, 3)) for q in combinations(range(n), 4)]
    for mask in range(1 << len(triples)):
        if all(sum(((mask >> i) & 1) << j for j, i in enumerate(packet)) in ALLOWED_PACKETS
               for packet in packets):
            yield mask


def incoming_states(n, mask, width, height):
    """Actual consecutive-chain maxima minus one, in cap,cup coordinates."""
    index = {t: i for i, t in enumerate(combinations(range(n), 3))}
    labels, states = {}, []
    for v in range(n):
        heights = [0] * width
        for u in range(v):
            cap = cup = 1
            for t in range(u):
                if (mask >> index[t, u, v]) & 1:
                    cup = max(cup, labels[t, u][1] + 1)
                else:
                    cap = max(cap, labels[t, u][0] + 1)
            labels[u, v] = cap, cup
            if cap > width or cup > height:
                return None
            for x in range(cap):
                heights[x] = max(heights[x], cup)
        states.append(tuple(heights))
    return tuple(states)


def enumerate_prefixes(n, catalog):
    states = [tuple(s) for s in catalog["states"]]
    width, height = catalog["width"], catalog["height"]
    if len(states) != len(set(states)):
        raise ValueError("Duplicate catalogue states")
    lookup = {s: i for i, s in enumerate(states)}
    patterns = outside = 0
    sets, orders = {}, set()
    for mask in signotope_masks(n):
        patterns += 1
        prefix = incoming_states(n, mask, width, height)
        if prefix is None:
            outside += 1
            continue
        labels = tuple(lookup[s] for s in prefix)
        if len(set(labels)) != n:
            raise AssertionError("Incoming states should be injective")
        sets.setdefault(tuple(sorted(labels)), mask)
        orders.add(labels)
    return {
        "vertices": n, "orientation_patterns": patterns, "outside_rank_rectangle": outside,
        "unique_state_sets": len(sets), "unique_state_orders": len(orders),
        "state_sets": sorted(sets),
        "representatives": [{"states": list(k), "orientation_mask": v} for k, v in sorted(sets.items())],
        "scope": "Exhaustive short-prefix signotope relaxation; finite coverage and rank semantics are not Lean-certified",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--vertices", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    started = time.monotonic()
    result = enumerate_prefixes(args.vertices, json.loads(args.catalog.read_text()))
    result.update(catalog=str(args.catalog), catalog_sha256=hashlib.sha256(args.catalog.read_bytes()).hexdigest(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  seconds=time.monotonic()-started)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print({k: v for k, v in result.items() if k not in ("state_sets", "representatives")})

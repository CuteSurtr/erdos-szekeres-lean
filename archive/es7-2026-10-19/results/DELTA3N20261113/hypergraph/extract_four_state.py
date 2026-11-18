#!/usr/bin/env python3
"""Extract local cup fans proving a closed four-state vacancy component.

Checks a supplied transversal; does NOT optimize its size or enumerate
transversals. The input coordinate set and candidate came from coordinator.
"""

import argparse
import hashlib
import itertools
import json
import resource
from pathlib import Path

from obstruction_check import bits, geometry, mask, orient, works


def isolated_cap(points, n, target):
    caps, gons, triples = geometry(points, n)
    target_mask = mask(target)
    lower = set(lo for _, lo, _ in gons)
    if target_mask not in caps or not all(e & target_mask for e in lower):
        return None
    for p in target:
        intersection = (1 << len(points)) - 1
        for e in lower:
            if e & target_mask == 1 << p:
                intersection &= e
        if intersection != 1 << p:
            return None
    return caps, gons, triples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimize-support", action="store_true",
                        help="Delete vertices preserving the LOCAL four-state trap, not a cardinality gap")
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
    raw = args.input.read_bytes()
    source = json.loads(raw)
    original, n, original_target = source["P"], source["n"], source["bare"]
    retained = list(range(len(original)))
    assert isolated_cap(original, n, original_target)
    if args.minimize_support:
        changed = True
        while changed:
            changed = False
            for q in list(retained):
                if q in original_target:
                    continue
                trial = [i for i in retained if i != q]
                target_trial = [trial.index(i) for i in original_target]
                if isolated_cap([original[i] for i in trial], n, target_trial):
                    retained = trial
                    changed = True
    points = [original[i] for i in retained]
    target = [retained.index(i) for i in original_target]
    caps, gons, triples = isolated_cap(points, n, target)
    carriers = {}
    for g, lo, up in gons:
        carriers.setdefault(lo, (g, up))
    target_mask = mask(target)
    assert len(target) == 4 and target_mask in caps
    assert all(e & target_mask for e in carriers), "Given cap does not hit every lower chain"
    fans = []
    for p in target:
        possible = [e for e in sorted(carriers) if e & target_mask == 1 << p]
        intersection = (1 << len(points)) - 1
        selected = []
        while intersection != 1 << p:
            e = min(possible, key=lambda e: ((e & intersection).bit_count(), e))
            assert intersection & e != intersection, "No cup fan with intersection {p}"
            intersection &= e
            selected.append({"lower": bits(e), "gon": bits(carriers[e][0]),
                             "upper": bits(carriers[e][1])})
        fans.append({"pivot": p, "witnesses": selected})
    # A fixed-size feasibility witness separates a reconfiguration obstruction
    # from a global size obstruction. No minimum is computed.
    compatible = next((list(t) for t in itertools.combinations(range(len(points)), 4)
                       if works(mask(t), caps, list(carriers))), None)
    inherited = [retained.index(i) for i in [0, 1, 2, 5, 6] if i in retained]
    assert works(mask(inherited), caps, list(carriers))
    output = {"label": "COMPUTED", "purpose": "local four-state vacancy obstruction",
              "source": str(args.input), "source_sha256": hashlib.sha256(raw).hexdigest(),
              "P": points, "n": n, "T": target, "source_point_indices": retained,
              "support_deletion_minimized": args.minimize_support,
              "cap_determinants": [{"triple": list(t), "det": orient(points, *t)}
                                   for t in itertools.combinations(target, 3)],
              "cap4_count": len(caps), "gon_count": len(gons), "lower_count": len(carriers),
              "minimum_absolute_orientation": min(map(abs, triples.values())),
              "fans": fans, "known_cap_free_transversal": inherited,
              "compatible_four_point_red": compatible}
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k not in ("P", "source_sha256")}))


if __name__ == "__main__":
    main()

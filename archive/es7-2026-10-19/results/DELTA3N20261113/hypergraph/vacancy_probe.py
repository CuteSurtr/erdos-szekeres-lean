#!/usr/bin/env python3
"""Enumerate proper one-hole states of a fixed mixed hypergraph (COMPUTED).

A move fills the hole with another vertex's color and makes that vertex the
new hole. Cup constraints are fixed from the original set, not recomputed
from a geometric deletion. This distinction is intentional.
"""

import argparse
import json
import resource
import time
from collections import deque
from pathlib import Path

from obstruction_check import bits, geometry, works


def components(m, caps, positive):
    allbits = (1 << m) - 1
    full = {r for r in range(1 << m) if works(r, caps, positive)}
    states = set()
    for r in range(1 << m):
        if any(r & c == c for c in caps):
            continue
        holes = allbits ^ r
        for e in positive:
            if not r & e:
                holes &= e
        states.update(r * m + p for p in bits(holes))
    unseen = set(states)
    count, trapped, first = 0, 0, None
    sizes = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = deque([start])
        component = []
        terminals = 0
        while queue:
            s = queue.popleft()
            component.append(s)
            r, p = divmod(s, m)
            terminals += r in full or (r | (1 << p)) in full
            for q in range(m):
                if q == p:
                    continue
                new_r = (r ^ (1 << q)) | (1 << p) if r & (1 << q) else r
                target = new_r * m + q
                if target in unseen:
                    unseen.remove(target)
                    queue.append(target)
        count += 1
        if not terminals:
            trapped += 1
            if first is None:
                r, p = divmod(start, m)
                equal_size_models = [x for x in full if x.bit_count() in (r.bit_count(), r.bit_count() + 1)]
                first = {"hole": p, "red": bits(r), "component_size": len(component),
                         "full_colorings_at_compatible_sizes": len(equal_size_models),
                         "component_states": [{"hole": t % m, "red": bits(t // m)}
                                              for t in sorted(component)]}
        sizes.append(len(component))
    return {"proper_states": len(states), "components": count, "trapped_components": trapped,
            "largest_component": max(sizes, default=0), "first_trapped": first}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
    start = time.monotonic()
    results = []
    for path in args.input:
        source = json.loads(path.read_text())
        points, n = source["P"], source["n"]
        assert len(points) <= 16
        caps, gons, _ = geometry(points, n)
        result = {"source": str(path), "P": points, "n": n, "modes": {}}
        for mode in ("weak", "cup"):
            positive = sorted(set(g if mode == "weak" else lo for g, lo, _ in gons))
            report = components(len(points), caps, positive)
            result["modes"][mode] = report
            small = {k: v for k, v in report.items() if k != "first_trapped"}
            if report["first_trapped"]:
                small["first_trapped"] = {k: v for k, v in report["first_trapped"].items()
                                          if k != "component_states"}
            print(json.dumps({"n": n, "mode": mode, **small}), flush=True)
        results.append(result)
    args.output.write_text(json.dumps({"label": "COMPUTED", "results": results}, indent=2) + "\n")
    print(json.dumps({"elapsed_seconds": time.monotonic() - start,
                      "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()

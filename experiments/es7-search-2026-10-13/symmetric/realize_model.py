#!/usr/bin/env python3
"""Try to realize models (lines of X literals, as written by enum_models) of a symcnf.py CNF with
the rotational symmetry imposed (symrealize), then verify the integer coordinates independently:
  * every orientation of the integer point set equals the model's chi (all C(P,3) triples)
  * general position of the set points
  * largest convex subset of the set points (exact DP from scripts/es_lower_bound_witness.py) < K
usage: realize_model.py map.json models.txt outdir [max_models] [restarts] [iters]
Prints one line per model and a summary.
"""
import itertools
import json
import os
import subprocess
import sys

sys.path.insert(0, "/Users/jiho/Desktop/lean 4 /scripts")
from es_lower_bound_witness import largest_convex_subset, orient, general_position  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def parity(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return -1 if inv & 1 else 1


def main():
    mp, models, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    maxm = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
    restarts = sys.argv[5] if len(sys.argv) > 5 else "20"
    iters = sys.argv[6] if len(sys.argv) > 6 else "40000"
    info = json.load(open(mp))
    P, m, K = info["P"], info["m"], info["K"]
    has_center = 1 if info["center"] != "none" else 0
    os.makedirs(outdir, exist_ok=True)
    n = realized = 0
    for line in open(models):
        lits = [int(x) for x in line.split()]
        if not lits:
            continue
        n += 1
        if n > maxm:
            break
        vals = {abs(l): l > 0 for l in lits}
        sig = {}
        for a, b, c, v, s in info["triples"]:
            sig[(a, b, c)] = s * (1 if vals[v] else -1)
        sigpath = os.path.join(outdir, f"model{n}.sig")
        with open(sigpath, "w") as f:
            for (a, b, c), s in sorted(sig.items()):
                f.write(f"{a} {b} {c} {s}\n")
        ptspath = os.path.join(outdir, f"model{n}.pts")
        r = subprocess.run([os.path.join(HERE, "symrealize"), str(P), str(m), str(has_center), sigpath, str(n), restarts, iters, ptspath],
                           capture_output=True, text=True)
        last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "no output"
        if r.returncode != 0:
            print(f"model {n}: {last}")
            continue
        pts = [tuple(map(int, l.split())) for l in open(ptspath)]
        assert len(pts) == P
        bad = sum(1 for (a, b, c), s in sig.items() if (orient(pts[a], pts[b], pts[c]) > 0) != (s > 0) or orient(pts[a], pts[b], pts[c]) == 0)
        setpts = [pts[i] for i in info["setpts"]]
        gp = general_position(setpts)
        big = largest_convex_subset(setpts)
        ok = bad == 0 and gp and big < K
        realized += ok
        print(f"model {n}: {last}; python re-check: orientation mismatches={bad} general_position={gp} largest_convex_subset={big} -> {'OK' if ok else 'FAIL'}")
    print(f"SUMMARY {models}: models_tried={min(n, maxm)} realized_and_verified={realized}")


if __name__ == "__main__":
    main()

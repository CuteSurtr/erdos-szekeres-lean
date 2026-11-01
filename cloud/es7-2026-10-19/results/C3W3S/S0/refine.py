#!/usr/bin/env python3
"""C3W3S level-2 refinement: for each open level-1 cube C of NODE (given as its 3 bit values), the 8 cubes on
the 6 smallest free residues extending C, via sigma_cubes.run (imported unmodified), 3 at a time.
usage (from TOOLS): refine.py BASE OUT.jsonl NODE v1v2v3 [v1v2v3 ...]   e.g. 010"""
import concurrent.futures as cf
import itertools
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import sigma_cubes  # noqa: E402
from hullcase import parse_layers  # noqa: E402


def main():
    base, out, node = sys.argv[1], sys.argv[2], sys.argv[3]
    used = {r for L in parse_layers(node) for r, _ in L}
    bits6 = [r for r in range(1, 11) if r not in used][:6]
    tasks = [(base, node, bits6, tuple(int(c) for c in v3) + ext, 300)
             for v3 in sys.argv[4:] for ext in itertools.product((0, 1), repeat=3)]
    os.makedirs(sigma_cubes.WORK, exist_ok=True)
    with open(out, "a") as fo, cf.ProcessPoolExecutor(3) as ex:
        for fu in cf.as_completed([ex.submit(sigma_cubes.run, t) for t in tasks]):
            rec = fu.result()
            fo.write(json.dumps(rec) + "\n"); fo.flush()
            print(json.dumps({x: rec.get(x) for x in ("node", "cube", "status", "solve_s", "certified")}), flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Random KNOWN-realizable symmetric chirotopes for calibration: random symmetric integer point
sets (sampler of symvalidate.py, labelling normal form included), chirotope written to
<out>/<tag>_<i>.sig (0-based a<b<c over all P points), ground truth to <out>/<tag>_<i>.truth.pts.
usage: gen_random_sym.py map.json tag count seed outdir
"""
import itertools
import json
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.environ.get("ES_REPO", "."), "scripts"))  # ES_REPO = repository root
from symvalidate import sample_points  # noqa: E402
from es_lower_bound_witness import orient  # noqa: E402

mp, tag, count, seed, outdir = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
info = json.load(open(mp))
rng = random.Random(seed)
os.makedirs(outdir, exist_ok=True)
for i in range(count):
    pts = None
    while pts is None:
        pts = sample_points(info, rng)
    with open(os.path.join(outdir, f"{tag}_{i}.sig"), "w") as f:
        for a, b, c in itertools.combinations(range(len(pts)), 3):
            f.write(f"{a} {b} {c} {1 if orient(pts[a], pts[b], pts[c]) > 0 else -1}\n")
    with open(os.path.join(outdir, f"{tag}_{i}.truth.pts"), "w") as f:
        for x, y in pts:
            f.write(f"{x} {y}\n")
print(f"wrote {count} instances to {outdir}")

#!/usr/bin/env python3
"""Calibrate symrealize on KNOWN realizable symmetric chirotopes: random symmetric point sets
(same sampler as symvalidate), chi over all P points -> symrealize with a given budget."""
import json, os, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symvalidate import sample_points
from es_lower_bound_witness import orient
mp, trials, restarts, iters = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
info = json.load(open(mp)); P, m = info["P"], info["m"]; hc = 1 if info["center"] != "none" else 0
rng = random.Random(99); ok = 0
for t in range(trials):
    pts = None
    while pts is None: pts = sample_points(info, rng)
    sig = f"calib/{os.path.basename(mp)}.{t}.sig"
    with open(sig, "w") as f:
        import itertools
        for a, b, c in itertools.combinations(range(P), 3):
            f.write(f"{a} {b} {c} {1 if orient(pts[a], pts[b], pts[c]) > 0 else -1}\n")
    r = subprocess.run(["./symrealize", str(P), str(m), str(hc), sig, str(t), restarts, iters, sig + ".pts"], capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1]
    ok += r.returncode == 0
    print(f"trial {t}: {last}", flush=True)
print(f"CALIBRATION {mp} restarts={restarts} iters={iters}: realized {ok}/{trials} known-realizable symmetric chirotopes", flush=True)

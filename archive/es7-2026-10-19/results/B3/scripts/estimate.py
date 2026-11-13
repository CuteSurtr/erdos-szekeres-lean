#!/usr/bin/env python3
"""Knuth-style estimate of total plain-CaDiCaL cost at a fixed march_cu cutoff depth.
Input: sample_node.sh lines "seed steps prod result secs". For each sample, est = prod * secs
(prod = product of surviving-cube counts on the random path = 1/probability of the node).
Timeouts (T) are counted at the cap, so the mean is a LOWER bound whenever any T occurs.
usage: estimate.py FILE [FILE...]"""
import sys, math, statistics, collections
by = collections.defaultdict(list)
for fn in sys.argv[1:]:
    for line in open(fn):
        p = line.split()
        if len(p) == 5:
            by[int(p[1]) * 6].append((int(p[2]), p[3], float(p[4])))
for d in sorted(by):
    S = by[d]; est = [pr * t for pr, r, t in S]; n = len(S); m = statistics.mean(est)
    se = statistics.stdev(est) / math.sqrt(n) if n > 1 else float('nan')
    nT = sum(r == 'T' for _, r, _ in S); ts = sorted(t for _, _, t in S)
    print(f"depth {d}: n={n} timeouts={nT} node secs median={ts[n//2]:.2f} max={ts[-1]:.1f} "
          f"mean={statistics.mean(ts):.1f}{' (>=, censored)' if nT else ''} | "
          f"est total={m:.3g} s = {m/3600:.3g} core-h{' (lower bound)' if nT else ''} +- {se:.2g} s (1 s.e.)")

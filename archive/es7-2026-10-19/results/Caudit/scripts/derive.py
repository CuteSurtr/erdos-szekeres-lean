#!/usr/bin/env python3
"""Near-extremal mirror sets with one axis point, derived from heptagon-free mirror 32-point
sets (0 axis points): for every open interval of the axis cut by the lines through two
points (and beyond the extremes), add the axis point (0, t) at a rational t inside it and
scale to integers.  Optionally first delete `drop` mirror pairs (chosen at random).
usage: derive.py <sets32 file(s)...> --drop D --per P --seed S > out
(input lines "label n x1 y1 ..."; at most P intervals per (set, deletion), all if P = 0)."""
import sys, random, argparse
from fractions import Fraction as F
from math import lcm
ap = argparse.ArgumentParser(); ap.add_argument("files", nargs="+"); ap.add_argument("--drop", type=int, default=0)
ap.add_argument("--per", type=int, default=0); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--reps", type=int, default=1)
a = ap.parse_args(); rng = random.Random(a.seed)
for fn in a.files:
    for line in open(fn):
        t = line.split()
        if len(t) < 3: continue
        n = int(t[1]); v = list(map(int, t[2:2 + 2 * n])); P0 = [(v[2 * i], v[2 * i + 1]) for i in range(n)]
        for rep in range(a.reps if a.drop else 1):
            pairs = sorted(set((abs(x), y) for x, y in P0))
            drop = set(rng.sample(pairs, a.drop)) if a.drop else set()
            P = [q for q in P0 if (abs(q[0]), q[1]) not in drop]
            ts = set()
            for i in range(len(P)):
                for j in range(i + 1, len(P)):
                    (x1, y1), (x2, y2) = P[i], P[j]
                    if x1 != x2: ts.add(F(y1 * x2 - y2 * x1, x2 - x1))
            ts = sorted(ts)
            reps = [ts[0] - 1] + [(ts[i] + ts[i + 1]) / 2 for i in range(len(ts) - 1)] + [ts[-1] + 1]
            idx = list(range(len(reps)))
            if a.per and len(idx) > a.per: idx = sorted(rng.sample(idx, a.per))
            for k in idx:
                tq = reps[k]; d = tq.denominator
                Q = [(x * d, y * d) for x, y in P] + [(0, tq.numerator)]
                print(f"{t[0]}_d{a.drop}r{rep}_iv{k} {len(Q)} " + " ".join(f"{x} {y}" for x, y in Q))

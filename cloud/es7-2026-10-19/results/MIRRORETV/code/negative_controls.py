#!/usr/bin/env python3
"""Negative controls near the critical size: sets that DO contain a convex k-gon must be reported with >= k.

For k in (8, 10, 12):
  (1) axis points on both sides: S' = R_H u mu(R_H) u {(-1,0), (W+1,0)} -- a (j-1)-cap of R, its mirror image and
      the two axis points form a convex k-gon (2(j-1) + 2 = k);
  (2) cups-caps set: R2 = G(k, j) (no j-cap, no k-cup, C(k+j-4, j-2) points) mirrored with the same placement --
      R2 contains convex k-gons, so S2 does;
  (3) the certified set S plus one extra mirror pair placed just above/below the highest point of R_H -- the
      checkers must give a value >= k-1 (we only report it);
  (4) positive control with a hard instance: the witness (k-1)-gon of S plus 30 random points of S: must be k-1.
Both checkers are run on each file (method B only when n <= 800: it is O(n^4) with an O(n^3) table).
"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from construct import G, realize, max_abs_slope, collinear_count  # noqa: E402


def run(prog, fn):
    args = [os.path.join(HERE, prog), fn] + (["-q"] if prog == "maxconv_a" else [])
    out = subprocess.run(args, capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("LARGEST"):
            return int(line.split(":")[1].split()[0])
        if line.startswith("NOT IN GENERAL") or "collinear triples =" in line and not line.endswith("= 0"):
            pass
    return out.strip().splitlines()[-1]


def write(fn, P):
    with open(fn, "w") as f:
        f.write("".join(f"{x} {y}\n" for x, y in P))


def load(fn):
    return [tuple(map(int, l.split())) for l in open(fn) if l.strip()]


def main():
    rng = random.Random(5)
    os.makedirs(os.path.join(HERE, "controls"), exist_ok=True)
    for k in (8, 10, 12):
        j = k // 2
        S = load(os.path.join(HERE, "..", "sets", f"mirror_S_k{k}.txt"))
        RH = [p for p in S if p[1] > 0]
        W = max(x for x, _ in RH)
        # (1)
        S1 = [p for p in S if p[1] != 0] + [(-1, 0), (W + 1, 0)]
        assert collinear_count(S1) == 0
        f1 = os.path.join(HERE, "controls", f"k{k}_axis_both_sides.txt")
        write(f1, S1)
        # (2)
        R2, s2 = realize(G(k, j), 1.0)
        W2 = R2[-1][0]
        H = int(s2 * (W2 + 2)) + 1
        while True:
            R2H = [(x, y + H) for x, y in R2]
            S2 = R2H + [(x, -y) for x, y in R2H] + [(-1, 0), (-2, 0)]
            if collinear_count(S2) == 0:
                break
            H += 1
        f2 = os.path.join(HERE, "controls", f"k{k}_cupscaps_G{k}_{j}.txt")
        write(f2, S2)
        # (3)
        top = max(RH, key=lambda p: p[0])
        for d in range(1, 1000):
            q = (top[0] + d, top[1] + 3 * d)
            S3 = S + [q, (q[0], -q[1])]
            if collinear_count(S3) == 0:
                break
        f3 = os.path.join(HERE, "controls", f"k{k}_plus_pair.txt")
        write(f3, S3)
        # (4)
        out = subprocess.run([os.path.join(HERE, "maxconv_a"), os.path.join(HERE, "..", "sets", f"mirror_S_k{k}.txt"), "-q"],
                             capture_output=True, text=True).stdout
        wl = [l for l in out.splitlines() if l.startswith("witness polygon")][0]
        widx = [int(t) for t in wl.split(":")[1].split()]
        rest = [i for i in range(len(S)) if i not in widx]
        P4 = [S[i] for i in widx] + [S[i] for i in rng.sample(rest, 30)]
        f4 = os.path.join(HERE, "controls", f"k{k}_witness_plus30.txt")
        write(f4, P4)
        for name, fn, expect in [("axis points on both sides", f1, f">= {k}"), (f"mirrored G({k},{j})", f2, f">= {k}"),
                                 ("S + extra pair", f3, f">= {k - 1}"), ("witness + 30 points", f4, f"= {k - 1}")]:
            a = run("maxconv_a", fn)
            nn = len(load(fn))
            b = run("maxconv_b", fn) if nn <= 800 else "(not run: n > 800)"
            print(f"k={k} {name:28s} n={nn:4d}  method A: {a}  method B: {b}  (expected {expect})", flush=True)


if __name__ == "__main__":
    main()

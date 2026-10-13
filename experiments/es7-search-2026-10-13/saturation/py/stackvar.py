#!/usr/bin/env python3
"""Stacking variants of witness(n): the repository's stack() applied to
randomly perturbed cup-cap-free blocks.

usage: stackvar.py n count seed walksteps out_batch_file

Each block cup_cap_free(n-j, j+2) of the construction is replaced by a state
of a random walk that starts at the canonical block and moves one point at a
time, accepting a move iff the block stays in general position with distinct
x-coordinates and still has no (n-j)-cup and no (j+2)-cap (x-sorted chains).
The blocks are then stacked exactly as witness(n) does.  The output batch has
the line format of gen (tag E canon canonm n coords), with E from `cgon count`
and canon from `gen canon`; lines with E != 0 are emitted as they are, so the
driver flags them.
"""
import os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from es_lower_bound_witness import stack, cup_cap_free, general_position, orient  # noqa: E402


def longest_cup_cap(P):
    Q = sorted(P)
    n = len(Q)
    cup = [[2] * n for _ in range(n)]
    cap = [[2] * n for _ in range(n)]
    best_cup = best_cap = min(n, 2)
    for j in range(n):
        for i in range(j):
            for h in range(i):
                o = orient(Q[h], Q[i], Q[j])
                if o > 0 and cup[h][i] + 1 > cup[i][j]:
                    cup[i][j] = cup[h][i] + 1
                if o < 0 and cap[h][i] + 1 > cap[i][j]:
                    cap[i][j] = cap[h][i] + 1
            best_cup = max(best_cup, cup[i][j]); best_cap = max(best_cap, cap[i][j])
    return best_cup, best_cap


def walk_block(k, l, steps, rng):
    S = rng.choice([1, 1, 2])  # x scale; S=1 keeps x fixed (only y moves), S=2 allows +-1 in x
    B = [(x * S, y * S) for x, y in cup_cap_free(k, l)]
    if len(B) <= 2:
        return B
    ys = [y for _, y in B]
    yspan = max(1, max(ys) - min(ys))
    for _ in range(steps):
        i = rng.randrange(len(B))
        x, y = B[i]
        nx = x + rng.randint(-S + 1, S - 1) if S > 1 else x
        ny = y + int(round(rng.uniform(-1, 1) * yspan * rng.choice([0.05, 0.2, 0.5])))
        C = B[:i] + [(nx, ny)] + B[i + 1:]
        if len({p[0] for p in C}) != len(C) or not general_position(C):
            continue
        cu, ca = longest_cup_cap(C)
        if cu < k and ca < l:
            B = C
    return B


def variant(n, steps, rng):
    points = cup_cap_free(n, 2)
    for j in range(1, n - 1):
        points = stack(-1, points, walk_block(n - j, j + 2, steps, rng))
    return points


def main():
    n, count, seed, steps, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = random.Random(seed)
    sets = []
    for c in range(count):
        P = variant(n, steps, rng)
        if max(abs(v) for p in P for v in p) >= 2 ** 26:
            continue
        sets.append(P)
    inp = "".join(f"{len(P)} " + " ".join(f"{x} {y}" for x, y in P) + "\n" for P in sets)
    can = subprocess.run([os.path.join(ROOT, "bin", "gen"), "canon"], input=inp, capture_output=True, text=True,
                         check=True).stdout.splitlines()
    with open(out, "w") as f:
        for c, (P, cl) in enumerate(zip(sets, can)):
            txt = "".join(f"{x} {y}\n" for x, y in P)
            cg = subprocess.run([os.path.join(ROOT, "bin", "cgon"), "count", str(n)], input=txt, capture_output=True,
                                text=True).stdout.split()
            E = int([t for t in cg if t.startswith(f"c{n}=")][0].split("=")[1])
            f.write(f"SV{seed}_{c} {E} {cl} {len(P)} " + " ".join(f"{x} {y}" for x, y in P) + "\n")
    print(f"stackvar n={n} seed={seed} written={len(sets)}")


if __name__ == "__main__":
    main()

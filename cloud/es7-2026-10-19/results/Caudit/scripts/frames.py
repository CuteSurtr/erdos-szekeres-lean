#!/usr/bin/env python3
"""Compute orientation assignments of given mirror-symmetric sets (one axis point) in the
plain x-sorted frame (.xs), frame (ii) (.ii, interior sets) and frame (i) (.i, hull-vertex
sets).  usage: frames.py <sets> <outprefix>; <sets> lines: "id n x1 y1 ... xn yn" (integers).
x-ties are removed by the checked symmetric perturbation."""
import sys, os, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import *
from multiprocessing import Pool


def work(line):
    t = line.split(); sid, n = t[0], int(t[1]); v = list(map(int, t[2:2 + 2 * n]))
    P = [(v[2 * i], v[2 * i + 1]) for i in range(n)]
    assert is_mirror(P) and general_position(P)
    axis = [q for q in P if q[0] == 0]; assert len(axis) == 1
    rng = random.Random(sid); o0 = orient_all(P)
    vertex = P.index(axis[0]) in hull_vertices(P)
    for _ in range(6):
        ok = len(set(q[0] for q in P)) == n
        if ok and vertex:
            try: frame_i(P)
            except AssertionError: ok = False
        if ok: break
        P2 = sym_perturb(P, rng); assert np.array_equal(orient_all(P2), o0); P = P2
    xs = bits(orient_all(sorted(P)))
    if vertex: return sid, "i", bits(frame_i(P)[1]), xs
    return sid, "ii", bits(frame_ii(P)[1]), xs


if __name__ == "__main__":
    lines = [l for l in open(sys.argv[1]) if l.strip()]
    pre = sys.argv[2]
    f = {k: open(f"{pre}.{k}.txt", "w") for k in ("i", "ii", "xs")}
    cnt = {"i": 0, "ii": 0}
    with Pool(os.cpu_count()) as pool:
        for sid, kind, b, xs in pool.imap_unordered(work, lines, chunksize=4):
            f[kind].write(f"{sid} {b}\n"); f["xs"].write(f"{sid} {xs}\n"); cnt[kind] += 1
    print(json.dumps(cnt))

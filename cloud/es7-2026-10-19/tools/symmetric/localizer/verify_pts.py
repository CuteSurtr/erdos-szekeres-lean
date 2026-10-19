#!/usr/bin/env python3
"""Independent verification of an integer point set claimed to realize a chirotope.
  1. every orientation (exact Python integers) equals the required sign in file.sig (0-based a<b<c)
  2. general position (no zero orientation), all points distinct
  3. symmetry: p[o*m+r] = R^r p[o*m] exactly (m = 2: antipodes; m = 4: quarter turns)
  4. largest convex subset via the repo DP (scripts/es_lower_bound_witness.largest_convex_subset)
  5. brute force over all K-subsets with ./brute7 (C, __int128)
usage: verify_pts.py N m K file.sig file.pts
"""
import itertools
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.environ.get("ES_REPO", "."), "scripts"))  # ES_REPO = repository root
from es_lower_bound_witness import largest_convex_subset, orient, general_position  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    N, m, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    sigpath, ptspath = sys.argv[4], sys.argv[5]
    pts = [tuple(map(int, l.split())) for l in open(ptspath) if l.strip()]
    assert len(pts) == N, (len(pts), N)
    sig = {}
    for l in open(sigpath):
        a, b, c, s = map(int, l.split())
        sig[(a, b, c)] = s
    assert len(sig) == N * (N - 1) * (N - 2) // 6
    mism = zero = 0
    for (a, b, c), s in sig.items():
        d = orient(pts[a], pts[b], pts[c])
        if d == 0:
            zero += 1
        elif (d > 0) != (s > 0):
            mism += 1
    distinct = len(set(pts)) == N
    gp = general_position(pts)
    sym_ok = True
    if m == 2:
        for o in range(N // 2):
            sym_ok &= pts[2 * o + 1] == (-pts[2 * o][0], -pts[2 * o][1])
    elif m == 4:
        for o in range(N // 4):
            x, y = pts[4 * o]
            sym_ok &= pts[4 * o + 1] == (-y, x) and pts[4 * o + 2] == (-x, -y) and pts[4 * o + 3] == (y, -x)
    big = largest_convex_subset(pts)
    r = subprocess.run([os.path.join(HERE, "brute7"), str(K), ptspath], capture_output=True, text=True)
    brute_line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "no output"
    ok = mism == 0 and zero == 0 and distinct and gp and sym_ok and big < K and r.returncode == 0
    print(f"VERIFY {os.path.basename(ptspath)}: orientation_mismatches={mism} zero_orientations={zero} distinct={distinct} "
          f"general_position={gp} exact_symmetry(m={m})={sym_ok} largest_convex_subset(DP)={big} brute7: {brute_line} -> {'OK' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

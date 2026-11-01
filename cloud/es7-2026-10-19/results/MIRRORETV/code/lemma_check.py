#!/usr/bin/env python3
"""Third, structural route to conv(S) (exact integer arithmetic; uses the placement lemma).

Placement lemma (proved in PROOFS.md, Lemma 5.3): let S = R_H u mu(R_H) u A with mu(x,y) = (x,-y), R_H in {y > 0}, R_H with
distinct abscissae, |A| <= 2, A on the axis strictly to the left of every point of R_H, S in general position, and
   (*) for every r in R_H and z in mu(R_H) u A:  x_r = x_z  or  |slope(r,z)| > s_R := max |slope| inside R_H.
Then every subset of S in convex position has at most max(conv(R_H), 2 cap(R_H) + min(|A|,1), cap(R_H) + |A|)
points (= max(conv, 2 cap + 1, cap + 2) for two axis points, max(conv, 2 cap) for none).

This script checks the hypotheses exactly, checks that R_H is a translate of the given R file, and runs
maxconv_a (largest convex subset) and longcap (longest cap) on R to evaluate the bound.
Usage: lemma_check.py SFILE RFILE
"""
import sys
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def load(fn):
    return [tuple(map(int, l.split())) for l in open(fn) if l.strip() and not l.startswith("#")]


def main():
    S = load(sys.argv[1])
    R = load(sys.argv[2])
    RH = [p for p in S if p[1] > 0]
    MR = [p for p in S if p[1] < 0]
    A = [p for p in S if p[1] == 0]
    assert len(set(S)) == len(S)
    assert sorted((x, -y) for x, y in RH) == sorted(MR), "not mirror symmetric"
    assert len(A) <= 2
    xs = [x for x, _ in RH]
    assert len(set(xs)) == len(xs), "abscissae of R_H not distinct"
    assert all(a[0] < min(xs) for a in A), "axis points not left of R_H"
    # R_H is a translate of R by (0, H)
    RHs = sorted(RH)
    Rs = sorted(R)
    H = RHs[0][1] - Rs[0][1]
    assert RHs[0][0] == Rs[0][0] and [(x, y + H) for x, y in Rs] == RHs, "R_H is not R + (0,H)"
    # s_R = max |slope| inside R_H, as num/den
    num, den = 0, 1
    P = sorted(RH)
    for i in range(len(P)):
        xi, yi = P[i]
        for j in range(i + 1, len(P)):
            dx = P[j][0] - xi
            dy = abs(P[j][1] - yi)
            if dy * den > num * dx:
                num, den = dy, dx
    # condition (*)
    bad = 0
    Z = MR + A
    for (xr, yr) in RH:
        for (xz, yz) in Z:
            if xr == xz:
                continue
            if not ((yr - yz) * den > num * abs(xr - xz)):
                bad += 1
    print(f"S: {len(S)} points = 2*{len(RH)} + {len(A)} axis points; H = {H}; s_R = {num}/{den}")
    print(f"condition (*) violations: {bad}")
    outA = subprocess.run([os.path.join(HERE, "maxconv_a"), sys.argv[2], "-q"], capture_output=True, text=True).stdout
    conv = [int(l.split(":")[1].split()[0]) for l in outA.splitlines() if l.startswith("LARGEST")][0]
    outC = subprocess.run([os.path.join(HERE, "longcap"), sys.argv[2]], capture_output=True, text=True).stdout
    cap = int(outC.split("longest cap")[1].split(",")[0])
    print(f"R: largest convex subset {conv} (maxconv_a), longest cap {cap} (longcap)")
    print(outC.strip())
    if bad == 0:
        t2, t3 = 2 * cap + min(len(A), 1), cap + len(A)
        print(f"LEMMA BOUND: every convex subset of S has at most max({conv}, {t2}, {t3}) = "
              f"{max(conv, t2, t3)} points")


if __name__ == "__main__":
    main()

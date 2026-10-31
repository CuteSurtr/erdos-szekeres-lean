#!/usr/bin/env python3
"""Build the AlphaEvolve-derived and near-full signotopes (exact).

usage: make_extra_sets.py INPUTS_DIR BRUTE_BIN TMPDIR OUTDIR

* alphaevolve_pts.json `points_7` (33 points; decimals read exactly as Fractions and scaled to
  integers by the common denominator). Its convex 7-subsets are found with brute_kgon; we expect
  exactly one. Deleting each of its 7 vertices gives 7 heptagon-free 32-point sets (ae.sig);
  deleting a non-vertex gives a 32-point set that keeps the 7-gon (negative control, ae_bad.sig).
* nearfull_p2c.txt / nearfull_p2d.txt: `tag k n x1 y1 ...` 33-point sets with convex 7-gons
  (negative controls, nearfull.sig).
"""
import json
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import to_sig, brute  # noqa: E402


def main():
    inp, bb, tmp, out = sys.argv[1:5]
    os.makedirs(out, exist_ok=True)
    d = json.load(open(os.path.join(inp, 'alphaevolve_pts.json')), parse_float=Fraction)
    P = [(Fraction(x), Fraction(y)) for x, y in d['points_7']]
    den = 1
    for x, y in P:
        den = den * x.denominator // math.gcd(den, x.denominator)
        den = den * y.denominator // math.gcd(den, y.denominator)
    Q = [(int(x * den), int(y * den)) for x, y in P]
    assert all(Fraction(a, den) == x and Fraction(b, den) == y for (a, b), (x, y) in zip(Q, P))
    spts, signs, sh = to_sig(Q)
    b = brute(bb, 33, 7, signs, tmp, 'ae33')
    info = {"ae33_sheared": sh, "ae33_violations": b["violations"], "ae33_convex7": b["convex"],
            "ae33_convex7_sorted_labels": b["first_convex"]}
    assert b["convex"] == 1, info
    hept = b["first_convex"][0]  # 1-based labels in x-sorted order
    # original indices (0-based in the JSON) of the heptagon vertices
    orig = [Q.index(spts[v - 1]) for v in hept]
    info["ae33_convex7_json_indices"] = sorted(orig)
    with open(os.path.join(out, 'ae33.sig'), 'w') as f:
        f.write(f"AE33 AE33 alphaevolve - 33 {signs}\n")
    with open(os.path.join(out, 'ae33.pts'), 'w') as f:
        f.write("AE33 33 " + " ".join(f"{x} {y}" for x, y in spts) + "\n")
    good, bad = [], []
    for v in range(1, 34):
        pts32 = [p for t, p in enumerate(spts, 1) if t != v]
        s32, sg32, _ = to_sig(pts32)
        bb32 = brute(bb, 32, 7, sg32, tmp, f'ae{v}')
        rec = (v, Q.index(spts[v - 1]), s32, sg32, bb32)
        (good if v in hept else bad).append(rec)
    with open(os.path.join(out, 'ae.sig'), 'w') as f, open(os.path.join(out, 'ae.pts'), 'w') as fp:
        for v, j, s32, sg32, bb32 in good:
            assert bb32["convex"] == 0 and bb32["violations"] == 0
            f.write(f"AEdel{j} AE del_json_idx_{j} alphaevolve 32 {sg32}\n")
            fp.write(f"AEdel{j} 32 " + " ".join(f"{x} {y}" for x, y in s32) + "\n")
    with open(os.path.join(out, 'ae_bad.sig'), 'w') as f:
        for v, j, s32, sg32, bb32 in bad[:3]:
            assert bb32["convex"] >= 1
            f.write(f"AEbad{j} AE del_json_idx_{j} alphaevolve 32 {sg32}\n")
    info["ae_good_sets"] = len(good)
    info["ae_bad_convex7_counts"] = [r[4]["convex"] for r in bad]
    # near-full sets
    nf = []
    for fn in ('nearfull_p2c.txt', 'nearfull_p2d.txt'):
        for lineno, line in enumerate(open(os.path.join(inp, fn)), 1):
            t = line.split()
            if not t:
                continue
            n = int(t[2])
            vals = list(map(int, t[3:]))
            assert len(vals) == 2 * n
            pts = [(vals[2 * a], vals[2 * a + 1]) for a in range(n)]
            s, sg, _ = to_sig(pts)
            nf.append((f"{fn[9:12]}_L{lineno}", n, sg, s))
    with open(os.path.join(out, 'nearfull.sig'), 'w') as f:
        for lab, n, sg, _ in nf:
            f.write(f"NF_{lab} NF {lab} - {n} {sg}\n")
    info["nearfull_sets"] = len(nf)
    info["nearfull_sizes"] = sorted(set(n for _, n, _, _ in nf))
    # extra extension targets: delete each vertex of each near-full set's convex 7-gon(s)
    nd = 0
    hept_counts = []
    with open(os.path.join(out, 'nf_del.sig'), 'w') as f, open(os.path.join(out, 'nf_del.pts'), 'w') as fp:
        for lab, n, sg, spts in nf:
            b = brute(bb, n, 7, sg, tmp, 'nf')
            hept_counts.append(b["convex"])
            if b["convex"] != 1:
                continue
            for v in b["first_convex"][0]:
                pts32 = [p for t, p in enumerate(spts, 1) if t != v]
                s32, sg32, _ = to_sig(pts32)
                b32 = brute(bb, 32, 7, sg32, tmp, 'nf32')
                assert b32["convex"] == 0 and b32["violations"] == 0
                f.write(f"NFd_{lab}_v{v} NFd {lab}_v{v} - 32 {sg32}\n")
                fp.write(f"NFd_{lab}_v{v} 32 " + " ".join(f"{x} {y}" for x, y in s32) + "\n")
                nd += 1
    info["nearfull_convex7_counts"] = sorted(set(hept_counts))
    info["nf_del_sets"] = nd
    json.dump(info, open(os.path.join(out, 'extra_meta.json'), 'w'), indent=1)
    print(json.dumps(info))


if __name__ == '__main__':
    main()

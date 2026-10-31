#!/usr/bin/env python3
"""Build the A2 base sample (exact, Python ints).

usage: make_bases.py WORKDIR INPUTS_DIR PER_TAG SEED OUT.jsonl

* PER_TAG seeded-random pool sets from each source tag (pool.sig / pool.pts from A's convert.py),
  avoiding A's sample107.txt where possible, plus the 7 AlphaEvolve-derived 32-point sets.
* Near-miss sets: each of the 273 nearfull_p2c/p2d 33-point sets and AlphaEvolve's 33-point set
  (exactly one convex 7-gon each, found by brute_kgon). One heptagon vertex v (seeded random) is
  deleted; the 32-point remainder is re-sorted and re-checked by brute_kgon (must be 0 convex
  7-subsets, 0 axiom violations). We keep the 6 surviving heptagon vertices (32-point labels) and
  the coordinates of the deleted vertex, for the 'hv' and 'hnear' deletion kinds.
Output: one JSON line per base: id, src, signs, pts (x-sorted), hept6 (or []), vdel (or null).
"""
import json
import os
import random
import sys
from fractions import Fraction
import math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'A', 'scripts'))
from sigutil import to_sig, brute  # noqa: E402


def main():
    wd, inp, per_tag, seed, out = sys.argv[1:6]
    per_tag, rng = int(per_tag), random.Random(int(seed))
    bb, tmp = os.path.join(wd, 'brute_kgon'), os.path.join(wd, 'tmp')
    a_sample = set(l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                        '..', '..', 'A', 'data', 'sample107.txt')))
    sig, tag, pts = {}, {}, {}
    for l in open(os.path.join(wd, 'pool.sig')):
        t = l.split()
        sig[t[0]], tag[t[0]] = t[-1], t[1]
    for l in open(os.path.join(wd, 'pool.pts')):
        t = l.split()
        v = list(map(int, t[2:]))
        pts[t[0]] = [(v[2 * a], v[2 * a + 1]) for a in range(32)]
    bases = []
    for tg in sorted(set(tag.values())):
        ids = [i for i in sig if tag[i] == tg and i not in a_sample]
        for i in rng.sample(ids, min(per_tag, len(ids))):
            bases.append({"id": f"P{i}", "src": tg, "signs": sig[i], "pts": pts[i], "hept6": [], "vdel": None})
    for l in open(os.path.join(wd, 'extra', 'ae.sig')):
        t = l.split()
        s = t[0]
        p = [l2.split() for l2 in open(os.path.join(wd, 'extra', 'ae.pts')) if l2.split()[0] == s][0]
        v = list(map(int, p[2:]))
        bases.append({"id": s, "src": "AEdel", "signs": t[-1], "pts": [(v[2 * a], v[2 * a + 1]) for a in range(32)],
                      "hept6": [], "vdel": None})
    # near-miss 33-point sets
    nm = []
    for fn in ('nearfull_p2c.txt', 'nearfull_p2d.txt'):
        for ln, line in enumerate(open(os.path.join(inp, fn)), 1):
            t = line.split()
            if not t:
                continue
            v = list(map(int, t[3:]))
            nm.append((f"NM{fn[9:12]}L{ln}", fn[9:12], [(v[2 * a], v[2 * a + 1]) for a in range(int(t[2]))]))
    d = json.load(open(os.path.join(inp, 'alphaevolve_pts.json')), parse_float=Fraction)
    P = [(Fraction(x), Fraction(y)) for x, y in d['points_7']]
    den = 1
    for x, y in P:
        den = math.lcm(den, x.denominator, y.denominator)
    nm.append(("NMae33", "AE33", [(int(x * den), int(y * den)) for x, y in P]))
    for nid, src, P33 in nm:
        s33, g33, _ = to_sig(P33)
        b = brute(bb, 33, 7, g33, tmp, 'nm')
        assert b["violations"] == 0 and b["convex"] == 1, (nid, b)
        hept = b["first_convex"][0]
        v = rng.choice(hept)
        vpt = s33[v - 1]
        p32 = [p for t, p in enumerate(s33, 1) if t != v]
        s32, g32, _ = to_sig(p32)
        b32 = brute(bb, 32, 7, g32, tmp, 'nm32')
        assert b32["violations"] == 0 and b32["convex"] == 0
        # surviving heptagon vertices, as labels in the 32-point x-order (shear-safe: look up points)
        hpts = [s33[h - 1] for h in hept if h != v]
        if s32 == sorted(p32):
            h6 = sorted(s32.index(q) + 1 for q in hpts)
        else:  # sheared: the shear is order-preserving lexicographically
            h6 = sorted(sorted(p32).index(q) + 1 for q in hpts)
        sheared = s32 != sorted(p32)
        if sheared:  # same exact shear as to_sig applied to p32, so vdel is in the base's frame
            L = 2 * max(abs(p[1]) for p in p32) + 1
            vpt = (L * vpt[0] + vpt[1], vpt[1])
        bases.append({"id": f"{nid}_v{v}", "src": "NM_" + src, "signs": g32, "pts": s32, "hept6": h6,
                      "vdel": list(vpt), "vdel_sheared": sheared})
    with open(out, 'w') as f:
        for b in bases:
            f.write(json.dumps(b) + "\n")
    from collections import Counter
    print(json.dumps({"bases": len(bases), "by_src": Counter(b["src"] for b in bases)}))


if __name__ == '__main__':
    main()

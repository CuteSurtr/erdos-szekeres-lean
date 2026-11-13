#!/usr/bin/env python3
"""Find and print one canonical tie frame where the tie matters: a largest convex polygon has an
edge parallel to l at its left side.  Prints the set, d, the tied pair, the longest chain under the
parity-defined B (it uses the tied partner) and checks it is a real convex polygon; also shows that
the strict x-order relation (ties dropped) has a shorter longest chain.
usage: find_example.py SEED m"""
import itertools
import json
import random
import sys

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import ties  # noqa: E402


def longest_chain(F, m, drop_ties):
    """return (length, chain) of a longest chain x | p1..pr under B (least fixpoint, explicit DP)."""
    n = 3 * m
    O = lambda a, b, c: ties.orient(F.lab[a], F.lab[b], F.lab[c]) > 0
    tset = set(F.ties)

    def B(a, b):
        if drop_ties and (min(a, b), max(a, b)) in tset:
            return False
        return bool(F.B[(a, b)]) if a < b else not F.B[(b, a)]
    best = (0, None)
    for x in range(n):
        P = [p for p in range(n) if p != x and B(x, p)]
        # chains of length 2: (a, b) with ccw(x, a, b); extend by c with ccw(x, b, c) and ccw(a, b, c)
        cur = {(a, b): [a, b] for a in P for b in P if a != b and O(x, a, b)}
        r = 2
        while cur:
            if r > best[0]:
                best = (r, [x] + next(iter(cur.values())))
            nxt = {}
            for (a, b), ch in cur.items():
                for c in P:
                    if c not in (a, b) and O(x, b, c) and O(a, b, c) and (b, c) not in nxt:
                        nxt[(b, c)] = ch + [c]
            cur = nxt
            r += 1
            assert r <= n
    return best


def main():
    seed, m = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    for t in range(2000):
        S, shape = ties.random_set(m, rng)
        g, wit = ties.largest_convex(S, witness=True)
        H, gaps = ties.canonical_gaps(S, m)
        for p, (u, w) in gaps:
            for i in range(len(wit)):
                a, b = wit[i], wit[(i + 1) % len(wit)]
                s = (b[0] - a[0], b[1] - a[1])
                for d in (s, (-s[0], -s[1])):
                    if not ties.in_cone(u, w, d):
                        continue
                    F = ties.Frame(S, m, d, p)
                    hres = sorted({F.idx[q] % m for q in H})
                    if not (len(hres) in (1, 2) and (len(hres) == 1 or hres[1] <= m // 2)):
                        continue
                    L1, ch1 = longest_chain(F, m, drop_ties=False)
                    L0, ch0 = longest_chain(F, m, drop_ties=True)
                    if L0 + 1 < g:
                        x = ch1[0]
                        tied = [(i_, j_) for (i_, j_) in F.ties if x in (i_, j_)]
                        poly = [F.lab[q] for q in ch1]
                        out = {"seed": seed, "set_index": t, "shape": shape, "m": m, "n": 3 * m,
                               "reps": S[::3], "d": F.d, "case_hull_residues": hres,
                               "largest_convex": g, "tied_pairs_labels": F.ties,
                               "x_coords_of_tied": [[F.x[i_], F.x[j_]] for i_, j_ in F.ties],
                               "longest_chain_parityB_labels": ch1, "its_length_plus_x": L1 + 1,
                               "chain_uses_tied_partner_of_x": bool(tied) and any(
                                   (i_ in ch1[1:] or j_ in ch1[1:]) for i_, j_ in tied),
                               "chain_is_convex_polygon": len(ties.hull_ccw(poly)) == len(poly),
                               "longest_chain_strict_relation_plus_x": L0 + 1}
                        print(json.dumps(out))
                        return
    print("none found")


if __name__ == "__main__":
    main()

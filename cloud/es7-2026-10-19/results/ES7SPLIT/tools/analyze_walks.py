#!/usr/bin/env python3
"""Analyse generator output lines 'tag E canon canonm n x1 y1 ...' (7-gon-free 32-point sets):
dedupe by order type up to reflection (canonm), re-verify exactly (general position, largest convex
subset), and record hull size, layer profile, nontrivial z-splits (types), hull-vertex frame caps/cups,
and ear nesting for hexagonal hulls.  Output: JSON lines."""
import json
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from geom import general_position, largest_convex_subset, hull, layers
import splits
from hullstats import ears, vertex_frame_chains


def main():
    seen = set()
    out = open(sys.argv[-1], "w")
    for fn in sys.argv[1:-1]:
        for line in open(fn):
            f = line.split()
            tag, E, canonm, n = f[0], int(f[1]), f[3], int(f[4])
            c = list(map(int, f[5:]))
            P = list(zip(c[0::2], c[1::2]))
            if canonm in seen:
                continue
            seen.add(canonm)
            assert E == 0 and len(P) == n
            gp = general_position(P)
            gon = largest_convex_subset(P)
            H = hull(P)
            S = splits.all_splits(P)
            types = Counter()
            for A, B, z in S:
                d = splits.describe(P, A, B, z)
                types[(d["sizes"][0], d["sizes"][1], d.get("capA"), d.get("cupB"))] += 1
            rec = dict(file=fn.rsplit('/', 1)[-1], tag=tag, n=n, general_position=gp, gon=gon, hull=len(H),
                       layers=[len(L) for L in layers(P)], n_splits=len(S),
                       split_types={str(k): v for k, v in types.items()},
                       vframe=vertex_frame_chains(P, H),
                       ears=ears(P, H) if len(H) == 6 else None)
            out.write(json.dumps(rec) + "\n")
            out.flush()


if __name__ == "__main__":
    main()

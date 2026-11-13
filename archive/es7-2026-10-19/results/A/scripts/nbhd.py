#!/usr/bin/env python3
"""r-point abstract neighbourhood search (delete r points, re-insert r+1).

usage: nbhd.py WORKDIR SAMPLE.txt R PER_KIND CONFLICT_LIMIT OUTDIR [workers] [seed] [kinds]
       (kinds: comma-separated subset of win,geo,rand; default all three)

SAMPLE.txt: set ids (one per line) from pool.sig / extra/ae.sig (32-point sets).
For every set, deletion sets D (|D| = R) of three kinds, PER_KIND each:
  'win'  : R consecutive points in x-order (random start),
  'geo'  : a random point and its R-1 Euclidean nearest neighbours (original coordinates),
  'rand' : R uniformly random points.
The kept 32-R points keep all their orientations (assumptions). Solver option lucky=0 (CaDiCaL's
'lucky' pre-checks dominated the per-call time; it does not change any answer). New points: one in each deleted
point's x-slot (the gap between kept points it occupied) plus one extra point, tried in every gap
e = 0..32-R (e = number of kept points left of it). Base CNF: 33 points, no symmetry breaking.
Job label: N<id>_<kind>_<d1-d2-..>; tag: e<e>@<new indices>.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import triples  # noqa: E402
from run_ext import run_pool  # noqa: E402


def load(wd):
    sig, pts = {}, {}
    for fn in ('pool.sig', os.path.join('extra', 'ae.sig')):
        for l in open(os.path.join(wd, fn)):
            t = l.split()
            sig[t[0]] = t[-1]
    for fn in ('pool.pts', os.path.join('extra', 'ae.pts')):
        for l in open(os.path.join(wd, fn)):
            t = l.split()
            v = list(map(int, t[2:]))
            pts[t[0]] = [(v[2 * a], v[2 * a + 1]) for a in range(int(t[1]))]
    return sig, pts


def deletion_sets(P, R, per_kind, rng, kinds=('win', 'geo', 'rand')):
    n = len(P)
    out = []
    seen = set()

    def add(kind, D):
        D = tuple(sorted(D))
        if D not in seen:
            seen.add(D)
            out.append((kind, D))

    for _ in range(per_kind if 'win' in kinds else 0):
        s = rng.randint(1, n - R + 1)
        add('win', range(s, s + R))
    for _ in range(per_kind if 'geo' in kinds else 0):
        c = rng.randint(1, n)
        cx, cy = P[c - 1]
        order = sorted(range(1, n + 1), key=lambda a: (P[a - 1][0] - cx) ** 2 + (P[a - 1][1] - cy) ** 2)
        add('geo', order[:R])
    for _ in range(per_kind if 'rand' in kinds else 0):
        add('rand', rng.sample(range(1, n + 1), R))
    return out


def blocks_for(sid, signs, D, kind, R, n=32):
    M = n + 1
    keep = [a for a in range(1, n + 1) if a not in D]
    T = triples(n)
    ks = set(keep)
    old = ''.join(c for t, c in zip(T, signs) if t[0] in ks and t[1] in ks and t[2] in ks)
    gaps = [sum(1 for a in keep if a < d) for d in D]  # deleted point d sits after `gap` kept points
    lab = f"N{sid}_{kind}_{'-'.join(map(str, D))}"
    lines = [f"S {lab} {len(keep)} {old}\n"]
    for e in range(0, len(keep) + 1):
        g = gaps + [e]
        mp = [a + sum(1 for x in g if x <= a - 1) for a in range(1, len(keep) + 1)]
        new = [t for t in range(1, M + 1) if t not in set(mp)]
        assert len(new) == R + 1
        lines.append(f"J e{e}@{'.'.join(map(str, new))} " + " ".join(map(str, mp)) + "\n")
    return "".join(lines)


def main():
    wd, sample, R, per_kind, climit, outdir = sys.argv[1:7]
    workers = int(sys.argv[7]) if len(sys.argv) > 7 else os.cpu_count()
    seed = int(sys.argv[8]) if len(sys.argv) > 8 else 1
    kinds = tuple(sys.argv[9].split(',')) if len(sys.argv) > 9 else ('win', 'geo', 'rand')
    R, per_kind = int(R), int(per_kind)
    sig, pts = load(wd)
    ids = [l.strip() for l in open(sample) if l.strip()]
    rng = random.Random(seed * 1000 + R)
    blocks = []
    meta = []
    for sid in ids:
        for kind, D in deletion_sets(pts[sid], R, per_kind, rng, kinds):
            blocks.append(blocks_for(sid, sig[sid], D, kind, R))
            meta.append({"id": sid, "kind": kind, "D": D})
    os.makedirs(outdir, exist_ok=True)
    json.dump(meta, open(os.path.join(outdir, 'deletions.json'), 'w'))
    info = run_pool(os.path.join(wd, 'ext_solve'), os.path.join(wd, 'n33k7.cnf'), 33, climit, blocks, outdir, workers,
                    opts=['lucky=0'])
    info.update({"R": R, "sets": len(ids), "deletion_sets": len(blocks)})
    json.dump(info, open(os.path.join(outdir, 'run.json'), 'w'))
    print(json.dumps(info))


if __name__ == '__main__':
    main()

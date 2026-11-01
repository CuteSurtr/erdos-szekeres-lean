#!/usr/bin/env python3
"""A2: r-point abstract neighbourhood search on realizable bases (delete r, re-insert r+1).

usage: nbhd2.py --bases B.jsonl --r R --out DIR [--kinds win,geo,rand,hv,hnear] [--per-kind K]
                [--modes slot,free] [--w 2] [--cap 200] [--climit 300000] [--workers 4] [--seed 1]
                [--src PREFIX[,PREFIX]] [--control]

Bases from make_bases.py (32-point x-sorted signotopes with coordinates). For each base, deletion
sets D (|D| = R) of these kinds:
  win   : R consecutive points in x-order;          geo  : a random point and its R-1 nearest;
  rand  : R uniformly random points;
  hv    : (near-miss bases only) R of the 6 surviving heptagon vertices (R <= 6), random;
  hnear : (near-miss bases only) the R points nearest to the deleted heptagon vertex.
The 32-R kept points keep every orientation (assumptions in ext_solve; base CNF gen_cnf.py 33 7).
Insertion modes for the R+1 new points (gap e = number of kept points to its left):
  slot : as task A - one new point in each deleted point's gap, plus one extra in every gap e;
  free : every multiset of R+1 gaps inside the window [min gap - w, max gap + w] (new points'
         x-ranks free within the window); if more than `cap`, a seeded random sample of `cap`.
Placements are de-duplicated per deletion set (slot first). --control: positive control in the
32-point CNF, re-inserting exactly R points with mode free (the original placement is always
included, so every deletion set must have at least one SAT answer).
Labels: <base>:<kind>:<d1-d2-..>, tags: <mode>@<new indices>.
"""
import argparse
import itertools
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'A', 'scripts'))
from sigutil import triples  # noqa: E402
from run_ext import run_pool  # noqa: E402

T32 = triples(32)


def deletion_sets(b, R, kinds, per_kind, rng):
    P, n = b["pts"], 32
    out, seen = [], set()

    def add(kind, D):
        D = tuple(sorted(D))
        if len(D) == R and D not in seen:
            seen.add(D)
            out.append((kind, D))

    def near(c, k, excl=()):
        cx, cy = c
        order = sorted((a for a in range(1, n + 1) if a not in excl),
                       key=lambda a: (P[a - 1][0] - cx) ** 2 + (P[a - 1][1] - cy) ** 2)
        return order[:k]
    nm = bool(b["hept6"])
    for kind in kinds:
        if kind in ('hv', 'hnear') and not nm:
            continue
        if kind == 'hv' and R > 6:
            continue
        tries = per_kind if kind != 'hnear' else 1
        for _ in range(tries * 3):
            if sum(1 for k, _ in out if k == kind) >= tries:
                break
            if kind == 'win':
                s = rng.randint(1, n - R + 1)
                add(kind, range(s, s + R))
            elif kind == 'geo':
                add(kind, near(P[rng.randint(1, n) - 1], R))
            elif kind == 'rand':
                add(kind, rng.sample(range(1, n + 1), R))
            elif kind == 'hv':
                add(kind, rng.sample(b["hept6"], R))
            elif kind == 'hnear':
                add(kind, near(b["vdel"], R))
    return out


def placements(gaps, R_new, nk, modes, w, cap, rng):
    seen, out = set(), []

    def add(mode, g):
        g = tuple(sorted(g))
        if g not in seen:
            seen.add(g)
            out.append((mode, g))
    if 'slot' in modes:
        for e in range(nk + 1):
            add('slot', list(gaps) + [e])
    if 'free' in modes:
        lo, hi = max(0, min(gaps) - w), min(nk, max(gaps) + w)
        G = hi - lo + 1
        total = math.comb(G + R_new - 1, R_new)
        if total <= cap:
            for g in itertools.combinations_with_replacement(range(lo, hi + 1), R_new):
                add('free', g)
        else:
            add('free', gaps)  # control: original placement always included
            k = 0
            while k < cap * 4 and sum(1 for m, _ in out if m == 'free') < cap:
                add('free', [rng.randint(lo, hi) for _ in range(R_new)])
                k += 1
    return out


def block(b, kind, D, R_new, modes, w, cap, rng, M):
    keep = [a for a in range(1, 33) if a not in D]
    ks = set(keep)
    old = ''.join(c for t, c in zip(T32, b["signs"]) if t[0] in ks and t[1] in ks and t[2] in ks)
    gaps = [sum(1 for a in keep if a < d) for d in D]
    nk = len(keep)
    lab = f"{b['id']}:{kind}:{'-'.join(map(str, D))}"
    lines = [f"S {lab} {nk} {old}\n"]
    pl = placements(gaps if R_new > len(D) else gaps, R_new, nk, modes, w, cap, rng)
    if R_new == len(D):  # control: drop slot mode's extra point, keep free placements
        pl = [(m, g) for m, g in pl if m == 'free']
    for mode, g in pl:
        mp = [a + sum(1 for x in g if x <= a - 1) for a in range(1, nk + 1)]
        new = [t for t in range(1, M + 1) if t not in set(mp)]
        assert len(new) == R_new and len(mp) == nk
        lines.append(f"J {mode}@{'.'.join(map(str, new))} " + " ".join(map(str, mp)) + "\n")
    return "".join(lines), len(pl)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bases', required=True)
    ap.add_argument('--r', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--kinds', default='win,geo,rand,hv,hnear')
    ap.add_argument('--per-kind', type=int, default=1)
    ap.add_argument('--modes', default='slot,free')
    ap.add_argument('--w', type=int, default=2)
    ap.add_argument('--cap', type=int, default=200)
    ap.add_argument('--climit', type=int, default=300000)
    ap.add_argument('--workers', type=int, default=os.cpu_count())
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--src', default='')
    ap.add_argument('--limit-bases', type=int, default=0)
    ap.add_argument('--control', action='store_true')
    ap.add_argument('--wd', default='.')
    a = ap.parse_args()
    rng = random.Random(a.seed * 1000 + a.r)
    bases = [json.loads(l) for l in open(a.bases)]
    if a.src:
        pre = tuple(a.src.split(','))
        bases = [b for b in bases if b["src"].startswith(pre)]
    if a.limit_bases:
        bases = bases[:a.limit_bases]
    M = 32 if a.control else 33
    R_new = a.r if a.control else a.r + 1
    modes = ('free',) if a.control else tuple(a.modes.split(','))
    blocks, meta, njobs = [], [], 0
    for b in bases:
        for kind, D in deletion_sets(b, a.r, a.kinds.split(','), a.per_kind, rng):
            txt, k = block(b, kind, D, R_new, modes, a.w, a.cap, rng, M)
            blocks.append(txt)
            njobs += k
            meta.append({"id": b["id"], "src": b["src"], "kind": kind, "D": D, "jobs": k})
    os.makedirs(a.out, exist_ok=True)
    json.dump({"args": vars(a), "deletions": meta}, open(os.path.join(a.out, 'deletions.json'), 'w'))
    print(json.dumps({"bases": len(bases), "deletion_sets": len(blocks), "jobs": njobs}), flush=True)
    # longest blocks first, dealt round-robin
    blocks.sort(key=len, reverse=True)
    info = run_pool(os.path.join(a.wd, 'ext_solve'), os.path.join(a.wd, f'n{M}k7.cnf'), M, a.climit, blocks,
                    a.out, a.workers, opts=['lucky=0'])
    info.update({"R": a.r, "M": M, "bases": len(bases), "deletion_sets": len(blocks), "jobs": njobs})
    json.dump(info, open(os.path.join(a.out, 'run.json'), 'w'))
    print(json.dumps(info))


if __name__ == '__main__':
    main()

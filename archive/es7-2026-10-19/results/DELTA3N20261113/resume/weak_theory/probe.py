#!/usr/bin/env python3
"""Bounded exact probe; no imports from any earlier research program."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import time

resource.setrlimit(resource.RLIMIT_AS, (384 * 1024**2,) * 2)
resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
START = time.monotonic()


def det(P, a, b, c):
    x, y = P[a]
    u, v = P[b]
    s, t = P[c]
    return (u-x)*(t-y)-(v-y)*(s-x)


def hull(P, ids):
    lo, hi = [], []
    for chain, seq in ((lo, ids), (hi, reversed(ids))):
        for p in seq:
            while len(chain) >= 2 and det(P, chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
    return lo[:-1]+hi[:-1]


def mask(ids):
    return sum(1 << i for i in ids)


def ids(mask_value):
    return [i for i in range(mask_value.bit_length()) if mask_value >> i & 1]


def family(P, size, cap=False):
    if cap:
        return [mask(C) for C in it.combinations(range(len(P)), size)
                if all(det(P, *t) < 0 for t in it.combinations(C, 3))]
    return [mask(C) for C in it.combinations(range(len(P)), size)
            if len(hull(P, C)) == size]


def run(P, n, tag):
    m = len(P)
    assert m <= 16
    assert all(P[i][0] < P[i+1][0] for i in range(m-1))
    ds = [det(P, *t) for t in it.combinations(range(m), 3)]
    assert all(ds)
    caps, gons = family(P, 4, True), family(P, n-1)
    badcaps, badgons = family(P, 5, True), family(P, n)
    assert not badcaps and not badgons
    result = dict(tag=tag, n=n, m=m, P=P, cap4=len(caps), gons=len(gons),
                  min_abs_det=min(map(abs, ds)), cap5=0, ngon=0, endpoints=[])
    for p in [0, m-1]:
        bit = 1 << p
        oldcaps = [K for K in caps if not K & bit]
        oldgons = [H for H in gons if not H & bit]
        newcaps = [K ^ bit for K in caps if K & bit]
        newgons = [H ^ bit for H in gons if H & bit]
        capfree = bytearray([1]) * (1 << m)
        hitold = bytearray([1]) * (1 << m)
        redgood = bytearray(1 << m)
        for A in range(1 << m):
            if A & bit:
                continue
            capfree[A] = not any(A & K == K for K in oldcaps)
            hitold[A] = all(A & H for H in oldgons)
            redgood[A] = (capfree[A] and hitold[A]
                          and not any(A & K == K for K in newcaps))
        redpossible = bytearray(redgood)
        for q in range(m):
            if q == p:
                continue
            qb = 1 << q
            for A in range(1 << m):
                if A & qb and not A & bit:
                    redpossible[A] |= redpossible[A ^ qb]
        counts = dict(old_deltas=0, already_full=0, add_only=0,
                      deletion_repair=0, monotone_failure=0)
        witness = None
        protected_witness = None
        repair_witness = None
        for A in range(1 << m):
            if A & bit or not capfree[A] or not hitold[A]:
                continue
            counts['old_deltas'] += 1
            if all(A & H for H in newgons):
                counts['already_full'] += 1
            elif redgood[A]:
                counts['add_only'] += 1
            elif redpossible[A]:
                counts['deletion_repair'] += 1
                if repair_witness is None:
                    B = A
                    while not redgood[B]:
                        B = next(B ^ (1 << q) for q in ids(B)
                                 if redpossible[B ^ (1 << q)])
                    repair_witness = dict(A=ids(A), removed=ids(A ^ B),
                                          full_delta=ids(B | bit))
            else:
                counts['monotone_failure'] += 1
                if witness is None:
                    witness = dict(A=ids(A), blockers=[ids(K | bit) for K in newcaps if A & K == K],
                                   supports=[dict(support=ids(A & H), polygon=ids(H)) for H in oldgons],
                                   missed_polygon=ids(next(H | bit for H in newgons if not A & H)))
                if protected_witness is None:
                    private = {next(iter(ids(A & H))): H for H in oldgons if (A & H).bit_count() == 1}
                    K = next((K for K in newcaps if A & K == K and all(q in private for q in ids(K))), None)
                    if K is not None:
                        protected_witness = dict(A=ids(A), cap=ids(K | bit),
                                                 private_polygons={str(q):ids(private[q]) for q in ids(K)},
                                                 missed_polygon=ids(next(H | bit for H in newgons if not A & H)))
        result['endpoints'].append(dict(point=p, counts=counts, first_failure=witness,
                                        protected_cap_failure=protected_witness, repair_witness=repair_witness))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input')
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text())
    P = data.get('P', data.get('points', data.get('coordinates')))
    assert P is not None
    result = run(P, args.n, args.input)
    result['label'] = 'COMPUTED'
    result['source_sha256'] = hashlib.sha256(Path(args.input).read_bytes()).hexdigest()
    result['elapsed_seconds'] = time.monotonic() - START
    Path(args.out).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(output=args.out, seconds=result['elapsed_seconds'],
                          endpoints=[dict(point=e['point'], counts=e['counts'],
                                          protected_cap_failure=e['protected_cap_failure'],
                                          repair_witness=e['repair_witness']) for e in result['endpoints']])))


if __name__ == '__main__':
    main()

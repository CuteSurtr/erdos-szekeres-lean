"""Bounded exact finder for geometric two-support examples; no Delta search."""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
import random
import time


def orient(p, a, b, c):
    return ((p[b][0]-p[a][0])*(p[c][1]-p[a][1])
            - (p[b][1]-p[a][1])*(p[c][0]-p[a][0]))


def profile(p):
    n = len(p)
    turns = {t: orient(p, *t) for t in combinations(range(n), 3)}
    if not all(turns.values()):
        return None
    caps = {t for t, v in turns.items() if v < 0}
    c4 = [c for c in combinations(range(n), 4)
          if all(t in caps for t in combinations(c, 3))]
    # Any five-cap consists of a four-cap and one more point on the right.
    if any(all((a, b, e) in caps for a, b in combinations(c, 2))
           for c in c4 for e in range(c[-1]+1, n)):
        return None
    m = p[-1][0]
    pairs = {t[-2:] for t in caps}
    lines = {}
    for a, b in sorted(pairs):
        slope = Q(p[b][1]-p[a][1], p[b][0]-p[a][0])
        lines[a, b] = (slope, p[b][1]+slope*(m-p[b][0]))
    ambient = {c[-2:]: lines[c[-2:]] for c in c4}
    twos = []
    exposed = []
    singles = []
    for pair, (s, z) in lines.items():
        if any(u >= s and w >= z for u, w in ambient.values()):
            singles.append(pair)
            continue
        lows = [(ab, (w-z)/(s-u)) for ab, (u, w) in ambient.items() if u < s]
        highs = [(ab, (z-w)/(u-s)) for ab, (u, w) in ambient.items() if u > s]
        lo = max(lows, key=lambda it: it[1]) if lows else (None, Q(0))
        hi = min(highs, key=lambda it: it[1]) if highs else (None, None)
        if hi[1] is not None and lo[1] >= hi[1]:
            a, b = lo[0], hi[0]
            assert a is not None and b is not None
            weight = (ambient[b][0]-s)/(ambient[b][0]-ambient[a][0])
            twos.append(dict(pair=pair, triple=next(t for t in sorted(caps) if t[-2:] == pair),
                             support=[a, b], weight=str(weight),
                             lower=str(lo[1]), upper=str(hi[1])))
        else:
            exposed.append(pair)
    return dict(points=p, cap4=c4, lines={str(k): [str(v) for v in vs] for k, vs in ambient.items()},
                two=twos, exposed=exposed, singles=singles,
                orientations=''.join('+' if turns[t] > 0 else '-' for t in sorted(turns)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=20261114)
    ap.add_argument('--count', type=int, default=3000)
    ap.add_argument('--seconds', type=float, default=15)
    ap.add_argument('--n', type=int, default=8)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    assert not args.out.exists()
    rng = random.Random(args.seed)
    start = time.monotonic()
    valid = attempted = 0
    found = None
    for it in range(args.count):
        if time.monotonic()-start >= args.seconds:
            break
        p = [(x, rng.randrange(-30, 31)) for x in range(args.n)]
        attempted += 1
        result = profile(p)
        if result is None:
            continue
        valid += 1
        if result['two']:
            found = result
            break
    output = dict(seed=args.seed, n=args.n, attempted=attempted, valid=valid,
                  elapsed=time.monotonic()-start, found=found,
                  status='FOUND' if found else 'BOUNDED_NO_HIT')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()

"""Exact finite reduction; no imports from previous Delta encoders/checkers."""
from fractions import Fraction as Q
from itertools import combinations


def turn(p, a, b, c):
    ax, ay = p[a]
    bx, by = p[b]
    cx, cy = p[c]
    return (bx-ax)*(cy-ay) - (by-ay)*(cx-ax)


def cap(p, ids):
    return all(turn(p, *t) < 0 for t in combinations(ids, 3))


def convex(p, ids):
    # Every point must be a strict vertex of the monotone-chain hull.
    lo, hi = [], []
    for i in ids:
        while len(lo) > 1 and turn(p, lo[-2], lo[-1], i) <= 0:
            lo.pop()
        lo.append(i)
    for i in reversed(ids):
        while len(hi) > 1 and turn(p, hi[-2], hi[-1], i) <= 0:
            hi.pop()
        hi.append(i)
    return len(lo) + len(hi) - 2 == len(ids)


def line(p, pair, M):
    a, b = pair
    slope = Q(p[b][1]-p[a][1], p[b][0]-p[a][0])
    return slope, Q(p[b][1]) + slope*(M-p[b][0])


def value(l, t):
    return l[0]*t + l[1]


def upper_hull(lines):
    """Entries (line, start) in increasing slope; start None means -infinity."""
    by_slope = {}
    for s, z in lines:
        by_slope[s] = max(z, by_slope.get(s, z))
    hull = []
    for s, z in sorted(by_slope.items()):
        start = None
        while hull:
            (u, w), last_start = hull[-1]
            start = (w-z)/(s-u)
            if last_start is None or start > last_start:
                break
            hull.pop()
        hull.append(((s, z), start if hull else None))
    return hull


def dominates(l, q):
    return l[0] >= q[0] and l[1] >= q[1]


def finite_test(q, hull):
    if not hull:
        return False
    if q[0] > hull[-1][0][0]:
        return False
    checks = [Q(0)] + [t for _, t in hull if t is not None and t > 0]
    return all(value(q, t) <= max(value(l, t) for l, _ in hull) for t in checks)


def convex_certificate(q, lines):
    """Return <=2 lines and rational weights dominating (slope,height at M)."""
    for l in lines:
        if dominates(l, q):
            return [(l, Q(1))]
    # A useful two-line segment must bracket the required slope. At its
    # intersection with that slope the height must be at least q's height.
    for a, b in combinations(lines, 2):
        if a[0] > b[0]:
            a, b = b, a
        if not a[0] < q[0] < b[0]:
            continue
        w = (b[0]-q[0])/(b[0]-a[0])
        if w*a[1] + (1-w)*b[1] >= q[1]:
            return [(a, w), (b, 1-w)]
    return None


def exposure(q, lines):
    """Open interval of t>0 where q exceeds every ambient line, or None."""
    lo, hi = Q(0), None
    for s, z in lines:
        ds, dz = q[0]-s, q[1]-z
        if ds == 0:
            if dz <= 0:
                return None
        elif ds > 0:
            lo = max(lo, -dz/ds)
        else:
            bound = -dz/ds
            hi = bound if hi is None else min(hi, bound)
    if hi is not None and lo >= hi:
        return None
    return lo, hi


def model(p):
    assert p and all(p[i][0] < p[i+1][0] for i in range(len(p)-1))
    assert all(turn(p, *t) != 0 for t in combinations(range(len(p)), 3))
    M = p[-1][0]
    c3 = [t for t in combinations(range(len(p)), 3) if cap(p, t)]
    c4 = [t for t in combinations(range(len(p)), 4) if cap(p, t)]
    pair_caps = {}
    for t in c4:
        pair_caps.setdefault(t[-2:], t)
    ambient = {pair: line(p, pair, M) for pair in pair_caps}
    hull = upper_hull(ambient.values())
    states = {}
    for t in c3:
        pair = t[-2:]
        if pair in states:
            continue
        q = line(p, pair, M)
        safe = finite_test(q, hull)
        interval = exposure(q, list(ambient.values()))
        assert safe == (interval is None)
        cert = convex_certificate(q, list(ambient.values())) if safe else None
        assert not safe or cert is not None
        states[pair] = dict(line=q, safe=safe, interval=interval, certificate=cert)
    return dict(M=M, caps3=c3, caps4=c4, ambient=ambient,
                pair_caps=pair_caps, hull=hull, states=states,
                bad=[t for t in c3 if not states[t[-2:]]["safe"]])


def serial(obj):
    if isinstance(obj, Q):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): serial(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [serial(v) for v in obj]
    return obj

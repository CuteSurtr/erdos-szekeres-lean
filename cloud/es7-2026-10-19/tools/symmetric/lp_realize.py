#!/usr/bin/env python3
"""Realizer for rotationally symmetric chirotopes by orbit insertion with exact 2-D feasibility.

Points: orbit o has representative q_o, points (o,r) = R^r q_o (R = rotation by 2 pi/m about the
origin), optional centre at the origin.  Orbit 0 is fixed at q_0 = (1,0) (rotation and scale are
free).  Orbits are inserted one at a time.  For the new representative q:
  * every required orientation of a triple with exactly ONE new point is a half-plane in q:
        orient(a, b, R^r q) = s   <=>   orient(R^-r a, R^-r b, q) = s   (linear in q)
    -> the intersection is a convex polygon (half-plane clipping);
  * a triple with TWO new points, orient(a, R^r q, R^s q), is quadratic in q, but in polar form
    q = rho*(cos th, sin th) its sign is sign(rho*alpha(th) - beta(th)), linear in rho; triples
    with three new points or with the centre and two new points have constant sign.
  Hence for every direction th the feasible set of rho is an interval, computed exactly from the
  polygon edges and the quadratic constraints ("polar sweep" over a grid of directions).
Search: depth-first insertion with backtracking (node budget); candidates are drawn from the
feasible (th, rho) set, ordered by the feasible measure of the NEXT orbit (one-step lookahead);
the sweep covers only the angular extent of the polygon (adaptive resolution); restarts use
random insertion orders.
A floating-point realization is rounded to integers at increasing scales and ALL triple
orientations are re-checked exactly in integer arithmetic before success is reported.

usage: lp_realize.py map.json file.sig out.pts [restarts] [nodes] [candidates] [seed] [theta_grid]
file.sig: lines "a b c s" with 0-based a<b<c over all P points (centre last if present).
"""
import json
import math
import random
import sys

BOX = 60.0
INF = float("inf")


def clip(poly, a, b, c, eps=1e-12):
    """keep the part of convex polygon poly with a*x + b*y + c >= 0"""
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        fp = a * P[0] + b * P[1] + c
        fq = a * Q[0] + b * Q[1] + c
        if fp >= -eps:
            out.append(P)
        if (fp < -eps) != (fq < -eps):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


class Realizer:
    def __init__(self, info, sig, rng, ngrid=720):
        self.m = info["m"]
        self.t = info["t"]
        self.P = info["P"]
        self.c = info["center_index"]
        self.sig = sig
        self.rng = rng
        self.ngrid = ngrid
        m = self.m
        self.cs = [(math.cos(2 * math.pi * r / m), math.sin(2 * math.pi * r / m)) for r in range(m)]
        self.set_order(list(range(self.t)))

    def set_order(self, order):
        """order[level] = orbit inserted at that level (order[0] = 0 is fixed at (1,0))"""
        self.order = order
        rank = {o: i for i, o in enumerate(order)}
        m = self.m
        self.lin = [[] for _ in range(self.t)]    # (a,b,c, new, r, s): one point of the new orbit
        self.quad = [[] for _ in range(self.t)]   # (a,b,c, s): >= 2 points of the new orbit
        for (a, b, c), s in self.sig.items():
            lv = [rank[x // m] if x != self.c else -1 for x in (a, b, c)]
            L = max(lv)
            if lv.count(L) == 1:
                new = (a, b, c)[lv.index(L)]
                self.lin[L].append((a, b, c, new, new % m, s))
            else:
                self.quad[L].append((a, b, c, s))

    def rot(self, p, r):
        cr, sr = self.cs[r % self.m]
        return (cr * p[0] - sr * p[1], sr * p[0] + cr * p[1])

    def point(self, i, reps):
        if i == self.c:
            return (0.0, 0.0)
        o, r = divmod(i, self.m)
        return self.rot(reps[o], r)

    # ---- linear part
    def halfplanes(self, o, reps):
        hp = []
        for a, b, c, new, r, s in self.lin[o]:
            pts = [None if i == new else self.point(i, reps) for i in (a, b, c)]
            idx = pts.index(None)
            X, Y = [p for p in pts if p is not None]
            # orient(X,Y,Z) = al*Zx + be*Zy + ga ; positions: idx 2 -> (X,Y,Z), idx 0 -> (Z,X,Y) same, idx 1 -> (X,Z,Y) negated
            al, be = -(Y[1] - X[1]), (Y[0] - X[0])
            ga = -(al * X[0] + be * X[1])
            if idx == 1:
                al, be, ga = -al, -be, -ga
            cr, sr = self.cs[r]
            A, B, C = al * cr + be * sr, -al * sr + be * cr, ga
            if s < 0:
                A, B, C = -A, -B, -C
            hp.append((A, B, C))
        return hp

    def feasible_polygon(self, o, reps):
        poly = [(-BOX, -BOX), (BOX, -BOX), (BOX, BOX), (-BOX, BOX)]
        for A, B, C in self.halfplanes(o, reps):
            poly = clip(poly, A, B, C - 1e-9 * math.hypot(A, B))
            if len(poly) < 3:
                return None
        return poly

    @staticmethod
    def poly_edges(poly):
        """half-planes (A,B,C) of a ccw/cw convex polygon with the interior on the >= 0 side"""
        n = len(poly)
        # orientation of polygon
        area2 = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
        sgn = 1 if area2 > 0 else -1
        edges = []
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            A, B = -(y2 - y1), (x2 - x1)        # left normal
            C = -(A * x1 + B * y1)
            edges.append((sgn * A, sgn * B, sgn * C))
        return edges

    # ---- quadratic part in polar form
    def quad_linear(self, o, reps, d):
        """for direction d: list of (alpha, beta, s): need sign(rho*alpha - beta) = s"""
        out = []
        m = self.m
        orb = self.order[o]
        for a, b, c, s in self.quad[o]:
            trip = (a, b, c)
            new = [i for i in trip if i != self.c and i // m == orb]
            if len(new) == 3:
                u, v, w = (self.rot(d, i % m) for i in trip)
                val = orient(u, v, w)          # times rho^2 > 0
                out.append((0.0, -val, s))
                continue
            kn = [i for i in trip if i not in new][0]
            a_pt = self.point(kn, reps)
            idx = trip.index(kn)
            u = self.rot(d, new[0] % m)
            v = self.rot(d, new[1] % m)
            # orient(a,u,v) scaled: rho^2 det(u,v) - rho (det(u,a) + det(a,v)) ; sign = sign(rho*alpha - beta)
            alpha = det(u, v)
            beta = det(u, a_pt) + det(a_pt, v)
            # position of the known point: idx 0 -> orient(a,u,v); idx 2 -> orient(u,v,a) = orient(a,u,v); idx 1 -> orient(u,a,v) = -orient(a,u,v)
            if idx == 1:
                alpha, beta = -alpha, -beta
            out.append((alpha, beta, s))
        return out

    def rho_interval(self, edges, quads):
        lo, hi = 1e-6, INF
        for A, B, C, k in edges:      # rho*k + C >= 0
            if k > 1e-15:
                lo = max(lo, -C / k)
            elif k < -1e-15:
                hi = min(hi, -C / k)
            elif C < 0:
                return None
            if lo >= hi:
                return None
        for alpha, beta, s in quads:  # sign(rho*alpha - beta) = s
            if abs(alpha) < 1e-15:
                if (-beta > 0) != (s > 0) or beta == 0:
                    return None
                continue
            thr = beta / alpha
            if (alpha > 0) == (s > 0):
                lo = max(lo, thr)
            else:
                hi = min(hi, thr)
            if lo >= hi:
                return None
        return (lo, hi)

    def sweep(self, o, reps, poly):
        """feasible (theta, rho_lo, rho_hi) over a jittered grid of directions; returns list and measure"""
        edges = self.poly_edges(poly)
        res = []
        measure = 0.0
        off = self.rng.random()
        n = self.ngrid
        # angular extent of the polygon seen from the origin
        inside0 = all(A * 0 + B * 0 + C >= 0 for A, B, C in edges)
        if inside0:
            th0, span = 0.0, 2 * math.pi
        else:
            angs = sorted(math.atan2(y, x) for x, y in poly)
            gaps = [(angs[(i + 1) % len(angs)] - angs[i]) % (2 * math.pi) for i in range(len(angs))]
            i = max(range(len(angs)), key=lambda j: gaps[j])
            th0 = angs[(i + 1) % len(angs)]
            span = 2 * math.pi - gaps[i]
        for g in range(n):
            th = th0 + span * (g + off) / n
            d = (math.cos(th), math.sin(th))
            e = [(A, B, C, A * d[0] + B * d[1]) for A, B, C in edges]
            iv = self.rho_interval(e, self.quad_linear(o, reps, d))
            if iv is None:
                continue
            lo, hi = iv
            if hi == INF:
                hi = BOX
            if hi - lo <= 1e-9:
                continue
            res.append((th, lo, hi))
            measure += (hi - lo) * (hi + lo) / 2     # ~ area element
        return res, measure

    def candidates(self, feas, k):
        if not feas:
            return []
        # weight by interval width, pick k distinct directions
        w = [(hi - lo) for _, lo, hi in feas]
        picks = set()
        tries = 0
        while len(picks) < min(k, len(feas)) and tries < 20 * k:
            tries += 1
            picks.add(self.rng.choices(range(len(feas)), weights=w)[0])
        out = []
        for i in picks:
            th, lo, hi = feas[i]
            lam = 0.25 + 0.5 * self.rng.random()           # interior of the interval
            rho = lo + lam * (hi - lo)
            out.append((rho * math.cos(th), rho * math.sin(th)))
        return out

    def quad_ok(self, level, reps):
        for a, b, c, s in self.quad[level]:
            d = orient(self.point(a, reps), self.point(b, reps), self.point(c, reps))
            if d == 0 or (d > 0) != (s > 0):
                return False
        return True

    def level_feasible(self, o, reps):
        poly = self.feasible_polygon(o, reps)
        if poly is None:
            return None, 0.0
        return self.sweep(o, reps, poly)

    def search(self, nodes, ncand, order=None):
        """DFS with backtracking over orbit insertion levels; candidates ordered by the feasible
        measure of the next level (one-step lookahead); `nodes` bounds the polygon computations."""
        if order is None:
            order = list(range(self.t))
        self.set_order(order)
        reps = [None] * self.t
        reps[0] = (1.0, 0.0)
        if not self.quad_ok(0, reps):
            return None, 0
        self.best_depth = 1
        self.nodes = 0

        def dfs(level, feas):
            if level == self.t:
                return True
            orb = self.order[level]
            scored = []
            for q in self.candidates(feas, ncand):
                reps[orb] = q
                if not self.quad_ok(level, reps):
                    continue
                if level + 1 < self.t:
                    nf, meas = self.level_feasible(level + 1, reps)
                    self.nodes += 1
                    if not nf:
                        continue
                    scored.append((meas, q, nf))
                else:
                    scored.append((1.0, q, None))
            reps[orb] = None
            scored.sort(key=lambda z: -z[0])
            for meas, q, nf in scored:
                reps[orb] = q
                self.best_depth = max(self.best_depth, level + 1)
                if dfs(level + 1, nf):
                    return True
                if self.nodes >= nodes:
                    break
            reps[orb] = None
            return False

        feas, _ = self.level_feasible(1, reps)
        self.nodes += 1
        if not feas:
            return None, 1
        ok = dfs(1, feas)
        return (reps if ok else None), self.best_depth

    def exact_points(self, reps):
        pts = [self.point(i, reps) for i in range(self.P)]
        for sc in range(20, 60, 2):
            S = 2.0 ** sc
            ip = [(round(x * S), round(y * S)) for x, y in pts]
            good = True
            for (a, b, c), s in self.sig.items():
                d = orient(ip[a], ip[b], ip[c])
                if d == 0 or (d > 0) != (s > 0):
                    good = False
                    break
            if good:
                return ip
        return None


def main():
    mp, sigf, out = sys.argv[1], sys.argv[2], sys.argv[3]
    restarts = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    nodes = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
    cands = int(sys.argv[6]) if len(sys.argv) > 6 else 12
    seed = int(sys.argv[7]) if len(sys.argv) > 7 else 1
    ngrid = int(sys.argv[8]) if len(sys.argv) > 8 else 240
    info = json.load(open(mp))
    sig = {}
    for line in open(sigf):
        a, b, c, s = map(int, line.split())
        sig[(a, b, c)] = s
    rng = random.Random(seed)
    R = Realizer(info, sig, rng, ngrid)
    bestd = 0
    for rs in range(restarts):
        order = list(range(info["t"]))
        if rs > 0:
            tail = order[1:]
            rng.shuffle(tail)
            order = [0] + tail
        reps, depth = R.search(nodes, cands, order)
        bestd = max(bestd, depth)
        if reps is not None:
            ip = R.exact_points(reps)
            if ip is None:
                print(f"restart {rs}: float realization found but integer rounding failed", flush=True)
                continue
            with open(out, "w") as f:
                for x, y in ip:
                    f.write(f"{x} {y}\n")
            print(f"REALIZED restart={rs}; exact integer check passed (all {len(sig)} triples)")
            return 0
    print(f"NOT REALIZED: deepest level reached {bestd} of {info['t']} (restarts={restarts}, nodes={nodes}, candidates={cands}, grid={ngrid})")
    return 1


if __name__ == "__main__":
    sys.exit(main())

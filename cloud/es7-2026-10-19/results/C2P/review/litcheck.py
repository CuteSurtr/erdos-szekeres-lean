#!/usr/bin/env python3
"""Literal-level check of the relabelling maps on the actual cube files (no geometry, no solver).

Model: in the angular normal form the 2t points sit at angular positions 0..2t-1 around c (counter-clockwise):
(i,0) at position i, (i,1) at position i+t. Reflecting the configuration sends position p to -p (mod 2t) and negates
every orientation chi(x,y,z) of three points (and of triples containing c). Restarting the normal form at the point
at position f gives the point at position p the new label (j, r) with d = (p - f) mod 2t, j = d mod t, r = d // t.

Maps checked (a = hull class of case P_a):
  pi_a  : reflect, restart at the image of (a,1) [and of (a,0)]   claim (B): (P_a, V) -> (P_a, {(a - i) mod t})
  rho_a : no reflection, restart at (a,0) [and (a,1)]             claim (A): P_a -> P_{t-a}, V -> {(i - a) mod t}
  mu    : reflect, restart at the image of (0,0)                  P_a -> P_{t-a}, V -> {(-i) mod t}
For each map: the image of every literal of every cube is computed from EVERY triple of that literal's variable class
(well-definedness), and the image literal set of cube (P_a, V) is compared with the file's cube of the predicted case.
Also: SB units and hull-SB clauses defined from the docstring are compared with the CNF tail, and the SB unit set is
checked to be invariant under each map.
usage: litcheck.py MAP.json HULLCUBES.txt L2DIR(with P<a>_cubes.txt) [CNF_TAIL_FILE nsb nhull] [amin amax]"""
import itertools, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from geom import Map, load_cubes

mp = Map(sys.argv[1])
t, N, Z = mp.t, mp.N, mp.Z
hull = load_cubes(sys.argv[2])
L2DIR = sys.argv[3]
tail = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "-" else None
amin = int(sys.argv[7]) if len(sys.argv) > 7 else 1
amax = int(sys.argv[8]) if len(sys.argv) > 8 else t - 1

# variable -> all (triple, sign) with chi(triple) = sign * X_v
cls = {}
for a, b, c, v, s in mp.triples:
    cls.setdefault(v, []).append(((a, b, c), s))


def pos(i):
    if i == Z:
        return None
    o, r = divmod(i, 2)
    return o + r * t


def label(d):
    d %= 2 * t
    return 2 * (d % t) + d // t


def make_map(reflect, f):
    def m(i):
        if i == Z:
            return Z
        p = pos(i)
        p2 = (-p) % (2 * t) if reflect else p
        return label(p2 - f)
    return m, (-1 if reflect else 1)


def image_lit(l, m, flip):
    """image literal of literal l: X_v true <=> chi(T) = s for every (T, s) in the class; after the map,
    chi'(m T) = flip * chi(T)."""
    v = abs(l)
    outs = set()
    for (T, s) in cls[v]:
        # literal l says chi(T) = s * sign(l)
        want = s * (1 if l > 0 else -1)
        a, b, c = (m(x) for x in T)
        nl = mp.lit(a, b, c)
        assert nl != 0, (T, (a, b, c))
        outs.add(nl * want * flip)
    assert len(outs) == 1, f"map not well defined on class {v}: {outs}"
    return outs.pop()


def my_hull_cube(a):
    pt = lambda o, r: 2 * o + r
    poly = [pt(0, 0), pt(a, 0), pt(0, 1), pt(a, 1)]
    s = set()
    for k in range(4):
        u, w = poly[k], poly[(k + 1) % 4]
        for q in range(N):
            if q not in (u, w):
                s.add(mp.lit(u, w, q))
    return s


def my_l2_cube(a, V):
    pt = lambda o, r: 2 * o + r
    s = my_hull_cube(a)
    inner = [pt(o, r) for o in range(1, t) if o != a for r in (0, 1)]
    poly = [pt(o, 0) for o in V] + [pt(o, 1) for o in V]
    for k in range(len(poly)):
        u, w = poly[k], poly[(k + 1) % len(poly)]
        for x in inner:
            if x not in (u, w):
                s.add(mp.lit(u, w, x))
    return s


name = lambda a, V: f"P{a}_" + "-".join(map(str, sorted(V)))
fails = []
stats = dict(hull_cubes=0, l2_cubes=0, pi_checked=0, rho_checked=0, mu_checked=0, fixed=0)

# SB units by definition (m = 2)
sb = set()
for o in range(1, t):
    sb.add(mp.lit(Z, 0, 2 * o))
for o, o2 in itertools.combinations(range(1, t), 2):
    sb.add(mp.lit(Z, 2 * o, 2 * o2))
if tail:
    nsb, nh = int(sys.argv[5]), int(sys.argv[6])
    lines = [l.split() for l in open(tail) if l.strip() and not l.startswith(("c", "p"))]
    lines = lines[-(nsb + nh):]
    units = [int(l[0]) for l in lines[:nsb]]
    assert all(len(l) == 2 and l[1] == "0" for l in lines[:nsb])
    if set(units) != sb:
        fails.append("SB units in the CNF differ from the definition")
    hs = set()
    q = 0
    for a, b, d in itertools.combinations(range(1, N), 3):
        for s in (1, -1):
            cl = [-s * mp.lit(a, b, q), -s * mp.lit(b, d, q), -s * mp.lit(d, a, q)]
            if any(-l in cl for l in cl):
                continue
            hs.add(tuple(sorted(set(cl), key=abs)))
    filehs = {tuple(int(x) for x in l[:-1]) for l in lines[nsb:]}
    if filehs != hs or len(lines[nsb:]) != nh:
        fails.append(f"hull-SB clauses differ: file {len(filehs)} def {len(hs)}")
    print(f"CNF tail: {len(units)} SB units, {len(filehs)} hull-SB clauses; match definition: "
          f"{set(units) == sb and filehs == hs}")

for a in range(1, t):
    hc = set(hull[f"P{a}"])
    stats["hull_cubes"] += 1
    if hc != my_hull_cube(a):
        fails.append(f"hull cube P{a} differs from definition")

l2 = {}
for a in range(amin, amax + 1):
    l2[a] = load_cubes(f"{L2DIR}/P{a}_cubes.txt")
    exp = sum(1 for h in (2, 3) for _ in itertools.combinations([o for o in range(1, t) if o != a], h))
    if len(l2[a]) != exp:
        fails.append(f"P{a}: {len(l2[a])} cubes, expected {exp}")
    for nm, lits in l2[a].items():
        V = [int(x) for x in nm.split("_")[1].split("-")]
        stats["l2_cubes"] += 1
        if set(lits) != my_l2_cube(a, V):
            fails.append(f"{nm} differs from definition")
        if not set(hull[f"P{a}"]) <= set(lits):
            fails.append(f"{nm} lacks hull literals")

for a in range(amin, amax + 1):
    hc = set(hull[f"P{a}"])
    # pi_a: reflect, restart at image of (a,1): position of (a,1) is a+t, reflected -(a+t) = t-a (mod 2t)
    for f in ((t - a) % (2 * t), (-a) % (2 * t)):
        m, flip = make_map(True, f)
        assert m(2 * a + 1) in (0, 1) and m(2 * a) in (0, 1)
        img_sb = {image_lit(l, m, flip) for l in sb}
        if img_sb != sb:
            fails.append(f"pi_{a} (f={f}) does not preserve the SB units")
        img_h = {image_lit(l, m, flip) for l in hc}
        if img_h != hc:
            fails.append(f"pi_{a} (f={f}) maps hull cube P{a} elsewhere")
        for nm, lits in l2[a].items():
            V = [int(x) for x in nm.split("_")[1].split("-")]
            V2 = sorted((a - i) % t for i in V)
            img = {image_lit(l, m, flip) for l in lits}
            tgt = name(a, V2)
            stats["pi_checked"] += 1
            if tgt not in l2[a] or img != set(l2[a][tgt]):
                # find where it went
                where = [n2 for n2, l2s in l2[a].items() if set(l2s) == img]
                fails.append(f"pi_{a}: {nm} -> predicted {tgt}, image equals {where}")
            if f == (t - a) % (2 * t) and tgt == nm:
                stats["fixed"] += 1
            # class-level: the induced class map is i -> (a - i) mod t
            for i in range(t):
                j = m(2 * i) // 2
                if j != (a - i) % t:
                    fails.append(f"pi_{a}: class {i} -> {j}")
                    break
    # rho_a: no reflection, restart at (a,0) [position a] or (a,1) [position a+t]
    for f in (a, a + t):
        m, flip = make_map(False, f)
        if {image_lit(l, m, flip) for l in sb} != sb:
            fails.append(f"rho_{a} does not preserve SB units")
        b = t - a
        if {image_lit(l, m, flip) for l in hc} != set(hull[f"P{b}"]):
            fails.append(f"rho_{a}: hull cube P{a} does not map to P{b}")
        if b in l2:
            for nm, lits in l2[a].items():
                V = [int(x) for x in nm.split("_")[1].split("-")]
                tgt = name(b, [(i - a) % t for i in V])
                stats["rho_checked"] += 1
                if tgt not in l2[b] or {image_lit(l, m, flip) for l in lits} != set(l2[b][tgt]):
                    fails.append(f"rho_{a}: {nm} -/-> {tgt}")
    # mu: reflect, restart at image of (0,0) [position 0] or (0,1) [position t]
    for f in (0, t):
        m, flip = make_map(True, f)
        if {image_lit(l, m, flip) for l in sb} != sb:
            fails.append(f"mu does not preserve SB units")
        b = t - a
        if {image_lit(l, m, flip) for l in hc} != set(hull[f"P{b}"]):
            fails.append(f"mu: hull cube P{a} does not map to P{b}")
        if b in l2:
            for nm, lits in l2[a].items():
                V = [int(x) for x in nm.split("_")[1].split("-")]
                tgt = name(b, [(-i) % t for i in V])
                stats["mu_checked"] += 1
                if tgt not in l2[b] or {image_lit(l, m, flip) for l in lits} != set(l2[b][tgt]):
                    fails.append(f"mu: {nm} -/-> {tgt}")

print("stats", stats)
print("FAILURES", len(fails))
for x in fails[:40]:
    print("  ", x)

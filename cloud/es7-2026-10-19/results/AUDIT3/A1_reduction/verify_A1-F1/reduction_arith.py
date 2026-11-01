#!/usr/bin/env python3
"""Independent size bookkeeping for the assembled theorem of finding A1-F1.

Hypotheses (case theorems), as sub-configurations they need:
  C2-34 : 17 antipodal pairs, centre not in the set                (34 points)
  C3-33 : 11 orbits of a rotation of order 3, centre not in the set (33 points)
  C5>=35: a set of >= 35 points with a rotation of order 5          (applied to S itself)
  M34   : 17 mirror pairs, no point on the axis                     (34 points)
  M33   : 16 mirror pairs and exactly one point on the axis         (33 points)
  REG   : elementary lemma: an orbit of a rotation of order p >= 7 is a regular p-gon, so a convex 7-gon.
  (C4-32: 8 orbits of a rotation of order 4 -- the fourfold result; checked here to be redundant given C2-34.)

Witnesses a symmetric set S (|S| = n >= 33, general position, spanning the plane) can have:
  rot(p, e): a rotation of prime order p; e = 1 iff the centre is in S (e = 1 impossible for p = 2, because the
             centre would be collinear with x and -x).  n = p*k + e with k >= 1 non-central orbits of size p.
  ref(b):    a reflection with b points on the axis (b <= 2 by general position), n = 2*k + b.
Every nontrivial finite symmetry group contains such a witness (cyclic C_m: rho^(m/p); dihedral: a reflection);
checked for m <= 400 below.

The script checks, for n = 33..NMAX and all primes p <= PMAX, that every arithmetically possible witness
yields one of the needed sub-configurations, and it reports which hypothesis each case uses.
"""
import sys
from collections import Counter

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
PMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 400


def primes_upto(m):
    s = [True] * (m + 1)
    s[0] = s[1] = False
    for i in range(2, int(m ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, m + 1, i):
                s[j] = False
    return [i for i in range(m + 1) if s[i]]


P = primes_upto(PMAX)


def cover_rot(n, p, e, use_c2=True, use_c4=False):
    """Return the hypothesis used for witness rot(p,e) at size n, or None if not covered; 'IMPOSSIBLE' if no such set."""
    if p == 2 and e == 1:
        return "IMPOSSIBLE"
    if (n - e) % p != 0 or (n - e) // p < 1:
        return "IMPOSSIBLE"
    k = (n - e) // p
    if p == 2:
        if use_c2:
            return "C2-34" if k >= 17 else None
        return None
    if p == 3:
        return "C3-33" if k >= 11 else None
    if p == 5:
        return "C5>=35" if n >= 35 else None
    if p >= 7:
        return "REG" if k >= 1 else None
    raise AssertionError


def cover_ref(n, b):
    if (n - b) % 2 != 0:
        return "IMPOSSIBLE"
    k = (n - b) // 2
    if b == 0:
        return "M34" if k >= 17 else None
    return "M33" if k >= 16 else None


bad = []
used = Counter()
possible = Counter()
for n in range(33, NMAX + 1):
    for p in P:
        for e in (0, 1):
            r = cover_rot(n, p, e)
            if r == "IMPOSSIBLE":
                continue
            possible[("rot", p if p <= 7 else ">=7", e)] += 1
            if r is None:
                bad.append((n, "rot", p, e))
            else:
                used[r] += 1
    for b in (0, 1, 2):
        r = cover_ref(n, b)
        if r == "IMPOSSIBLE":
            continue
        possible[("ref", b)] += 1
        if r is None:
            bad.append((n, "ref", b))
        else:
            used[r] += 1

print(f"sizes 33..{NMAX}, primes <= {PMAX}")
print("uncovered witnesses:", len(bad), bad[:10])
print("hypothesis usage:", dict(used))

# The finding's one line: a half-turn set of n >= 33 points has an even size >= 34 and >= 17 antipodal pairs.
one_line = all(cover_rot(n, 2, 0) in ("C2-34", "IMPOSSIBLE") and cover_rot(n, 2, 1) == "IMPOSSIBLE"
               for n in range(33, NMAX + 1))
print("half-turn line holds (n even => n >= 34 => 17 pairs; centre never in S):", one_line)
print("smallest possible half-turn size >= 33:", min(n for n in range(33, NMAX + 1) if cover_rot(n, 2, 0) != "IMPOSSIBLE"))

# C5: sizes 33 and 34 impossible
print("fivefold sizes 33, 34 possible?:", [(n, e) for n in (33, 34) for e in (0, 1) if cover_rot(n, 5, e) != "IMPOSSIBLE"])

# Without C2-34: which witnesses are left?  (shows C2-34 is what closes the half-turn case)
left = Counter()
for n in range(33, NMAX + 1):
    if cover_rot(n, 2, 0) != "IMPOSSIBLE" and cover_rot(n, 2, 0, use_c2=False) is None:
        left["rot2"] += 1
print("witnesses left without C2-34 (only half-turns):", dict(left))

# C4 (order 4) redundant given C2-34: a rotation of order 4 squares to the half-turn, so every C4 set is a C2 set.
c4_ok = True
for n in range(33, NMAX + 1):
    if n % 4 == 0:  # C4 sets: centre excluded (contains the half-turn), n = 4k
        if cover_rot(n, 2, 0) != "C2-34":
            c4_ok = False
print("every fourfold size n >= 33 (n = 4k) is covered by C2-34 through the half-turn:", c4_ok)

# Every nontrivial finite subgroup of O(2) contains a reflection or a rotation of prime order.
grp_ok = True
for m in range(2, 401):
    ps = [p for p in primes_upto(m) if m % p == 0]
    if not ps:
        grp_ok = False
    # rho has order m; rho^(m/p) has order p exactly: order of rho^j is m/gcd(m,j)
    from math import gcd
    for p in ps:
        j = m // p
        if m // gcd(m, j) != p:
            grp_ok = False
print("cyclic C_m (2 <= m <= 400) always has an element of prime order:", grp_ok)

# 33-point statement alone: which hypotheses are needed at n = 33?
u33 = Counter()
for p in P:
    for e in (0, 1):
        r = cover_rot(33, p, e)
        if r not in ("IMPOSSIBLE", None):
            u33[r] += 1
for b in (0, 1, 2):
    r = cover_ref(33, b)
    if r not in ("IMPOSSIBLE", None):
        u33[r] += 1
print("hypotheses used at exactly n = 33:", dict(u33))

ok = (not bad) and one_line and c4_ok and grp_ok
print("ALL CHECKS PASS" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)

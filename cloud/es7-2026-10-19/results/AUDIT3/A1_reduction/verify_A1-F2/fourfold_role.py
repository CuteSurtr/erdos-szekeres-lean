#!/usr/bin/env python3
"""Where is the fourfold 32-point exclusion (C4-32) actually used?

Abstract case theorems (each "a set of this kind contains a convex 7-gon"):
  REG    rotation of order s >= 7, set != {centre}: a non-central orbit is a regular s-gon.
  C3_33  threefold, 33 points (necessarily no centre).
  C5_35  fivefold, >= 35 points.
  C2_34  half-turn symmetric, 34 points (centre never in the set).
  C4_32  fourfold, 32 points (centre never in the set).
Deleting whole orbits keeps general position and the symmetry, so a theorem for size n0 applies to every
larger size of the same symmetry that can be trimmed to exactly n0 by deleting whole orbits (and the centre).

Possible sizes (general position): for a rotation of order s, the centre is the only fixed point;
s even => the centre is not in the set and s | n; s odd => n = 0 or 1 mod s.

For every rotation order s in [2, SMAX] and size n in [NMIN, NMAX], decide which case theorems exclude a
set with a rotation of order s, under different hypothesis sets. Report where C4_32 is indispensable."""
import sys

SMAX, NMAX = 60, 600


def possible(n, s):
    if s % 2 == 0:
        return n % s == 0
    return n % s in (0, 1)


def trims_to(n, s, n0):
    """Can a C_s set of size n be trimmed to a C_s set of size exactly n0 by deleting whole orbits/centre?"""
    if n0 > n or not possible(n0, s):
        return False
    # orbits have size s; centre (if present) has size 1 and only for odd s
    if s % 2 == 0:
        return (n - n0) % s == 0
    # odd s: n = q*s + e, n0 = q0*s + e0, e,e0 in {0,1}; can drop the centre (e -> 0) but not add it
    e, e0 = n % s, n0 % s
    return e0 <= e and n0 <= n


def primes(s):
    out, p, t = [], 2, s
    while p * p <= t:
        while t % p == 0:
            out.append(p); t //= p
        p += 1
    if t > 1:
        out.append(t)
    return sorted(set(out))


def excluded(n, s, thms):
    """Return the list of theorems that exclude a C_s set of size n (using any subgroup C_d, d | s)."""
    hits = []
    for d in range(2, s + 1):
        if s % d:
            continue
        # a C_s set is C_d symmetric; its size n is possible for C_d automatically
        if 'REG' in thms and d >= 7 and n > 1:
            hits.append(('REG', d))
        if 'C3_33' in thms and d == 3 and trims_to(n, 3, 33):
            hits.append(('C3_33', d))
        if 'C5_35' in thms and d == 5 and n >= 35 and possible(n, 5):
            hits.append(('C5_35', d))
        if 'C2_34' in thms and d == 2 and n >= 34 and n % 2 == 0:
            hits.append(('C2_34', d))
        if 'C4_32' in thms and d == 4 and n >= 32 and n % 4 == 0:
            hits.append(('C4_32', d))
    return hits


def run(label, thms, nmin, nmax, verbose_limit=12):
    bad, c4only = [], []
    for s in range(2, SMAX + 1):
        for n in range(nmin, nmax + 1):
            if not possible(n, s):
                continue
            h = excluded(n, s, thms)
            if not h:
                bad.append((s, n))
            elif all(t == 'C4_32' for t, _ in h):
                c4only.append((s, n))
    print(f"[{label}] thms={sorted(thms)} n in [{nmin},{nmax}] s in [2,{SMAX}]")
    print(f"   not excluded: {len(bad)} pairs; first: {bad[:verbose_limit]}")
    print(f"   excluded ONLY via C4_32: {len(c4only)} pairs; first: {c4only[:verbose_limit]}")
    return bad, c4only


ALL = {'REG', 'C3_33', 'C5_35', 'C2_34', 'C4_32'}
print("== 1. The >= 33 claim (assembled theorem, rotations only; mirrors are handled by M33/M34) ==")
b, c = run("all five", ALL, 33, NMAX)
assert not b
b, c = run("without C4_32", ALL - {'C4_32'}, 33, NMAX)
assert not b, "C4_32 needed for >= 33?"
print("   => with C2_34, C4_32 is redundant for every n >= 33.")
print()
print("== 2. Corollary 3 as written (C2_34 NOT assumed): which orders survive? ==")
b, c = run("without C2_34", ALL - {'C2_34'}, 33, NMAX)
assert {s for s, _ in b} == {2}, b[:5]
b2, c2 = run("without C2_34 and C4_32", ALL - {'C2_34', 'C4_32'}, 33, NMAX)
surv = sorted({s for s, _ in b2})
print("   surviving orders without C2_34 and C4_32:", surv)
assert surv == [2, 4]
print("   => without C2_34, C4_32 is exactly what removes order 4 ('group exactly C2' in Cor. 3).")
print("      orders 4 surviving sizes (first):", [n for s, n in b2 if s == 4][:6])
print()
print("== 3. N(C4) = 28 ==")
sizes = [n for n in range(1, 200) if possible(n, 4)]
need = []
for n in sizes:
    if n <= 28:
        continue
    h_with = excluded(n, 4, ALL)
    h_wo = excluded(n, 4, ALL - {'C4_32'})
    if not h_wo:
        need.append(n)
print("   fourfold sizes above 28 not excluded without C4_32 (n<200):", need)
assert need == [32]
print("   => C4_32 is indispensable for N(C4)=28 only at n = 32 (n >= 36 also follows from C2_34).")
print()
print("== 4. 32-point sets: largest rotation order (SYM2/README claim) ==")
orders32 = [s for s in range(2, 33) if possible(32, s)]
print("   orders possible for n=32:", orders32)
for s in orders32:
    print(f"   s={s}: excluded by {excluded(32, s, ALL) or 'nothing'}")
print("   => 'order 2 is the largest for 32-point 7-gon-free sets' needs C4_32 (s=4); s=8,16,32 by REG.")

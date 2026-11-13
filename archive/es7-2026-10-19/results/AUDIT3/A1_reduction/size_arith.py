#!/usr/bin/env python3
"""A1 audit: exhaustive check of the size arithmetic of the symmetric-ES(7) reduction (Corollary 3) and of the
"largest size without a convex 7-gon" table, for every size n up to NMAX and every rotation order s up to SMAX.

Model (the geometric facts behind it are audited by hand in the report, not here):
  * rotation of order s about c: the non-centre points form orbits of exactly s points; the centre c may be a point
    of S only when s is odd (for even s, c is collinear with every antipodal pair p, -p).  So n = s*k + e, e in {0,1},
    e = 0 forced when s is even.  The group C_s contains C_d for every d | s, and a C_s-orbit splits into s/d C_d-orbits.
  * reflection: n = 2k + b, b = number of axis points, b in {0,1,2} (at most 2 collinear points).
Deletion of whole orbits (and of the centre / of axis points) keeps the symmetry and general position.

Case theorems, with hypotheses exactly as stated in the case READMEs:
  T_C3  : C3-invariant, exactly 33 points (necessarily 11 orbits, no centre)         [C3FINAL]
  T_C5  : C5-invariant, at least 35 points (centre allowed)                           [SYM5]
  T_C4  : C4-invariant, exactly 32 points (8 orbits)                                  [C4CUT]
  T_C2  : C2-invariant (half-turn), exactly 34 points (17 pairs)                      [C2FINAL, pending]
  T_M33 : mirror, 16 pairs + exactly 1 axis point                                     [SYMZ 2a / MIRROR.md]
  T_M34 : mirror, 17 pairs + 0 axis points                                            [SYMZ 2b]
  T_REG : C_s with s >= 7 and at least one non-centre orbit (regular s-gon, elementary)
"""
import itertools, json, sys

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 600
SMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 60


def divisors(s):
    return [d for d in range(2, s + 1) if s % d == 0]


def rot_decomps(s, n):
    """all (k, e) with n = s*k + e, e in {0,1}, e = 0 if s even"""
    out = []
    for e in ((0,) if s % 2 == 0 else (0, 1)):
        if n - e >= 0 and (n - e) % s == 0:
            out.append(((n - e) // s, e))
    return out


def rot_excluders(s, k, e, thms):
    """which theorems in `thms` exclude a C_s-invariant set with k orbits and centre flag e (using subgroups and
    deletion of whole orbits / the centre).  Returns the list of (theorem, subgroup order d, witness)."""
    hits = []
    for d in divisors(s):
        kd = k * (s // d)            # number of C_d orbits
        ed = e                        # centre is still the only fixed point
        if d % 2 == 0:
            assert ed == 0
        if "T_REG" in thms and d >= 7 and kd >= 1:
            hits.append(("T_REG", d, f"one regular {d}-gon orbit"))
        if "T_C3" in thms and d == 3 and kd >= 11:
            hits.append(("T_C3", d, f"keep 11 of {kd} C3-orbits, drop centre={ed}"))
        if "T_C5" in thms and d == 5 and 5 * kd + ed >= 35:
            hits.append(("T_C5", d, f"{5 * kd + ed} >= 35 points"))
        if "T_C4" in thms and d == 4 and kd >= 8:
            hits.append(("T_C4", d, f"keep 8 of {kd} C4-orbits"))
        if "T_C2" in thms and d == 2 and kd >= 17:
            hits.append(("T_C2", d, f"keep 17 of {kd} antipodal pairs"))
    return hits


def mirror_excluders(k, b, thms):
    hits = []
    if "T_M34" in thms and b == 0 and k >= 17:
        hits.append(("T_M34", 2, f"keep 17 of {k} pairs"))
    if "T_M33" in thms and b >= 1 and k >= 16:
        hits.append(("T_M33", 2, f"keep 16 of {k} pairs and 1 of {b} axis points"))
    return hits


ALL = {"T_C3", "T_C5", "T_C4", "T_C2", "T_M33", "T_M34", "T_REG"}
MINIMAL = {"T_C3", "T_C5", "T_C2", "T_M33", "T_M34", "T_REG"}
WRITEUP_COR3 = {"T_C3", "T_C5", "T_C4", "T_M33", "T_M34", "T_REG"}   # Corollary 3 hypotheses (no T_C2)

report = {"NMAX": NMAX, "SMAX": SMAX}

# 1. every n >= 33, every symmetry type: excluded by MINIMAL; by WRITEUP_COR3 except pure half-turn (s = 2)
fail_min, fail_cor3, used = [], [], {}
for n in range(33, NMAX + 1):
    for s in range(2, SMAX + 1):
        for (k, e) in rot_decomps(s, n):
            h = rot_excluders(s, k, e, MINIMAL)
            if not h:
                fail_min.append(("C%d" % s, n, k, e))
            for t, d, w in h:
                used.setdefault(t, set()).add("C%d" % s)
            h3 = rot_excluders(s, k, e, WRITEUP_COR3)
            if not h3 and s != 2:
                fail_cor3.append(("C%d" % s, n, k, e))
            if s == 2 and h3:
                fail_cor3.append(("C2 unexpectedly excluded", n))
            if s == 2:
                assert n % 2 == 0 and n >= 34, (n, k, e)    # Corollary 3: the residual case is even, >= 34
    for b in (0, 1, 2):
        if (n - b) % 2 == 0:
            k = (n - b) // 2
            h = mirror_excluders(k, b, MINIMAL)
            if not h:
                fail_min.append(("mirror", n, k, b))
            for t, d, w in h:
                used.setdefault(t, set()).add("mirror b=%d" % b)
report["minimal_set_failures"] = fail_min
report["cor3_failures"] = fail_cor3
report["theorems_used_by_minimal_set"] = {t: sorted(v) for t, v in used.items()}

# 2. necessity of each member of MINIMAL: drop it and find the first n >= 33 where something is not excluded
need = {}
for t in sorted(MINIMAL):
    rest = MINIMAL - {t}
    first = None
    for n in range(33, NMAX + 1):
        for s in range(2, SMAX + 1):
            for (k, e) in rot_decomps(s, n):
                if not rot_excluders(s, k, e, rest):
                    first = first or ("C%d" % s, n, k, e)
        for b in (0, 1, 2):
            if (n - b) % 2 == 0 and not mirror_excluders((n - b) // 2, b, rest):
                first = first or ("mirror", n, (n - b) // 2, b)
        if first:
            break
    need[t] = first
report["dropping_each_minimal_theorem_first_uncovered"] = need

# 3. redundancy of T_C4 (and of any C6-specific statement) once T_C2 holds, for n >= 33
red = {}
for s in (4, 6, 8, 12):
    ok = all(rot_excluders(s, k, e, MINIMAL - {"T_C3"} if s % 3 else MINIMAL)
             for n in range(33, NMAX + 1) for (k, e) in rot_decomps(s, n))
    red["C%d covered without T_C4%s" % (s, "" if s % 3 == 0 else " and without T_C3")] = ok
report["redundancy"] = red

# 4. the table N(type) = largest n with a decomposition NOT excluded by ALL theorems (n < NMAX)
table = {}
for s in range(2, SMAX + 1):
    best = None
    for n in range(0, NMAX + 1):
        for (k, e) in rot_decomps(s, n):
            if not rot_excluders(s, k, e, ALL):
                best = (n, k, e)
    table["C%d" % s] = best
best = None
for n in range(0, NMAX + 1):
    for b in (0, 1, 2):
        if (n - b) % 2 == 0 and n - b >= 0 and not mirror_excluders((n - b) // 2, b, ALL):
            best = (n, (n - b) // 2, b)
table["mirror"] = best
report["table_N_with_all_theorems"] = {k: v for k, v in table.items() if k in ("C2", "C3", "C4", "C5", "C6", "mirror", "C7", "C8")}
claimed = {"C2": 32, "C3": 31, "C4": 28, "C5": 31, "C6": 30, "mirror": 32}
report["table_matches_claim"] = {k: (table[k][0] == v) for k, v in claimed.items()}
report["Cs_s_ge_7_all_N_equal_1"] = all(table["C%d" % s][0] == 1 for s in range(7, SMAX + 1) if s % 2 == 1) and \
    all(table["C%d" % s][0] == 0 for s in range(7, SMAX + 1) if s % 2 == 0)

# 5. the table without T_C4 (only T_C2 for the fourfold case) and without T_C2 (C2 open)
for drop in ("T_C4", "T_C2"):
    t2 = {}
    for s in (2, 4, 6):
        best = None
        for n in range(0, NMAX + 1):
            for (k, e) in rot_decomps(s, n):
                if not rot_excluders(s, k, e, ALL - {drop}):
                    best = (n, k, e)
        t2["C%d" % s] = best
    report["table_without_" + drop] = t2

# 6. which sizes are possible for each type in [28, 40] (for the record)
poss = {}
for s in (2, 3, 4, 5, 6):
    poss["C%d" % s] = [n for n in range(28, 41) if rot_decomps(s, n)]
poss["mirror"] = [n for n in range(28, 41)]
report["possible_sizes_28_40"] = poss

# 7. per-size breakdown for n = 33..40: for every symmetry type with that size possible (rotation orders up to 40),
#    the theorems of MINIMAL that exclude it
per = {}
for n in range(33, 41):
    rows = []
    for s in range(2, 41):
        for (k, e) in rot_decomps(s, n):
            hs = sorted({t for t, d, w in rot_excluders(s, k, e, MINIMAL)})
            rows.append("C%d(k=%d,centre=%d): %s" % (s, k, e, "+".join(hs) if hs else "NOT EXCLUDED"))
    for b in (0, 1, 2):
        if (n - b) % 2 == 0:
            hs = sorted({t for t, d, w in mirror_excluders((n - b) // 2, b, MINIMAL)})
            rows.append("mirror(pairs=%d,axis=%d): %s" % ((n - b) // 2, b, "+".join(hs) if hs else "NOT EXCLUDED"))
    per[n] = rows
report["per_size_33_40"] = per
needed_at = {}
for n in range(33, 41):
    needed_at[n] = sorted({t for r in per[n] for t in r.split(": ")[1].split("+") if t != "T_REG"})
report["non_elementary_theorems_touched_per_size"] = needed_at

ok = (not fail_min and not fail_cor3 and all(report["table_matches_claim"].values())
      and all(v is not None for v in need.values()) and all(red.values()))
report["ALL_OK"] = ok
print(json.dumps(report, indent=1, default=list))
sys.exit(0 if ok else 1)

**Verdict: CONFIRMED** for the main statement and every count. TS±(6) fails for an abstract (5,6)-valid signotope on
15 points; label EXACT, abstract signotope (claim `tspm6-m15-abstract`, filed by T3; verifier V3, 15 November 2026,
15:02-15:06 KST).
**One sentence is NOT CONFIRMED:** "TS±(6) is decided for signotopes: true up to 14 points, false at 15."
- It rests on claim tspm6-14 (TS±(6) at 14 points). V2 gave tspm6-14 **NOT CONFIRMED** at 14:46 KST (VERIFY_TSPM6_14.md): an independent
  cake_lpr re-run did not fit in a verifier's 400 MB budget.
- So "true at 14" is CERTIFIED only by T3's own cake_lpr run and is not yet independently verified.
- The other two premises are verified: tspm6-le13 (CONFIRMED by V3) and "no valid 16-point signotope" (root6-m16-vacuous,
  CONFIRMED by V1).
- [note 15 Nov pm (C1 issue 5; added by H1, not by V3): the premise of this exception lapsed when V2 changed tspm6-14 to
  CONFIRMED (verdict file 16:53:54; its `previous` field keeps the 14:46 NOT CONFIRMED). V3 has not updated this verdict
  (verdict file 16:33:57, checked at 19:15), so the sentence stays NOT CONFIRMED in V3's verdict; H1 changes no verdict.]

# Independent check: TS±(6) fails on an abstract 15-point signotope

**Definitions** (CONJTS_TEST.md §2, THEORY_1115PM.md §0, ROUND6.md "Definitions", candidates.md K2/K2′), with n = 6, so a
gon is a convex pentagon.
- Terminal-safe weak Δ of U: a 4-cap-free subset of U meeting every gon of U, where every 3-cap a<b<c inside it has
  (b,c) ending a 4-cap of U.
- Initial-safe weak Δ of V: the mirror notion, where (a,b) starts a 4-cap of V.
- Signs: variables 1..455 are the lexicographic triples of 0..14, true = cup.
- A k-cap has every triple a cap. A 4-set is convex iff s(abc) = s(abd) and s(acd) = s(bcd).

## Results (own code `v3_tspm15_check.py`, written before reading T3's tools; 1.5 s, single thread)

| check | result | claim |
|---|---|---|
| CNF SHA-256 | `1467209fc569ac9c2f1a074c69e956600657ee7c5419e98f9d107bac72637b1f` | equal |
| solver log `t3/cert/tspm6/tspm6_m15.cadical.log` | `c Version 2.1.3`, `s SATISFIABLE`, `c exit 10` | |
| model | all 11,284 variables assigned once; **0 of 120,464 clauses falsified** | 120,464 ✓ |
| decoding | variables 1..455 equal `t3/models/tspm6_m15.json` | ✓ |
| signotope / 5-caps / convex hexagons | 0 violations / 0 / 0 | ✓ |
| 4-caps; ending at r = 14; starting at l = 0 | 25; 3; 5 | 25; 3; 5 ✓ |
| convex pentagons in U / V / S | 210 / 216 / 282 | 210 / 216 ✓ |
| **terminal-safe weak Δs of U** (all 2^14 subsets) | **0** | 0 ✓ |
| **initial-safe weak Δs of V** (all 2^14 subsets) | **0** | 0 ✓ |
| weak Δs of S / through r / through l | 1,607 / 914 / 717 | 1,607 / 914 / 717 ✓ |
| ENV# Δs of S / of U (↑P4 by reachability over the generated order) | 1,014 / 526 | 1,014 / 526 ✓ |

- ROOT and mirror ROOT hold on S, because there are weak Δs through r and through l. A weak Δ of S through r is the same
  thing as a rooted Δ of U.
- So LR(6) holds on S, consistent with lrr6-certified (CONFIRMED by V1).
- U has ENV# Δs, so TWO-ENV#(6) holds on S (K2′: U has an ENV# Δ or V has a mirror-ENV# Δ).
- Weak D(5,6) holds on S.

**Positive control.** For each interior p = 1..13, S − p is a 14-point valid signotope in which r ends and l starts a
4-cap. In all 13 cases my counter finds terminal-safe and initial-safe weak Δs (TS 1-30, IS 3-33). So the counter
does find solutions where they exist, and S is point-minimal for the failure. This agrees with TS±(6) at 14 points,
but it does not prove it.

**Comparison** with T3's `runs/tspm6_m15.forms.json`, read after my run. Every number agrees: 25, 282, 1,607, 3, 210,
914, 0, 5, 216, 717, 0, 1,014 and 526. T3's tools `check_forms.py` (`33dc47ca…`) and `t3lib.py` (`9e15cee6…`) were not
needed for the comparison.

**Scope.**
- This is an abstract signotope. Its realizability is "being tested" by the filer and is not part of this verdict.
  [superseded 15 Nov pm (C1 issue 18; note by H1): settled; it has no x-sorted realization (BFP certificate on 9 points
  + V, 76 inequalities, checked by V2 in VERIFY_TSPM6_REAL15.md)]
- The claim is a model of a CNF, so no proof file is involved.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/v3/tspm6-m15-abstract/`)

| file | SHA-256 |
|---|---|
| `v3_tspm15_check.py` | `cae399c70e6cb2030bd172b6deac342edc10523bf8292b2af432778c706edf34` |
| `v3_tspm15_check.out.json` | `26303704843196ed6c72ec61926c2caa15dc50747b0cb6fc484fb94291ff682e` |

Inputs:

| file | SHA-256 |
|---|---|
| `tspm6_m15.cadical.log` | `aec69f89…2157` |
| `tspm6_m15.json` | `a3210576…08ce` |

Re-run: `python3 -I v3_tspm15_check.py $T3/cnf/tspm6_m15.cnf $T3/cert/tspm6/tspm6_m15.cadical.log
$T3/models/tspm6_m15.json`, with `T3=/home/jay/research/data/roadmap-20261115/pm1115/t3`.

## Update (16:35 KST, V3)

- **tspm6_m14 has been re-run.** The main session re-ran cake_lpr on T3's kept tspm6_m14 proof
  (`round6/mainsession/tspm6recake/`, heap 1500, FIFO stream). It finished at 14:46:19, 19 s after V2's verdict.
  - exactly one `s VERIFIED UNSAT` line, exit 0;
  - CNF SHA-256 `921018d6…c9ac` and streamed LRAT SHA-256 `aa802dae…e104`, both equal to claim tspm6-14;
  - `.zst` SHA-256 equal to the kept file.

  V2 named that re-run as the only missing step, so the evidence for "TS±(6) true at 14" is now complete.
- **The formal status is unchanged.** tspm6-14 still carries V2's NOT CONFIRMED verdict until V2 or another verifier
  updates it. So the "decided" sentence of this claim stays **NOT CONFIRMED** here. [superseded 15 Nov pm (C1 issue 5;
  note by H1): V2 updated tspm6-14 to CONFIRMED at 16:53:54; this verdict was not updated afterwards (see the note at
  the top)]

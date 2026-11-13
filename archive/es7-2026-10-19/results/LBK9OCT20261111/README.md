# LBK9OCT20261111: an 8-fold set of 128 points without a convex 9-gon? (11–12 November 2026)

**Question.** Is there a set of 128 = 2^7 points in general position, invariant under a rotation of order 8, with no
9 points in convex position? This is the k = 9 case of the PRIMEFOLD conjecture (`PRIMEFOLD` §7). By the layer lemma
(K = 9 <= 2m = 16; `LAYERLEAN`, Lean-checked) such a set is t = 16 nested regular octagons without the centre. The
best known size is 120 (t = 15; `PRIMEFOLD` §5, `K9SEARCH`).

**Outcome.** The question stays **open**: no 128-point set was found, and nothing is proved for general phase orders.
Four new partial impossibility results restrict the phases; the strongest are Theorems 3 and 4. Label the layers
outermost first and let psi_i in [0°, 45°) be the phase of layer i relative to layer 0 (encoder A's convention,
`SOUNDNESS.md` §0).

- **Theorem 1 (no spiral).** In every 8-fold 128-point set in general position without 9 points in convex position,
  psi_1, …, psi_15 is neither increasing nor decreasing (not even weakly). All known 120-point sets and both 128-point
  near misses are increasing spirals.
- **Theorem 2 (no spiral in the middle).** In every such set, psi_2, …, psi_14 is neither (weakly) increasing nor
  (weakly) decreasing, whatever psi_1 and psi_15 are (the outermost needle layer and the inner octagon are free).
  It contains Theorem 1.
- **Theorem 3 (no spiral on layers 3..13).** In every such set, psi_3, …, psi_13 is neither (weakly) increasing
  nor (weakly) decreasing, whatever psi_1, psi_2, psi_14, psi_15 are. It contains Theorems 1 and 2 (every monotone
  run that contains layers 3..13 is excluded).
- **Theorem 4 (no 12 monotone in a row).** In every such set, no 12 consecutive phases psi_a, …, psi_{a+11}
  (a = 1, …, 4) are (weakly) increasing or decreasing.
- **Status of all:** certificate accepted by cake_lpr (every cube verdict "s VERIFIED UNSAT", bound to the hashes of
  the cube formula and the proof) on top of written soundness arguments (not refereed): encoder A (`C7UPPER/gen.py`),
  the chord lemma (`CHORD20261105`), the perturbation and reflection steps, and three new clause families (cone rules,
  threshold-order rules, cell rules) whose proofs are in `SOUNDNESS.md`. One step of the threshold-order family is a
  floating-point computation with explicit error bounds, not exact arithmetic. None of the new arguments has been
  reviewed by anyone else (a second reading only).
- **Gate.** Before these claims, every added family was checked against real configurations (§3): the exact
  assignments of four 120-point sets, two 128-point near misses, a 112- and a 104-point set, their mirror images and
  layer subsets (446 configurations, 87,122,802 clause evaluations, 0 violations); 7 cube-level positive controls
  at t = 15 (the same formulas and cube splits, one layer fewer: all SAT, also without fixing a set); and random real
  configurations (0 violations).
- **Evidence** (phase-fixed LP-CEGAR, §7): the 16 phases of the near miss admit no radii; the phases of
  `c8_120pts_15layers` plus one new octagon admit no radii at any of 31 tried insertions (all 15 radial slots);
  an outer octagon added to `f_del0` fails at 12 tried phases.

Rigor labels: Lean-checked / certificate accepted by cake_lpr / exact computation / written proof (not refereed) /
computational evidence / conjecture. One Linux machine (x86_64), at most 6 (later 8) threads and 14 (later 16) GB,
CaDiCaL 2.1.3 (system build), cake_lpr in `~/.local/bin`. Work directory (outside Git): `<lb-k9oct-work-dir>`
= `/home/jay/research/data/lb-k9oct-20261111`; `<six10-work-dir>` as in `SIX60`.

## 1. Encoding and exact labelling

**Encoder A** (`C7UPPER/gen.py`; byte-identical copy `tools/gen.py`, SHA-256 `4564e7f0…`). Its soundness for
(m, K, t) with K <= 2m is the written proof in its docstring (not refereed; reviewed for (6, 8) in `ROT456` §2). The
layer lemma, strict nesting, the chain family's soundness and the polar rules are Lean-checked (`LAYERLEAN`).

| CNF | variables | clauses | triple orbits | SHA-256 |
|---|---:|---:|---:|---|
| `gen.py 8 9 15` | 410,352 | 22,680,241 | 35,105 | `0bd760bf…` |
| `gen.py 8 9 16` | 497,697 | 29,479,779 | 42,672 | `91394934…` |

The chain family is almost all of it (t = 16: 29.4 M clauses; 5.1 M for the outermost pivot alone). Chord-lemma
clauses (`CHORD20261105`; `tools/chord_rules_m.py`, the source with one path line changed, same output byte for
byte): 3,758 (t = 15) and 4,296 (t = 16).

**Exact labelling** (`tools/label8.py`). From a `.pts` file (rows of Z[zeta_8] coefficients) it checks exactly, in
Z[sqrt2], the orbit structure (row 8o+k = zeta^k row 8o), distinct points and strictly decreasing radii, and computes
the sector labelling of encoder A, the sign of every triple-orbit representative (all nonzero) and Y(i, j). The bin
variables Z(i, b) are computed exactly by doubling or quadrupling the angle (`tools/check_cells.py`,
`tools/controls2.py`).

## 2. Three new clause families

Encoder A's angular rules use only the phase *order* and two patterns (centre inside the triangle; middle point
outermost). Every orientation of nested regular octagons is linear in the inverse radii u_i = 1/r_i (`ES8SYM`
Lemma 1). The new families use this with the radius order 0 < u_0 < u_1 < … . Full statements, hypotheses and
proofs: **`SOUNDNESS.md`** (written proofs, not refereed).

- **(a) Cone rules** (`tools/cone_rules.py`; exact rational arithmetic in units of pi). A triple's sign is fixed for
  all radii iff the form is >= 0 (or <= 0) on every generator of the radius cone and nonzero on one; each generator
  value is a product of sines of affine functions of the phases, whose signs are constant and exactly computable on
  an order cell. t = 16: 64,197 clauses (17,787 units). Under the increasing order they fix 26,432 triple signs,
  against 23,192 for gen.py's rules plus the chord clauses (all but 120 of which they reproduce).
- **(b) Threshold-order rules** (`tools/thr_rules2.py`). Two orbits on the same two layers change sign at thresholds
  of the radius ratio; when the order of the thresholds is the same on the whole phase cell, one implies the other
  (binary clause with the pair's Y literal as premise). The order is decided by exact algebra in Q(zeta_16) at the
  cell's endpoints and a bisection with explicit bounds inside (**floating point with explicit error bounds**).
  t = 16: 8,550 clauses.
- **(c) Cell rules** (`tools/cell_rules.py`, `tools/cell_thr.py`, `tools/binorder.py`). Bin variables
  Z(i, b) = [psi_i < b·45°/B] refine the order cells; (a) and (b) on each cell (exact vertex enumeration, endpoint
  algebra in Q(zeta_{16B})); bin-order clauses. B = 2, t = 16: 191,930 + 29,700 + 210 clauses; Z_i := Z(i, 1) =
  [psi_i < 22.5°] is variable 497,697 + i. B = 4 (only in the unsolved run S10): 965,980 + 132,480 + 630 + 30.

Only gen.py's nest and chain families need the strict nesting of the convex layers; only the chain family needs "no
convex 9-gon"; all other families need only the radius order and generic phases (`SOUNDNESS.md` §1).

## 3. The gate: controls before any claim

**(i) Exact assignments of real configurations** (`tools/controls2.py`, `logs/controls2.log`; exact computation).
Every subset of the octagons of a real configuration is again a configuration with (H) and (G), and so is its mirror
image (complex conjugation of the Z[zeta_8] coefficients; it reverses the phase order). For each of
`PRIMEFOLD/sets/k9/c8_120pts_15layers`, `K9SEARCH/sets/f_del0`, `PRIMEFOLD/sets2/c8_120pts_blowup2orb`,
`…_blowup3orb`, `K9SEARCH/sets/k9_128_final`, `K9SEARCH/sets/k9_128_best`, `PRIMEFOLD/sets/k9/c8_112pts_14layers`
and `c8_104pts_13layers`: the set itself, every set with one octagon removed, the outermost and innermost k octagons
and 6 random k-subsets (k in {10, 12, 14, 15}), each also mirrored. For each, all clauses of gen.py's order, angle and
nest families, chord, cone, threshold-order, cell (B = 2) and bin-order families for the matching t were evaluated on
the exact assignment (with Z). Result: 446 configurations (t = 10 … 16), 87,122,802 clause
evaluations, **0 violations**. The 120- and 128-point sets have the increasing order and their mirrors the decreasing
one; the 112- and 104-point sets have non-monotone orders, as do 98 of the 446 configurations; the bin patterns
vary. (The near misses have convex 9-gons, so only the chain family can and does
reject them.) Encoder A (8, 9, 15) plus the exact values of `c8_120pts_15layers`: SAT, so the chain family accepts a
real 120-point set; encoder A (8, 9, 16) plus the near miss: UNSAT (it sees the 1,136 9-gons)
(`logs/controls_exact.log`, `logs/controls_sat.log`).

**(ii) Cube-level positive controls at t = 15** (`tools/ctrl15/run.sh`, `run2.sh`; `logs/controls15_cubes.txt`). BASE15 is
built exactly like the BASE of §4 with one layer fewer (encoder A (8, 9, 15) + chord + cone + threshold-order + cell
B = 2 + bin-order + the 91 increasing-order units; 22,923,910 clauses), BASE15dec the same with the 91 units negated.
With the same decision-list cubes:

| control | formula | result |
|---|---|---|
| P1 | BASE15 + cube "Z_1..Z_14" + exact values of `c8_120pts_15layers` | SAT (6 s) |
| P2 | BASE15 + cube "Z_1..Z_13, not Z_14" + exact values of `c8_120pts_blowup3orb` | SAT (5 s) |
| P3 | BASE15 + cube "Z_1..Z_14", nothing else | SAT (35 s) |
| P4 | BASE15 + cube "Z_1..Z_13, not Z_14", nothing else | SAT (11 s) |
| P5 | BASE15dec + cube "not Z_1" + exact values of the mirror of `c8_120pts_15layers` | SAT (6 s) |
| P6 | BASE15dec + cube "not Z_1" + exact values of the mirror of `f_del0` | SAT (5 s) |
| P7 | BASE15dec + cube "not Z_1", nothing else | SAT (27 s) |

So the machinery that refutes every cube at t = 16 in 3–7 minutes finds models at t = 15 within seconds, also in the
mirrored (decreasing) setting.

**(iii) Random real configurations** (`tools/rand_check.py`; evidence). Random phases in any order, random radii
over several scales and near-generator radius patterns, float orientations with a margin filter:
- configurations with only the radius order (H0): 270–357 per family for chord, cone, threshold-order, cell B = 2 and
  B = 4, bin-order, at t = 15 and 16: 0 violations; gen.py's nest units are violated by such configurations, as they
  must be (they need strict nesting), and nothing else;
- configurations filtered for strict nesting of the convex layers (H), all families including gen.py's order,
  angle and nest: 146 at t = 15 and 241 at t = 16, 0 violations;
- near-generator radii ("extreme"): 131 (t = 16) and 100 (t = 15) configurations, 0 violations;
- t = 4, every cone and threshold-order clause against 18,955 random configurations: 0 violations
  (`tests/test_cone_dense.py`).

**(iv) Cube covers** are checked separately (`tools/verify_cover_mono.py`: enumeration of all assignments of the
cube variables, recomputed cube hashes, recorded verdicts; §4–§5b) and argued in `SOUNDNESS.md` §5 (reflection,
decision-list cover).

## 4. Theorem 1: no monotone phase order (t = 16)

**Statement.** Let S be 16 nested regular octagons about O (no centre), in general position, with no 9 points in
convex position. Then psi_1, …, psi_15 is neither (weakly) increasing nor (weakly) decreasing.

**Proof** (`SOUNDNESS.md` §5). Perturb to generic phases keeping the order type and the monotonicity; reflect a
decreasing sequence into an increasing one; the intended assignment satisfies BASE = encoder A (8, 9, 16) + chord +
cone + threshold-order + cell (B = 2) + bin-order + the 105 units Y(i, j); the 16 cubes c_r (r = 0..14:
Z_1..Z_r true, Z_{r+1} false; c_15: all true) cover all assignments of Z_1..Z_15; each BASE ∧ c_r is UNSAT with a
cake_lpr-verified LRAT proof.

BASE: `sat/S8/S8.cnf` in the work directory, 497,712 variables, 29,778,767 clauses, SHA-256 `c21e70c6…`;
`tools/build_S8.sh` rebuilds it and every part from the generators with the recorded hashes (`logs/build_S8.log`).

| cube | Z cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 |
|---|---|---:|---:|---:|---|---|---|
| c_0 | not Z_1 | 206 | 19,587 | 0.93 | verified, 47 s | `3a1e08a1…` | `04c23f28…` |
| c_1 | Z_1, not Z_2 | 211 | 19,450 | 0.95 | verified, 47 s | `8bed4c11…` | `ea0e4774…` |
| c_2 | Z_1..Z_2, not Z_3 | 235 | 27,164 | 0.97 | verified, 48 s | `bad7e247…` | `6725e9e6…` |
| c_3 | Z_1..Z_3, not Z_4 | 165 | 15,577 | 0.92 | verified, 48 s | `b56368e9…` | `1d9493ee…` |
| c_4 | Z_1..Z_4, not Z_5 | 270 | 33,173 | 1.07 | verified, 50 s | `b99b4790…` | `bbc1f663…` |
| c_5 | Z_1..Z_5, not Z_6 | 286 | 37,821 | 1.09 | verified, 51 s | `db15a655…` | `8154ccce…` |
| c_6 | Z_1..Z_6, not Z_7 | 278 | 36,831 | 1.09 | verified, 52 s | `b96e05ba…` | `c634e838…` |
| c_7 | Z_1..Z_7, not Z_8 | 328 | 42,764 | 1.10 | verified, 53 s | `ed75abca…` | `a7c3941a…` |
| c_8 | Z_1..Z_8, not Z_9 | 353 | 47,390 | 1.10 | verified, 52 s | `d58f2569…` | `03a43f8b…` |
| c_9 | Z_1..Z_9, not Z_10 | 360 | 46,170 | 1.08 | verified, 52 s | `ec9dabe0…` | `a2ccc14a…` |
| c_10 | Z_1..Z_10, not Z_11 | 334 | 45,437 | 1.11 | verified, 51 s | `a3607e75…` | `87530020…` |
| c_11 | Z_1..Z_11, not Z_12 | 320 | 42,117 | 1.06 | verified, 51 s | `ed1497cc…` | `890cc864…` |
| c_12 | Z_1..Z_12, not Z_13 | 372 | 42,712 | 1.06 | verified, 50 s | `1575830f…` | `97b15fdb…` |
| c_13 | Z_1..Z_13, not Z_14 | 319 | 37,233 | 1.05 | verified, 50 s | `4a74a682…` | `1eaeaf96…` |
| c_14 | Z_1..Z_14, not Z_15 | 291 | 37,703 | 1.06 | verified, 54 s | `866aec31…` | `87689d88…` |
| c_15 | Z_1..Z_15 | 281 | 38,651 | 1.09 | verified, 51 s | `4603e2ac…` | `7e939f66…` |

Totals: 4,588 s of CaDiCaL (569,780 conflicts), 16.7 GB of LRAT (4.2 GB with zstd -3; every decompression round trip
checked, `logs/roundtrip_mono.log`), 13.5 minutes of cake_lpr (heap 11,000 MB; 7,000 MB is too small for these
29.8 M-clause formulas). `logs/verify_cover_mono.log`: cover by enumeration, all 16 recomputed cube hashes equal to the
recorded ones, 16 verdicts. Per-cube logs: `logs/cubes/c_r/`.

## 5. Theorem 2: no monotone phase order on layers 2..14

**Statement.** Let S be 16 nested regular octagons about O (no centre), in general position, with no 9 points in
convex position. Then psi_2, …, psi_14 is neither (weakly) increasing nor (weakly) decreasing; psi_1 and psi_15 are
arbitrary. (This contains Theorem 1.)

**Proof** (`SOUNDNESS.md` §5, "partially monotone"). As for Theorem 1, with BASE2 = encoder A (8, 9, 16) + chord +
cone + threshold-order + cell (B = 2) + bin-order + the 78 units Y(i, j), 2 <= i < j <= 14 (`cnf/mono2to14.units`),
and the 14 decision-list cubes on Z_2..Z_14 (Z_1 and Z_15 free). The reflection maps a sequence decreasing on layers
2..14 to one increasing on them.

BASE2: `sat/S13/S13.cnf` in the work directory, 497,712 variables, 29,778,740 clauses, SHA-256 `ad8ef197…`;
`tools/build_base.sh OUT mono2to14` rebuilds it with the same hash (`logs/build_S13.log`).

| cube | Z cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 |
|---|---|---:|---:|---:|---|---|---|
| c_0 | not Z_2 | 249 | 19,124 | 0.92 | verified, 51 s | `6f529b18…` | `d44ec3d5…` |
| c_1 | Z_2, not Z_3 | 330 | 31,688 | 1.01 | verified, 51 s | `bbc5d333…` | `d3083ed7…` |
| c_2 | Z_2..Z_3, not Z_4 | 309 | 28,391 | 0.96 | verified, 48 s | `ce547ac0…` | `80ec42e7…` |
| c_3 | Z_2..Z_4, not Z_5 | 360 | 38,400 | 1.09 | verified, 57 s | `bc0a0172…` | `f040a995…` |
| c_4 | Z_2..Z_5, not Z_6 | 390 | 38,778 | 1.09 | verified, 58 s | `810e398c…` | `0168abfd…` |
| c_5 | Z_2..Z_6, not Z_7 | 343 | 38,906 | 1.09 | verified, 55 s | `31f1ef1b…` | `4c04411e…` |
| c_6 | Z_2..Z_7, not Z_8 | 404 | 43,206 | 1.09 | verified, 58 s | `21ce6f02…` | `92118132…` |
| c_7 | Z_2..Z_8, not Z_9 | 433 | 46,438 | 1.03 | verified, 53 s | `c49eda4c…` | `e173dd50…` |
| c_8 | Z_2..Z_9, not Z_10 | 503 | 52,567 | 1.13 | verified, 57 s | `df20fa7e…` | `0ba968ee…` |
| c_9 | Z_2..Z_10, not Z_11 | 558 | 55,818 | 1.10 | verified, 64 s | `684a9722…` | `545e04bd…` |
| c_10 | Z_2..Z_11, not Z_12 | 473 | 48,261 | 1.03 | verified, 60 s | `7268a66a…` | `e5c6b37a…` |
| c_11 | Z_2..Z_12, not Z_13 | 473 | 48,831 | 1.04 | verified, 61 s | `a72a5cf7…` | `63030fae…` |
| c_12 | Z_2..Z_13, not Z_14 | 393 | 44,189 | 1.07 | verified, 63 s | `657176c9…` | `55b11bf3…` |
| c_13 | Z_2..Z_14 | 424 | 40,991 | 1.04 | verified, 61 s | `7fc81961…` | `61f36598…` |

Totals: 5,632 s of CaDiCaL (575,588 conflicts), 14.7 GB of LRAT (3.8 GB with zstd -3; round trips checked,
`logs/roundtrip_g5.log`), 13.3 minutes of cake_lpr (heap 11,000 MB). `logs/verify_cover_g5.log`: cover of all 2^13
assignments of Z_2..Z_14 by enumeration, 14 recomputed cube hashes equal to the recorded ones, 14 verdicts. Per-cube
logs: `logs/cubes13/c_r/`.

## 5a. Theorem 3: no monotone phase order on layers 3..13

**Statement.** Let S be 16 nested regular octagons about O (no centre), in general position, with no 9 points in
convex position. Then psi_3, …, psi_13 is neither (weakly) increasing nor (weakly) decreasing; psi_1, psi_2, psi_14
and psi_15 are arbitrary. (This contains Theorems 1 and 2.)

**Proof.** As for Theorem 2 with BASE3 = encoder A (8, 9, 16) + chord + cone + threshold-order + cell (B = 2) +
bin-order + the 55 units Y(i, j), 3 <= i < j <= 13 (`cnf/mono3to13.units`), and the 12 decision-list cubes on
Z_3..Z_13 (Z_1, Z_2, Z_14, Z_15 free).

BASE3: `sat/S14/S14.cnf` in the work directory, 497,712 variables, 29,778,717 clauses, SHA-256 `ccb947f7…`;
`tools/build_base.sh OUT 3-13` rebuilds it with the same hash (`logs/build_S14.log`).

| cube | Z cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 |
|---|---|---:|---:|---:|---|---|---|
| c_0 | not Z_3 | 510 | 43,546 | 1.14 | verified, 60 s | `9ee4edea…` | `c3d2911f…` |
| c_1 | Z_3, not Z_4 | 641 | 48,697 | 1.13 | verified, 59 s | `7b52881e…` | `4a1b4098…` |
| c_2 | Z_3..Z_4, not Z_5 | 635 | 50,324 | 1.29 | verified, 67 s | `1f9a0735…` | `1a6a69e2…` |
| c_3 | Z_3..Z_5, not Z_6 | 684 | 53,767 | 1.18 | verified, 61 s | `7adcc100…` | `ddb5d46d…` |
| c_4 | Z_3..Z_6, not Z_7 | 737 | 66,095 | 1.19 | verified, 65 s | `5c61558d…` | `ca573340…` |
| c_5 | Z_3..Z_7, not Z_8 | 1347 | 131,209 | 1.52 | verified, 70 s | `621a5e81…` | `af799d88…` |
| c_6 | Z_3..Z_8, not Z_9 | 1572 | 146,683 | 1.64 | verified, 72 s | `44050afd…` | `0b231797…` |
| c_7 | Z_3..Z_9, not Z_10 | 1480 | 136,747 | 1.58 | verified, 73 s | `4a0b8bd9…` | `45b9c2ca…` |
| c_8 | Z_3..Z_10, not Z_11 | 1436 | 134,243 | 1.53 | verified, 71 s | `0d7cafb5…` | `f6099925…` |
| c_9 | Z_3..Z_11, not Z_12 | 1323 | 127,805 | 1.54 | verified, 72 s | `064119be…` | `e3f917b2…` |
| c_10 | Z_3..Z_12, not Z_13 | 1411 | 127,130 | 1.61 | verified, 75 s | `3074213a…` | `d677cc48…` |
| c_11 | Z_3..Z_13 | 642 | 68,823 | 1.25 | verified, 66 s | `a48e0f8e…` | `d6fa118b…` |

Totals: 12,370 s of CaDiCaL (1,135,069 conflicts; the cubes took 8.5–26 minutes), 16.6 GB of LRAT (4.3 GB with
zstd -3; round trips checked, `logs/roundtrip_g6.log`), 13.5 minutes of cake_lpr (heap 11,000 MB).
`logs/verify_cover_g6.log`: cover of all 2^11 assignments of Z_3..Z_13 by enumeration, 12 recomputed cube hashes
equal to the recorded ones, 12 verdicts. Per-cube logs: `logs/cubes14/c_r/`.

## 5b. Theorem 4: no 12 consecutive monotone phases

**Statement.** Let S be as above. Then no 12 consecutive phases psi_a, …, psi_{a+11} (a = 1, 2, 3, 4) are (weakly)
increasing or (weakly) decreasing.

**Proof.** The windows 2..13 and 3..14 contain 3..13, so Theorem 3 excludes them. The windows 1..12 and 4..15 are
excluded as in Theorem 2, with the units Y(i, j) for 1 <= i < j <= 12 (`cnf/mono1to12.units`, base `sat/V1/V1.cnf`,
SHA-256 `6d97dccb…`) and the 13 cubes on Z_1..Z_12, resp. 4 <= i < j <= 15 (`cnf/mono4to15.units`, base
`sat/V4/V4.cnf`, `cacb288c…`) and the 13 cubes on Z_4..Z_15. `tools/build_base.sh OUT 1-12` and `OUT 4-15` rebuild both
bases with these hashes (`logs/build_V1.log`, `logs/build_V4.log`).

Window 1..12:

| cube | Z cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 |
|---|---|---:|---:|---:|---|---|---|
| c_0 | not Z_1 | 661 | 45,947 | 1.16 | verified, 60 s | `f1c81c19…` | `a6a51c1f…` |
| c_1 | Z_1, not Z_2 | 677 | 54,231 | 1.30 | verified, 63 s | `66ff3dc4…` | `adde1cdd…` |
| c_2 | Z_1..Z_2, not Z_3 | 611 | 51,255 | 1.25 | verified, 60 s | `4041543c…` | `7b51bee1…` |
| c_3 | Z_1..Z_3, not Z_4 | 642 | 54,890 | 1.27 | verified, 62 s | `6dd5f7a3…` | `df112462…` |
| c_4 | Z_1..Z_4, not Z_5 | 776 | 78,216 | 1.41 | verified, 67 s | `509f50d0…` | `74b7054f…` |
| c_5 | Z_1..Z_5, not Z_6 | 863 | 88,707 | 1.38 | verified, 65 s | `4ff40f39…` | `4221948a…` |
| c_6 | Z_1..Z_6, not Z_7 | 1359 | 136,424 | 1.64 | verified, 73 s | `f7362646…` | `b79cff58…` |
| c_7 | Z_1..Z_7, not Z_8 | 1202 | 141,766 | 1.71 | verified, 75 s | `c3e28281…` | `2517471d…` |
| c_8 | Z_1..Z_8, not Z_9 | 1440 | 156,644 | 1.73 | verified, 75 s | `1d472e0f…` | `f3335bc1…` |
| c_9 | Z_1..Z_9, not Z_10 | 1166 | 134,369 | 1.54 | verified, 68 s | `edbb46bb…` | `2caf7c7a…` |
| c_10 | Z_1..Z_10, not Z_11 | 914 | 105,863 | 1.55 | verified, 70 s | `3a25e271…` | `76363592…` |
| c_11 | Z_1..Z_11, not Z_12 | 803 | 97,812 | 1.42 | verified, 63 s | `fdbb4b21…` | `5aaf31d6…` |
| c_12 | Z_1..Z_12 | 642 | 60,128 | 1.15 | verified, 56 s | `ef83ccf3…` | `4913d6b3…` |

Window 4..15:

| cube | Z cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 |
|---|---|---:|---:|---:|---|---|---|
| c_0 | not Z_4 | 552 | 43,578 | 1.10 | verified, 57 s | `cb7e20e3…` | `ccdf1555…` |
| c_1 | Z_4, not Z_5 | 477 | 40,298 | 1.15 | verified, 60 s | `6c72286c…` | `b4bcd454…` |
| c_2 | Z_4..Z_5, not Z_6 | 565 | 46,554 | 1.15 | verified, 59 s | `7bbece60…` | `39799b24…` |
| c_3 | Z_4..Z_6, not Z_7 | 611 | 54,138 | 1.33 | verified, 61 s | `a8f4a9d5…` | `72315652…` |
| c_4 | Z_4..Z_7, not Z_8 | 658 | 51,811 | 1.18 | verified, 59 s | `f9afd40a…` | `f659b941…` |
| c_5 | Z_4..Z_8, not Z_9 | 765 | 58,736 | 1.25 | verified, 61 s | `031e64f6…` | `fa8683d3…` |
| c_6 | Z_4..Z_9, not Z_10 | 1215 | 109,098 | 1.61 | verified, 71 s | `aab3dde2…` | `731e6ed0…` |
| c_7 | Z_4..Z_10, not Z_11 | 1228 | 105,383 | 1.55 | verified, 69 s | `3d4c8764…` | `0d114292…` |
| c_8 | Z_4..Z_11, not Z_12 | 1338 | 127,556 | 1.58 | verified, 71 s | `f9d97f60…` | `340a9135…` |
| c_9 | Z_4..Z_12, not Z_13 | 1398 | 129,319 | 1.56 | verified, 60 s | `8b3c098a…` | `1186f10d…` |
| c_10 | Z_4..Z_13, not Z_14 | 790 | 74,117 | 1.26 | verified, 47 s | `cb2fb8b7…` | `86b61aaa…` |
| c_11 | Z_4..Z_14, not Z_15 | 910 | 71,698 | 1.26 | verified, 47 s | `400277df…` | `d4089c07…` |
| c_12 | Z_4..Z_15 | 879 | 61,673 | 1.25 | verified, 47 s | `7e1ae2ed…` | `97c7f8ce…` |

Totals: window 1..12: 11,742 s of CaDiCaL (1,206,252 conflicts), 18.5 GB of LRAT (4.7 GB with zstd), 14.3 minutes of
cake_lpr; window 4..15: 11,336 s (973,959 conflicts), 17.2 GB (4.4 GB), 12.8 minutes. Covers by enumeration (2^12
assignments each), recomputed cube hashes and verdicts: `logs/verify_cover_V1.log`, `logs/verify_cover_V4.log`; round
trips: `logs/roundtrip_V1.log`, `logs/roundtrip_V4.log`. Per-cube logs: `logs/cubesV1/c_r/`, `logs/cubesV4/c_r/`.

## 6. Whole-cube SAT runs (computational record)

All on t = 16, one thread each, CaDiCaL 2.1.3 with text LRAT; "A" = encoder A, "+" adds a family of §2. Every run
below was stopped by hand to free memory for a stronger formula (`logs/notes.txt`); none of them answered.

| run | formula | phase cube | stopped after | conflicts |
|---|---|---|---:|---:|
| S1 | A + chord | Y(1,2) | 975 s | 140,017 |
| S2 | A + chord | increasing (105 Y units) | 1,553 s | 390,666 |
| S3 | + cone | increasing | 753 s | 127,013 |
| S4 | + cone | Y(1,2) | 718 s | 78,023 |
| S5 | + cone + threshold | increasing | 1,046 s | 153,941 |
| S5u | as S5, `--unsat` preset | increasing | 735 s | 105,024 |
| S6 | + cone + threshold | Y(1,2) | 966 s | 115,612 |
| S7 | + cone + threshold + cone-cell (B = 2) | increasing | 218 s | 24,608 |
| S8 | + cone + threshold + cell (B = 2) + bin-order = BASE | increasing | 395 s | 50,003 |
| S9 | as S8 | Y(1,2) | 345 s | 36,373 |
| S10 | + cone + threshold + cell (B = 4) + bin-order | Y(1,2) | 232 s | 26,418 |

The step that worked was splitting S8 on the bins (§4): each of the 16 cubes took 3–6 minutes. The reflection unit
Y(1,2) = variable 42,673 is sound by the argument of `C6UPPER` §2 (written proof); it is used only in S1, S4, S6, S9
and S10, not in the certificate.

## 7. Phase-fixed LP-CEGAR for m = 8 (computational evidence)

`tools/lpc8.py` adapts the 6-fold LP-CEGAR of `SIX60` (`<six10-work-dir>/search/cegar/lpcegar.py`). With all 16
phases fixed, every orientation is the sign of a linear form in u; an orbit whose form has one strict sign on every
cone generator is forced (27,312 of 42,672 for the phase vectors tried; float test, relative tolerance 1e-9). The
phase-specialised CNF has the forced units, the Y units, gen.py's chain family simplified with the forced values
(about 16.1 M clauses), the remaining angle and chord clauses and the 2-layer threshold implications at the actual
phases. Loop: SAT model -> LP for u (maximal normalised margin, cone constraints) -> candidate, or a Farkas clause.
"Phase-UNSAT": the phase-specialised CNF itself is unsatisfiable, so no radii exist for these phases.

**Validation.** With the phases of `c8_120pts_15layers` and its signs as SAT assumptions (`--guide`), it returns at
iteration 1 a new radius vector (LP margin 3.7e-4); rounded to Z[zeta_8] (`tools/cand2pts.py`) it passes the exact
pipeline `tools/exact_check.sh` (label8; the independent `exact_geom.py` + `cvxcount` of `PRIMEFOLD/check120`, two
exact orientation methods and two DPs; the producer's `verify_cfg.py` methods A/B/C + `cvx2`): 120 points, no convex
9-gon, the same convex k-gon counts as the original (`logs/t15cand_exact.log`, set in `logs/t15cand/`). Subsets of the
near miss with 6, 7, 10 and 12 layers are realised by the loop (float N9 = 0, not verified exactly).

**Results** (`logs/lpc8_results.tsv`, `logs/lpc8/`; evidence only):
- The 16 phases of the near miss `k9_128_final`: phase-UNSAT. Without its inner octagon (15 layers) the phases are
  phase-SAT (the loop did not finish in 90 s), so the inner octagon is part of the obstruction.
- The phases of `c8_120pts_15layers` plus one new layer, at each of the 15 radial slots with 1–3 phase choices
  (midpoint and ±0.3° of the neighbours; for the innermost slot five phases): 31 phase vectors, all phase-UNSAT
  (first solve 16–248 s, median 48 s). The same scan for `f_del0` was not reached.
- The phases of `f_del0` plus a new outer octagon at phase 1°, 3°, …, 23°: 12 phase vectors, all phase-UNSAT.
- Without the 2-layer threshold implications the near miss's phase CNF was still unsolved after 9.5 minutes (with
  them, phase CNFs are refuted in 20–220 s); this motivated family (b).

## 8. Other evidence

- Adding an outer octagon (40 radii × 45 phases) to `c8_120pts_blowup2orb` (one orbit of the 14-point cluster of
  `PRIMEFOLD/sets2/c8_112pts_1orbit14` plus an inner octagon) leaves at least 3,544 convex 9-gons (float count,
  `logs/scan_outer_blowup2orb.txt`).
- Sampling (`tools/univ.py`, `tools/thr_univ.py`) first showed that about 26,200 signs are forced for all sampled
  increasing phase vectors and that 74% of same-pair threshold orders are; the exact families replaced the samples
  (the sampled clause sets were never used in a claim).

## 9. What this does not show

- Nothing is decided for phase sequences that are non-monotone on the layers named in the theorems: the whole formula
  with only the reflection unit Y(1,2) (S6, S9, S10) was not solved. 128 points remain open; the 8-fold maximum for
  k = 9 is 120 or 128. The 112- and 104-point records of `PRIMEFOLD` have non-monotone phase orders, so non-monotone
  structures do occur in good sets.
- A failed search is not impossibility: the LP-CEGAR scans looked at a few dozen phase vectors.
- The certificates rest on unrefereed written arguments, three of them new (`SOUNDNESS.md`), and on one
  floating-point step with explicit error bounds (family (b)).
- All LP-CEGAR statements are float computations: evidence, not proof.

## 10. Novelty

Bounded check on 11 November 2026 (evidence, not a priority claim), on top of the inspections recorded in
`PRIMEFOLD` §8 and `NOVELTY20261106`:
- arXiv API: `all:Szekeres` and `abs:"convex position"`, newest first (to 2611.05300, 3 November 2026): no paper on
  symmetric Erdős–Szekeres sets, convex 9-gons or 128-point constructions.
- arXiv versions: SMQH arXiv:2506.00224 (only v1; symmetric constructions, the "symmetric constructions for all
  k >= 7" suspicion; nothing for k = 9), Krapivin–Przybocki–Heule arXiv:2607.02958 (only v1; "satisfiability modulo
  realizability": SAT over abstract order types steered by realizability feedback, applied to the 23-point
  empty-hexagon/heptagon problem; no symmetry, no layers, no k = 9), Dumitru arXiv:2512.24061 (only v1).
- Web search for rotationally symmetric 128-point sets without a convex 9-gon: nothing beyond SMQH.
- Not re-inspected tonight: Baek–Balko (JCTA 2026 full text was not accessible before), Mackey CMU-CS-25-108
  (inspected in `PRIMEFOLD`: symmetric constructions for k <= 7 only).

No matching prior result was found for: Theorems 1 and 2 (§4, §5; no monotone phase order for 128-point 8-fold sets),
and the cone, threshold-order and cell families as SAT encodings of nested regular polygons. The closest methodological
relatives are encoder A's own angular rules (`C7UPPER`), the chord lemma (`CHORD20261105`), the phase-fixed LP of
`SIX60`, and the realizability feedback of arXiv:2607.02958.

## 11. Files

In this directory (`LBK9OCT20261111/`):
- `SOUNDNESS.md`: hypotheses and written proofs for every clause family and for the case splits.
- `tools/`
  - Encoder and families: `gen.py` (copy of `C7UPPER/gen.py`), `chord_rules_m.py` (copy of the `CHORD20261105`
    tool; path line changed, identical output), `cone_rules.py`, `thr_rules2.py`, `cell_rules.py`, `cell_thr.py`,
    `binorder.py`, `gen_families.sh` (all families for a given t), `withunits.sh`, `build_S8.sh` and `build_base.sh`
    (rebuild the base formulas of Theorems 1 and 2 and print every part's hash); `thr_rules.py` (first threshold version with a cruder test; not used).
  - Cubes and certificates: `cubes_mono.sh` (as run for solving Theorem 1's cubes), `cubes.sh` (the same with a heap
    retry and a parameter for the decision list; used for the cake_lpr checks), `cubes_g4.sh` (the same with an
    offset of the decision list; Theorem 2), `verify_cover_mono.py` (cover by enumeration + recomputed cube hashes +
    recorded verdicts), `roundtrip.sh` (zstd round trips), `cube_table.sh`; orchestration as run: `vlane.sh`,
    `wait_then_check_g5.sh`, `after_g5check.sh`, `after_g6.sh`, `after_g6b.sh`, `after_g6c.sh`, `after_v2.sh` (`wlane.sh`,
    `after_g6b.sh` and `after_v.sh` were stopped before doing anything; `logs/notes.txt`).
  - Controls: `label8.py`, `check_cnf.py`, `check_cells.py`, `controls2.py` (sets, mirrors, layer subsets),
    `run_controls.sh`, `rand_check.py`, `tools/ctrl15/run.sh` and `run2.sh` (cube-level controls at t = 15),
    `tests/test_cone_dense.py`.
  - Exact set checks: `exact_check.sh`, `cand2pts.py`, and in `tools/check/` unchanged copies of
    `PRIMEFOLD/check120/{exact_geom.py,cvxcount.c,cvxenum.c}` and `PRIMEFOLD/check120/producer/{verify_cfg.py,cvx2.c,zm.py,FORMAT.txt}`.
  - Evidence: `lpc8.py` (phase-fixed LP-CEGAR; numpy, scipy with HiGHS and python-sat, as in the venv of
    `<six10-work-dir>`), `ev9.py` + `cnt9.c` (float convex-k-gon counter), `summarize_lpc.py`, `scan_outer.py`,
    `univ.py`, `thr_univ.py`; `fit8.py`, `model2json.py`, `gen_b2.py`, `gen_b2s.py` (prepared, not used).
- `cnf/`: the small clause files for t = 15 and 16 and the unit files of the cubes; `cnf_sha256.txt` (hashes of every
  formula built, in order of creation).
- `logs/`: `notes.txt` (time-stamped run notes, including every stopped run), controls (`controls_exact.log`,
  `controls_sat.log`, `controls2.log`, `controls15_cubes.txt`, `rand_check_*.log`, `test_cone_dense_t4.log`),
  certificates (`cubes/c_r/`, `cubes13/c_r/`, `cubes14/c_r/`, `cubesV1/`, `cubesV4/`, `verify_cover_*.log`, `roundtrip_*.log`, `build_S8.log`, `build_S13.log`), LP-CEGAR
  (`lpc8/`, `lpc8_results.tsv`), scans, and the validation set `t15cand/` with `t15cand_exact.log`.

In the work directory (outside Git): the full formulas (`sat/S8/S8.cnf`, `sat/S13/S13.cnf`, `sat/S14/S14.cnf`, `sat/V1/V1.cnf`, `sat/V4/V4.cnf`), the
zstd-compressed LRAT proofs `sat/cubes*/c_r/proof.lrat.zst` (raw and compressed hashes in each `result.txt`), and all
run directories.

## 12. Reproduction

From this directory, with Python 3 (stdlib), CaDiCaL 2.1.3, cake_lpr and zstd; disk about 20 GB.

```sh
T=tools
sh $T/build_S8.sh out                         # BASE of Theorem 1 = out/S8.cnf, SHA-256 c21e70c6... (about 5 minutes)
# one cube, e.g. r = 7 (Z_1..Z_7 true, Z_8 false); Z_i is variable 497697 + i
for i in 1 2 3 4 5 6 7; do echo "$((497697 + i)) 0"; done > c7.units; echo "-497705 0" >> c7.units
sh $T/withunits.sh out/S8.cnf c7.units c7.cnf            # SHA-256 ed75abca... (logs/cubes/c_7/cnf.sha256)
cadical --lrat --binary=false c7.cnf c7.lrat             # exit 20, about 5 minutes, about 1 GB of proof
cake_lpr --CML_HEAP_SIZE=11000 --CML_STACK_SIZE=1000 c7.cnf c7.lrat   # must print "s VERIFIED UNSAT"
python3 $T/verify_cover_mono.py out/S8.cnf logs/cubes           # cover, recomputed hashes, recorded verdicts
# Theorem 2: sh $T/build_base.sh out2 mono2to14   (out2/BASE.cnf, SHA-256 ad8ef197...), cubes on Z_2..Z_14:
#   python3 $T/verify_cover_mono.py out2/BASE.cnf logs/cubes13 13 1
# controls
python3 $T/controls2.py 'fam/t{t}' <sets...>    # after: for t in 10 12 13 14 15; do sh $T/gen_families.sh $t fam/t$t; done
```

The recorded proofs are `<lb-k9oct-work-dir>/sat/cubes*/c_r/proof.lrat.zst`; `zstd -dc` restores the proof whose
SHA-256 is in `logs/cubes*/c_r/result.txt`.


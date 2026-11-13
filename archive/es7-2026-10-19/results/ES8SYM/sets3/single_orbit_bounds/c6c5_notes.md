# push2/c6c5: sixfold and fivefold octagon-free sets (K = 8), 2026-11-02

Working notes of the sixfold/fivefold search (2 November 2026); paths below are relative to that working directory.
Session 22:36-00:05 KST, at most 3 processes. Status words follow `$S/brief/COMMON.md`.

## 0. Headline

1. **Fivefold: a certified 56-point 5-fold symmetric set with no convex octagon** (11 nested regular pentagons plus
   the centre). This improves the previous certified 51 (S1, `c5_51pts_10layers_centre`). File:
   `cert/c5_56pts_11layers_centre.pts`. It is a **two-orbit rotated blow-up**: an outer pentagon carrying 6-point
   clusters and an inner pentagon (radius ratio 0.822, phase offset 19.25 deg) carrying 5-point clusters, plus the
   centre.
2. **Sixfold: no improvement on 54.** The obstruction for one family is now proved:
   **one orbit of tiny clusters (any cluster, Lemma 1) gives at most 9 points per cluster for m = 6, K = 8**,
   hence at most 54 points (computer-assisted: SAT relaxation, UNSAT at 10 points, LRAT proof accepted by
   lrat-check; the relaxation is satisfiable at 9 and a real 9-point cluster exists). For m = 5 the analogous bound
   is 10 points per cluster (51 points with the centre), with a two-line proof. So, within tiny-cluster blow-ups,
   more than 54 (6-fold) or 51 (5-fold) points need at least two base orbits (the 56-point set has two). The bound
   54 is attained by a single-orbit blow-up (certified, C6; a different order type from S1's 54-point set).
3. **Targets 60 (6-fold) and 60/61 (5-fold) not reached.** Multi-orbit searches (2 and 3 orbits; 145 annealing runs
   of 30-90 s, about 2.5 CPU-hours, plus 11 minutes of S1's `nest3`) found nothing; see sec. 4 for the best residuals. This is computational evidence only, not impossibility.

## 1. Claims

| id | statement | status | evidence |
|---|---|---|---|
| C1 | There is a 5-fold rotationally symmetric set of 56 points in general position with no 8 points in convex position (11 pentagon layers + centre). Hence the largest 5-fold octagon-free set has >= 56 points and L(5,8) >= 11. | certified | `cert/c5_56pts_11layers_centre.*`, log `cert/c5_56pts_11layers_centre.log`: (1) S1 `verify_config.py` (exact Z[zeta_5] arithmetic): distinct, invariant under zeta, no zero orientation, every layer is one orbit and contains the later ones, exact DP largest convex subset 7; (2) S1 `cvxcheck` on that table: DFS finds 0 convex 8-subsets (2,398,345 convex 7-subsets), coordinate-free DP 7; (3) primefold/theory `orient.py` (independent exact arithmetic, polynomial in 2cos(2pi/5) on a 2^-400 bracket) from the .pts file: table byte-identical to (1); theory `inv.c` DFS: max_convex 7, same k-subset counts, layers 5^11 1, rotation automorphism of order 5; (4) S1 `crosscheck_decimal.py`: all 27,720 signs recomputed with 160-digit decimals agree, min abs det 8.9e14 vs error bound 6e-126 |
| C2 | Blow-up formula tool for general K (`bu.c`): formula (1) of primefold/theory Lemma 1 over all convex sub-polygons of a multi-orbit base (+ centre), and the exact number of convex K-subsets in the eps -> 0 limit (sum over base polygons of products of chain counts) | validated (tool, not a claim about point sets) | 24 + 60 random 1-3 orbit configurations (`validate.py`, values 5..18): formula value = direct DP on the realized set (`realize.c`, eps 1e-6), 0 mismatches; the eps -> 0 counts 90 and 330 of two near-solutions equal S1 `nest3`'s float counts of the realized sets (eps 1e-3); chain-count formula 425 = exact count of convex 8-subsets of a realized 61-point configuration (S1 cvxcheck on an exact Z[zeta_5] table); C1 itself agrees (formula 7) |
| C3 | One orbit of tiny clusters, m = 6, K = 8 (base = regular hexagon, cluster C at each vertex, rotated copies; C generic in the sense of Lemma 1, i.e. no segment of C parallel to a chord of the hexagon, and eps small enough for formula (1)): if the blow-up has no convex 8-gon then |C| <= 9, so the set has <= 54 points. | proven, computer-assisted (UNSAT of a sound relaxation, LRAT checked) | `sat/clsat_full.py 6 8 10`: UNSAT, LRAT accepted by `lrat-check` (`sat/single_orbit_sat.log`, cnf sha256 4ef7a9a1..., lrat 9942f25f...); a tampered proof is rejected; n = 9 satisfiable and realized (54-point formula-level example `runs/m6n9.cfg`); faithfulness test: for 179 random real clusters the relaxation with the real bins/turns fixed is SAT iff the formula says "no 8-gon" (`sat/soundness_test.py`, 179/179) |
| C6 | C3 is tight: a single-orbit 6-fold blow-up with a 9-point cluster gives a 54-point 6-fold octagon-free set; it is not order-type equivalent to S1's 54-point set (convex 7-subsets 52,902 vs 70,134) | certified | `cert/c6_54pts_1orbit.*` (log): S1 `verify_config.py` (exact Z[zeta_6]) PASS, largest convex subset 7; `cvxcheck`: 0 convex 8-subsets, DP 7; `exact6.py` (own exact Eisenstein-integer orientation, integer determinant in the basis (1, zeta)): table identical to S1's, own DP 7; `crosscheck_decimal.py` PASS (min abs det 1.1e14, error bound 6e-126) |
| C4 | One orbit of tiny clusters, m = 5, K = 8 (centre optional; same genericity and eps assumptions as C3): |C| <= 10, so <= 51 points. | proven (hand proof, sec. 3); also UNSAT at 11 points with LRAT (`sat/single_orbit_sat.log`) | sec. 3 |
| C5 | Flat clusters (Valtr/Baek-Balko type, one orbit), m = 6, K = 8: |C| <= 9 | proven (special case of C3; direct hand argument in sec. 3) | sec. 3 |
| E1 | Searches for 6-fold 60 (two orbits: splits (6,4),(4,6),(5,5),(1,9),(7,3),(3,7) and the single-orbit 9-cluster plus a 1-point orbit; three orbits: (4,3,3),(3,4,3),(3,3,4)) | computational evidence only (search; failure is not impossibility) | sec. 4 |
| E2 | Searches for 5-fold 61 (centre) and 60 (no centre): two and three orbits, random starts and growth from C1 | computational evidence only | sec. 4 |
| E3 | Adding one more pentagon layer (1-point orbit) to C1 anywhere (outside, between the orbits, inside, with or without centre; 1,000+ radius/phase choices) leaves >= 720 convex 8-gons (eps -> 0 count) | computational evidence only | sec. 4 |
| A1 | An apparent 61-point solution of an early search was a floating-point artefact (absolute convexity tolerance in the base-polygon enumeration when the inner orbit shrank to radius 5e-7); the exact check rejected it (largest convex subset 10, layers not nested). Fixed (scale-free test, orbit radius ratio >= 0.01); the corrected formula gives 10, matching the exact check. | resolved | sec. 2 |

Not claimed: any upper bound for multi-orbit blow-ups or for general 5- or 6-fold sets; that 56 is optimal for
5-fold; novelty beyond the sources listed in S1 (no new literature search was done in this session).

## 2. Method

**Formula.** primefold/theory Lemma 1: for tiny clusters C_b at the points b of a base B in general position,
mc = max(max_b mc(C_b), max over convex B' (|B'| >= 2) of sum_b f_{C_b}(I_b(B'))), f_C(I) = longest ccw chain of C
with edge directions in the open arc I. A convex K-subset of the blow-up meets a convex set B' of clusters in ccw
chains with directions in the arcs I_b(B'), and conversely (same proof), so the number of convex K-subsets is
sum over B' of the coefficient of x^K in prod_b (sum_k N_b(k) x^k) plus the K-subsets inside single clusters
(N_b(k) = number of such chains with k points). `bu.c` evaluates both for a base made of orbits
r_l e^{i(psi_l + 2 pi j/m)} (+ centre) with arbitrary clusters (rotated copies), and anneals cluster coordinates and
orbit radii/phases with cost = total excess over K-1 (mode 0), log(1 + number of convex K-subsets) (mode 1), a
mix (mode 2), or mode 1 with the 8-gons of single-orbit base polygons weighted 50 (mode 3). Only directions matter (scale invariance), so clusters are free point sets.

**Realization and certification.** `realize.c` builds the explicit point set at cluster scale eps (float DP as a
sanity check) and writes the orbit representatives as (log radius, phase); `certify.sh` then runs the four exact
checks listed in C1 (exact points in Z[zeta_m] from S1's `verify_config.py`, rounding at scale 1.22e11; for m = 6
the theory `orient.py` does not apply and `exact6.py` replaces it, as in C6).

**Artefact A1.** The first version enumerated convex base polygons with an absolute tolerance 1e-12 on cross
products. The annealer shrank one orbit to radius 4.9e-7, which silently dropped all polygons inside it, and
reported a "61-point" configuration. Exact certification failed (largest convex subset 10). After the fix the
formula gives 10 for that configuration too. All results above were obtained with the fixed code.

## 3. Proofs

**Setting.** One orbit: base = regular m-gon L = {v_j}, cluster at v_j = R^j(C) (C in the frame of v_0: radial,
tangential), S = union of v_j + eps R^j C (+ centre for odd m), eps small; K = 8. A vertex with gaps a (before) and
b (after) along L (units 2 pi/m) has the turning arc (-a, b) in units pi/m measured from the ccw tangent, so a
base polygon with cyclic gaps (g_1, ..., g_r) (r >= 2, sum m) contributes sum_i F(g_i, g_{i+1}) with
F(a, b) = f_C((-a, b)) (primefold/theory Prop. C proof).

**C4 (m = 5).** The full pentagon gives 5 F(1,1) <= 7, so F(1,1) = 1: no segment of C has direction within pi/5
of the tangent. Sort C by the radial coordinate; every forward segment has direction t in (1, 4). The 2-gon
{v_0, v_1} (gaps 4 and 1) gives F(4,1) + F(1,4) <= 7, and F(1,4) = g(4) = longest cup, F(4,1) = h(4) = longest cap
(all forward directions lie in (0,4), all backward ones in (-4,0)). By the Erdos-Szekeres cup-cap theorem
|C| <= C(c+d-2, c-1) <= max_{c+d=7} C(5, c-1) = 10. (The same argument gives |C| <= 10 for m = 6.)

**C3 (m = 6), relaxation.** Again F(1,1) = 1 (6 F(1,1) <= 7), so C can be sorted radially and every forward
direction t_ij lies in (1, 5). A ccw chain with directions in (-a, b) consists of an outward part followed by an
inward part meeting at their common outermost point p; read in radial order it is a cap starting at p with all
t > m - a plus a cup starting at p with all t < b. Hence F(a,b) = max_p [capS_p(m-a) + cupS_p(b) - 1].
`sat/clsat_full.py` encodes: order-encoded bins floor(t_ij) in {1..4}; turn variables (left turn iff
t_ij < t_jk); the mediant facts (t_ik strictly between t_ij and t_jk, and on the correct side for left/right
turns); cup/cap variables per start point p and last edge (forcing implications only); "capS_p(y) >= l",
"cupS_p(x) >= l"; "F(a,b) >= v" forced by every pair (p, l1, l2) with l1 + l2 - 1 = v; and, for every composition of
6 into r >= 2 parts and every (v_1..v_r) with sum 8, the clause "not all F(g_i, g_{i+1}) >= v_i". Every clause holds
for the true values of a real admissible cluster, so UNSAT at n = 10 proves C3. Checks: n = 10 UNSAT with LRAT
verified; n = 9 SAT; fixing the bins/turns of a real valid 9-point cluster stays SAT; 179 random real clusters:
SAT-with-fixed-geometry iff formula value <= 7 (so the encoding is also faithful, not only sound). For m = 5 the
same encoder gives n = 11 UNSAT (LRAT verified), n = 10 SAT, 86/86 faithfulness agreements.

**C5 (flat clusters, direct).** For a flat cluster (largest cup c >= 2, cap d >= 2, flattening angle beta,
x = (m/pi)(beta + pi/2) non-integer, y = 6 - x) a vertex gets weight c iff its preceding gap exceeds y and d iff its
following gap exceeds x, else 1 (primefold/theory Thm A proof). The full hexagon forces 1 < x < 5 (else all six
weights are >= 2). The polygon of s + 1 consecutive vertices gives s + 1 + (c-1)[s < x] + (d-1)[s < y] <= 7; s = 1
gives c + d <= 7, so |C| <= C(c+d-2, c-1) <= 10 with equality only for {c, d} = {3, 4}.
(c,d) = (3,4): s = 2 forbids x > 2 and y > 2 together; s = 4 forbids y > 4 (5 + 3 = 8); so x > 2, hence x > 4 and
y < 2. Then every vertex of the polygon with gaps (2,2,2) has preceding gap 2 > y: total 3c = 9 > 7.
(c,d) = (4,3): s = 4 forbids x > 4; s = 2 then forces x < 2; every vertex of (2,2,2) has following gap 2 > x:
total 3d = 9 > 7. So a flat single-orbit cluster has <= 9 points (consistent with C3).

## 4. Searches (float; heuristic; nothing here is a claim)

All searches anneal `bu.c` configurations (cluster coordinates, orbit radii and phases; outer orbit radius 1, inner
radii >= 0.01 times the next outer one after the fix of A1). Drivers: `driver.py` (random starts, cycling through
cluster-size splits, outermost orbit first), `seed_driver.py` (growth from the 56-point solution: one more cluster
point or one more 1-point orbit, optionally without the centre), `seed19.py` (6-fold: the single-orbit 9-point
cluster plus one 1-point orbit). Per run 30-90 s. Logs `runs/drv_*.log`, `runs/sdrv_*.log`, `runs/seed19.log`;
best configurations per split `runs/best_*.cfg`, `runs/sbest_*.cfg`; summary `python3 summarize.py`.
Values: mode 0 = total excess over 7 (a class of m rotated copies counts m), mode 1 = log(1 + N8) with N8 the number
of convex 8-subsets in the eps -> 0 limit, mode 2 = excess + 0.05 log(1 + N8).

| target | family | runs | best |
|---|---|---|---|
| 5-fold 56 (centre) | two orbits (6,5) | 1 | **found in 5.5 s (excess mode), certified (C1)** |
| 5-fold 61 (centre) | two orbits (6,6), (7,5), (5,7); three orbits (4,4,4), (6,4,2), (6,5,1); growth from C1 | 39 | N8 = 400 (one rotation class of excess, (7,5)) |
| 5-fold 60 (no centre) | (6,6), (7,5), (5,7), (8,4), (4,8), (4,4,4); growth from C1 minus centre | 49 | N8 = 330 ((6,6), one class: excess 5) |
| 5-fold 61 | S1 `nest3` (float-count annealer on layer coordinates) from C1's 11 layers + 1 random layer | 420 s, 2 restarts | 770 convex 8-gons |
| 6-fold 54 | one orbit, 9-point cluster | 1 | found in 3.6 s (formula level, `runs/m6n9.cfg`; matches C3) |
| 6-fold 60 | one orbit, 10-point cluster | 6 | always stuck at the adjacent 2-gon (cup + cap = 8); now proved impossible (C3) |
| 6-fold 60 | two orbits (6,4), (4,6), (5,5), (1,9), (7,3), (3,7) (modes 0-3), and 9-cluster + 1-point orbit | ~50 | N8 = 90 for (6,4) (reached twice from different seeds; residual = adjacent 2-gon of the outer orbit, whose 6-point cluster became a 6-cap: cup + cap = 8) |
| 6-fold 60 | three orbits (4,3,3), (3,4,3), (3,3,4) | 4 | N8 >= 1,500 |
| 6-fold 60 | S1 `nest3` from the (6,4) near-solution realized at eps = 1e-3 (N8 = 90 there too) | 240 s, 3 restarts | 90, no improvement |

The same residual values recur from independent random starts and in different cost modes (N8 = 400 for 5-fold
(7,5) + centre in five runs, N8 = 90 for 6-fold (6,4) twice, 6-fold (4,6) value 6.871 three times): strong
attractors of these families rather than lack of iterations.
Realizing the near-solutions at larger eps (3e-3 .. 3e-2) only increases the number of convex 8-gons (and for the
5-fold one the layers stop being nested), so the tiny-cluster limit is the best point of these families.
Adding one pentagon layer to C1 anywhere (E3) leaves >= 720 convex 8-gons: C1 is saturated for one-layer growth.
Calibration caveat: the 56-point set was found within seconds, the 61/60 targets not in about 2.5 CPU-hours; the
earlier S1 annealer (layer coordinates, exact counts) had reached only 51 for 5-fold. This says nothing about
existence.

## 5. Files

- `bu.c` (+ `bu_v1.c`, first version with the artefact A1): evaluator/annealer. `realize.c`: explicit realization.
  `validate.py`: formula vs direct DP. `exact6.py`: independent exact checker for Z[zeta_6] point files.
- `certify.sh`: exact certification pipeline (m = 5). `cert/`: the 56-point certificate C1 (`.blowup.cfg`
  construction parameters, `.layers` orbit representatives, `.pts` exact points, `.orient.gz` S1 table, `.ot`
  theory table, `.log` all checks with SHA-256) and the single-orbit 54-point 6-fold set C6 (`c6_54pts_1orbit.*`).
- `SHA256SUMS.txt`: hashes of the point files, configurations, CNFs, LRAT proofs and main tools.
- `polish/`: S1 `nest3` runs (layer files realized from near-solutions, outputs).
- `val/v75.*`: the realized 61-point (7,5)+centre configuration used to validate the chain-count formula (exact S1
  table; cvxcheck: 425 convex 8-subsets, none of size 9; formula: 425).
- `driver.py`, `seed_driver.py`, `seed19.py`: search drivers; `runs/`: logs and best configurations;
  `summarize.py`: best value per log and split.
- `analyze.py`: cluster description (direction bins).
- `sat/clsat_full.py` (single-orbit relaxation, all compositions), `sat/run_single_orbit_sat.sh`,
  `sat/single_orbit_sat.log`, `sat/f_m6n10.{cnf,lrat}`, `sat/f_m5n11.{cnf,lrat}`, `sat/soundness_test.py`,
  `sat/clsat_k.py` (primefold clsat2 generalized to K, weaker: only the consecutive-vertex compositions; SAT at
  m = 6, n = 10, so it does not prove C3).

Reproduce C1: `./certify.sh cert/c5_56pts_11layers_centre.blowup.cfg 5 1 8 1e-3 NAME` (writes `cert/NAME.*`).
Reproduce C3: `sat/run_single_orbit_sat.sh`.

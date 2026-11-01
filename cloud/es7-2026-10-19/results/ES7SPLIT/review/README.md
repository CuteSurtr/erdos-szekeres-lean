# Independent review of ES7SPLIT (1 November 2026)

**The review.** Seven independent checks, one per claim, each run separately from the work it checks and from the
other checks. Each was given the claim, its written proof and the files it cites, and was asked to find errors. Each
wrote its own exact-arithmetic code (integers and fractions). None imports `../tools/`, except one re-run noted in §5
and two comparison runs noted in §7. The only solver used was CaDiCaL 3.0.1 (§7); the Lean file of §2 was compiled
with the repository's Lean build.

**Verdict.** No claim was refuted and no mathematical error was found. The remarks below were taken into the main
`../README.md` and the proof files.

| claim | directory | result | label after the check |
|---|---|---|---|
| Theorem 5 (split theorem) | `split_theorem/` | not refuted | written proof (reviewed) |
| Theorem 6 (equivalence with ETV(7,5,7)) | `equivalence/` | not refuted | written proof (reviewed) |
| Corollary 7 (general k) | `general_k/` | not refuted | written proof (reviewed) |
| Proposition 8 (hull vertices and hexagons) | `hull_vertex_hexagon/` | not refuted | written proof (reviewed) |
| the 27-point witness | `witness27/` | not refuted | exact computation |
| hexagon chord lemma | `chord_lemma/` | not refuted | written proof (reviewed) |
| z-splits of the example sets | `example_set_splits/` | not refuted | exact computation |

The walk-sample statistics (main README §6) had no check of their own. The chord-lemma check re-ran all 216 order
types with its own code (§6 below).

## 1. Theorem 5 (`split_theorem/`)

- **By hand.** Lemma 0 (items (b), (c), (d) and the direction case), Lemma 0′, Lemmas 2 and 3, Corollary 4 and the
  case table. Lemma 2 also follows straight from the definitions, without the normal form.
- **Baek's theorem.** Published (Eur. J. Combin. 124 (2025) 104085). The repository's Lean theorem `main`
  (`ErdosSzekeres/Vendor/ETV/Main/Main.lean`) is stated for abstract configurations. The repository's bridge to real
  point sets covers the octagon case only. So for n = 7 the geometric statement rests on the published paper. That is
  enough for a written proof, not for "Lean-checked".
- **Lemmas 2, 3 and Corollary 4** (`test_lemmas_ind.py`, `igeom.py`). 2,840 random z-splits from three generators:
  finite z by rejection sampling, random directions, and z close to the points. Brute force over all subsets:
  0 violations (`log_lemmas_seed11.txt`, `log_lemmas_seed12.txt`).
- **The normal-form map** (`test_phi_ind.py`). 600 trials with an arbitrary separating vector, planted ties and
  directions: 0 violations (`log_phi_seed5.txt`).
- **Example sets** (`gon_ind.py`, `splits_ind.py`). Classical, mirror, central and the witness: general position,
  largest convex subset 6 (`log_gon_examples.txt`). Split enumeration by exact half-plane clipping, no LP: the same 6
  splits of the classical set, none in the mirror, central and five symmetric sets, 4 in the witness
  (`log_splits_examples.txt`).
- **Smaller k, where all needed ETV values are known.**
  - k = 5 (`test_k_analogue.py`): 300 random 8-point pentagon-free sets, 44 splits, all of the predicted type
    (4, 4, 2, 2) (`log_k5.txt`).
  - k = 6 (`test_k6_walk.py`, with Baek's N(6,4,6) = 11): 510 visited 16-point hexagon-free sets, 1,144 splits, all of
    type (5, 11, 2, 3) or (11, 5, 3, 2) (`log_k6_walk_seed1.txt`, `log_k6_walk_more.txt`).
  - k = 7: a walk from the classical set that moves one point per step (40 visited sets) finds splits only at the
    start, all of the predicted types (`log_k7_walk.txt`).
- **Witness.** Its hull vertex (0, 0) lies on no convex hexagon; the other four hull vertices do (`check_prop8b.py`,
  `log_prop8b.txt`).
- **Remarks.** "Lean-formalized" applies to the abstract form of Baek's theorem only. Lemma 0′ calls "z outside
  conv(S)" a finite set of strict inequalities; it is an open condition, which is all the argument needs. Novelty was
  not assessed.

## 2. Theorem 6 (`equivalence/`)

- **By hand.** Every step, including the line formula y = −M − ε(t_i + t_j)x + εt_it_j of the gluing and the
  finiteness of the bad values of M.
- **Lemmas 2, 3 and Corollary 4 from the definitions** (`direct_lemmas.py`, no normal form). 29,820 nontrivial splits,
  19,179 of them with finite z, 133 distinct types: 0 failures (`direct_lemmas_seed2.txt`, `direct_lemmas_seed3.txt`).
- **Ties across the parts** (`coverage_zline.py`). 4,781 nontrivial splits whose finite z lies on a line through a
  point of A and a point of B: 0 failures (`coverage_zline.txt`).
- **The map φ** (`lemma0_exact.py`). 1,500 trials, 614 of them with z on a line through two points: 226,926
  orientation triples, 48,246 order pairs, 110,979 side tests and 88,724 partitions, 0 violations
  (`lemma0_exact_seed7.txt`).
- **The gluing on 26 points** (`gluing_check.py`, `geomdp.py`, `gluing_check.txt`). The 26 leftmost points of the
  classical set have no 5-cap and largest convex subset 6, so N(7,5,7) ≥ 26 by exact computation. With
  B₀ = {(t_j, −M − t_j²)} and M ∈ {10, 100, 1000, 3000, 10⁴, 10⁵, 10⁶}: for M = 3000, 10⁴, 10⁵ and 10⁶ the split
  conditions hold, the set is in general position and its largest convex subset is 6; for M = 10, 100 and 1000 the
  split fails and the largest convex subset has 10, 9 and 9 points.
- **Lean** (`BaekSeven.lean`, `BaekSeven.out`). Baek's abstract theorem at n = 7: 17 elements of an abstract
  configuration contain a 4-cap or a 7-gon. Compiled against the repository's port; axioms `propext`,
  `Classical.choice`, `Quot.sound`. Lean-checked (abstract form only).
- **Remarks.**
  1. The equivalent form "some 27 points with distinct x-coordinates have no 5-cap and no 7-gon" needs "in general
     position": 27 collinear points would satisfy it trivially. The main README states it with general position.
  2. Direction 2 ⇒ 1 is classical. Direction 1 ⇒ 2 is a short combination of the classical cap–cup mechanism with
     Baek's theorem.
  3. Both sides of the equivalence are believed false (ES(7) = 33 is conjectured), so the theorem prunes little.

## 3. Corollary 7 (`general_k/`)

- **By hand.** Every step. Only Lemma 0 and Lemma 3 (through c + d ≤ gon(S)) are needed; Lemma 2 and Lemma 0′ are not.
- **Arithmetic** (`arith_check.py`, `arith_check.out`, exact integers). For all k ≤ 120 and all c, d ≥ 2 with
  c + d ≤ k − 1, the two ETV bounds add up to at most 2^(k−2), with equality exactly when c + d = k − 1. The values
  needed are a = 3, …, k − 2; beyond Baek's theorem: {5} for k = 7 and {5, 6} for k = 8.
- **Lemmas 2, 3 and Corollary 4** (`lemma_test.py`, `lemma_test_big.py`). 1,900 splits generated from Definition 1,
  half with finite z and half with directions, up to 14 points: 0 violations in about 760,000 checks of each lemma
  (`lemma_test_seed2.out`, `lemma_test_big.out`).
- **The map φ** on 400 finite-z splits: 0 violations (`lemma0_test.py`, `lemma0_test.out`).
- **Remarks.**
  1. General position is needed. Two parallel rows of 5 points form a z-split of 10 > 8 points with no 5 points in
     strictly convex position (`nongp_example.py`, `nongp_example.out`).
  2. The statement is vacuous for k ≤ 6 (ES(5) = 9, ES(6) = 17) and conditional for k ≥ 7.
  3. The written proof is a short sketch that refers back to Theorem 5. Every step is either independent of k or
     written out.
  4. "Only a = 5 open for k = 7, a = 5, 6 for k = 8" matches `docs/RELATED_WORK_2026-10-14.md`. It was not checked
     beyond that note.

## 4. Proposition 8 (`hull_vertex_hexagon/`)

- **By hand.** Proposition 8 and the lemmas it uses. Lemma 0(d) already follows from (b) and (c). The frame lemma
  (Y ∪ {v} is convex iff Y is a v-cap) is correct. N(7,5,7) ≤ 56 = C(8,3) by the cups–caps theorem.
- **The witness** (`check_witness.py`, `logs_check_witness.txt`). General position; 0 of 888,030 7-subsets convex;
  v = (0, 0) is a vertex of a 5-point hull; 0 of 65,780 6-subsets through v are convex (two convexity tests); the
  largest convex set through v has 5 points; the largest v-cap has 4; the frame lemma holds on all 83,655 subsets
  tested.
- **An explicit 26-point set for N(7,5,7) ≥ 26**, independent of the ETV paper: φ applied to the witness minus v gives
  26 points with distinct x-coordinates, in general position, with no 5-cap (2,001 4-caps) and largest convex subset 6.
  The construction of Proposition 8(b) applied to it gives 27 points, largest convex subset 6, the new point a hull
  vertex on no convex hexagon.
- **Random tests** (`test_equiv.py`, `logs_test_equiv.txt`). 3 seeds × 300 sets of 6–11 points, 5,408 hull vertices,
  about 1.93 million subset checks of the frame lemma: 0 violations. The k = 5 analogue, with N(5,3,5) = 4, also
  passes.
- **Spot check** (`spot32.py`, `logs_spot32.txt`). Every hull vertex of the classical, mirror and central sets has a
  v-cap of 5 points.
- **Remark.** The wording of the claim as submitted omitted general position; the proof file assumes it.

## 5. The 27-point witness (`witness27/`)

- **Independence.** The dynamic program in `../tools/geom.py` re-types the repository's own program, so it is not an
  independent check. It was replaced by exhaustive enumeration with three convexity tests:
  - method A (`brute.c`, C with 128-bit integers): no point inside a triangle of three others;
  - method B (`verify_witness.py`, numpy over an exact sign table): counting hull edges;
  - method C (`verify_witness.py`, pure Python): angular sort around b and strict left turns.
- **Results** (`brute_witness27.log`, `verify_witness27.log`). 27 distinct points in general position. 0 of 888,030
  7-subsets convex; 9,632 convex hexagons. b = (0, 0) is a hull vertex. 0 of the 65,780 6-subsets through b are convex,
  by all three methods; 2,001 convex pentagons pass through b. Layer profile (5, 6, 5, 6, 4, 1).
- **Controls** (`controls.py`, `controls.log`). On the 10 points (i, i²), methods A and B count every subset as
  convex. On 40 random sets of 14–18 points they agree on all counts, including 24,385 convex 7-subsets.
- **Provenance** (`verify_split.py`, `verify_split.log`, `brute_classical32.log`).
  - `../data/classical32.txt` equals the output of `scripts/es_lower_bound_witness.py 7 --json`
    (`classical_regen.json`).
  - The witness is classical[6..31] followed by classical[0].
  - With A = classical[6..31], B = classical[0..5] and z = (−290/3141, 1000290/3141), conditions (S1) and (S2) hold
    exactly and z is outside the hull. A has 2,001 z-4-caps and no z-5-cap. B has no z-cup triple: it is a z-6-cap.
  - In the full classical set (largest convex subset 6), (0, 0) lies on 10,006 convex hexagons.
- **Re-run of the original tool** (`geom_repro.log`). `../tools/geom.py` on the witness prints
  `27 True 6 [5, 6, 5, 6, 4, 1]`, as in `../logs/prop8b_witness.txt`.
- **Remarks.** The code that wrote the witness had been run inline and not saved; it is now
  `../tools/make_witness27.py`, and a re-run reproduces the file byte for byte. The witness shows the property failing
  at 27 points. That is N(7,5,7) + 1 only if N(7,5,7) = 26. The first version of method C had an indexing bug; it was
  fixed and re-run, with the same result. The check ran on `witness27_copy.txt` (not included here), a byte copy of
  `../data/prop8b_witness27.txt` (SHA-256 `a888c6b2…`).

## 6. The hexagon chord lemma (`chord_lemma/`)

- **By hand.** The proof line by line: the 7-vertex polygon formed by the two convex pieces, the turns at a and b, the
  case m = 3, and the nesting and region description of the corollary.
- **Exhaustive check** (`chordcheck.c`). All convex subsets are enumerated by brute force, without a dynamic program.
  For every convex hexagon and every i and m it computes the longest chain beyond the chord (cross-checked by brute
  force), the region equality of the corollary, pairwise nesting, and visibility around 6-holes.
  - Classical, mirror and central sets: 39,648, 23,184 and 27,055 convex hexagons; 0 convex 7-sets; the longest chain
    is exactly m; 0 violations (`exhaustive_32.txt`).
  - The 3-fold 27, 30, 31, 4-fold 28 and 6-fold 30 sets and the witness: the same (`exhaustive_other.txt`).
  - All 216 walk order types (`walks_driver.py`, brute-force cross-check on every 25th hexagon): 3,545,557 convex
    hexagons, 26,760 6-holes, 0 violations; hull sizes {3: 40, 4: 127, 5: 45, 6: 4}, as in `../logs/walks_summary.txt`;
    all hexagonal-hull ears nested (`walks_check.txt`).
- **Geometric steps on arbitrary configurations** (`universal_test.py`, `universal_test_log.txt`). Seeds 11–13, 30,000
  trials each: 497,212 checks of the core implication, 16,199,850 of the region description, 399,533 of
  "one visible edge gives a convex 7-gon", 917,827 of the nesting criterion and 2,334,501 of edge contiguity;
  0 violations.
- **Mutation control** (`control_test.py`, `control_test_log.txt`). Dropping the edge-line condition at a, or at b,
  gives 14,158 and 21,052 violations, so the test detects errors.
- **Remarks.** (i) General position is assumed; the "interior of the triangle" form of nesting needs it. (ii) The
  control in `../tools/test_chord_lemma.py` "reaches m + 2" because that is the cap of its search loop, not a measured
  maximum; the proof file now says so. (iii) The Heule–Scheucher citation is motivation only; the paper was not opened.

## 7. z-splits of the example sets (`example_set_splits/`)

- **Inputs.** The data files equal the repository originals; `classical32.txt` equals a fresh run of
  `scripts/es_lower_bound_witness.py 7` and an own re-implementation of the construction. All sets are in general
  position. The 3-fold and 6-fold files use Eisenstein coordinates; the map to the plane is linear with positive
  determinant, so the results transfer. The check read byte copies of the files now in `../data/` (directory
  `inputs/`, not included here; same SHA-256).
- **Completeness without Lemma 4′.** One-sidedness (every pair of A sees all of B strictly on one side, and the same
  for B) is necessary for a split. All partitions with |A|, |B| ≥ 2 that satisfy it were enumerated by two methods
  that do not use the linear-partition argument: CaDiCaL with blocking clauses (`indep_splits.py`) and a solver-free
  backtracking search (`backtrack_onesided.py`). Both were first compared with brute force over all 2^n partitions on
  99 small sets: exact agreement on 298 partitions (`validate_enumerators.py`, `validation.log`).
- **Results** (`indep_summary.log`, `indep_results_classical.json`, `indep_results_symmetric.json`,
  `backtrack_onesided.log`). Classical set: exactly 6, the block boundaries 6 | 26, 16 | 16 and 26 | 6, each with both
  choices of upper part. Mirror, central, 3-fold 31, 30, 27, 6-fold 30 and 4-fold 28: 0. The counts of ordered linear
  partitions, 980, 980, 984, 918, 858, 696, 858 and 748, match `../logs/split_exactness.txt`.
- **Witnesses.** The review's own witnesses and the six printed by `../tools/splits.py` (`splits_rerun.log`,
  `check_witnesses.py`, `check_witnesses.log`) were verified exactly. Vertical directions do not work for these
  splits; the valid z are tilted.
- **Types.** Brute force over subsets with the all-triples definitions: (26, 6, 4, 2) ×2, (16, 16, 3, 3) ×2,
  (6, 26, 2, 4) ×2. The type does not depend on the choice of z; this was also checked by a z-free computation.
- **Robustness** (`variants.py`, `variants.log`). 15 realizations of the classical construction, with coordinates up
  to about 2.6 · 10^37: the same order type, and all 6 splits admit an exact z.
- **Fivefold sets** (`fivefold_check.py`, `fivefold_check.log`, exact arithmetic in Q(√5)). The 5-fold 30- and
  31-point sets have no one-sided partition.
- **Comparison runs.** `crosscheck_zneg2.py` and `splits_rerun.log` call `../tools/splits.py` on purpose, to compare it
  with the review's own exact procedure (`exact_z.py`).
- **Remarks.**
  1. "At the ETV bounds" means Baek's bound 16 and, for 26, the ETV construction value, that is the conjectured
     N(7,5,7) = 26, not a proven bound.
  2. "Exactly 6" counts ordered splits: 3 partitions, each with both choices of upper part.
  3. One-sidedness alone already forces the two hulls to be disjoint.
  4. One-sidedness does not imply that a z exists in general (31 of the 298 small partitions have none), but for the
     claimed sets every negative was decided by one-sidedness. `../tools/splits.py` reports badly scaled cases as
     "numeric-only" (20 in the small tests) and never rejects them silently; its numeric-only count is 0 for every
     claimed set.

## Reproduction

From `cloud/es7-2026-10-19/results`. Needs Python 3, a C compiler, numpy for `verify_witness.py` and `controls.py`,
numpy and scipy for `indep_splits.py` and `crosscheck_zneg2.py`, and CaDiCaL for `indep_splits.py` and
`validate_enumerators.py`. The Lean file is compiled from the repository root with the repository's Lean build.

```sh
R=ES7SPLIT/review; D=ES7SPLIT/data
# 1. Theorem 5
python3 $R/split_theorem/test_lemmas_ind.py 11 1500        # also seed 12
python3 $R/split_theorem/test_phi_ind.py 5 600
python3 $R/split_theorem/gon_ind.py $D/classical32.txt $D/mirror32.txt $D/central32.txt $D/prop8b_witness27.txt
python3 $R/split_theorem/splits_ind.py $D/classical32.txt $D/mirror32.txt $D/central32.txt $D/c3_31points.txt \
  $D/c3_30points.txt $D/c6_30points.txt $D/c4_28points.txt $D/c3_27points.txt $D/prop8b_witness27.txt
python3 $R/split_theorem/test_k_analogue.py 5 300 1
for s in 2 3 4; do python3 $R/split_theorem/test_k6_walk.py k6 $s 150 | tail -1; done
python3 $R/split_theorem/test_k6_walk.py k7 7 40 $D/classical32.txt
python3 $R/split_theorem/check_prop8b.py $D/prop8b_witness27.txt
# 2. Theorem 6
python3 $R/equivalence/direct_lemmas.py 2 3000              # also seed 3
python3 $R/equivalence/coverage_zline.py 99
python3 $R/equivalence/lemma0_exact.py 7 1500
python3 $R/equivalence/gluing_check.py $D/classical32.txt
(cd ../../.. && lake env lean cloud/es7-2026-10-19/results/$R/equivalence/BaekSeven.lean)
# 3. Corollary 7 (the scripts import each other; run them from their directory)
(cd $R/general_k && python3 arith_check.py && python3 lemma_test.py 2 1500 && python3 lemma_test_big.py 11 400 \
  && python3 lemma0_test.py 7 400 && python3 nongp_example.py)
# 4. Proposition 8
python3 $R/hull_vertex_hexagon/check_witness.py $D/prop8b_witness27.txt
for s in 2026 7 31337; do python3 $R/hull_vertex_hexagon/test_equiv.py $s 300; done
python3 $R/hull_vertex_hexagon/spot32.py $D/classical32.txt $D/mirror32.txt $D/central32.txt $D/prop8b_witness27.txt
# 5. The witness (controls.py calls ./brute next to it)
cc -O2 -o $R/witness27/brute $R/witness27/brute.c
$R/witness27/brute $D/prop8b_witness27.txt; $R/witness27/brute $D/classical32.txt 0
python3 $R/witness27/verify_witness.py $D/prop8b_witness27.txt
python3 $R/witness27/controls.py
python3 $R/witness27/verify_split.py $D/classical32.txt $D/prop8b_witness27.txt $R/witness27/classical_regen.json
# 6. Chord lemma
cc -O2 -o $R/chord_lemma/chordcheck $R/chord_lemma/chordcheck.c
for f in classical32 mirror32 central32; do
  python3 $R/chord_lemma/tostdin.py $D/$f.txt | $R/chord_lemma/chordcheck --every 1; done
python3 $R/chord_lemma/walks_driver.py $R/chord_lemma/chordcheck 25 $D/walks/walk_*.txt
for s in 11 12 13; do python3 $R/chord_lemma/universal_test.py $s 30000 | tail -1; done
python3 $R/chord_lemma/control_test.py $R/chord_lemma/universal_test.py drop_a    # and drop_b
# 7. Example-set splits (CADICAL names the solver binary; indep_splits.py writes indep_results.json next to itself)
X=$R/example_set_splits
CADICAL=cadical python3 $X/indep_splits.py $D/classical32.txt
python3 $X/backtrack_onesided.py $D/classical32.txt $D/mirror32.txt $D/central32.txt $D/c3_31points.txt \
  $D/c3_30points.txt $D/c3_27points.txt $D/c6_30points.txt $D/c4_28points.txt
CADICAL=cadical python3 $X/validate_enumerators.py; python3 $X/crosscheck_zneg2.py ES7SPLIT/tools
python3 $X/check_witnesses.py $D/classical32.txt
python3 $X/variants.py $D/classical32.txt
python3 $X/fivefold_check.py $D/c5_31points.txt $D/c5_30points.txt
```

`log_k6_walk_seed1.txt` was written before the move scales in `test_k6_walk.py` were widened; the other walk logs
used the file as it is here. The `.time` files are `/usr/bin/time -l` outputs of the runs.

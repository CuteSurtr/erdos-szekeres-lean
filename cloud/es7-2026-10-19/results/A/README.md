# Task A: realizable-anchored abstract extension (19 October 2026)

**Outcome: no 33-point heptagon-free set was found, and no SAT answer was found at 33 points.**
Every abstract extension instance that finished was UNSAT. These are solver answers about specific
CNFs. They are not theorems. A random sample of 100 was re-checked with DRAT proofs, and nothing
else was proof-checked.

## Setup

- **Machine.** The run used the local Apple M5 Pro laptop, not a cloud VM. It has 15 logical
  CPUs (5 performance and 10 efficiency cores), and every pool used 15 worker processes. Other
  agents' jobs shared the machine the whole time, with a load average of 80–140. All wall times
  are therefore inflated, and conflict counts are the better measure of difficulty.
- **Solver.** CaDiCaL 3.0.1, commit `c607304`, built from GitHub as both a library and a binary.
  The link step needed `SDKROOT=MacOSX26.5.sdk`.
- **Proof checker.** drat-trim is the existing local build; it was not rebuilt.
- **Base CNFs.** These are `tools/trackB/gen_cnf.py N 7` with no symmetry breaking:
  - N = 33: 47,002 variables and 679,038 clauses;
  - N = 32: 42,666 variables and 597,524 clauses.
- **Tester.** `scripts/ext_solve.cpp` loads a base CNF once and freezes the X variables. Each job
  fixes every old triple through assumptions only, so learned clauses remain valid for later jobs.
  It uses the `ext_cnf.py` index map: old point a goes to the a-th index of 1..M other than the
  new ones.
  - A SAT answer prints the full model. The tool aborts if the model disagrees with an assumption.
  - The `lucky=0` option (CaDiCaL's pre-solve "lucky" checks) cut the time per call by about 4x
    without changing any answer. It was used for every run except part 1 of the main run.

## 1. Conversion (`scripts/convert.py`, `scripts/brute_all.py`)

- **Input.** 8,537 pool sets, all integer and exact.
- **Shear.** 1,492 sets repeat an x-coordinate. They got the exact shear (x, y) → (Lx + y, y)
  with L = 2·max|y| + 1. Its determinant is L > 0, so it changes no orientation and makes every x
  distinct.
- **Signotopes.** Points were sorted by x, and every one of the C(32,3) = 4,960 triple
  orientations was computed with Python integers. No triple was collinear.
- **Brute-force check.** The unchanged `tools/trackB/brute_kgon.c` checked all 8,537 signotopes:
  - signotope-axiom violations: 0;
  - convex 7-subsets: 0, out of 3,365,856 seven-point subsets per set.
- **AlphaEvolve.** The exact recount of `alphaevolve_pts.json` (decimals read as exact
  fractions) finds exactly one convex 7-gon, at JSON indices {14, 15, 17, 20, 23, 25, 32}.
  Deleting each of its vertices gives 7 sets of 32 points, and brute force confirms all 7 are
  heptagon-free.
- **Extra near-full sets.** The 273 sets in `nearfull_p2c/p2d` have 33 points and exactly one
  convex 7-gon each. Deleting a heptagon vertex gives 1,911 sets of 32 points:
  - 1,792 have the same signotope as a pool set;
  - 33 duplicate each other;
  - **86 are new**, and these were also tested.

## 2. Controls (`scripts/controls.py`, `data/controls.json`): all passed

| Control | What was checked | Result |
|---|---|---|
| C1, required positive | 30 pool sets spread evenly across the files, one seeded-random point q deleted. The 31-point signotope was extended with the 32-point base CNF at p = 1..32. | Position q was SAT in **30/30**. 369 of the 960 answers were SAT, and all 369 models passed brute force (old triples as fixed, signotope axioms, 0 convex 7-subsets). |
| C2, positive | All 8,544 heptagon-free 32-point signotopes (pool plus AlphaEvolve-derived), every triple fixed, in the 32-point CNF. | 8,544/8,544 SAT. The encoding accepts every known example. |
| C3, required negative | The 274 corrupted signotopes with a convex 7-gon (273 near-full sets plus AlphaEvolve's 33-point set), every triple fixed, in the 33-point CNF. | 274/274 UNSAT. brute_kgon finds exactly 1 convex 7-subset in each. |
| C3, negative | 3 AlphaEvolve 32-point sets that keep the 7-gon, all 33 extension positions. | 99/99 UNSAT. |
| C3, negative | Pool set 0 with triple (1,2,4) flipped. | brute_kgon reports 1 axiom violation, and the solver returns UNSAT. |
| Independent re-check | 100 random (set, p) pairs from the main run, rebuilt with the repository's `ext_cnf.py` (an independently written index map), solved by the stand-alone CaDiCaL binary, proof checked with drat-trim. 5 C1 own-position cases rebuilt the same way. | **100/100 UNSAT, all DRAT-verified.** The 5 C1 cases were 5/5 SAT. |
| Independent re-check, neighbourhoods | 20 random r = 4 and 20 random r = 5 neighbourhood jobs. The map was recomputed in Python from the label, the CNF was rebuilt as the base plus unit clauses, solved by the stand-alone binary, and proof checked with drat-trim (`scripts/cert_nbhd.py`). | 20/20 and 20/20: maps identical, UNSAT, DRAT-verified. |

## 3. One-point extension: every set and every position (`data/main_summary.json`, `data/main_per_set.tsv`)

| Sets | Positions | SAT | UNSAT | UNKNOWN |
|---|---|---|---|---|
| 8,537 pool sets + 7 AlphaEvolve-derived sets | 8,544 × 33 = 281,952 | 0 | 281,952 | 0 |
| 86 new near-full-derived sets | 2,838 | 0 | 2,838 | 0 |
| Second sweep direction, 8,537 pool sets rotated by 90° | 281,721 | 0 | 281,721 | 0 |

- **Conflict limit.** The limit was 10⁶ conflicts per call and was never reached. Conflicts per
  call: mean 1.3, median 0, 99th percentile 8, maximum 21. Most answers come from propagation
  under the assumptions alone.
- **Abstractly saturated.** All 8,544 sets (8,630 counting the near-full-derived sets) are
  abstractly saturated: no 33-point signotope without a convex 7-gon extends their signotope at any
  insertion position. Per source tag, every set in every tag is saturated (see `by_source_tag`).
- **What saturation covers.**
  - It is stronger than the earlier per-realization geometric saturation. It rules out every
    pseudoline extension, and it covers every realization with the same x-sorted signotope.
  - It is still relative to one sweep direction. The 90° rotation (x, y) → (−y, x) repeats the
    test for a second direction, so all 8,537 pool sets are abstractly saturated in both
    directions. To get distinct x after rotation, 1,585 sets were sheared; brute_kgon again found
    0 axiom violations and 0 convex 7-subsets, and no rotated signotope equals the original. The
    rotated run averaged 2.7 conflicts per call, with a maximum of 23.
- **Timing.** Part 1 (6,587 sets, default options) took about 25 minutes. Part 2 (1,957 sets,
  `lucky=0`) took 220 s. Both ran with 15 workers under heavy outside load.

## 4. r-point neighbourhoods (`scripts/nbhd.py`, `data/nb*.json`, `data/nb*.tsv`)

**Design.**
- Delete r points, keep all orientations of the remaining 32 − r points, and insert r + 1 new
  points: one in each deleted point's x-slot, plus one extra point tried in every gap
  e = 0..32 − r.
- Deletion sets come in three kinds: `win` (r consecutive points in x-order), `geo` (a random
  point and its r − 1 nearest Euclidean neighbours) and `rand` (r random points).
- The sample (`data/sample107.txt`) has 10 seeded-random sets from each of the 10 source tags,
  plus the 7 AlphaEvolve-derived sets.

| Phase | r | Base sets | Deletion sets | Answers | SAT | UNSAT | UNKNOWN | Conflicts per call (mean / max) |
|---|---|---|---|---|---|---|---|---|
| N1 | 2 | 107 | 1,190 | 36,890 | 0 | 36,890 | 0 | 3.4 / 65 |
| N1 | 3 | 107 | 1,186 | 35,580 | 0 | 35,580 | 0 | 7.2 / 236 |
| N1 | 4 | 107 | 1,185 | 34,365 | 0 | 34,365 | 0 | 24.7 / 1,533 |
| N2 | 5 | 107 | 626 | 17,528 | 0 | 17,528 | 0 | 105 / 6,517 |
NB2_ROWS

## 5. Realization

- **No models to realize.** No SAT answer occurred at 33 points, so no 33-point model was decoded
  or realized.
- **The pipeline was still built and calibrated** (`scripts/realize_models.py`,
  `lp_realize.c`, `nl_realize.c`):
  - Old points keep their original x, and new points are placed inside their slot.
  - The search alternates an LP in y (x fixed) with an LP in x (y fixed). Both are restricted to
    a growing trust region and maximise the worst normalised orientation margin.
  - If that fails, a local nonlinear hinge-loss search starts from the same coordinates and is
    then polished by the LPs.
  - Every candidate's doubles are taken as exact dyadic rationals. Every orientation is recomputed
    with integers, the signotope is recomputed from the points alone, and brute_kgon is run on it.
- **Calibration results.**
  - 24 of 30 guaranteed-realizable targets were realized and exactly verified. Each target was a
    pool set's own signotope with one point's coordinates forgotten and that point re-placed in
    the middle of its slot.
  - 107 of the 369 solver-chosen C1 models (31 → 32 points) were realized and exactly verified.
  - So a "not realized" verdict from this pipeline is weak evidence.

## Not tested

- r ≥ 5 beyond the samples above, and r-neighbourhoods for most sets. Phase N3 (one `geo` r = 4
  neighbourhood per set) is reported above only if it finished.
- Sweep directions other than the original and the 90° rotation. Insertion of new points outside
  the deleted points' slots, other than the single extra point.
- The 168 31-point starts (`starts_K7_a.txt`), which this task did not cover.
- Certification: only the DRAT samples (100 one-point instances and 40 neighbourhood instances)
  are proof-checked. Everything else is a solver answer.
- The encoding with these unit assumptions is not verified in Lean. Task H on this branch reports
  a Lean soundness proof for `gen_cnf.py`'s base encoding, but it does not cover the
  assumption-based instances used here.

# Witness saturation and a 65-point octagon search

Two finished computations ask whether the 64-point construction behind
ES(8) ≥ 65 can be extended by one point, and whether a heuristic search finds
65 points with no convex octagon. **No lower-bound improvement is established.
ES(8) ≥ 65 (`sixtyFive_le_esNumber_eight`) is unchanged, as is ES(8) ≤ 314.**
Neither computation is a Lean proof, and the Lean library does not use them.

## Exact saturation of the witnesses

For n = 5, 6, 7, 8, let S be `witness(n)` from
[`scripts/es_lower_bound_witness.py`](../../scripts/es_lower_bound_witness.py):
2^(n−2) integer points in general position with no convex n-gon
(`saturation/witness{5..8}.txt`). The question is whether some point p, with
S ∪ {p} in general position, still avoids a convex n-gon. The order type of
S ∪ {p} depends only on the face containing p in the arrangement of the lines
through pairs of points of S. [`sat.c`](saturation/sat.c) tests one symbolic
point p = v + εd in every angular sector at every arrangement vertex v. It
decides exactly, with int64 and `__int128` arithmetic and asserted coordinate
bounds, whether a convex n-gon through p exists. The distinct sign vectors
reached are counted against Euler's formula F = 1 + L + Σ_v (m_v − 1).

| n | Points | Lines | Faces F (Euler) | Faces reached | Candidates (skipped) | Faces without a convex n-gon | Certificate polygons |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 8 | 28 | 280 | 280 | 928 (0) | 0 | 43 |
| 6 | 16 | 120 | 5,742 | 5,742 | 22,100 (2) | 0 | 237 |
| 7 | 32 | 496 | 108,875 | 108,875 | 431,952 (10) | 0 | 2,294 |
| 8 | 64 | 2,016 | 1,909,613 | 1,909,613 | 7,624,184 (4) | 0 | 14,085 |

A skipped candidate direction is parallel to a further line through its vertex;
that sector is reached from another pair of lines. For n = 8 the arrangement has
2,098 parallel line pairs, 1,903,444 distinct vertices outside S, and at most 15
lines through one such vertex. `out/cert{5..8}.txt` lists the (n−1)-subsets of S
found by the exact search; each one completes some p to a convex n-gon.

[`verify.c`](saturation/verify.c) checks the same claim with different face
representatives (v + δu + δ²w along every edge), a different face count
(F = E − V + 1 by exact per-line sorting) and a different convexity test (the
re-validated certificate polygons, with exactly one edge visible from p):

| n | E | V | F = E − V + 1 | Candidates | Distinct faces reached | Faces not covered |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 489 | 210 | 280 | 1,844 | 280 | 0 |
| 6 | 11,147 | 5,406 | 5,742 | 44,108 | 5,742 | 0 |
| 7 | 216,284 | 107,410 | 108,875 | 863,152 | 108,875 | 0 |
| 8 | 3,813,120 | 1,903,508 | 1,909,613 | 15,244,416 | 1,909,613 | 0 |

A bad face below is one where p creates no convex K-gon.

| Cross-check | Scope | Result |
| --- | --- | --- |
| `independent.py`: exact fractions, edge-midpoint faces, subset enumeration | n = 5, 6 | 280 and 5,742 faces, 0 bad, same bad set as `sat.c` |
| `brute_test.py`: `sat test` against subset enumeration | 80 random sets, 480 added points | 0 mismatches |
| `random_crosscheck.py`: `sat.c`, `verify.c`, `independent.py`, seeds 7 and 11 | 40 random 6–9-point sets each; K at and above the largest convex subset | 0 failures; 29,115 and 30,874 faces compared; 20,058 and 21,715 bad faces matched |
| `spotcheck.py`: explicit integer points, repository DP `largest_convex_subset` | 100, 300, 40 random faces for n = 6, 7, 8 | n in every sample |

For n = 5 and 6 the outcome is forced by the known values ES(5) = 9 and
ES(6) = 17, so these rows are controls for the programs. For n = 8, every
general-position one-point extension of this particular 64-point set has a
convex octagon. This is a finite exact computation by unverified C and Python
code, cross-validated as above; **it is not a Lean proof.** It shows only that
this extremal set cannot be extended. A 65-point octagon-free set, if one
exists, need not contain `witness(8)`, so the result says nothing about whether
ES(8) > 65. Points on a line through two points of S are excluded, as general
position requires.

## Heuristic 65-point search

[`cgon.c`](anneal/cgon.c) counts convex k-gons exactly (integer coordinates
below 2^30, `__int128` orientations). Its simulated annealing moves one point at
a time to minimize the number of convex K-gons, using log or raw energy and an
optional weight mu on the (K−1)-gon count. Floating point appears only in
acceptance and proposals. Mode `addpoint` adds one point at many random positions and
records the counts; `scan` does the same for single-point moves. **No 65-point set without a convex octagon
was found.** This is evidence only, and the controls below show the method is
underpowered at octagon scale.

| Run (driver) | Start | Energy, T0 → T1, mu | Iterations | Final convex octagons |
| --- | --- | --- | ---: | ---: |
| M65w raw s1–s4 (`main65b.sh`) | `init_w8p_1`–`4` | raw, 1.5 → 0.05, 0 | 200,000 each | 1 each |
| M65v s1–s3 (`batch2_coreA.sh`) | `init_v8p_1`–`3` | raw, 1.0 → 0.05, 0.05 | 200,000 each | 1 each |
| M65w mu s71 (`batch2_coreA.sh`) | `init_w8p_3` | raw, 2.0 → 0.1, 0.2 | 200,000 | 1 |
| M65 plateau s81 (`batch3_coreB.sh`) | `init_w8p_4` | raw, 0.6 → 0.2, 0 | 300,000 | 1 |
| M65w s1 (`main65.sh`) | `init_w8p_1` | log, 0.3 → 0.005, 0 | interrupted; last progress line at 49,152 | no output |
| R65 s7 (`batch2_coreB.sh`) | random | log, 0.5 → 0.01, 0 | 100,000 | 15 |

Each start is an octagon-free 64-point set plus the point that `addpoint` found
with the fewest octagons. The base set is `witness(8)` for `init_w8p_*`, and one
of three randomized-offset realizations `v8_*` of the construction for
`init_v8p_*`. **The annealer saves a configuration only after a strict decrease.
Every run above started at one octagon and ended at one, so each saved file is
byte-identical to its start set.** `m65w_mu_s71.txt` and `m65w_raw_s3.txt` are
both `init_w8p_3.txt`. The one-octagon sets come from adding a point, not from
annealing. In the runs that record dwell counts, 40 to 819 evaluated steps sat
at one octagon and the rest at two or more (`out/batch2A.log`,
`out/batch3B.log`).

The repository DP confirms exactly one convex octagon in `out/m65w_raw_s1.txt`
and `out/m65w_mu_s71.txt`. In each, the largest convex subset has 8 points and
exactly 8 points lie in every maximum convex subset. `cgon count` gives one
octagon for all nine 65-point outputs. The variants `v8_*` have no convex
octagon, and all 41,664 of their triple orientations agree with `witness(8)`:
they realize the same order type with different coordinates.

No sampled one-point addition produced zero octagons, consistent with the
exact saturation result:

| Base set (log) | Seeds | Valid candidates | Minimum | Candidates with exactly 1 |
| --- | --- | --- | ---: | --- |
| `witness(8)` (`addpoint_w8_inits.log`) | 11–14 | 3,885; 3,868; 3,875; 3,846 | 1 | 841; 810; 850; 837 |
| `witness(8)` (`batch2B.log`) | 22 | 19,371 | 1 | 4,223 |
| `v8_1`–`v8_3` (`batch2A.log`) | 51–53 | 3,855; 3,926; 3,928 | 1 | 761; 804; 792 |
| `witness(7)`, K = 7 (`batch2B.log`) | 21 | 37,284 | 1 | 9,455 |

Scans of single-point moves from `init_w8p_1` and `init_w8p_2` evaluated 62,833
and 62,817 valid moves, and none went below 1 octagon. Scans of `witness(7)` and
`witness(6)` plus one point (93,059 and 46,771 moves) also never went below 1.

### Controls

| Run (driver) | Points | Forbidden | Starts | Iterations | Result | Exact check |
| --- | ---: | --- | --- | ---: | --- | --- |
| C16 (`controls.sh`) | 16 | hexagon | 20 random | ≤ 300,000 | 0 in 20/20 | DP 5; brute-force hexagon count 0 |
| C17 (`controls.sh`) | 17 | hexagon | 20 random | 300,000 | minimum 1 in 20/20 | DP 6; count 1 |
| C17w (`controls.sh`) | 17 | hexagon | 10 from `init_w6p` | 300,000 | 1 in 10/10, start set returned | DP 6; count 1 |
| C32 (`controls.sh`) | 32 | 7-gon | 6 random | ≤ 600,000 | 0 in 6/6 | DP 6 |
| C33 (`controls.sh`) | 33 | 7-gon | 3 random | 600,000 | minimum 1 in 3/3 | DP 7 |
| C33w (`batch2_coreB.sh`) | 33 | 7-gon | 3 from `init_w7p` | 400,000 | 1 in 3/3, start set returned | DP 7 |
| R64 s91 (`batch3_coreB.sh`) | 64 | octagon | 1 random | 300,000 | 46 | DP 9 |
| R64 s92 (`batch4_coreB.sh`) | 64 | octagon | continues s91 | 200,000 | 43 | `cgon count` 43 |

Runs stop on reaching zero, hence "≤". The method finds extremal sets at 16 and
32 points from random starts; at 17 points the minimum of 1 is forced by
ES(6) = 17. At 64 points, where `witness(8)` has no octagon, the random start
stalled at 46 and then 43 octagons. The method does not rediscover a 64-point
octagon-free set, so its failure at 65 points is weak evidence.

## Provenance

- The files were copied on 11 October 2026 from ignored scratch directories.
  The algorithmic sources `sat.c`, `verify.c`, `independent.py`,
  `spotcheck.py`, `cgon.c`, `brute_addpoint.py`, `verify.py`, `verify_core.py`,
  `gen_witness.py` and `gen_variant.py` are unchanged.
- Only paths changed in `run_all.sh`, `brute_test.py`, `random_crosscheck.py`,
  `brute.py` and the anneal drivers. They now build into, and write to, an
  ignored directory, never this one. `run_all.sh` no longer hard-codes a macOS
  SDK path. It also writes each result before printing it, so a failing check
  stops the script, and it ends by comparing fresh outputs with `out/`.
- New files are `anneal/common.sh` (paths and on-demand build),
  `anneal/verify_all.sh`, and two reconstructed drivers. The original batch-4
  driver and input-generation commands were not kept. In
  `anneal/batch4_coreB.sh`, the parameters are those printed in
  `out/batch4B.log`, and the start set is inferred from `out/r64_cont_s92.err`.
  For `anneal/make_inputs.sh`, the seeds were recovered by search during
  packaging. Both reproduce the retained files byte for byte.
- The runs used three successive builds of `cgon.c`, as noted in each driver.
  Only the last source was kept, and the original compile flags were not
  recorded. Replays with the kept source reproduce logged runs from all three
  builds exactly.
- No copied log or JSON file contained an absolute path, so no `<repo>/`
  placeholder was needed.
- Not copied: binaries, temporary files, an empty waiter log, `c16_test.txt`
  from an unrecorded test, and `.err` progress logs. The exceptions are
  `out/r64_cont_s92.err`, which shows the continuation starting at 46
  octagons, and `out/m65w_s1.err`, the only record of the interrupted
  `main65.sh` run.
- `saturation/run_all.log` and `run_all.time` record the original run: 4 min
  35 s wall, 260.03 s user. `saturation/out/first-run/` is an earlier run of
  the same programs under other file names; it agrees with `out/` apart from
  timings.

## Re-run on 11 October 2026

The packaged copy was re-run on at most two cores:

- `saturation/run_all.sh` took 178.25 s wall (172.31 s user) on one core. All
  36 files in `out/` were reproduced apart from timing fields
  ([log](saturation/rerun-2026-10-11.log)).
- The anneal checks all matched ([log](anneal/rerun-2026-10-11.log)):
  `verify_all.sh` (12.36 s), `make_inputs.sh`, `batch4_coreB.sh` (147.96 s),
  and replays of C16 and C17 seed 1, `addpoint` seeds 21, 22 and 51, and C33w
  seed 1.

No other annealing run was repeated.

## Reproduction

Run these from the repository root. Binaries and fresh outputs go to the ignored
`.cache/es8-lower-bound-search-2026-10-11/`; set `BUILD_DIR` to change this.
The scripts compile with `cc -O2 -Wall -Wextra` (`CC` and `CFLAGS` override
this) and use only the Python 3 standard library. If the default macOS SDK
cannot link, export `SDKROOT` to an installed SDK. The original run used the
Command Line Tools MacOSX26.5 SDK.

```sh
sh experiments/es8-lower-bound-search-2026-10-11/saturation/run_all.sh
```

This takes about 3–5 minutes on one core: 4 min 35 s originally and 2 min 58 s
in the re-run. For n = 8, `sat` takes 19–30 CPU seconds and `verify` 59–86. The
final line must be `{"files_compared_with_committed_out": 36, "differences": []}`.

```sh
bash experiments/es8-lower-bound-search-2026-10-11/anneal/make_inputs.sh
bash experiments/es8-lower-bound-search-2026-10-11/anneal/verify_all.sh
python3 experiments/es8-lower-bound-search-2026-10-11/anneal/verify_core.py \
  experiments/es8-lower-bound-search-2026-10-11/anneal/out/m65w_mu_s71.txt
```

These take about 10 s, 12 s and 4 s. The annealing drivers repeat the original
searches sequentially on one core; logged CPU seconds are shown below.

| Driver | Original CPU seconds |
| --- | ---: |
| `controls.sh` | 567 |
| `main65b.sh` | 1,077 |
| `batch2_coreA.sh` | 1,133, plus three `addpoint` runs |
| `batch2_coreB.sh` | 329 for annealing, plus `addpoint` and `scan` |
| `batch3_coreB.sh` | 869 |
| `batch4_coreB.sh` | 260 (147 in the re-run) |

Two batches originally ran at once, so these times include contention.
`main65.sh` repeats the interrupted run. Drivers append to logs in
`$BUILD_DIR/out/`, so use a fresh `BUILD_DIR` for a clean repeat.

## A family of stacking constructions (added 11 October 2026)

`family/` extends the saturation test from the canonical witness to other
64-point sets built by the same stacking method. `dp.py` runs the bound
recursion of the Lean construction (cup, cap and convex bounds of an upward or
downward stacking, plus c ≤ c₊ + c₋ − 2) over all stacking trees. About
1.2 × 10²¹ labelled trees certify 64 points with no convex octagon. **No tree
certifies 65 points**: under a convex-subset limit c, the recursion's largest
size is exactly 2^(c−1). Every certified tree uses cup/cap blocks of sizes
1, 6, 15, 20, 15, 6, 1.

`generate.py` realized 4,128 certified trees with exact least-offset integer
coordinates. They give 1,592 distinct order types under relabeling and
reflection, each checked for general position, distinct abscissae and a
largest convex subset of exactly 7. The canonical tree reproduces `witness(8)`
byte for byte. Representatives within the coordinate bound of `sat.c` exist for
1,233 order types; 76 sets covering 75 order types were tested:

| Category | Sets tested | Saturated |
| --- | ---: | ---: |
| Canonical witness and a second realization of its order type | 2 | 2 |
| Bracketings of the downward chain of blocks | 13 | 13 |
| Arrangements of the canonical blocks | 13 | 13 |
| Canonical arrangement with randomly built blocks | 12 | 12 |
| Arrangements with randomly built blocks | 11 | 11 |
| Random certified trees | 25 | 25 |

Every run reached all faces of its arrangement (1,909,148 to 1,911,468) and
found no face without a convex octagon. `verify.c` independently covered every
face for `ot0016` and `ot0772`. The tested sets are in `family/sets/`, with
per-set results in `family/out/results.json` and `family/out/summary.txt`.

Saturation depends on the coordinates, not only on the order type, and these
are 75 of 1,592 order types from one construction method. A 65-point set
without a convex octagon need not contain any of them. The results are
evidence only. To rerun, copy `family/` to a directory under `.cache/`, build
`sat` and `verify` from `saturation/` into its `bin/`, and run
`run_queue.sh`; outputs are written beside the copy.

### Completion of the family test (13 October 2026)

The remaining 1,158 order-type representatives within the coordinate bound of
`sat.c` were tested on 12–13 October with the same program
(`family/out/results-remaining.json`, sets in `family/sets/`). Every one is
saturated: no face of its line arrangement admits a 65th point without a convex
octagon. With the 76 sets above, 1,234 tested sets cover all 1,233 order types
of this family that fit the coordinate bound; 359 order types with larger
coordinates remain untested. ES(8) ≥ 65 is unchanged.

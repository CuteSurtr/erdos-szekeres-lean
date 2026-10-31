# Task N2: exact arrangement-face search for 33 points with no convex 7-gon (session 1)

**Result: no heptagon-free 33-point set was found.** Across 60 runs (36,082 CPU-s), the
lowest heptagon count reached was 1. The one-heptagon plateau was reached from every
near-miss seed, and from 29 of 36 random starts within 600 CPU-s. All 60 best sets were
re-checked exactly by three independent methods (cups/caps, triangle-criterion DFS, `cgon`),
and the counts agree: 53 sets have exactly one convex 7-gon, 5 have 2, 1 has 3 and 1 has 6
(`session1/verify_best.json`). Every set is in general position. None has 0 heptagons.

This README covers session 1 (started 00:35 UTC, environment in `env.txt`). A second
firing of the same task (session 2, `env_session2.txt`, started 02:18 UTC on a separate VM)
also wrote to this directory: `runs/`, `runs2/`, `starts2/`, `src/resume.sh`, `src/wave2.sh`
and `src/make_starts2.py` are session 2's. Its numbers are an independent replicate and are
not merged into the tables below. **Session 1's logs are in `session1/logs/`, and
`session1/summary.json` and `session1/table.md` hold its statistics.**

## Machine

Session 1 ran on a cloud VM with 4 cores and 15 GB RAM (Linux 6.18). From about 02:30 UTC,
8 processes shared the 4 cores (see "Incident" below). Every budget and time here is
per-process **CPU** time (`clock()`), so runs stay comparable.

## Tools and calibration

- `src/n2.c` (one C program) with `src/arr_core.inc`. The include is a verbatim copy of
  `results/D/src/satcount.c`'s face enumeration and exact slot count. Only two changes:
  results are recorded in memory, and only faces that contain an exactly verified integer
  point (|c| < 2^29) are kept.
  - Each move puts a point in a face of the line arrangement of the other points.
  - The number of convex 7-gons the point creates there is exact.
  - After every accepted move, the 7-gons of the new 33-point set are re-enumerated from
    scratch (angular DFS) and compared with the prediction H(S − moved) + Σ m(face).
  - **0 mismatches in 64,721 sweeps** (all sweeps were complete by Euler's formula).
- Start sets are rescaled exactly (×⌊2^28 / max|c|⌋, same order type), so that small faces
  still contain integer points.
- Calibration (`calib/`):
  - `ae_triple_check.json`: AlphaEvolve's set (integer realization from
    `results/D/calib`) has c7 = 1 and c8 = 0 by cups/caps, DFS and `cgon`. Its 7-gon is
    {14, 15, 17, 20, 23, 25, 32}.
  - `ae_deletions.json`, `p2d_16_deletions.json`: for all 33 deletions of AlphaEvolve's set
    and of seed p2d_16, n2's sweep was checked against standalone `satcount` and `cgon`.
    The face totals, H(S − i) and the lowest m level all match (66/66).
  - Before the realizable-face filter was added, the full m = 0/1/2 face histograms also
    matched `satcount` exactly on all 33 AlphaEvolve deletions.
  - The 7 heptagon-vertex deletions of AlphaEvolve's set have no m = 0 face, as D/D2 found.

## Methods (all exact; same move engine)

- **(a) tabu**:
  - Each step considers up to 3 heptagon vertices (sampled by heptagon degree) plus one
    other point, excluding points moved in the last 3 steps.
  - For each, it sweeps the arrangement of the other 32 points and takes up to 12 faces at
    the lowest realizable m and 4 at the next level.
  - It moves to the best candidate whose order-type fingerprint has not been visited yet.
    A candidate that beats the best H so far is allowed even if visited (aspiration).
- **(b) LNS + LAHC**:
  - Remove k = 3..6 points: 1–3 vertices of a random current heptagon, the rest sampled in
    proportion to near-heptagon participation.
  - Re-insert one point at a time into a best face: greedily (70%), or by beam search with
    width 3 and branching 3 (30%).
  - Accept with late-acceptance hill climbing, history length 20.
- **(c) pen**: the same as (a), but the energy is H + λ(t)·NEAR. λ(0)·NEAR(start) = 10,
  and λ falls linearly to 0 at 75% of the budget.
  - NEAR = #(convex hexagon Q, point p) with p strictly inside the quadrilateral of 4
    consecutive vertices of Q. Such a 7-subset has 6 hull vertices, and pushing p across
    the adjacent edge would make a convex 7-gon.
  - NEAR is evaluated for the 8 lowest-H candidates of each step.
- **Order-type fingerprint**: a mirror-invariant hash of the per-point sorted λ-vectors
  (λ(i,j) = #points left of i→j). Equal order types give equal fingerprints, so "distinct
  fingerprints" is a lower bound on distinct order types.

## Campaign (paired, equal CPU)

Every start was run with every method: seed 1, 600 CPU-s each.

- **Starts** (`starts/`, made by `src/make_starts.py`):
  - 8 near-miss seeds: AlphaEvolve's set plus 7 drawn with `random.Random(2026)` from the
    273 sets in `nearfull_p2{c,d}.txt`.
  - 12 random starts: 4 plain uniform, 4 with 3-fold rotational symmetry (11 orbits) and 4
    mirror-symmetric (16 pairs + 1 axis point).

| family | method | runs | best H (per run) | reached H ≤ 1 | median CPU-s to H ≤ 1 | distinct fingerprints | per CPU-h | arrangement sweeps |
|---|---|---|---|---|---|---|---|---|
| near-miss | tabu | 8 | all 1 | 8/8 (start) | 0 | 1,985 | 1,486 | 7,908 |
| near-miss | lns | 8 | all 1 | 8/8 (start) | 0 | 1,438 | 1,077 | 10,696 |
| near-miss | pen | 8 | all 1 | 8/8 (start) | 0 | 1,982 | 1,483 | 7,896 |
| random (12) | tabu | 12 | 1×8, 2×3, 3×1 | 8/12 | 123.5 (mean 184) | 2,830 | 1,412 | 11,272 |
| random (12) | lns | 12 | 1×12 | **12/12** | **86.8** (mean 121) | 2,192 | 1,093 | 15,709 |
| random (12) | pen | 12 | 1×9, 2×2, 6×1 | 9/12 | 122.8 (mean 194) | 2,822 | 1,408 | 11,240 |

By symmetry class (reached H ≤ 1, then median CPU-s):

| class | tabu | lns | pen |
|---|---|---|---|
| plain | 3/4, 106 s | 4/4, 92 s | 2/4, 347 s |
| 3-fold | 3/4, 121 s | 4/4, 105 s | 3/4, 114 s |
| mirror | 2/4, 219 s | 4/4, 66 s | 4/4, 163 s |

The symmetric starts are only symmetric at the start; no method preserves symmetry.

**Other statistics**

- The 600 CPU-s near-miss runs never left the H = 1 plateau. Tabu visited a new
  fingerprint at every step, about 250 plateau states per run.
- LNS accepted about 90% of its re-insertions: LAHC accepts ties, and nearly every
  destroy-and-repair on the plateau lands back on H = 1. The acceptance rate per k is in
  `summary.json`.
- None of the heptagon-vertex deletions that were swept (64,721 sweeps in all) had a
  realizable m = 0 face; one would have produced H = 0.

## Comparison and assessment

- **Reaching the plateau.** LNS is the clear winner from random starts: 12/12 runs reached
  one heptagon, with a median of 87 CPU-s. Tabu managed 8/12 (median 124) and pen 9/12
  (median 123).
  - From 200k heptagons, removing several points and re-inserting them into exact best faces
    makes big jumps.
  - Single-point best-face relocation pays 4 full sweeps (~2.4 CPU-s) per step and needs
    about 50–100 steps.
  - Annealing reportedly reaches the plateau in 35–40 CPU-s (plan #3), so no exact method
    here is faster at descent. Their value is complete local information, not speed.
- **Exploring the plateau.** Tabu and pen visit about 1,450 distinct order types per CPU-h.
  LNS visits about 1,080 per CPU-h, because its moves are larger and more of its sweeps go
  to intermediate sets.
  - Penalty shaping (c) did not change plateau behaviour measurably at this weight. Its
    fingerprint rate and outcomes match (a), and from random starts it was no better.
- **Overall.** 10.0 CPU-h of exact face-level search visited 13,249 distinct fingerprints
  (summed over runs), 5,405 of them in the near-miss runs, which all stayed on the
  one-heptagon plateau. It also produced 29 new one-heptagon 33-point sets from random
  starts, 20 of them from symmetric starts (see `session1/logs/*/rnd_*.best.txt`).
  - Not one heptagon-free set appeared.
  - This matches D2's finding that all 1,918 heptagon-free deletions of the 274 seeds are
    saturated. Saturation under one-point relocation looks generic on this plateau, not a
    feature of particular seeds.
  - This is evidence, not proof. Tabu tested only 3 of the 7 heptagon vertices per step, so
    a plateau state could have had an unsaturated deletion that was never swept.
    (`N2_NV=7` in `n2.c` tests all of them; it was not run, for lack of time.)

## Incident (data handling)

At about 02:20 UTC, a `git pull --rebase` in the live worktree collided with session 2's
commits and with run files that were still open for writing. The checkout restored the
in-progress (empty) versions of 13 finished runs' JSON files.

- Those 13 jobs were re-run from scratch with the same seed and budget (`src/rerun.sh`).
  Their tables above come from the re-runs.
- Afterwards, the live logs lived in scratch, and checkpoints were committed from a
  separate clone.
- No reported number comes from a clobbered file.

## Reproduction

```
cd results/N2 && gcc -O3 -march=native -w -o bin_n2 src/n2.c -lm   # needs results/D/bin (sh ../D/src/build.sh) for checks
python3 src/make_starts.py starts 4
BUDGET=600 sh src/run_all.sh            # writes runs/<method>/<start>.{json,traj,best.txt}
python3 src/summarize.py runs           # summary.json + table
python3 src/verify_best.py runs verify_best.json
python3 src/calib_vs_satcount.py starts/nm_ae.txt calib/ae_deletions.json
```

# LBS L2: extend32 heuristic search for 33 points without a convex 7-gon

Machine L2, strategy `extend32`, budget 3.0 h, task file at 640a56c2.
Environment: `env.txt` (4-core Xeon 2.1 GHz, gcc 13.3, Python 3.11).

**Result: no counterexample. The best count found is 1 convex 7-gon** (`best.txt`).
686 of 687 runs ended at exactly 1, and one ended at 2. No run went below 1.
This is heuristic evidence only.

## Program

- `lbs.c` holds 33 integer points (|c| < 2^40, `__int128` orientations) and
  counts convex k-gons, k = 3..7. Each polygon is counted once, at its lowest
  vertex: the other points are sorted by angle around that vertex, and a DP runs
  over increasing chains with left turns. A one-point move is scored
  incrementally as through(p, new) − through(p, old). Here through(p) is the
  same DP restricted to chains that contain p. Any move that creates a
  collinear triple or a repeated point is rejected. `lbs count` cross-checks the
  incremental count against full recounts with every point deleted.
- `vfy.c` is the independent exact check. It tests general position on all
  triples, computing orientations from the coordinates with no tables. It
  counts convex k-subsets (k = 4..7) by enumerating subsets and building each
  convex hull with Andrew's monotone chain, then lists the 7-gons and the points
  that lie in all of them.
- `gen_bases.py` builds 40 realizations of the 32-point Erdős–Szekeres
  construction (`bases/`). It uses the stacking of `ErdosSzekeres/LowerBound`,
  as in `scripts/es_lower_bound_witness.py`, with random extra horizontal gaps
  and vertical offsets, then scales the result. `base000` is the canonical
  witness. All 40 bases have c6 = 39,648 and c7 = 0.
- `run.sh SECONDS` starts 4 workers (seeds 1 to 4). Each run of a worker:
  1. Picks a random base.
  2. Runs a neutral random walk of 0, 1,000, 10,000 or 50,000 proposals that
     accepts only moves keeping the 32-point set free of convex 7-gons. This
     gives perturbed 7-gon-free sets, generally of other order types.
  3. Tries 4,000 candidate positions for a 33rd point (log-scale offsets from
     the existing points, plus jumps) and keeps a random minimizer.
  4. Anneals all 33 points for 100k or 300k Metropolis steps. The energy is
     c7 + mu·c6, with mu in {0, 0.002, 0.01, 0.05}. T0 is in {0.3, 0.6, 1, 2, 4},
     falling geometrically to T1 in [0.05, 0.15]. Moves are log-uniform
     single- or two-axis shifts, jumps next to another point, and Gaussian
     relocations.

  Each run keeps its best state, lexicographically by (c7, c6). Logs are in
  `out/w?.log`. Every best state with c7 ≤ 1 is saved in `out/w?.sets`, one
  line per run.
- `analyze.py` writes `analysis.txt` and `best.txt`. It re-verifies the 10
  best sets and 20 random saved sets with `vfy`: 0 mismatches in c7, c6 or
  general position.

The search ran from 04:46 to 07:19 UTC: 4 workers, 687 runs, 1.343·10^8
annealing steps. The workers write their logs into the repository directory,
and an early `git pull --rebase` unlinked those files. The workers kept writing to the open
files, which were copied out every 20 s and then every 0.5 s, so no run is
missing: each worker's log and sets files agree line for line.

## Results

| Quantity | Value |
| --- | --- |
| Runs | 687 |
| Best c7 per run | 1 in 686 runs, 2 in 1 |
| Minimum over the 4,000 extension candidates | 1 in 685 runs, 2 in 1, 3 in 1 |
| Final c7 at the end of annealing | 1: 289, 2: 146, 3–20: 117, 21–115: 135 |
| Final c7 = 1 by mu | mu = 0: 269/288; 0.002: 17/139; 0.01: 3/123; 0.05: 0/137 |

The full distribution of final counts is in `analysis.txt`. A positive weight
on 6-gons lowers c6 but leaves the walk at higher c7, and no setting found a
move from 1 to 0.

**Extension statistics.** On an unperturbed realization, about 19% of valid
candidate points create exactly one 7-gon and none create zero. This is
consistent with the exact saturation result for `witness(7)` in
`experiments/es8-lower-bound-search-2026-10-11`. After a neutral walk, only
2–3% of candidates give exactly one. In 2 of 526 walked bases, no candidate
gave fewer than 2 or 3, although the annealer still reached 1.

## Near-misses

The best set (`best.txt`, worker 3, run 173) has 33 points in general
position. It has c4 = 20,326, c5 = 21,169, c6 = 5,766 and **c7 = 1**. `vfy`,
`lbs count` and the repository's Python DP (largest convex subset = 7) all
confirm it. Its only 7-gon is {2, 4, 8, 16, 21, 25, 32}, and it contains the
added point 32. Coordinates reach about 8·10^11 in y and 2·10^8 in x.

What the near-misses look like:
- Every c7 = 1 set is a 7-gon-free 32-point set plus one point that completes
  a single convex 6-gon to a 7-gon. Deleting any vertex of that 7-gon leaves a
  7-gon-free 32-point set. Deleting vertex 2 of the best set leaves one with
  c6 = 4,690, against 39,648 for the construction. The neutral walks and the
  annealing therefore reach 7-gon-free 32-point sets with far fewer 6-gons
  than the construction. These are other order types, and even so the 33rd
  point cannot avoid every 6-gon.
- In 429 of the 686 c7 = 1 sets, the lone 7-gon uses the added point. In the
  other 257, annealing moved the configuration so that the 7-gon lies among
  the original points.
- Over the c7 = 1 sets, c6 ranges from 5,766 to 51,660 (median 13,662). The
  ten best sets (`analysis.txt`) all have c6 between 5,766 and 7,814. Their
  7-gons often use runs of consecutive indices, for example
  {0, 1, 2, 3, 4, 31, 32}. Point indices follow the base order, but after
  annealing the points no longer keep their block structure, so this is a
  description only.

## Files

`lbs.c`, `vfy.c`, `gen_bases.py`, `run.sh`, `analyze.py`, `bases/`,
`out/w?.log`, `out/w?.sets`, `out/w?.best.txt`, `analysis.txt`, `best.txt`
(one "x y" per line), `env.txt`.

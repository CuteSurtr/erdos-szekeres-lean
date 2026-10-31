# LBS L3: c3coords heuristic search (33 points, convex 7-gons)

Machine L3, strategy `c3coords`, budget 3.0 h, task file at commit 640a56c2.
Runs went from 04:46 to 07:13 UTC on 4 cores (`env.txt`).

**Result: no counterexample. The best count found is 3 convex 7-gons**, which is a single
orbit of one 7-gon under the 120° rotation. Over 1391 random symmetric restarts the count never
went below 3, and the symmetry-breaking phases never went below 3 either.

## Program (`src/`)
- `lbs.c` (gcc -O2): 33 points in Eisenstein coordinates (a,b) = a + bω with ω = e^{2πi/3}.
  Rotating by 120° about the origin is exact on integers: (a,b) → (−b, a−b). The map to the
  plane is linear with positive determinant, so orientation signs computed on integer (a,b)
  are exact. The program keeps a 33³ orientation-sign table and updates only the triples
  through a moved point. Any move that makes three points collinear, or makes two points
  coincide, is rejected.
  It counts convex 6-gons and 7-gons exactly: for each lowest vertex p, it sorts the
  points above p by angle and runs a DP over convex chains (about 0.3 ms per full count).
  Each restart has two phases:
  1. Simulated annealing on 11 orbit representatives: moves one orbit at a time, with
     random coordinates in [−R,R] and log-uniform step sizes that shrink over the schedule.
  2. Simulated annealing on all 33 points individually, starting from the best set of
     phase 1 (this breaks the symmetry).
  Acceptance uses energy c7 + w·c6.
  The polish mode (an extra argument giving an init file) skips phase 1 and runs a long
  phase 2 from a stored c7 = 3 set.
  The tool used all 4 cores by running 4 independent processes.
- `verify.c`: independent exact check. It reads only the integer affine image
  (u,v) = (2a−b, b) and uses 128-bit cross products. It checks that the points are distinct
  and that no three are collinear, then computes the hull size of every 6-subset and every
  7-subset by point-in-triangle tests.
- `verify2.py`: second independent check in pure Python. It runs Andrew's monotone chain
  on every 7-subset and also checks the 3-fold symmetry.
- `analyze.py` (convex layers, orbit structure of the 7-gons) and `summarize.py` (distributions).

Every count reported here was confirmed by `verify` (`near_analysis.txt` has every stored
near-miss with c7 ≤ 6). The best set was confirmed by both verifiers
(`verify_c.txt`, `verify_py.txt`).

Bug note: before 05:16 UTC, the c6 tie-break in `lbs.c` skipped lowest vertices that had
exactly 5 points above them, so c6 could come out at most 1 too low. The c7 count was never
affected (it needs 6 points above p), and every c7 matched the verifiers. I fixed it in the
source; runs r11–r14 used the old binary, which only affects their c6 tie-break. All c6
values in `near_analysis.txt` and here come from the brute-force verifier.

## Runs (`runs/`)
| run | R | phase-1 / phase-2 steps | w | restarts | restarts with c7 = 3 |
|---|---|---|---|---|---|
| r11 | 1e5 | 30k / 15k | 0 | 684 | 28 |
| r12 | 1e5 | 150k / 60k | 1e-3 | 146 | 30 |
| r13 | 1e7 | 30k / 30k | 1e-4 | 511 | 25 |
| r14 | 1e4 | 60k / 60k | 1e-3 | 50 (stopped at 05:13 to free a core for r15) | 1 |
| r15 | 1e5 | polish: 1M free steps from the 14 c7 = 3 sets found by 05:13 | 1e-3 | 25 | 25 (none improved) |

The search ran about 120M exact counts in total. Each run has a `*_runs.tsv` with one line
per restart, plus `*_near.txt` (all sets with c7 ≤ 6) and `*_best*.txt`.

## Distribution of final counts (best c7 per restart, 1391 random-start restarts)
| c7 | 3 | 5–6 | 9 | 10–17 | 18 | 19–30 | 31–60 | 61–120 | >120 |
|---|---|---|---|---|---|---|---|---|---|
| symmetric phase | 84 | 5 | 102 | 99 | 214 | 253 | 340 | 226 | 68 |
| after free phase | 84 | 6 | 102 | 115 | 212 | 257 | 369 | 188 | 58 |

`summary.txt` has the full distributions. The symmetric counts are always multiples of 3,
because no convex 7-gon is fixed by the rotation (7 is not divisible by 3). The values
3, 9, 18 and 24 occur much more often than their neighbours. 6 = two orbits is rare
(5 times).

The free phase improved 342 of 1391 restarts (25%), mostly high counts by a few units. It never
improved a restart that ended at 3, 6 or 9 in a way that went below 3. The best results from
non-symmetric sets were c7 = 5 (once) and 7 (once). The 25 polish restarts each ran 1M
single-point moves from a c7 = 3 set and all stayed at 3, while lowering c6 (for example
from 17989 to 10569). The symmetric minimum with c7 = 3 seems to be a local minimum for
single-point moves as well.

## Near-misses
- There are 109 stored sets with c7 = 3 (84 from random restarts, 25 polished versions of 14 of them; 58 are still exactly 3-fold symmetric). In every
  one the three convex 7-gons form one rotation orbit (the same 7 orbit representatives).
- Their convex-layer structure is almost always a 3-fold pattern of triangles and hexagons.
  The most common patterns are [6,6,6,3,6,6] (25 sets), [3,3,3,6,6,6,6] (18) and [3,6,6,6,6,6] (17).
- Across the c7 = 3 sets, convex 6-gons range from 7449 to 34511. "Six-gons-plus-one" (7-subsets
  whose hull has exactly 6 vertices) range from 43932 to 294864.
- **Best set** (`best.txt`, run r12, restart 110): 3-fold symmetric, c7 = 3, c6 = 7449,
  six-gons-plus-one = 43932. Its 7-subset hull-size distribution is
  h3 = 2076264, h4 = 1626372, h5 = 525477, h6 = 43932, h7 = 3. Its convex layers are [3,3,3,6,6,6,6].
  Its convex 7-gons are point indices {3,7,10,16,17,19,31}, {5,6,8,20,25,29,32} and
  {9,14,18,21,27,28,30}: rotations of the 7-gon on orbit representatives {3,5,6,7,8,9,10}.

`best.txt` has the coordinates as a b (Eisenstein, exact 120° symmetry: point i+11 is the
rotation of point i) and as u v = (2a−b, b), an integer affine image with the same convexity
and collinearity structure.

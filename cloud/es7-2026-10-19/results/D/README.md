# Task D: near-miss plateau walks and diversified annealing (ES(7) > 33 search)

__HEADLINE__

All numbers below come from `summary.json`, `calib/*.json` and the run logs summarised there.
Nothing here is a theorem: every "saturated" statement is about one explicit integer point set
(its full line arrangement was swept), not about its order type or about all 32-point sets.

## Machine and budget

- Apple M5 Pro, 15 cores (5 "Super" + 10 "Performance"), 48 GB, macOS (Darwin 25.6).
- The machine was shared with other ES(7) jobs started at the same time (load average 60 to 100
  on 15 cores for most of the run), so each of my processes got roughly a quarter of a core.
  All rates below are per **CPU** second or hour (process plus child CPU from `getrusage`, or the
  tools' own `clock()`), not per wall second.
- Wall time: started 21:14 KST, runs launched 21:32, runs stopped __STOP__, report __END__.
- Build note: the default macOS 27 SDK fails to link on this machine (tapi "unknown
  architecture"); `SDKROOT=.../MacOSX26.5.sdk sh src/build.sh` works.

## 1. Calibration (required, all passed)

**k = 6 (ES(6) = 17, so every hexagon-free 16-point set must be saturated).** Each set below
was checked with `sat.c` (K = 6) and with `satcount` (K = 6). Every face of the full line
arrangement was hit (the face count equals Euler's count), and no face admits a new point
without a convex hexagon.

| sets | hexagon-free | `sat.c` bad faces | `satcount` m = 0 faces |
|---|---|---|---|
| classical ES(6) construction (`tools/decomp/sets.py`, integer realization, same order type) | yes (exact: c6 = 0) | 0 | 0 |
| 4-fold symmetric 16-point set (`sets.py`) | yes | 0 | 0 |
| 5-fold symmetric 16-point set (`sets.py`) | yes | 0 | 0 |
| 1,001 distinct annealed hexagon-free 16-point order types (`gen walk 6 16`) | all | 0 | 0 |
| 1,156 deletions of one-hexagon 17-point sets (`gen near 6 17`, the k = 6 null) | all | 0 | 0 |

**k = 7, AlphaEvolve's 33-point set (`inputs/alphaevolve_pts.json`, `points_7`).** Each float
was converted exactly to a binary fraction (Python `Fraction`). The set is in general position
(all 5,456 triples nonzero). Convex k-gon counts by two exact methods, cups/caps and a DFS over
convex subsets with the triangle criterion, agree:
c3..c8 = 5456, 24758, 47945, 32055, **1**, **0**. The unique 7-gon is {14, 15, 17, 20, 23, 25,
32} (0-based), the same as the critique's. An integer realization with identical orientation
signs (`calib/alphaevolve_int.txt`, extent 2^26) gives the same counts with `cgon`, cups/caps and
the DFS.

**Seeds.** `nearfull_p2c.txt` has 147 lines and `nearfull_p2d.txt` has 126. The line format is
`label E 33 x1 y1 ... x33 y33`; every label is `FULL0`, E = 1, and |c| <= 67,100,107. All 273
sets are in general position with exactly one convex 7-gon and no 8-gon, by cups/caps and by
`cgon` (`calib/seeds_check.json`). Together with AlphaEvolve's set these are 274 distinct order
types.

## 2. `satcount`

`src/satcount.c` keeps `sat.c`'s face enumeration (symbolic points at every arrangement vertex,
128-bit face hashes, completeness checked against Euler's formula) and replaces the existence DP
by an exact count:

- A convex 7-gon through a new point p is p plus a convex hexagon Q of S such that p sees exactly
  one edge of Q. That edge ab with its neighbours c, d gives three sign conditions:
  orient(a,b,p) < 0, orient(c,a,p) > 0, orient(b,d,p) > 0.
- All convex hexagons of S are enumerated once (lowest-vertex angular DFS; the count equals
  `cgon`'s c6). They are grouped into slots (c,a,b,d) with multiplicity W, and
  m(face) = sum of W over the satisfied slots.
- m is capped at 3. A move-to-front cache of satisfied slots settles most faces; the rest get a
  full scan, grouped by the beyond-line.
- For each face with m <= 1 it also reports the blocking heptagon (when m = 1) and tries to find an
  exactly verified integer point in the face (|c| < 2^29). It does this by float half-plane
  clipping, then rounding the centroid, then a ray search, then a small lattice-box scan; every
  candidate point is checked exactly against all 496 signs.
- Arithmetic is exact: int64 for predicates on S (coordinates < 2^29, so differences < 2^30 and
  products < 2^61), and `__int128` for vertex predicates (< 2^123).
- One sweep of a 32-point set takes about 0.4 CPU-s (109,337 faces).

Validation (all exact, all passed):

- `satcount test` (exact m, uncapped) against a `cgon` recount of S + {p}: 5,448 points on 21
  sets, 0 mismatches. The sets are 6 annealed and 6 null k = 6 sets, the 7 heptagon-free deletions
  of the first `nearfull_p2c` seed, a 32-point pool set with 25 heptagons, and AlphaEvolve's
  33-point set. The points are random multi-scale points plus the lattice points that `satcount`
  found inside m <= 1 faces, so the per-face capped m is checked as well.
- Faces with m = 0 (`calib/satcount_m0_validation.json`): on 4 heptagon-free 31-point sets from
  `inputs/starts_K7_a.txt`, which are not saturated, the number of m = 0 faces equals the number
  of distinct bad faces from `sat.c` (994/994, 322/322, 873/873, 10975/10975). 800 face points
  and 645 random points were recounted by `cgon` with 0 mismatches.
- On 60 random walk states, the number of convex hexagons `satcount` enumerated equals `cgon`'s
  c6 (`calib/hexcount_check.json`). Every sweep in this task reported a complete face
  enumeration (`complete: true`).

## 3. Plateau statistics: sweeps of all seed deletions

__SEEDS__

## 4. Relocation walk vs plain random restarts

__WALK__

## 5. Diversified annealing at 33 points

__ANNEAL__

## 6. Exact verification

__VERIFY__

## Files

- `summary.json`: all statistics (calibration, seed sweep, walk, baseline, annealing).
- `anneal_best50.jsonl`: the 50 best distinct annealed 33-point sets (distinct up to reflection
  by order type). Each line has the integer points, `cgon` counts, the independent exact Python
  heptagon/octagon counts, and the family and run id.
- `walk_states_sample.jsonl` __WALKFILE__
- `calib/`: `calib_summary.json` (k = 6 saturation, k = 6 null, AlphaEvolve, satcount
  validation), `satcount_m0_validation.json`, `seeds_check.json`, AlphaEvolve triple checks,
  and `alphaevolve_int.txt` (an integer realization with the same orientation signs as the
  exact binary fractions of the floats).
- `logs/`: compressed per-step walk logs, annealing run records and baseline logs.
- `src/`:
  - `satcount.c` and `canon.c`, plus the exact checkers `verify_exact.py` (cups/caps) and
    `triple_check.py` (cups/caps, triangle-criterion DFS, cgon).
  - `walk.py`, `baseline.py`, `anneal33.py`, `seedsweep.py`, `anneal_seeds.py`,
    `calib.py`, `calib_m0.py`, `check_seeds.py`, `summarize.py`, `dlib.py`.
  - `build.sh`.

## Reproduction

```
SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk sh src/build.sh
python3 src/calib.py                 # k=6 saturation, k=6 null, AlphaEvolve, satcount validation
python3 src/calib_m0.py calib/satcount_m0_validation.json 4
python3 src/check_seeds.py calib/seeds_check.json ../../inputs/nearfull_p2c.txt ../../inputs/nearfull_p2d.txt
python3 src/seedsweep.py RUNS/seedsweep 4 ../../inputs/nearfull_p2c.txt ../../inputs/nearfull_p2d.txt int:calib/alphaevolve_int.txt
python3 src/walk.py RUNS/walk W 6 random|greedy SECONDS SEED <seed files>
python3 src/baseline.py RUNS/baseline B SECONDS SEED
python3 src/anneal33.py RUNS/anneal W SECONDS SEED <seed files>
python3 src/summarize.py RUNS .
```

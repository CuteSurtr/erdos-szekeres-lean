# Task D2: real-coordinate search for a heptagon-free 33-point set (cloud run, 20 Oct 2026)

**No set with zero convex 7-gons was found.** The best exactly verified result is the same as
before the run: 33-point sets with exactly one convex 7-gon. This run found 386 new ones (distinct
order types) by annealing, on top of the 274 seeds. None of this is evidence for or against
ES(7) = 33 beyond the explicit sets and faces that were searched.

All numbers come from `summary.json` (written by `src/summarize.py`), `calib/*.json`,
`seedsweep/` and the compressed run logs in `logs/runs/`.

## Where it ran (`env.txt`)

- A cloud container: `Linux vm 6.18.44-fc-v139 x86_64`, 4 cores, 15 GB RAM, hostname `vm`.
- Start 00:21 UTC, final summary 03:45 UTC on 2026-10-20.
- The container was restarted at about 03:14 UTC. The same machine shape is recorded in
  `env.txt`. Files on disk survived. The annealing processes running at that moment were
  killed, and their in-flight runs (at most 6, never logged) are lost. Four new workers ran from
  03:15 to 03:42.
- All 4 cores were used throughout. CPU figures below are process plus child CPU, or the tools'
  own `clock()`.
- Tools are the Task D sources (`../D/src`, copied into `src/`), built with `src/build.sh` (gcc).
  Two changes for D2: `walk.py` gained `MAXLEN` / `ONE_PER_SEED` (bounded walks from every
  seed), and `summarize.py` gained a `walk_multistart` section.

## 1. Calibration (all passed, re-run in the cloud)

- **k = 6 (ES(6) = 17), saturation.** `sat.c` and `satcount` both report 0 bad faces and 0 m = 0
  faces, with Euler-complete face enumeration, on:
  - the classical ES(6) 16-point construction;
  - the 4-fold and 5-fold symmetric 16-point sets;
  - 287 distinct annealed hexagon-free 16-point order types;
  - 355 deletions of one-hexagon 17-point sets (the k = 6 null).
- **satcount against exact `cgon` recounts.** 5,460 points on 21 sets, 0 mismatches.
- **m = 0 faces against `sat.c` bad faces.** On 4 non-saturated 31-point sets, the counts match
  exactly: 994/994, 322/322, 873/873 and 10975/10975. 800 face points and 645 random points were
  recounted with 0 mismatches.
- **AlphaEvolve's 33-point set** (exact binary fractions, and an integer realization).
  - It is in general position.
  - c3..c8 = 5456, 24758, 47945, 32055, **1**, 0, by cups/caps and by `cgon`.
  - The unique 7-gon is {14, 15, 17, 20, 23, 25, 32}.
- **Seeds.** All 273 `nearfull` sets plus AlphaEvolve's set (274 distinct order types) are in
  general position, with exactly one convex 7-gon and no 8-gon.

## 2. Plateau statistics: every heptagon-free deletion of every seed

The 274 seeds give 1,918 deletions (1,347 distinct 32-point order types). Every deletion's full
line arrangement was swept with `satcount` (109,337 faces each, all complete), using 1,434 CPU-s.

| quantity | value |
|---|---|
| m = 0 faces (a heptagon-free 33-point extension) | **0** in all 1,918 |
| m = 1 faces per deletion | min 11, p10 115, median 589, p90 2,447, max 14,353 |
| m = 1 faces as a fraction of all faces | median 0.54% (k = 6 null: median 1.7%) |
| m = 2 faces | median 15, max 2,503 |
| distinct blocking 7-gons over the m = 1 faces | median 2, max 4 |
| m = 1 faces holding an exactly verified lattice point | 69.9% |

The m = 1 tail is not heavier than the k = 6 null as a fraction of faces. As critique item 13
says, this comparison has no calibrated alternative, so it decides nothing either way.

## 3. Relocation walk vs plain random restarts (equal CPU)

One step of the walk:
1. Take a heptagon-free 32-point set S.
2. Sweep all faces of its arrangement.
3. For a random m = 1 face (a lattice point p is verified exactly), form S + p − v for a vertex
   v of the unique 7-gon that p creates.

A tabu list holds the canonical order types visited (up to reflection). Every state is
re-checked heptagon-free with `cgon`.

| run | CPU | 32-point states swept (all distinct, all saturated) | m = 0 faces |
|---|---|---|---|
| long walk w0, random move, from the full seed pool | 3,567 s | 4,835 | 0 |
| long walk w1, greedy (best of 4 by m = 1 count) | 3,562 s | 4,789 | 0 |
| bounded walks: 15 steps from one deletion of **each** of the 274 seeds, 2 processes | 3,392 s | 4,384 | 0 |
| baseline: `gen near` random restarts (63 starts, 58 reached E ≤ 1) | 3,571 s | 3,352 distinct deletions emitted, 300 sampled and swept | 0 |

- **Rate.** The walk produced 4,860 new swept heptagon-free 32-sets per CPU-hour. The baseline
  produced 3,379 per CPU-hour unswept, or 2,001 per CPU-hour counting a 0.73 s sweep for each.
  That is a ratio of 1.44× (unswept) to 2.43× (swept). This is **below the plan's 3× bar**.
- **Overlap.** The long walks, the bounded walks and the baseline visited disjoint sets of order
  types (overlap 0).
- **Walk structure.** The long walks never hit a dead end: every state had a non-tabu lattice
  neighbour, so each long walk descended from its first start only. The bounded multi-start run
  was added to cover all 274 seeds.
- **m = 1 face counts along the walks.**
  - Random walk: median 266. It fell from a mean of 389 in the first quarter to 322 in the last.
  - Greedy walk: median 586. It rose from a mean of 636 to 712.
  - Bounded walks: median 233.
  - Baseline sample: median 465.
- No visited state was ever close to an m = 0 face. The minimum m = 1 count was 5, and no state
  lacked a lattice m = 1 face.

## 4. Diversified annealing at 33 points (exact convex 7-gon count)

Each run uses `cgon anneal 7 33`: exact counts, energy log(1+E), Metropolis, 100k/200k/400k
iterations. Starts come from five families, all far from the classical construction:
- convex layers (2–5 ellipses);
- random lattice points (24–64 grid);
- perturbed near-miss sets (random affine map plus noise of 1e-4..1e-1);
- clusters;
- uniform (control).

**457 runs, 30,513 CPU-s.**

| min energy reached (exact c7) | runs |
|---|---|
| 0 | **0** |
| 1 | 386 |
| 2 | 7 |
| 3–5 | 18 |
| 6–49 | 11 |
| ≥ 100 (did not converge) | 35 |

- **By family** (runs; best energy 1 in every family):
  - layers: 111 runs, 94 reached E = 1;
  - lattice: 115 runs, 99 reached E = 1;
  - nearpert: 112 runs, 93 reached E = 1;
  - clusters: 78 runs, 67 reached E = 1;
  - uniform: 41 runs, 33 reached E = 1.
- **Distinctness.** All 386 E = 1 sets are distinct order types.
- **Recount.** `cgon` recounted the best energy of every run, with 0 mismatches.
- **The 50 best distinct sets** are in `anneal_best50.jsonl`.
  - Each has exactly one convex 7-gon.
  - They are sorted by fewest convex hexagons, from 11,739 to 19,100.
  - Each was checked exactly for general position and recounted by two methods: `cgon` and the
    Python cups/caps counter. The two agree on all 50.
- **Their deletions are saturated.** The 304 heptagon-free 32-point deletions of these 50 sets
  were all swept exhaustively. They have 0 m = 0 faces, and the m = 1 median is 512.

## 5. Exact verification

No set reached zero, so nothing needed the zero-set triple check (`src/triple_check.py`). The
following were checked exactly:
- every walk state was re-checked heptagon-free by `cgon` before it was swept;
- every anneal result's c7 was recounted by `cgon`;
- the 50 best sets were checked by `cgon` and by an exact Python cups/caps count with general
  position checked on Python integers.

## Scope (do not overstate)

- **Saturation is per set.** "Saturated" means that one explicit integer 32-point set admits no
  33rd point without a convex 7-gon. The full arrangement was swept, so this holds for every real
  position of the new point, but it says nothing about other realizations of the same order type.
- **Number of sets checked.** 1,918 + 9,624 + 4,384 + 300 + 304 32-point sets were checked this
  way, about 16.5k in all.
- **Annealing is a local search.** A minimum energy of 1 in 386 runs is not evidence that 0 is
  impossible.
- **Plan gate #3.** The walk was not ≥ 3× faster than the baseline, and the m = 1 tails are not
  heavier than the k = 6 null. By the plan's own rule this line should stop.

## Files

- `env.txt`: execution environment, before and after the restart.
- `calib/`: calibration JSONs.
- `seedsweep/`: per-deletion sweep statistics.
- `summary.json`: all statistics.
- `anneal_best50.jsonl`: the 50 best sets.
- `interim/`: phase-1 summary.
- `logs/progress.txt`, `logs/*.log`, and `logs/runs/*.tar.gz` (walk, multi-start walk, baseline
  and annealing records, including the points of every annealing result).
- `src/`: all code.

## Reproduction

```
sh src/build.sh
DWORK=/tmp NPROC=4 python3 src/calib.py
python3 src/calib_m0.py calib/satcount_m0_validation.json 4
python3 src/check_seeds.py calib/seeds_check.json ../../inputs/nearfull_p2c.txt ../../inputs/nearfull_p2d.txt
S="../../inputs/nearfull_p2c.txt ../../inputs/nearfull_p2d.txt int:calib/alphaevolve_int.txt"
python3 src/seedsweep.py RUNS/seedsweep 3 $S
python3 src/walk.py RUNS/walk 0 1 random 3600 11 $S ; python3 src/walk.py RUNS/walk 1 1 greedy 3600 12 $S
python3 src/baseline.py RUNS/baseline 0 3600 13
MAXLEN=15 ONE_PER_SEED=1 python3 src/walk.py RUNS/walkms {0,1} 2 random 4200 {21,22} $S
python3 src/anneal33.py RUNS/anneal W SECONDS 100W $S        # W = 0..9
NPROC=4 python3 src/summarize.py RUNS . 300
```

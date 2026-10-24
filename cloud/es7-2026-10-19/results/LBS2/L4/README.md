# LBS2 L4 (walk32): exact one-point saturation of heptagon-free 32-point sets

Task: `results/LBS2/TASK.md` at cbe809a1, with V = L4, STRATEGY = walk32, H = 3.0. Machine: 4-core
x86_64 cloud VM (`env.txt`). Wall time 05:51 to 08:50 UTC on 21 Oct 2026. The workers ran from
05:54 to 08:36.

## Result

**27,449 heptagon-free 32-point sets were tested. They have 25,298 distinct order types. Every one
is saturated.** For every set, `bad_candidates = 0` and `faces_euler == faces_hit`. So for none of
these sets is there a point p (off the lines through pairs of S) with S + p free of convex
7-gons. No counterexample was found, and no set needed step 4.

## Tools and smoke test (`tools.txt`)

- `sat`: `tools/trackA/sat.c`, built with `gcc -O2` and unchanged. `tools/realizer/saturate.py`
  is also unchanged; it re-checks general position and the largest convex subset exactly in
  Python before it calls `sat`.
- **Smoke test.** `saturate.py` on `results/LBS/L2/bases/base000.txt`, the minimal Erdős–Szekeres
  witness. It gives: largest convex subset 6, `faces_euler == faces_hit == 108875`, and
  0 bad candidates, so the set is saturated.
- `gen_es.py`: ES 32-point construction with mild random gaps and offsets. It is adapted from
  L2's `gen_bases.py` (credit L2), but it does not scale and it keeps |coord| < 2^24.
  - MILD=0 is the minimal witness, which has the same order type as L2's base000.
  - MILD=1 and MILD=2 add random gaps (2,252 distinct bases in total).
- `walk.c`: the random walk.
  - Setup: it centres the base and scales each axis by an integer factor so that the
    coordinates fill about 2^25. The order type does not change.
  - Moves: it moves one point at a time by a Gaussian step of r·(nearest-neighbour distance),
    with r log-uniform in [RMIN, 1].
  - Acceptance: a move is kept only if |coord| < 2^26 < 2^27, the set stays in general position
    (__int128), and the largest convex subset stays ≤ 6 (anchor DP).
  - Variant `walk32-lowc6` (40% of runs from epoch 4): an extra Metropolis bias towards few
    convex 6-gons, with β ∈ {10, 100, 1000} per 1000 six-gons.
- `vfy4.c`: an independent exact check, with no DP.
  - General position: tested on all triples.
  - Convex-subset counts: the numbers of convex 5-, 6-, 7- and 8-subsets, by brute-force
    enumeration with triangle-containment tests.
  - Order-type hash: the lexicographically least chirotope over all hull vertices and both
    orientations, so it is invariant under relabelling and reflection.
  - Cross-checks:
    - c5 and c6 agree with L2's `lbs count` on base000 and on L2's 33-point best set
      (c7 = 1 detected).
    - The hash stays the same under relabelling, reflection and scaling.
    - The DP 6-gon count in `walk.c` agrees with vfy4.
- Every recorded set therefore passed three independent exact checks:
  1. vfy4: general position, c7 = 0.
  2. `saturate.py`'s Python checks: general position, largest convex subset = 6.
  3. `sat.c`'s load-time checks.
- `driver.py` / `run.sh`: 4 workers. `sync.py`, `analyze.py`, `make_out.py` and `commit.sh`
  handle bookkeeping.

## Data

- `out.jsonl` has one line per set with these fields:
  - epoch, generator, worker, run, base and walk seeds, steps, rmin, beta, walk length;
  - order-type hash, c5, c6, hull size, max |coord|;
  - faces, faces_hit, `faces_euler_eq_hit`, `bad_candidates`, `saturated`, seconds;
  - `gp_and_c7` = [vfy4 GP, vfy4 c7, Python GP, Python largest convex subset].
- `data/*.jsonl.part*.gz` holds the full records, including the raw vfy4 output and walk
  statistics.
- `data/*sets*.part*.gz` holds the coordinates of every tested set: the hash, then 32 points.
- `data/summary.json` is the output of `analyze.py`.
- **Epochs.** Epoch 1 lines were recovered from the workers' open file descriptors after a git
  autostash had replaced the tracked files. After that, output went to an untracked `live/`
  and was copied into append-only chunks. Epochs 1–2 skipped repeated order types within a
  worker. Epochs 3–4 test every snapshot, because saturation depends on the realization and
  not only on the order type. Epoch 4 adds the lowc6 variant.

## Distributions (all 27,449 sets)

| | sets | distinct OT | saturated | c6 min / p10 / median / p90 / max |
|---|---|---|---|---|
| walk32 | 20,359 | 18,238 | 20,359 | 10,932 / 15,702 / 22,293 / 33,739 / 39,648 |
| walk32-lowc6 | 7,090 | 7,060 | 7,090 | 5,327 / 6,815 / 10,298 / 15,732 / 35,302 |

- **c6 histogram** (bins of 5,000):

  | c6 | sets |
  |---|---|
  | 5k–10k | 3,332 |
  | 10k–15k | 3,940 |
  | 15k–20k | 7,820 |
  | 20k–25k | 3,652 |
  | 25k–30k | 3,349 |
  | 30k–35k | 3,957 |
  | 35k–40k | 1,399 |

  The ES witness itself has c6 = 39,648 and c5 = 49,884. The lowest is c6 = 5,327 (c5 = 17,306,
  hull 3), from a β = 1000 walk of 30,000 moves.
- **Faces:** min 108,875, median 109,335, max 109,337.
  - The minimum, 108,875, is the ES witness, with 388 parallel line pairs.
  - The maximum, 109,337 = 1 + 496 + 32·30 + 107,880, is a simple arrangement with no parallel
    lines and no concurrences off S. 12,245 sets reach it.
- **Hull sizes:** 3: 2,302; 4: 9,201; 5: 12,056; 6: 3,890.
- **Walk lengths:** 1 to 60,000 accepted moves (median 600).
- **Bases:**
  - minimal witness: 4,633 sets;
  - mild: 13,806;
  - L2-like: 9,010.
- **Cost:** mean 0.89 s per set for vfy4 plus saturate.py with sat.c.

## Remarks

- Saturation was robust everywhere. It held near the ES construction, and it held after long
  walks that removed three quarters of the convex 6-gons. Fewer 6-gons did not produce a single
  face whose point avoids a convex 7-gon.
- 1,045 order types were tested in two or more different realizations, each time with the
  same result (saturated). Saturation is a property of the realization, but here it never
  differed.
- All sets come from walks started at ES realizations. Long walks change the order type a
  lot: 25,298 distinct hashes. Still, they may stay in a neighbourhood of the ES family. This
  run says nothing about heptagon-free sets that are far from it (strategy anneal32 covers
  those).

# LBS2 L5: exact one-point saturation of heptagon-free 32-point sets (strategy anneal32)

Machine L5 (4 cores, see `env.txt`), budget 3.0 h (05:51 to 08:51 UTC, 21 Oct 2026), task file at
commit cbe809a1.

**Result: no extension found.** 1,728 heptagon-free 32-point sets were tested. They have 1,526
distinct order types, and every one of the 1,526 is saturated: `bad_candidates = 0` and
`faces_euler == faces_hit` for each. So none of these sets extends to a 33-point set without a
convex 7-gon. Step 4 (constructing a counterexample) never applied.

## Tools and smoke test (`tools.txt`)

- `sat`: `tools/trackA/sat.c`, built unchanged with `gcc -O2`. `saturate.py`: `tools/realizer/saturate.py`, unchanged.
- **`sat_wide`** (`src/sat_wide.c`, built with clang 18): sat.c with `_BitInt(256)` / `_BitInt(512)`
  in place of int64 / `__int128`, input read as long long, and coordinate bound 2^60 instead of 2^27.
  Nothing else changed. The header comment gives the degree bound: every intermediate value is
  < 2^250, well below 2^511. `src/saturate_wide.py` is saturate.py with the 2^60 bound.
  sat_wide was used for the 1,081 order types whose sets have |coord| >= 2^27. These are mostly
  L2's multi-scale sets, with coordinates up to about 1.6e11.
  - The task suggested two options. Reducing coordinates was tried first: uniform scaling failed on
    the L2 sets, and the F realizer did not realize a test set in 30 CPU-s. So I extended sat.c instead.
- Smoke tests:
  - On the Erdős–Szekeres 32-point witness (`gen_bases.witness(7, Minimal())`, |coord| <= 110,353):
    sat and sat_wide both give 108,875 faces, all hit, and 0 bad candidates (saturated).
  - The same set scaled by 2^20 and shifted (|coord| 1.2e11) gives identical output under sat_wide.
  - sat and sat_wide produce byte-identical stdout (apart from timing) and byte-identical
    bad-candidate files on the witness with K = 6 and 7, and on its first 14 points with K = 6.
    That last case has 729 bad candidates, so it exercises the reporting path.
- **`vfy7`** (`src/vfy7.c`): my own exact checker, independent of the generators. It tests general
  position with `__int128` orientations and counts convex k-subsets (k = 5..8) by depth-first
  extension, using the rule that a set is in convex position iff all its 4-subsets are. It
  reproduces L1's and L2's published counts (c7 = 1 with c6 = 20,891 and 10,075).
- Order-type hash (`src/pipeline.py: ot_hash`): canonical form under relabelling and reflection.
  For each hull vertex h and each orientation, label h first and the other points by angle around
  h; take the minimal sign string; then sha256, truncated to 16 hex digits.

## Generators (strategy anneal32)

1. **`anneal32`** (`src/anneal32.cpp`, my own; the counting DP follows the scheme of L1's `lbs2.cpp`).
   It anneals 32 random integer points (|coord| < 2^26) down to 0 convex 7-gons and rejects any
   collinear triple.
   - When a run hits 0, it writes the set, then takes a random walk that keeps c7 = 0 and writes 4
     more snapshots, 1,500 accepted moves apart.
   - v1 used Gaussian moves only. Its best was 1 in 20 minutes, never 0, so I stopped it (seeds 11,
     12 and 21).
   - v2 adds contraction moves (30%): a point moves toward another point by a log-uniform fraction.
     - Random starts (seeds 13, 14, 15): 74 of 90 runs reached 0, after a median of 0.46 M steps
       (range 0.05 to 2.0 M).
     - Start-file mode (seed 22): a 33-point L1/L3 near-miss with a random point dropped (41 start
       sets; L3's sets have 3 disjoint 7-gons). 7 of 21 runs reached 0.
   - Output: 405 sets (81 zero runs × 5 snapshots), all of different order types.
2. **Near-miss subsets** (`src/nearmiss.py`): all 33-point sets with 1 to 3 convex 7-gons in
   `results/LBS/L1` (`snap/*.best.txt`), L2 (`best.txt`, `out/*.best.txt`, `out/*.sets`) and L3
   (`runs/*_near.txt`, `*_best*.txt`), as checked out at the start: 223 sets in total.
   - Each convex 7-gon was listed with vfy7. Every point lying in all of a set's 7-gons was dropped
     in turn, and a subset was kept if vfy7 gives c7 = 0.
   - This gave 1,323 subsets: 14 from L1 and 1,309 from L2.
   - L3 contributes none directly: its 45 sets all have 3 pairwise disjoint 7-gons, so no single
     point can be dropped. They were used as annealing starts instead (item 1).

## Tests (`out.jsonl`, one line per set; `summary.txt`)

Each set went through three checks:
1. vfy7: general position, and c7 = 0 by an exact count.
2. Exact order-type hash.
3. `saturate.py --K 7`, which runs its own exact checks (general position, largest convex
   subset = 6) and then the saturation test, on `sat`, or on `sat_wide` for |coord| >= 2^27.

A set whose order type had already been tested is recorded as a duplicate and was not run again.
Saturation depends only on the order type.

| source | sets | distinct order types tested | c6 min / median / max |
|---|---|---|---|
| anneal32, random starts | 370 | 370 | 8,171 / 15,841 / 34,535 |
| anneal32, from L1/L3 near-misses | 35 | 35 | 11,234 / 17,509 / 27,500 |
| near-miss subsets, L1 | 14 | 14 | 16,665 / 22,715 / 24,520 |
| near-miss subsets, L2 | 1,309 | 1,107 (202 duplicates) | 6,162 / 11,154 / 39,648 |
| **total** | **1,728** | **1,526** | |

c6 distribution (the number of tested order types in each range):

| c6 | anneal random | anneal from near-miss | L1 | L2 |
|---|---|---|---|---|
| 5k to 10k | 12 | 0 | 0 | 274 |
| 10k to 15k | 136 | 8 | 0 | 568 |
| 15k to 20k | 139 | 19 | 7 | 139 |
| 20k to 25k | 70 | 6 | 7 | 79 |
| 25k to 30k | 9 | 2 | 0 | 33 |
| 30k to 40k | 4 | 0 | 0 | 14 |

Face counts (`faces_euler`, always equal to `faces_hit`):
- 1,452 of 1,526 have 109,337 faces. This is the count when no three of the 496 lines meet off S
  and no two are parallel: 1 + 496 + 32·30 + C(496,2) − 32·C(31,2) = 109,337.
- The other 74 lie between 109,317 and 109,336. These have parallel line pairs or concurrent lines
  (the full distribution is in `summary.txt`).
- The ES witness smoke test has 108,875 faces because of its 388 parallel pairs.

Every tested set:
- has largest convex subset 6;
- is in general position under both vfy7 and saturate.py;
- has `bad_candidates = 0` and `saturated = true`.

The sat CPU time was about 1 s per set, or about 4 s with sat_wide.

## Anything unusual

- Nothing in the saturation results: all 1,526 order types are saturated.
- The annealed sets look different from the L2 sets. Their median c6 is 15.8k against 11.2k for
  L2's ES-derived subsets. The lowest c6 seen was 6,162, in an L2 subset. The ES witness itself
  has 39,648.
- **Lost results during pushes.** Until 07:21 I pushed with `git pull --rebase --autostash` from the
  live checkout, and the autostash overwrote files that running processes were appending to.
  - Two lines of `run/out_near.jsonl` were lost. Both sets were re-run (saturated).
  - Most of `run/pipeline_near.log` was lost; `out_near.jsonl` is the record.
  - No anneal output was lost: 81 zero runs × 5 = 405 sets, all present.
  - From 07:31 on, commits were made from a separate worktree.
  - `run/out_anneal.jsonl` has a few duplicate ids, because two conversion loops overlapped
    briefly after the restart. `out.jsonl` keeps the first line for each id.

## Files

- `out.jsonl`: one line per set, including its coordinates (`pts`).
- `summary.txt`: output of `src/summary.py`.
- `tools.txt`, `env.txt`.
- `src/`: `anneal32.cpp` (v2), `vfy7.c`, `sat_wide.c`, `saturate_wide.py`, `pipeline.py`,
  `nearmiss.py`, `anneal2cands.py`, `summary.py` and `run.sh` (with a note on the 06:26 v1 → v2 switch).
- `run/`:
  - raw annealer output: `a*.sets` and `a*.sets.log`;
  - pipeline inputs and outputs: `cands_*.jsonl` and `out_*.jsonl`;
  - the annealing start sets: `starts.txt`;
  - the smoke-test point sets.

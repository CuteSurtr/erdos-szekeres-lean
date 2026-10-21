# C3WAVE2 / K17: shard 17 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 10 of my 34 roots are closed, 3 are partial, and 21 were not reached. No SAT. No proof rejection.**
All 308 certified nodes have lrat-check (E2 patch) `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
Two worker restarts of the cloud session killed the runner (see Incidents), which cost about 20 minutes of solving time.

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Started 00:24:50 UTC on 2026-10-21, budget H = 1.5 h, END = 01:39:50, stopped at 01:41.
Tools as in `results/C3WAVE1/C00/README.md` (`tools.txt`):
- C3-S tools: worktree of `132398c` (8dc27c3 before the rewrite) at /opt/c3s, used unmodified; live files in /opt/work.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (`make cake_lpr`; its example prints `s VERIFIED UNSAT`);
  drat-trim lrat-check 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`. Sanity check: on {1},{-1}, the LRAT `3 0 0`
  is rejected by both (`c NOT VERIFIED`; cake_lpr "pivot must be non-zero") and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 17 (mod 40): 34 roots (`roots.tsv`).
- `runner.sh` (the K00 runner with my start time): `close_tree.py … R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(0.17, hours left before END).

## Per root (depth = number of layers; roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_5s0-6s0 | **closed** | d2: 1 | – | 31 | 36 |
| 2 | 0s0-2s0_1s0-3s0 | **closed** | d2: 1 | – | 16 | 32 |
| 3 | 0s0-2s0_3s1-4s1 | **closed** | d2: 1 | – | 10 | 26 |
| 4 | 0s0-2s0_5s1-10s1 | **closed** | d2: 1 | – | 37 | 32 |
| 5 | 0s0-2s0_9 | partial | d3: 117 | d2: 1 | 2399 | 2262 |
| 6 | 0s0-2s1_3s0-5s0 | **closed** | d2: 1 | – | 43 | 37 |
| 7 | 0s0-2s1_4s1-5s1 | **closed** | d2: 1 | – | 37 | 36 |
| 8 | 0s0-2s1_6s1-10s1 | **closed** | d2: 1 | – | 225 | 44 |
| 9 | 0s0-3s0_1s0-4s0 | **closed** | d2: 1 | – | 21 | 33 |
| 10 | 0s0-3s0_2s0-8s1 | **closed** | d2: 1 | – | 82 | 38 |
| 11 | 0s0-3s0_4s1-9s0 | **closed** | d2: 1 | – | 58 | 35 |
| 12 | 0s0-3s0_7 | partial | d3: 19 | d2: 1 | 1469 | 533 |
| 13 | 0s0-3s1_1s0-7s1 | partial | d4: 162 | d2: 1, d3: 7 | 859 | 1925 |
| 14–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node, not wall-clock (3 jobs share 4 cores).

- Root 5 `0s0-2s0_9` (one-orbit layer {9}): pre-split into 120 depth-3 children; 117 certified (all at the 300 s cap), 3 not finished (the run was killed).
  `close_tree.py` checks `--hours` only between batches, so this batch ran past its 10-minute slice (00:31 to 00:58).
- Root 12 `0s0-3s0_7` (one-orbit layer {7}): pre-split into 120 depth-3 children; 19 certified, the rest not finished (killed at about 01:20, slice used up).
- Root 13 `0s0-3s1_1s0-7s1`: UNKNOWN at 300 s, split into 91 depth-3 children; 7 of them are one-orbit and were pre-split (66 depth-4 children each).
  162 depth-4 nodes certified; the rest were not attempted when I stopped the run at the budget.
  Its slice ended at about 01:32, but the batch kept running until I killed it at 01:41.

Totals: 308 certified nodes (d2: 10, d3: 136, d4: 162), 1 UNKNOWN record (root 13 at 300 s), 10 split records (3 roots, 7 pre-split depth-3 nodes).
Summed solve time 5,287 s, check time 5,069 s. Per-root breakdown in `summary.jsonl` (made by `summary.py`).

**Closed roots (10):** 0s0-1s1_5s0-6s0, 0s0-2s0_1s0-3s0, 0s0-2s0_3s1-4s1, 0s0-2s0_5s1-10s1, 0s0-2s1_3s0-5s0, 0s0-2s1_4s1-5s1, 0s0-2s1_6s1-10s1, 0s0-3s0_1s0-4s0, 0s0-3s0_2s0-8s1, 0s0-3s0_4s1-9s0.

**Partial roots (3):** 0s0-2s0_9, 0s0-3s0_7, 0s0-3s1_1s0-7s1. Their records are in `out.jsonl`, so a later wave can resume them.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. Every UNSAT record is certified by both checkers.
- Memory: up to about 9 GB used of 15 GB with 3 jobs; no problems.

## Incidents (affect time only, not results)

1. About 00:58 UTC the cloud session's worker process restarted and killed the runner and all its children during root 5. That root's slice was already used up,
   so I restarted at root 6 with `runner_resume.sh` (the same runner, starting at the 6th root).
2. About 01:20 the same thing happened during root 12 (slice used up). I restarted at root 13 with `runner_resume2.sh`.
3. At 01:41 I stopped root 13 by hand because the budget had run out. In each case the solves still running were lost, and their nodes have no record. `out.jsonl` is complete JSON (319 lines).

## compose.py

compose.py was still running at the commit time; its output is added in the next commit (`compose.txt`).

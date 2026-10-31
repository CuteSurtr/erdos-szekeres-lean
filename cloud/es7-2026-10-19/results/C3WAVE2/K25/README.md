# C3WAVE2 / K25: shard 25 of 40, 3-fold class (m = 11, k = 7)

**Result: 4 of my 34 roots are closed and 1 is partial. The other 29 were not reached. There was no SAT,
no proof rejection and no memory problem.**

## Setup

One cloud VM with 4 cores, 15 GB RAM and no swap (`env.txt`). It started at 00:27:50 UTC on 2026-10-21, with a 1.5 h budget.
The runner's END was 01:42:50. `tools.txt` lists the tools:

- C3-S tools come from a worktree of `132398c` (8dc27c3 before the rewrite) at `/opt/c3s`, used unmodified.
- CaDiCaL 3.0.1, commit c6073042.
- cake_lpr a36874a8 (`make cake_lpr`). Its example prints `s VERIFIED UNSAT`.
- lrat-check from drat-trim 2e3b2dc, with the E2 patch. Sanity check: the LRAT `3 0 0` on {1},{-1} is rejected
  by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`. It matches.
- Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 25 (mod 40), 34 roots (`roots.tsv`).
- The runner is `runner.sh`. It runs `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
  with S = min(0.17, hours left).

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s0-10s0 | **closed** | d2: 1 | 0 | 105 | 41 |
| 2 | 0s0-2s0_1s0-8s0 | **closed** | d2: 1 | 0 | 111 | 45 |
| 3 | 0s0-2s0_3s1-9s1 | **closed** | d2: 1 | 0 | 98 | 41 |
| 4 | 0s0-2s0_6s0-10s0 | **closed** | d2: 1 | 0 | 26 | 31 |
| 5 | 0s0-2s1_1s0-3s1 | partial | d3: 38, d4: 462 | d2: 1 (timeout at 300 s); d3: 7 (pre-split, one-orbit) | 3661 | 7543 |
| 6–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock time.

Root 5 hit the 300 s cap at depth 2 (UNKNOWN), so it was split into 91 depth-3 children. 7 of those are
one-orbit layers, and they were pre-split into depth-4 children. All 462 depth-4 children were certified. Of the
84 depth-3 nodes that were solved directly, 38 were certified and 46 are open: they were never attempted
or were in flight at the stop. None timed out at depth 3.

**Why only 5 roots ran.** `close_tree.py` checks `--hours` only between layers. Each layer's whole frontier
is submitted at once, so root 5's 10-minute slice ran from 00:38 to 01:44. That covered its full depth-4
layer (462 nodes) and part of its depth-3 layer. At 01:44:47 I killed the driver by hand because the
budget was used up. The nodes in flight were discarded and nothing was written for them. Every finished
record is in `out.jsonl`, so the root can be resumed.

## Totals

There are 504 certified nodes: 4 at d2, 38 at d3 and 462 at d4. Each one has both `c VERIFIED` (lrat-check, E2 patch) and
`s VERIFIED UNSAT` (cake_lpr). `out.jsonl` also holds 1 UNKNOWN at d2 (300 s) and the split records. Summed solve
time is 4002 s and summed check time is 7702 s. `summary.jsonl` gives the per-root breakdown.

`compose.txt` reports `certified_nodes: 504, class_covered: false`, as expected. compose recomputed the
CNF sha256 of every certified node and found no mismatch.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem. Peak use was about 4 GB per cake_lpr.

Closed roots: 0s0-1s1_6s0-10s0, 0s0-2s0_1s0-8s0, 0s0-2s0_3s1-9s1, 0s0-2s0_6s0-10s0.
Partial root: 0s0-2s1_1s0-3s1.

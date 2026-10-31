# C3WAVE2 / K15: shard 15 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 2 of my 34 roots are fully closed (`0s0-1s1_4s1-9s1`, `0s0-2s0_1s0-10s0`). Roots 3 to 34 were not reached.
No SAT. No proof rejection. No memory problem.**

## What ran where

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`), 00:25:07 to about 01:55 UTC on 2026-10-21 (budget 1.5 h).
TASK.md at 852bee7, followed as written. Tools as in `results/C3WAVE1/C00/README.md` (`tools.txt`):

- C3-S tools: git worktree of 132398c (8dc27c3 before the author rewrite) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); the bundled example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`.
  Sanity check on the CNF {1},{-1}: LRAT `3 0 0` is rejected by both (lrat-check `c NOT VERIFIED`,
  cake_lpr `pivot must be non-zero`); `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 15 (mod 40): 34 roots (`roots.tsv`).
- Runner: `runner.sh`, `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
  S = min(0.17, hours left before END), END = 01:40:07 UTC.

## Per root (depth = number of layers; roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_4s1-9s1 | **closed** | d3: 84, d4: 462 | d2: 1 (UNKNOWN at 300 s, 91 children); d3: 7 one-orbit pre-split (66 children each) | 4107 | 7931 |
| 2 | 0s0-2s0_1s0-10s0 | **closed** | d2: 1 | 0 | 176 | 34 |
| 3–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 1 ran from 00:27:17 to 01:38:50 (72 min), not the 10-minute slice: `close_tree.py` checks `--hours`
only between rounds, and the second round (84 depth-3 and 462 depth-4 nodes after the depth-2 timeout) was
submitted as one batch, which runs to completion. It finished with `open_frontier: 0`. Root 2 started at
01:38:50 with S = 0.021 h and closed at the root in one solve (01:42:21); the runner then stopped at END.
Solve and check times are summed per node (3 jobs on 4 cores), not wall-clock.

## Totals

| depth | certified | split | open |
|-------|-----------|-------|------|
| 2 | 1 | 1 (timeout at 300 s) | 32 roots not reached |
| 3 | 84 | 7 (pre-split) | 0 |
| 4 | 462 | 0 | 0 |

547 certified nodes, every one with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. One UNKNOWN record
(root 1 at 300 s). Largest proof 327,537,856 bytes; longest solve 176 s. `out.jsonl`: 556 records
(548 solve records, 8 split records), resumable.

## compose.py

`compose.txt`: `{"certified_nodes": 547, "class_covered": false, "uncovered_frontier_nodes": 313, ...}`.
As expected, the class is not covered (this machine holds 1/40 of the wave-2 roots). compose recomputed the CNF
sha256 of all 547 certified nodes.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: peak use seen about 9 GB of 15 GB; no OOM.

Closed roots: `0s0-1s1_4s1-9s1`, `0s0-2s0_1s0-10s0`. Partial roots: none. Not reached: the other 32 rows of `roots.tsv`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl`, `driver.log` (last 200 lines), `compose.txt`, `README.md`.

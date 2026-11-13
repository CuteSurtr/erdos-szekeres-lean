# C3WAVE2 / K02: shard 2 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 1 of my 34 roots is closed (`0s0-1s1_3s0-9s1`). One is partial (`0s0-1s1_8`). The other 32 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM with 4 cores, 15 GB RAM and no swap (`env.txt`). It ran from 00:22:09 to 01:37:09 UTC on 2026-10-21 (END = start + 1.5 h − 15 min).
- The C3-S tools come from a worktree of `132398c` (8dc27c3 before the rewrite) at `/opt/c3s`, used unmodified. Live files are in `/opt/work`.
- Tools: CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8, whose example prints `s VERIFIED UNSAT`; lrat-check 2e3b2dc with the E2 patch. The sanity check passed: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Roots: the rows of `roots.tsv` with idx ≡ 2 (mod 40), 34 roots. `runner.sh` is the task's runner (`--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`).

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_3s0-9s1 | **closed** | d2: 1 | 0 | 92 | 50 |
| 2 | 0s0-1s1_8 | partial | d3: 57 | d2: 1 (pre-split, 120 children); d3: 8 (timeout at 300 s) | 10434 | 2011 |
| 3–34 | (`roots.tsv`) | not reached | – | – | – | – |

Root 2 at the stop: 57 of 120 depth-3 children were certified and 8 timed out at 300 s and were split. Their depth-4 children were never attempted. The remaining 55 depth-3 children were in flight or queued when the run was stopped, so they have no record.

Totals: 58 certified nodes, all with `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr). There are also 8 UNKNOWN records at the 300 s cap.

## The 10-minute slice was not enforced

`close_tree.py` checks `--hours` only between tree levels. It submits a whole level at once: the 120 pre-split children of `0s0-1s1_8` ran with 3 jobs. So root 2 started at 00:26:26 and was still on its first level at END, about 70 minutes later. To stay within the time budget, I killed the driver and its solvers at END (01:37). Records already in `out.jsonl` are kept, so the root can be resumed; in-flight results were lost. Other machines whose first pre-split root is a one-orbit layer will see the same thing.

## compose.py

Output in `compose.txt`: `certified_nodes 58, class_covered false, uncovered_frontier_nodes 224`. This is expected for one shard. compose recomputed the CNF sha256 of all 58 certified nodes.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.

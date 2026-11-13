# C3WAVE2 / K03: shard 3 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: 7 of my 34 roots are closed, root 8 (`0s0-2s1_5s1-8s0`) is partial, and roots 9–34 were not reached.
No SAT. No proof rejection. No memory problem.** All 486 certified nodes have `c VERIFIED` (lrat-check, E2 patch)
and `s VERIFIED UNSAT` (cake_lpr).

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`), 00:21:50 to 01:51:50 UTC on 2026-10-21 (H = 1.5 h;
END = 01:36:50). Task file at 852bee7.

- C3-S tools: worktree of commit `132398c` (8dc27c3 before the author rewrite) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); the bundled example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`
  (a normal diff, applied with `patch`). Sanity check on {1},{-1}: LRAT `3 0 0` rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none -o /opt/work/base.cnf` (the script needs `-o`): `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 3 (mod 40): 34 roots (`roots.tsv`).
- `runner.sh`: per root `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
  S = min(0.17, hours left before END).

## Per root (depth = number of layers; roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_3s1-10s0 | **closed** | d2: 1 | 0 | 54 | 40 |
| 2 | 0s0-1s1_8s0-10s0 | **closed** | d2: 1 | 0 | 19 | 33 |
| 3 | 0s0-2s0_3s0-10s1 | **closed** | d2: 1 | 0 | 15 | 33 |
| 4 | 0s0-2s0_4s1-8s0 | **closed** | d2: 1 | 0 | 90 | 43 |
| 5 | 0s0-2s0_7s0-9s1 | **closed** | d2: 1 | 0 | 74 | 41 |
| 6 | 0s0-2s1_1s1-5s1 | **closed** | d2: 1 | 0 | 58 | 37 |
| 7 | 0s0-2s1_4s0-10s1 | **closed** | d2: 1 | 0 | 76 | 41 |
| 8 | 0s0-2s1_5s1-8s0 | partial | d3: 17, d4: 462 | d2: 1 (timeout at 300 s); d3: 7 (pre-split) | 3151 | 7291 |
| 9–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node (3 jobs on 4 cores, so not wall-clock).

Root 8 timed out at 300 s and was split into 91 depth-3 children: 84 two-orbit children and 7 one-orbit
children (layers {1},{3},{4},{6},{7},{9},{10}), each pre-split into 66 depth-4 children (462). All 462 depth-4
nodes are certified; 17 of the 84 depth-3 two-orbit nodes are certified, and **67 depth-3 nodes are still open**
(never finished; one or more were in flight at the stop and left no record). No node at depth 3 or 4 timed out.

The 10-minute slice did not hold for root 8: `close_tree.py` checks `--hours` only between levels, and it submits
a whole level at once, so the depth-3/4 level (546 nodes) ran from 00:39 until I stopped it. At END (01:37:05) I
killed the runner, the driver and its solvers by hand (`=== KILLED` line in `driver.log`). Every finished node
was already in `out.jsonl` (written per result), so root 8 can be resumed from it.

## Totals

| depth | certified | split | open |
|-------|-----------|-------|------|
| 2 | 7 | 1 (timeout) | 26 roots not reached |
| 3 | 17 | 7 (pre-split) | 67 |
| 4 | 462 | 0 | 0 |

486 certified nodes; `out.jsonl` has 486 UNSAT records (all certified), 1 UNKNOWN (root 8 at 300 s) and 8 split records.

## compose.py

`compose.txt`: `{"certified_nodes": 486, "class_covered": false, "uncovered_frontier_nodes": 526, ...}`.
As expected the class is not covered (this is 1/40 of the wave). compose recomputed the CNF sha256 of all 486
certified nodes from the base CNF and the node names.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: peak about 9 GB used of 15 GB with 3 jobs; no failures.

Closed roots: 0s0-1s1_3s1-10s0, 0s0-1s1_8s0-10s0, 0s0-2s0_3s0-10s1, 0s0-2s0_4s1-8s0, 0s0-2s0_7s0-9s1,
0s0-2s1_1s1-5s1, 0s0-2s1_4s0-10s1. Partial: 0s0-2s1_5s1-8s0.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`.

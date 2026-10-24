# C3WAVE1 / C22: machine 22 of 24, wave 1, 3-fold class (m = 11, k = 7)

Status: **not closed.** 10 of my 67 roots are fully closed. Root 11 (`0s0-1s1_6`) is partly closed. Roots 12–67 were not started. No SAT. One proof was not accepted; the cause was memory, and the node was later certified.

## What ran where

- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Ran 2026-10-20 from 07:38 to 11:13 UTC.
- Tools (`tools.txt`):
  - CaDiCaL 3.0.1 at `c60730422e75`
  - cake_lpr at `a36874a8b750`. The bundled example prints `s VERIFIED UNSAT`.
  - drat-trim lrat-check at `2e3b2dc0ecf9`, with `results/E2/tools/lrat-check-E2.patch` applied.
- C3-S/C3a tools: worktree at `8dc27c3`, unmodified. `/opt/work` was writable, so there is no diff.
- Base CNF: `gen_case.py 11 7 none`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the 67 depth-2 nodes with index ≡ 22 (mod 24) (`roots.tsv`). They come from the SHARD expression in `close_tree.py` and are identical to the sorted depth-2 rows of `manifest_depth2.tsv`.
- Command, one root at a time:
  `close_tree.py base.cnf out.jsonl ROOT --jobs 4 --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  From 09:52 it ran with `--jobs 3` (see below). The driver was stopped by `timeout` at 11:13 (rc 124).
- Files:
  - `out.jsonl`: all records.
  - `driver.log`: driver output plus runner markers.
  - `compose.txt`: compose.py output.
  - `summary.md`: tables.
  - `recheck_*.txt`: the proof re-check.

## Per root

| root | status | certified by depth | splits (pre-split) | open leaves | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-1s0_2s1-4s0 | CLOSED | d2:1 | 0 | 0 | 75 | 37 |
| 0s0-1s0_3s0-8s1 | CLOSED | d2:1 | 0 | 0 | 33 | 34 |
| 0s0-1s0_4s0-7s0 | CLOSED | d2:1 | 0 | 0 | 4 | 19 |
| 0s0-1s0_5s0-7s1 | CLOSED | d2:1 | 0 | 0 | 61 | 38 |
| 0s0-1s0_6s1-10s0 | CLOSED | d2:1 | 0 | 0 | 60 | 38 |
| 0s0-1s0_8s0-9s0 | CLOSED | d2:1 | 0 | 0 | 5 | 20 |
| 0s0-1s1_2s0-7s1 | CLOSED | d2:1 | 0 | 0 | 281 | 50 |
| 0s0-1s1_3s0-4s0 | CLOSED | d2:1 | 0 | 0 | 31 | 38 |
| 0s0-1s1_3s1-9s0 | CLOSED | d2:1 | 0 | 0 | 60 | 39 |
| 0s0-1s1_4s1-8s1 | CLOSED | d2:1 | 0 | 0 | 198 | 48 |
| 0s0-1s1_6 | open | d3:112, d4:310 | 9 (1) | 418 | 28685 | 11088 |
| the other 56 roots (index 286 … 1606) | not started | – | – | – | – | – |

Times are per-node wall-clock sums, with up to 4 nodes running in parallel.

### Root `0s0-1s1_6`

- The root is a single-orbit layer, so it was pre-split into 120 depth-3 children. 112 were certified.
- The other 8 are single-orbit layers `_2, _3, _4, _5, _7, _8, _9, _10`. Each timed out at 300 s and was split into 91 depth-4 children.
- `_2`, `_3` and `_4` are fully closed: 91/91 children each.
- Still open: `_5` (9/91 certified), and `_7`, `_8`, `_9`, `_10` (7/91 each). That leaves 418 depth-4 nodes not yet solved.

## Per depth, all roots

| depth | certified | split | open (not yet solved) |
|---|---|---|---|
| 2 | 10 | 1 | 0 (+56 roots not started) |
| 3 | 112 | 8 | 0 |
| 4 | 310 | 0 | 418 |

`compose.py base.cnf out.jsonl`: `certified_nodes 432`, `class_covered false`, 722 uncovered frontier nodes (as expected for one shard).

## Events

- **SAT:** none.
- **Proof rejection:** `0s0-1s1_6_2_4s1-8s1`. lrat-check said `c VERIFIED`, but cake_lpr printed nothing. At the time 4 cake_lpr processes (heap 12 GB each) were running and about 1 GB was free.
  - Re-run alone: sha256 matched, CaDiCaL UNSAT in 24 s, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`.
  - Cause: memory. I resumed with `--jobs 3`, and the driver itself then certified the node with both checkers.
  - No real rejection.
- **Operational incident:** at 08:13 a `git pull --rebase` in the live checkout replaced `out.jsonl` and `driver.log` with new files. The running driver kept writing to the old, deleted files.
  - I paused the driver, recovered both files intact from `/proc/<pid>/fd` (no record lost; the old content was a prefix of the recovered content), and restarted root `0s0-1s1_6` at 08:24. Nodes that were in flight were re-solved.
  - From then on, commits were made from a separate worktree that copies the results directory.
- Earlier, at 07:52, the first driver run of root `0s0-1s1_3s0-4s0` exited with no output and wrote no record; the cause is not known. A manual test run (outside `out.jsonl`) certified it, and the runner then re-ran it into `out.jsonl`, where it is certified.

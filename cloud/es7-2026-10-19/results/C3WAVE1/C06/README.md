# C3WAVE1 / C06: machine 6 of 24, wave 1, 3-fold class (m = 11, k = 7)

**Summary.** 11 of my 68 roots are fully closed. 1,207 nodes are certified, each accepted by both
cake_lpr (`s VERIFIED UNSAT`) and lrat-check with the E2 patch (`c VERIFIED`). No SAT. No real
proof rejection: the one "PROOF NOT ACCEPTED" was cake_lpr being OOM-killed. The node passed both
checkers when re-run alone. Root 12 (`0s0-1s1_6s0-9s1`) is partly done: 532 nodes certified,
14 depth-3 children not yet tried. Roots 13–68 were never started.

## What ran where

- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). The memory cgroup of the shell is
  limited to 13.4 GB (14,343,688,192 bytes).
- Driver ran from 08:18:26 to 11:55:00 UTC on 2026-10-20 (`run.sh`, `driver.log`).
- Tools (`tools.txt`):
  - C3-S/C3a tools: git worktree of `8dc27c3` at `/opt/c3s`, unmodified. `/opt/work` was
    writable, so there is no path diff.
  - CaDiCaL 3.0.1 `c6073042`.
  - cake_lpr `a36874a8` (`make cake_lpr`). The bundled example prints `s VERIFIED UNSAT`.
  - drat-trim `2e3b2dc` `lrat-check`, with `results/E2/tools/lrat-check-E2.patch` applied.
- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the 68 depth-2 nodes with index ≡ 6 (mod 24) (`roots.txt`). They come from the
  `close_tree.py` SHARD expression. That expression's list equals the depth-2 order of
  `manifest_depth2.tsv`, and the sha256 of the name list is `5412782c…`, which matches.
- Command, run one root at a time in order:
  `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  All roots share one resumable `out.jsonl`.
- J = 4 until 08:59, then J = 3 (see "Proof rejection").
- Live files were kept in `/opt/work/live` and copied here at each commit, so that
  `git pull --rebase` never rewrote a file the driver had open.

## Proof rejection (memory, not real)

At 08:59, `0s0-1s1_4s0-6s1_2_5` came back UNSAT with `lrat_check = c VERIFIED` and
`cake_lpr = none`. dmesg shows `Memory cgroup out of memory: Killed process (cake_lpr)`: four
cake_lpr processes were running at once, each with about a 4 GB heap.

I re-ran that node alone with `recheck_node.py` (output in
`recheck_0s0-1s1_4s0-6s1_2_5.txt`):
- CNF sha256 `e18cce39…` is the same as before;
- CaDiCaL returned UNSAT in 5.7 s;
- both checkers accepted the proof.

The driver then resumed with `--jobs 3`. It re-solved the node, and the node is certified in
`out.jsonl`. No later rejections. The 4th core sat idle after that, because a 4th cake_lpr does
not fit in memory.

## compose.py (`compose.txt`)

`{"certified_nodes": 1207, "class_covered": false, "uncovered_frontier_nodes": 317, ...}`.
As expected, the class is not covered.

## Per root

`summary.md` has the full table for all 68 roots, made by `summarize.py out.jsonl roots.txt`.
In it, "open" counts frontier nodes that are neither certified nor split. Times are wall-clock
seconds per process: solve is CaDiCaL time and includes the 300 s timeouts; check is both
checkers together.

| # | root | status | certified by depth | splits | solve s | check s |
|---|---|---|---|---|---|---|
| 1 | `0s0-1s0_2s0-4s0` | closed | d2:1 | 0 | 6 | 33 |
| 2 | `0s0-1s0_2s1-8s0` | closed | d2:1 | 0 | 11 | 32 |
| 3 | `0s0-1s0_3s1-5s1` | closed | d2:1 | 0 | 12 | 31 |
| 4 | `0s0-1s0_4s1-5s0` | closed | d2:1 | 0 | 121 | 50 |
| 5 | `0s0-1s0_5s1-6s1` | closed | d2:1 | 0 | 5 | 24 |
| 6 | `0s0-1s0_7` | closed | d3:120 | 1 (pre-split, one orbit) | 2463 | 2509 |
| 7 | `0s0-1s0_9s0-10s1` | closed | d2:1 | 0 | 88 | 29 |
| 8 | `0s0-1s1_2s1-3s1` | closed | d2:1 | 0 | 35 | 24 |
| 9 | `0s0-1s1_3s0-8s0` | closed | d2:1 | 0 | 280 | 41 |
| 10 | `0s0-1s1_4s0-6s1` | closed | d3:84, d4:462 | 8 (root timed out at 300 s; 7 one-orbit pre-splits) | 6471 | 9639 |
| 11 | `0s0-1s1_5s0-7s0` | closed | d2:1 | 0 | 35 | 22 |
| 12 | `0s0-1s1_6s0-9s1` | **open** | d3:70, d4:462 | 8 (same shape as #10) | 5336 | 8980 |
| 13–68 | (see `summary.md`) | open, not started | – | – | – | – |

For root 12, all 7 one-orbit depth-3 subtrees are closed (462 depth-4 nodes certified). Of the
84 two-orbit depth-3 children, 70 are certified and 14 were not yet tried when time ran out.

## Per depth, all roots

| depth | certified | split | still open |
|---|---|---|---|
| 2 | 9 | 3 (2 timed out at 300 s, 1 pre-split) | 56 (all never started) |
| 3 | 274 | 14 (all one-orbit pre-splits) | 14 (never tried, under root 12) |
| 4 | 924 | 0 | 0 |

Totals:
- 1,207 certified nodes;
- CaDiCaL time 14,869 s, checker time 21,437 s;
- 2 timeouts (UNKNOWN at 300 s: roots 10 and 12), and no node below depth 2 timed out;
- slowest certified node: 279.5 s solve.

## SAT

None.

## Files

`env.txt`, `tools.txt`, `roots.txt`, `run.sh`, `out.jsonl` (all records), `driver.log`,
`roots_done.txt` (the 11 closed roots), `compose.txt`, `summarize.py`, `summary.md`,
`recheck_node.py` (copied from C02), and `recheck_0s0-1s1_4s0-6s1_2_5.txt`.

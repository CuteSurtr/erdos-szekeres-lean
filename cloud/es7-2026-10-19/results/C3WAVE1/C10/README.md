# C3WAVE1 / C10: machine 10 of 24, wave 1, 3-fold class (m = 11, k = 7)

## What ran where
One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`), 07:35 to 11:13 UTC on 2026-10-20 (driver),
README at about 11:20. C3-S/C3a tools from a worktree of `8dc27c3` at `/opt/c3s`. `/opt/work` was writable,
so `close_tree.py` ran unmodified (no diff).

Tools (`tools.txt`):
- cadical: CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr: tanyongkiam/cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). The bundled example prints `s VERIFIED UNSAT`.
- lrat-check: marijnheule/drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch` applied.

Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
`bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

Roots: 68 depth-2 nodes with index ≡ 10 (mod 24), computed with the SHARD-mode expression from `close_tree.py`
(`roots.txt`). The sha256 of all 1,630 names is `5412782c…` as in shard_plan.md, and the list agrees with
`manifest_depth2.tsv` (`roots_check.txt`).

Command per root, in order, one root at a time:
`close_tree.py /opt/work/base.cnf OUT ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`,
with H = time left. The output is `out.jsonl` (one file for all roots); `driver.log` holds the driver output.

## Results
- **No SAT. No real proof rejection.**
- **6 of 68 roots fully closed**: 0s0-1s0_2s0-6s0, 0s0-1s0_3 (120 children), 0s0-1s0_3s1-7s1,
  0s0-1s0_4s1-7s0, 0s0-1s0_5s1-8s1, 0s0-1s0_7s0-8s1.
- The 7th root, **0s0-1s1_2, is open**. It was pre-split into 120 depth-3 children. 112 of them were certified;
  8 (the single-orbit layers `0s0-1s1_2_3` … `_10`) timed out at 300 s and were split into 91 children each.
  Of those depth-4 children, all 91 of `_4` and 69 of 91 of `_5` are certified; `_3`, `_6`–`_10` were not reached.
  So 568 depth-4 nodes are still open under this root.
- 61 roots (0s0-1s1_2s1-5s1 onward in `roots.txt`) were not started.
- In total: 406 CaDiCaL runs, 397 certified, 8 timeouts, 1 re-run (below). 25,124 s solve time and 9,862 s check time, summed over runs at 3–4 parallel jobs.
- `compose.py` (`compose.txt`): `certified_nodes: 397, class_covered: false, uncovered_frontier_nodes: 336`.
  As expected, it does not report the class covered.

Per root (from `summary.md`; certified = both checkers, cake_lpr `s VERIFIED UNSAT`):

| root | status | certified by depth | splits | open by depth | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-1s0_2s0-6s0 | CLOSED | d2:1 | 0 | - | 9 | 27 |
| 0s0-1s0_3 | CLOSED | d3:120 | 1 (pre-split) | - | 1622 | 2071 |
| 0s0-1s0_3s1-7s1 | CLOSED | d2:1 | 0 | - | 35 | 20 |
| 0s0-1s0_4s1-7s0 | CLOSED | d2:1 | 0 | - | 75 | 26 |
| 0s0-1s0_5s1-8s1 | CLOSED | d2:1 | 0 | - | 5 | 12 |
| 0s0-1s0_7s0-8s1 | CLOSED | d2:1 | 0 | - | 60 | 23 |
| 0s0-1s1_2 | open | d3:112 d4:160 | 9 (1 pre-split + 8 timeouts) | d4:568 | 23256 | 7663 |
| the other 61 roots | not started | - | 0 | d2:1 each | 0 | 0 |

Per depth, over all 68 roots:

| depth | certified | split | still open |
|---|---|---|---|
| 2 | 5 | 2 | 61 |
| 3 | 232 | 8 | 0 |
| 4 | 160 | 0 | 568 |

## Incidents (none affects soundness)
1. **cake_lpr OOM at --jobs 4.** Node `0s0-1s0_3_6` got `lrat_check: c VERIFIED` and `cake_lpr: none`. The
   kernel log shows the memory cgroup OOM-killed cake_lpr (4 GB RSS while 3 other jobs ran). I re-ran that node alone
   (`logs/recheck_0s0-1s0_3_6.json`): same CNF sha256 and proof size, `c VERIFIED` / `s VERIFIED UNSAT`. The record was
   appended to `out.jsonl` with `"recheck_alone": true`, and the rest ran at --jobs 3, with no further OOM.
   The driver had returned on "PROOF NOT ACCEPTED", but `ProcessPoolExecutor.__exit__` kept running the queued futures without
   recording them. I killed it, and those results were lost (they were re-solved later).
2. **Output file swapped by git.** The first progress push ran `git pull --rebase --autostash` while the driver held
   `out.jsonl` open. The autostash replaced the file, so the driver kept appending to the deleted inode. I copied the records
   from `/proc/PID/fd` (`tail --pid -f`) into `/opt/work/out.jsonl`, and every later run wrote there; the copy in this directory is
   made at commit time. No record was lost: 397 certified records, all consistent with `compose.py`'s
   recomputed CNF sha256s.

## Files
`env.txt`, `tools.txt`, `roots.txt`, `roots_check.txt`, `out.jsonl`, `driver.log`, `compose.txt`,
`summary.md` + `summarize.py` (per-root/per-depth table; run from C3-S/tools), `logs/recheck_0s0-1s0_3_6.json`.
No CNF or proof files are committed.

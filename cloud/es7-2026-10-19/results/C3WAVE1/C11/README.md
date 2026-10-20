# C3WAVE1 / C11: machine 11 of 24, wave 1, 3-fold class (m = 11, k = 7)

## What ran where
- One cloud VM, from 08:16 to 11:55 UTC on 2026-10-20 (`env.txt`). It had 4 cores and 15 GB RAM, and the job's memory cgroup limit was 14.3 GB.
- Tools: C3-S/C3a scripts from a worktree of commit `8dc27c3` at `/opt/c3s`, unchanged. `/opt/work` was writable, so the driver needed no edit.
- `cadical`: CaDiCaL 3.0.1, commit c6073042.
- `cake_lpr`: commit a36874a8, `make cake_lpr`. The bundled example prints `s VERIFIED UNSAT`.
- `lrat-check`: drat-trim 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`.
- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (as expected).
- Roots: the 68 depth-2 nodes with index ≡ 11 (mod 24), from the same expression as `close_tree.py` SHARD mode
  (`roots.txt`). They are identical to rows 11, 35, … of the sorted `manifest_depth2.tsv`, whose name list has the expected sha256 `5412782c…`.
- Command per root, one root at a time, in order (`scripts/run.sh`):
  `close_tree.py base.cnf OUT.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  J was 4 at first and 3 from 08:38 on (see "Incidents").
  The driver was stopped at the 11:52 deadline, so the last root is partial.
- Records: `out.jsonl` (1,494 records). Driver output: `driver.log`. Rechecks: `rechecks.jsonl` and `recheck_*.md`.

## Per root (roots 1–9 of 68 were started; roots 10–68 were not reached)
Times are summed over all attempts. Check time is lrat-check plus cake_lpr.

| root | status | certified by depth | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s0_2s0-6s1 | closed | d2:1 | 0 | 62 | 42 |
| 0s0-1s0_3s0-10s0 | closed | d2:1 | 0 | 54 | 36 |
| 0s0-1s0_3s1-8s0 | closed | d2:1 | 0 | 33 | 34 |
| 0s0-1s0_4s1-7s1 | closed | d2:1 | 0 | 6 | 25 |
| 0s0-1s0_5s1-9s0 | closed | d2:1 | 0 | 73 | 46 |
| 0s0-1s0_7s0-9s0 | closed | d2:1 | 0 | 5 | 18 |
| 0s0-1s1_2s0-10s0 | closed (every child closed) | d3:84, d4:462 | 8 | 4953 | 8438 |
| 0s0-1s1_2s1-6s0 | closed (every child closed) | d3:84, d4:462 | 8 | 4414 | 8141 |
| 0s0-1s1_3s1-10s1 | open (stopped at deadline) | d4:367 | 8 | 2367 | 5049 |

The splits of each split root are:
- the root itself, after its 300 s timeout;
- its 7 one-orbit children, pre-split by `--split-singles`, 66 children each.

Each closed split root has 84 two-orbit children at depth 3 and 7 × 66 = 462 nodes at depth 4, all certified.
In the open root, 367 of the 462 depth-4 nodes are certified. Its 84 depth-3 two-orbit children and 95 depth-4 nodes were not run yet.

Fully closed roots (certified, or every child closed, recursively): 8 of 68, the first 8 in `roots.txt`.

## Per depth, all roots
| depth | certified | split | still open |
|---|---|---|---|
| 2 | 6 | 3 | 0 |
| 3 | 168 | 21 | 84 |
| 4 | 1291 | 0 | 95 |

The 21 depth-3 splits are pre-splits of one-orbit layers, not timeouts. Only 3 caps ran out, all on depth-2 roots.
59 roots were never started.
Totals: 1,465 nodes certified. Solve time was 11,967 s and check time 21,828 s. The largest proof was 253 MB.
No CNF or proof files are kept.

## compose.py
`python3 tools/compose.py /opt/work/base.cnf out.jsonl` gave:
`{"certified_nodes": 1465, "class_covered": false, "uncovered_frontier_nodes": 420, ...}` (`compose.txt`).
All 1,465 CNF sha256 values were re-derived without a mismatch. As expected, the class is not covered.

## SAT
None. No node returned SATISFIABLE.

## Proof rejections
No real rejection. Two "PROOF NOT ACCEPTED" records were caused by memory:
- `0s0-1s1_2s0-10s0_3_7` (08:31, jobs 4) and `0s0-1s1_2s0-10s0_3s0-4s0` (08:35).
- In both records lrat-check printed `c VERIFIED` and cake_lpr printed nothing. dmesg shows the cgroup OOM killer killed cake_lpr;
  this cake_lpr build uses about 4.2 GB of RSS on every proof.
- Re-run alone, both proofs were accepted by both checkers (`rechecks.jsonl`).
- Both nodes were later certified by the driver itself, and the summary counts only those driver records.

## Incidents (deviations, all recorded in driver.log)
1. **OOM / zombie driver.** After its first PROOF NOT ACCEPTED, the jobs-4 driver's `main` returned inside the
   `ProcessPoolExecutor` block. The executor's shutdown waits for every pending future, and the whole frontier had been submitted.
   So that driver went on solving without writing records, while the jobs-3 driver ran. Seven workers on one cgroup
   caused the second OOM.
   - Both drivers were killed. The second driver had written no certified records in that window.
   - `scripts/run.sh` now runs each driver in its own process group and kills the group on SAT, on a rejection or at the deadline.
     The driver code is unchanged. Jobs were set to 3 as instructed and stayed at 3, with no further OOM kills.
2. **OUT file inode.** At first OUT.jsonl was this directory's `out.jsonl`. At 09:03 `git pull --rebase --autostash` replaced the
   file, and the driver kept appending to the deleted inode.
   - At 09:30 the full file was recovered from `/proc/PID/fd/3`. Its first 99 lines are byte-identical to the committed file, and all 349 lines parse.
   - The driver was then restarted with OUT=`/opt/work/out.jsonl`, which is copied here before each commit. No records were lost;
     only in-flight nodes were redone.
3. The runner's own CaDiCaL / cake_lpr processes were killed at the deadline. Unfinished nodes have no record.

## Files
`env.txt`, `tools.txt`, `roots.txt`, `out.jsonl`, `driver.log`, `compose.txt`, `summary.md`, `rechecks.jsonl`,
`recheck_0s0-1s1_2s0-10s0_3_7.md`, `scripts/` (runner, recheck, summary, commit helpers).

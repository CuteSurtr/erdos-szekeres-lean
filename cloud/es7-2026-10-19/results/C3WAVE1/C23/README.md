# C3WAVE1 / C23: machine 23 of 24, wave 1, 3-fold class (m = 11, k = 7)

Nothing here closes the class. A node counts as certified only when the driver recorded
`lrat_check == "c VERIFIED"` (E2-patched) **and** `cake_lpr == "s VERIFIED UNSAT"`.

## What ran where

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`), 07:35 to 11:11 UTC on 2026-10-20 for the
driver, then compose and this write-up.

- Tools (`tools.txt`): CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (`make cake_lpr`; bundled
  example prints `s VERIFIED UNSAT`); drat-trim 2e3b2dc lrat-check with
  `results/E2/tools/lrat-check-E2.patch`.
- C3-S/C3a tools from a worktree of 8dc27c3 at /opt/c3s, **unmodified** (/opt/work was writable).
- Base CNF: `gen_case.py 11 7 none`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the 67 depth-2 nodes with index ≡ 23 (mod 24) from close_tree.py's SHARD expression
  (`roots.txt`, index and name). Agrees with `manifest_depth2.tsv`; the sorted-name sha256 is
  `5412782c…6b7e` as in shard_plan.md.
- Each root run alone, in order, by `run.sh`:
  `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  J = 4 for the first 4 roots, then 3 (see below). One out.jsonl for all roots.

## Results

8 of 67 roots fully closed, 1 partly done (stopped on the time budget), 58 not started.

| root | status | certified by depth | splits | open leaves | solve s / check s |
|---|---|---|---|---|---|
| 0s0-1s0_2s1-4s1 | CLOSED | d2:1 | 0 | 0 | 12 / 34 |
| 0s0-1s0_3s0-9s0 | CLOSED | d2:1 | 0 | 0 | 48 / 40 |
| 0s0-1s0_4s0-7s1 | CLOSED | d2:1 | 0 | 0 | 68 / 45 |
| 0s0-1s0_5s0-8s0 | CLOSED | d2:1 | 0 | 0 | 5 / 19 |
| 0s0-1s0_6s1-10s1 | CLOSED | d2:1 | 0 | 0 | 9 / 24 |
| 0s0-1s0_8s0-9s1 | CLOSED | d2:1 | 0 | 0 | 79 / 46 |
| 0s0-1s1_2s0-8s0 | CLOSED | d3:84, d4:462 | 8 | 0 | 4756 / 9202 |
| 0s0-1s1_3s0-4s1 | CLOSED | d3:84, d4:462 | 8 | 0 | 6228 / 9399 |
| 0s0-1s1_3s1-9s1 | open | d4:200 | 8 | 346 | 1550 / 3074 |
| 0s0-1s1_4s1-9s0 | not started | | | | |
| 0s0-1s1_6s0-10s0 | not started | | | | |
| 0s0-1s1_7s1-10s1 | not started | | | | |
| 0s0-2s0_1s0-3s1 | not started | | | | |
| 0s0-2s0_1s1-7s1 | not started | | | | |
| 0s0-2s0_3s1-5s0 | not started | | | | |
| 0s0-2s0_4s1-10s1 | not started | | | | |
| 0s0-2s0_5s1-6s0 | not started | | | | |
| 0s0-2s0_6s1-9s1 | not started | | | | |
| 0s0-2s0_9s0-10s0 | not started | | | | |
| 0s0-2s1_1s1-3s0 | not started | | | | |
| 0s0-2s1_3s0-7s1 | not started | | | | |
| 0s0-2s1_4s0-6s0 | not started | | | | |
| 0s0-2s1_5s0-6s1 | not started | | | | |
| 0s0-2s1_6s0-9s0 | not started | | | | |
| 0s0-2s1_8s0-10s0 | not started | | | | |
| 0s0-3s0_1s0-6s1 | not started | | | | |
| 0s0-3s0_2s0-10s0 | not started | | | | |
| 0s0-3s0_2s1-8s0 | not started | | | | |
| 0s0-3s0_4s1-7s1 | not started | | | | |
| 0s0-3s0_5s1-9s0 | not started | | | | |
| 0s0-3s0_7s0-9s0 | not started | | | | |
| 0s0-3s1_1s0-10s0 | not started | | | | |
| 0s0-3s1_1s1-6s0 | not started | | | | |
| 0s0-3s1_2s1-10s1 | not started | | | | |
| 0s0-3s1_4s0-9s0 | not started | | | | |
| 0s0-3s1_5s0-9s1 | not started | | | | |
| 0s0-3s1_6s1-8s0 | not started | | | | |
| 0s0-3s1_8s1-9s0 | not started | | | | |
| 0s0-4s0_1s0-9s1 | not started | | | | |
| 0s0-4s0_2s0-6s0 | not started | | | | |
| 0s0-4s0_3s0-10s1 | not started | | | | |
| 0s0-4s0_5s0-10s0 | not started | | | | |
| 0s0-4s0_6s0-7s1 | not started | | | | |
| 0s0-4s0_7s1-9s0 | not started | | | | |
| 0s0-4s1_1s0-5s0 | not started | | | | |
| 0s0-4s1_1s1-9s0 | not started | | | | |
| 0s0-4s1_2s1-6s1 | not started | | | | |
| 0s0-4s1_3s1-6s0 | not started | | | | |
| 0s0-4s1_5s1-7s1 | not started | | | | |
| 0s0-4s1_7s0-10s1 | not started | | | | |
| 0s0-4s1_9s1-10s1 | not started | | | | |
| 0s0-5s0_1s1-3s1 | not started | | | | |
| 0s0-5s0_2s0-9s0 | not started | | | | |
| 0s0-5s0_3s0-7s1 | not started | | | | |
| 0s0-5s0_4s0-8s0 | not started | | | | |
| 0s0-5s0_6s1-10s1 | not started | | | | |
| 0s0-5s0_8s0-9s1 | not started | | | | |
| 0s0-5s1_1s0-8s0 | not started | | | | |
| 0s0-5s1_2s0-3s1 | not started | | | | |
| 0s0-5s1_2s1-9s1 | not started | | | | |
| 0s0-5s1_3s1-9s0 | not started | | | | |
| 0s0-5s1_6s0-10s0 | not started | | | | |
| 0s0-5s1_7s1-10s1 | not started | | | | |
| 0s0_1s0-3s0 | not started | | | | |
| 0s0_1s1-6s1 | not started | | | | |
| 0s0_2s1-4s0 | not started | | | | |
| 0s0_3s1-5s0 | not started | | | | |

| depth | certified | split | open |
|---|---|---|---|
| 2 | 6 | 3 | 58 |
| 3 | 168 | 21 | 84 |
| 4 | 1124 | 0 | 262 |

solver statuses: {'UNSATISFIABLE': 1299, 'UNKNOWN': 3}  closed roots: 8 of 67

Splits at depth 2 are CaDiCaL 300 s timeouts (UNKNOWN); splits at depth 3 are the
`--split-singles` pre-splits of one-orbit layers. Times are summed over node records (wall
seconds per process, 3–4 processes at once); total solve 12,761 s, check 21,902 s.
Checking (mostly cake_lpr, ~4.2 GB RSS each) costs about twice the solving.

`compose.py base.cnf out.jsonl` (`compose.txt`):
`{"certified_nodes": 1298, "class_covered": false, "uncovered_frontier_nodes": 457, ...}`.
All 1,298 sha256s were recomputed by compose and matched.

## SAT, rejections, incidents

- **No SAT.** All 1,299 decided nodes were UNSAT; 3 UNKNOWN (timeouts, then split).
- **One "PROOF NOT ACCEPTED", not a real rejection** (`rejection_3_7.md`):
  0s0-1s1_2s0-8s0_3_7 at 07:50, lrat-check VERIFIED, cake_lpr empty output. dmesg shows the
  cgroup OOM killer killed cake_lpr (4 parallel cake_lpr × ~4.2 GB > 15 GB). Re-run alone:
  both checkers accept (peak RSS 4.2 GB). Resumed with --jobs 3; the driver then re-solved and
  certified the node itself (its uncertified record stays in out.jsonl and is ignored by
  compose). No further OOM with 3 jobs.
- **Lost-records incident, recovered.** After the resume, the `git pull --rebase --autostash`
  before a push replaced out.jsonl and driver.log in the work tree, so the running driver kept
  writing to the unlinked old files (07:52–08:15). I stopped the driver with SIGSTOP, copied the
  records out of /proc/PID/fd (the first 16 lines matched the committed file byte for byte),
  and moved the live files to /opt/work; they are copied into this directory before each commit.
  In-flight nodes at the stop were discarded and re-run. **Advice for other machines:** do not
  keep a file that a running driver appends to under git's work tree while you run
  `git pull --autostash`.
- The driver checks `--hours` only between batches, so at 11:11 I stopped it by hand (in-flight
  nodes of root 0s0-1s1_3s1-9s1 discarded). It resumes from out.jsonl.

## Files

`env.txt`, `tools.txt`, `roots.txt`, `out.jsonl` (all node records), `driver.log`,
`compose.txt`, `summary.md` (made by `summ.py`), `rejection_3_7.md`, `run.sh`, `recheck.py`.
No CNF or proof files.

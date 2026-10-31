# C03: wave 1 of the 3-fold class, machine 3 of 24

Result: **19 of 68 roots fully closed**, 1 root partly done, 48 not started. 661 nodes certified
(both checkers). No SAT. No real proof rejection: one cake_lpr run was killed for lack of memory, and the node passed both checkers when re-run alone.

## What ran where
One cloud VM: 4 cores, 15 GB RAM with a 14.3 GB cgroup limit, no swap (`env.txt`). The driver ran 07:39–11:12 UTC on 2026-10-20.
- C3-S/C3a tools: a worktree of `8dc27c3` at `/opt/c3s`, unmodified. `/opt/work` was writable, so the driver's WORK path was not changed.
- cadical 3.0.1 `c60730422e758ef1cebe7aeddf2dda31c996bf04`
- cake_lpr `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` (`make cake_lpr`); the bundled example prints `s VERIFIED UNSAT`
- lrat-check: drat-trim `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` + `results/E2/tools/lrat-check-E2.patch`
- base CNF `gen_case.py 11 7 none`: sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches)
- roots: the 68 depth-2 nodes with index ≡ 3 (mod 24) (`roots.txt`). They come from the SHARD expression in `close_tree.py`, which gives the same list and order as `manifest_depth2.tsv`; the name-list sha256 `5412782c…` matches.
- Each root ran alone and in order (`run.sh`): `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours <remaining>`, with a hard stop at 11:12 UTC (`timeout`).

## Incidents (all recorded in `driver.log` / `driver_attempt1.log`)
1. **Lost first attempt (07:37–07:39).** `out.jsonl` sat inside the git tree. A `git pull --rebase` replaced the file while the driver was appending to it, so root 1's record was lost. Fix: the live files moved to `/opt/work`, and the commit loop copies them into the repo. Root 1 was re-solved.
2. **Out of memory, not a rejection (08:03).** With --jobs 4, several cake_lpr processes ran at once (about 4 GB each), and the cgroup OOM killer killed one. The driver printed "PROOF NOT ACCEPTED 0s0-1s1_3s0-6s1_2_4", with `lrat_check: c VERIFIED` and `cake_lpr: none`. Re-run alone, the node gave `c VERIFIED` and `s VERIFIED UNSAT` (`recheck_2_4.json`, same CNF sha256), and that record was appended to `out.jsonl`. The driver resumed with **--jobs 3** for the rest of the run.
3. After the resume, the stop check in `run.sh` matched the old "PROOF NOT ACCEPTED" line in the log and stopped the run by mistake. The check was changed to read only the current root's output, and the run restarted at 08:04:53. No work was lost, because the driver is resumable.
4. At 11:12 the timeout stopped root `0s0-2s1_1` mid-run (rc=124). Unfinished solves left no record.

## Per root
Solve and check times are sums over nodes, in seconds. Nodes ran 3–4 at a time, so wall time is lower. "splits" counts nodes split, including presplits of single-orbit layers.

| root | status | certified by depth | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s0_2s0-10s1 | closed | d2:1 | 0 | 9 | 31 |
| 0s0-1s0_2s1-6s1 | closed | d2:1 | 0 | 43 | 43 |
| 0s0-1s0_3s1-4s0 | closed | d2:1 | 0 | 79 | 40 |
| 0s0-1s0_4s0-9s1 | closed | d2:1 | 0 | 33 | 35 |
| 0s0-1s0_5s1-10s0 | closed | d2:1 | 0 | 43 | 36 |
| 0s0-1s0_6s1-8s1 | closed | d2:1 | 0 | 5 | 18 |
| 0s0-1s0_8s1-9s1 | closed | d2:1 | 0 | 4 | 20 |
| 0s0-1s1_2s1-10s0 | closed | d2:1 | 0 | 49 | 50 |
| 0s0-1s1_3s0-6s1 | closed | d3:84, d4:462 | 8 | 5279 | 8714 |
| 0s0-1s1_4s0-5s0 | closed | d2:1 | 0 | 31 | 23 |
| 0s0-1s1_5s0-10s1 | closed | d2:1 | 0 | 241 | 36 |
| 0s0-1s1_6s0-8s0 | closed | d2:1 | 0 | 32 | 20 |
| 0s0-1s1_7s1-9s1 | closed | d2:1 | 0 | 33 | 21 |
| 0s0-2s0_1s0-5s1 | closed | d2:1 | 0 | 156 | 35 |
| 0s0-2s0_1s1-9s1 | closed | d2:1 | 0 | 107 | 30 |
| 0s0-2s0_3s1-7s0 | closed | d2:1 | 0 | 74 | 28 |
| 0s0-2s0_4s1-6s1 | closed | d2:1 | 0 | 10 | 13 |
| 0s0-2s0_5s1-8s0 | closed | d2:1 | 0 | 94 | 27 |
| 0s0-2s0_7s0-8s0 | closed | d2:1 | 0 | 7 | 13 |
| 0s0-2s1_1 | open | d3:83 | 9 | 11790 | 2666 |
| 0s0-2s1_1s1-5s0 | not started | | | | |
| 0s0-2s1_3s0-9s1 | not started | | | | |
| 0s0-2s1_4s0-8s0 | not started | | | | |
| 0s0-2s1_5s0-8s1 | not started | | | | |
| 0s0-2s1_6s1-7s0 | not started | | | | |
| 0s0-2s1_8s1-10s0 | not started | | | | |
| 0s0-3s0_1s0-8s1 | not started | | | | |
| 0s0-3s0_2s0-5s0 | not started | | | | |
| 0s0-3s0_4 | not started | | | | |
| 0s0-3s0_4s1-9s1 | not started | | | | |
| 0s0-3s0_6s0-10s1 | not started | | | | |
| 0s0-3s0_7s1-8s0 | not started | | | | |
| 0s0-3s1_1s0-4s0 | not started | | | | |
| 0s0-3s1_1s1-8s0 | not started | | | | |
| 0s0-3s1_2s1-5s1 | not started | | | | |
| 0s0-3s1_4s1-5s0 | not started | | | | |
| 0s0-3s1_5s1-6s1 | not started | | | | |
| 0s0-3s1_7 | not started | | | | |
| 0s0-3s1_9s0-10s1 | not started | | | | |
| 0s0-4s0_1s1-2s1 | not started | | | | |
| 0s0-4s0_2s0-8s0 | not started | | | | |
| 0s0-4s0_3s0-6s1 | not started | | | | |
| 0s0-4s0_5s0-7s0 | not started | | | | |
| 0s0-4s0_6s0-9s1 | not started | | | | |
| 0s0-4s0_8s0-10s1 | not started | | | | |
| 0s0-4s1_1s0-7s0 | not started | | | | |
| 0s0-4s1_2s0-10s1 | not started | | | | |
| 0s0-4s1_2s1-8s1 | not started | | | | |
| 0s0-4s1_3s1-8s0 | not started | | | | |
| 0s0-4s1_5s1-9s1 | not started | | | | |
| 0s0-4s1_7s0-9s1 | not started | | | | |
| 0s0-5s0_1s0-10s1 | not started | | | | |
| 0s0-5s0_1s1-6s1 | not started | | | | |
| 0s0-5s0_2s1-3s0 | not started | | | | |
| 0s0-5s0_3s0-9s1 | not started | | | | |
| 0s0-5s0_4s1-10s0 | not started | | | | |
| 0s0-5s0_6s1-8s1 | not started | | | | |
| 0s0-5s0_8s1-9s1 | not started | | | | |
| 0s0-5s1_1s1-10s0 | not started | | | | |
| 0s0-5s1_2s0-6s1 | not started | | | | |
| 0s0-5s1_3s0-4s0 | not started | | | | |
| 0s0-5s1_4s0-10s1 | not started | | | | |
| 0s0-5s1_6s0-8s0 | not started | | | | |
| 0s0-5s1_7s1-9s1 | not started | | | | |
| 0s0_1s0-5s0 | not started | | | | |
| 0s0_1s1-8s1 | not started | | | | |
| 0s0_2s1-6s0 | not started | | | | |
| 0s0_3s1-7s0 | not started | | | | |

| depth | certified | split | open |
|---|---|---|---|
| 2 | 18 | 2 | 0 |
| 3 | 167 | 15 | 29 |
| 4 | 462 | 0 | 728 |

closed roots: 19/68; SAT: []; rejected proofs: ['0s0-1s1_3s0-6s1_2_4 (later certified on recheck)']

The depth table counts nodes in the subtrees of my roots. "open" means queued but not certified: never tried, killed at the stop, or a timeout whose children have not run.
Wall time: `0s0-1s1_3s0-6s1` took 08:04:55–09:21:51 (546 leaves). `0s0-2s1_1` ran 09:39–11:12 and stayed open: 83 depth-3 nodes certified, 9 timed out at 300 s and were split.

## compose.py
`python3 tools/compose.py base.cnf out.jsonl` (`compose.txt`):
```
{"certified_nodes": 661, "class_covered": false, "uncovered_frontier_nodes": 622, "uncovered_sample": ["0s0", "0s0-1s0_2", "0s0-1s0_3", "0s0-1s0_4", "0s0-1s0_5", "0s0-1s0_6", "0s0-1s0_7", "0s0-1s0_8", "0s0-1s0_9", "0s0-1s0_10"]}
```
As expected, it does not report the class covered. The 19 closed roots are listed above: 18 were certified directly at depth 2, and `0s0-1s1_3s0-6s1` is closed because every child is closed, recursively.

## SAT / rejections
- SAT: none.
- Proof rejections: none real. The one "PROOF NOT ACCEPTED" was the OOM kill described above.

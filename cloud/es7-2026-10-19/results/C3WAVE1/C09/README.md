# C3WAVE1 / C09: machine 9 of 24, wave 1, 3-fold class (m = 11, k = 7)

Nothing here is a theorem. A node counts as closed only if cake_lpr printed `s VERIFIED UNSAT` on
its LRAT proof and lrat-check (E2 patch) printed `c VERIFIED`.

## Summary

- 68 roots (depth-2 nodes with index ≡ 9 mod 24). **6 roots fully closed**, 1 partly done
  (`0s0-1s1_10`: 465 of its nodes certified, 375 depth-4 nodes untried), 61 not started.
- 471 certified nodes: depth 2: 6, depth 3: 112, depth 4: 353.
- **No SAT.** No real proof rejection. One `PROOF NOT ACCEPTED` was caused by memory: the cgroup
  OOM killer stopped cake_lpr. Re-run alone, the node was accepted by both checkers (details below).
- `compose.py`: `certified_nodes 471, class_covered false, uncovered_frontier_nodes 683`
  (`compose_output.txt`), as expected for one shard.

## What ran where

One cloud VM: Linux 6.18 x86_64, 4 cores, 15 GB RAM, no swap (`env.txt`). The driver ran from
07:37 to 11:15 UTC on 2026-10-20. It used 4 jobs until 09:18 and 3 jobs after that (see the OOM
section). The tools were built from source (`tools.txt`):

| tool | commit |
|---|---|
| CaDiCaL 3.0.1 | c60730422e758ef1cebe7aeddf2dda31c996bf04 |
| cake_lpr (`make cake_lpr`; bundled example prints `s VERIFIED UNSAT`) | a36874a8b750b43fe4b385b8ddbf5b033e46a3fa |
| drat-trim lrat-check + `results/E2/tools/lrat-check-E2.patch` | 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 |
| C3-S / C3a tools (git worktree, unmodified; `/opt/work` was writable, so no path change) | 8dc27c3 |

- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots (`roots.txt`): I took the `close_tree.py` SHARD expression with i = 9, N = 24. It gives
  68 nodes, identical to the same selection from `manifest_depth2.tsv`. The sorted 1,630-name list
  has sha256 `5412782c…6b7e`, as in `shard_plan.md`.
- Command, one root at a time in order (`notes/run_roots.sh`):
  `close_tree.py base.cnf out.jsonl ROOT --jobs 4 --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  Every root ran under `timeout` set to the shared stop time, 11:15 UTC.
- Files: `out.jsonl` (all node records), `driver.log`, `summary.md` (from `summarize_c09.py`),
  `compose_output.txt`, `notes/`.

## Per root

| root | status | certified by depth | splits | still open | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-1s0_2s0-5s1 | closed | d2:1 | - | - | 74 | 34 |
| 0s0-1s0_2s1-9s1 | closed | d2:1 | - | - | 83 | 43 |
| 0s0-1s0_3s1-7s0 | closed | d2:1 | - | - | 69 | 45 |
| 0s0-1s0_4s1-6s1 | closed | d2:1 | - | - | 7 | 25 |
| 0s0-1s0_5s1-8s0 | closed | d2:1 | - | - | 106 | 46 |
| 0s0-1s0_7s0-8s0 | closed | d2:1 | - | - | 5 | 19 |
| 0s0-1s1_10 | open | d3:112, d4:353 | d2:1 (pre-split, single orbit, 120 children), d3:8 (91 children each) | d4:375 | 27,489 | 13,139 |
| the other 61 roots, from 0s0-1s1_2s1-5s0 on | not started | - | - | d2:1 each | 0 | 0 |

Solve and check times are wall-clock seconds summed over nodes. Up to 4 processes ran at once.
The full per-root table is in `summary.md`.

Inside `0s0-1s1_10`: 112 of its 120 depth-3 children were certified at the 300 s cap (max solve
237 s). The other 8 (`_2` … `_9`, one-orbit third layers) timed out and were split. Of their
8 × 91 = 728 depth-4 children, 353 are certified: all of `_2`, `_3` and `_4` (so these three are
closed), 52 of `_5`, and 7 each of `_6` … `_9`. No depth-4 node timed out: every one tried was UNSAT
in at most 62 s (cap 600 s). The rest of this root is mechanical and costs about
375 × (37 s solve + 27 s check) ≈ 6.7 core-hours.

## Per depth (all roots)

| depth | certified | split | open |
|---|---|---|---|
| 2 | 6 | 1 | 61 |
| 3 | 112 | 8 | 0 |
| 4 | 353 | 0 | 375 |

Certified solve times: depth 2 sum 345 s (max 106), depth 3 sum 11,834 s (max 237), depth 4 sum
13,210 s (max 62). Check times (both checkers): 213 s, 3,739 s, 9,378 s. Largest proof: 371 MB.

## SAT

None.

## Proof rejections

At 09:18 the driver printed `PROOF NOT ACCEPTED 0s0-1s1_10_4_3s0-6s1` with lrat-check
`c VERIFIED` and cake_lpr `none`. `dmesg` shows a memory-cgroup OOM kill of cake_lpr (anon-rss
4.2 GB) while two cake_lpr and two CaDiCaL processes were running (`notes/oom_dmesg.txt`).
Re-run alone (`notes/recheck_note.txt`): CNF sha256 matched the record; CaDiCaL UNSAT in 43 s;
lrat-check `c VERIFIED`; cake_lpr `s VERIFIED UNSAT`. The cause was memory, not a real rejection.
The driver resumed with `--jobs 3`. It re-solved the node itself, and the new record says
`certified: true` with both checkers accepting. The failed record stays in `out.jsonl`.
`compose.py` and `summary.md` ignore it, except that the summary's "rejected" column counts it
once.

## Operational incidents (no effect on soundness; all recorded)

1. **Lost record from a git rebase.** At first the driver wrote `out.jsonl` and `driver.log`
   directly in the repo. The first commit's `git pull --rebase --autostash` replaced those files
   while the driver held them open. Root 1's record (`0s0-1s0_2s0-5s1`) was lost, and the early
   log survives as `driver_part1.log` content at the top of `driver.log`. From 07:50 the driver
   wrote to `/opt/work`, and a committer process (`notes/committer3.sh`) copied the files into
   the repo before each commit. Root 1 was solved again and certified.
2. **Bogus split from my own kill.** While stopping the old driver, my `kill` of CaDiCaL hit root
   `0s0-1s1_2s1-5s0` 1.4 s into its run. The driver recorded it as UNKNOWN and split it (one
   split record plus seven pre-split records). I deleted these 9 records from `out.jsonl` before
   the root was solved again; they are kept in `notes/removed_records.jsonl`. Keeping them would
   have been sound but wasteful, since a split only enumerates children. The root then stayed
   unstarted because time ran out.
3. The OOM described above.

## For the next machine on this shard

Resume with the same `out.jsonl` (`--jobs 3` on a 15 GB machine) from root `0s0-1s1_10`. It
needs only the 375 open depth-4 nodes. Then continue with `0s0-1s1_2s1-5s0` and the rest of
`roots.txt`.

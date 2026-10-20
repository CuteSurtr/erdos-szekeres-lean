# C3WAVE1 / C02: machine 2 of 24, wave 1, 3-fold class (m = 11, k = 7)

**Result: 20 of my 68 roots are closed, 48 are open. 1,110 nodes are certified. No SAT.
No proof was rejected for real: the one rejection was cake_lpr running out of memory, and the
same node was later accepted.** The class is not covered (expected, since this is one shard).

## What ran where

- One cloud VM: 4 cores, 15 GB RAM, no swap, Linux 6.18 x86_64 (`env.txt`). Run on 2026-10-20 from 07:38 to 11:14 UTC.
- C3-S/C3a tools: `git worktree add /opt/c3s 8dc27c3`. I did not modify the driver: `/opt/work` was writable, so no diff.
- Tools, built from source and on PATH (`tools.txt`):
  - CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04;
  - cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`; the bundled example prints `s VERIFIED UNSAT`);
  - drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with `results/E2/tools/lrat-check-E2.patch` applied.
- Base CNF: `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`. It matches the expected value.
- Roots (`roots.txt`): the depth-2 nodes with index ≡ 2 (mod 24), from the SHARD expression in `close_tree.py`, 68 of them.
  - The SHARD expression gives 1,630 names in all, and the sha256 of the joined list is `5412782c…`, as in `shard_plan.md`.
  - My list is identical to rows 2, 26, … of the sorted depth-2 names in `manifest_depth2.tsv`.
- Command, one root at a time and in order (`run.sh`):
  `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  - J was 4 until 08:09 and 3 after that (see below).
  - A watchdog killed the driver at 11:13:53. Root 21 (`0s0-2s1_1s1-4s1`) had started at 11:12:49 and left no record.

## Incidents

1. **The first attempt lost its records (07:38–07:40).**
   - The live `out.jsonl` and `driver.log` were inside the git checkout. `git pull --rebase` replaced those files under the running driver, so its writes went to unlinked inodes.
   - I moved the live files to `/opt/work/live`; they are copied into this directory at commit time. I then restarted from the beginning. Root 1 was re-solved, and nothing else was affected (`driver_attempt1.log`).
2. **PROOF NOT ACCEPTED on `0s0-1s1_6s0-7s1_2_5` (08:08).**
   - lrat-check printed `c VERIFIED`, but cake_lpr printed nothing. Three cake_lpr processes (CML_HEAP_SIZE=12000) were running at once, and 13 of 15 GB was in use.
   - I re-ran the node alone (`recheck_node.py`, `recheck_0s0-1s1_6s0-7s1_2_5.txt`). The CNF sha256 and the proof size (20,634,413 bytes) were the same, and both checkers accepted.
   - Cause: memory. I resumed with `--jobs 3`. The resumed driver re-solved the node, and it was certified (both records are in `out.jsonl`). Peak memory after that was 10.6 GB (`mem.log`).
   - No other rejection occurred.

## Per root

Only roots with records are listed. The other 48 roots, from `0s0-2s1_1s1-4s1` onward in `roots.txt`, were not reached and are open. Full table: `summary.md`.

| root | status | certified by depth | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s0_2s0-10s0 | closed | d2:1 | 0 | 65 | 44 |
| 0s0-1s0_2s1-6s0 | closed | d2:1 | 0 | 60 | 40 |
| 0s0-1s0_3s1-10s1 | closed | d2:1 | 0 | 82 | 46 |
| 0s0-1s0_4s0-9s0 | closed | d2:1 | 0 | 29 | 36 |
| 0s0-1s0_5s0-9s1 | closed | d2:1 | 0 | 50 | 42 |
| 0s0-1s0_6s1-8s0 | closed | d2:1 | 0 | 89 | 48 |
| 0s0-1s0_8s1-9s0 | closed | d2:1 | 0 | 100 | 46 |
| 0s0-1s1_2s0-9s1 | closed | d2:1 | 0 | 68 | 46 |
| 0s0-1s1_3s0-6s0 | closed | d2:1 | 0 | 36 | 40 |
| 0s0-1s1_4s0-10s1 | closed | d2:1 | 0 | 90 | 44 |
| 0s0-1s1_5s0-10s0 | closed | d2:1 | 0 | 226 | 52 |
| 0s0-1s1_6s0-7s1 | closed | d3:84, d4:462 | 8 | 5942 | 9623 |
| 0s0-1s1_7s1-9s0 | closed | d3:84, d4:462 | 8 | 5885 | 9423 |
| 0s0-2s0_1s0-5s0 | closed | d2:1 | 0 | 21 | 20 |
| 0s0-2s0_1s1-9s0 | closed | d2:1 | 0 | 8 | 13 |
| 0s0-2s0_3s1-6s1 | closed | d2:1 | 0 | 17 | 20 |
| 0s0-2s0_4s1-6s0 | closed | d2:1 | 0 | 136 | 34 |
| 0s0-2s0_5s1-7s1 | closed | d2:1 | 0 | 9 | 13 |
| 0s0-2s0_7s0-10s1 | closed | d2:1 | 0 | 88 | 28 |
| 0s0-2s0_9s1-10s1 | closed | d2:1 | 0 | 8 | 14 |

- The two split roots each timed out at 300 s, and the timeout counts as 1 split.
- Each then had 21 depth-3 children: 14 were two-orbit nodes, which all closed, and 7 were one-orbit nodes, which were pre-split by `--split-singles`. Every one of their depth-4 children was certified.
- Solve and check times are wall-clock, with 3–4 jobs sharing 4 cores. Over all roots, 1,113 solver runs took 3.61 h and the checks took 5.46 h. The largest proof was 317 MB.

## Per depth, all 68 roots

| depth | certified | split | open |
|---|---|---|---|
| 2 | 18 | 2 (timeout) | 48 (not reached) |
| 3 | 168 | 14 (pre-split one-orbit) | 0 |
| 4 | 924 | 0 | 0 |

## compose.py

```
{"certified_nodes": 1110, "class_covered": false, "uncovered_frontier_nodes": 447, "uncovered_sample": ["0s0", "0s0-1s0_2", "0s0-1s0_3", "0s0-1s0_4", "0s0-1s0_5", "0s0-1s0_6", "0s0-1s0_7", "0s0-1s0_8", "0s0-1s0_9", "0s0-1s0_10"]}
```

As expected, the class is not covered: only this shard's records were given, and the uncovered sample lists other shards' nodes.

## Files

- `env.txt`, `tools.txt`, `roots.txt`: environment, tool commits and the root list.
- `out.jsonl`: all node records. Proofs and CNFs were deleted; they can be regenerated from base.cnf and the node name.
- `driver.log`, `driver_attempt1.log`, `mem.log`: driver output and memory samples.
- `run.sh`: the runner. `summarize.py` and `summary.md`: the per-root and per-depth tables. `compose.txt`: the compose output.
- `recheck_node.py`, `recheck_*.txt`: the standalone recheck of the one rejected node.

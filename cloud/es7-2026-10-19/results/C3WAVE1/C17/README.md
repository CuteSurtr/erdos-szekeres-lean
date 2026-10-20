# C3WAVE1 / C17: machine 17 of 24, wave 1, 3-fold class (m = 11, k = 7)

Nothing here is a theorem. A node counts as certified only if cake_lpr printed `s VERIFIED UNSAT`
and the E2-patched lrat-check printed `c VERIFIED` on its LRAT proof.

## What ran where

- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). The memory cgroup limit is 13.4 GB.
  Solving ran from 07:38 to 11:13 UTC on 2026-10-20.
- C3-S/C3a tools: `git worktree add /opt/c3s 8dc27c3`, unmodified. `/opt/work` was writable,
  so the driver's work path needed no change.
- cadical: CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr: tanyongkiam/cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, built with
  `make cake_lpr`. The bundled example.cnf/example.lpr printed `s VERIFIED UNSAT`.
- lrat-check: drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with
  `results/E2/tools/lrat-check-E2.patch` applied.
- Base CNF: `gen_case.py 11 7 none` gave sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`, which matches.
- Roots: indices that are 17 mod 24 in the sorted depth-2 list, using the SHARD-mode expression
  from `close_tree.py`. That gives 68 roots (`roots.txt`). The 1,630-name list equals
  `manifest_depth2.tsv` exactly, and its sha256 is 5412782c…, as in shard_plan.
- Each root was run in order by a loop:
  `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  H was the time left before 11:13. At 11:13 the loop stopped the driver with `timeout`.

## Incidents (none affects soundness)

1. **Lost records for root 1 (07:38–07:39).** `out.jsonl` and `driver.log` first lived in the
   git work tree. The `git pull --rebase --autostash` run for the 07:38 commit replaced them
   on disk while the driver had them open, so root 1's record went to an unlinked file. After
   that, the live files were kept in `/opt/work/live/` and copied here before each commit.
   Root 1 was solved again. `driver_attempt1.log` is the log of that first run.
2. **"PROOF NOT ACCEPTED" on `0s0-1s1_4s1-6s0_2_5` (07:56), caused by memory.** Four
   cake_lpr processes of about 4 GB each ran at once, over the 13.4 GB cgroup limit, and the
   kernel OOM-killed one (dmesg: `Memory cgroup out of memory: Killed process … (cake_lpr)`).
   That record has `cake_lpr: "none"` and `certified: false`, and it does not count. The node
   was then re-run alone (`recheck_0s0-1s1_4s1-6s0_2_5.txt`): same CNF sha256, UNSAT in 6 s,
   lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`. The driver was resumed with
   **--jobs 3**, as the task says, and that run certified the node again (a later record in
   `out.jsonl`). There were no further OOM kills. `driver_attempt2.log` is the log up to
   this stop.

**Real proof rejections: none. SAT: none.**

## Per root

Times are wall seconds per process, summed over all of a root's attempts, including the
300 s timeouts. "Splits" includes the driver's --split-singles pre-splits.
Only roots 1–20 were reached. Roots 21–68 were not started (open at depth 2).

| root | status | certified by depth | splits | open by depth | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-1s0_2s0-9s1 | closed | d2:1 | 0 | - | 11 | 33 |
| 0s0-1s0_3s0-6s0 | closed | d2:1 | 0 | - | 5 | 24 |
| 0s0-1s0_4s0-10s1 | closed | d2:1 | 0 | - | 17 | 35 |
| 0s0-1s0_5s0-10s0 | closed | d2:1 | 0 | - | 36 | 36 |
| 0s0-1s0_6s0-7s1 | closed | d2:1 | 0 | - | 85 | 43 |
| 0s0-1s0_7s1-9s0 | closed | d2:1 | 0 | - | 95 | 44 |
| 0s0-1s1_2s0-5s0 | closed | d2:1 | 0 | - | 27 | 34 |
| 0s0-1s1_2s1-9s0 | closed | d2:1 | 0 | - | 57 | 43 |
| 0s0-1s1_3s1-6s1 | closed | d2:1 | 0 | - | 33 | 38 |
| 0s0-1s1_4s1-6s0 | closed | d3:84 d4:462 | 8 | - | 5995 | 9547 |
| 0s0-1s1_5s1-7s1 | closed | d2:1 | 0 | - | 34 | 22 |
| 0s0-1s1_7s0-10s1 | closed | d3:84 d4:462 | 8 | - | 5258 | 8898 |
| 0s0-1s1_9s1-10s1 | closed | d2:1 | 0 | - | 33 | 22 |
| 0s0-2s0_1s1-4s1 | closed | d2:1 | 0 | - | 17 | 19 |
| 0s0-2s0_3s0-9s0 | closed | d2:1 | 0 | - | 59 | 26 |
| 0s0-2s0_4s0-7s1 | closed | d2:1 | 0 | - | 76 | 27 |
| 0s0-2s0_5s0-8s0 | closed | d2:1 | 0 | - | 7 | 13 |
| 0s0-2s0_6s1-10s1 | closed | d2:1 | 0 | - | 14 | 13 |
| 0s0-2s0_8s0-9s1 | closed | d2:1 | 0 | - | 113 | 29 |
| 0s0-2s1_1s0-8s0 | open | d4:101 | 8 | d3:84 d4:361 | 824 | 1568 |
| 0s0-2s1_3s0-4s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-2s1_3s1-9s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-2s1_4s1-9s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-2s1_6s0-10s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-2s1_7s1-10s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s0_1s0-2s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s0_1s1-7s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s0_2s1-5s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s0_4s1-10s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s0_5s1-6s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s0_6s1-9s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s0_9s0-10s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s1_1s1-2s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s1_2s0-7s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s1_4s0-6s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s1_5s0-6s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s1_6s0-9s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-3s1_8s0-10s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s0_1s0-6s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s0_2s0-10s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s0_2s1-8s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s0_3s1-7s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s0_5s1-9s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s0_7s0-9s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s1_1s0-10s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s1_1s1-6s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s1_2s1-10s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s1_3s0-9s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s1_5s0-9s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s1_6s1-8s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-4s1_8s1-9s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s0_1s0-9s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s0_2s0-6s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s0_3s0-10s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s0_4s0-10s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s0_6s0-7s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s0_7s1-9s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s1_1s0-4s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s1_1s1-9s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s1_2s1-6s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s1_3s1-6s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s1_4s1-7s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s1_7s0-10s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0-5s1_9s1-10s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0_1s1-3s1 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0_2s0-8s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0_3s0-7s0 | open | - | 0 | d2:1 | 0 | 0 |
| 0s0_4s1-7s0 | open | - | 0 | d2:1 | 0 | 0 |

## Per depth, over all 68 roots

| depth | certified | split | open |
|---|---|---|---|
| 2 | 17 | 3 | 48 |
| 3 | 168 | 21 | 84 |
| 4 | 1025 | 0 | 361 |
closed roots: 19 of 68

- Closed (certified, or every child closed, recursively): roots 1–19.
- Root 20, `0s0-2s1_1s0-8s0`, is partly done: 101 depth-4 nodes certified. Its 84 depth-3
  two-orbit nodes and 361 depth-4 nodes are unsolved (not tried).
- Roots 21–68 were not tried.
- Totals: 1,214 solver runs, 12,806 s of solve time and 20,533 s of check time. 3 runs hit
  the 300 s cap (the depth-2 nodes of roots 10, 12 and 20, which were then split). The
  largest proof was 297 MB. Proofs and CNFs were deleted.
- The two large roots (10 and 12) each needed 84 + 462 certified nodes and about 4 core-hours
  in total.

## compose.py

`python3 tools/compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`):

```
{"certified_nodes": 1210, "class_covered": false, "uncovered_frontier_nodes": 719, "uncovered_sample": ["0s0", "0s0-1s0_2", "0s0-1s0_3", "0s0-1s0_4", "0s0-1s0_5", "0s0-1s0_6", "0s0-1s0_7", "0s0-1s0_8", "0s0-1s0_9", "0s0-1s0_10"]}
```

All 1,210 certified records passed compose's CNF-sha256 recomputation. As expected, the class
is not covered by one shard.

## Files

`env.txt`, `tools.txt`, `roots.txt`, `out.jsonl` (all node records), `driver.log`,
`driver_attempt1.log`, `driver_attempt2.log`, `recheck_0s0-1s1_4s1-6s0_2_5.txt`,
`compose.txt`, `summary.txt` (this table, from the full `out.jsonl`).

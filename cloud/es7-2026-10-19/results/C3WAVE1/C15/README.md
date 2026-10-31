# C3WAVE1 / C15: machine 15 of 24, wave 1, 3-fold class (m = 11, k = 7)

**Result: 11 of my 68 roots are fully closed. The 12th, `0s0-1s1_7`, is open: it was in progress at the time limit.
The remaining 56 were not started. No SAT. No real proof rejection.** One "PROOF NOT ACCEPTED" was an OOM kill of cake_lpr
(`recheck_0s0-1s0_4_5.md`).

## What ran where
- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Ran from 07:35 to 11:13 UTC on 2026-10-20.
- The C3-S and C3a tools were used unmodified from a worktree of commit `8dc27c3` at /opt/c3s. /opt/work was writable, so the driver needed no change.
- Tool commits are in `tools.txt`:
  - CaDiCaL 3.0.1 c60730422e75
  - cake_lpr a36874a8b750 (the bundled example prints `s VERIFIED UNSAT`)
  - drat-trim lrat-check 2e3b2dc0ecf9 with the E2 patch
- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the depth-2 nodes with index ≡ 15 (mod 24), 68 of them (`roots.tsv`). They come from the SHARD-mode expression in `close_tree.py` and are identical to the matching rows of `manifest_depth2.tsv`. The sha256 of the 1,630 sorted names matches `shard_plan.md`.
- Command for each root, in order: `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`. H was the time left before 11:13. All roots shared one out.jsonl.
  - Run 1 (07:38–08:05) used J = 4. Its log is `run1.log`.
  - Run 2 (08:08–11:13) used J = 3. Its log is `run2.log`. I stopped run 2 at 11:13 because the time budget was used up; in-flight nodes were discarded.

## Incidents
1. **OOM, not a rejection.** In run 1, cake_lpr was OOM-killed twice (dmesg at about 07:42 and 07:58). Each checker needs about 4.2 GB of RSS, and with 4 jobs plus the solvers this exceeded the 15 GB memory cgroup. The driver printed `PROOF NOT ACCEPTED 0s0-1s0_4_5`.
   - I re-ran that node alone. lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT` (`recheck_0s0-1s0_4_5.md`).
   - I resumed with --jobs 3. After that there were no OOM kills, and the driver re-certified the node itself.
2. **File loss in my harness.** At first the driver wrote out.jsonl and run.log directly in the git checkout. `git pull --rebase` replaced those files, so the driver went on writing to deleted inodes. The records from 07:41 to 08:05 were lost, including the rejected record for 0s0-1s0_4_5. All of those nodes were solved and checked again in run 2.
   - Since then the live files sit in /opt/work/c15 and are copied into the repo before each commit.
   - Records were lost, never altered. Every certified record in out.jsonl was written by the driver after both checkers accepted.

## Per root (roots I started; d = depth of the node in the layer tree)
| root | status | certified by depth | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s0_2s0-8s1 | CLOSED | d2: 1 | 0 | 16 | 34 |
| 0s0-1s0_3s0-5s0 | CLOSED | d2: 1 | 0 | 4 | 22 |
| 0s0-1s0_4 | CLOSED | d3: 120 | 1 | 2127 | 2607 |
| 0s0-1s0_4s1-9s1 | CLOSED | d2: 1 | 0 | 26 | 24 |
| 0s0-1s0_6s0-10s1 | CLOSED | d2: 1 | 0 | 54 | 36 |
| 0s0-1s0_7s1-8s0 | CLOSED | d2: 1 | 0 | 93 | 42 |
| 0s0-1s1_2s0-4s0 | CLOSED | d2: 1 | 0 | 34 | 38 |
| 0s0-1s1_2s1-8s0 | CLOSED | d2: 1 | 0 | 61 | 26 |
| 0s0-1s1_3s1-5s1 | CLOSED | d2: 1 | 0 | 33 | 26 |
| 0s0-1s1_4s1-5s0 | CLOSED | d3: 84, d4: 462 | 8 | 6207 | 9586 |
| 0s0-1s1_5s1-6s1 | CLOSED | d2: 1 | 0 | 35 | 22 |
| 0s0-1s1_7 | open | d3: 61 | 9 | 9030 | 2028 |
Solve and check times are summed wall-clock seconds over the root's subtree, with up to 3 or 4 jobs running in parallel.
"Splits" counts nodes split, including pre-splits (`--split-singles`).
`0s0-1s1_7` has 9 splits: the root's own pre-split, plus 8 depth-3 nodes that timed out at the 300 s cap.
Its open frontier is 51 unsolved depth-3 nodes plus 728 depth-4 children.

Roots not started (56): every root after `0s0-1s1_7` in `roots.tsv`, from `0s0-1s1_9s0-10s1` on.

## Per depth, over all 68 roots
| depth | certified | split | open |
|---|---|---|---|
| 2 | 9 | 3 | 56 |
| 3 | 265 | 15 | 51 |
| 4 | 462 | 0 | 728 |
"Open" counts frontier nodes that are neither certified nor split. At depth 2 these are the 56 unstarted roots.

Totals: 745 solver records, of which 736 are certified (both checkers accepted) and 9 hit the cap and were split. Summed solve time is 17,720 s and summed check time is 14,490 s. The largest proof was 368 MB; proofs and CNFs were deleted.

## compose.py
Command: `python3 tools/compose.py /opt/work/base.cnf out.jsonl`. Output (`compose_output.txt`):
```
{"certified_nodes": 736, "class_covered": false, "uncovered_frontier_nodes": 362, "uncovered_sample": ["0s0", "0s0-1s0_2", "0s0-1s0_3", "0s0-1s0_5", "0s0-1s0_6", "0s0-1s0_7", "0s0-1s0_8", "0s0-1s0_9", "0s0-1s0_10", "0s0-1s0_2s0-3s0"]}
```
As expected, it does not report the class covered, because this file holds only my shard. compose.py found no hash mismatches: it recomputes every certified node's CNF sha256.

## SAT / rejections
- No SATISFIABLE node.
- No real proof rejection. The single "PROOF NOT ACCEPTED" (0s0-1s0_4_5) was a cake_lpr OOM kill, and both checkers accept that node when run alone.

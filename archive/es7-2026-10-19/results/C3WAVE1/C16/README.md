# C3WAVE1 / C16: machine 16 of 24, wave 1, 3-fold class (m = 11, k = 7)

Nothing here is a theorem. A node counts as closed only if cake_lpr printed `s VERIFIED UNSAT` on its LRAT
proof and lrat-check (E2 patch) printed `c VERIFIED` (the driver requires both).

## What ran where
- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). It ran from 07:35 to 11:08 UTC on 2026-10-20 (the driver's deadline), and this write-up was done after.
- C3-S/C3a tools from a worktree of commit `8dc27c3` at `/opt/c3s`, used unchanged. `/opt/work` was writable, so the
  driver's work path was not changed (no diff).
- Tools (`tools.txt`): CaDiCaL 3.0.1 `c6073042` (c60730422e75…); cake_lpr `a36874a8` (`make cake_lpr`; bundled
  example prints `s VERIFIED UNSAT`); drat-trim lrat-check `2e3b2dc` + `results/E2/tools/lrat-check-E2.patch`.
- Base CNF: `gen_case.py 11 7 none`, `p cnf 168399 4154921`, sha256
  `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the 68 depth-2 nodes with index ≡ 16 (mod 24), from the driver's SHARD expression. They are identical to the sorted depth-2
  rows of `manifest_depth2.tsv` at the same indices (name-list sha256 `5412782c…` matches). The list is in `roots.tsv`.
- Command per root, roots one at a time in order (H = time left):
  `close_tree.py base.cnf out.jsonl ROOT --jobs J --caps 300,300,600 --cadopts=--sat --split-singles --hours H`.
  J = 4 for the first 4 roots, then J = 3 after an out-of-memory failure (see below).
  With one root at a time, a root that closes as a single node uses only one core.

## Results
`out.jsonl` holds the records, `driver.log` the driver output, `summary.tsv` comes from `summarize_c16.py`, and `compose.txt` is compose's output.

**7 of 68 roots are fully closed.** One more was in progress at the deadline, and 60 were never started.

| root | status | certified by depth | splits | open leaves | solve s | check s |
|---|---|---|---|---|---|---|
| 0s0-1s0_2s0-9s0 | closed | d2: 1 | 0 | 0 | 58 | 41 |
| 0s0-1s0_3s0-5s1 | closed | d2: 1 | 0 | 0 | 65 | 38 |
| 0s0-1s0_4s0-10s0 | closed | d2: 1 | 0 | 0 | 45 | 37 |
| 0s0-1s0_5 | closed | d3: 120 | 1 (presplit) | 0 | 2307* | 2527* |
| 0s0-1s0_6s0-7s0 | closed | d2: 1 | 0 | 0 | 5 | 14 |
| 0s0-1s0_7s1-8s1 | closed | d2: 1 | 0 | 0 | 5 | 18 |
| 0s0-1s1_2s0-4s1 | closed | d3: 84, d4: 462 | 8 (root timed out at 300 s + 7 presplits) | 0 | 5780 | 8879 |
| 0s0-1s1_2s1-8s1 | **open** (in progress at deadline) | d3: 66, d4: 462 | 8 | 18 (depth 3) | 4622 | 8020 |
| remaining 60 roots (index 208 … 1624) | open, not started | – | – | – | – | – |

Solve and check times are summed per node as wall-clock seconds, with 3–4 processes sharing 4 cores. *These include the one node
that was solved twice (0s0-1s0_5_6, after the OOM failure). Records lost in the 08:22 incident (below) are not counted.

Per depth over all 68 roots (open = leaf not certified, including roots never started):

| depth | certified | split | open |
|---|---|---|---|
| 2 | 5 | 3 | 60 |
| 3 | 270 | 14 | 18 |
| 4 | 924 | 0 | 0 |

Total: 1,199 certified nodes. `compose.py base.cnf out.jsonl` gives `certified_nodes 1199, class_covered false,
uncovered_frontier_nodes 325`, as expected for one shard.

**SAT: none.** No proof was rejected by both checkers.

## Incidents
1. **PROOF NOT ACCEPTED 0s0-1s0_5_6 (07:44, --jobs 4): out of memory, not a real rejection.** lrat-check printed `c VERIFIED`, but
   cake_lpr gave no output because the memory cgroup OOM killer had killed it (dmesg). Re-run alone, the same CNF (sha 196b59d3…) gave
   UNSAT in 76 s. lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`. Details are in `recheck_0s0-1s0_5_6.md`. I resumed with --jobs 3, and there
   were no further problems. Driver issue: after it prints PROOF NOT ACCEPTED, `close_tree.py` returns inside the
   ProcessPoolExecutor block. The block's exit then waits for every node already queued in the batch and discards their results. I killed it by hand.
2. **Lost records (08:22).** My own push step committed the driver's output files from inside the git tree and then ran
   `git pull --rebase --autostash`. That rewrote the files while the driver held them open, so the driver's later appends went to an
   unlinked inode. The records of 10 depth-3 children of 0s0-1s0_5 were lost, along with the driver's final line. No record was corrupted:
   every line is valid JSON, and certification comes from each record. At 08:33 I restarted the driver with its files
   in `/opt/work`, copied into the results dir before each commit. It re-solved and certified those 10 nodes. Root 0s0-1s1_2s0-4s1,
   which was in progress at the restart, resumed from its records, and its in-flight nodes were re-solved.

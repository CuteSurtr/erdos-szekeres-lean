# C3WAVE2 K39 (shard i = 39, N = 40, H = 1.5 h)

Task: `results/C3WAVE2/TASK.md` at 852bee7. Start 00:31:21 UTC, END (start + 1.5 h - 15 min) = 01:46:21 UTC. Runner stopped by hand at 01:50 UTC (time budget).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and base CNF (`tools.txt`)
- C3-S tools: worktree of 132398c (8dc27c3 before the rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc + lrat-check-E2.patch.
  Sanity check passed: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…dd6da (matches).
- Roots: 33 rows of C3WAVE2/roots.tsv with idx ≡ 39 (mod 40) (`roots.tsv`).

## Run
`runner.sh` used a 10-minute slice per root with `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles`.
- Root `0s0-2s0_7` overran its slice: it started at 00:36:51 and ended at 01:06:20. The driver finishes the jobs it has already started (their caps run up to 600 s) after the slice ends.
- **A restart interrupted the run.** At about 01:2x UTC the session's worker/VM was restarted, which killed the runner during root `0s0-2s1_5s1-6s0` (/opt/work/out.jsonl and the tools survived). At 01:24:11 `runner_resume.sh` restarted the run at that root. It is `runner.sh` with the root list starting at `0s0-2s1_5s1-6s0` and the same START/END. close_tree resumed from out.jsonl and kept the existing certified children. The only duplicate record is the root's split line. The interruption is marked in driver.log with `=== RESTART`.
- At 01:50 UTC, past END, I killed the runner by hand during root `0s0-2s1_5s1-6s0`; this is marked with `=== KILLED`. Every record of that root stays in out.jsonl, so it can be resumed.
- There was no SAT FOUND, no PROOF NOT ACCEPTED, and no memory problem (at most about 7 GB in use).

## Per root
"certified by depth": depth = number of layers (roots are at depth 2). solve/check = summed seconds.

| root | status | certified by depth | splits | solve s | check s | unknown runs |
|---|---|---|---|---|---|---|
| 0s0-1s1_7s1-10s1 | closed (frontier 0) | d2:1 | 0 | 26 | 29 | 0 |
| 0s0-2s0_1s1-8s0 | closed (frontier 0) | d2:1 | 0 | 9 | 21 | 0 |
| 0s0-2s0_4s1-5s0 | closed (frontier 0) | d2:1 | 0 | 90 | 35 | 0 |
| 0s0-2s0_7 | closed (frontier 0) | d3:120 | 1 | 2820 | 2424 | 0 |
| 0s0-2s1_1s1-3s1 | closed (frontier 0) | d2:1 | 0 | 38 | 21 | 0 |
| 0s0-2s1_3s1-9s0 | closed (frontier 0) | d2:1 | 0 | 63 | 27 | 0 |
| 0s0-2s1_5s1-6s0 | partial (frontier ?) | d3:71, d4:96 | 8 | 3505 | 3048 | 1 |
| 0s0-2s1_8s0-10s1 | not reached | | | | | |
| 0s0-3s0_1s1-7s0 | not reached | | | | | |
| 0s0-3s0_4s0-6s0 | not reached | | | | | |
| 0s0-3s0_5s1-9s1 | not reached | | | | | |
| 0s0-3s0_9 | not reached | | | | | |
| 0s0-3s1_2s0-10s0 | not reached | | | | | |
| 0s0-3s1_4s0-9s1 | not reached | | | | | |
| 0s0-3s1_6s0-8s1 | not reached | | | | | |
| 0s0-4s0_1s0-10s0 | not reached | | | | | |
| 0s0-4s0_2s0-6s1 | not reached | | | | | |
| 0s0-4s0_3s1-7s0 | not reached | | | | | |
| 0s0-4s0_6s1-8s0 | not reached | | | | | |
| 0s0-4s1_1s0-5s1 | not reached | | | | | |
| 0s0-4s1_2s1-10s0 | not reached | | | | | |
| 0s0-4s1_5s0-10s0 | not reached | | | | | |
| 0s0-4s1_7s0-8s0 | not reached | | | | | |
| 0s0-5s0_1s0-9s0 | not reached | | | | | |
| 0s0-5s0_2s1-6s1 | not reached | | | | | |
| 0s0-5s0_4s0-8s1 | not reached | | | | | |
| 0s0-5s0_7s1-8s1 | not reached | | | | | |
| 0s0-5s1_1s1-3s1 | not reached | | | | | |
| 0s0-5s1_3 | not reached | | | | | |
| 0s0-5s1_4s1-7s0 | not reached | | | | | |
| 0s0-5s1_8s0-9s1 | not reached | | | | | |
| 0s0_1s1-7s0 | not reached | | | | | |
| 0s0_3s0-6s1 | not reached | | | | | |

Closed roots (6): 0s0-1s1_7s1-10s1, 0s0-2s0_1s1-8s0, 0s0-2s0_4s1-5s0, 0s0-2s0_7, 0s0-2s1_1s1-3s1, 0s0-2s1_3s1-9s0.
`0s0-2s0_7` was split once into 120 children, and all 120 are certified; the other five closed as single depth-2 nodes.

Partial (1): 0s0-2s1_5s1-6s0. It hit the cap at depth 2 (status UNKNOWN), was split into 91 children, and 7 of those were single-split into 66 each. That is 553 children in all; 167 are certified (71 at depth 3, 96 at depth 4) and 7 are split, so about 379 are still open.

Not reached (26): every other root in `roots.tsv`.

## Totals
292 certified nodes, each accepted by both cake_lpr (`s VERIFIED UNSAT`) and lrat-check. There are 9 split records, about 6552 s of solve time and 5605 s of check time. `compose.txt`: certified_nodes 292, class_covered false (expected).

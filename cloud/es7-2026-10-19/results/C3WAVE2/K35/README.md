# C3WAVE2 K35: shard 35 of 40 (idx ≡ 35 mod 40, 33 roots)

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 00:31:20 UTC on 2026-10-21, END (start + 1.5 h - 15 min) 01:46:20 UTC.

## Tools and base CNF (`tools.txt`)
- C3-S tools: worktree of 132398c (8dc27c3 before the author rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`; example prints `s VERIFIED UNSAT`), drat-trim lrat-check 2e3b2dc with lrat-check-E2.patch.
  Sanity check passed: on {1},{-1}, LRAT `3 0 0` rejected by both (lrat-check `c NOT VERIFIED`, cake_lpr `pivot must be non-zero`), `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…0cdd6da (matches).

## Run
`runner.sh`: per root, `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`.
6 of 33 roots were started. Root 6 (0s0-2s1_3s1-7s0) began at 00:42:00 and ran far past its 10-minute slice: close_tree.py checks
its deadline only between levels, so once the root timed out at its 300 s cap and was split (91 children, with the single-orbit layers
pre-split), the whole next level had to finish first. **At about 01:42 UTC the VM rebooted** (uptime 0 min, new kernel build) and killed the runner
in the middle of that level. All 503 records written before then are intact and parse as JSON. With 4 minutes left before END the runner was
not restarted. No memory problem showed (peak ~5 GB used); no OOM.

## Per root
| root | status | certified (by depth) | splits | solve s | check s |
|---|---|---|---|---|---|
| 0s0-1s1_7s0-8s0 | closed | 1 (d2) | 0 | 30.0 | 35.6 |
| 0s0-2s0_1s1-6s0 | closed | 1 (d2) | 0 | 56.4 | 37.7 |
| 0s0-2s0_4s0-9s0 | closed | 1 (d2) | 0 | 35.3 | 33.3 |
| 0s0-2s0_6s1-8s0 | closed | 1 (d2) | 0 | 105.1 | 42.8 |
| 0s0-2s1_1s0-9s1 | closed | 1 (d2) | 0 | 51.5 | 34.6 |
| 0s0-2s1_3s1-7s0 | partial | 489 (d3: 27, d4: 462) | 8 (root UNKNOWN at 300 s + 7 pre-splits) | 3068.1 | 6970.5 |
| the other 27 | not reached | | | | |

Partial root 0s0-2s1_3s1-7s0: 57 open frontier nodes are left (none of them solved yet); a later wave resumes it from `out.jsonl`.

Closed (5): 0s0-1s1_7s0-8s0, 0s0-2s0_1s1-6s0, 0s0-2s0_4s0-9s0, 0s0-2s0_6s1-8s0, 0s0-2s1_1s0-9s1.
Partial (1): 0s0-2s1_3s1-7s0.
Not reached (27): 0s0-2s1_5s0-9s0 0s0-2s1_7s1-9s0 0s0-3s0_1s1-5s0 0s0-3s0_4s0-10s0 0s0-3s0_5s1-7s1 0s0-3s0_8s1-10s0 0s0-3s1_1s1-8s1 0s0-3s1_4s0-7s1 0s0-3s1_6s0-10s1 0s0-3s1_9s1-10s0 0s0-4s0_2s0-3s1 0s0-4s0_3s1-5s0 0s0-4s0_6s1-10s0 0s0-4s1_1s0-2s1 0s0-4s1_2s0-8s0 0s0-4s1_3s1-8s1 0s0-4s1_6s1-9s1 0s0-5s0_1s0-7s0 0s0-5s0_2s1-3s1 0s0-5s0_4s0-6s1 0s0-5s0_7s0-9s1 0s0-5s1_1s1-10s1 0s0-5s1_2s1-8s0 0s0-5s1_4s1-10s0 0s0-5s1_8 0s0_1s1-5s0 0s0_3s0-4s1 

## Totals
503 records: 494 UNSAT nodes, all certified (cake_lpr `s VERIFIED UNSAT` and lrat-check `c VERIFIED`), 1 UNKNOWN, 8 split records.
Solve time 0.93 h and check time 1.99 h in total (summed over jobs). Largest proof 265 MB (not committed).
**No SAT FOUND, no PROOF NOT ACCEPTED.**
`compose.txt`: 494 certified nodes, class_covered false (as expected), 518 uncovered frontier nodes.

Files: env.txt, tools.txt, roots.tsv, runner.sh, out.jsonl, driver_tail.log (last 200 lines of driver.log), compose.txt.

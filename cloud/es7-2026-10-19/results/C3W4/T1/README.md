# C3W4 / T1: wave 4, W4_two.tsv shard 1 of 4 (σ-cube splitting)

**Result: 8 of my 44 roots are closed (open frontier 0, no childless timed-out node). One root (#9, `0s0-3s1_4s0-8s0`) was started at 15:14:14 and killed at END (15:16:38) before it wrote any record; it counts as not reached, like roots 10–44. No partial roots. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:27 UTC, END 15:16:27 UTC (start + 4 h − 15 min); runner 11:34:53 to 15:16:38.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified (no `compose.py` run, as TASK.md says).
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc with the E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches). Details in `tools.txt`.
- Roots: rows of `lists/W4_two.tsv` with row ≡ 1 (mod 4), 44 roots (`roots.tsv`), none seeded.
- Runner (`runner.sh`): per root `close_tree.py /opt/work/base.cnf /opt/work/out.jsonl R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(1.0, hours left before END). A watchdog killed close_tree and the solvers/checkers at END.

## Per root

"certified (layers, σ level)": number of certified nodes by layer depth of the node and number of σ-splits (3 bits each) on its path. Timeouts are UNKNOWN records at the 300 s cap; each was σ-split (24 σ-splits, 0 layer splits, 0 pre-splits, 0 records with `"children": 0`). Solve and check seconds are summed over nodes (3 jobs share 4 cores).

| # | root | stratum | status | certified (layers, σ level): n | timeouts | childless split | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 1 | 0s0-3s1_1s0-9s0 | H6(3,1)/two | closed | (2,1): 5, (2,2): 24 | 4 | 0 | 3615 | 1560 |
| 2 | 0s0-3s1_4s0-7s1 | H6(3,1)/two | closed | (2,1): 2, (2,2): 48 | 7 | 0 | 5591 | 2378 |
| 3 | 0s0-4s0_1s0-9s0 | H6(4,0)/two | closed | (2,1): 8 | 1 | 0 | 1494 | 495 |
| 4 | 0s0-4s1_5s0-6s1 | H6(4,1)/two | closed | (2,1): 1, (2,2): 56 | 8 | 0 | 6765 | 2915 |
| 5 | 0s0-5s0_1s0-3s1 | H6(5,0)/two | closed | (2,1): 7, (2,2): 8 | 2 | 0 | 2193 | 770 |
| 6 | 0s0-5s0_2s0-10s0 | H6(5,0)/two | closed | (2,1): 8 | 1 | 0 | 1602 | 430 |
| 7 | 0s0-5s0_7s1-9s0 | H6(5,0)/two | closed | (2,1): 8 | 1 | 0 | 1630 | 486 |
| 8 | 0s0-2s0_3s1-7s1 | H6(2,0)/two | closed | (2,0): 1 | 0 | 0 | 176 | 45 |
| 9 | 0s0-3s1_4s0-8s0 | H6(3,1)/two | not reached | – | – | – | – | – |
| 10 | 0s0-3s1_5s0-6s0 | H6(3,1)/two | not reached | – | – | – | – | – |
| 11 | 0s0-3s1_5s1-8s0 | H6(3,1)/two | not reached | – | – | – | – | – |
| 12 | 0s0-4s0_2s0-5s0 | H6(4,0)/two | not reached | – | – | – | – | – |
| 13 | 0s0-4s0_2s0-7s0 | H6(4,0)/two | not reached | – | – | – | – | – |
| 14 | 0s0-4s1_1s0-6s1 | H6(4,1)/two | not reached | – | – | – | – | – |
| 15 | 0s0-4s1_1s1-2s0 | H6(4,1)/two | not reached | – | – | – | – | – |
| 16 | 0s0-4s1_1s1-9s1 | H6(4,1)/two | not reached | – | – | – | – | – |
| 17 | 0s0-4s1_2s0-5s1 | H6(4,1)/two | not reached | – | – | – | – | – |
| 18 | 0s0-4s1_2s0-8s0 | H6(4,1)/two | not reached | – | – | – | – | – |
| 19 | 0s0-4s1_5s0-7s1 | H6(4,1)/two | not reached | – | – | – | – | – |
| 20 | 0s0-4s1_5s1-6s0 | H6(4,1)/two | not reached | – | – | – | – | – |
| 21 | 0s0-4s1_5s1-8s1 | H6(4,1)/two | not reached | – | – | – | – | – |
| 22 | 0s0-4s1_6s1-7s1 | H6(4,1)/two | not reached | – | – | – | – | – |
| 23 | 0s0-4s1_7s0-8s0 | H6(4,1)/two | not reached | – | – | – | – | – |
| 24 | 0s0-5s0_1s0-9s0 | H6(5,0)/two | not reached | – | – | – | – | – |
| 25 | 0s0-5s0_1s1-2s0 | H6(5,0)/two | not reached | – | – | – | – | – |
| 26 | 0s0-5s0_2s0-8s0 | H6(5,0)/two | not reached | – | – | – | – | – |
| 27 | 0s0-5s0_2s1-10s0 | H6(5,0)/two | not reached | – | – | – | – | – |
| 28 | 0s0-5s0_6s0-9s1 | H6(5,0)/two | not reached | – | – | – | – | – |
| 29 | 0s0-5s0_6s1-8s0 | H6(5,0)/two | not reached | – | – | – | – | – |
| 30 | 0s0-5s0_7s0-8s0 | H6(5,0)/two | not reached | – | – | – | – | – |
| 31 | 0s0-5s1_1s0-2s0 | H6(5,1)/two | not reached | – | – | – | – | – |
| 32 | 0s0-5s1_1s0-6s1 | H6(5,1)/two | not reached | – | – | – | – | – |
| 33 | 0s0-5s1_1s0-9s0 | H6(5,1)/two | not reached | – | – | – | – | – |
| 34 | 0s0-5s1_1s1-2s1 | H6(5,1)/two | not reached | – | – | – | – | – |
| 35 | 0s0-5s1_1s1-7s1 | H6(5,1)/two | not reached | – | – | – | – | – |
| 36 | 0s0-5s1_2s0-10s0 | H6(5,1)/two | not reached | – | – | – | – | – |
| 37 | 0s0-5s1_2s0-6s1 | H6(5,1)/two | not reached | – | – | – | – | – |
| 38 | 0s0-5s1_2s1-10s0 | H6(5,1)/two | not reached | – | – | – | – | – |
| 39 | 0s0-5s1_2s1-7s0 | H6(5,1)/two | not reached | – | – | – | – | – |
| 40 | 0s0-5s1_2s1-9s1 | H6(5,1)/two | not reached | – | – | – | – | – |
| 41 | 0s0-5s1_6s0-7s1 | H6(5,1)/two | not reached | – | – | – | – | – |
| 42 | 0s0-5s1_6s1-8s0 | H6(5,1)/two | not reached | – | – | – | – | – |
| 43 | 0s0-5s1_7s0-8s0 | H6(5,1)/two | not reached | – | – | – | – | – |
| 44 | 0s0-5s1_7s1-8s1 | H6(5,1)/two | not reached | – | – | – | – | – |

## Totals per stratum

| stratum | closed | partial | not reached | certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|
| H6(2,0)/two | 1 | 0 | 0 | 1 | 0 | 176 | 45 |
| H6(3,1)/two | 2 | 0 | 3 | 79 | 11 | 9206 | 3938 |
| H6(4,0)/two | 1 | 0 | 2 | 8 | 1 | 1494 | 495 |
| H6(4,1)/two | 1 | 0 | 10 | 57 | 8 | 6765 | 2915 |
| H6(5,0)/two | 3 | 0 | 7 | 31 | 4 | 5425 | 1686 |
| H6(5,1)/two | 0 | 0 | 14 | 0 | 0 | 0 | 0 |

Total: 224 records, 176 certified nodes (all with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`), 24 timeouts, 24 σ-split records. No record with cake_lpr `none`, so no re-check was needed (no `recheck.jsonl`).

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: peak use about 9 GB of 15 GB (three cake_lpr runs at once); no failure.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records), `driver.log.tail` (last 100 lines of the driver log), `README.md`.

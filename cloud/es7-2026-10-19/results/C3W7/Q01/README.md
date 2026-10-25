# C3W7 Q01: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv, shard 1 of 36)

Task `results/C3W7/TASK.md` at 39bb1bac, with V = Q01, LIST = W7.tsv, j = 1, N = 36, H = 4.5. One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:11 UTC, lanes started 10:49:40, END 15:01:11 UTC (start + 4.5 h − 15 min). The watchdog killed the lanes at 15:01:23.

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity check passed: LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).

## Run

- 54 units: rows of W7.tsv with row ≡ 1 (mod 36), listed in `units.tsv`. No records were seeded.
- 3 lanes (`lane0.sh` to `lane2.sh`, started with `setsid nohup`). Each runs `close_tree.py … --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds the records of lane 0, then lane 1, then lane 2 (48 solve records and 44 layer-split records). The `driver{k}.log.tail` files hold the end of each driver log.
- Outcome: 51 units started. 48 finished (4 certified, 44 timed out at 900 s). 3 were killed at END with no record, and 3 were never started.
- Nothing went wrong:
  - no SAT;
  - no `PROOF NOT ACCEPTED`;
  - no certified-looking record with cake_lpr `none`, so no rechecks were needed and there is no `recheck.jsonl`;
  - no unit ended in under 72 s;
  - no memory problem (at most about 2 GB used, 13 GB available).
- Timeout rate: only 4 of the 48 solved units (8%) were certified within 900 s. The X1 pilot (450–662 s) suggested most would be. Each timed-out unit has its layer-split record (45 children, unsolved, in `open_frontier`), as the task intends.

## Per unit

| row | unit | parent six-bit cube | lane | result |
|---|---|---|---|---|
| 1 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0` | 0 | certified (solve 696.3 s, check 100.4 s) |
| 37 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 73 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 109 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 145 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 181 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 217 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 253 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 289 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 325 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 361 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 397 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 433 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 469 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 505 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 541 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 577 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0` | 1 | certified (solve 817.1 s, check 102.9 s) |
| 613 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 649 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 685 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 721 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 757 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 793 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 829 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 865 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 901 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 937 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 973 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1009 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1045 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1081 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1117 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1153 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0` | 2 | certified (solve 804.6 s, check 95.3 s) |
| 1189 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1225 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1261 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1297 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1333 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1369 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1405 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1441 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1477 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1513 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1549 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1` | 1 | certified (solve 816.3 s, check 90.7 s) |
| 1585 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1621 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0` | 0 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1657 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1` | 1 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1693 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1` | 2 | timed out at 900 (layer-split record, 45 children, unsolved) |
| 1729 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0` | 0 | not reached (started 14:48–14:51, killed at END, no record) |
| 1765 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0` | 1 | not reached (started 14:48–14:51, killed at END, no record) |
| 1801 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1` | 2 | not reached (started 14:48–14:51, killed at END, no record) |
| 1837 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1` | 0 | not reached |
| 1873 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0` | 1 | not reached |
| 1909 | `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0` | 2 | not reached |

## Totals per root

| root | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|
| 0s0_1 | 15 | 1 | 14 | 0 |
| 0s0_2 | 14 | 1 | 13 | 0 |
| 0s0_3 | 14 | 1 | 13 | 0 |
| 0s0_4 | 11 | 1 | 4 | 6 |
| all | 54 | 4 | 44 | 6 |

Per parent six-bit cube: each of the 54 units has a different parent (rows are 36 apart and every parent has 8 consecutive rows), so every parent has exactly one unit on this machine; its total is that unit's result in the table above. Parents all of whose units on this machine were certified (4):

- `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0`
- `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0`
- `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0`
- `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1`

## Solve times of the certified units

4 certified: min 696.3 s, Q1 777.5 s, median 810.5 s, Q3 816.5 s, p90 816.9 s, max 817.1 s; certified above 300 s: 4 of 4. Check times (both checkers) 90.7–102.9 s.

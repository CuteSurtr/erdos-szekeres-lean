# C3W7 / Q06: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv, shard 6 of 36)

**Result: 0 of 53 units certified. 48 timed out at 900 s, and 5 were not reached (3 of them were running when the lanes were killed at END). No SAT, no proof rejection, no memory problem, and no unit ended early.**

## Setup

- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:33 UTC, END 15:01:33 UTC (H = 4.5 h minus 15 min). The lanes ran from 10:50 to 15:01.
- Tools (`tools.txt`): C3U2 tools from a worktree of cad4e050 (`/opt/c3u2`), used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Checker sanity test passed: `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Units: rows of `lists/W7.tsv` with row ≡ 6 (mod 36), giving 53 nine-bit cubes (`units.tsv`). Nothing was seeded. 3 lanes ran (`lane.sh`, `lane0..2.sh`). Each unit ran `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. `compose.py` was not run.

## Outcome

- Every one of the 48 attempted units returned `UNKNOWN`, with solve times from 900.1 to 900.3 s. Each unit's single solve took the full cap of about 900 s, and no unit ended in under 72 s.
- As intended, close_tree wrote a layer-split record with 45 children for each timed-out unit (48 split records, `unsplittable` 0). Those children were not solved and are in `open_frontier`.
- Certified units: none. So there is no solve-time distribution, and none were certified above 300 s.
- 5 units were not reached: rows 1734, 1770 and 1806 were running when the lanes were killed at END (started 14:50, so they would have finished after END), and rows 1842 and 1878 were never started.
- SAT: none. PROOF NOT ACCEPTED: none (no `recheck.jsonl`). There were no checker runs at all, so no node has cake_lpr `none`. Memory stayed at about 2.5 GB used out of 16 GB.
- Note: the 3 lanes ran concurrently on 4 cores. The 450–662 s times in `results/C3H1/X1` were not reproduced on this machine for any of these 48 cubes.

## Totals per root

| root | certified | timed out at 900 | not reached | other |
|---|---|---|---|---|
| `0s0_1` | 0 | 15 | 0 | 0 |
| `0s0_2` | 0 | 14 | 0 | 0 |
| `0s0_3` | 0 | 14 | 0 | 0 |
| `0s0_4` | 0 | 5 | 5 | 0 |

## Totals per parent six-bit cube

Each parent has exactly one unit on this machine. Parents with all their units certified here: none.

| parent | certified | timed out at 900 | not reached | other |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0` | 0 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1` | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1` | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0` | 0 | 0 | 1 | 0 |

## Per unit

| pos | row | lane | node | result |
|---|---|---|---|---|
| 0 | 6 | lane 0 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 1 | 42 | lane 1 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 2 | 78 | lane 2 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 3 | 114 | lane 0 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 4 | 150 | lane 1 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 5 | 186 | lane 2 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 6 | 222 | lane 0 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 7 | 258 | lane 1 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 8 | 294 | lane 2 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 9 | 330 | lane 0 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 10 | 366 | lane 1 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 11 | 402 | lane 2 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 12 | 438 | lane 0 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 13 | 474 | lane 1 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 14 | 510 | lane 2 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 15 | 546 | lane 0 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 16 | 582 | lane 1 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 17 | 618 | lane 2 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 18 | 654 | lane 0 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 19 | 690 | lane 1 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 20 | 726 | lane 2 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 21 | 762 | lane 0 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 22 | 798 | lane 1 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 23 | 834 | lane 2 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 24 | 870 | lane 0 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 25 | 906 | lane 1 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 26 | 942 | lane 2 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 27 | 978 | lane 0 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 28 | 1014 | lane 1 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 29 | 1050 | lane 2 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 30 | 1086 | lane 0 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 31 | 1122 | lane 1 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 32 | 1158 | lane 2 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 33 | 1194 | lane 0 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 34 | 1230 | lane 1 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 35 | 1266 | lane 2 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.3 s; split record: 45 children) |
| 36 | 1302 | lane 0 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 37 | 1338 | lane 1 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 38 | 1374 | lane 2 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 39 | 1410 | lane 0 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 40 | 1446 | lane 1 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 41 | 1482 | lane 2 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 42 | 1518 | lane 0 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 43 | 1554 | lane 1 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 44 | 1590 | lane 2 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s; split record: 45 children) |
| 45 | 1626 | lane 0 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 46 | 1662 | lane 1 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 47 | 1698 | lane 2 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s; split record: 45 children) |
| 48 | 1734 | lane 0 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0-8s1-9s1-10s0` | not reached |
| 49 | 1770 | lane 1 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s0-9s1-10s0` | not reached |
| 50 | 1806 | lane 2 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1-8s1-9s1-10s0` | not reached |
| 51 | 1842 | lane 0 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s0-9s1-10s0` | not reached |
| 52 | 1878 | lane 1 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0-8s1-9s1-10s0` | not reached |

## Files

`env.txt`, `tools.txt`, `units.tsv`, `lane.sh`, `lane0.sh`, `lane1.sh`, `lane2.sh`, `out.jsonl` (lane 0, then 1, then 2: 48 solve records and 48 split records), and `driver{0,1,2}.log.tail`.

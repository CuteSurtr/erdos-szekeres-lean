# C3W7 / Q31: nine-bit σ-cubes of the H3/one roots, shard 31 of 36 of W7.tsv

**Result: of 53 units, 34 certified, 17 timed out at 900 s, and 2 were killed at END. No SAT. No proof rejections. No memory problems. No unit ended early.**

## Setup

- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Started 2026-10-25 10:46:28 UTC; lanes launched at 10:48:57; END was 15:01:28 UTC (start + 4.5 h − 15 min). At END, lanes 0 and 1 were killed (their whole process groups, then the cadical processes). Lane 2 had already finished its units at 14:50:11.
- Tools (`tools.txt`): the C3U2 tools from a worktree of cad4e050, unmodified. CaDiCaL 3.0.1 at c6073042, cake_lpr at a36874a8 (its example gives `s VERIFIED UNSAT`), and lrat-check at 2e3b2dc with the E2 patch. In the sanity test, `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Units: rows of `lists/W7.tsv` with row ≡ 31 (mod 36), giving 53 units (`units.tsv`). Each has a different parent six-bit cube. No records were seeded.
- 3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`). Lane k ran the units at positions ≡ k (mod 3), with `close_tree.py base.cnf out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds the lane 0, lane 1 and lane 2 records in that order. There is no `recheck.jsonl` because no re-check was needed. Every certified record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- Each of the 17 timed-out units has a layer-split record with 45 children, all of them unsolved (`open_frontier` 45), as the task intends. `unsplittable` was 0 for every unit.
- The 2 units killed at END (rows 1867 and 1903) were still in their cadical solve and have no record.

## Per unit

| row | unit | result |
|---|---|---|
| 31 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | certified (761.4 s solve, 112.4 s check) |
| 67 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | certified (585.1 s solve, 105.5 s check) |
| 103 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | certified (772.8 s solve, 119.6 s check) |
| 139 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | certified (875.4 s solve, 113.5 s check) |
| 175 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | certified (828.8 s solve, 115.6 s check) |
| 211 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 |
| 247 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | certified (731.0 s solve, 105.5 s check) |
| 283 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | certified (811.1 s solve, 121.2 s check) |
| 319 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | certified (779.6 s solve, 102.1 s check) |
| 355 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 |
| 391 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 |
| 427 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 |
| 463 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 |
| 499 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | certified (887.8 s solve, 109.3 s check) |
| 535 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | certified (636.0 s solve, 95.4 s check) |
| 571 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | certified (772.2 s solve, 109.7 s check) |
| 607 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | certified (783.4 s solve, 98.2 s check) |
| 643 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | certified (671.2 s solve, 105.1 s check) |
| 679 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | certified (826.6 s solve, 110.1 s check) |
| 715 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 |
| 751 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | certified (713.4 s solve, 97.0 s check) |
| 787 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | certified (734.0 s solve, 102.5 s check) |
| 823 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 |
| 859 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 |
| 895 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | certified (820.1 s solve, 97.2 s check) |
| 931 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 |
| 967 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 |
| 1003 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 |
| 1039 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | certified (724.9 s solve, 101.3 s check) |
| 1075 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | certified (732.5 s solve, 111.4 s check) |
| 1111 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | certified (758.9 s solve, 97.3 s check) |
| 1147 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | certified (614.7 s solve, 83.7 s check) |
| 1183 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | certified (761.4 s solve, 93.6 s check) |
| 1219 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | certified (768.6 s solve, 103.6 s check) |
| 1255 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 |
| 1291 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | certified (614.2 s solve, 85.0 s check) |
| 1327 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | certified (852.6 s solve, 103.4 s check) |
| 1363 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 |
| 1399 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | certified (776.0 s solve, 93.2 s check) |
| 1435 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 |
| 1471 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | certified (862.9 s solve, 97.8 s check) |
| 1507 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 |
| 1543 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0-8s1-9s1-10s1` | certified (588.2 s solve, 74.2 s check) |
| 1579 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1-8s0-9s1-10s1` | certified (671.1 s solve, 92.8 s check) |
| 1615 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1-8s1-9s1-10s1` | certified (683.3 s solve, 89.5 s check) |
| 1651 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0-8s0-9s1-10s1` | certified (803.9 s solve, 95.5 s check) |
| 1687 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0-8s1-9s1-10s1` | certified (784.0 s solve, 103.1 s check) |
| 1723 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1-8s0-9s1-10s1` | certified (818.6 s solve, 88.2 s check) |
| 1759 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 |
| 1795 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s0-9s1-10s1` | certified (622.1 s solve, 82.0 s check) |
| 1831 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 |
| 1867 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s0-9s1-10s1` | started, killed at END (no record) |
| 1903 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s1-9s1-10s1` | started, killed at END (no record) |

## Per root

| root | units | certified | timed out | not reached / killed |
|---|---|---|---|---|
| `0s0_1` | 14 | 9 | 5 | 0 |
| `0s0_2` | 14 | 8 | 6 | 0 |
| `0s0_3` | 14 | 10 | 4 | 0 |
| `0s0_4` | 11 | 7 | 2 | 2 |

## Per parent six-bit cube

| parent | units | certified | timed out | not reached / killed |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 0 | 1 |

Parents all of whose units on this machine were certified (34):
- `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1`
- `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0`
- `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0`
- `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1`
- `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1`
- `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0`
- `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1`
- `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1`
- `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0`
- `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0`
- `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1`
- `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1`
- `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0`
- `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0`
- `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1`
- `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0`
- `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1`
- `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1`
- `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0`
- `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0`
- `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1`
- `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1`
- `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0`
- `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1`
- `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1`
- `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0`
- `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1`
- `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0`
- `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1`
- `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1`
- `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0`
- `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0`
- `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1`
- `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0`

## Solve times of certified units (n = 34)

min 585.1, Q1 680.3, median 765.0, Q3 813.0, p90 857.8, max 887.8 s; certified above 300 s: 34

Solve and check times are per node, measured while 3 lanes shared the 4 cores.

## SAT / rejections / incidents

- SAT: none.
- PROOF NOT ACCEPTED: none. No record has cake_lpr `none`.
- Memory: peak use about 10 GB of 15 GB. No OOM.
- Units that ended early (under 72 s without a certificate): none. Every timeout ran the full 900 s cap.

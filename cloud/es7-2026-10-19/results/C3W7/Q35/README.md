# C3W7 / Q35: nine-bit σ-cubes of the H3/one roots, shard 35 of 36 of W7.tsv

**Result: of the 53 units, 17 were certified, 32 timed out at 900 s, and 4 were not reached (3 of these were killed at END while running). No SAT. No proof rejections. No memory problems. No unit ended early.**

## Setup

- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 10:46:21 UTC. Lanes started 10:48:32. END was 15:01:21 UTC.
- Tools (`tools.txt`): the C3U2 tools from a worktree of `cad4e050`, used unmodified. CaDiCaL 3.0.1 `c6073042`, cake_lpr `a36874a8` (example prints `s VERIFIED UNSAT`), and drat-trim lrat-check `2e3b2dc` with the E2 patch. In the sanity test, `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Units: rows of `lists/W7.tsv` with row ≡ 35 (mod 36), giving 53 units (`units.tsv`). Nothing was seeded.
- 3 lanes (`lane0.sh` to `lane2.sh`, started with `setsid nohup`). Lane k ran the units at positions ≡ k (mod 3). Each unit ran `close_tree.py base.cnf out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. At END the lanes' process groups were killed. `compose.py` was not run.
- Each unit took about 14–16 minutes of wall time, so each lane fit about 16–17 units.

## Files

- `out.jsonl` holds 81 records (lanes 0, 1, 2): 49 solve records (17 certified UNSAT and 32 UNKNOWN at 900 s), plus 32 layer-split records for the timed-out units, each with 45 children. The children are unsolved and open, as intended.
- The 3 runs killed at END left no record, so no checker was killed and there is no `none` to re-check. There is no `recheck.jsonl`.
- `driver{k}.log.tail` holds the last 100 lines of each driver log.

## Solve times of the certified units

17 certified, all above 300 s. Solve time in seconds: min 695.0, Q1 764.2, median 795.9, Q3 838.7, p90 867.4, max 879.6. Check time per unit (lrat-check plus cake_lpr) was 84.5–109.9 s, 1601 s in total. Every certified record has `c VERIFIED` and `s VERIFIED UNSAT`.

## Per unit

| row | unit | parent | result | solve s | check s |
|---|---|---|---|---|---|
| 35 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | `2s0-3s0-4s0-5s1-6s0-7s0` | certified | 728.4 | 98.4 |
| 71 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | `2s0-3s0-4s1-5s0-6s0-7s0` | certified | 772.7 | 97.6 |
| 107 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | `2s0-3s0-4s1-5s1-6s0-7s1` | certified | 864.4 | 101.6 |
| 143 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | `2s0-3s1-4s0-5s0-6s0-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 179 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | `2s0-3s1-4s0-5s1-6s1-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 215 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | `2s0-3s1-4s1-5s0-6s1-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 251 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | `2s0-3s1-4s1-5s1-6s1-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 287 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | `2s1-3s0-4s0-5s0-6s1-7s1` | certified | 879.6 | 102.1 |
| 323 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | `2s1-3s0-4s1-5s0-6s0-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 359 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | `2s1-3s0-4s1-5s1-6s0-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 395 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | `2s1-3s1-4s0-5s0-6s0-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 431 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | `2s1-3s1-4s0-5s1-6s0-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 467 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | `2s1-3s1-4s1-5s0-6s1-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 503 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | `2s1-3s1-4s1-5s1-6s1-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 539 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | `1s0-3s0-4s0-5s0-6s1-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 575 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | `1s0-3s0-4s0-5s1-6s1-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 611 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | `1s0-3s0-4s1-5s1-6s0-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 647 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | `1s0-3s1-4s0-5s0-6s0-7s0` | certified | 813.2 | 108.4 |
| 683 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | `1s0-3s1-4s0-5s1-6s0-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 719 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | `1s0-3s1-4s1-5s0-6s0-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 755 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | `1s0-3s1-4s1-5s1-6s1-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 791 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | `1s1-3s0-4s0-5s0-6s1-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 827 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | `1s1-3s0-4s0-5s1-6s1-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 863 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | `1s1-3s0-4s1-5s0-6s1-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 899 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | `1s1-3s1-4s0-5s0-6s0-7s0` | certified | 856.0 | 109.9 |
| 935 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | `1s1-3s1-4s0-5s1-6s0-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 971 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | `1s1-3s1-4s1-5s0-6s0-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1007 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | `1s1-3s1-4s1-5s1-6s0-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1043 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | `1s0-2s0-4s0-5s0-6s1-7s0` | certified | 802.6 | 94.1 |
| 1079 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | `1s0-2s0-4s0-5s1-6s1-7s0` | certified | 795.9 | 92.2 |
| 1115 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | `1s0-2s0-4s1-5s0-6s1-7s1` | certified | 783.8 | 91.3 |
| 1151 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | `1s0-2s0-4s1-5s1-6s1-7s1` | certified | 746.2 | 95.3 |
| 1187 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | `1s0-2s1-4s0-5s1-6s0-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1223 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | `1s0-2s1-4s1-5s0-6s0-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1259 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | `1s0-2s1-4s1-5s1-6s0-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1295 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | `1s1-2s0-4s0-5s0-6s0-7s1` | certified | 787.7 | 84.5 |
| 1331 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | `1s1-2s0-4s0-5s1-6s1-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1367 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | `1s1-2s0-4s1-5s0-6s1-7s0` | timed out at 900 (layer split, 45 children) | 900.0 | – |
| 1403 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | `1s1-2s0-4s1-5s1-6s1-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1439 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | `1s1-2s1-4s0-5s0-6s1-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1475 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | `1s1-2s1-4s1-5s0-6s0-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1511 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | `1s1-2s1-4s1-5s1-6s0-7s0` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1547 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1-8s0-9s1-10s1` | `1s0-2s0-3s0-5s0-6s0-7s1` | certified | 821.4 | 86.4 |
| 1583 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1-8s1-9s1-10s1` | `1s0-2s0-3s0-5s1-6s0-7s1` | certified | 695.0 | 85.3 |
| 1619 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0-8s0-9s1-10s1` | `1s0-2s0-3s1-5s0-6s1-7s0` | certified | 816.0 | 87.7 |
| 1655 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0-8s1-9s1-10s1` | `1s0-2s0-3s1-5s1-6s1-7s0` | certified | 858.7 | 93.0 |
| 1691 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1-8s0-9s1-10s1` | `1s0-2s1-3s0-5s0-6s1-7s1` | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1727 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1-8s1-9s1-10s1` | `1s0-2s1-3s0-5s1-6s1-7s1` | certified | 785.5 | 87.5 |
| 1763 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0-8s0-9s1-10s1` | `1s0-2s1-3s1-5s1-6s0-7s0` | not reached | – | – |
| 1799 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s1-9s1-10s1` | `1s1-2s0-3s0-5s0-6s0-7s0` | certified | 755.8 | 85.7 |
| 1835 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1-8s0-9s1-10s1` | `1s1-2s0-3s0-5s1-6s0-7s1` | not reached | – | – |
| 1871 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s1-9s1-10s1` | `1s1-2s0-3s1-5s0-6s0-7s1` | not reached | – | – |
| 1907 | `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s0-9s1-10s1` | `1s1-2s0-3s1-5s1-6s1-7s0` | not reached | – | – |

## Totals per root

| root | units | certified | timed out | not reached |
|---|---|---|---|---|
| 0s0_1 | 14 | 4 | 10 | 0 |
| 0s0_2 | 14 | 2 | 12 | 0 |
| 0s0_3 | 14 | 5 | 9 | 0 |
| 0s0_4 | 11 | 6 | 1 | 4 |

## Totals per parent six-bit cube

| parent | units | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 0 | 1 |

Parents all of whose units on this machine were certified: `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0`, `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0`, `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1`, `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1`, `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0`, `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0`, `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0`, `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0`, `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1`, `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1`, `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1`, `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1`, `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1`, `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0`, `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0`, `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1`, `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0`


Every parent six-bit cube has exactly 1 unit on this machine, so "all certified" here means that its one unit was certified.

## Not reached

These 4 `0s0_4` units were not reached. Three were still running when they were killed at END (15:01): `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0-8s0-9s1-10s1` (started 14:49), `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1-8s0-9s1-10s1` (started 14:49) and `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s0-9s1-10s1` (started 15:00). The fourth, `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s1-9s1-10s1`, never started.

## SAT, rejections, memory

- SAT: none.
- PROOF NOT ACCEPTED: none. No certified-looking record has cake_lpr `none`.
- Memory: at most about 6 GB was in use at any time, with 3 jobs.
- Early ends: none. Every UNKNOWN ran for the full 900 s.

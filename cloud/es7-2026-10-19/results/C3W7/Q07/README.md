# C3W7 Q07: nine-bit σ-cubes of the H3/one roots, W7.tsv shard 7 of 36

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q07, LIST = W7.tsv, j = 7, N = 36, H = 4.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 10:46:34 UTC, END 15:01:34 UTC.

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e; cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity test: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Matches.

## Run

There are 53 units (`units.tsv`, the rows of W7.tsv with row ≡ 7 mod 36). No records were seeded. Three lanes ran (`lane0.sh`–`lane2.sh`). Each lane started one `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02` per unit. `out.jsonl` holds lane 0, then lane 1, then lane 2. There are 63 records: 51 solve records and 12 layer-split records.

- **No SAT. No proof rejections.** All 39 UNSAT proofs were accepted by both checkers (`c VERIFIED` and `s VERIFIED UNSAT`). No record has cake_lpr `none`, so no recheck was needed and there is no `recheck.jsonl`.
- No memory problem: peak use was about 8 GB of 15 GB, with no OOM.
- No unit ended early: every solve without a certificate ran the full 900 s.
- Lane 2 finished all its units at 14:52. At END, lanes 0 and 1 were killed during their last unit, which had started at 14:54–14:55. Those 2 units have no record and count as not reached.
- Each of the 12 timed-out units has a layer-split record (`children` 45), as intended. Their children are unsolved and stay in `open_frontier`.

## Totals

Certified: 39. Timed out at 900 s: 12. Not reached (killed at END): 2.

| root | units | certified | timed out at 900 | killed at END |
|---|---|---|---|---|
| `0s0_1` | 15 | 14 | 1 | 0 |
| `0s0_2` | 14 | 10 | 4 | 0 |
| `0s0_3` | 14 | 8 | 6 | 0 |
| `0s0_4` | 10 | 7 | 1 | 2 |

Certified solve times (n=39): min 509.6, Q1 669.9, median 753.0, Q3 848.6, p90 868.4, max 883.1 s; above 300 s: 39. Check times: min 71.1, median 101.7, max 122.1 s.

All 39 certified units took more than 300 s.

## Per parent six-bit cube

Each parent has exactly 1 unit on this machine.

| parent six-bit cube | units | certified | timed out at 900 | killed at END |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0` | 1 | 0 | 0 | 1 |

Parents all of whose units here were certified (39 of 53; each has 1 unit on this machine): `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0`, `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1`, `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1`, `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0`, `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0`, `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1`, `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1`, `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0`, `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0`, `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1`, `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1`, `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0`, `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1`, `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1`, `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0`, `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0`, `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1`, `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1`, `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0`, `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1`, `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1`, `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0`, `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1`, `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0`, `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1`, `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1`, `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0`, `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0`, `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0`, `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1`, `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1`, `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0`, `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0`, `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0`, `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1`, `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1`, `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0`, `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0`, `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1`

## Per unit

| row | unit (nine-bit cube) | lane | result | solve s | check s |
|---|---|---|---|---|---|
| 7 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | 0 | certified | 577.9 | 98.5 |
| 43 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | 1 | certified | 705.2 | 101.7 |
| 79 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | 2 | certified | 643.8 | 94.0 |
| 115 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | 0 | certified | 765.9 | 116.8 |
| 151 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | 1 | certified | 714.0 | 107.5 |
| 187 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | 2 | certified | 681.0 | 105.8 |
| 223 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | 0 | certified | 729.0 | 95.5 |
| 259 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | 1 | certified | 578.4 | 104.7 |
| 295 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | 2 | certified | 864.8 | 112.7 |
| 331 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | 0 | certified | 883.1 | 102.9 |
| 367 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | 1 | certified | 861.2 | 113.0 |
| 403 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | 2 | certified | 794.7 | 117.3 |
| 439 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 475 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | 1 | certified | 868.5 | 122.1 |
| 511 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | 2 | certified | 710.3 | 93.5 |
| 547 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | 0 | certified | 609.7 | 97.8 |
| 583 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | 1 | certified | 653.6 | 109.3 |
| 619 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | 2 | certified | 870.0 | 107.2 |
| 655 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | 0 | certified | 695.6 | 102.6 |
| 691 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 727 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | 2 | certified | 868.2 | 107.2 |
| 763 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | 0 | certified | 652.6 | 90.5 |
| 799 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | 1 | certified | 777.3 | 96.2 |
| 835 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | 2 | certified | 725.1 | 94.1 |
| 871 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 907 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | 1 | certified | 808.1 | 109.2 |
| 943 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 979 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 1015 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | 1 | certified | 753.0 | 106.7 |
| 1051 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | 2 | certified | 593.2 | 92.8 |
| 1087 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | 0 | certified | 713.4 | 92.8 |
| 1123 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | 1 | certified | 851.0 | 97.4 |
| 1159 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | 2 | certified | 756.5 | 100.2 |
| 1195 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 1231 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 1267 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 1303 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | 0 | certified | 793.3 | 94.3 |
| 1339 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | 1 | certified | 874.6 | 103.7 |
| 1375 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | 2 | certified | 868.4 | 98.4 |
| 1411 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | 0 | certified | 826.7 | 102.7 |
| 1447 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 1483 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 1519 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 1555 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0-8s0-9s1-10s1` | 1 | certified | 529.2 | 73.2 |
| 1591 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0-8s1-9s1-10s1` | 2 | certified | 509.6 | 71.1 |
| 1627 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1-8s0-9s1-10s1` | 0 | certified | 848.9 | 104.3 |
| 1663 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1-8s1-9s1-10s1` | 1 | certified | 691.4 | 99.5 |
| 1699 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0-8s0-9s1-10s1` | 2 | certified | 835.5 | 110.7 |
| 1735 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0-8s1-9s1-10s1` | 0 | certified | 848.4 | 99.7 |
| 1771 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children open) | 900.1 |  |
| 1807 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1-8s1-9s1-10s1` | 2 | certified | 658.8 | 85.6 |
| 1843 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s0-9s1-10s1` | 0 | killed at END (started 14:54-14:55, no record) |  |  |
| 1879 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0-8s1-9s1-10s1` | 1 | killed at END (started 14:54-14:55, no record) |  |  |


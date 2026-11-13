# C3W6 P23: shard 23 of 44 of W6.tsv, cap 900, one machine

Task: `results/C3W6/TASK.md` at c5260b44 with V = P23, LIST = W6.tsv, j = 23, N = 44, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 05:31:17 UTC, END 09:46:17 UTC;
lanes started 05:34:06, all three lanes ran out of units by 08:06:22 (well before END), so nothing was killed.

## Tools (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, unmodified; `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`);
  lrat-check drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 + E2 patch. Sanity check passed: on {1},{-1},
  `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).

## Run

93 units (rows ≡ 23 mod 44 of `lists/W6.tsv`, `units.tsv`), no seeded records, 3 lanes (`lane0.sh`–`lane2.sh`), each
`close_tree.py base.cnf out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
`out.jsonl` = lane 0, 1, 2 records (93 records, one per unit, no split records).

## Result

**All 93 units certified** (both checkers: `c VERIFIED` and `s VERIFIED UNSAT`) at cap 900. No timeouts, no splits,
no SAT, no proof rejection, no `none` checker result, no recheck needed (`recheck.jsonl` absent), no memory problem
(peak used about 6 GB), no unit ended early without a certificate (all units < 72 s were certified).

| stratum | units | certified |
|---|---|---|
| H3/two | 76 | 76 |
| H6(1,1)/one | 2 | 2 |
| H6(2,1)/one | 3 | 3 |
| H6(3,1)/one | 3 | 3 |
| H6(4,0)/one | 1 | 1 |
| H6(5,0)/one | 3 | 3 |
| H6(5,1)/one | 3 | 3 |
| H6(5,1)/two | 2 | 2 |
| **total** | **93** | **93** |

| prior | units | certified |
|---|---|---|
| presplit | 58 | 58 |
| timeout300 | 26 | 26 |
| never_ran | 9 | 9 |

Solve time of the certified units (s, 3 jobs on 4 cores): min 15.7, Q1 95.1, median 263.6, Q3 356.0, p90 405.6, max 542.5;
36 of 93 certified above 300 s. Total solve 21,754 s, total check 3,746 s.

## Per unit

| row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|
| 23 | `0s0_1s0-2s0__3s0-4s0-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 40.0 | 43.4 |
| 67 | `0s0_1s0-2s0__3s1-4s1-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 32.7 | 36.7 |
| 111 | `0s0_1s0-2s1__3s1-4s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 358.5 | 60.3 |
| 155 | `0s0_1s0-3s1__2s1-4s1-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 400.5 | 66.6 |
| 199 | `0s0_1s0-4s1__2s1-3s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 311.2 | 61.5 |
| 243 | `0s0_1s0-5s1__2s1-3s1-4s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 367.0 | 65.0 |
| 287 | `0s0_1s0-7s0__2s1-3s0-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 143.2 | 49.3 |
| 331 | `0s0_1s1-2s0__3s0-4s1-5s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 338.0 | 58.9 |
| 375 | `0s0_1s1-4s0__2s1-3s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 351.6 | 44.7 |
| 419 | `0s0_1s1-5s0__2s1-3s0-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 281.0 | 57.9 |
| 463 | `0s0_1s1-5s1__2s0-3s1-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 183.4 | 45.1 |
| 507 | `0s0_1s1-7s1__2s0-3s1-4s0-5s1-6s1-8s0` | H3/two | timeout300 | certified | 375.7 | 44.8 |
| 551 | `0s0_1s1-8s0__2s0-3s0-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 93.1 | 33.5 |
| 595 | `0s0_1s1-8s0__2s1-3s1-4s0-5s0-6s0-7s0` | H3/two | presplit | certified | 51.8 | 33.2 |
| 639 | `0s0_1s1-8s1__2s1-3s1-4s1-5s0-6s0-7s0` | H3/two | timeout300 | certified | 329.1 | 45.5 |
| 683 | `0s0_1s1-9s1__2s1-3s1-4s0-5s0-6s0-7s1` | H3/two | never_ran | certified | 366.8 | 62.4 |
| 727 | `0s0_2s0-3s1__1s0-4s1-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 406.8 | 48.5 |
| 771 | `0s0_2s0-4s1__1s0-3s0-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 295.7 | 44.6 |
| 815 | `0s0_2s0-4s1__1s1-3s1-5s0-6s1-7s0-8s1` | H3/two | presplit | certified | 450.9 | 50.4 |
| 859 | `0s0_2s0-5s0__1s1-3s0-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 82.4 | 31.6 |
| 903 | `0s0_2s0-5s1__1s0-3s1-4s0-6s1-7s0-8s0` | H3/two | timeout300 | certified | 414.5 | 52.5 |
| 947 | `0s0_2s0-6s1__1s0-3s0-4s0-5s0-7s0-8s1` | H3/two | timeout300 | certified | 263.6 | 47.6 |
| 991 | `0s0_2s0-6s1__1s1-3s0-4s1-5s1-7s1-8s0` | H3/two | timeout300 | certified | 301.4 | 45.2 |
| 1035 | `0s0_2s0-7s0__1s0-3s1-4s1-5s0-6s1-8s0` | H3/two | presplit | certified | 100.5 | 29.3 |
| 1079 | `0s0_2s0-7s1__1s0-3s0-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 166.1 | 34.1 |
| 1123 | `0s0_2s0-7s1__1s1-3s1-4s0-5s0-6s1-8s0` | H3/two | presplit | certified | 216.0 | 41.7 |
| 1167 | `0s0_2s0-8s0__1s1-3s1-4s0-5s0-6s0-7s0` | H3/two | presplit | certified | 199.2 | 35.5 |
| 1211 | `0s0_2s1-3s0__1s0-4s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 386.5 | 47.7 |
| 1255 | `0s0_2s1-3s1__1s0-4s0-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 64.0 | 30.1 |
| 1299 | `0s0_2s1-3s1__1s1-4s1-5s0-6s1-7s0-8s1` | H3/two | presplit | certified | 52.9 | 25.9 |
| 1343 | `0s0_2s1-4s0__1s1-3s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 400.9 | 45.8 |
| 1387 | `0s0_2s1-5s0__1s0-3s1-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 273.2 | 39.4 |
| 1431 | `0s0_2s1-5s0__1s1-3s1-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 366.9 | 51.2 |
| 1475 | `0s0_2s1-6s0__1s1-3s0-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 311.0 | 41.8 |
| 1519 | `0s0_2s1-6s1__1s0-3s1-4s0-5s1-7s1-8s1` | H3/two | presplit | certified | 182.1 | 37.3 |
| 1563 | `0s0_2s1-7s0__1s0-3s0-4s0-5s0-6s1-8s1` | H3/two | never_ran | certified | 175.4 | 33.7 |
| 1607 | `0s0_2s1-7s0__1s1-3s1-4s0-5s1-6s1-8s1` | H3/two | never_ran | certified | 322.7 | 42.1 |
| 1651 | `0s0_2s1-7s1__1s1-3s1-4s1-5s1-6s0-8s1` | H3/two | never_ran | certified | 347.9 | 39.2 |
| 1695 | `0s0_2s1-8s1__1s1-3s1-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 345.0 | 41.9 |
| 1739 | `0s0_2s1-9s0__1s0-3s1-4s1-5s1-6s1-7s0` | H3/two | presplit | certified | 85.9 | 28.8 |
| 1783 | `0s0_3s0-4s1__1s0-2s0-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 298.6 | 39.9 |
| 1827 | `0s0_3s0-4s1__1s1-2s1-5s0-6s1-7s1-8s0` | H3/two | presplit | certified | 542.5 | 50.3 |
| 1871 | `0s0_3s0-5s0__1s1-2s0-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 46.5 | 28.5 |
| 1915 | `0s0_3s0-5s1__1s0-2s1-4s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 353.5 | 42.5 |
| 1959 | `0s0_3s0-6s0__1s0-2s0-4s0-5s1-7s0-8s0` | H3/two | presplit | certified | 34.6 | 20.7 |
| 2003 | `0s0_3s0-6s0__1s1-2s1-4s0-5s0-7s0-8s0` | H3/two | presplit | certified | 98.8 | 56.1 |
| 2047 | `0s0_3s0-6s1__1s0-2s1-4s1-5s1-7s0-8s0` | H3/two | timeout300 | certified | 453.7 | 49.0 |
| 2091 | `0s0_3s0-7s0__1s0-2s0-4s1-5s0-6s0-8s0` | H3/two | presplit | certified | 68.1 | 29.6 |
| 2135 | `0s0_3s0-7s0__1s1-2s1-4s0-5s1-6s0-8s0` | H3/two | presplit | certified | 138.1 | 34.6 |
| 2179 | `0s0_3s0-7s1__1s1-2s0-4s0-5s0-6s0-8s0` | H3/two | presplit | certified | 276.7 | 61.9 |
| 2223 | `0s0_3s0-8s0__1s1-2s0-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 135.5 | 33.3 |
| 2267 | `0s0_3s0-8s1__1s1-2s0-4s1-5s1-6s0-7s1` | H3/two | timeout300 | certified | 293.3 | 36.7 |
| 2311 | `0s0_3s1-4s0__1s0-2s1-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 413.2 | 45.5 |
| 2355 | `0s0_3s1-4s1__1s0-2s0-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 121.5 | 51.0 |
| 2399 | `0s0_3s1-4s1__1s1-2s1-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 59.2 | 24.9 |
| 2443 | `0s0_3s1-5s0__1s1-2s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 375.7 | 42.6 |
| 2487 | `0s0_3s1-5s1__1s0-2s0-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 114.0 | 34.8 |
| 2531 | `0s0_3s1-5s1__1s1-2s1-4s1-6s0-7s1-8s1` | H3/two | presplit | certified | 71.2 | 25.4 |
| 2575 | `0s0_3s1-7s0__1s1-2s1-4s0-5s1-6s0-8s1` | H3/two | never_ran | certified | 358.6 | 41.6 |
| 2619 | `0s0_3s1-8s0__1s0-2s0-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 123.3 | 29.6 |
| 2663 | `0s0_3s1-8s0__1s1-2s1-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 208.4 | 34.1 |
| 2707 | `0s0_4s0-5s1__1s1-2s0-3s0-6s0-7s0-8s0` | H3/two | presplit | certified | 250.9 | 43.5 |
| 2751 | `0s0_4s0-6s1__1s0-2s0-3s1-5s1-7s0-8s0` | H3/two | presplit | certified | 410.8 | 48.6 |
| 2795 | `0s0_4s0-6s1__1s1-2s1-3s1-5s0-7s0-8s0` | H3/two | presplit | certified | 329.6 | 41.9 |
| 2839 | `0s0_4s0-7s0__1s1-2s0-3s0-5s1-6s0-8s0` | H3/two | presplit | certified | 40.9 | 20.6 |
| 2883 | `0s0_4s0-7s1__1s0-2s1-3s1-5s0-6s0-8s1` | H3/two | presplit | certified | 417.5 | 47.6 |
| 2927 | `0s0_4s1-5s0__1s0-2s0-3s0-6s1-7s0-8s1` | H3/two | never_ran | certified | 272.6 | 54.3 |
| 2971 | `0s0_4s1-5s0__1s1-2s1-3s0-6s0-7s0-8s1` | H3/two | never_ran | certified | 410.7 | 45.7 |
| 3015 | `0s0_4s1-6s0__1s0-2s1-3s0-5s1-7s0-8s0` | H3/two | presplit | certified | 392.7 | 45.7 |
| 3059 | `0s0_4s1-6s1__1s0-2s0-3s0-5s0-7s0-8s0` | H3/two | presplit | certified | 95.8 | 29.2 |
| 3103 | `0s0_4s1-6s1__1s1-2s0-3s1-5s1-7s0-8s0` | H3/two | presplit | certified | 94.3 | 31.4 |
| 3147 | `0s0_4s1-7s0__1s0-2s1-3s1-5s0-6s0-8s0` | H3/two | presplit | certified | 314.0 | 39.7 |
| 3191 | `0s0_5s0-6s0__1s0-2s0-3s0-4s1-7s0-8s0` | H3/two | presplit | certified | 15.7 | 15.1 |
| 3235 | `0s0_5s0-6s0__1s1-2s1-3s0-4s0-7s0-8s0` | H3/two | presplit | certified | 17.7 | 15.2 |
| 3279 | `0s0_5s0-6s1__1s0-2s1-3s1-4s1-7s0-8s0` | H3/two | presplit | certified | 394.6 | 42.7 |
| 3323 | `0s0_5s1-6s0__1s1-2s0-3s1-4s0-7s1-8s1` | H3/two | timeout300 | certified | 403.8 | 45.8 |
| 3367 | `0s0-1s1_5__2s0-3s0-4s1-6s0-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 267.9 | 38.1 |
| 3411 | `0s0-1s1_5__2s1-3s1-4s1-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 216.5 | 36.4 |
| 3455 | `0s0-2s1_4__1s1-3s1-5s1-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 390.5 | 40.9 |
| 3499 | `0s0-2s1_5__1s1-3s1-4s0-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 290.9 | 43.1 |
| 3543 | `0s0-2s1_6__1s1-3s0-4s0-5s0-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 298.1 | 41.7 |
| 3587 | `0s0-3s1_4__1s1-2s0-5s0-6s1-7s0-8s0` | H6(3,1)/one | timeout300 | certified | 303.4 | 40.5 |
| 3631 | `0s0-3s1_5__1s0-2s1-4s0-6s0-7s1-8s0` | H6(3,1)/one | presplit | certified | 202.1 | 39.2 |
| 3675 | `0s0-3s1_5__1s1-2s1-4s1-6s1-7s1-8s0` | H6(3,1)/one | presplit | certified | 252.0 | 35.0 |
| 3719 | `0s0-4s0_6__1s1-2s0-3s1-5s0-7s1-8s0` | H6(4,0)/one | presplit | certified | 54.6 | 28.8 |
| 3763 | `0s0-5s0_6__1s0-2s1-3s0-4s0-7s0-8s1` | H6(5,0)/one | presplit | certified | 55.3 | 26.9 |
| 3807 | `0s0-5s0_6__1s1-2s1-3s1-4s1-7s0-8s1` | H6(5,0)/one | presplit | certified | 74.0 | 28.9 |
| 3851 | `0s0-5s0_7__1s1-2s0-3s1-4s0-6s0-8s1` | H6(5,0)/one | presplit | certified | 53.6 | 28.0 |
| 3895 | `0s0-5s1_1__2s1-3s0-4s0-6s0-7s1-8s1` | H6(5,1)/one | presplit | certified | 176.4 | 35.1 |
| 3939 | `0s0-5s1_2__1s0-3s0-4s1-6s1-7s1-8s1` | H6(5,1)/one | presplit | certified | 155.7 | 35.4 |
| 3983 | `0s0-5s1_2__1s1-3s1-4s1-6s0-7s1-8s1` | H6(5,1)/one | presplit | certified | 197.3 | 35.8 |
| 4027 | `0s0-5s1_1s1-10s1__2s0-3s0-4s1-6s1-7s1-8s0` | H6(5,1)/two | never_ran | certified | 40.0 | 29.0 |
| 4071 | `0s0-5s1_1s1-10s1__2s1-3s1-4s1-6s0-7s1-8s0` | H6(5,1)/two | never_ran | certified | 43.5 | 28.9 |

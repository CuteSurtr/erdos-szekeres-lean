# C3W6 P15: shard 15 of 44 of W6.tsv at cap 900

Task: `results/C3W6/TASK.md` at c5260b44, with V = P15, LIST = W6.tsv, j = 15, N = 44, H = 4.5.
Machine: one cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:13 UTC, END 09:46:13 UTC. The lanes started at 05:34:07 and all three finished their units early, by 07:45:58 UTC.

## Tools (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042. cake_lpr a36874a8: its example prints `s VERIFIED UNSAT`. lrat-check 2e3b2dc with the E2 patch. Sanity test: `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).

## Run

- Units: the rows of W6.tsv with row % 44 == 15, which gives 94 units (`units.tsv`). No records were seeded.
- 3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`); lane k runs the positions ≡ k (mod 3). Each unit ran `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds 94 records: lane 0 (32), then lane 1 (31), then lane 2 (31). There are no split records and no `recheck.jsonl`.

## Result

**All 94 units were certified in their single solve at cap 900.** Both checkers accepted every one: lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. Every unit has open_frontier 0.
- No unit timed out and none went unreached.
- No SAT, no proof rejection, no cake_lpr `none`, no memory problem, and no unit ended early without a certificate.
- The largest proof was 564 MB. Proofs were not committed.

| stratum | units | certified |
|---|---|---|
| H3/two | 76 | 76 |
| H6(1,1)/one | 2 | 2 |
| H6(2,1)/one | 3 | 3 |
| H6(3,1)/one | 3 | 3 |
| H6(4,0)/one | 1 | 1 |
| H6(5,0)/one | 3 | 3 |
| H6(5,1)/one | 3 | 3 |
| H6(5,1)/two | 3 | 3 |

| prior | units | certified |
|---|---|---|
| presplit | 59 | 59 |
| timeout300 | 28 | 28 |
| never_ran | 7 | 7 |

Solve seconds over the 94 certified units: min 16.1, Q1 81.3, median 209.5, Q3 272.8, p90 329.5, max 368.9 (sum 17,978 s).
- 17 units were certified above 300 s, and none above 600 s.
- 21 units solved in under 72 s, all of them certified.

Check seconds: min 20.1, median 43.5, max 67.6 (sum 4,144 s).

## Per unit

| row | node | stratum | prior | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 15 | `0s0_1s0-2s0__3s0-4s0-5s0-6s0-7s1-8s0` | H3/two | presplit | 0 | certified | 38.8 | 39.8 |
| 59 | `0s0_1s0-2s0__3s1-4s0-5s1-6s1-7s1-8s0` | H3/two | presplit | 1 | certified | 24.0 | 35.7 |
| 103 | `0s0_1s0-2s1__3s1-4s0-5s0-6s0-7s0-8s1` | H3/two | timeout300 | 2 | certified | 251.6 | 60.7 |
| 147 | `0s0_1s0-3s1__2s1-4s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 340.9 | 65.5 |
| 191 | `0s0_1s0-4s1__2s1-3s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 285.8 | 64.3 |
| 235 | `0s0_1s0-5s1__2s1-3s1-4s0-6s0-7s0-8s1` | H3/two | timeout300 | 2 | certified | 292.5 | 63.4 |
| 279 | `0s0_1s0-7s0__2s1-3s0-4s0-5s1-6s1-8s1` | H3/two | timeout300 | 0 | certified | 148.9 | 54.0 |
| 323 | `0s0_1s1-2s0__3s0-4s1-5s0-6s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 268.7 | 49.6 |
| 367 | `0s0_1s1-4s0__2s0-3s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | 2 | certified | 266.4 | 51.9 |
| 411 | `0s0_1s1-5s0__2s1-3s0-4s0-6s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 199.9 | 51.3 |
| 455 | `0s0_1s1-5s1__2s0-3s1-4s0-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 105.1 | 42.1 |
| 499 | `0s0_1s1-6s1__2s1-3s1-4s1-5s1-7s0-8s1` | H3/two | timeout300 | 2 | certified | 298.1 | 67.6 |
| 543 | `0s0_1s1-7s1__2s1-3s1-4s1-5s1-6s0-8s0` | H3/two | timeout300 | 0 | certified | 322.7 | 57.7 |
| 587 | `0s0_1s1-8s0__2s1-3s0-4s1-5s0-6s0-7s0` | H3/two | presplit | 1 | certified | 61.8 | 44.8 |
| 631 | `0s0_1s1-8s1__2s1-3s0-4s1-5s1-6s1-7s1` | H3/two | timeout300 | 2 | certified | 368.9 | 52.2 |
| 675 | `0s0_1s1-9s1__2s1-3s0-4s1-5s0-6s0-7s1` | H3/two | never_ran | 0 | certified | 332.4 | 48.9 |
| 719 | `0s0_2s0-3s1__1s0-4s1-5s0-6s1-7s0-8s1` | H3/two | presplit | 1 | certified | 314.9 | 58.6 |
| 763 | `0s0_2s0-4s1__1s0-3s0-5s0-6s0-7s0-8s1` | H3/two | presplit | 2 | certified | 209.0 | 43.7 |
| 807 | `0s0_2s0-4s1__1s1-3s0-5s1-6s1-7s0-8s1` | H3/two | presplit | 0 | certified | 358.3 | 50.6 |
| 851 | `0s0_2s0-5s0__1s0-3s1-4s1-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 49.8 | 29.7 |
| 895 | `0s0_2s0-5s1__1s0-3s0-4s1-6s1-7s0-8s0` | H3/two | timeout300 | 2 | certified | 246.1 | 45.9 |
| 939 | `0s0_2s0-5s1__1s1-3s1-4s1-6s0-7s0-8s0` | H3/two | timeout300 | 0 | certified | 258.3 | 46.3 |
| 983 | `0s0_2s0-6s1__1s1-3s0-4s0-5s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 256.9 | 42.7 |
| 1027 | `0s0_2s0-7s0__1s0-3s1-4s0-5s0-6s1-8s0` | H3/two | presplit | 2 | certified | 80.2 | 41.7 |
| 1071 | `0s0_2s0-7s0__1s1-3s1-4s1-5s1-6s1-8s0` | H3/two | presplit | 0 | certified | 114.8 | 46.0 |
| 1115 | `0s0_2s0-7s1__1s1-3s0-4s1-5s0-6s1-8s0` | H3/two | presplit | 1 | certified | 175.5 | 41.2 |
| 1159 | `0s0_2s0-8s0__1s1-3s0-4s1-5s0-6s0-7s0` | H3/two | presplit | 2 | certified | 138.6 | 38.9 |
| 1203 | `0s0_2s1-3s0__1s0-4s1-5s0-6s1-7s0-8s1` | H3/two | timeout300 | 0 | certified | 277.9 | 45.6 |
| 1247 | `0s0_2s1-3s1__1s0-4s0-5s0-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 61.8 | 32.1 |
| 1291 | `0s0_2s1-3s1__1s1-4s0-5s1-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 46.4 | 30.2 |
| 1335 | `0s0_2s1-4s0__1s0-3s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 318.9 | 45.6 |
| 1379 | `0s0_2s1-5s0__1s0-3s0-4s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 248.4 | 52.9 |
| 1423 | `0s0_2s1-5s0__1s1-3s1-4s0-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 234.2 | 39.5 |
| 1467 | `0s0_2s1-6s0__1s1-3s0-4s0-5s0-7s1-8s1` | H3/two | presplit | 0 | certified | 210.9 | 38.8 |
| 1511 | `0s0_2s1-6s1__1s0-3s0-4s1-5s1-7s1-8s1` | H3/two | presplit | 1 | certified | 165.4 | 39.4 |
| 1555 | `0s0_2s1-6s1__1s1-3s1-4s1-5s0-7s1-8s1` | H3/two | presplit | 2 | certified | 152.3 | 38.8 |
| 1599 | `0s0_2s1-7s0__1s1-3s0-4s1-5s1-6s1-8s1` | H3/two | never_ran | 0 | certified | 290.5 | 59.2 |
| 1643 | `0s0_2s1-7s1__1s1-3s1-4s0-5s1-6s0-8s1` | H3/two | never_ran | 1 | certified | 214.8 | 41.8 |
| 1687 | `0s0_2s1-8s1__1s1-3s0-4s1-5s0-6s1-7s0` | H3/two | presplit | 2 | certified | 222.2 | 59.0 |
| 1731 | `0s0_2s1-9s0__1s0-3s1-4s0-5s1-6s1-7s0` | H3/two | presplit | 0 | certified | 72.2 | 28.6 |
| 1775 | `0s0_3s0-4s1__1s0-2s0-5s0-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 213.6 | 41.4 |
| 1819 | `0s0_3s0-4s1__1s1-2s0-5s1-6s1-7s1-8s0` | H3/two | presplit | 2 | certified | 341.3 | 48.5 |
| 1863 | `0s0_3s0-5s0__1s0-2s1-4s1-6s0-7s1-8s0` | H3/two | presplit | 0 | certified | 43.3 | 33.1 |
| 1907 | `0s0_3s0-5s1__1s0-2s0-4s1-6s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 310.5 | 50.2 |
| 1951 | `0s0_3s0-5s1__1s1-2s1-4s1-6s1-7s0-8s0` | H3/two | timeout300 | 2 | certified | 363.2 | 52.9 |
| 1995 | `0s0_3s0-6s0__1s1-2s0-4s1-5s0-7s0-8s0` | H3/two | presplit | 0 | certified | 47.9 | 29.1 |
| 2039 | `0s0_3s0-6s1__1s0-2s1-4s0-5s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 248.0 | 40.9 |
| 2083 | `0s0_3s0-7s0__1s0-2s0-4s0-5s0-6s0-8s0` | H3/two | presplit | 2 | certified | 48.1 | 32.5 |
| 2127 | `0s0_3s0-7s0__1s1-2s0-4s1-5s1-6s0-8s0` | H3/two | presplit | 0 | certified | 57.6 | 32.0 |
| 2171 | `0s0_3s0-7s1__1s0-2s1-4s1-5s0-6s0-8s0` | H3/two | presplit | 1 | certified | 256.2 | 47.4 |
| 2215 | `0s0_3s0-8s0__1s0-2s1-4s1-5s0-6s1-7s0` | H3/two | presplit | 2 | certified | 118.0 | 32.9 |
| 2259 | `0s0_3s0-8s1__1s0-2s1-4s1-5s0-6s1-7s0` | H3/two | timeout300 | 0 | certified | 254.4 | 50.1 |
| 2303 | `0s0_3s1-4s0__1s0-2s1-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 358.6 | 52.0 |
| 2347 | `0s0_3s1-4s1__1s0-2s0-5s0-6s0-7s1-8s1` | H3/two | presplit | 2 | certified | 67.9 | 33.0 |
| 2391 | `0s0_3s1-4s1__1s1-2s0-5s1-6s1-7s1-8s1` | H3/two | presplit | 0 | certified | 53.8 | 37.9 |
| 2435 | `0s0_3s1-5s0__1s0-2s1-4s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 333.1 | 48.4 |
| 2479 | `0s0_3s1-5s1__1s0-2s0-4s0-6s1-7s1-8s1` | H3/two | presplit | 2 | certified | 84.5 | 31.2 |
| 2523 | `0s0_3s1-5s1__1s1-2s1-4s0-6s0-7s1-8s1` | H3/two | presplit | 0 | certified | 65.4 | 46.4 |
| 2567 | `0s0_3s1-7s0__1s1-2s0-4s1-5s1-6s0-8s1` | H3/two | never_ran | 1 | certified | 221.5 | 43.0 |
| 2611 | `0s0_3s1-8s0__1s0-2s0-4s0-5s0-6s0-7s0` | H3/two | presplit | 2 | certified | 91.7 | 44.9 |
| 2655 | `0s0_3s1-8s0__1s1-2s0-4s1-5s1-6s0-7s0` | H3/two | presplit | 0 | certified | 131.3 | 36.6 |
| 2699 | `0s0_4s0-5s1__1s0-2s1-3s1-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 274.2 | 42.5 |
| 2743 | `0s0_4s0-6s1__1s0-2s0-3s0-5s1-7s0-8s0` | H3/two | presplit | 2 | certified | 210.0 | 58.9 |
| 2787 | `0s0_4s0-6s1__1s1-2s1-3s0-5s0-7s0-8s0` | H3/two | presplit | 0 | certified | 260.6 | 43.3 |
| 2831 | `0s0_4s0-7s0__1s0-2s1-3s1-5s1-6s0-8s0` | H3/two | presplit | 1 | certified | 53.1 | 30.9 |
| 2875 | `0s0_4s0-7s1__1s0-2s1-3s0-5s0-6s0-8s1` | H3/two | presplit | 2 | certified | 249.3 | 60.7 |
| 2919 | `0s0_4s0-7s1__1s1-2s1-3s1-5s1-6s0-8s1` | H3/two | presplit | 0 | certified | 346.1 | 46.1 |
| 2963 | `0s0_4s1-5s0__1s1-2s0-3s1-6s0-7s0-8s1` | H3/two | never_ran | 1 | certified | 300.6 | 50.7 |
| 3007 | `0s0_4s1-6s0__1s0-2s0-3s1-5s1-7s0-8s0` | H3/two | presplit | 2 | certified | 265.8 | 51.6 |
| 3051 | `0s0_4s1-6s0__1s1-2s1-3s1-5s0-7s0-8s0` | H3/two | presplit | 0 | certified | 318.6 | 59.1 |
| 3095 | `0s0_4s1-6s1__1s1-2s0-3s0-5s1-7s0-8s0` | H3/two | presplit | 1 | certified | 74.8 | 41.1 |
| 3139 | `0s0_4s1-7s0__1s0-2s1-3s0-5s0-6s0-8s0` | H3/two | presplit | 2 | certified | 190.3 | 55.8 |
| 3183 | `0s0_4s1-7s0__1s1-2s1-3s1-5s1-6s0-8s0` | H3/two | presplit | 0 | certified | 319.4 | 59.7 |
| 3227 | `0s0_5s0-6s0__1s1-2s0-3s1-4s0-7s0-8s0` | H3/two | presplit | 1 | certified | 16.1 | 20.1 |
| 3271 | `0s0_5s0-6s1__1s0-2s1-3s0-4s1-7s0-8s0` | H3/two | presplit | 2 | certified | 289.0 | 45.7 |
| 3315 | `0s0_5s1-6s0__1s0-2s1-3s1-4s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 336.3 | 49.2 |
| 3359 | `0s0-1s1_5__2s0-3s0-4s0-6s0-7s1-8s1` | H6(1,1)/one | timeout300 | 1 | certified | 140.2 | 37.2 |
| 3403 | `0s0-1s1_5__2s1-3s1-4s0-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | 2 | certified | 168.4 | 39.6 |
| 3447 | `0s0-2s1_4__1s1-3s1-5s0-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | 0 | certified | 261.5 | 47.2 |
| 3491 | `0s0-2s1_5__1s1-3s0-4s1-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | 1 | certified | 243.8 | 44.7 |
| 3535 | `0s0-2s1_6__1s0-3s1-4s1-5s0-7s1-8s0` | H6(2,1)/one | timeout300 | 2 | certified | 189.7 | 44.5 |
| 3579 | `0s0-3s1_4__1s0-2s1-5s0-6s1-7s1-8s0` | H6(3,1)/one | timeout300 | 0 | certified | 255.2 | 64.6 |
| 3623 | `0s0-3s1_5__1s0-2s0-4s1-6s0-7s1-8s0` | H6(3,1)/one | presplit | 1 | certified | 182.3 | 39.4 |
| 3667 | `0s0-3s1_5__1s1-2s1-4s0-6s1-7s1-8s0` | H6(3,1)/one | presplit | 2 | certified | 204.6 | 38.5 |
| 3711 | `0s0-4s0_6__1s1-2s0-3s0-5s0-7s1-8s0` | H6(4,0)/one | presplit | 0 | certified | 31.8 | 24.0 |
| 3755 | `0s0-5s0_6__1s0-2s0-3s1-4s0-7s0-8s1` | H6(5,0)/one | presplit | 1 | certified | 47.7 | 38.4 |
| 3799 | `0s0-5s0_6__1s1-2s1-3s0-4s1-7s0-8s1` | H6(5,0)/one | presplit | 2 | certified | 50.4 | 31.3 |
| 3843 | `0s0-5s0_7__1s1-2s0-3s0-4s0-6s0-8s1` | H6(5,0)/one | presplit | 0 | certified | 59.2 | 28.2 |
| 3887 | `0s0-5s1_1__2s0-3s1-4s1-6s0-7s1-8s1` | H6(5,1)/one | presplit | 1 | certified | 101.7 | 33.0 |
| 3931 | `0s0-5s1_2__1s0-3s0-4s0-6s1-7s1-8s1` | H6(5,1)/one | presplit | 2 | certified | 131.9 | 35.0 |
| 3975 | `0s0-5s1_2__1s1-3s1-4s0-6s0-7s1-8s1` | H6(5,1)/one | presplit | 0 | certified | 147.8 | 39.6 |
| 4019 | `0s0-5s1_1s1-10s1__2s0-3s0-4s0-6s1-7s1-8s0` | H6(5,1)/two | never_ran | 1 | certified | 27.8 | 23.3 |
| 4063 | `0s0-5s1_1s1-10s1__2s1-3s1-4s0-6s0-7s1-8s0` | H6(5,1)/two | never_ran | 2 | certified | 39.7 | 33.5 |
| 4107 | `0s0-5s1_7s0-9s1__1s1-2s1-3s0` | H6(5,1)/two | presplit | 0 | certified | 155.8 | 35.5 |

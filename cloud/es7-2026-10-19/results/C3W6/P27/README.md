# C3W6 / P27: shard 27 of 44 of W6.tsv, cap 900, one machine

**Result: all 93 units were certified at the 900 s cap: 0 timed out, 0 not reached. No SAT. No proof rejection.** Each unit is a six-bit σ-cube; there are no 3-bit cubes in this shard.

## Setup

- One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:11 UTC on 2026-10-25, END 09:46:11 UTC. All three lanes had finished by 07:48:08 UTC.
- Tools (`tools.txt`): C3U2 tools from a worktree of cad4e050 at `/opt/c3u2`, used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch.
  - Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers; `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Units: the rows of `lists/W6.tsv` with row ≡ 27 (mod 44), giving 93 units (`units.tsv`). No records were seeded.
- Lanes: 3 lanes (`lane0.sh`–`lane2.sh`), each running `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`. Lane k ran positions ≡ k (mod 3).
- `out.jsonl` holds 93 records, one per unit (lanes 0, 1, 2 in that order). There are no split records, because no unit timed out. `compose.py` was not run.

## Totals

| stratum | units | certified | timed out at 900 | not reached | median solve s | max solve s | certified above 300 s |
|---|---|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 230 | 476 | 27 |
| H6(1,1)/one | 1 | 1 | 0 | 0 | 183 | 183 | 0 |
| H6(2,1)/one | 4 | 4 | 0 | 0 | 262 | 277 | 0 |
| H6(3,1)/one | 2 | 2 | 0 | 0 | 235 | 261 | 0 |
| H6(4,0)/one | 2 | 2 | 0 | 0 | 66 | 87 | 0 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 51 | 56 | 0 |
| H6(5,1)/one | 3 | 3 | 0 | 0 | 179 | 195 | 0 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 31 | 36 | 0 |

| prior | units | certified | median solve s | max solve s | certified above 300 s |
|---|---|---|---|---|---|
| timeout300 | 24 | 24 | 339 | 476 | 14 |
| presplit | 59 | 59 | 127 | 449 | 11 |
| never_ran | 10 | 10 | 258 | 446 | 2 |

Solve times of the 93 certified units, in seconds: min 12.6, Q1 83.2, median 217.9, Q3 315.1, p90 402.7, max 476.0, sum 19,964. **27 were certified above 300 s**, all of them H3/two.

Check times: 14.9–64.7 s per unit (median 40.3, sum 3,729). Every record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

20 units were solved in under 72 s, and all 20 were certified. No unit ended early without a certificate.

## SAT, rejections, memory

- SAT: none.
- PROOF NOT ACCEPTED: none, and no cake_lpr `none`. No recheck was needed, so there is no `recheck.jsonl`.
- Memory: peak use was about 10 GB of 15 GB with 3 lanes. There was no memory problem.
- Incident (affected neither the run nor the results): for about 10 minutes around 06:15 UTC, the session's command-safety check failed. The lanes kept running, and one progress push came late (06:25 instead of about 06:27–06:28 due, so within 25 min of the 06:03 push anyway).

## Per unit

| pos | row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0 | 27 | `0s0_1s0-2s0__3s0-4s0-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 29.4 | 36.3 |
| 1 | 71 | `0s0_1s0-2s0__3s1-4s1-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 48.5 | 32.0 |
| 2 | 115 | `0s0_1s0-2s1__3s1-4s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 403.4 | 63.7 |
| 3 | 159 | `0s0_1s0-3s1__2s1-4s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 444.3 | 64.7 |
| 4 | 203 | `0s0_1s0-4s1__2s1-3s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 412.7 | 60.2 |
| 5 | 247 | `0s0_1s0-5s1__2s1-3s1-4s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 364.0 | 49.2 |
| 6 | 291 | `0s0_1s0-7s0__2s1-3s1-4s0-5s0-6s1-8s1` | H3/two | timeout300 | certified | 217.9 | 51.2 |
| 7 | 335 | `0s0_1s1-2s0__3s1-4s0-5s0-6s0-7s0-8s0` | H3/two | timeout300 | certified | 297.5 | 58.0 |
| 8 | 379 | `0s0_1s1-4s0__2s1-3s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 423.6 | 60.9 |
| 9 | 423 | `0s0_1s1-5s0__2s1-3s1-4s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 279.2 | 56.0 |
| 10 | 467 | `0s0_1s1-5s1__2s1-3s0-4s0-6s0-7s0-8s0` | H3/two | presplit | certified | 134.5 | 43.9 |
| 11 | 511 | `0s0_1s1-7s1__2s0-3s1-4s1-5s0-6s1-8s0` | H3/two | timeout300 | certified | 378.3 | 52.7 |
| 12 | 555 | `0s0_1s1-8s0__2s0-3s0-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 68.7 | 41.3 |
| 13 | 599 | `0s0_1s1-8s0__2s1-3s1-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 82.4 | 31.8 |
| 14 | 643 | `0s0_1s1-8s1__2s1-3s1-4s1-5s1-6s0-7s0` | H3/two | timeout300 | certified | 338.1 | 51.1 |
| 15 | 687 | `0s0_1s1-9s1__2s1-3s1-4s0-5s1-6s0-7s1` | H3/two | never_ran | certified | 445.9 | 52.4 |
| 16 | 731 | `0s0_2s0-3s1__1s1-4s0-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 371.9 | 54.7 |
| 17 | 775 | `0s0_2s0-4s1__1s0-3s0-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 343.1 | 52.5 |
| 18 | 819 | `0s0_2s0-4s1__1s1-3s1-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 432.6 | 53.5 |
| 19 | 863 | `0s0_2s0-5s0__1s1-3s0-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 83.9 | 38.4 |
| 20 | 907 | `0s0_2s0-5s1__1s0-3s1-4s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 311.9 | 45.4 |
| 21 | 951 | `0s0_2s0-6s1__1s0-3s0-4s0-5s1-7s0-8s1` | H3/two | timeout300 | certified | 256.3 | 57.6 |
| 22 | 995 | `0s0_2s0-6s1__1s1-3s1-4s0-5s0-7s1-8s0` | H3/two | timeout300 | certified | 349.4 | 51.6 |
| 23 | 1039 | `0s0_2s0-7s0__1s0-3s1-4s1-5s1-6s1-8s0` | H3/two | presplit | certified | 92.0 | 27.9 |
| 24 | 1083 | `0s0_2s0-7s1__1s0-3s0-4s1-5s0-6s1-8s0` | H3/two | presplit | certified | 205.1 | 41.8 |
| 25 | 1127 | `0s0_2s0-7s1__1s1-3s1-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 218.0 | 40.6 |
| 26 | 1171 | `0s0_2s0-8s0__1s1-3s1-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 171.4 | 51.9 |
| 27 | 1215 | `0s0_2s1-3s0__1s1-4s0-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 349.1 | 45.8 |
| 28 | 1259 | `0s0_2s1-3s1__1s0-4s0-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 69.8 | 34.3 |
| 29 | 1303 | `0s0_2s1-3s1__1s1-4s1-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 43.0 | 23.1 |
| 30 | 1347 | `0s0_2s1-4s0__1s1-3s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 476.0 | 48.5 |
| 31 | 1391 | `0s0_2s1-5s0__1s0-3s1-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 194.1 | 35.4 |
| 32 | 1435 | `0s0_2s1-6s0__1s0-3s0-4s0-5s0-7s1-8s1` | H3/two | presplit | certified | 170.2 | 34.1 |
| 33 | 1479 | `0s0_2s1-6s0__1s1-3s0-4s1-5s1-7s1-8s1` | H3/two | presplit | certified | 315.1 | 43.6 |
| 34 | 1523 | `0s0_2s1-6s1__1s0-3s1-4s1-5s0-7s1-8s1` | H3/two | presplit | certified | 197.1 | 33.6 |
| 35 | 1567 | `0s0_2s1-7s0__1s0-3s0-4s0-5s1-6s1-8s1` | H3/two | never_ran | certified | 199.8 | 34.6 |
| 36 | 1611 | `0s0_2s1-7s0__1s1-3s1-4s1-5s0-6s1-8s1` | H3/two | never_ran | certified | 225.1 | 38.8 |
| 37 | 1655 | `0s0_2s1-8s1__1s0-3s0-4s1-5s0-6s1-7s0` | H3/two | presplit | certified | 248.9 | 44.7 |
| 38 | 1699 | `0s0_2s1-8s1__1s1-3s1-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 355.0 | 44.1 |
| 39 | 1743 | `0s0_2s1-9s0__1s1-3s0-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 103.0 | 31.5 |
| 40 | 1787 | `0s0_3s0-4s1__1s0-2s0-5s1-6s1-7s1-8s0` | H3/two | presplit | certified | 344.9 | 43.4 |
| 41 | 1831 | `0s0_3s0-4s1__1s1-2s1-5s1-6s0-7s1-8s0` | H3/two | presplit | certified | 418.4 | 45.5 |
| 42 | 1875 | `0s0_3s0-5s0__1s1-2s0-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 44.8 | 23.1 |
| 43 | 1919 | `0s0_3s0-5s1__1s0-2s1-4s1-6s1-7s0-8s0` | H3/two | timeout300 | certified | 376.9 | 46.5 |
| 44 | 1963 | `0s0_3s0-6s0__1s0-2s0-4s1-5s0-7s0-8s0` | H3/two | presplit | certified | 29.1 | 19.5 |
| 45 | 2007 | `0s0_3s0-6s0__1s1-2s1-4s0-5s1-7s0-8s0` | H3/two | presplit | certified | 75.6 | 27.0 |
| 46 | 2051 | `0s0_3s0-6s1__1s1-2s0-4s0-5s0-7s0-8s0` | H3/two | timeout300 | certified | 205.9 | 32.3 |
| 47 | 2095 | `0s0_3s0-7s0__1s0-2s0-4s1-5s1-6s0-8s0` | H3/two | presplit | certified | 46.8 | 25.5 |
| 48 | 2139 | `0s0_3s0-7s0__1s1-2s1-4s1-5s0-6s0-8s0` | H3/two | presplit | certified | 101.2 | 32.2 |
| 49 | 2183 | `0s0_3s0-7s1__1s1-2s0-4s0-5s1-6s0-8s0` | H3/two | presplit | certified | 251.1 | 38.8 |
| 50 | 2227 | `0s0_3s0-8s0__1s1-2s0-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 102.0 | 29.9 |
| 51 | 2271 | `0s0_3s0-8s1__1s1-2s1-4s0-5s1-6s0-7s1` | H3/two | never_ran | certified | 293.8 | 40.1 |
| 52 | 2315 | `0s0_3s1-4s0__1s1-2s0-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 339.2 | 42.9 |
| 53 | 2359 | `0s0_3s1-4s1__1s0-2s0-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 83.2 | 30.4 |
| 54 | 2403 | `0s0_3s1-4s1__1s1-2s1-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 52.1 | 28.5 |
| 55 | 2447 | `0s0_3s1-5s0__1s1-2s0-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 341.9 | 42.4 |
| 56 | 2491 | `0s0_3s1-5s1__1s0-2s1-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 65.6 | 28.9 |
| 57 | 2535 | `0s0_3s1-5s1__1s1-2s1-4s1-6s1-7s1-8s1` | H3/two | presplit | certified | 52.6 | 25.5 |
| 58 | 2579 | `0s0_3s1-7s0__1s1-2s1-4s1-5s0-6s0-8s1` | H3/two | never_ran | certified | 255.8 | 40.8 |
| 59 | 2623 | `0s0_3s1-8s0__1s0-2s0-4s1-5s1-6s0-7s0` | H3/two | presplit | certified | 94.3 | 42.3 |
| 60 | 2667 | `0s0_3s1-8s0__1s1-2s1-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 156.1 | 32.8 |
| 61 | 2711 | `0s0_4s0-5s1__1s1-2s0-3s0-6s1-7s0-8s0` | H3/two | presplit | certified | 278.1 | 42.6 |
| 62 | 2755 | `0s0_4s0-6s1__1s0-2s1-3s0-5s0-7s0-8s0` | H3/two | presplit | certified | 234.5 | 44.9 |
| 63 | 2799 | `0s0_4s0-6s1__1s1-2s1-3s1-5s1-7s0-8s0` | H3/two | presplit | certified | 312.7 | 40.8 |
| 64 | 2843 | `0s0_4s0-7s0__1s1-2s0-3s1-5s0-6s0-8s0` | H3/two | presplit | certified | 65.9 | 30.3 |
| 65 | 2887 | `0s0_4s0-7s1__1s0-2s1-3s1-5s1-6s0-8s1` | H3/two | presplit | certified | 448.9 | 54.7 |
| 66 | 2931 | `0s0_4s1-5s0__1s0-2s0-3s1-6s0-7s0-8s1` | H3/two | never_ran | certified | 278.1 | 40.3 |
| 67 | 2975 | `0s0_4s1-5s0__1s1-2s1-3s0-6s1-7s0-8s1` | H3/two | never_ran | certified | 433.5 | 49.1 |
| 68 | 3019 | `0s0_4s1-6s0__1s0-2s1-3s1-5s0-7s0-8s0` | H3/two | presplit | certified | 277.9 | 40.5 |
| 69 | 3063 | `0s0_4s1-6s1__1s0-2s0-3s0-5s1-7s0-8s0` | H3/two | presplit | certified | 81.8 | 25.5 |
| 70 | 3107 | `0s0_4s1-6s1__1s1-2s1-3s0-5s0-7s0-8s0` | H3/two | presplit | certified | 127.3 | 33.5 |
| 71 | 3151 | `0s0_4s1-7s0__1s0-2s1-3s1-5s1-6s0-8s0` | H3/two | presplit | certified | 305.1 | 49.8 |
| 72 | 3195 | `0s0_5s0-6s0__1s0-2s0-3s1-4s0-7s0-8s0` | H3/two | presplit | certified | 12.6 | 14.9 |
| 73 | 3239 | `0s0_5s0-6s0__1s1-2s1-3s0-4s1-7s0-8s0` | H3/two | presplit | certified | 38.9 | 22.0 |
| 74 | 3283 | `0s0_5s0-6s1__1s1-2s0-3s0-4s0-7s0-8s0` | H3/two | presplit | certified | 221.1 | 39.9 |
| 75 | 3327 | `0s0_5s1-6s0__1s1-2s0-3s1-4s1-7s1-8s1` | H3/two | timeout300 | certified | 399.9 | 61.9 |
| 76 | 3371 | `0s0-1s1_5__2s0-3s0-4s1-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 182.6 | 37.3 |
| 77 | 3415 | `0s0-2s1_3__1s1-4s0-5s1-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 277.0 | 43.3 |
| 78 | 3459 | `0s0-2s1_5__1s0-3s0-4s0-6s0-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 264.1 | 39.4 |
| 79 | 3503 | `0s0-2s1_5__1s1-3s1-4s1-6s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 259.2 | 41.8 |
| 80 | 3547 | `0s0-2s1_6__1s1-3s0-4s0-5s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 260.1 | 50.8 |
| 81 | 3591 | `0s0-3s1_4__1s1-2s0-5s1-6s0-7s1-8s0` | H6(3,1)/one | never_ran | certified | 260.7 | 39.9 |
| 82 | 3635 | `0s0-3s1_5__1s0-2s1-4s0-6s1-7s1-8s0` | H6(3,1)/one | presplit | certified | 210.2 | 37.7 |
| 83 | 3679 | `0s0-4s0_6__1s0-2s0-3s0-5s0-7s1-8s0` | H6(4,0)/one | presplit | certified | 44.9 | 29.4 |
| 84 | 3723 | `0s0-4s0_6__1s1-2s0-3s1-5s1-7s1-8s0` | H6(4,0)/one | presplit | certified | 87.4 | 30.3 |
| 85 | 3767 | `0s0-5s0_6__1s0-2s1-3s0-4s1-7s0-8s1` | H6(5,0)/one | presplit | certified | 46.6 | 27.0 |
| 86 | 3811 | `0s0-5s0_7__1s0-2s0-3s0-4s0-6s0-8s1` | H6(5,0)/one | presplit | certified | 51.3 | 41.3 |
| 87 | 3855 | `0s0-5s0_7__1s1-2s0-3s1-4s1-6s0-8s1` | H6(5,0)/one | presplit | certified | 56.1 | 36.7 |
| 88 | 3899 | `0s0-5s1_1__2s1-3s0-4s0-6s1-7s1-8s1` | H6(5,1)/one | presplit | certified | 195.1 | 37.7 |
| 89 | 3943 | `0s0-5s1_2__1s0-3s1-4s0-6s0-7s1-8s1` | H6(5,1)/one | presplit | certified | 179.0 | 34.2 |
| 90 | 3987 | `0s0-5s1_2__1s1-3s1-4s1-6s1-7s1-8s1` | H6(5,1)/one | presplit | certified | 130.5 | 30.9 |
| 91 | 4031 | `0s0-5s1_1s1-10s1__2s0-3s1-4s0-6s0-7s1-8s0` | H6(5,1)/two | never_ran | certified | 25.1 | 23.6 |
| 92 | 4075 | `0s0-5s1_1s1-10s1__2s1-3s1-4s1-6s1-7s1-8s0` | H6(5,1)/two | never_ran | certified | 36.1 | 25.1 |

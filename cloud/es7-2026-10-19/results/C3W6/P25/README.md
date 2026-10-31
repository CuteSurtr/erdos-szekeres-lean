# C3W6 P25: W6.tsv shard 25 of 44, cap 900

**All 93 units certified** (both checkers accepted every proof). No SAT, no proof rejections, no timeouts, no split records, no rechecks needed, no memory problems (at least 6 GB free the whole time), and no unit ended early without a certificate.

## Setup

- Task: `results/C3W6/TASK.md` at c5260b44, with V = P25, LIST = W6.tsv, j = 25, N = 44, H = 4.5.
- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `.../results/C3U2/tools`, used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. The checker sanity test passed: `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both. Details are in `tools.txt`.
- Base CNF: `gen_case.py 11 7 none` gives `p cnf 168399 4154921` with sha256 `bf0e502e…6da` (matches).
- Units: the rows of W6.tsv with row ≡ 25 (mod 44), so 93 units (`units.tsv`). Nothing was seeded. Lane k (`lane{k}.sh`) took positions ≡ k (mod 3), 31 units per lane, and ran `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- Times: start 05:31:40 UTC and END 09:46:40 UTC. The lanes started at 05:34:38 and all three finished on their own, at 08:26:45, 08:40:27 and 08:31:43, so nothing was killed at END.
- `out.jsonl` holds lane 0, then lane 1, then lane 2. `driver{k}.log.tail` holds the last 100 lines of each driver log.

## Totals

| stratum | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 |
| H6(1,1)/one | 1 | 1 | 0 | 0 |
| H6(2,1)/one | 4 | 4 | 0 | 0 |
| H6(3,1)/one | 2 | 2 | 0 | 0 |
| H6(4,0)/one | 2 | 2 | 0 | 0 |
| H6(5,0)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/two | 2 | 2 | 0 | 0 |
| **all** | **93** | **93** | 0 | 0 |

| prior | units | certified |
|---|---|---|
| timeout300 | 25 | 25 |
| presplit | 58 | 58 |
| never_ran | 10 | 10 |

Solve times of the 93 certified units:

| min | Q1 | median | Q3 | p90 | max |
|---|---|---|---|---|---|
| 16.0 s | 98.4 s | 290.4 s | 458.8 s | 542.9 s | 694.7 s |

- 43 units were certified above 300 s, so they would have timed out at the old cap.
- Total solve time was 27,362 s and total check time 4,494 s. The longest check took 77.1 s.
- 12 units solved in under 72 s. Every one of them is certified, so none of them is an early end.

## Per unit

Lane = position mod 3. Times are in seconds.

| row | lane | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 25 | 0 | `0s0_1s0-2s0__3s0-4s0-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 41.9 | 43.0 |
| 69 | 1 | `0s0_1s0-2s0__3s1-4s1-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 59.6 | 49.7 |
| 113 | 2 | `0s0_1s0-2s1__3s1-4s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 474.1 | 73.9 |
| 157 | 0 | `0s0_1s0-3s1__2s1-4s1-5s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 486.8 | 77.1 |
| 201 | 1 | `0s0_1s0-4s1__2s1-3s1-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 502.3 | 74.0 |
| 245 | 2 | `0s0_1s0-5s1__2s1-3s1-4s1-6s0-7s1-8s1` | H3/two | timeout300 | certified | 469.1 | 72.4 |
| 289 | 0 | `0s0_1s0-7s0__2s1-3s1-4s0-5s0-6s0-8s1` | H3/two | timeout300 | certified | 219.3 | 62.3 |
| 333 | 1 | `0s0_1s1-2s0__3s0-4s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 477.9 | 74.6 |
| 377 | 2 | `0s0_1s1-4s0__2s1-3s0-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 395.0 | 57.4 |
| 421 | 0 | `0s0_1s1-5s0__2s1-3s1-4s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 367.0 | 65.0 |
| 465 | 1 | `0s0_1s1-5s1__2s0-3s1-4s1-6s1-7s1-8s0` | H3/two | presplit | certified | 201.7 | 56.7 |
| 509 | 2 | `0s0_1s1-7s1__2s0-3s1-4s1-5s0-6s0-8s0` | H3/two | timeout300 | certified | 299.2 | 54.2 |
| 553 | 0 | `0s0_1s1-8s0__2s0-3s0-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 117.8 | 42.2 |
| 597 | 1 | `0s0_1s1-8s0__2s1-3s1-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 94.7 | 40.3 |
| 641 | 2 | `0s0_1s1-8s1__2s1-3s1-4s1-5s0-6s1-7s0` | H3/two | timeout300 | certified | 555.3 | 61.7 |
| 685 | 0 | `0s0_1s1-9s1__2s1-3s1-4s0-5s0-6s1-7s1` | H3/two | never_ran | certified | 530.2 | 60.8 |
| 729 | 1 | `0s0_2s0-3s1__1s0-4s1-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 344.3 | 56.2 |
| 773 | 2 | `0s0_2s0-4s1__1s0-3s0-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 403.2 | 54.8 |
| 817 | 0 | `0s0_2s0-4s1__1s1-3s1-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 603.6 | 63.5 |
| 861 | 1 | `0s0_2s0-5s0__1s1-3s0-4s0-6s0-7s1-8s1` | H3/two | presplit | certified | 95.0 | 42.1 |
| 905 | 2 | `0s0_2s0-5s1__1s0-3s1-4s0-6s1-7s1-8s0` | H3/two | timeout300 | certified | 471.3 | 59.8 |
| 949 | 0 | `0s0_2s0-6s1__1s0-3s0-4s0-5s0-7s1-8s1` | H3/two | timeout300 | certified | 335.2 | 49.3 |
| 993 | 1 | `0s0_2s0-6s1__1s1-3s1-4s0-5s0-7s0-8s0` | H3/two | timeout300 | certified | 333.5 | 45.0 |
| 1037 | 2 | `0s0_2s0-7s0__1s0-3s1-4s1-5s1-6s0-8s0` | H3/two | presplit | certified | 117.3 | 38.9 |
| 1081 | 0 | `0s0_2s0-7s1__1s0-3s0-4s1-5s0-6s0-8s0` | H3/two | presplit | certified | 250.4 | 61.8 |
| 1125 | 1 | `0s0_2s0-7s1__1s1-3s1-4s0-5s1-6s0-8s0` | H3/two | presplit | certified | 275.5 | 47.4 |
| 1169 | 2 | `0s0_2s0-8s0__1s1-3s1-4s0-5s0-6s1-7s0` | H3/two | presplit | certified | 229.5 | 58.2 |
| 1213 | 0 | `0s0_2s1-3s0__1s0-4s1-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 384.3 | 50.4 |
| 1257 | 1 | `0s0_2s1-3s1__1s0-4s0-5s1-6s0-7s1-8s1` | H3/two | presplit | certified | 78.7 | 36.9 |
| 1301 | 2 | `0s0_2s1-3s1__1s1-4s1-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 77.4 | 36.5 |
| 1345 | 0 | `0s0_2s1-4s0__1s1-3s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 525.6 | 58.3 |
| 1389 | 1 | `0s0_2s1-5s0__1s0-3s1-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 400.1 | 55.6 |
| 1433 | 2 | `0s0_2s1-6s0__1s0-3s0-4s0-5s0-7s0-8s1` | H3/two | presplit | certified | 260.1 | 42.9 |
| 1477 | 0 | `0s0_2s1-6s0__1s1-3s0-4s1-5s1-7s0-8s1` | H3/two | presplit | certified | 551.3 | 57.1 |
| 1521 | 1 | `0s0_2s1-6s1__1s0-3s1-4s1-5s0-7s0-8s1` | H3/two | presplit | certified | 314.7 | 48.6 |
| 1565 | 2 | `0s0_2s1-7s0__1s0-3s0-4s0-5s1-6s0-8s1` | H3/two | never_ran | certified | 205.6 | 41.3 |
| 1609 | 0 | `0s0_2s1-7s0__1s1-3s1-4s1-5s0-6s0-8s1` | H3/two | never_ran | certified | 258.1 | 63.2 |
| 1653 | 1 | `0s0_2s1-7s1__1s1-3s1-4s1-5s1-6s1-8s1` | H3/two | never_ran | certified | 413.1 | 54.3 |
| 1697 | 2 | `0s0_2s1-8s1__1s1-3s1-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 356.7 | 49.6 |
| 1741 | 0 | `0s0_2s1-9s0__1s1-3s0-4s0-5s0-6s0-7s0` | H3/two | presplit | certified | 160.3 | 38.1 |
| 1785 | 1 | `0s0_3s0-4s1__1s0-2s0-5s1-6s1-7s0-8s0` | H3/two | presplit | certified | 432.5 | 59.9 |
| 1829 | 2 | `0s0_3s0-4s1__1s1-2s1-5s1-6s0-7s0-8s0` | H3/two | presplit | certified | 512.7 | 57.1 |
| 1873 | 0 | `0s0_3s0-5s0__1s1-2s0-4s0-6s1-7s0-8s0` | H3/two | presplit | certified | 60.4 | 32.7 |
| 1917 | 1 | `0s0_3s0-5s1__1s0-2s1-4s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 559.4 | 64.2 |
| 1961 | 2 | `0s0_3s0-6s0__1s0-2s0-4s0-5s1-7s1-8s0` | H3/two | presplit | certified | 50.0 | 27.6 |
| 2005 | 0 | `0s0_3s0-6s0__1s1-2s1-4s0-5s0-7s1-8s0` | H3/two | presplit | certified | 148.7 | 36.2 |
| 2049 | 1 | `0s0_3s0-6s1__1s0-2s1-4s1-5s1-7s1-8s0` | H3/two | timeout300 | certified | 621.2 | 58.3 |
| 2093 | 2 | `0s0_3s0-7s0__1s0-2s0-4s1-5s0-6s1-8s0` | H3/two | presplit | certified | 77.3 | 35.8 |
| 2137 | 0 | `0s0_3s0-7s0__1s1-2s1-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 137.0 | 53.0 |
| 2181 | 1 | `0s0_3s0-7s1__1s1-2s0-4s0-5s0-6s1-8s0` | H3/two | presplit | certified | 290.4 | 46.8 |
| 2225 | 2 | `0s0_3s0-8s0__1s1-2s0-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 174.8 | 40.0 |
| 2269 | 0 | `0s0_3s0-8s1__1s1-2s0-4s1-5s1-6s1-7s1` | H3/two | timeout300 | certified | 425.7 | 59.5 |
| 2313 | 1 | `0s0_3s1-4s0__1s1-2s0-5s0-6s0-7s0-8s1` | H3/two | timeout300 | certified | 419.7 | 53.3 |
| 2357 | 2 | `0s0_3s1-4s1__1s0-2s0-5s1-6s1-7s0-8s1` | H3/two | presplit | certified | 90.1 | 33.5 |
| 2401 | 0 | `0s0_3s1-4s1__1s1-2s1-5s1-6s0-7s0-8s1` | H3/two | presplit | certified | 68.3 | 30.8 |
| 2445 | 1 | `0s0_3s1-5s0__1s1-2s0-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 508.1 | 55.1 |
| 2489 | 2 | `0s0_3s1-5s1__1s0-2s1-4s0-6s0-7s0-8s1` | H3/two | presplit | certified | 101.7 | 32.1 |
| 2533 | 0 | `0s0_3s1-5s1__1s1-2s1-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 77.7 | 32.2 |
| 2577 | 1 | `0s0_3s1-7s0__1s1-2s1-4s0-5s1-6s1-8s1` | H3/two | never_ran | certified | 529.9 | 50.7 |
| 2621 | 2 | `0s0_3s1-8s0__1s0-2s0-4s1-5s0-6s1-7s0` | H3/two | presplit | certified | 157.0 | 38.9 |
| 2665 | 0 | `0s0_3s1-8s0__1s1-2s1-4s0-5s1-6s1-7s0` | H3/two | presplit | certified | 278.9 | 43.9 |
| 2709 | 1 | `0s0_4s0-5s1__1s1-2s0-3s0-6s0-7s1-8s0` | H3/two | presplit | certified | 412.7 | 49.0 |
| 2753 | 2 | `0s0_4s0-6s1__1s0-2s0-3s1-5s1-7s1-8s0` | H3/two | presplit | certified | 466.8 | 55.3 |
| 2797 | 0 | `0s0_4s0-6s1__1s1-2s1-3s1-5s0-7s1-8s0` | H3/two | presplit | certified | 616.5 | 58.1 |
| 2841 | 1 | `0s0_4s0-7s0__1s1-2s0-3s0-5s1-6s1-8s0` | H3/two | presplit | certified | 56.6 | 44.4 |
| 2885 | 2 | `0s0_4s0-7s1__1s0-2s1-3s1-5s0-6s1-8s1` | H3/two | presplit | certified | 474.0 | 54.6 |
| 2929 | 0 | `0s0_4s1-5s0__1s0-2s0-3s0-6s1-7s1-8s1` | H3/two | never_ran | certified | 291.2 | 41.6 |
| 2973 | 1 | `0s0_4s1-5s0__1s1-2s1-3s0-6s0-7s1-8s1` | H3/two | never_ran | certified | 613.1 | 59.2 |
| 3017 | 2 | `0s0_4s1-6s0__1s0-2s1-3s0-5s1-7s1-8s0` | H3/two | presplit | certified | 493.4 | 68.4 |
| 3061 | 0 | `0s0_4s1-6s1__1s0-2s0-3s0-5s0-7s1-8s0` | H3/two | presplit | certified | 130.3 | 36.2 |
| 3105 | 1 | `0s0_4s1-6s1__1s1-2s0-3s1-5s1-7s1-8s0` | H3/two | presplit | certified | 79.3 | 32.4 |
| 3149 | 2 | `0s0_4s1-7s0__1s0-2s1-3s1-5s0-6s1-8s0` | H3/two | presplit | certified | 450.7 | 51.4 |
| 3193 | 0 | `0s0_5s0-6s0__1s0-2s0-3s0-4s1-7s1-8s0` | H3/two | presplit | certified | 23.0 | 17.0 |
| 3237 | 1 | `0s0_5s0-6s0__1s1-2s1-3s0-4s0-7s1-8s0` | H3/two | presplit | certified | 23.3 | 21.5 |
| 3281 | 2 | `0s0_5s0-6s1__1s0-2s1-3s1-4s1-7s1-8s0` | H3/two | presplit | certified | 553.9 | 60.5 |
| 3325 | 0 | `0s0_5s1-6s0__1s1-2s0-3s1-4s1-7s0-8s1` | H3/two | timeout300 | certified | 694.7 | 66.4 |
| 3369 | 1 | `0s0-1s1_5__2s0-3s0-4s1-6s1-7s0-8s1` | H6(1,1)/one | timeout300 | certified | 378.4 | 48.8 |
| 3413 | 2 | `0s0-2s1_3__1s1-4s0-5s0-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | certified | 420.1 | 48.8 |
| 3457 | 0 | `0s0-2s1_5__1s0-3s0-4s0-6s0-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 272.1 | 42.4 |
| 3501 | 1 | `0s0-2s1_5__1s1-3s1-4s0-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 426.6 | 51.1 |
| 3545 | 2 | `0s0-2s1_6__1s1-3s0-4s0-5s1-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 290.4 | 44.1 |
| 3589 | 0 | `0s0-3s1_4__1s1-2s0-5s1-6s0-7s0-8s0` | H6(3,1)/one | never_ran | certified | 326.4 | 49.6 |
| 3633 | 1 | `0s0-3s1_5__1s0-2s1-4s0-6s1-7s0-8s0` | H6(3,1)/one | presplit | certified | 296.0 | 45.6 |
| 3677 | 2 | `0s0-4s0_6__1s0-2s0-3s0-5s0-7s0-8s0` | H6(4,0)/one | presplit | certified | 44.2 | 29.9 |
| 3721 | 0 | `0s0-4s0_6__1s1-2s0-3s1-5s1-7s0-8s0` | H6(4,0)/one | presplit | certified | 91.1 | 33.4 |
| 3765 | 1 | `0s0-5s0_6__1s0-2s1-3s0-4s0-7s1-8s1` | H6(5,0)/one | presplit | certified | 44.6 | 25.1 |
| 3809 | 2 | `0s0-5s0_6__1s1-2s1-3s1-4s1-7s1-8s1` | H6(5,0)/one | presplit | certified | 81.0 | 35.6 |
| 3853 | 0 | `0s0-5s0_7__1s1-2s0-3s1-4s0-6s1-8s1` | H6(5,0)/one | presplit | certified | 73.4 | 31.6 |
| 3897 | 1 | `0s0-5s1_1__2s1-3s0-4s0-6s1-7s0-8s1` | H6(5,1)/one | presplit | certified | 258.3 | 44.4 |
| 3941 | 2 | `0s0-5s1_2__1s0-3s1-4s0-6s0-7s0-8s1` | H6(5,1)/one | presplit | certified | 247.3 | 42.8 |
| 3985 | 0 | `0s0-5s1_2__1s1-3s1-4s1-6s1-7s0-8s1` | H6(5,1)/one | presplit | certified | 203.5 | 40.1 |
| 4029 | 1 | `0s0-5s1_1s1-10s1__2s0-3s1-4s0-6s0-7s0-8s0` | H6(5,1)/two | never_ran | certified | 16.0 | 17.9 |
| 4073 | 2 | `0s0-5s1_1s1-10s1__2s1-3s1-4s1-6s1-7s0-8s0` | H6(5,1)/two | never_ran | certified | 55.3 | 30.5 |

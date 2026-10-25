# C3W6 P03: units of W6.tsv with row ≡ 3 (mod 44), cap 900

Task: `results/C3W6/TASK.md` at c5260b44, with V = P03, LIST = W6.tsv, j = 3, N = 44, H = 4.5.

## Result

**All 94 units were certified at cap 900.** None timed out, none were left unreached, and no split records were written. There was no SAT, no proof rejection and no memory problem (free memory never fell below about 6 GB, with no OOM). No unit ended in under 72 s without a certificate. The fastest unit took 47.2 s, and it was certified. All 94 records have `status` UNSATISFIABLE, `lrat_check` "c VERIFIED", `cake_lpr` "s VERIFIED UNSAT" and `certified` true. No recheck was needed, so there is no `recheck.jsonl`.

## Tools and base check

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Checker sanity test passed: `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches). Details are in `tools.txt`.
- `compose.py` was not run.

## Run

- Machine: 4 cores, 15 GB RAM (`env.txt`). Start 05:31:48 UTC on 2026-10-25, END 09:46:48 UTC.
- Lanes started at 05:35:32. All three ran out of units before END; the last one finished at 09:21:22. Nothing had to be killed at END.
- 3 lanes (`lane0.sh`–`lane2.sh`), lane k = positions ≡ k (mod 3) of `units.tsv`. Each unit ran `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` holds lane 0, then lane 1, then lane 2 (94 records). Records were not seeded.
- Total solve time 33,265 s; total check time 5,084 s (max 88.2 s).

## Solve-time distribution of the certified units

certified: 94; solve s min 47.2, q1 173.2, median 380.4, q3 491.8, p90 600.5, max 872.8; above 300 s: 58

Above 300 s by `prior`:
- timeout300: 26 of 28 (median 454.5 s, max 666.9 s)
- never_ran: 8 of 11 (median 377.7 s, max 872.8 s)
- presplit: 24 of 55 (median 256.0 s, max 740.6 s)

The cap of 900 s was needed: 58 of 94 units would have timed out at 300 s.

## Totals per stratum and per prior

| group | value | certified | timed out at 900 | not reached |
|---|---|---|---|---|
| prior | never_ran | 11 | 0 | 0 |
| prior | presplit | 55 | 0 | 0 |
| prior | timeout300 | 28 | 0 | 0 |
| stratum | H3/two | 76 | 0 | 0 |
| stratum | H6(1,1)/one | 2 | 0 | 0 |
| stratum | H6(2,1)/one | 4 | 0 | 0 |
| stratum | H6(3,1)/one | 2 | 0 | 0 |
| stratum | H6(4,0)/one | 1 | 0 | 0 |
| stratum | H6(4,1)/one | 1 | 0 | 0 |
| stratum | H6(5,0)/one | 2 | 0 | 0 |
| stratum | H6(5,1)/one | 4 | 0 | 0 |
| stratum | H6(5,1)/two | 2 | 0 | 0 |


## Per unit

| pos | lane | row | node | stratum | prior | result | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 3 | 0s0_1s0-10s0__2s1-3s0-4s1-5s1-6s1-7s0 | H3/two | timeout300 | certified | 269.8 | 63.9 |
| 1 | 1 | 47 | 0s0_1s0-2s0__3s1-4s0-5s0-6s0-7s1-8s0 | H3/two | presplit | certified | 47.2 | 47.3 |
| 2 | 2 | 91 | 0s0_1s0-2s1__3s0-4s1-5s0-6s1-7s0-8s1 | H3/two | timeout300 | certified | 487.9 | 76.4 |
| 3 | 0 | 135 | 0s0_1s0-3s1__2s0-4s1-5s1-6s0-7s1-8s0 | H3/two | timeout300 | certified | 515.3 | 76.9 |
| 4 | 1 | 179 | 0s0_1s0-4s1__2s0-3s1-5s1-6s0-7s1-8s0 | H3/two | timeout300 | certified | 498.2 | 75.8 |
| 5 | 2 | 223 | 0s0_1s0-5s1__2s1-3s0-4s0-6s0-7s1-8s0 | H3/two | timeout300 | certified | 406.8 | 69.7 |
| 6 | 0 | 267 | 0s0_1s0-7s0__2s0-3s1-4s1-5s0-6s1-8s0 | H3/two | timeout300 | certified | 207.8 | 47.7 |
| 7 | 1 | 311 | 0s0_1s1-2s0__3s0-4s0-5s1-6s0-7s0-8s0 | H3/two | timeout300 | certified | 413.3 | 67.3 |
| 8 | 2 | 355 | 0s0_1s1-2s0__3s1-4s1-5s0-6s1-7s0-8s0 | H3/two | timeout300 | certified | 486.0 | 68.6 |
| 9 | 0 | 399 | 0s0_1s1-5s0__2s0-3s1-4s1-6s0-7s0-8s0 | H3/two | timeout300 | certified | 428.9 | 68.3 |
| 10 | 1 | 443 | 0s0_1s1-5s1__2s0-3s0-4s1-6s0-7s0-8s0 | H3/two | presplit | certified | 153.3 | 53.1 |
| 11 | 2 | 487 | 0s0_1s1-5s1__2s1-3s1-4s0-6s1-7s0-8s0 | H3/two | presplit | certified | 263.8 | 51.3 |
| 12 | 0 | 531 | 0s0_1s1-7s1__2s1-3s1-4s0-5s0-6s0-8s0 | H3/two | timeout300 | certified | 349.3 | 53.6 |
| 13 | 1 | 575 | 0s0_1s1-8s0__2s0-3s1-4s1-5s1-6s0-7s0 | H3/two | presplit | certified | 100.9 | 52.8 |
| 14 | 2 | 619 | 0s0_1s1-8s1__2s0-3s1-4s1-5s1-6s0-7s1 | H3/two | timeout300 | certified | 540.2 | 66.7 |
| 15 | 0 | 663 | 0s0_1s1-9s1__2s0-3s1-4s1-5s1-6s0-7s1 | H3/two | never_ran | certified | 660.6 | 84.2 |
| 16 | 1 | 707 | 0s0_2s0-3s1__1s0-4s0-5s1-6s0-7s0-8s1 | H3/two | presplit | certified | 448.4 | 65.6 |
| 17 | 2 | 751 | 0s0_2s0-3s1__1s1-4s1-5s0-6s1-7s0-8s1 | H3/two | presplit | certified | 572.8 | 67.2 |
| 18 | 0 | 795 | 0s0_2s0-4s1__1s1-3s0-5s0-6s0-7s0-8s1 | H3/two | presplit | certified | 450.8 | 63.5 |
| 19 | 1 | 839 | 0s0_2s0-5s0__1s0-3s0-4s1-6s1-7s0-8s1 | H3/two | presplit | certified | 64.4 | 41.0 |
| 20 | 2 | 883 | 0s0_2s0-5s0__1s1-3s1-4s1-6s0-7s0-8s1 | H3/two | presplit | certified | 103.0 | 38.4 |
| 21 | 0 | 927 | 0s0_2s0-5s1__1s1-3s0-4s1-6s1-7s0-8s0 | H3/two | timeout300 | certified | 472.9 | 50.2 |
| 22 | 1 | 971 | 0s0_2s0-6s1__1s0-3s1-4s1-5s0-7s1-8s0 | H3/two | timeout300 | certified | 586.8 | 66.5 |
| 23 | 2 | 1015 | 0s0_2s0-7s0__1s0-3s0-4s0-5s1-6s1-8s0 | H3/two | presplit | certified | 128.0 | 39.2 |
| 24 | 0 | 1059 | 0s0_2s0-7s0__1s1-3s1-4s0-5s0-6s1-8s0 | H3/two | presplit | certified | 182.1 | 41.2 |
| 25 | 1 | 1103 | 0s0_2s0-7s1__1s0-3s1-4s1-5s1-6s1-8s0 | H3/two | presplit | certified | 475.5 | 71.6 |
| 26 | 2 | 1147 | 0s0_2s0-8s0__1s0-3s1-4s1-5s1-6s0-7s0 | H3/two | presplit | certified | 180.1 | 43.5 |
| 27 | 0 | 1191 | 0s0_2s1-3s0__1s0-4s0-5s1-6s0-7s0-8s1 | H3/two | timeout300 | certified | 416.3 | 53.8 |
| 28 | 1 | 1235 | 0s0_2s1-3s0__1s1-4s1-5s0-6s1-7s0-8s1 | H3/two | timeout300 | certified | 666.9 | 62.4 |
| 29 | 2 | 1279 | 0s0_2s1-3s1__1s1-4s0-5s0-6s0-7s0-8s1 | H3/two | presplit | certified | 93.6 | 36.1 |
| 30 | 0 | 1323 | 0s0_2s1-4s0__1s0-3s1-5s0-6s0-7s0-8s0 | H3/two | timeout300 | certified | 385.5 | 53.8 |
| 31 | 1 | 1367 | 0s0_2s1-4s0__1s1-3s1-5s1-6s1-7s1-8s1 | H3/two | timeout300 | certified | 468.5 | 68.0 |
| 32 | 2 | 1411 | 0s0_2s1-5s0__1s1-3s0-4s1-6s0-7s1-8s1 | H3/two | presplit | certified | 623.0 | 65.1 |
| 33 | 0 | 1455 | 0s0_2s1-6s0__1s0-3s1-4s0-5s1-7s1-8s1 | H3/two | presplit | certified | 352.5 | 50.6 |
| 34 | 1 | 1499 | 0s0_2s1-6s1__1s0-3s0-4s0-5s0-7s1-8s1 | H3/two | presplit | certified | 179.8 | 59.7 |
| 35 | 2 | 1543 | 0s0_2s1-6s1__1s1-3s0-4s1-5s1-7s1-8s1 | H3/two | presplit | certified | 262.5 | 38.4 |
| 36 | 0 | 1587 | 0s0_2s1-7s0__1s1-3s0-4s0-5s0-6s1-8s1 | H3/two | never_ran | certified | 379.2 | 49.0 |
| 37 | 1 | 1631 | 0s0_2s1-7s1__1s1-3s0-4s1-5s0-6s0-8s1 | H3/two | never_ran | certified | 238.0 | 46.6 |
| 38 | 2 | 1675 | 0s0_2s1-8s1__1s0-3s1-4s1-5s1-6s1-7s0 | H3/two | presplit | certified | 644.4 | 59.6 |
| 39 | 0 | 1719 | 0s0_2s1-9s0__1s0-3s0-4s1-5s0-6s1-7s0 | H3/two | presplit | certified | 111.7 | 31.8 |
| 40 | 1 | 1763 | 0s0_2s1-9s0__1s1-3s1-4s0-5s1-6s1-7s0 | H3/two | presplit | certified | 125.6 | 39.1 |
| 41 | 2 | 1807 | 0s0_3s0-4s1__1s1-2s0-5s0-6s0-7s1-8s0 | H3/two | presplit | certified | 548.6 | 56.6 |
| 42 | 0 | 1851 | 0s0_3s0-5s0__1s0-2s0-4s1-6s1-7s1-8s0 | H3/two | presplit | certified | 54.4 | 26.7 |
| 43 | 1 | 1895 | 0s0_3s0-5s0__1s1-2s1-4s1-6s0-7s1-8s0 | H3/two | presplit | certified | 106.4 | 32.9 |
| 44 | 2 | 1939 | 0s0_3s0-5s1__1s1-2s1-4s0-6s0-7s0-8s0 | H3/two | timeout300 | certified | 514.2 | 58.7 |
| 45 | 0 | 1983 | 0s0_3s0-6s0__1s0-2s1-4s1-5s1-7s0-8s0 | H3/two | presplit | certified | 84.3 | 32.9 |
| 46 | 1 | 2027 | 0s0_3s0-6s1__1s0-2s0-4s1-5s0-7s0-8s0 | H3/two | timeout300 | certified | 399.3 | 51.2 |
| 47 | 2 | 2071 | 0s0_3s0-6s1__1s1-2s1-4s0-5s1-7s0-8s0 | H3/two | never_ran | certified | 491.7 | 66.7 |
| 48 | 0 | 2115 | 0s0_3s0-7s0__1s1-2s0-4s0-5s0-6s0-8s0 | H3/two | presplit | certified | 108.0 | 63.5 |
| 49 | 1 | 2159 | 0s0_3s0-7s1__1s0-2s0-4s1-5s1-6s0-8s0 | H3/two | presplit | certified | 392.4 | 53.9 |
| 50 | 2 | 2203 | 0s0_3s0-7s1__1s1-2s1-4s1-5s0-6s0-8s0 | H3/two | presplit | certified | 404.0 | 55.7 |
| 51 | 0 | 2247 | 0s0_3s0-8s0__1s1-2s1-4s1-5s0-6s1-7s0 | H3/two | presplit | certified | 256.0 | 44.1 |
| 52 | 1 | 2291 | 0s0_3s1-4s0__1s0-2s0-5s1-6s0-7s1-8s1 | H3/two | timeout300 | certified | 567.0 | 68.9 |
| 53 | 2 | 2335 | 0s0_3s1-4s0__1s1-2s1-5s0-6s1-7s1-8s1 | H3/two | never_ran | certified | 565.1 | 59.5 |
| 54 | 0 | 2379 | 0s0_3s1-4s1__1s1-2s0-5s0-6s0-7s1-8s1 | H3/two | presplit | certified | 95.0 | 34.7 |
| 55 | 1 | 2423 | 0s0_3s1-5s0__1s0-2s0-4s1-6s1-7s1-8s1 | H3/two | presplit | certified | 396.2 | 45.7 |
| 56 | 2 | 2467 | 0s0_3s1-5s0__1s1-2s1-4s1-6s0-7s1-8s1 | H3/two | presplit | certified | 724.9 | 62.7 |
| 57 | 0 | 2511 | 0s0_3s1-5s1__1s1-2s0-4s0-6s1-7s1-8s1 | H3/two | presplit | certified | 114.1 | 49.7 |
| 58 | 1 | 2555 | 0s0_3s1-7s0__1s1-2s0-4s0-5s0-6s0-8s1 | H3/two | never_ran | certified | 363.3 | 47.3 |
| 59 | 2 | 2599 | 0s0_3s1-7s1__1s1-2s0-4s0-5s1-6s1-8s0 | H3/two | timeout300 | certified | 435.5 | 54.5 |
| 60 | 0 | 2643 | 0s0_3s1-8s0__1s1-2s0-4s0-5s0-6s0-7s0 | H3/two | presplit | certified | 228.4 | 43.3 |
| 61 | 1 | 2687 | 0s0_4s0-5s1__1s0-2s0-3s1-6s1-7s0-8s0 | H3/two | presplit | certified | 614.3 | 60.2 |
| 62 | 2 | 2731 | 0s0_4s0-5s1__1s1-2s1-3s1-6s0-7s0-8s0 | H3/two | presplit | certified | 569.4 | 57.4 |
| 63 | 0 | 2775 | 0s0_4s0-6s1__1s1-2s0-3s0-5s1-7s0-8s0 | H3/two | presplit | certified | 438.0 | 69.1 |
| 64 | 1 | 2819 | 0s0_4s0-7s0__1s0-2s1-3s0-5s0-6s0-8s0 | H3/two | presplit | certified | 73.5 | 37.0 |
| 65 | 2 | 2863 | 0s0_4s0-7s0__1s1-2s1-3s1-5s1-6s0-8s0 | H3/two | presplit | certified | 185.6 | 42.7 |
| 66 | 0 | 2907 | 0s0_4s0-7s1__1s1-2s1-3s0-5s0-6s0-8s1 | H3/two | presplit | certified | 653.9 | 61.5 |
| 67 | 1 | 2951 | 0s0_4s1-5s0__1s0-2s1-3s1-6s1-7s0-8s1 | H3/two | never_ran | certified | 872.8 | 69.9 |
| 68 | 2 | 2995 | 0s0_4s1-6s0__1s0-2s0-3s0-5s0-7s0-8s0 | H3/two | presplit | certified | 334.0 | 49.1 |
| 69 | 0 | 3039 | 0s0_4s1-6s0__1s1-2s0-3s1-5s1-7s0-8s0 | H3/two | presplit | certified | 740.6 | 69.1 |
| 70 | 1 | 3083 | 0s0_4s1-6s1__1s0-2s1-3s1-5s0-7s0-8s0 | H3/two | presplit | certified | 146.5 | 41.6 |
| 71 | 2 | 3127 | 0s0_4s1-7s0__1s0-2s0-3s0-5s1-6s0-8s0 | H3/two | presplit | certified | 313.3 | 48.5 |
| 72 | 0 | 3171 | 0s0_4s1-7s0__1s1-2s1-3s0-5s0-6s0-8s0 | H3/two | presplit | certified | 448.0 | 70.5 |
| 73 | 1 | 3215 | 0s0_5s0-6s0__1s0-2s1-3s1-4s1-7s0-8s0 | H3/two | presplit | certified | 86.0 | 31.5 |
| 74 | 2 | 3259 | 0s0_5s0-6s1__1s0-2s0-3s1-4s0-7s0-8s0 | H3/two | presplit | certified | 413.6 | 48.7 |
| 75 | 0 | 3303 | 0s0_5s0-6s1__1s1-2s1-3s0-4s1-7s0-8s0 | H3/two | presplit | certified | 583.8 | 65.4 |
| 76 | 1 | 3347 | 0s0-1s1_4__2s1-3s0-5s0-6s0-7s0-8s1 | H6(1,1)/one | timeout300 | certified | 524.9 | 88.2 |
| 77 | 2 | 3391 | 0s0-1s1_5__2s1-3s0-4s1-6s0-7s1-8s1 | H6(1,1)/one | timeout300 | certified | 358.7 | 50.2 |
| 78 | 0 | 3435 | 0s0-2s1_4__1s1-3s0-5s0-6s1-7s1-8s1 | H6(2,1)/one | timeout300 | certified | 567.1 | 78.1 |
| 79 | 1 | 3479 | 0s0-2s1_5__1s1-3s0-4s0-6s0-7s0-8s0 | H6(2,1)/one | timeout300 | certified | 491.9 | 64.0 |
| 80 | 2 | 3523 | 0s0-2s1_6__1s0-3s0-4s1-5s1-7s1-8s0 | H6(2,1)/one | timeout300 | certified | 315.1 | 46.8 |
| 81 | 0 | 3567 | 0s0-2s1_6__1s1-3s1-4s1-5s0-7s1-8s0 | H6(2,1)/one | timeout300 | certified | 381.6 | 51.3 |
| 82 | 1 | 3611 | 0s0-3s1_4__1s1-2s1-5s1-6s1-7s1-8s0 | H6(3,1)/one | never_ran | certified | 326.2 | 48.6 |
| 83 | 2 | 3655 | 0s0-3s1_5__1s1-2s0-4s1-6s0-7s1-8s0 | H6(3,1)/one | presplit | certified | 478.9 | 61.0 |
| 84 | 0 | 3699 | 0s0-4s0_6__1s0-2s1-3s0-5s1-7s1-8s0 | H6(4,0)/one | presplit | certified | 80.8 | 36.1 |
| 85 | 1 | 3743 | 0s0-4s1_5__1s1-2s1-3s0-6s1-7s0-8s1 | H6(4,1)/one | timeout300 | certified | 440.5 | 58.0 |
| 86 | 2 | 3787 | 0s0-5s0_6__1s1-2s0-3s1-4s0-7s0-8s1 | H6(5,0)/one | presplit | certified | 83.3 | 42.1 |
| 87 | 0 | 3831 | 0s0-5s0_7__1s0-2s1-3s0-4s1-6s0-8s1 | H6(5,0)/one | presplit | certified | 108.1 | 36.6 |
| 88 | 1 | 3875 | 0s0-5s1_1__2s0-3s0-4s1-6s1-7s1-8s1 | H6(5,1)/one | presplit | certified | 260.4 | 55.1 |
| 89 | 2 | 3919 | 0s0-5s1_1__2s1-3s1-4s1-6s0-7s1-8s1 | H6(5,1)/one | presplit | certified | 203.5 | 45.8 |
| 90 | 0 | 3963 | 0s0-5s1_2__1s1-3s0-4s0-6s1-7s1-8s1 | H6(5,1)/one | presplit | certified | 374.8 | 43.8 |
| 91 | 1 | 4007 | 0s0-5s1_6__1s1-2s1-3s0-4s1-7s0-8s0 | H6(5,1)/one | never_ran | certified | 377.7 | 52.5 |
| 92 | 2 | 4051 | 0s0-5s1_1s1-10s1__2s1-3s0-4s0-6s1-7s1-8s0 | H6(5,1)/two | never_ran | certified | 67.4 | 36.2 |
| 93 | 0 | 4095 | 0s0-5s1_2s1-3s0__1s1-4s1-6s1-7s0-8s1-9s0 | H6(5,1)/two | never_ran | certified | 60.8 | 33.2 |


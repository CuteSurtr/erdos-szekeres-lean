# C3W6 P01: units of W6.tsv with row ≡ 1 (mod 44), cap 900

Task `results/C3W6/TASK.md` at c5260b44, V = P01, LIST = W6.tsv, j = 1, N = 44, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 05:31:49 UTC, END 09:46:49 UTC;
the three lanes started at 05:35:01 and had all finished by 08:34:28 (lane 1 at 08:12, lane 0 at 08:16, lane 2 at 08:34), so END never came and nothing was killed.

## Tools (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. Checker sanity test on {1},{-1}: `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).

## Run

94 units (`units.tsv`), no seeding. Three lanes (`lane0.sh`–`lane2.sh`, started with `setsid nohup`). Lane k took positions ≡ k (mod 3), and each unit ran
`close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
`out.jsonl` holds the records of lane 0, then lane 1, then lane 2: 94 solve records and no split records.

## Result

**All 94 units were certified at cap 900.** None timed out, none was left unreached, and none was split. Every record has
`UNSATISFIABLE`, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT` and `certified: true`.

- SAT: none. Proof rejections: none. Records with cake_lpr `none`: none, so there is no `recheck.jsonl`. Memory problems: none (at most about 6 GB was in use).
- Units that ended in under 72 s: 11, all certified (28.1–69.9 s), so none ended early without a certificate.

| stratum | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 |
| H6(1,1)/one | 2 | 2 | 0 | 0 |
| H6(2,1)/one | 4 | 4 | 0 | 0 |
| H6(3,1)/one | 2 | 2 | 0 | 0 |
| H6(4,0)/one | 1 | 1 | 0 | 0 |
| H6(4,1)/one | 1 | 1 | 0 | 0 |
| H6(5,0)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/one | 3 | 3 | 0 | 0 |
| H6(5,1)/two | 2 | 2 | 0 | 0 |
| total | 94 | 94 | 0 | 0 |

| prior | units | certified | median solve s | certified above 300 s | max solve s |
|---|---|---|---|---|---|
| timeout300 | 29 | 29 | 355.6 | 22 | 571.6 |
| presplit | 54 | 54 | 186.9 | 18 | 586.4 |
| never_ran | 11 | 11 | 287.1 | 5 | 606.7 |

Solve time of the 94 certified units: min 28.1 s, Q1 107.7 s, median 287.8 s, Q3 384.0 s, p90 468.6 s, max 606.7 s.
**45 of the 94 were certified above 300 s**: a cap of 300 would have missed them, and cap 900 missed none.
Total solve time was 25,510 s. Check time was 22.7–68.6 s per unit, 4,242 s in all.

## Per unit (solve s, check s)

| row | node | stratum | prior | status | solve s | check s |
|---|---|---|---|---|---|---|
| 1 | `0s0_1s0-10s0__2s1-3s0-4s1-5s1-6s0-7s0` | H3/two | timeout300 | certified | 202.5 | 58.9 |
| 45 | `0s0_1s0-2s0__3s1-4s0-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 57.9 | 48.9 |
| 89 | `0s0_1s0-2s1__3s0-4s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 352.3 | 61.7 |
| 133 | `0s0_1s0-2s1__3s1-4s1-5s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 250.0 | 43.6 |
| 177 | `0s0_1s0-4s1__2s0-3s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | certified | 358.4 | 61.6 |
| 221 | `0s0_1s0-5s1__2s0-3s1-4s1-6s1-7s1-8s1` | H3/two | timeout300 | certified | 340.0 | 55.7 |
| 265 | `0s0_1s0-7s0__2s0-3s1-4s1-5s0-6s0-8s0` | H3/two | timeout300 | certified | 147.9 | 48.0 |
| 309 | `0s0_1s0-7s1__2s1-3s1-4s1-5s1-6s1-8s1` | H3/two | timeout300 | certified | 291.0 | 51.8 |
| 353 | `0s0_1s1-2s0__3s1-4s1-5s0-6s0-7s1-8s0` | H3/two | timeout300 | certified | 429.9 | 59.6 |
| 397 | `0s0_1s1-5s0__2s0-3s0-4s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 322.0 | 54.7 |
| 441 | `0s0_1s1-5s1__2s0-3s0-4s0-6s1-7s1-8s0` | H3/two | presplit | certified | 114.7 | 44.5 |
| 485 | `0s0_1s1-5s1__2s1-3s1-4s0-6s0-7s1-8s0` | H3/two | presplit | certified | 232.3 | 48.9 |
| 529 | `0s0_1s1-7s1__2s1-3s0-4s1-5s1-6s1-8s0` | H3/two | timeout300 | certified | 443.8 | 51.0 |
| 573 | `0s0_1s1-8s0__2s0-3s1-4s1-5s0-6s1-7s0` | H3/two | presplit | certified | 94.2 | 31.7 |
| 617 | `0s0_1s1-8s1__2s0-3s1-4s1-5s0-6s1-7s1` | H3/two | timeout300 | certified | 461.1 | 57.5 |
| 661 | `0s0_1s1-9s1__2s0-3s1-4s1-5s0-6s1-7s1` | H3/two | never_ran | certified | 472.8 | 58.0 |
| 705 | `0s0_2s0-3s1__1s0-4s0-5s0-6s1-7s1-8s1` | H3/two | presplit | certified | 388.9 | 64.2 |
| 749 | `0s0_2s0-3s1__1s1-4s1-5s0-6s0-7s1-8s1` | H3/two | presplit | certified | 475.8 | 68.6 |
| 793 | `0s0_2s0-4s1__1s0-3s1-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 396.1 | 55.9 |
| 837 | `0s0_2s0-5s0__1s0-3s0-4s1-6s0-7s1-8s1` | H3/two | presplit | certified | 51.9 | 36.9 |
| 881 | `0s0_2s0-5s0__1s1-3s1-4s0-6s1-7s1-8s1` | H3/two | presplit | certified | 107.5 | 38.6 |
| 925 | `0s0_2s0-5s1__1s1-3s0-4s1-6s0-7s1-8s0` | H3/two | timeout300 | certified | 386.0 | 52.5 |
| 969 | `0s0_2s0-6s1__1s0-3s1-4s1-5s0-7s0-8s0` | H3/two | timeout300 | certified | 309.0 | 54.0 |
| 1013 | `0s0_2s0-7s0__1s0-3s0-4s0-5s1-6s0-8s0` | H3/two | presplit | certified | 97.3 | 41.5 |
| 1057 | `0s0_2s0-7s0__1s1-3s1-4s0-5s0-6s0-8s0` | H3/two | presplit | certified | 140.8 | 41.0 |
| 1101 | `0s0_2s0-7s1__1s0-3s1-4s1-5s1-6s0-8s0` | H3/two | presplit | certified | 348.5 | 58.3 |
| 1145 | `0s0_2s0-8s0__1s0-3s1-4s1-5s0-6s1-7s0` | H3/two | presplit | certified | 148.5 | 39.2 |
| 1189 | `0s0_2s1-3s0__1s0-4s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | certified | 315.1 | 47.4 |
| 1233 | `0s0_2s1-3s0__1s1-4s1-5s0-6s0-7s1-8s1` | H3/two | timeout300 | certified | 422.7 | 66.9 |
| 1277 | `0s0_2s1-3s1__1s0-4s1-5s1-6s1-7s1-8s1` | H3/two | presplit | certified | 107.7 | 30.9 |
| 1321 | `0s0_2s1-4s0__1s0-3s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 431.0 | 50.4 |
| 1365 | `0s0_2s1-4s0__1s1-3s1-5s1-6s1-7s0-8s1` | H3/two | timeout300 | certified | 472.0 | 59.4 |
| 1409 | `0s0_2s1-5s0__1s1-3s0-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 408.7 | 50.9 |
| 1453 | `0s0_2s1-6s0__1s0-3s1-4s0-5s1-7s0-8s1` | H3/two | presplit | certified | 287.8 | 39.8 |
| 1497 | `0s0_2s1-6s1__1s0-3s0-4s0-5s0-7s0-8s1` | H3/two | presplit | certified | 136.7 | 37.0 |
| 1541 | `0s0_2s1-6s1__1s1-3s0-4s1-5s1-7s0-8s1` | H3/two | presplit | certified | 186.9 | 41.6 |
| 1585 | `0s0_2s1-7s0__1s1-3s0-4s0-5s0-6s0-8s1` | H3/two | never_ran | certified | 196.6 | 37.3 |
| 1629 | `0s0_2s1-7s1__1s1-3s0-4s0-5s1-6s1-8s1` | H3/two | never_ran | certified | 305.4 | 43.8 |
| 1673 | `0s0_2s1-8s1__1s0-3s1-4s1-5s1-6s0-7s0` | H3/two | presplit | certified | 365.6 | 44.8 |
| 1717 | `0s0_2s1-9s0__1s0-3s0-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 66.9 | 31.7 |
| 1761 | `0s0_2s1-9s0__1s1-3s1-4s0-5s1-6s0-7s0` | H3/two | presplit | certified | 103.0 | 34.0 |
| 1805 | `0s0_3s0-4s1__1s1-2s0-5s0-6s0-7s0-8s0` | H3/two | presplit | certified | 302.4 | 51.3 |
| 1849 | `0s0_3s0-5s0__1s0-2s0-4s1-6s1-7s0-8s0` | H3/two | presplit | certified | 29.9 | 22.7 |
| 1893 | `0s0_3s0-5s0__1s1-2s1-4s1-6s0-7s0-8s0` | H3/two | presplit | certified | 93.2 | 31.8 |
| 1937 | `0s0_3s0-5s1__1s1-2s0-4s1-6s1-7s1-8s0` | H3/two | timeout300 | certified | 571.6 | 57.4 |
| 1981 | `0s0_3s0-6s0__1s0-2s1-4s1-5s0-7s1-8s0` | H3/two | presplit | certified | 78.8 | 31.8 |
| 2025 | `0s0_3s0-6s1__1s0-2s0-4s0-5s1-7s1-8s0` | H3/two | timeout300 | certified | 355.6 | 45.5 |
| 2069 | `0s0_3s0-6s1__1s1-2s1-4s0-5s0-7s1-8s0` | H3/two | timeout300 | certified | 447.9 | 65.5 |
| 2113 | `0s0_3s0-7s0__1s0-2s1-4s1-5s1-6s1-8s0` | H3/two | presplit | certified | 93.7 | 36.5 |
| 2157 | `0s0_3s0-7s1__1s0-2s0-4s1-5s0-6s1-8s0` | H3/two | presplit | certified | 285.3 | 42.9 |
| 2201 | `0s0_3s0-7s1__1s1-2s1-4s0-5s1-6s1-8s0` | H3/two | presplit | certified | 267.8 | 54.9 |
| 2245 | `0s0_3s0-8s0__1s1-2s1-4s1-5s0-6s0-7s0` | H3/two | presplit | certified | 200.9 | 37.6 |
| 2289 | `0s0_3s1-4s0__1s0-2s0-5s1-6s0-7s0-8s1` | H3/two | timeout300 | certified | 361.2 | 43.4 |
| 2333 | `0s0_3s1-4s0__1s1-2s1-5s0-6s1-7s0-8s1` | H3/two | never_ran | certified | 606.7 | 67.7 |
| 2377 | `0s0_3s1-4s1__1s1-2s0-5s0-6s0-7s0-8s1` | H3/two | presplit | certified | 78.3 | 29.0 |
| 2421 | `0s0_3s1-5s0__1s0-2s0-4s1-6s1-7s0-8s1` | H3/two | presplit | certified | 361.4 | 46.6 |
| 2465 | `0s0_3s1-5s0__1s1-2s1-4s1-6s0-7s0-8s1` | H3/two | presplit | certified | 562.0 | 67.3 |
| 2509 | `0s0_3s1-5s1__1s1-2s0-4s0-6s1-7s0-8s1` | H3/two | presplit | certified | 84.9 | 29.0 |
| 2553 | `0s0_3s1-7s0__1s0-2s1-4s1-5s1-6s1-8s1` | H3/two | never_ran | certified | 355.1 | 42.0 |
| 2597 | `0s0_3s1-7s1__1s0-2s1-4s1-5s1-6s1-8s0` | H3/two | timeout300 | certified | 368.2 | 42.3 |
| 2641 | `0s0_3s1-8s0__1s0-2s1-4s1-5s1-6s1-7s0` | H3/two | presplit | certified | 233.6 | 39.9 |
| 2685 | `0s0_4s0-5s1__1s0-2s0-3s1-6s0-7s1-8s0` | H3/two | presplit | certified | 383.5 | 47.1 |
| 2729 | `0s0_4s0-5s1__1s1-2s1-3s0-6s1-7s1-8s0` | H3/two | presplit | certified | 465.1 | 50.1 |
| 2773 | `0s0_4s0-6s1__1s1-2s0-3s0-5s0-7s1-8s0` | H3/two | presplit | certified | 354.5 | 51.8 |
| 2817 | `0s0_4s0-7s0__1s0-2s0-3s1-5s1-6s1-8s0` | H3/two | presplit | certified | 56.0 | 27.2 |
| 2861 | `0s0_4s0-7s0__1s1-2s1-3s1-5s0-6s1-8s0` | H3/two | presplit | certified | 118.4 | 31.5 |
| 2905 | `0s0_4s0-7s1__1s1-2s0-3s1-5s1-6s1-8s1` | H3/two | presplit | certified | 586.4 | 51.6 |
| 2949 | `0s0_4s1-5s0__1s0-2s1-3s1-6s0-7s1-8s1` | H3/two | never_ran | certified | 531.3 | 55.9 |
| 2993 | `0s0_4s1-5s1__1s1-2s1-3s1-6s1-7s1-8s0` | H3/two | never_ran | certified | 49.4 | 25.1 |
| 3037 | `0s0_4s1-6s0__1s1-2s0-3s1-5s0-7s1-8s0` | H3/two | presplit | certified | 346.4 | 46.5 |
| 3081 | `0s0_4s1-6s1__1s0-2s1-3s0-5s1-7s1-8s0` | H3/two | presplit | certified | 89.2 | 30.7 |
| 3125 | `0s0_4s1-7s0__1s0-2s0-3s0-5s0-6s1-8s0` | H3/two | presplit | certified | 254.9 | 46.7 |
| 3169 | `0s0_4s1-7s0__1s1-2s0-3s1-5s1-6s1-8s0` | H3/two | presplit | certified | 586.4 | 55.4 |
| 3213 | `0s0_5s0-6s0__1s0-2s1-3s1-4s0-7s1-8s0` | H3/two | presplit | certified | 28.1 | 22.7 |
| 3257 | `0s0_5s0-6s1__1s0-2s0-3s0-4s1-7s1-8s0` | H3/two | presplit | certified | 373.6 | 46.6 |
| 3301 | `0s0_5s0-6s1__1s1-2s1-3s0-4s0-7s1-8s0` | H3/two | presplit | certified | 411.6 | 47.1 |
| 3345 | `0s0-1s1_4__2s0-3s1-5s1-6s1-7s1-8s1` | H6(1,1)/one | timeout300 | certified | 369.2 | 59.5 |
| 3389 | `0s0-1s1_5__2s1-3s0-4s1-6s0-7s0-8s1` | H6(1,1)/one | timeout300 | certified | 239.3 | 39.1 |
| 3433 | `0s0-2s1_4__1s1-3s0-5s0-6s1-7s0-8s1` | H6(2,1)/one | timeout300 | certified | 342.2 | 47.4 |
| 3477 | `0s0-2s1_5__1s0-3s1-4s1-6s1-7s1-8s0` | H6(2,1)/one | timeout300 | certified | 214.8 | 41.3 |
| 3521 | `0s0-2s1_6__1s0-3s0-4s1-5s1-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 255.8 | 42.7 |
| 3565 | `0s0-2s1_6__1s1-3s1-4s1-5s0-7s0-8s0` | H6(2,1)/one | timeout300 | certified | 320.8 | 44.0 |
| 3609 | `0s0-3s1_4__1s1-2s1-5s1-6s1-7s0-8s0` | H6(3,1)/one | never_ran | certified | 287.1 | 37.2 |
| 3653 | `0s0-3s1_5__1s1-2s0-4s1-6s0-7s0-8s0` | H6(3,1)/one | presplit | certified | 403.4 | 45.5 |
| 3697 | `0s0-4s0_6__1s0-2s1-3s0-5s1-7s0-8s0` | H6(4,0)/one | presplit | certified | 69.9 | 32.3 |
| 3741 | `0s0-4s1_5__1s1-2s1-3s0-6s0-7s0-8s1` | H6(4,1)/one | timeout300 | certified | 385.5 | 63.1 |
| 3785 | `0s0-5s0_6__1s1-2s0-3s0-4s1-7s1-8s1` | H6(5,0)/one | presplit | certified | 79.2 | 31.1 |
| 3829 | `0s0-5s0_7__1s0-2s1-3s0-4s0-6s1-8s1` | H6(5,0)/one | presplit | certified | 59.0 | 30.1 |
| 3873 | `0s0-5s0_7__1s1-2s1-3s1-4s1-6s1-8s1` | H6(5,0)/one | presplit | certified | 91.6 | 36.6 |
| 3917 | `0s0-5s1_1__2s1-3s1-4s1-6s0-7s0-8s1` | H6(5,1)/one | presplit | certified | 151.5 | 31.8 |
| 3961 | `0s0-5s1_2__1s1-3s0-4s0-6s1-7s0-8s1` | H6(5,1)/one | presplit | certified | 287.8 | 43.7 |
| 4005 | `0s0-5s1_6__1s1-2s1-3s0-4s0-7s1-8s0` | H6(5,1)/one | never_ran | certified | 279.9 | 37.2 |
| 4049 | `0s0-5s1_1s1-10s1__2s1-3s0-4s0-6s1-7s0-8s0` | H6(5,1)/two | never_ran | certified | 29.6 | 26.2 |
| 4093 | `0s0-5s1_2s1-3s0__1s1-4s1-6s1-7s0-8s0-9s0` | H6(5,1)/two | never_ran | certified | 43.1 | 29.4 |

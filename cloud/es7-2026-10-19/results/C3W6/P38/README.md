# C3W6 P38: shard 38 of 44 of `W6.tsv`

Task: `results/C3W6/TASK.md` at c5260b44, with V = P38, LIST = W6.tsv, j = 38, N = 44, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 05:31:44 UTC, END (start + 4.5 h − 15 min) 09:46:44 UTC.
The three lanes ran from 05:35:08 UTC and had all finished by 08:21:56 UTC, before END. No lane was killed.

## Tools (`tools.txt`)

- C3U2 tools: worktree of commit cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its example prints `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. In the sanity test, LRAT `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches.

## Run

Units: the 93 rows of `lists/W6.tsv` with row ≡ 38 (mod 44) (`units.tsv`). No records were seeded. There were 3 lanes (`lane0.sh` to `lane2.sh`), and lane k took the units at positions ≡ k (mod 3).
Each unit ran `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`.
`out.jsonl` holds the records of lane 0, then lane 1, then lane 2: 93 solve records, 0 split records.

## Result

**All 93 units were certified at cap 900.** Both checkers accepted every proof (`c VERIFIED` and `s VERIFIED UNSAT`). None timed out and none was not reached. The run produced no split records, no `unsplittable` nodes and no `recheck.jsonl`.
There was no SAT, no proof rejection, no checker killed (cake_lpr `none`) and no memory problem. Free memory never fell below about 9 GB, and the largest proof was 576 MB, deleted after checking.
No unit ended early without a certificate. 15 units were solved in under 72 s, and each of them is certified.

Solve times of the 93 certified units (s): min 29.6, Q1 110.5, median 293.1, Q3 393.8, p90 500.2, max 609.1. **45 of 93 were certified above 300 s**, so they would have timed out at the old cap.
Total solve time 7.11 h; total check time 1.14 h (per unit 21.0–70.3 s).

## Totals per stratum and per prior

| stratum | units | certified | timed out | not reached | >300 s | median solve s |
|---|---|---|---|---|---|---|
| H3/two | 76 | 76 | 0 | 0 | 39 | 315.5 |
| H6(1,1)/one | 1 | 1 | 0 | 0 | 1 | 318.4 |
| H6(2,1)/one | 4 | 4 | 0 | 0 | 4 | 361.3 |
| H6(3,1)/one | 2 | 2 | 0 | 0 | 1 | 317.4 |
| H6(4,0)/one | 2 | 2 | 0 | 0 | 0 | 52.8 |
| H6(5,0)/one | 3 | 3 | 0 | 0 | 0 | 81.5 |
| H6(5,1)/one | 3 | 3 | 0 | 0 | 0 | 189.2 |
| H6(5,1)/two | 2 | 2 | 0 | 0 | 0 | 49.5 |

| prior | units | certified | timed out | not reached | >300 s | median solve s |
|---|---|---|---|---|---|---|
| never_ran | 10 | 10 | 0 | 0 | 2 | 195.2 |
| presplit | 56 | 56 | 0 | 0 | 19 | 161.1 |
| timeout300 | 27 | 27 | 0 | 0 | 24 | 386.4 |

## Per unit

| row | node | stratum | prior | lane | status | solve s | check s |
|---|---|---|---|---|---|---|---|
| 38 | `0s0_1s0-2s0__3s0-4s1-5s1-6s0-7s0-8s1` | H3/two | presplit | 0 | certified | 32.6 | 37.6 |
| 82 | `0s0_1s0-2s1__3s0-4s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | 1 | certified | 375.5 | 67.7 |
| 126 | `0s0_1s0-2s1__3s1-4s1-5s1-6s0-7s0-8s0` | H3/two | timeout300 | 2 | certified | 419.9 | 57.0 |
| 170 | `0s0_1s0-4s1__2s0-3s0-5s1-6s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 386.4 | 54.0 |
| 214 | `0s0_1s0-4s1__2s1-3s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 393.3 | 63.6 |
| 258 | `0s0_1s0-7s0__2s0-3s0-4s1-5s0-6s0-8s1` | H3/two | timeout300 | 2 | certified | 192.5 | 55.1 |
| 302 | `0s0_1s0-7s1__2s1-3s1-4s1-5s0-6s0-8s0` | H3/two | timeout300 | 0 | certified | 271.0 | 57.2 |
| 346 | `0s0_1s1-2s0__3s1-4s0-5s1-6s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 503.8 | 63.8 |
| 390 | `0s0_1s1-4s0__2s1-3s1-5s1-6s1-7s1-8s0` | H3/two | timeout300 | 2 | certified | 379.1 | 61.8 |
| 434 | `0s0_1s1-5s0__2s1-3s1-4s1-6s1-7s1-8s1` | H3/two | timeout300 | 0 | certified | 316.2 | 41.7 |
| 478 | `0s0_1s1-5s1__2s1-3s0-4s1-6s0-7s1-8s1` | H3/two | presplit | 1 | certified | 208.2 | 57.3 |
| 522 | `0s0_1s1-7s1__2s1-3s0-4s0-5s1-6s1-8s1` | H3/two | timeout300 | 2 | certified | 389.9 | 56.2 |
| 566 | `0s0_1s1-8s0__2s0-3s1-4s0-5s0-6s1-7s1` | H3/two | presplit | 0 | certified | 146.7 | 49.3 |
| 610 | `0s0_1s1-8s0__2s1-3s1-4s1-5s1-6s1-7s1` | H3/two | presplit | 1 | certified | 205.1 | 48.9 |
| 654 | `0s0_1s1-9s1__2s0-3s0-4s1-5s1-6s1-7s1` | H3/two | never_ran | 2 | certified | 543.2 | 60.5 |
| 698 | `0s0_2s0-3s1__1s0-4s0-5s0-6s0-7s0-8s0` | H3/two | presplit | 0 | certified | 255.6 | 55.1 |
| 742 | `0s0_2s0-3s1__1s1-4s0-5s1-6s1-7s0-8s0` | H3/two | presplit | 1 | certified | 494.3 | 58.3 |
| 786 | `0s0_2s0-4s1__1s0-3s1-5s1-6s0-7s0-8s0` | H3/two | presplit | 2 | certified | 406.0 | 67.4 |
| 830 | `0s0_2s0-5s0__1s0-3s0-4s0-6s1-7s0-8s0` | H3/two | presplit | 0 | certified | 72.4 | 39.9 |
| 874 | `0s0_2s0-5s0__1s1-3s1-4s0-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 78.1 | 51.1 |
| 918 | `0s0_2s0-5s1__1s1-3s0-4s0-6s0-7s1-8s1` | H3/two | timeout300 | 2 | certified | 518.0 | 51.6 |
| 962 | `0s0_2s0-6s1__1s0-3s1-4s0-5s0-7s0-8s1` | H3/two | timeout300 | 0 | certified | 387.3 | 47.1 |
| 1006 | `0s0_2s0-6s1__1s1-3s1-4s1-5s1-7s0-8s1` | H3/two | timeout300 | 1 | certified | 474.0 | 47.6 |
| 1050 | `0s0_2s0-7s0__1s1-3s0-4s1-5s0-6s0-8s1` | H3/two | presplit | 2 | certified | 248.0 | 37.7 |
| 1094 | `0s0_2s0-7s1__1s0-3s1-4s0-5s1-6s0-8s1` | H3/two | presplit | 0 | certified | 355.0 | 46.0 |
| 1138 | `0s0_2s0-8s0__1s0-3s1-4s0-5s0-6s1-7s1` | H3/two | presplit | 1 | certified | 175.4 | 34.3 |
| 1182 | `0s0_2s0-8s0__1s1-3s1-4s1-5s1-6s1-7s1` | H3/two | presplit | 2 | certified | 140.9 | 30.5 |
| 1226 | `0s0_2s1-3s0__1s1-4s0-5s1-6s1-7s0-8s0` | H3/two | timeout300 | 0 | certified | 434.3 | 45.4 |
| 1270 | `0s0_2s1-3s1__1s0-4s1-5s1-6s0-7s0-8s0` | H3/two | presplit | 1 | certified | 52.1 | 24.0 |
| 1314 | `0s0_2s1-4s0__1s0-3s0-5s0-6s1-7s1-8s1` | H3/two | timeout300 | 2 | certified | 377.2 | 44.8 |
| 1358 | `0s0_2s1-4s0__1s1-3s1-5s0-6s1-7s1-8s0` | H3/two | timeout300 | 0 | certified | 487.5 | 49.7 |
| 1402 | `0s0_2s1-5s0__1s1-3s0-4s0-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 357.6 | 44.9 |
| 1446 | `0s0_2s1-6s0__1s0-3s0-4s1-5s1-7s1-8s0` | H3/two | presplit | 2 | certified | 365.1 | 43.0 |
| 1490 | `0s0_2s1-6s0__1s1-3s1-4s1-5s0-7s1-8s0` | H3/two | presplit | 0 | certified | 382.7 | 44.5 |
| 1534 | `0s0_2s1-6s1__1s1-3s0-4s0-5s1-7s1-8s0` | H3/two | presplit | 1 | certified | 119.5 | 33.8 |
| 1578 | `0s0_2s1-7s0__1s0-3s1-4s1-5s0-6s1-8s0` | H3/two | never_ran | 2 | certified | 201.2 | 34.1 |
| 1622 | `0s0_2s1-7s1__1s1-3s0-4s0-5s0-6s0-8s0` | H3/two | never_ran | 0 | certified | 172.0 | 34.5 |
| 1666 | `0s0_2s1-8s1__1s0-3s1-4s0-5s1-6s0-7s1` | H3/two | presplit | 1 | certified | 431.0 | 43.6 |
| 1710 | `0s0_2s1-9s0__1s0-3s0-4s0-5s0-6s0-7s1` | H3/two | presplit | 2 | certified | 110.5 | 31.0 |
| 1754 | `0s0_2s1-9s0__1s1-3s0-4s1-5s1-6s0-7s1` | H3/two | presplit | 0 | certified | 127.4 | 33.4 |
| 1798 | `0s0_3s0-4s1__1s0-2s1-5s1-6s0-7s0-8s1` | H3/two | presplit | 1 | certified | 560.7 | 54.0 |
| 1842 | `0s0_3s0-5s0__1s0-2s0-4s0-6s1-7s0-8s1` | H3/two | presplit | 2 | certified | 29.6 | 22.6 |
| 1886 | `0s0_3s0-5s0__1s1-2s1-4s0-6s0-7s0-8s1` | H3/two | presplit | 0 | certified | 64.1 | 35.9 |
| 1930 | `0s0_3s0-5s1__1s1-2s0-4s0-6s1-7s1-8s1` | H3/two | timeout300 | 1 | certified | 373.1 | 46.3 |
| 1974 | `0s0_3s0-6s0__1s0-2s1-4s0-5s0-7s1-8s1` | H3/two | presplit | 2 | certified | 122.1 | 45.3 |
| 2018 | `0s0_3s0-6s0__1s1-2s1-4s1-5s1-7s1-8s1` | H3/two | presplit | 0 | certified | 122.2 | 31.6 |
| 2062 | `0s0_3s0-6s1__1s1-2s0-4s1-5s0-7s1-8s1` | H3/two | timeout300 | 1 | certified | 609.1 | 70.3 |
| 2106 | `0s0_3s0-7s0__1s0-2s1-4s0-5s1-6s1-8s1` | H3/two | presplit | 2 | certified | 102.0 | 30.7 |
| 2150 | `0s0_3s0-7s1__1s0-2s0-4s0-5s0-6s1-8s1` | H3/two | presplit | 0 | certified | 261.7 | 40.1 |
| 2194 | `0s0_3s0-7s1__1s1-2s0-4s1-5s1-6s1-8s1` | H3/two | presplit | 1 | certified | 498.9 | 66.0 |
| 2238 | `0s0_3s0-8s0__1s1-2s1-4s0-5s0-6s0-7s1` | H3/two | presplit | 2 | certified | 222.8 | 56.0 |
| 2282 | `0s0_3s1-4s0__1s0-2s0-5s0-6s0-7s1-8s0` | H3/two | timeout300 | 0 | certified | 314.9 | 41.9 |
| 2326 | `0s0_3s1-4s0__1s1-2s0-5s1-6s1-7s1-8s0` | H3/two | timeout300 | 1 | certified | 539.0 | 53.5 |
| 2370 | `0s0_3s1-4s1__1s0-2s1-5s1-6s0-7s1-8s0` | H3/two | presplit | 2 | certified | 66.9 | 27.0 |
| 2414 | `0s0_3s1-5s0__1s0-2s0-4s0-6s1-7s1-8s0` | H3/two | presplit | 0 | certified | 333.5 | 43.7 |
| 2458 | `0s0_3s1-5s0__1s1-2s1-4s0-6s0-7s1-8s0` | H3/two | presplit | 1 | certified | 501.0 | 50.9 |
| 2502 | `0s0_3s1-5s1__1s0-2s1-4s1-6s1-7s1-8s0` | H3/two | presplit | 2 | certified | 70.0 | 45.1 |
| 2546 | `0s0_3s1-7s0__1s0-2s1-4s1-5s0-6s0-8s0` | H3/two | never_ran | 0 | certified | 286.5 | 41.9 |
| 2590 | `0s0_3s1-7s1__1s0-2s0-4s1-5s1-6s0-8s1` | H3/two | timeout300 | 1 | certified | 250.7 | 37.6 |
| 2634 | `0s0_3s1-8s0__1s0-2s1-4s0-5s1-6s1-7s1` | H3/two | presplit | 2 | certified | 380.8 | 45.5 |
| 2678 | `0s0_4s0-5s1__1s0-2s0-3s0-6s0-7s1-8s1` | H3/two | presplit | 0 | certified | 293.1 | 40.7 |
| 2722 | `0s0_4s0-5s1__1s1-2s0-3s1-6s1-7s1-8s1` | H3/two | presplit | 1 | certified | 522.0 | 48.5 |
| 2766 | `0s0_4s0-6s1__1s0-2s1-3s1-5s0-7s1-8s1` | H3/two | presplit | 2 | certified | 514.2 | 54.2 |
| 2810 | `0s0_4s0-7s0__1s0-2s0-3s0-5s1-6s1-8s1` | H3/two | presplit | 0 | certified | 60.0 | 27.2 |
| 2854 | `0s0_4s0-7s0__1s1-2s1-3s0-5s0-6s1-8s1` | H3/two | presplit | 1 | certified | 69.6 | 29.7 |
| 2898 | `0s0_4s0-7s1__1s1-2s0-3s1-5s0-6s0-8s0` | H3/two | presplit | 2 | certified | 375.7 | 47.8 |
| 2942 | `0s0_4s1-5s0__1s0-2s1-3s0-6s1-7s0-8s0` | H3/two | never_ran | 0 | certified | 440.7 | 47.1 |
| 2986 | `0s0_4s1-5s1__1s1-2s1-3s0-6s1-7s1-8s1` | H3/two | never_ran | 1 | certified | 64.8 | 28.7 |
| 3030 | `0s0_4s1-6s0__1s1-2s0-3s0-5s0-7s1-8s1` | H3/two | presplit | 2 | certified | 461.8 | 50.2 |
| 3074 | `0s0_4s1-6s1__1s0-2s0-3s1-5s1-7s1-8s1` | H3/two | presplit | 0 | certified | 82.9 | 27.8 |
| 3118 | `0s0_4s1-6s1__1s1-2s1-3s1-5s0-7s1-8s1` | H3/two | presplit | 1 | certified | 75.7 | 28.8 |
| 3162 | `0s0_4s1-7s0__1s1-2s0-3s0-5s1-6s1-8s1` | H3/two | presplit | 2 | certified | 415.2 | 44.3 |
| 3206 | `0s0_5s0-6s0__1s0-2s1-3s0-4s0-7s1-8s1` | H3/two | presplit | 0 | certified | 44.5 | 36.3 |
| 3250 | `0s0_5s0-6s0__1s1-2s1-3s1-4s1-7s1-8s1` | H3/two | presplit | 1 | certified | 110.6 | 33.6 |
| 3294 | `0s0_5s0-6s1__1s1-2s0-3s1-4s0-7s1-8s1` | H3/two | presplit | 2 | certified | 492.5 | 50.3 |
| 3338 | `0s0_5s1-6s0__1s1-2s1-3s1-4s0-7s1-8s1` | H3/two | timeout300 | 0 | certified | 472.3 | 69.2 |
| 3382 | `0s0-1s1_5__2s1-3s0-4s0-6s0-7s1-8s0` | H6(1,1)/one | timeout300 | 1 | certified | 318.4 | 59.6 |
| 3426 | `0s0-2s1_4__1s0-3s1-5s1-6s1-7s0-8s0` | H6(2,1)/one | timeout300 | 2 | certified | 375.9 | 48.3 |
| 3470 | `0s0-2s1_5__1s0-3s0-4s1-6s1-7s1-8s1` | H6(2,1)/one | timeout300 | 0 | certified | 346.7 | 46.2 |
| 3514 | `0s0-2s1_6__1s0-3s0-4s0-5s0-7s1-8s1` | H6(2,1)/one | timeout300 | 1 | certified | 394.3 | 43.0 |
| 3558 | `0s0-2s1_6__1s1-3s1-4s0-5s0-7s0-8s1` | H6(2,1)/one | timeout300 | 2 | certified | 325.2 | 41.6 |
| 3602 | `0s0-3s1_4__1s1-2s1-5s0-6s1-7s0-8s1` | H6(3,1)/one | never_ran | 0 | certified | 298.6 | 46.4 |
| 3646 | `0s0-3s1_5__1s1-2s0-4s0-6s0-7s0-8s1` | H6(3,1)/one | presplit | 1 | certified | 336.1 | 42.5 |
| 3690 | `0s0-4s0_6__1s0-2s0-3s1-5s1-7s0-8s1` | H6(4,0)/one | presplit | 2 | certified | 62.4 | 33.0 |
| 3734 | `0s0-4s0_6__1s1-2s1-3s1-5s0-7s0-8s1` | H6(4,0)/one | presplit | 0 | certified | 43.3 | 21.0 |
| 3778 | `0s0-5s0_6__1s1-2s0-3s0-4s0-7s0-8s0` | H6(5,0)/one | presplit | 1 | certified | 81.5 | 33.1 |
| 3822 | `0s0-5s0_7__1s0-2s0-3s1-4s1-6s0-8s0` | H6(5,0)/one | presplit | 2 | certified | 93.9 | 38.1 |
| 3866 | `0s0-5s0_7__1s1-2s1-3s1-4s0-6s0-8s0` | H6(5,0)/one | presplit | 0 | certified | 63.6 | 28.1 |
| 3910 | `0s0-5s1_1__2s1-3s1-4s0-6s0-7s1-8s0` | H6(5,1)/one | presplit | 1 | certified | 226.7 | 37.4 |
| 3954 | `0s0-5s1_2__1s0-3s1-4s1-6s1-7s1-8s0` | H6(5,1)/one | presplit | 2 | certified | 137.5 | 34.1 |
| 3998 | `0s0-5s1_6__1s1-2s0-3s1-4s0-7s1-8s1` | H6(5,1)/one | never_ran | 0 | certified | 189.2 | 37.3 |
| 4042 | `0s0-5s1_1s1-10s1__2s0-3s1-4s1-6s1-7s0-8s1` | H6(5,1)/two | never_ran | 1 | certified | 51.7 | 28.1 |
| 4086 | `0s0-5s1_2s1-3s0__1s1-4s1-6s0-7s0-8s0-9s1` | H6(5,1)/two | never_ran | 2 | certified | 47.4 | 29.9 |

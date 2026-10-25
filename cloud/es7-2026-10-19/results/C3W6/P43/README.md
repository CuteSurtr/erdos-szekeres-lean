# C3W6 P43: shard 43 of 44 of W6.tsv, cap 900, 3 lanes

Task: `results/C3W6/TASK.md` at c5260b44 with V = P43, LIST = W6.tsv, j = 43, N = 44, H = 4.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:25 UTC, lanes started 05:35:38, END 09:46:25 UTC (lanes killed by process group at END).

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at /opt/c3u2, `results/C3U2/tools`, unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity test on {1},{-1}: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…dd6da (matches).

## Run

93 units (`units.tsv`, rows ≡ 43 mod 44), no seeding. Lane k took positions ≡ k (mod 3): `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02` (`lane0.sh`–`lane2.sh`). `out.jsonl` = records of lane 0, 1, 2 in that order. A timed-out six-bit cube got its layer split record (51 children each, unsolved), as intended.

No SAT answer, no proof rejection, no record with cake_lpr `none` (no checker was running at END: the three killed units were in CaDiCaL), no unit that ended in under 72 s without a certificate, no memory problem (used memory stayed ≤ 6 GB, disk ≥ 26 GB free), no unsplittable node. `recheck.jsonl` not needed.

The three units killed at END are listed as "killed at END" (no record); they are open as before.

## Per unit

| row | node | stratum | prior | result | solve s / check s |
|---|---|---|---|---|---|
| 43 | 0s0_1s0-2s0__3s0-4s1-5s1-6s1-7s1-8s0 | H3/two | presplit | certified | 60.1 / 54.6 |
| 87 | 0s0_1s0-2s1__3s0-4s1-5s0-6s0-7s0-8s1 | H3/two | timeout300 | certified | 692.2 / 103.0 |
| 131 | 0s0_1s0-2s1__3s1-4s1-5s1-6s1-7s0-8s1 | H3/two | timeout300 | certified | 563.4 / 93.6 |
| 175 | 0s0_1s0-4s1__2s0-3s1-5s0-6s1-7s1-8s0 | H3/two | timeout300 | certified | 773.4 / 91.6 |
| 219 | 0s0_1s0-5s1__2s0-3s1-4s1-6s1-7s0-8s1 | H3/two | timeout300 | certified | 739.1 / 92.5 |
| 263 | 0s0_1s0-7s0__2s0-3s0-4s1-5s1-6s1-8s0 | H3/two | timeout300 | certified | 367.0 / 78.2 |
| 307 | 0s0_1s0-7s1__2s1-3s1-4s1-5s1-6s0-8s1 | H3/two | timeout300 | certified | 719.4 / 96.3 |
| 351 | 0s0_1s1-2s0__3s1-4s1-5s0-6s0-7s0-8s0 | H3/two | timeout300 | certified | 700.7 / 96.1 |
| 395 | 0s0_1s1-5s0__2s0-3s0-4s1-6s1-7s0-8s0 | H3/two | timeout300 | certified | 649.9 / 92.9 |
| 439 | 0s0_1s1-5s1__2s0-3s0-4s0-6s1-7s0-8s0 | H3/two | presplit | certified | 206.0 / 75.2 |
| 483 | 0s0_1s1-5s1__2s1-3s1-4s0-6s0-7s0-8s0 | H3/two | presplit | certified | 421.2 / 79.6 |
| 527 | 0s0_1s1-7s1__2s1-3s0-4s1-5s1-6s0-8s0 | H3/two | timeout300 | certified | 797.1 / 87.4 |
| 571 | 0s0_1s1-8s0__2s0-3s1-4s1-5s0-6s0-7s0 | H3/two | presplit | certified | 136.6 / 70.9 |
| 615 | 0s0_1s1-8s1__2s0-3s1-4s1-5s0-6s0-7s1 | H3/two | timeout300 | certified | 892.3 / 98.5 |
| 659 | 0s0_1s1-9s1__2s0-3s1-4s1-5s0-6s0-7s1 | H3/two | never_ran | certified | 815.5 / 96.4 |
| 703 | 0s0_2s0-3s1__1s0-4s0-5s0-6s1-7s0-8s1 | H3/two | presplit | certified | 646.2 / 88.1 |
| 747 | 0s0_2s0-3s1__1s1-4s1-5s0-6s0-7s0-8s1 | H3/two | presplit | certified | 876.2 / 98.7 |
| 791 | 0s0_2s0-4s1__1s0-3s1-5s1-6s1-7s0-8s1 | H3/two | presplit | timed out at 900 | solve 900.2; split: 51 children |
| 835 | 0s0_2s0-5s0__1s0-3s0-4s1-6s0-7s0-8s1 | H3/two | presplit | certified | 74.7 / 50.6 |
| 879 | 0s0_2s0-5s0__1s1-3s1-4s0-6s1-7s0-8s1 | H3/two | presplit | certified | 131.5 / 61.7 |
| 923 | 0s0_2s0-5s1__1s1-3s0-4s1-6s0-7s0-8s0 | H3/two | timeout300 | certified | 651.3 / 82.7 |
| 967 | 0s0_2s0-6s1__1s0-3s1-4s0-5s1-7s1-8s0 | H3/two | timeout300 | certified | 775.4 / 89.8 |
| 1011 | 0s0_2s0-7s0__1s0-3s0-4s0-5s0-6s1-8s0 | H3/two | presplit | certified | 194.9 / 62.5 |
| 1055 | 0s0_2s0-7s0__1s1-3s0-4s1-5s1-6s1-8s0 | H3/two | presplit | certified | 283.0 / 70.8 |
| 1099 | 0s0_2s0-7s1__1s0-3s1-4s1-5s0-6s1-8s0 | H3/two | presplit | certified | 616.6 / 83.8 |
| 1143 | 0s0_2s0-8s0__1s0-3s1-4s1-5s0-6s0-7s0 | H3/two | presplit | certified | 334.8 / 65.3 |
| 1187 | 0s0_2s1-3s0__1s0-4s0-5s0-6s1-7s0-8s1 | H3/two | timeout300 | certified | 783.8 / 88.5 |
| 1231 | 0s0_2s1-3s0__1s1-4s1-5s0-6s0-7s0-8s1 | H3/two | timeout300 | timed out at 900 | solve 900.2; split: 51 children |
| 1275 | 0s0_2s1-3s1__1s0-4s1-5s1-6s1-7s0-8s1 | H3/two | presplit | certified | 154.0 / 57.9 |
| 1319 | 0s0_2s1-4s0__1s0-3s0-5s1-6s1-7s0-8s0 | H3/two | timeout300 | certified | 796.2 / 109.8 |
| 1363 | 0s0_2s1-4s0__1s1-3s1-5s1-6s0-7s1-8s1 | H3/two | timeout300 | timed out at 900 | solve 900.6; split: 51 children |
| 1407 | 0s0_2s1-5s0__1s1-3s0-4s0-6s1-7s1-8s1 | H3/two | presplit | certified | 779.1 / 77.8 |
| 1451 | 0s0_2s1-6s0__1s0-3s1-4s0-5s0-7s1-8s1 | H3/two | presplit | certified | 408.6 / 76.5 |
| 1495 | 0s0_2s1-6s0__1s1-3s1-4s1-5s1-7s1-8s1 | H3/two | presplit | certified | 762.0 / 75.0 |
| 1539 | 0s0_2s1-6s1__1s1-3s0-4s1-5s0-7s1-8s1 | H3/two | presplit | certified | 288.8 / 61.9 |
| 1583 | 0s0_2s1-7s0__1s0-3s1-4s1-5s1-6s1-8s1 | H3/two | never_ran | certified | 471.0 / 63.6 |
| 1627 | 0s0_2s1-7s1__1s1-3s0-4s0-5s1-6s0-8s1 | H3/two | never_ran | certified | 430.6 / 65.0 |
| 1671 | 0s0_2s1-8s1__1s0-3s1-4s1-5s0-6s1-7s0 | H3/two | presplit | timed out at 900 | solve 900.1; split: 51 children |
| 1715 | 0s0_2s1-9s0__1s0-3s0-4s0-5s1-6s1-7s0 | H3/two | presplit | certified | 186.4 / 55.0 |
| 1759 | 0s0_2s1-9s0__1s1-3s1-4s0-5s0-6s1-7s0 | H3/two | presplit | certified | 209.5 / 53.1 |
| 1803 | 0s0_3s0-4s1__1s0-2s1-5s1-6s1-7s1-8s0 | H3/two | presplit | timed out at 900 | solve 900.1; split: 51 children |
| 1847 | 0s0_3s0-5s0__1s0-2s0-4s1-6s0-7s1-8s0 | H3/two | presplit | certified | 57.4 / 41.1 |
| 1891 | 0s0_3s0-5s0__1s1-2s1-4s0-6s1-7s1-8s0 | H3/two | presplit | certified | 160.0 / 55.6 |
| 1935 | 0s0_3s0-5s1__1s1-2s0-4s1-6s1-7s0-8s0 | H3/two | timeout300 | certified | 843.8 / 99.9 |
| 1979 | 0s0_3s0-6s0__1s0-2s1-4s1-5s0-7s0-8s0 | H3/two | presplit | certified | 128.3 / 84.7 |
| 2023 | 0s0_3s0-6s1__1s0-2s0-4s0-5s1-7s0-8s0 | H3/two | timeout300 | certified | 564.2 / 80.4 |
| 2067 | 0s0_3s0-6s1__1s1-2s1-4s0-5s0-7s0-8s0 | H3/two | timeout300 | certified | 701.9 / 77.6 |
| 2111 | 0s0_3s0-7s0__1s0-2s1-4s1-5s1-6s0-8s0 | H3/two | presplit | certified | 193.8 / 52.8 |
| 2155 | 0s0_3s0-7s1__1s0-2s0-4s1-5s0-6s0-8s0 | H3/two | presplit | certified | 611.9 / 70.8 |
| 2199 | 0s0_3s0-7s1__1s1-2s1-4s0-5s1-6s0-8s0 | H3/two | presplit | certified | 645.7 / 100.6 |
| 2243 | 0s0_3s0-8s0__1s1-2s1-4s0-5s1-6s1-7s0 | H3/two | presplit | certified | 368.3 / 93.6 |
| 2287 | 0s0_3s1-4s0__1s0-2s0-5s0-6s1-7s1-8s1 | H3/two | timeout300 | certified | 714.5 / 75.6 |
| 2331 | 0s0_3s1-4s0__1s1-2s1-5s0-6s0-7s1-8s1 | H3/two | never_ran | timed out at 900 | solve 900.2; split: 51 children |
| 2375 | 0s0_3s1-4s1__1s0-2s1-5s1-6s1-7s1-8s1 | H3/two | presplit | certified | 112.2 / 58.1 |
| 2419 | 0s0_3s1-5s0__1s0-2s0-4s1-6s0-7s1-8s1 | H3/two | presplit | certified | 863.7 / 76.4 |
| 2463 | 0s0_3s1-5s0__1s1-2s1-4s0-6s1-7s1-8s1 | H3/two | presplit | timed out at 900 | solve 900.1; split: 51 children |
| 2507 | 0s0_3s1-5s1__1s1-2s0-4s0-6s0-7s1-8s1 | H3/two | presplit | certified | 168.8 / 51.5 |
| 2551 | 0s0_3s1-7s0__1s0-2s1-4s1-5s1-6s0-8s1 | H3/two | never_ran | certified | 814.9 / 81.3 |
| 2595 | 0s0_3s1-7s1__1s0-2s1-4s1-5s1-6s0-8s0 | H3/two | timeout300 | certified | 649.3 / 93.5 |
| 2639 | 0s0_3s1-8s0__1s0-2s1-4s1-5s1-6s0-7s0 | H3/two | presplit | certified | 431.2 / 63.7 |
| 2683 | 0s0_4s0-5s1__1s0-2s0-3s1-6s0-7s0-8s0 | H3/two | presplit | certified | 680.9 / 85.7 |
| 2727 | 0s0_4s0-5s1__1s1-2s1-3s0-6s1-7s0-8s0 | H3/two | presplit | timed out at 900 | solve 900.2; split: 51 children |
| 2771 | 0s0_4s0-6s1__1s1-2s0-3s0-5s0-7s0-8s0 | H3/two | presplit | certified | 555.0 / 73.5 |
| 2815 | 0s0_4s0-7s0__1s0-2s0-3s1-5s1-6s0-8s0 | H3/two | presplit | certified | 125.6 / 56.6 |
| 2859 | 0s0_4s0-7s0__1s1-2s1-3s1-5s0-6s0-8s0 | H3/two | presplit | killed at END |  |
| 2903 | 0s0_4s0-7s1__1s1-2s0-3s1-5s1-6s0-8s1 | H3/two | presplit | timed out at 900 | solve 900.2; split: 51 children |
| 2947 | 0s0_4s1-5s0__1s0-2s1-3s1-6s0-7s0-8s1 | H3/two | never_ran | timed out at 900 | solve 900.2; split: 51 children |
| 2991 | 0s0_4s1-5s1__1s1-2s1-3s1-6s1-7s0-8s0 | H3/two | never_ran | not reached |  |
| 3035 | 0s0_4s1-6s0__1s1-2s0-3s1-5s0-7s0-8s0 | H3/two | presplit | certified | 778.8 / 84.0 |
| 3079 | 0s0_4s1-6s1__1s0-2s1-3s0-5s1-7s0-8s0 | H3/two | presplit | certified | 159.9 / 53.6 |
| 3123 | 0s0_4s1-7s0__1s0-2s0-3s0-5s0-6s0-8s0 | H3/two | presplit | not reached |  |
| 3167 | 0s0_4s1-7s0__1s1-2s0-3s1-5s1-6s0-8s0 | H3/two | presplit | certified | 851.1 / 86.7 |
| 3211 | 0s0_5s0-6s0__1s0-2s1-3s1-4s0-7s0-8s0 | H3/two | presplit | certified | 46.6 / 30.4 |
| 3255 | 0s0_5s0-6s1__1s0-2s0-3s0-4s1-7s0-8s0 | H3/two | presplit | not reached |  |
| 3299 | 0s0_5s0-6s1__1s1-2s1-3s0-4s0-7s0-8s0 | H3/two | presplit | certified | 648.8 / 74.8 |
| 3343 | 0s0-1s1_4__2s0-3s1-5s1-6s0-7s1-8s0 | H6(1,1)/one | timeout300 | killed at END |  |
| 3387 | 0s0-1s1_5__2s1-3s0-4s0-6s1-7s1-8s1 | H6(1,1)/one | timeout300 | not reached |  |
| 3431 | 0s0-2s1_4__1s1-3s0-5s0-6s0-7s1-8s1 | H6(2,1)/one | timeout300 | killed at END |  |
| 3475 | 0s0-2s1_5__1s0-3s1-4s1-6s1-7s0-8s0 | H6(2,1)/one | timeout300 | not reached |  |
| 3519 | 0s0-2s1_6__1s0-3s0-4s1-5s0-7s0-8s0 | H6(2,1)/one | timeout300 | not reached |  |
| 3563 | 0s0-2s1_6__1s1-3s1-4s0-5s1-7s1-8s0 | H6(2,1)/one | timeout300 | not reached |  |
| 3607 | 0s0-3s1_4__1s1-2s1-5s1-6s0-7s1-8s0 | H6(3,1)/one | never_ran | not reached |  |
| 3651 | 0s0-3s1_5__1s1-2s0-4s0-6s1-7s1-8s0 | H6(3,1)/one | presplit | not reached |  |
| 3695 | 0s0-4s0_6__1s0-2s1-3s0-5s0-7s1-8s0 | H6(4,0)/one | presplit | not reached |  |
| 3739 | 0s0-4s0_6__1s1-2s1-3s1-5s1-7s1-8s0 | H6(4,0)/one | presplit | not reached |  |
| 3783 | 0s0-5s0_6__1s1-2s0-3s0-4s1-7s0-8s1 | H6(5,0)/one | presplit | not reached |  |
| 3827 | 0s0-5s0_7__1s0-2s1-3s0-4s0-6s0-8s1 | H6(5,0)/one | presplit | not reached |  |
| 3871 | 0s0-5s0_7__1s1-2s1-3s1-4s1-6s0-8s1 | H6(5,0)/one | presplit | not reached |  |
| 3915 | 0s0-5s1_1__2s1-3s1-4s0-6s1-7s1-8s1 | H6(5,1)/one | presplit | not reached |  |
| 3959 | 0s0-5s1_2__1s1-3s0-4s0-6s0-7s1-8s1 | H6(5,1)/one | presplit | not reached |  |
| 4003 | 0s0-5s1_6__1s1-2s1-3s0-4s0-7s0-8s0 | H6(5,1)/one | never_ran | not reached |  |
| 4047 | 0s0-5s1_1s1-10s1__2s1-3s0-4s0-6s0-7s1-8s0 | H6(5,1)/two | never_ran | not reached |  |
| 4091 | 0s0-5s1_2s1-3s0__1s1-4s1-6s0-7s1-8s1-9s0 | H6(5,1)/two | never_ran | not reached |  |

| group | value | certified | timed out at 900 | not reached / killed |
|---|---|---|---|---|
| all | all | 61 | 10 | 22 |
| prior | never_ran | 4 | 2 | 5 |
| prior | presplit | 38 | 6 | 11 |
| prior | timeout300 | 19 | 2 | 6 |
| stratum | H3/two | 61 | 10 | 4 |
| stratum | H6(1,1)/one | 0 | 0 | 2 |
| stratum | H6(2,1)/one | 0 | 0 | 4 |
| stratum | H6(3,1)/one | 0 | 0 | 2 |
| stratum | H6(4,0)/one | 0 | 0 | 2 |
| stratum | H6(5,0)/one | 0 | 0 | 3 |
| stratum | H6(5,1)/one | 0 | 0 | 3 |
| stratum | H6(5,1)/two | 0 | 0 | 2 |

Certified solve times (n=61): min 46.6, Q1 194.4, median 564.2, Q3 750.5, p90 814.9, max 892.3; above 300 s: 41; under 72 s: 3
Uncertified solves under 72 s: none

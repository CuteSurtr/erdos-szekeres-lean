# C3W7 / Q30: nine-bit σ-cubes of the H3/one roots at cap 900

**Result: 2 of 53 units certified (both checkers), 46 timed out at 900 s, 5 not reached (3 started and killed at END, 2 never started). No SAT. No proof rejection, no checker `none`, no unit that ended early (every non-certified solve ran the full 900 s), no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Task `results/C3W7/TASK.md` at 39bb1bac; V = Q30, LIST = W7.tsv, j = 30, N = 36, H = 4.5. Start 10:46:34 UTC, END 15:01:34 UTC; the lanes started at 10:49:14 and were killed (whole process groups) at 15:01:4x.

- Tools (`tools.txt`): C3U2 tools from a worktree of cad4e050 at `/opt/c3u2`, unmodified. CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (its bundled example gives `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity test: the LRAT `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both. `compose.py` was not run.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Units: the rows of `lists/W7.tsv` with row ≡ 30 (mod 36), giving 53 units (`units.tsv`). 3 lanes (`lane.sh`, `lane0.sh`–`lane2.sh`), each started with `setsid nohup`. Lane k runs positions ≡ k (mod 3) with `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. No records were seeded.
- `out.jsonl` holds lane 0, then lane 1, then lane 2: 48 solve records (2 certified, 46 UNKNOWN at 900 s) and 46 layer-split records (45 children each, all unsolved and so open, as the task intends). There is no `recheck.jsonl` because no re-check was needed.

Because 36 ≡ 4 (mod 8) and each parent has 8 consecutive rows, every unit on this machine is child index 6 or 2 of its parent. So every unit's last three bits are `8s?-9s1-10s0`, and each parent six-bit cube has exactly one unit here.

## Per unit

| pos | row | unit | parent six-bit cube | lane | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0 | 30 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1 | 66 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 2 | 102 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 3 | 138 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 4 | 174 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 5 | 210 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0` | 2 | timed out at 900 (layer split, 45 children) | 900.2 | – |
| 6 | 246 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 7 | 282 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 8 | 318 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 9 | 354 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 10 | 390 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 11 | 426 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 12 | 462 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1` | 0 | timed out at 900 (layer split, 45 children) | 900.2 | – |
| 13 | 498 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 14 | 534 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 15 | 570 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 16 | 606 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 17 | 642 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0` | 2 | certified | 861.7 | 100.1 |
| 18 | 678 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 19 | 714 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 20 | 750 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 21 | 786 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 22 | 822 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 23 | 858 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 24 | 894 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 25 | 930 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 26 | 966 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 27 | 1002 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 28 | 1038 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 29 | 1074 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 30 | 1110 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 31 | 1146 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 32 | 1182 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1` | 2 | timed out at 900 (layer split, 45 children) | 900.2 | – |
| 33 | 1218 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 34 | 1254 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 35 | 1290 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 36 | 1326 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 37 | 1362 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0` | 1 | timed out at 900 (layer split, 45 children) | 900.7 | – |
| 38 | 1398 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 39 | 1434 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 40 | 1470 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 41 | 1506 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0` | 2 | timed out at 900 (layer split, 45 children) | 900.2 | – |
| 42 | 1542 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0-8s1-9s1-10s0` | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0` | 0 | certified | 827.9 | 107.6 |
| 43 | 1578 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1-8s0-9s1-10s0` | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 44 | 1614 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1-8s1-9s1-10s0` | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 45 | 1650 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0-8s0-9s1-10s0` | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 46 | 1686 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0-8s1-9s1-10s0` | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 47 | 1722 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1-8s0-9s1-10s0` | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 48 | 1758 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s1-9s1-10s0` | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1` | 0 | not reached (started, killed at END) | – | – |
| 49 | 1794 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s0-9s1-10s0` | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0` | 1 | not reached (started, killed at END) | – | – |
| 50 | 1830 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s1-9s1-10s0` | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0` | 2 | not reached (started, killed at END) | – | – |
| 51 | 1866 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s0-9s1-10s0` | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1` | 0 | not reached | – | – |
| 52 | 1902 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s1-9s1-10s0` | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1` | 1 | not reached | – | – |

## Totals per root

| root | units | certified | timed out at 900 | not reached |
|---|---|---|---|---|
| 0s0_1 | 14 | 0 | 14 | 0 |
| 0s0_2 | 14 | 1 | 13 | 0 |
| 0s0_3 | 14 | 0 | 14 | 0 |
| 0s0_4 | 11 | 1 | 5 | 5 |
| **total** | **53** | **2** | **46** | **5** |

## Per parent six-bit cube

There are 53 parents with one unit each. On this machine, all units were certified for 2 parents (their other 7 nine-bit cubes are on other machines):
- `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0` (unit `…-8s0-9s1-10s0`, 861.7 s)
- `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0` (unit `…-8s1-9s1-10s0`, 827.9 s)

The units of 46 parents timed out, and the units of 5 parents were not reached (see the table).

## Solve times of the certified units

There are only 2: 827.9 s and 861.7 s, so min 827.9 and max 861.7; quartiles, median and p90 mean nothing with n = 2. Both were certified above 300 s, and both above 800 s. Check times were 107.6 s and 100.1 s, with cake_lpr `s VERIFIED UNSAT` and lrat-check `c VERIFIED` on both.

## Notes

- The C3H1/X1 pilot (one 0s0_5 parent, 450–662 s) does not carry over to these units. Here 46 of 48 solved units ran past 900 s, with 3 jobs on 4 cores just as in X1. The two that closed needed 828–862 s. For the 9s1-10s0 children of roots 0s0_1 to 0s0_4, cap 900 is well below the typical solve time.
- Memory: about 2 GB used and at least 13 GB available at every sample. No memory problem.
- Unit timeouts were not killed early. Every UNKNOWN record has solve_s 900.1–900.7.
- 3 units were killed at END mid-solve (started at 14:49:50–14:50:53): `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s1-9s1-10s0`, `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s0-9s1-10s0` and `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s1-9s1-10s0`. They have no records. 2 units were never started: `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s0-9s1-10s0` and `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s1-9s1-10s0`.

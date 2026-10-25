# C3W7 / Q02: nine-bit σ-cubes of the H3/one roots, shard 2 of 36 of W7.tsv

**38 of my 54 units are certified, 13 timed out at 900 s, and 3 were running when END came and were killed. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Ran 10:49–15:01 UTC on 2026-10-25 (start 10:46:21, END = start + 4.5 h − 15 min = 15:01:21). Task: `results/C3W7/TASK.md` at 39bb1bac (unchanged at HEAD).

- Tools: worktree of cad4e050 at `/opt/c3u2`, `TOOLS=/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8b750 (bundled example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf9 + E2 patch. Sanity: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).
- Units: rows of `lists/W7.tsv` with row ≡ 2 (mod 36): 54 units (`units.tsv`), no seeding. Three lanes (`lane0.sh`–`lane2.sh` exec `lane.sh K`), lane k takes positions ≡ k (mod 3). Per unit: `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
- `out.jsonl` = lane 0, then 1, then 2 records. Each timed-out unit has its layer-split record there, and its children were left unsolved (in `open_frontier`), as intended. No `recheck.jsonl`, because there was nothing to re-check.

## Per unit

| row | unit (nine-bit cube) | result | solve s | check s |
|---|---|---|---|---|
| 2 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 426.0 | 93.2 |
| 38 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | certified | 600.2 | 108.6 |
| 74 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 684.8 | 95.9 |
| 110 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 146 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | certified | 682.1 | 95.7 |
| 182 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 218 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | certified | 899.6 | 105.2 |
| 254 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | certified | 744.7 | 105.8 |
| 290 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | certified | 666.9 | 103.7 |
| 326 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | certified | 806.0 | 110.3 |
| 362 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | certified | 823.2 | 111.3 |
| 398 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 434 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | certified | 668.1 | 93.0 |
| 470 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | certified | 881.0 | 101.0 |
| 506 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | certified | 688.8 | 97.2 |
| 542 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | certified | 684.4 | 105.2 |
| 578 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 590.0 | 102.1 |
| 614 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | certified | 825.2 | 104.9 |
| 650 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 698.9 | 96.9 |
| 686 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 722 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | certified | 799.9 | 101.4 |
| 758 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | certified | 755.6 | 101.2 |
| 794 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 830 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 866 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | certified | 786.4 | 110.7 |
| 902 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | certified | 805.7 | 108.3 |
| 938 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 974 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1010 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | certified | 866.5 | 101.7 |
| 1046 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | certified | 683.5 | 84.6 |
| 1082 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | certified | 820.4 | 108.9 |
| 1118 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | certified | 862.8 | 94.6 |
| 1154 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 638.4 | 108.0 |
| 1190 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1226 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 882.1 | 108.7 |
| 1262 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1298 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | certified | 793.0 | 98.6 |
| 1334 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | certified | 865.7 | 101.6 |
| 1370 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1406 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | certified | 698.0 | 83.6 |
| 1442 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | certified | 787.8 | 95.3 |
| 1478 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1514 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | certified | 890.9 | 107.2 |
| 1550 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1-8s1-9s1-10s0` | certified | 670.2 | 82.0 |
| 1586 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0-8s0-9s1-10s0` | certified | 783.8 | 111.9 |
| 1622 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0-8s1-9s1-10s0` | certified | 833.7 | 101.6 |
| 1658 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1-8s0-9s1-10s0` | certified | 865.4 | 92.9 |
| 1694 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1-8s1-9s1-10s0` | certified | 802.5 | 106.3 |
| 1730 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 689.6 | 84.4 |
| 1766 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1802 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 593.9 | 78.7 |
| 1838 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1-8s1-9s1-10s0` | killed at END (running) |  |  |
| 1874 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0-8s0-9s1-10s0` | killed at END (running) |  |  |
| 1910 | `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s1-9s1-10s0` | killed at END (running) |  |  |

Units 1838, 1874 and 1910 were running at END and were killed with no record. (Unit 1874 had started at 15:00:51, 30 s before END.) They count as not finished.

## Per root

| root | units here | certified | timed out | not reached / killed |
|---|---|---|---|---|
| `0s0_1` | 15 | 12 | 3 | 0 |
| `0s0_2` | 14 | 9 | 5 | 0 |
| `0s0_3` | 14 | 10 | 4 | 0 |
| `0s0_4` | 11 | 7 | 1 | 3 |

## Per parent six-bit cube

With N = 36, each parent has at most one unit on this machine, so "all units here certified" just means that one unit was certified.

| parent six-bit cube | units here | certified | timed out | not reached / killed |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 0 | 1 |

Parents all of whose units here were certified (38): `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0`, `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0`, `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1`, `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0`, `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1`, `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1`, `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0`, `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0`, `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1`, `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0`, `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0`, `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1`, `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1`, `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0`, `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0`, `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1`, `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0`, `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0`, `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0`, `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0`, `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0`, `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0`, `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1`, `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1`, `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0`, `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1`, `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0`, `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0`, `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1`, `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0`, `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1`, `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1`, `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0`, `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0`, `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1`, `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1`, `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0`, `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1`


## Solve times of the certified units

Certified: 38; solve s min 426.0, Q1 683.1, median 785.1, Q3 827.3, p90 881.1, max 899.6; above 300 s: 38. Totals over the certified units: 28546 s solve, 3802 s check (wall-clock with 3 lanes on 4 cores).

## SAT / rejections / anomalies

- SAT: none.
- PROOF NOT ACCEPTED: none. Every certified record has `c VERIFIED` and `s VERIFIED UNSAT`, and no record has cake_lpr `none`.
- No unit ended in under 72 s without a certificate. No memory problem: at least 9 GB was always available.
- 13 timed-out units, each with a layer-split record whose children are unsolved: open.
- 3 units were killed at END: not finished.

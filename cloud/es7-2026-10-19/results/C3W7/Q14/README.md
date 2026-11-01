# C3W7 Q14: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv, shard 14 of 36)

Task: `results/C3W7/TASK.md` at 39bb1bac, V = Q14, LIST = W7.tsv, j = 14, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:36 UTC on 2026-10-25, lanes started 10:48:59, END 15:01:36 UTC.

**No SAT answer, no proof rejection, no memory problem, no unit that ended early** (every non-certified solve ran the full 900 s).

## Tools and base CNF (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified; `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`.
  Sanity: on {1},{-1} the LRAT `3 0 0` is rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

## Run

53 units (`units.tsv`: rows of W7.tsv with row ≡ 14 mod 36), no seeded records, 3 lanes (`lane0.sh`–`lane2.sh`,
lane k = positions ≡ k mod 3), each unit `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3
--sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. `out.jsonl` = lane 0, 1, 2 records (35 certified solve records,
15 timed-out solve records, 15 layer-split records with 45 children each, children unsolved as intended). No `recheck.jsonl`
(no re-check was needed: every certified record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`).
Lane 2 finished all 17 of its units at 14:59:05. At END lanes 0 and 1 were killed (process groups) while solving
(not checking), so no checker was killed and there is no `none` record.

## Result

- **35 certified**, **15 timed out at 900** (layer split recorded, open), **2 killed at END while solving** (no record),
  **1 not reached**.
- Solve time of the 35 certified units: min 554.9 s, Q1 719.9, median 812.2, Q3 854.4, p90 892.7, max 896.9 s;
  all 35 were certified above 300 s. Total solve 27133.0 s, check 3712.5 s (80.5–121.7 s per check).

## Per unit

| pos | row | lane | unit | result | solve s / check s |
|---|---|---|---|---|---|
| 0 | 14 | 0 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | certified | 592.4 / 101.9 |
| 1 | 50 | 1 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | certified | 790.5 / 121.0 |
| 2 | 86 | 2 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | certified | 812.2 / 119.3 |
| 3 | 122 | 0 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | certified | 851.3 / 119.7 |
| 4 | 158 | 1 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | certified | 787.9 / 105.0 |
| 5 | 194 | 2 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 665.2 / 106.2 |
| 6 | 230 | 0 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | certified | 854.4 / 114.2 |
| 7 | 266 | 1 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 734.4 / 108.9 |
| 8 | 302 | 2 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 9 | 338 | 0 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | certified | 821.2 / 121.3 |
| 10 | 374 | 1 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 11 | 410 | 2 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 / - |
| 12 | 446 | 0 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | certified | 836.9 / 113.9 |
| 13 | 482 | 1 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | certified | 751.7 / 105.8 |
| 14 | 518 | 2 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | certified | 580.2 / 92.2 |
| 15 | 554 | 0 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | certified | 730.3 / 99.5 |
| 16 | 590 | 1 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 17 | 626 | 2 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | certified | 895.6 / 121.7 |
| 18 | 662 | 0 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | certified | 847.0 / 116.4 |
| 19 | 698 | 1 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | certified | 868.5 / 106.8 |
| 20 | 734 | 2 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | certified | 854.6 / 111.7 |
| 21 | 770 | 0 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 554.9 / 92.8 |
| 22 | 806 | 1 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | certified | 826.6 / 100.8 |
| 23 | 842 | 2 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 850.8 / 110.0 |
| 24 | 878 | 0 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 25 | 914 | 1 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | certified | 783.5 / 101.7 |
| 26 | 950 | 2 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 27 | 986 | 0 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | certified | 892.1 / 109.9 |
| 28 | 1022 | 1 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | certified | 829.8 / 95.0 |
| 29 | 1058 | 2 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | certified | 583.2 / 96.8 |
| 30 | 1094 | 0 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | certified | 802.6 / 108.4 |
| 31 | 1130 | 1 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 / - |
| 32 | 1166 | 2 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | certified | 893.5 / 116.9 |
| 33 | 1202 | 0 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | certified | 877.9 / 113.8 |
| 34 | 1238 | 1 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 35 | 1274 | 2 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | certified | 821.5 / 107.7 |
| 36 | 1310 | 0 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 37 | 1346 | 1 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 719.9 / 94.5 |
| 38 | 1382 | 2 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 39 | 1418 | 0 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 / - |
| 40 | 1454 | 1 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.2 / - |
| 41 | 1490 | 2 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | certified | 862.7 / 108.0 |
| 42 | 1526 | 0 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | certified | 896.9 / 99.8 |
| 43 | 1562 | 1 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s0-9s1-10s0` | certified | 605.7 / 91.0 |
| 44 | 1598 | 2 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1-8s1-9s1-10s0` | certified | 578.0 / 80.5 |
| 45 | 1634 | 0 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s0-9s1-10s0` | certified | 788.7 / 105.4 |
| 46 | 1670 | 1 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0-8s1-9s1-10s0` | certified | 690.4 / 94.0 |
| 47 | 1706 | 2 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 | 900.0 / - |
| 48 | 1742 | 0 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s1-9s1-10s0` | killed at END (no record) | - |
| 49 | 1778 | 1 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 | 900.1 / - |
| 50 | 1814 | 2 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 / - |
| 51 | 1850 | 0 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s0-9s1-10s0` | not reached | - |
| 52 | 1886 | 1 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s1-9s1-10s0` | killed at END (no record) | - |

### Totals per root

| root | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1` | 14 | 11 | 3 | 0 | 0 |
| `0s0_2` | 15 | 12 | 3 | 0 | 0 |
| `0s0_3` | 14 | 8 | 6 | 0 | 0 |
| `0s0_4` | 10 | 4 | 3 | 2 | 1 |

### Totals per parent

| parent | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1` | 1 | 0 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | 1 | 0 | 0 | 1 | 0 |

### Parents all of whose units on this machine were certified (35)

(each parent six-bit cube has one unit on this machine)

- `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1`
- `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0`
- `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0`
- `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1`
- `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1`
- `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0`
- `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0`
- `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1`
- `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0`
- `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1`
- `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0`
- `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0`
- `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1`
- `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0`
- `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0`
- `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1`
- `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1`
- `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0`
- `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0`
- `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1`
- `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0`
- `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1`
- `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1`
- `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0`
- `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0`
- `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1`
- `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0`
- `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1`
- `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0`
- `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0`
- `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0`
- `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1`
- `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1`
- `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0`
- `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0`

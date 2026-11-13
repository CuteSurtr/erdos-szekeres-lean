# C3W7 Q15: nine-bit σ-cubes of the H3/one roots, shard 15 of 36 of W7.tsv

Task: `results/C3W7/TASK.md` at 39bb1bac, V = Q15, LIST = W7.tsv, j = 15, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 10:46:31 UTC, END 15:01:31 UTC; the three lanes were killed (whole process groups) at 15:01:33.

## Tools and base check

- C3U2 tools: worktree of cad4e050 (cad4e050d778aa37c9ea23afcbe704c94db3e890), used unmodified; `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check passed: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Details in `tools.txt`. Command per unit: `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02` (`lane.sh`).

## Outcome

53 units (rows ≡ 15 mod 36): **19 certified, 30 timed out at 900 s, 3 killed at END while solving, 1 not reached.**

- No SAT. No `PROOF NOT ACCEPTED`, so `recheck.jsonl` does not exist. Every certified record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`; no record has cake_lpr `none`.
- No memory problem (used memory stayed under 6 GB of 16 GB). No unit ended early: every timeout ran the full 900 s, and no solve finished in under 72 s without a certificate.
- Each of the 30 timed-out units has its layer-split record (45 children, unsolved, in `open_frontier`), as the task intends.
- The 3 units killed at END have no record and are open. They are listed below as "killed at END".

`out.jsonl` holds lanes 0, 1 and 2 in that order: 49 solve records and 30 split records.

## Per unit

| row | lane | unit (bits after __) | status | solve s | check s |
|---|---|---|---|---|---|
| 15 | 0 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | certified | 686.1 | 111.0 |
| 51 | 1 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | certified | 804.5 | 122.6 |
| 87 | 2 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | certified | 802.4 | 117.7 |
| 123 | 0 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 159 | 1 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 195 | 2 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 231 | 0 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 267 | 1 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 303 | 2 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 339 | 0 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 375 | 1 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 | 900.2 |  |
| 411 | 2 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 | 900.2 |  |
| 447 | 0 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 483 | 1 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 519 | 2 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | certified | 812.9 | 105.9 |
| 555 | 0 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | certified | 747.7 | 117.1 |
| 591 | 1 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | certified | 851.2 | 112.3 |
| 627 | 2 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 663 | 0 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 699 | 1 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 735 | 2 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | certified | 878.6 | 115.2 |
| 771 | 0 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | certified | 755.6 | 100.8 |
| 807 | 1 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 843 | 2 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 879 | 0 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 915 | 1 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 951 | 2 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 987 | 0 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1023 | 1 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | certified | 807.0 | 97.3 |
| 1059 | 2 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | certified | 657.6 | 92.8 |
| 1095 | 0 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | certified | 663.1 | 98.3 |
| 1131 | 1 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1167 | 2 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | certified | 809.9 | 103.4 |
| 1203 | 0 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1239 | 1 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1275 | 2 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | certified | 830.1 | 111.8 |
| 1311 | 0 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | certified | 802.0 | 103.7 |
| 1347 | 1 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | certified | 828.1 | 100.6 |
| 1383 | 2 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1419 | 0 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1455 | 1 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1491 | 2 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1527 | 0 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1563 | 1 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s0-9s1-10s1` | certified | 676.0 | 90.3 |
| 1599 | 2 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1-8s1-9s1-10s1` | certified | 778.8 | 107.2 |
| 1635 | 0 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s0-9s1-10s1` | certified | 874.8 | 109.7 |
| 1671 | 1 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0-8s1-9s1-10s1` | certified | 745.3 | 95.0 |
| 1707 | 2 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1743 | 0 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 | 900.1 |  |
| 1779 | 1 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s0-9s1-10s1` | killed at END (started, no record) |  |  |
| 1815 | 2 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s1-9s1-10s1` | killed at END (started, no record) |  |  |
| 1851 | 0 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s0-9s1-10s1` | killed at END (started, no record) |  |  |
| 1887 | 1 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s1-9s1-10s1` | not reached |  |  |

Per root:

| root | units | certified | timed out | not reached/killed |
|---|---|---|---|---|
| 0s0_1 | 14 | 3 | 11 | 0 |
| 0s0_2 | 15 | 6 | 9 | 0 |
| 0s0_3 | 14 | 6 | 8 | 0 |
| 0s0_4 | 10 | 4 | 2 | 4 |

Per parent six-bit cube:

| parent | units here | certified | timed out | not reached/killed |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | 1 | 0 | 0 | 1 |

Parents all of whose units on this machine were certified: `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1`, `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0`, `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0`, `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0`, `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1`, `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1`, `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1`, `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0`, `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1`, `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0`, `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0`, `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1`, `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1`, `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1`, `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0`, `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1`, `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1`, `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0`, `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0`

Certified solve times (n=19): min 657.6, Q1 745.3, median 802.4, Q3 828.1, p90 874.8, max 878.6; above 300 s: 19



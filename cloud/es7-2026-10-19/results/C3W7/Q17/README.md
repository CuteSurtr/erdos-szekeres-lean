# C3W7 Q17: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv, shard 17 of 36)

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q17, LIST = W7.tsv, j = 17, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 10:45:54 UTC, END 15:00:54 UTC (lanes killed at 15:01:04).

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its example prints `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check passed: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).

## Run

53 units (rows ≡ 17 mod 36 of `W7.tsv`, `units.tsv`), 3 lanes (`lane0.sh`–`lane2.sh`), lane k = positions ≡ k (mod 3), each unit run as
`close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. No records were seeded.
`out.jsonl` holds the records of lane 0, then 1, then 2 (68 lines: 34 certified solves, and 17 timed-out solves each with its layer-split record of 45 children, left unsolved as intended).

**Result: 34 certified, 17 timed out at 900 s, 2 not reached** (both were started, at 14:49:27 on lane 1 and 14:57:25 on lane 0, and killed at END with no record; lane 2 finished all its units at 14:59:18).

- No SAT. No proof rejection: every certified record has `c VERIFIED` and `s VERIFIED UNSAT`; no record has a checker result `none`, so nothing needed a re-check (no `recheck.jsonl`).
- No memory problem (used memory stayed at or under about 6 GB of 15 GB). No unit ended early: every non-certified solve ran the full 900 s.
- Total over certified units: solve 25469 s, check 3581 s (per-node times with 3 solves sharing 4 cores).
- The solve times are well above the 450–662 s of `results/C3H1/X1`: all 34 certified units took more than 300 s, and 11 of them more than 800 s, so a third of the units missed the 900 s cap.

## Per unit

| pos | lane | row | unit | status | solve s | check s |
|---|---|---|---|---|---|---|
| 0 | 0 | 17 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | certified | 524.7 | 96.8 |
| 1 | 1 | 53 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | certified | 701.6 | 109.6 |
| 2 | 2 | 89 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | certified | 783.4 | 104.2 |
| 3 | 0 | 125 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | certified | 676.2 | 108.3 |
| 4 | 1 | 161 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | certified | 612.7 | 106.1 |
| 5 | 2 | 197 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | certified | 882.5 | 124.0 |
| 6 | 0 | 233 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | certified | 871.1 | 127.4 |
| 7 | 1 | 269 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | certified | 829.5 | 111.9 |
| 8 | 2 | 305 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | certified | 798.1 | 113.4 |
| 9 | 0 | 341 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | certified | 870.4 | 120.0 |
| 10 | 1 | 377 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | certified | 821.1 | 124.0 |
| 11 | 2 | 413 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 12 | 0 | 449 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | certified | 640.4 | 100.4 |
| 13 | 1 | 485 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | certified | 849.4 | 116.6 |
| 14 | 2 | 521 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | certified | 590.0 | 108.0 |
| 15 | 0 | 557 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | certified | 690.2 | 101.2 |
| 16 | 1 | 593 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | certified | 735.8 | 106.2 |
| 17 | 2 | 629 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 18 | 0 | 665 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | certified | 890.6 | 120.0 |
| 19 | 1 | 701 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | certified | 703.2 | 94.5 |
| 20 | 2 | 737 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | certified | 715.7 | 100.3 |
| 21 | 0 | 773 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | certified | 745.6 | 106.8 |
| 22 | 1 | 809 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | certified | 843.1 | 110.4 |
| 23 | 2 | 845 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 24 | 0 | 881 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 25 | 1 | 917 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 26 | 2 | 953 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 27 | 0 | 989 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 28 | 1 | 1025 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | certified | 529.4 | 87.6 |
| 29 | 2 | 1061 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | certified | 759.9 | 98.7 |
| 30 | 0 | 1097 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | certified | 754.0 | 94.9 |
| 31 | 1 | 1133 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | certified | 664.2 | 89.5 |
| 32 | 2 | 1169 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | certified | 776.3 | 100.3 |
| 33 | 0 | 1205 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 34 | 1 | 1241 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 35 | 2 | 1277 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | certified | 869.8 | 109.8 |
| 36 | 0 | 1313 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | certified | 798.8 | 102.4 |
| 37 | 1 | 1349 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 38 | 2 | 1385 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 39 | 0 | 1421 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 40 | 1 | 1457 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 41 | 2 | 1493 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 42 | 0 | 1529 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 43 | 1 | 1565 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s1-9s0-10s1` | certified | 684.1 | 97.9 |
| 44 | 2 | 1601 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s0-9s0-10s1` | certified | 622.6 | 86.4 |
| 45 | 0 | 1637 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s1-9s0-10s1` | certified | 859.4 | 106.3 |
| 46 | 1 | 1673 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s0-9s0-10s1` | certified | 703.7 | 94.6 |
| 47 | 2 | 1709 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s1-9s0-10s1` | certified | 896.5 | 104.7 |
| 48 | 0 | 1745 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s0-9s0-10s1` | timed out at 900 | 900.1 |  |
| 49 | 1 | 1781 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s1-9s0-10s1` | timed out at 900 | 900.1 |  |
| 50 | 2 | 1817 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s0-9s0-10s1` | certified | 775.4 | 98.2 |
| 51 | 0 | 1853 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s1-9s0-10s1` | not reached |  |  |
| 52 | 1 | 1889 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s0-9s0-10s1` | not reached |  |  |


### Totals per root

| root | units | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1` | 14 | 13 | 1 | 0 |
| `0s0_2` | 14 | 8 | 6 | 0 |
| `0s0_3` | 15 | 7 | 8 | 0 |
| `0s0_4` | 10 | 6 | 2 | 2 |

### Totals per parent six-bit cube

| parent six-bit cube | units | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0` | 1 | 0 | 0 | 1 |

Each parent has exactly one of its 8 nine-bit cubes on this machine. Parents all of whose units here were certified (34): `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0`, `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0`, `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1`, `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1`, `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0`, `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0`, `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1`, `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1`, `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0`, `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0`, `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1`, `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0`, `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0`, `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1`, `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1`, `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0`, `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1`, `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1`, `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0`, `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0`, `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1`, `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0`, `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0`, `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1`, `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1`, `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0`, `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1`, `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0`, `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1`, `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0`, `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0`, `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1`, `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1`, `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1`

## Solve-time distribution of the certified units

Certified solve times (n=34): min 524.7, Q1 682.1, median 757.0, Q3 844.7, p90 876.8, max 896.5; above 300 s: 34


# C3W7 / Q23: nine-bit σ-cubes of the H3/one roots, shard 23 of 36 of W7.tsv

**Result: none of my 53 units was certified. 48 timed out at cap 900. 3 were running at END and killed with no record, and 2 were not reached. No SAT, no proof rejection, no checker `none`, no memory problem, and no unit ended early.**

## Setup

One cloud VM: 4 cores (Intel Xeon @ 2.80 GHz), 15 GB RAM, no swap (`env.txt`). Task `results/C3W7/TASK.md` at 39bb1bac with V = Q23, LIST = W7.tsv, j = 23, N = 36, H = 4.5. Start 10:46:26 UTC, lanes started 10:50:02, END 15:01:26 UTC.

- Tools: worktree of cad4e050 at /opt/c3u2 (C3U2 tools, unmodified). CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. The sanity test passed: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both. Details are in `tools.txt`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Units: the rows of W7.tsv with row ≡ 23 (mod 36), 53 units (`units.tsv`), no seeding. Three lanes ran with `setsid nohup` (`lane.sh`, `lane0-2.sh`). Lane k took positions ≡ k (mod 3) and ran `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. At END a killer script stopped every lane's process group.
- `out.jsonl` holds lanes 0, 1 and 2 in that order: 48 UNKNOWN solve records at cap 900, each followed by its layer-split record with 45 children. The children were left unsolved, as intended. There is no `recheck.jsonl` because no re-check was needed.

## Per unit

| row | unit | result |
|-----|------|--------|
| 23 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 59 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 95 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 131 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 167 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 203 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 239 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 275 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 311 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 347 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 383 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 419 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 455 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 491 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 527 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 563 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.3 s); layer-split record, 45 children (unsolved) |
| 599 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 635 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 671 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 707 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 743 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 779 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 815 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 851 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 887 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 923 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 959 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 995 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1031 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1067 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.4 s); layer-split record, 45 children (unsolved) |
| 1103 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1139 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.2 s); layer-split record, 45 children (unsolved) |
| 1175 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1211 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1247 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1283 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1319 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1355 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.2 s); layer-split record, 45 children (unsolved) |
| 1391 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1427 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1463 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1499 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1535 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1571 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.2 s); layer-split record, 45 children (unsolved) |
| 1607 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.4 s); layer-split record, 45 children (unsolved) |
| 1643 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1679 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1715 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s); layer-split record, 45 children (unsolved) |
| 1751 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s1-9s1-10s1` | started 14:50 UTC, killed at END (no record) |
| 1787 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s0-9s1-10s1` | started 14:50 UTC, killed at END (no record) |
| 1823 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s1-9s1-10s1` | started 14:50 UTC, killed at END (no record) |
| 1859 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s0-9s1-10s1` | not reached |
| 1895 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s1-9s1-10s1` | not reached |

## Totals

| root | units | certified | timed out at 900 | killed at END | not reached |
|------|-------|-----------|------------------|---------------|-------------|
| 0s0_1 | 14 | 0 | 14 | 0 | 0 |
| 0s0_2 | 14 | 0 | 14 | 0 | 0 |
| 0s0_3 | 15 | 0 | 15 | 0 | 0 |
| 0s0_4 | 10 | 0 | 5 | 3 | 2 |
| total | 53 | 0 | 48 | 3 | 2 |

Per parent six-bit cube: each of my 53 units has a different parent, so I have exactly one unit per parent. No parent had all of its units on this machine certified. Each unit's result is the result for its parent column in the table above.

Solve-time distribution of certified units: none were certified, so there is no distribution, and 0 were certified above 300 s. Every solve ran to the cap (900.1–900.4 s).

## Remark: these units may all be harder, or this machine slower

Every unit on this shard has σ bits 9 = 1 and 10 = 1. Because 36 ≡ 4 (mod 8), rows ≡ 23 (mod 36) always land on positions 3 or 7 within each parent's 8 cubes. In the C3W7 records pushed by 15:03 UTC (all Q machines, including mine), the `-9s1-10s1` cubes were certified 131 times and timed out 282 times. Without my 48 timeouts, that is about 36% certified, and the median certified solve time over all classes is about 750 s. A 0-of-48 result at about 36% is very unlikely by chance. So this VM was probably slower than the others; three solvers sharing 4 cores is the same load as on the other machines. The 48 timed-out units are still open (their layer-split children are unsolved), and so are the 5 units that never got a record.

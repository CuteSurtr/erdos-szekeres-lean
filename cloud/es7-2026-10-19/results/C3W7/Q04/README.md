# C3W7 Q04: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv, shard 4 of 36)

TASK.md at 39bb1bac with V = Q04, LIST = W7.tsv, j = 4, N = 36, H = 4.5. One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`).
Start 10:46:00 UTC, lanes started 10:49:14, END 15:01:00 (lanes killed at 15:01:23 by a watcher), 2026-10-25.

## Tools and base check (`tools.txt`)

- σ tools: worktree of cad4e050, `results/C3U2/tools`, unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (bundled example `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0 with the E2 patch. Sanity check passes: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).

## Run

53 units (rows ≡ 4 mod 36 of `lists/W7.tsv`, in `units.tsv`), no seeded records. 3 lanes (`lane0.sh`–`lane2.sh`), each running
`close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02` per unit.
`out.jsonl` = lane 0, 1, 2 records (35 certified solve records, 16 timed-out solve records, and 16 layer-split records written for the timeouts; their children are unsolved and are in `open_frontier`, as intended).

- **No SAT. No proof rejection** (every UNSAT answer was accepted by both lrat-check and cake_lpr; no `none`, so no `recheck.jsonl`). No memory problem (used memory stayed at or below about 6 GB of 15). No unit ended under 72 s without a certificate.
- Lane 2 finished all its 17 units at 14:56:44. Lanes 0 and 1 each had their last unit running at END (`0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s0-9s0-10s0`, started 14:51:25, and `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0-8s1-9s0-10s0`, started 14:46:39). Both were killed at 15:01:23 and wrote no record, so they are open (no node was left with a killed checker and `none`).
- Check time of the certified units: 78–133 s.

## Totals

### Totals per root

| root | units | certified | timed out at 900 | killed at END | not reached |
|---|---|---|---|---|---|
| 0s0_1 | 15 | 11 | 4 | 0 | 0 |
| 0s0_2 | 14 | 11 | 3 | 0 | 0 |
| 0s0_3 | 14 | 9 | 5 | 0 | 0 |
| 0s0_4 | 10 | 4 | 4 | 2 | 0 |
| **all** | 53 | 35 | 16 | 2 | 0 |

Parents all of whose units on Q04 were certified (35): `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0`, `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1`, `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0`, `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0`, `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0`, `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0`, `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1`, `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0`, `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0`, `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1`, `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1`, `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0`, `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0`, `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1`, `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1`, `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0`, `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0`, `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1`, `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0`, `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1`, `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0`, `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0`, `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1`, `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1`, `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0`, `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0`, `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1`, `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0`, `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0`, `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0`, `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1`, `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0`, `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0`, `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1`, `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0`

Solve time of the 35 certified units: min 508.2, Q1 646.1, median 718.9, Q3 840.4, p90 882.2, max 890.4 s; 35 certified above 300 s.

Units ending under 72 s without a certificate: none

Each parent six-bit cube has exactly one of its 8 nine-bit units on this machine, so the per-parent table is the per-unit table grouped by parent; it is below. The parents listed above as all-certified are the 35 parents of the certified units.

## Per unit

| row | lane | unit | result | solve s | check s |
|---|---|---|---|---|---|
| 4 | 0 | 0s0_1__2s0-3s0-4s0-5s0-6s0-7s0-8s1-9s0-10s0 | certified | 525.1 | 104.4 |
| 40 | 1 | 0s0_1__2s0-3s0-4s0-5s1-6s0-7s1-8s0-9s0-10s0 | certified | 639.1 | 111.0 |
| 76 | 2 | 0s0_1__2s0-3s0-4s1-5s0-6s0-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 112 | 0 | 0s0_1__2s0-3s0-4s1-5s1-6s1-7s0-8s0-9s0-10s0 | certified | 884.1 | 133.4 |
| 148 | 1 | 0s0_1__2s0-3s1-4s0-5s0-6s1-7s0-8s1-9s0-10s0 | certified | 811.5 | 121.4 |
| 184 | 2 | 0s0_1__2s0-3s1-4s0-5s1-6s1-7s1-8s0-9s0-10s0 | timed out at 900 | 900.1 |  |
| 220 | 0 | 0s0_1__2s0-3s1-4s1-5s0-6s1-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 256 | 1 | 0s0_1__2s1-3s0-4s0-5s0-6s0-7s0-8s0-9s0-10s0 | certified | 508.2 | 89.6 |
| 292 | 2 | 0s0_1__2s1-3s0-4s0-5s1-6s0-7s0-8s1-9s0-10s0 | certified | 725.4 | 99.4 |
| 328 | 0 | 0s0_1__2s1-3s0-4s1-5s0-6s0-7s1-8s0-9s0-10s0 | certified | 630.6 | 94.9 |
| 364 | 1 | 0s0_1__2s1-3s0-4s1-5s1-6s0-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 400 | 2 | 0s0_1__2s1-3s1-4s0-5s0-6s1-7s0-8s0-9s0-10s0 | certified | 668.8 | 91.9 |
| 436 | 0 | 0s0_1__2s1-3s1-4s0-5s1-6s1-7s0-8s1-9s0-10s0 | certified | 699.5 | 102.9 |
| 472 | 1 | 0s0_1__2s1-3s1-4s1-5s0-6s1-7s1-8s0-9s0-10s0 | certified | 679.9 | 97.7 |
| 508 | 2 | 0s0_1__2s1-3s1-4s1-5s1-6s1-7s1-8s1-9s0-10s0 | certified | 718.9 | 95.2 |
| 544 | 0 | 0s0_2__1s0-3s0-4s0-5s1-6s0-7s0-8s0-9s0-10s0 | certified | 508.9 | 91.0 |
| 580 | 1 | 0s0_2__1s0-3s0-4s1-5s0-6s0-7s0-8s1-9s0-10s0 | certified | 656.8 | 110.8 |
| 616 | 2 | 0s0_2__1s0-3s0-4s1-5s1-6s0-7s1-8s0-9s0-10s0 | certified | 864.4 | 113.6 |
| 652 | 0 | 0s0_2__1s0-3s1-4s0-5s0-6s0-7s1-8s1-9s0-10s0 | certified | 852.9 | 106.2 |
| 688 | 1 | 0s0_2__1s0-3s1-4s0-5s1-6s1-7s0-8s0-9s0-10s0 | certified | 886.3 | 106.2 |
| 724 | 2 | 0s0_2__1s0-3s1-4s1-5s0-6s1-7s0-8s1-9s0-10s0 | certified | 881.0 | 109.7 |
| 760 | 0 | 0s0_2__1s0-3s1-4s1-5s1-6s1-7s1-8s0-9s0-10s0 | certified | 736.5 | 103.9 |
| 796 | 1 | 0s0_2__1s1-3s0-4s0-5s0-6s1-7s1-8s1-9s0-10s0 | timed out at 900 | 900.2 |  |
| 832 | 2 | 0s0_2__1s1-3s0-4s1-5s0-6s0-7s0-8s0-9s0-10s0 | certified | 580.0 | 87.4 |
| 868 | 0 | 0s0_2__1s1-3s0-4s1-5s1-6s0-7s0-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 904 | 1 | 0s0_2__1s1-3s1-4s0-5s0-6s0-7s1-8s0-9s0-10s0 | certified | 712.4 | 94.7 |
| 940 | 2 | 0s0_2__1s1-3s1-4s0-5s1-6s0-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 976 | 0 | 0s0_2__1s1-3s1-4s1-5s0-6s1-7s0-8s0-9s0-10s0 | certified | 668.8 | 95.3 |
| 1012 | 1 | 0s0_2__1s1-3s1-4s1-5s1-6s1-7s0-8s1-9s0-10s0 | certified | 818.6 | 111.8 |
| 1048 | 2 | 0s0_3__1s0-2s0-4s0-5s0-6s1-7s1-8s0-9s0-10s0 | certified | 840.4 | 102.3 |
| 1084 | 0 | 0s0_3__1s0-2s0-4s0-5s1-6s1-7s1-8s1-9s0-10s0 | certified | 890.4 | 116.0 |
| 1120 | 1 | 0s0_3__1s0-2s0-4s1-5s1-6s0-7s0-8s0-9s0-10s0 | certified | 646.1 | 91.2 |
| 1156 | 2 | 0s0_3__1s0-2s1-4s0-5s0-6s0-7s0-8s1-9s0-10s0 | certified | 667.1 | 88.3 |
| 1192 | 0 | 0s0_3__1s0-2s1-4s0-5s1-6s0-7s1-8s0-9s0-10s0 | certified | 786.7 | 121.7 |
| 1228 | 1 | 0s0_3__1s0-2s1-4s1-5s0-6s0-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1264 | 2 | 0s0_3__1s0-2s1-4s1-5s1-6s1-7s0-8s0-9s0-10s0 | certified | 813.8 | 100.1 |
| 1300 | 0 | 0s0_3__1s1-2s0-4s0-5s0-6s1-7s0-8s1-9s0-10s0 | certified | 847.7 | 113.1 |
| 1336 | 1 | 0s0_3__1s1-2s0-4s0-5s1-6s1-7s1-8s0-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1372 | 2 | 0s0_3__1s1-2s0-4s1-5s0-6s1-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1408 | 0 | 0s0_3__1s1-2s1-4s0-5s0-6s0-7s0-8s0-9s0-10s0 | certified | 647.8 | 95.5 |
| 1444 | 1 | 0s0_3__1s1-2s1-4s0-5s1-6s0-7s0-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1480 | 2 | 0s0_3__1s1-2s1-4s1-5s0-6s0-7s1-8s0-9s0-10s0 | certified | 817.2 | 128.5 |
| 1516 | 0 | 0s0_3__1s1-2s1-4s1-5s1-6s0-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1552 | 1 | 0s0_4__1s0-2s0-3s0-5s0-6s1-7s0-8s0-9s0-10s0 | certified | 539.1 | 78.2 |
| 1588 | 2 | 0s0_4__1s0-2s0-3s0-5s1-6s1-7s0-8s1-9s0-10s0 | certified | 863.0 | 108.9 |
| 1624 | 0 | 0s0_4__1s0-2s0-3s1-5s0-6s1-7s1-8s0-9s0-10s0 | certified | 830.9 | 104.2 |
| 1660 | 1 | 0s0_4__1s0-2s0-3s1-5s1-6s1-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1696 | 2 | 0s0_4__1s0-2s1-3s0-5s1-6s0-7s0-8s0-9s0-10s0 | certified | 644.0 | 103.3 |
| 1732 | 0 | 0s0_4__1s0-2s1-3s1-5s0-6s0-7s0-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1768 | 1 | 0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s0-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1804 | 2 | 0s0_4__1s1-2s0-3s0-5s0-6s0-7s1-8s1-9s0-10s0 | timed out at 900 | 900.1 |  |
| 1840 | 0 | 0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s0-9s0-10s0 | killed at END (no record) |  |  |
| 1876 | 1 | 0s0_4__1s1-2s0-3s1-5s0-6s1-7s0-8s1-9s0-10s0 | killed at END (no record) |  |  |

### Totals per parent six-bit cube


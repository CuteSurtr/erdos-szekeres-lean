# C3W7 / Q32: nine-bit σ-cubes of the H3/one roots at cap 900, shard 32 of 36 of W7.tsv

**Result: 37 of my 53 units are certified, 14 timed out at 900 s (each got its layer-split record, 45 children, not solved), and 2 were still running at END and were killed. No SAT. No proof rejection. No memory problem. No unit ended early.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 10:46:14 UTC, END 15:01:14 UTC (H = 4.5 h minus 15 min). Task: `results/C3W7/TASK.md` at 39bb1bac.

- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `results/C3U2/tools`, not modified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch. Sanity test: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches). Details are in `tools.txt`.
- Units: rows of `lists/W7.tsv` with row ≡ 32 (mod 36), 53 units (`units.tsv`). No seeding.
- 3 lanes (`lane0.sh`–`lane2.sh` → `lane.sh`). Lane k runs the units at positions ≡ k (mod 3), each with `close_tree.py … --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
- Lane 2 finished its 17 units at 14:51:49. Lanes 0 and 1 were killed (whole process groups) at 15:01:19. Each was in the middle of a solve, so neither unit has a record. No checker was killed, so there are no `none` records.

## Totals

- Certified: 37. Every one shows `c VERIFIED` (lrat-check) and `s VERIFIED UNSAT` (cake_lpr).
- Timed out at 900: 14. Each has a split record with 45 children, which are open.
- Killed at END: 2. Not reached: 0.
- Solve time of the certified units: min 501.6, Q1 635.5, median 752.6, Q3 817.5, p90 848.3, max 869.0 s. All 37 were certified above 300 s. The sums are 27,075 s solve and 3,809 s check; check time per unit was 79–127 s and the largest proof was 1.17 GB (deleted).
- No unit ended in under 72 s without a certificate. There was no `PROOF NOT ACCEPTED`, so there is no `recheck.jsonl`.

## Per root

| root | units | certified | timed out | killed at END |
|---|---|---|---|---|
| 0s0_1 | 14 | 11 | 3 | 0 |
| 0s0_2 | 14 | 10 | 4 | 0 |
| 0s0_3 | 14 | 11 | 3 | 0 |
| 0s0_4 | 11 | 5 | 4 | 2 |

The two `0s0_4` units killed at END are `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s1-9s0-10s0` (lane 0, started 14:51:34) and `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s0-9s0-10s0` (lane 1, started 14:47:30). Both are still unsolved.

Each of my units has a different parent six-bit cube, so each parent has exactly 1 unit on this machine. In the per-parent table, "all certified" marks the 37 parents whose only unit here was certified. The other units of those parents are on other machines.

## Per unit and per parent

(The "not reached" column below counts the 2 units killed at END.)

| pos | lane | row | unit | result | solve s | check s |
|---|---|---|---|---|---|---|
| 0 | 0 | 32 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 551.6 | 103.8 |
| 1 | 1 | 68 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 666.7 | 114.7 |
| 2 | 2 | 104 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 3 | 0 | 140 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | certified | 869.0 | 127.4 |
| 4 | 1 | 176 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | certified | 806.1 | 122.7 |
| 5 | 2 | 212 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 6 | 0 | 248 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | certified | 820.1 | 103.9 |
| 7 | 1 | 284 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 8 | 2 | 320 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 619.6 | 92.7 |
| 9 | 0 | 356 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | certified | 760.5 | 109.7 |
| 10 | 1 | 392 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 605.0 | 103.0 |
| 11 | 2 | 428 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | certified | 775.8 | 103.8 |
| 12 | 0 | 464 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 632.3 | 95.4 |
| 13 | 1 | 500 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | certified | 637.1 | 94.4 |
| 14 | 2 | 536 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | certified | 720.8 | 116.6 |
| 15 | 0 | 572 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 16 | 1 | 608 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 689.3 | 99.8 |
| 17 | 2 | 644 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 633.3 | 94.1 |
| 18 | 0 | 680 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | certified | 751.1 | 97.8 |
| 19 | 1 | 716 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 20 | 2 | 752 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | certified | 704.6 | 100.9 |
| 21 | 0 | 788 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | certified | 842.5 | 107.2 |
| 22 | 1 | 824 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 23 | 2 | 860 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 24 | 0 | 896 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 597.1 | 89.9 |
| 25 | 1 | 932 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0-8s1-9s0-10s0` | certified | 820.4 | 112.4 |
| 26 | 2 | 968 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 741.9 | 102.7 |
| 27 | 0 | 1004 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1-8s1-9s0-10s0` | certified | 806.0 | 124.2 |
| 28 | 1 | 1040 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 501.6 | 78.6 |
| 29 | 2 | 1076 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | certified | 815.6 | 109.8 |
| 30 | 0 | 1112 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | certified | 818.2 | 94.7 |
| 31 | 1 | 1148 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 32 | 2 | 1184 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 641.1 | 87.6 |
| 33 | 0 | 1220 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 821.0 | 92.7 |
| 34 | 1 | 1256 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | certified | 791.9 | 100.0 |
| 35 | 2 | 1292 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | certified | 752.6 | 108.6 |
| 36 | 0 | 1328 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | certified | 816.7 | 107.3 |
| 37 | 1 | 1364 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | certified | 868.0 | 109.3 |
| 38 | 2 | 1400 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | certified | 848.3 | 124.7 |
| 39 | 0 | 1436 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 40 | 1 | 1472 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 737.9 | 94.0 |
| 41 | 2 | 1508 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 42 | 0 | 1544 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 543.1 | 87.6 |
| 43 | 1 | 1580 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1-8s1-9s0-10s0` | certified | 862.7 | 102.6 |
| 44 | 2 | 1616 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 786.3 | 105.6 |
| 45 | 0 | 1652 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 46 | 1 | 1688 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1-8s0-9s0-10s0` | certified | 785.1 | 100.9 |
| 47 | 2 | 1724 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 48 | 0 | 1760 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0-8s0-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 49 | 1 | 1796 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 633.8 | 87.5 |
| 50 | 2 | 1832 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 (layer split, 45 children) | 900.1 |  |
| 51 | 0 | 1868 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s1-9s0-10s0` | not reached |  |  |
| 52 | 1 | 1904 | `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s0-9s0-10s0` | not reached |  |  |

| root | units | certified | timed out | not reached |
|---|---|---|---|---|
| 0s0_1 | 14 | 11 | 3 | 0 |
| 0s0_2 | 14 | 10 | 4 | 0 |
| 0s0_3 | 14 | 11 | 3 | 0 |
| 0s0_4 | 11 | 5 | 4 | 2 |

| parent six-bit cube | units here | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | all certified
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | all certified
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 0 | 1 |

## Files

`env.txt`, `tools.txt`, `units.tsv`, `lane.sh`, `lane0.sh`–`lane2.sh`, `out.jsonl` (the records of lanes 0, 1 and 2, in that order: 65 lines = 51 solve records + 14 split records), `driver{0,1,2}.log.tail`.

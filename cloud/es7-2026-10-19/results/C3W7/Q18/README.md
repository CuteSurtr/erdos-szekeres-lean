# C3W7 Q18: nine-bit σ-cubes of the H3/one roots, W7.tsv shard 18 of 36

Task `results/C3W7/TASK.md` at 39bb1bac; V = Q18, LIST = W7.tsv, j = 18, N = 36, H = 4.5.
Start 2026-10-25 10:46:30 UTC, END 15:01:30 UTC (lanes killed at END). Machine: 4 cores, 15 GB, no swap (`env.txt`).

## Tools (details in `tools.txt`)
- C3U2 tools at cad4e050, unmodified (`/opt/c3u2/.../C3U2/tools`); `compose.py` not run.
- CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc + E2 patch (sanity: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both).
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…cdd6da`, matches.

## Run
53 units (`units.tsv`), 3 lanes (`lane0.sh` … `lane2.sh`), each unit `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. No seeding. Records: `out.jsonl` (lane 0, 1, 2; 88 lines: 48 solve records and 40 layer-split records), driver log tails `driver{k}.log.tail`.

## Result
- **Certified: 8.** **Timed out at 900 s: 40** (each got its layer-split record with 45 children, left unsolved as intended). **Not reached: 5**: rows 1746, 1782 and 1818 started at 14:48–14:50 and were killed at END with no record; rows 1854 and 1890 never started.
- No SAT. No proof rejection: every UNSAT record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, no `none`, so no re-check was needed and there is no `recheck.jsonl`. No memory problem (no OOM, no killed process before END). No unit ended early: every timeout is 900.1–900.3 s; the fastest certified solve was 582 s.

### Per unit
| row | unit | result |
|---|---|---|
| 18 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | certified solve 765.0 check 111.2 |
| 54 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 90 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 126 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 162 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | certified solve 751.3 check 116.3 |
| 198 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 234 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 270 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 306 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 342 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 378 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 414 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 450 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 486 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 522 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified solve 762.4 check 117.3 |
| 558 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 594 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 630 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 666 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 702 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 738 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 774 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 810 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 846 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 882 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 918 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 954 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 990 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1026 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | certified solve 582.4 check 96.5 |
| 1062 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | certified solve 810.6 check 107.0 |
| 1098 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1134 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1170 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1206 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1242 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1278 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1314 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1350 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1386 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1422 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1458 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1494 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1530 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1566 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s1-9s1-10s0` | certified solve 893.1 check 116.9 |
| 1602 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s0-9s1-10s0` | certified solve 792.4 check 114.2 |
| 1638 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1674 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified solve 850.2 check 120.2 |
| 1710 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1746 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s0-9s1-10s0` | not reached (started, killed at END, no record) |
| 1782 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s1-9s1-10s0` | not reached (started, killed at END, no record) |
| 1818 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s0-9s1-10s0` | not reached (started, killed at END, no record) |
| 1854 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s1-9s1-10s0` | not reached |
| 1890 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s0-9s1-10s0` | not reached |
| 18 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | certified solve 765.0 check 111.2 |
| 54 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 90 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 126 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 162 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | certified solve 751.3 check 116.3 |
| 198 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 234 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 270 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 306 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 342 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 378 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 414 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 450 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 486 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 522 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified solve 762.4 check 117.3 |
| 558 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 594 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 630 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 666 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 702 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 738 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 774 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 810 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 846 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 882 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 918 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 954 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 990 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1026 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | certified solve 582.4 check 96.5 |
| 1062 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | certified solve 810.6 check 107.0 |
| 1098 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1134 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1170 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1206 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1242 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1278 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1314 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1350 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1386 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1422 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1458 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1494 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1530 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (split children 45) |
| 1566 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s1-9s1-10s0` | certified solve 893.1 check 116.9 |
| 1602 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s0-9s1-10s0` | certified solve 792.4 check 114.2 |
| 1638 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1674 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified solve 850.2 check 120.2 |
| 1710 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (split children 45) |
| 1746 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s0-9s1-10s0` | not reached |
| 1782 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s1-9s1-10s0` | not reached |
| 1818 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s0-9s1-10s0` | not reached |
| 1854 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s1-9s1-10s0` | not reached |
| 1890 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s0-9s1-10s0` | not reached |

(Solve and check times in seconds.)

### Per root (the `root` column)
| root | units | certified | timed out | not reached |
|---|---|---|---|---|
| 0s0_1 | 14 | 2 | 12 | 0 |
| 0s0_2 | 14 | 1 | 13 | 0 |
| 0s0_3 | 15 | 2 | 13 | 0 |
| 0s0_4 | 10 | 3 | 2 | 5 |
| total | 53 | 8 | 40 | 5 |

### Per parent six-bit cube (the `parent` column)
With stride 36 every one of the 53 parents has exactly one unit (of its 8) on this machine, so each parent's count here is that one unit's result. Parents all of whose units on this machine were certified (8):
- `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0`
- `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0`
- `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1`
- `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0`
- `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0`
- `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1`
- `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0`
- `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1`

The other 45 parents: 40 with their unit timed out at 900, 5 with it not reached (rows 1746, 1782, 1818, 1854, 1890).

### Solve times of the certified units
8 units: min 582.4, Q1 759.6, median 778.7, Q3 820.5, p90 863.1, max 893.1 s (check 96.5–120.2 s). All 8 were certified above 300 s; 4 of them above 790 s.
At cap 900, with three solves in parallel on 4 cores, 40 of 48 nine-bit cubes time out. That is much worse than the 450–662 s per cube in `results/C3H1/X1/README.md`.

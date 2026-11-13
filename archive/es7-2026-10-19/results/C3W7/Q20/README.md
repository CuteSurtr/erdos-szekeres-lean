# C3W7 / Q20: nine-bit σ-cubes of the H3/one roots at cap 900, shard 20 of 36

**Result: 52 of my 53 units certified, 1 timed out at 900 s (layer-split record written, 45 children left open as intended), 0 not reached. No SAT. No proof rejection. No memory problem. No unit ended early.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:04 UTC on 2026-10-25, END 15:01:04 UTC (start + 4.5 h − 15 min). All three lanes ran out of units before END (last unit ended 14:41 UTC), so nothing was killed.

- C3U2 tools: worktree of cad4e050 at /opt/c3u2, used unmodified; `compose.py` not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check: on {1},{-1}, LRAT `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches). Details in `tools.txt`.
- Units: rows of `lists/W7.tsv` with row ≡ 20 (mod 36): 53 units (`units.tsv`), no seeding. Three lanes (`lane0.sh`–`lane2.sh`), lane k = positions ≡ k (mod 3), each unit run as `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
- Incident (no effect on results): the first launch at 10:48:54 had END set wrongly (start + 4 h 45 min). I killed it about 20 s later, before any record was written, deleted its empty files and relaunched at 10:49:22 with the correct END.

## Per unit

Solve and check seconds are wall time with 3 lanes sharing the 4 cores.

| row | unit | result | solve s | check s |
|-----|------|--------|---------|---------|
| 20 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | certified | 580.7 | 98.3 |
| 56 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | certified | 679.1 | 113.2 |
| 92 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | certified | 834.9 | 116.2 |
| 128 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 430.7 | 84.0 |
| 164 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s1-9s0-10s0` | certified | 636.4 | 97.0 |
| 200 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 580.8 | 92.8 |
| 236 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s1-9s0-10s0` | certified | 713.9 | 102.2 |
| 272 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 480.0 | 83.2 |
| 308 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | certified | 785.7 | 105.4 |
| 344 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | certified | 635.1 | 91.4 |
| 380 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | certified | 670.1 | 92.0 |
| 416 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 515.4 | 80.4 |
| 452 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 529.9 | 81.6 |
| 488 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | certified | 578.9 | 80.8 |
| 524 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | certified | 554.3 | 83.6 |
| 560 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | certified | 583.3 | 89.4 |
| 596 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | certified | 644.4 | 91.1 |
| 632 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | certified | 724.2 | 98.6 |
| 668 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | certified | 857.4 | 107.4 |
| 704 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 440.9 | 77.0 |
| 740 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | certified | 741.6 | 99.5 |
| 776 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 534.2 | 79.1 |
| 812 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | certified | 855.8 | 98.1 |
| 848 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 603.8 | 84.2 |
| 884 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | certified | 879.3 | 108.3 |
| 920 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | certified | 706.0 | 91.6 |
| 956 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | certified | 779.9 | 97.4 |
| 992 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 632.3 | 83.1 |
| 1028 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 412.1 | 84.1 |
| 1064 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | certified | 550.9 | 79.7 |
| 1100 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | certified | 787.8 | 100.2 |
| 1136 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | certified | 666.2 | 90.0 |
| 1172 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | certified | 784.0 | 100.2 |
| 1208 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | certified | 863.9 | 105.1 |
| 1244 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | certified | 876.6 | 101.7 |
| 1280 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 447.9 | 69.9 |
| 1316 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s1-9s0-10s0` | certified | 743.9 | 87.5 |
| 1352 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 641.1 | 76.8 |
| 1388 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s1-9s0-10s0` | certified | 805.2 | 97.7 |
| 1424 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 577.7 | 74.2 |
| 1460 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | certified | 846.4 | 97.9 |
| 1496 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | certified | 745.1 | 88.1 |
| 1532 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | certified | 851.4 | 91.2 |
| 1568 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 490.9 | 72.9 |
| 1604 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 603.6 | 79.8 |
| 1640 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1-8s0-9s0-10s0` | certified | 671.7 | 82.9 |
| 1676 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s1-9s0-10s0` | certified | 830.8 | 94.1 |
| 1712 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0-8s0-9s0-10s0` | certified | 675.5 | 81.4 |
| 1748 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1784 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s0-9s0-10s0` | certified | 742.7 | 88.9 |
| 1820 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s1-9s0-10s0` | certified | 869.8 | 98.0 |
| 1856 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 555.8 | 72.9 |
| 1892 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s1-9s0-10s0` | certified | 815.4 | 92.9 |

The timed-out unit `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s1-9s0-10s0` (row 1748) has its layer-split record (`"split": true, "children": 45`) in `out.jsonl`. Its 45 children were not solved (`open_frontier` 45, `unsplittable` 0), as the task intends.

## Totals per root

| root | units | certified | timed out at 900 | not reached |
|------|-------|-----------|------------------|-------------|
| `0s0_1` | 14 | 14 | 0 | 0 |
| `0s0_2` | 14 | 14 | 0 | 0 |
| `0s0_3` | 15 | 15 | 0 | 0 |
| `0s0_4` | 10 | 9 | 1 | 0 |
| total | 53 | 52 | 1 | 0 |

## Totals per parent six-bit cube

Each of the 53 parents has exactly one unit on this machine (its other 7 units are on other shards). All units on this machine were certified for 52 of the 53 parents, every parent except `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0`.

| parent | units | certified | timed out at 900 | not reached |
|--------|-------|-----------|------------------|-------------|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |

## Solve-time distribution of the 52 certified units

min 412.1 s, Q1 578.0 s, median 670.9 s, Q3 787.3 s, p90 856.9 s, max 879.3 s. All 52 were certified above 300 s. Check time (both checkers): 69.9–116.2 s, median 91.2 s. Largest proof 1.28 GB. Totals: 35,045 s solve, 4,715 s check.

## SAT / rejections / memory / early ends

- SAT: none.
- PROOF NOT ACCEPTED: none. Every certified record has `c VERIFIED` and `s VERIFIED UNSAT`. There was no `cake_lpr: none`, and no `recheck.jsonl`.
- Memory: no problem. Free memory never went below about 3 GB at the checks I made.
- No unit ended in under 72 s without a certificate.

## Files

`env.txt`, `tools.txt`, `units.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (lane 0, 1, 2: 54 records, 53 solve records and 1 split record), `driver{0,1,2}.log.tail`.

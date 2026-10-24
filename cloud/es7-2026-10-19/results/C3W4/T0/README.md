# C3W4 / T0: wave 4, W4_two.tsv shard 0 of 4

**Result: 36 of my 44 roots are closed, 1 is partial (`0s0-5s1_2s0-3s1`, open frontier 8), and 7 were not reached. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:15 UTC, END 15:16:15 UTC (start + 4 h − 15 min), 2026-10-24. TASK.md commit 3fd8a4d8. Details are in `tools.txt`.

- Tools: worktree of 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified. `compose.py` was not run, as the task says.
- CaDiCaL c6073042 (3.0.1); cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. **Matches.**
- Roots: the rows of `W4_two.tsv` with row ≡ 0 (mod 4), 44 roots (`roots.tsv`). None were seeded; every root started fresh.
- Runner `runner.sh`: `close_tree.py … --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(1.0, left)`.

## Outcome

- 134 certified nodes. Every one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, and none has cake_lpr `none`.
- 15 timeouts, all of them a root's direct attempt at 300 s. Each of those 15 roots was σ-split on 3 bits into 8 cubes. There are 15 split records, each with `children` 8; none has `children` 0.
- Of the 14 roots that were σ-split and finished, every cube was certified at the 300 s cap (σ level 1). No cube needed a second σ level or the layer split. The other 22 closed roots were certified directly at depth 2. The last root, `0s0-5s1_2s0-3s1`, was cut off by END: it timed out and was split, but none of its 8 cubes was attempted (it got only a 0.022 h slice).
- In the table, d2/s0 means the root itself was certified directly, and d2/s1 means the 8 σ-cubes on 3 bits were certified. Solve and check seconds are summed per node; with 3 jobs on 4 cores they are not wall-clock time.

| row | root | stratum | list status | result | open frontier | certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0s0-3s1_1s0-5s1 | H6(3,1)/two | partial | **closed** | 0 | d2/s1: 8 | 1 | 1349 | 372 |
| 4 | 0s0-3s1_4s0-6s1 | H6(3,1)/two | partial | **closed** | 0 | d2/s1: 8 | 1 | 1717 | 374 |
| 8 | 0s0-4s0_1s0-5s1 | H6(4,0)/two | partial | **closed** | 0 | d2/s1: 8 | 1 | 847 | 348 |
| 12 | 0s0-4s1_1s1-5s0 | H6(4,1)/two | partial | **closed** | 0 | d2/s1: 8 | 1 | 1219 | 359 |
| 16 | 0s0-5s0_1s0-2s1 | H6(5,0)/two | partial | **closed** | 0 | d2/s1: 8 | 1 | 912 | 325 |
| 20 | 0s0-5s0_1s1-3s0 | H6(5,0)/two | partial | **closed** | 0 | d2/s1: 8 | 1 | 872 | 319 |
| 24 | 0s0-5s0_7s1-8s0 | H6(5,0)/two | partial | **closed** | 0 | d2/s1: 8 | 1 | 754 | 295 |
| 28 | 0s0-2s0_3s1-6s0 | H6(2,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 98 | 31 |
| 32 | 0s0-2s0_4s0-6s0 | H6(2,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 6 | 18 |
| 36 | 0s0-3s1_4s1-8s0 | H6(3,1)/two | untouched | **closed** | 0 | d2/s1: 8 | 1 | 912 | 317 |
| 40 | 0s0-3s1_5s1-6s0 | H6(3,1)/two | untouched | **closed** | 0 | d2/s1: 8 | 1 | 1765 | 378 |
| 44 | 0s0-3s1_6s1-8s1 | H6(3,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 37 | 31 |
| 48 | 0s0-4s0_2s0-6s1 | H6(4,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 278 | 52 |
| 52 | 0s0-4s1_1s0-5s0 | H6(4,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 34 | 28 |
| 56 | 0s0-4s1_1s1-10s0 | H6(4,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 41 | 34 |
| 60 | 0s0-4s1_1s1-8s0 | H6(4,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 43 | 30 |
| 64 | 0s0-4s1_2s0-5s0 | H6(4,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 36 | 30 |
| 68 | 0s0-4s1_2s0-7s1 | H6(4,1)/two | untouched | **closed** | 0 | d2/s1: 8 | 1 | 1079 | 328 |
| 72 | 0s0-4s1_5s0-7s0 | H6(4,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 38 | 32 |
| 76 | 0s0-4s1_5s0-9s1 | H6(4,1)/two | untouched | **closed** | 0 | d2/s1: 8 | 1 | 1081 | 361 |
| 80 | 0s0-4s1_5s1-7s1 | H6(4,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 36 | 27 |
| 84 | 0s0-4s1_6s1-7s0 | H6(4,1)/two | untouched | **closed** | 0 | d2/s1: 8 | 1 | 1607 | 393 |
| 88 | 0s0-4s1_6s1-9s1 | H6(4,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 38 | 28 |
| 92 | 0s0-5s0_1s0-8s1 | H6(5,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 42 | 26 |
| 96 | 0s0-5s0_1s1-10s1 | H6(5,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 233 | 43 |
| 100 | 0s0-5s0_2s0-7s1 | H6(5,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 213 | 42 |
| 104 | 0s0-5s0_2s0-9s1 | H6(5,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 38 | 28 |
| 108 | 0s0-5s0_6s0-9s0 | H6(5,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 9 | 17 |
| 112 | 0s0-5s0_6s1-7s1 | H6(5,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 20 | 24 |
| 116 | 0s0-5s0_6s1-9s1 | H6(5,0)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 27 | 27 |
| 120 | 0s0-5s1_1s0-10s1 | H6(5,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 54 | 31 |
| 124 | 0s0-5s1_1s0-6s0 | H6(5,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 134 | 37 |
| 128 | 0s0-5s1_1s0-8s1 | H6(5,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 68 | 31 |
| 132 | 0s0-5s1_1s1-2s0 | H6(5,1)/two | untouched | **closed** | 0 | d2/s1: 8 | 1 | 1301 | 352 |
| 136 | 0s0-5s1_1s1-7s0 | H6(5,1)/two | untouched | **closed** | 0 | d2/s0: 1 | 0 | 161 | 35 |
| 140 | 0s0-5s1_1s1-9s1 | H6(5,1)/two | untouched | **closed** | 0 | d2/s1: 8 | 1 | 1585 | 362 |
| 144 | 0s0-5s1_2s0-3s1 | H6(5,1)/two | untouched | **partial** | 8 | – | 1 | 300 | 0 |
| 148 | 0s0-5s1_2s0-9s0 | H6(5,1)/two | untouched | **not reached** | - | – | 0 | 0 | 0 |
| 152 | 0s0-5s1_2s1-6s0 | H6(5,1)/two | untouched | **not reached** | - | – | 0 | 0 | 0 |
| 156 | 0s0-5s1_2s1-9s0 | H6(5,1)/two | untouched | **not reached** | - | – | 0 | 0 | 0 |
| 160 | 0s0-5s1_6s0-7s0 | H6(5,1)/two | untouched | **not reached** | - | – | 0 | 0 | 0 |
| 164 | 0s0-5s1_6s1-7s1 | H6(5,1)/two | untouched | **not reached** | - | – | 0 | 0 | 0 |
| 168 | 0s0-5s1_6s1-9s1 | H6(5,1)/two | untouched | **not reached** | - | – | 0 | 0 | 0 |
| 172 | 0s0-5s1_7s1-8s0 | H6(5,1)/two | untouched | **not reached** | - | – | 0 | 0 | 0 |

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(2,0)/two | 2 | 2 | 0 | 0 | 2 | 0 | 104 | 49 |
| H6(3,1)/two | 5 | 5 | 0 | 0 | 33 | 4 | 5781 | 1472 |
| H6(4,0)/two | 2 | 2 | 0 | 0 | 9 | 1 | 1125 | 400 |
| H6(4,1)/two | 11 | 11 | 0 | 0 | 39 | 4 | 5253 | 1650 |
| H6(5,0)/two | 10 | 10 | 0 | 0 | 31 | 3 | 3121 | 1147 |
| H6(5,1)/two | 14 | 6 | 1 | 7 | 20 | 3 | 3602 | 848 |
| **total** | 44 | 36 | 1 | 7 | 134 | 15 | 18987 | 5566 |

All 7 roots marked `partial` in the list closed from a fresh start in 10–17 minutes each, through 8 σ-cubes.

Not reached: 0s0-5s1_2s0-9s0, 0s0-5s1_2s1-6s0, 0s0-5s1_2s1-9s0, 0s0-5s1_6s0-7s0, 0s0-5s1_6s1-7s1, 0s0-5s1_6s1-9s1, 0s0-5s1_7s1-8s0.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. No re-checks were needed, so there is no `recheck.jsonl`.
- Memory: no problem. At most about 9 GB of the 15 GB was in use.
- Pushes: a few non-fast-forward races with other machines; each succeeded within 4 tries. The fallback branch was not used.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records), `driver.log.tail`, `summary.txt`.

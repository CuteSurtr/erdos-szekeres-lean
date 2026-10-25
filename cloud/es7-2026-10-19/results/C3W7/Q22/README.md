# C3W7 Q22: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv, shard 22 of 36)

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:34 UTC on 2026-10-25, lanes started 10:50:44, END 15:01:34 (start + 4.5 h − 15 min); the lanes were killed at 15:01:42.

## Tools and base CNF (`tools.txt`)

- C3U2 tools: worktree of `cad4e050` at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 `c60730422e758ef1cebe7aeddf2dda31c996bf04`; cake_lpr `a36874a8` (its example prints `s VERIFIED UNSAT`); drat-trim lrat-check `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` with `results/E2/tools/lrat-check-E2.patch`. Sanity test passed: on {1},{−1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

## Run

The units are the 53 rows of `lists/W7.tsv` with row ≡ 22 (mod 36) (`units.tsv`), with no seeded records. They ran in 3 lanes (`lane0.sh`, `lane1.sh`, `lane2.sh`, lane k = positions ≡ k mod 3). Each unit was run with `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.

## Result: no unit certified

- **Certified: 0.** No unit was certified, so there is no solve-time distribution (0 certified above 300 s), and no parent had all of its units here certified.
- **Timed out at 900: 48.** Each solve hit the cap (solve_s 900.1–900.4). Each one has its layer-split record (`"split": true, "children": 45`), with the 45 children unsolved and in `open_frontier` (45 each, 0 unsplittable).
- **Killed at END: 3.** These units were started at about 14:51 and killed at 15:01:42 before the solve finished, so they have no record (positions 48, 49, 50).
- **Not reached: 2** (positions 51, 52).
- No SAT, no proof rejection, no checker `none` and no recheck (`recheck.jsonl` does not exist). There were no memory problems: about 2.5 GB was in use throughout. No unit ended early: every finished solve ran the full 900 s.

This is not what `results/C3H1/X1` saw: there, the 8 nine-bit cubes of one six-bit cube closed in 450–662 s. Here, none of 48 nine-bit cubes from 46 different six-bit parents closed in 900 s with 3 solves running at once on 4 cores. At cap 900, the nine-bit cubes of these roots look mostly out of reach.

## Per unit

| pos | row | lane | unit | result |
|---|---|---|---|---|
| 0 | 22 | 0 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 1 | 58 | 1 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 2 | 94 | 2 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 3 | 130 | 0 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 4 | 166 | 1 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 5 | 202 | 2 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 6 | 238 | 0 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 7 | 274 | 1 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 8 | 310 | 2 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 9 | 346 | 0 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 10 | 382 | 1 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 11 | 418 | 2 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 12 | 454 | 0 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 13 | 490 | 1 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 14 | 526 | 2 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 15 | 562 | 0 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 16 | 598 | 1 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 17 | 634 | 2 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 18 | 670 | 0 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 19 | 706 | 1 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 20 | 742 | 2 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 21 | 778 | 0 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 22 | 814 | 1 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 23 | 850 | 2 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 24 | 886 | 0 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 25 | 922 | 1 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 26 | 958 | 2 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 27 | 994 | 0 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 28 | 1030 | 1 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 29 | 1066 | 2 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 30 | 1102 | 0 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 31 | 1138 | 1 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 32 | 1174 | 2 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.3 s) |
| 33 | 1210 | 0 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 34 | 1246 | 1 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 35 | 1282 | 2 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 36 | 1318 | 0 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 37 | 1354 | 1 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 38 | 1390 | 2 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 39 | 1426 | 0 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 40 | 1462 | 1 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 41 | 1498 | 2 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.4 s) |
| 42 | 1534 | 0 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 43 | 1570 | 1 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 44 | 1606 | 2 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (solve 900.1 s) |
| 45 | 1642 | 0 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 46 | 1678 | 1 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 47 | 1714 | 2 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (solve 900.2 s) |
| 48 | 1750 | 0 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s1-9s1-10s0` | started, killed at END (no record) |
| 49 | 1786 | 1 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s0-9s1-10s0` | started, killed at END (no record) |
| 50 | 1822 | 2 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s1-9s1-10s0` | started, killed at END (no record) |
| 51 | 1858 | 0 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s0-9s1-10s0` | not reached |
| 52 | 1894 | 1 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s1-9s1-10s0` | not reached |

Per root:

| root | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| 0s0_1 | 14 | 0 | 14 | 0 | 0 |
| 0s0_2 | 14 | 0 | 14 | 0 | 0 |
| 0s0_3 | 15 | 0 | 15 | 0 | 0 |
| 0s0_4 | 10 | 0 | 5 | 3 | 2 |

Per parent six-bit cube:

| parent | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0` | 1 | 0 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0` | 1 | 0 | 0 | 0 | 1 |

Parents all of whose units here were certified: none

Certified solve times: none certified

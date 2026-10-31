# C3W7 / Q10: nine-bit σ-cubes of the H3/one roots, shard 10 of 36 of W7.tsv

**Result: 2 of 53 units certified, 46 timed out at 900 s, 3 still running when END killed them, 2 never reached. No SAT, no proof rejection, no memory problem, and no unit ended early.**

## Setup
- Tools are from a worktree of cad4e050 at `/opt/c3u2` (C3U2 tools, unmodified). CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 and lrat-check 2e3b2dc with the E2 patch all built. The checker sanity test passed: `3 0 0` was rejected by both checkers and `3 0 1 2 0` was accepted by both. The cake_lpr example printed `s VERIFIED UNSAT`. Details are in `tools.txt`.
- Base CNF: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`. Both match.
- Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start was 10:46:11 UTC, the lanes started at 10:49:23 and END was 15:01:11 UTC. At END all three lanes were killed as whole process groups.
- Units: the rows of `lists/W7.tsv` with row ≡ 10 (mod 36), 53 units in `units.tsv`. There were 3 lanes (`lane.sh`, `lane0-2.sh`) running `close_tree.py … --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. No records were seeded. `compose.py` was not run.
- Each timed-out unit has its layer-split record (45 children, unsolved) in `out.jsonl`, as intended.

## Summary
- Certified: 2. Solve times were 689.0 s and 894.4 s, with checks of 98.6 s and 109.9 s. Both proofs passed lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. With only 2 certified units, the distribution is min 689.0, max 894.4, and both were above 300 s. Quartiles and p90 are not meaningful with n = 2.
- Timed out at 900 s: 46.
- Killed at END while still running, with no record: 3 (lane units of root `0s0_4`).
- Not reached: 2.
- SAT: none. PROOF NOT ACCEPTED: none, and no recheck was needed, so there is no `recheck.jsonl`. No checker was killed at END: the 3 killed units were still in the solve phase. Memory use stayed around 2 GB.
- A note on speed: here the nine-bit cubes are far harder than in the C3H1/X1 pilot, where they took 450–662 s. Only 2 of 51 finished units closed at the 900 s cap.

## Per unit

| pos | lane | row | unit | parent | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 10 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | certified | 894.4 | 109.9 |
| 1 | 1 | 46 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1` | timed out at 900 | 900.1 |  |
| 2 | 2 | 82 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0` | timed out at 900 | 900.1 |  |
| 3 | 0 | 118 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0` | timed out at 900 | 900.1 |  |
| 4 | 1 | 154 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1` | timed out at 900 | 900.1 |  |
| 5 | 2 | 190 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1` | timed out at 900 | 900.1 |  |
| 6 | 0 | 226 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0` | timed out at 900 | 900.1 |  |
| 7 | 1 | 262 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0` | timed out at 900 | 900.1 |  |
| 8 | 2 | 298 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1` | timed out at 900 | 900.1 |  |
| 9 | 0 | 334 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1` | timed out at 900 | 900.1 |  |
| 10 | 1 | 370 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0` | timed out at 900 | 900.1 |  |
| 11 | 2 | 406 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0` | timed out at 900 | 900.1 |  |
| 12 | 0 | 442 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1` | timed out at 900 | 900.1 |  |
| 13 | 1 | 478 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1` | timed out at 900 | 900.1 |  |
| 14 | 2 | 514 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` | certified | 689.0 | 98.6 |
| 15 | 0 | 550 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0` | timed out at 900 | 900.1 |  |
| 16 | 1 | 586 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1` | timed out at 900 | 900.1 |  |
| 17 | 2 | 622 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1` | timed out at 900 | 900.1 |  |
| 18 | 0 | 658 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | timed out at 900 | 900.1 |  |
| 19 | 1 | 694 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0` | timed out at 900 | 900.1 |  |
| 20 | 2 | 730 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1` | timed out at 900 | 900.1 |  |
| 21 | 0 | 766 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1` | timed out at 900 | 900.1 |  |
| 22 | 1 | 802 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0` | timed out at 900 | 900.1 |  |
| 23 | 2 | 838 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0` | timed out at 900 | 900.1 |  |
| 24 | 0 | 874 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1` | timed out at 900 | 900.1 |  |
| 25 | 1 | 910 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1` | timed out at 900 | 900.1 |  |
| 26 | 2 | 946 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0` | timed out at 900 | 900.1 |  |
| 27 | 0 | 982 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0` | timed out at 900 | 900.1 |  |
| 28 | 1 | 1018 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1` | timed out at 900 | 900.1 |  |
| 29 | 2 | 1054 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1` | timed out at 900 | 900.1 |  |
| 30 | 0 | 1090 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0` | timed out at 900 | 900.1 |  |
| 31 | 1 | 1126 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0` | timed out at 900 | 900.1 |  |
| 32 | 2 | 1162 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1` | timed out at 900 | 900.1 |  |
| 33 | 0 | 1198 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1` | timed out at 900 | 900.2 |  |
| 34 | 1 | 1234 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0` | timed out at 900 | 900.1 |  |
| 35 | 2 | 1270 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0` | timed out at 900 | 900.1 |  |
| 36 | 0 | 1306 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1` | timed out at 900 | 900.1 |  |
| 37 | 1 | 1342 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1` | timed out at 900 | 900.1 |  |
| 38 | 2 | 1378 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0` | timed out at 900 | 900.1 |  |
| 39 | 0 | 1414 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0` | timed out at 900 | 900.1 |  |
| 40 | 1 | 1450 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1` | timed out at 900 | 900.1 |  |
| 41 | 2 | 1486 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1` | timed out at 900 | 900.1 |  |
| 42 | 0 | 1522 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0` | timed out at 900 | 900.1 |  |
| 43 | 1 | 1558 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0-8s1-9s1-10s0` | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0` | timed out at 900 | 900.1 |  |
| 44 | 2 | 1594 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1-8s0-9s1-10s0` | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1` | timed out at 900 | 900.1 |  |
| 45 | 0 | 1630 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1-8s1-9s1-10s0` | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1` | timed out at 900 | 900.1 |  |
| 46 | 1 | 1666 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0-8s0-9s1-10s0` | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0` | timed out at 900 | 900.1 |  |
| 47 | 2 | 1702 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0-8s1-9s1-10s0` | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0` | timed out at 900 | 900.1 |  |
| 48 | 0 | 1738 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s0-9s1-10s0` | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1` | not finished (killed at END) |  |  |
| 49 | 1 | 1774 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s1-9s1-10s0` | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1` | not finished (killed at END) |  |  |
| 50 | 2 | 1810 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s0-9s1-10s0` | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0` | not finished (killed at END) |  |  |
| 51 | 0 | 1846 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s1-9s1-10s0` | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | not reached |  |  |
| 52 | 1 | 1882 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s0-9s1-10s0` | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | not reached |  |  |

| root | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1` | 14 | 1 | 13 | 0 | 0 |
| `0s0_2` | 15 | 1 | 14 | 0 | 0 |
| `0s0_3` | 14 | 0 | 14 | 0 | 0 |
| `0s0_4` | 10 | 0 | 5 | 3 | 2 |

| parent six-bit cube | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | 1 | 0 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | 1 | 0 | 0 | 0 | 1 |

Parents all of whose units here were certified: `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1`, `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0`


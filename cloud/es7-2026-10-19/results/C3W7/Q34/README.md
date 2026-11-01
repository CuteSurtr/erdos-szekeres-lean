# C3W7 Q34: nine-bit σ-cubes of the H3/one roots, shard 34 of 36 of W7.tsv

Task: `results/C3W7/TASK.md` at 39bb1bac with V = Q34, LIST = W7.tsv, j = 34, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:05 UTC on 2026-10-25, END 15:01:05 UTC. At END the three lanes were killed (whole process groups).

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (the example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc0 with the E2 patch. Sanity test: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.

## Run

There were 53 units: rows ≡ 34 (mod 36) of `W7.tsv` (`units.tsv`). Three lanes (`lane0.sh`–`lane2.sh`, which exec `lane.sh K`) ran `close_tree.py … --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. Nothing was seeded.

**Totals: 1 certified, 47 timed out at 900 s, 3 killed at END (started at 14:49–14:51 and cut off before they could reach the cap), 2 not reached.**

- No SAT, no `PROOF NOT ACCEPTED`, no `cake_lpr: none`, so `recheck.jsonl` was not needed.
- No unit ended early: every solve took between 879.3 and 900.2 s.
- No memory problem: at most about 2–3 GB was in use.
- Each timed-out unit has its layer-split record in `out.jsonl`, with 45 children each. As the task intends, those children are unsolved and in `open_frontier`.
- Certified solve times: there is only one value, 879.3 s, so min = quartiles = p90 = max = 879.3 s. That is 1 unit certified above 300 s. Its check took 101.2 s.
- Parents with all of their units on this machine certified: only `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1`, which has 1 unit here.

The cap of 900 s is too short for these cubes on this VM. 47 of the 48 solves that ran to completion timed out at 900 s, and the one that was certified needed 879 s. That contrasts with the 450–662 s reported in `C3H1/X1`.

## Per root

| root | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1` | 14 | 0 | 14 | 0 | 0 |
| `0s0_2` | 14 | 0 | 14 | 0 | 0 |
| `0s0_3` | 14 | 0 | 14 | 0 | 0 |
| `0s0_4` | 11 | 1 | 5 | 3 | 2 |

## Per parent six-bit cube

| parent six-bit cube | units | certified | timed out | killed at END | not reached |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1` | 1 | 0 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0` | 1 | 0 | 0 | 0 | 1 |

## Per unit

| row | lane | unit | result |
|---|---|---|---|
| 34 | 0 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 70 | 1 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 106 | 2 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 142 | 0 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 178 | 1 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 214 | 2 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 250 | 0 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 286 | 1 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 322 | 2 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 358 | 0 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 394 | 1 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 430 | 2 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 466 | 0 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 502 | 1 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 538 | 2 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 574 | 0 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 610 | 1 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 646 | 2 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 682 | 0 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 718 | 1 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 754 | 2 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 790 | 0 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 826 | 1 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 862 | 2 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 898 | 0 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 934 | 1 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 970 | 2 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1006 | 0 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1042 | 1 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1078 | 2 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1114 | 0 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1150 | 1 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1186 | 2 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1222 | 0 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1258 | 1 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1294 | 2 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1330 | 0 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1366 | 1 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (900.2 s); layer split written |
| 1402 | 2 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1438 | 0 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1474 | 1 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1510 | 2 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1546 | 0 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified (solve 879.3 s, check 101.2 s) |
| 1582 | 1 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1618 | 2 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1654 | 0 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1690 | 1 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1726 | 2 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 (900.1 s); layer split written |
| 1762 | 0 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s0-8s0-9s1-10s0` | killed at END (started, no record) |
| 1798 | 1 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s0-8s1-9s1-10s0` | killed at END (started, no record) |
| 1834 | 2 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s1-8s0-9s1-10s0` | killed at END (started, no record) |
| 1870 | 0 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s1-8s1-9s1-10s0` | not reached |
| 1906 | 1 | `0s0_4__1s1-2s0-3s1-5s1-6s1-7s0-8s0-9s1-10s0` | not reached |


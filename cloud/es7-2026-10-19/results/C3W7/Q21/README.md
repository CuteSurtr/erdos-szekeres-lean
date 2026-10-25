# C3W7 Q21: nine-bit σ-cubes of the H3/one roots, shard 21 of 36 of W7.tsv

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q21, LIST = W7.tsv, j = 21, N = 36, H = 4.5.
One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:32 UTC, lanes started 10:49:34, END 15:01:32 UTC (lanes killed 15:01:43).

## Tools and base check (`tools.txt`)

- C3U2 tools at cad4e050 (worktree `/opt/c3u2`), unmodified; `compose.py` not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc + E2 patch.
  Sanity test passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, matches.

## Summary

53 units (rows ≡ 21 mod 36 of W7.tsv, one unit from each of 53 parent six-bit cubes), 3 lanes, `--jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`, no records seeded.

- **19 certified** (both checkers: lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`).
- **32 timed out at 900 s.** Each one got its layer-split record (45 children each, unsolved, in `open_frontier`; no unsplittable nodes, no `"children": 0` records).
- **2 not finished.** Their solves were started at 14:54:57 and 14:57:16 and killed at END, so they have no record: `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s0-9s0-10s1` and `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s1-9s0-10s1`.
- No SAT. No `PROOF NOT ACCEPTED`. No certified-looking record with cake_lpr `none`, so no re-checks were needed and there is no `recheck.jsonl`. No memory problem: at most about 6 GB of 15 GB was used. No unit ended early, so no solve ended in under 72 s without a certificate.

Solve times of the 19 certified units: min 582.9, Q1 644.4, median 729.0, Q3 772.3, p90 809.3, max 888.4 s. All 19 were above 300 s. Check times were 85–126 s per unit.
Solve time over all 51 records was 42,430 s and check time 2,015 s. These are per-node times, with 3 lanes sharing 4 cores.

## Totals per root

| root | units | certified | timed out at 900 | not finished |
|---|---|---|---|---|
| 0s0_1 | 14 | 6 | 8 | 0 |
| 0s0_2 | 14 | 5 | 9 | 0 |
| 0s0_3 | 15 | 6 | 9 | 0 |
| 0s0_4 | 10 | 2 | 6 | 2 |
| total | 53 | 19 | 32 | 2 |

## Per parent six-bit cube

Each parent has exactly one unit on this machine, so the per-unit table below is also the per-parent table.
These 19 parents had all their units on this machine certified (their 7 other nine-bit cubes are on other machines):

- `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0`
- `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1`
- `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0`
- `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0`
- `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1`
- `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0`
- `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1`
- `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0`
- `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0`
- `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1`
- `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0`
- `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0`
- `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1`
- `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1`
- `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0`
- `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0`
- `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0`
- `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0`
- `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1`

## Per unit (lane = position mod 3)

| pos | lane | unit | parent six-bit cube | root | result | solve s | check s |
|---|---|---|---|---|---|---|---|
| 0 | 0 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0` | 0s0_1 | certified | 654.6 | 115.5 |
| 1 | 1 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1` | 0s0_1 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 2 | 2 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1` | 0s0_1 | certified | 772.3 | 126.1 |
| 3 | 0 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0` | 0s0_1 | certified | 582.9 | 103.7 |
| 4 | 1 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0` | 0s0_1 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 5 | 2 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1` | 0s0_1 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 6 | 0 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1` | 0s0_1 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 7 | 1 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0` | 0s0_1 | certified | 658.6 | 105.3 |
| 8 | 2 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0` | 0s0_1 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 9 | 0 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1` | 0s0_1 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 10 | 1 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1` | 0s0_1 | certified | 793.9 | 107.5 |
| 11 | 2 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0` | 0s0_1 | certified | 768.0 | 105.5 |
| 12 | 0 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0` | 0s0_1 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 13 | 1 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1` | 0s0_1 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 14 | 2 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1` | 0s0_2 | certified | 633.0 | 103.4 |
| 15 | 0 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0` | 0s0_2 | certified | 762.6 | 114.4 |
| 16 | 1 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 17 | 2 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 18 | 0 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 19 | 1 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0` | 0s0_2 | certified | 729.0 | 105.7 |
| 20 | 2 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 21 | 0 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1` | 0s0_2 | certified | 715.2 | 111.8 |
| 22 | 1 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 23 | 2 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 24 | 0 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 25 | 1 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 26 | 2 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1` | 0s0_2 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 27 | 0 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0` | 0s0_2 | certified | 739.0 | 113.8 |
| 28 | 1 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0` | 0s0_3 | certified | 594.3 | 85.4 |
| 29 | 2 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1` | 0s0_3 | certified | 760.3 | 101.2 |
| 30 | 0 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1` | 0s0_3 | certified | 712.8 | 97.1 |
| 31 | 1 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 32 | 2 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0` | 0s0_3 | certified | 809.3 | 101.1 |
| 33 | 0 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 34 | 1 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 35 | 2 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0` | 0s0_3 | certified | 644.4 | 97.5 |
| 36 | 0 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0` | 0s0_3 | certified | 888.4 | 117.1 |
| 37 | 1 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 38 | 2 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 39 | 0 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 40 | 1 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 41 | 2 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 42 | 0 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1` | 0s0_3 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 43 | 1 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0` | 0s0_4 | certified | 623.6 | 94.5 |
| 44 | 2 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0` | 0s0_4 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 45 | 0 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1` | 0s0_4 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 46 | 1 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1` | 0s0_4 | certified | 784.2 | 108.7 |
| 47 | 2 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0` | 0s0_4 | timed out at 900 (layer split, 45 children open) | 900.2 | – |
| 48 | 0 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0` | 0s0_4 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 49 | 1 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1` | 0s0_4 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 50 | 2 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1` | 0s0_4 | timed out at 900 (layer split, 45 children open) | 900.1 | – |
| 51 | 0 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0` | 0s0_4 | not reached (solve killed at END, no record) | – | – |
| 52 | 1 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0` | 0s0_4 | not reached (solve killed at END, no record) | – | – |


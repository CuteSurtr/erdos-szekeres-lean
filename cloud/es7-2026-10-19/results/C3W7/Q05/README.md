# C3W7 / Q05: nine-bit σ-cubes of the H3/one roots, shard 5 of 36 of `W7.tsv`

**Result: none of my 53 units was certified. 48 timed out at the 900 s cap, 3 were running when the lanes were stopped at END, and 2 were not started. No SAT, no proof rejection, no memory problem, and no unit ended early.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:35 UTC on 2026-10-25, END 15:01:35 UTC (start + 4.5 h − 15 min). Task: `results/C3W7/TASK.md` at 39bb1bac.

- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools`, used unmodified.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc0 with the E2 patch. Sanity test on {1},{-1}: LRAT `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches. Details are in `tools.txt`.
- Units: the rows of `lists/W7.tsv` with row ≡ 5 (mod 36), 53 nine-bit cubes (`units.tsv`). Nothing was seeded. Three lanes (`lane0.sh` to `lane2.sh`, each under `setsid nohup`); lane k ran positions ≡ k (mod 3) with `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
- At END, all three lane process groups were killed. compose.py was not run.

## Per unit

| pos | lane | row | unit | result |
|-----|------|-----|------|--------|
| 0 | 0 | 5 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 1 | 1 | 41 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 2 | 2 | 77 | `0s0_1__2s0-3s0-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 3 | 0 | 113 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 4 | 1 | 149 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 5 | 2 | 185 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 6 | 0 | 221 | `0s0_1__2s0-3s1-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 7 | 1 | 257 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 8 | 2 | 293 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 9 | 0 | 329 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 10 | 1 | 365 | `0s0_1__2s1-3s0-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 11 | 2 | 401 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 12 | 0 | 437 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 13 | 1 | 473 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 14 | 2 | 509 | `0s0_1__2s1-3s1-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 15 | 0 | 545 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 16 | 1 | 581 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 17 | 2 | 617 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 18 | 0 | 653 | `0s0_2__1s0-3s1-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 19 | 1 | 689 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 20 | 2 | 725 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 21 | 0 | 761 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 22 | 1 | 797 | `0s0_2__1s1-3s0-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 23 | 2 | 833 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 24 | 0 | 869 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 25 | 1 | 905 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 26 | 2 | 941 | `0s0_2__1s1-3s1-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 27 | 0 | 977 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 28 | 1 | 1013 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 29 | 2 | 1049 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 30 | 0 | 1085 | `0s0_3__1s0-2s0-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 31 | 1 | 1121 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 32 | 2 | 1157 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 33 | 0 | 1193 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 34 | 1 | 1229 | `0s0_3__1s0-2s1-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 35 | 2 | 1265 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 36 | 0 | 1301 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 37 | 1 | 1337 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 38 | 2 | 1373 | `0s0_3__1s1-2s0-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 39 | 0 | 1409 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 40 | 1 | 1445 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 41 | 2 | 1481 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 42 | 0 | 1517 | `0s0_3__1s1-2s1-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 43 | 1 | 1553 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 44 | 2 | 1589 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s0-8s1-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 45 | 0 | 1625 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 46 | 1 | 1661 | `0s0_4__1s0-2s0-3s1-5s1-6s1-7s1-8s1-9s0-10s1` | timed out at 900 (900.2 s); layer split, 45 children |
| 47 | 2 | 1697 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0-8s0-9s0-10s1` | timed out at 900 (900.1 s); layer split, 45 children |
| 48 | 0 | 1733 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s0-8s1-9s0-10s1` | not reached (started 14:52, killed at END) |
| 49 | 1 | 1769 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s0-9s0-10s1` | not reached (started 14:52, killed at END) |
| 50 | 2 | 1805 | `0s0_4__1s1-2s0-3s0-5s0-6s0-7s1-8s1-9s0-10s1` | not reached (started 14:52, killed at END) |
| 51 | 0 | 1841 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s0-9s0-10s1` | not reached |
| 52 | 1 | 1877 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s0-8s1-9s0-10s1` | not reached |

Each timed-out unit got its layer-split record: 45 children, unsolved and left in `open_frontier`, as intended. `out.jsonl` holds 96 records: 48 UNKNOWN solve records at cap 900 and 48 split records.

## Totals

| root | units | certified | timed out at 900 | not reached |
|------|-------|-----------|------------------|-------------|
| 0s0_1 | 15 | 0 | 15 | 0 |
| 0s0_2 | 14 | 0 | 14 | 0 |
| 0s0_3 | 14 | 0 | 14 | 0 |
| 0s0_4 | 10 | 0 | 5 | 5 (3 killed at END, 2 not started) |
| **all** | **53** | **0** | **48** | **5** |

Per parent six-bit cube: this machine has exactly one unit for each of 53 different parents (the `parent` column of `units.tsv`). No parent has all of its units on this machine certified, because no unit was certified. Each parent's result is the result of its one unit in the table above.

Solve-time distribution of certified units: none were certified, so there is none (0 certified above 300 s). All 48 solves that finished ran 900.1–900.2 s and returned UNKNOWN.

Note: every unit in this shard has σ bits 9s0-10s1 (8s0 or 8s1), because row ≡ 5 (mod 36) gives row mod 8 ∈ {1, 5}. The shard therefore covers only two of the 8 nine-bit cubes of each parent, both with the same (9, 10) bits, and those cubes may simply be harder than the 450–662 s seen in `results/C3H1/X1`. Three solves ran at once on 4 cores here, which may also slow them compared with that reference.

## SAT / proof rejections / incidents

- SAT: none.
- PROOF NOT ACCEPTED: none. No proof was produced, so no record has cake_lpr `none` and `recheck.jsonl` was not needed.
- Memory: about 2 GB used throughout. No problem.
- No unit ended early: every solve ran the full 900 s.
- The three units started at 14:52 were killed at END mid-solve and have no record.

## Files

`env.txt`, `tools.txt`, `units.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (lane 0, then 1, then 2), `driver0.log.tail`–`driver2.log.tail`, `README.md`.

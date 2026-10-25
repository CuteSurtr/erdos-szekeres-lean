# C3W7 / Q12: nine-bit σ-cubes of the H3/one roots, shard 12 of 36 of W7.tsv

**Result: 9 of my 53 units were certified at cap 900 (both checkers). 40 timed out at 900 s and got their layer-split records (45 children each, left unsolved as intended). 2 units were running when END came and were killed. 2 were not reached. No SAT. No proof rejection. No memory problem. No unit ended early.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:45:51 UTC, END 15:00:51 UTC (H = 4.5). The lanes ran from 10:48 to 15:00:57, when all three process groups were killed.

- Tools: worktree of `cad4e050` at `/opt/c3u2`, TOOLS = `results/C3U2/tools`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 `c60730422e758ef1cebe7aeddf2dda31c996bf04`; cake_lpr `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` (its example gives `s VERIFIED UNSAT`); drat-trim lrat-check `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` with the E2 patch. Sanity test: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches). Details are in `tools.txt`.
- Units: the rows of `C3W7/lists/W7.tsv` with row ≡ 12 (mod 36). That gives 53 nine-bit units (`units.tsv`), no seeding. There are 3 lanes, and lane k takes the units at positions ≡ k (mod 3). Command: `close_tree.py base.cnf out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02` (`lane.sh`, `lane0-2.sh`).
- `out.jsonl` (lanes 0, 1, 2 in order) has 49 records: 9 certified UNSAT, 40 UNKNOWN at 900 s, and 40 layer-split records with 45 children each. No record has cake_lpr `none`. No re-check was needed, so there is no `recheck.jsonl`.

## Per unit

Solve and check times are in seconds. Three solves shared the 4 cores, so the times are inflated compared with a solve run alone.

| row | unit | status | solve s | check s |
|-----|------|--------|---------|---------|
| 12 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 48 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 84 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 120 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.2 | – |
| 156 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 192 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 730.6 | 92.4 |
| 228 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 264 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 675.9 | 92.6 |
| 300 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 336 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 858.0 | 95.6 |
| 372 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 408 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 444 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 480 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 832.4 | 97.3 |
| 516 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 631.3 | 87.1 |
| 552 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 588 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 624 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 660 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 696 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 732 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 768 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 699.7 | 85.4 |
| 804 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 840 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 876 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 912 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 948 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 984 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1020 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1056 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 770.3 | 102.4 |
| 1092 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1128 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1164 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1200 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1236 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1272 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1308 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.4 | – |
| 1344 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 807.4 | 89.4 |
| 1380 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1416 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1452 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1488 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1524 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1560 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s0-9s0-10s0` | certified | 890.2 | 96.6 |
| 1596 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1632 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1668 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1704 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1740 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s1-9s0-10s0` | killed at END | – | – |
| 1776 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s0-9s0-10s0` | killed at END | – | – |
| 1812 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 | – |
| 1848 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s0-9s0-10s0` | not reached | – | – |
| 1884 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s1-9s0-10s0` | not reached | – | – |

## Totals per root

| root | units | certified | timed out at 900 | killed at END | not reached |
|------|-------|-----------|------------------|---------------|-------------|
| 0s0_1 | 14 | 4 | 10 | 0 | 0 |
| 0s0_2 | 15 | 2 | 13 | 0 | 0 |
| 0s0_3 | 14 | 2 | 12 | 0 | 0 |
| 0s0_4 | 10 | 1 | 5 | 2 | 2 |
| **total** | **53** | **9** | **40** | **2** | **2** |

## Per parent six-bit cube

Each of my 53 units has a different parent six-bit cube, so this machine holds one unit (of 8) of each parent. The parents whose only unit here was certified are listed below. None of them is closed by this machine alone, because their other 7 units are on other shards.

- `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0` (unit row 192)
- `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1` (unit row 264)
- `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0` (unit row 336)
- `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0` (unit row 480)
- `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` (unit row 516)
- `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0` (unit row 768)
- `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0` (unit row 1056)
- `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0` (unit row 1344)
- `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1` (unit row 1560)

Parents with a timed-out unit (40), a killed unit (2) or an unreached unit (2) are not closed. Their status is in the table above.

## Solve times of the certified units

There are 9 certified units. Their solve times: min 631.3 s, Q1 699.7 s, median 770.3 s, Q3 832.4 s, p90 864.4 s, max 890.2 s. All 9 were certified above 300 s. Check times were 85–102 s.

## Units not finished

- Killed at END (started too late for 900 s + check): row 1740 `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s1-9s0-10s0`, row 1776 `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s0-9s0-10s0`. They have no record.
- Not reached: row 1848 `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s0-9s0-10s0`, row 1884 `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s1-9s0-10s0`.

## SAT / rejections / incidents

- SAT: none.
- PROOF NOT ACCEPTED: none. All 9 certified records have `c VERIFIED` and `s VERIFIED UNSAT`.
- Memory: at most about 6 GB used. No out-of-memory event.
- Early ends: none. No solve ended in under 72 s without a certificate.

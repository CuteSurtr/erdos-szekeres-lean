# C3W7 Q27: nine-bit σ-cubes of the H3/one roots, shard 27 of 36 of W7.tsv

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q27, LIST = W7.tsv, j = 27, N = 36, H = 4.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:16 UTC on 2026-10-25, lanes started 10:49:03, END 15:01:16 UTC (lanes killed at 15:01:39).

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 (cad4e050d778aa37c9ea23afcbe704c94db3e890), `results/C3U2/tools`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity test: `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

## Run

53 units (`units.tsv`: rows of W7.tsv with row ≡ 27 mod 36), nothing seeded. There were 3 lanes (`lane0.sh` to `lane2.sh`, started with `setsid nohup`), and lane k ran units at positions ≡ k mod 3. Each unit ran `close_tree.py ... --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
`out.jsonl` holds lane 0, then lane 1, then lane 2: 48 solve records and 33 layer-split records (45 children each, left unsolved as intended).

## Outcome

- **15 certified, 33 timed out at 900 s, 5 not reached.** Of the 5 not reached, 3 were in progress at END and were killed before writing a record: `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s0-9s1-10s1`, `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s1-9s1-10s1` and `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s0-9s1-10s1`. The other 2 never started: `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s1-9s1-10s1` and `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s0-9s1-10s1`.
- No SAT. No proof rejection: every UNSAT record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, with no `none`. So there is no `recheck.jsonl`.
- No memory problem: about 2 GB was in use during the run, with about 13 GB available.
- No unit ended early: every timeout ran the full 900 s, and no unit ended in under 72 s without a certificate.
- Every certified unit took more than 300 s to solve (676–893 s), much slower than the 450–662 s of `results/C3H1/X1`. Many nine-bit cubes of these roots do not close at cap 900.

## Per unit

| row | unit | result |
|---|---|---|
| 27 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | certified (solve 756.4 s, check 104.3 s) |
| 63 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 99 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.0 s) |
| 135 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | certified (solve 803.8 s, check 105.4 s) |
| 171 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 207 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 243 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 279 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 315 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 351 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 387 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 423 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 459 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 495 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 531 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | certified (solve 736.7 s, check 99.7 s) |
| 567 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | certified (solve 788.5 s, check 99.2 s) |
| 603 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 639 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | certified (solve 892.8 s, check 90.2 s) |
| 675 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.0 s) |
| 711 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 747 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 783 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | certified (solve 836.2 s, check 104.1 s) |
| 819 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 855 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 891 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 927 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 963 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 999 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1035 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | certified (solve 737.7 s, check 92.7 s) |
| 1071 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | certified (solve 782.8 s, check 87.2 s) |
| 1107 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1143 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | certified (solve 722.8 s, check 88.9 s) |
| 1179 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1215 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | certified (solve 890.8 s, check 99.1 s) |
| 1251 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1287 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | certified (solve 871.4 s, check 91.8 s) |
| 1323 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1359 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1395 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1431 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1467 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1503 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1539 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0-8s0-9s1-10s1` | certified (solve 676.5 s, check 82.3 s) |
| 1575 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0-8s1-9s1-10s1` | certified (solve 750.0 s, check 86.2 s) |
| 1611 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (solve 900.1 s) |
| 1647 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1-8s1-9s1-10s1` | certified (solve 827.0 s, check 89.8 s) |
| 1683 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0-8s0-9s1-10s1` | certified (solve 851.3 s, check 93.6 s) |
| 1719 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (solve 900.3 s) |
| 1755 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s0-9s1-10s1` | not reached |
| 1791 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s1-9s1-10s1` | not reached |
| 1827 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s0-9s1-10s1` | not reached |
| 1863 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s1-9s1-10s1` | not reached |
| 1899 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s0-9s1-10s1` | not reached |

## Totals per root

| root | units | certified | timed out | not reached |
|---|---|---|---|---|
| 0s0_1 | 14 | 2 | 12 | 0 |
| 0s0_2 | 14 | 4 | 10 | 0 |
| 0s0_3 | 14 | 5 | 9 | 0 |
| 0s0_4 | 11 | 4 | 2 | 5 |

## Totals per parent six-bit cube

| parent | units | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 0 | 1 |

Parents all of whose units on this machine were certified (15): `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1`, `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0`, `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0`, `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0`, `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1`, `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1`, `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1`, `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1`, `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0`, `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1`, `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0`, `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0`, `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0`, `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1`, `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0`

## Solve times of certified units

n = 15; min 676.5, Q1 743.9, median 788.5, Q3 843.8, p90 883.0, max 892.8 s; certified above 300 s: 15
Check times: min 82.3, max 105.4 s.

Units ending in under 72 s without a certificate: none

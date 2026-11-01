# C3W7 Q11: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv shard 11 of 36)

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q11, LIST = W7.tsv, j = 11, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:32 UTC, lanes started 10:50:03, END 15:01:32 UTC
(lanes killed at 15:01:35) on 2026-10-25.

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (example prints
  `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`.
  Sanity check on {1},{-1}: LRAT `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).

## Run

53 units (W7.tsv rows ≡ 11 mod 36, `units.tsv`), no records seeded. Three lanes (`lane0.sh`–`lane2.sh`), lane k = positions ≡ k (mod 3),
each unit `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
`out.jsonl` (lane 0, 1, 2) holds 88 records: 48 solve records and 40 layer-split records (one per timed-out unit; children unsolved, as intended).

## Summary

- **8 certified**, **40 timed out at 900 s**, **5 not reached**. Of the 5 not reached, 3 were mid-solve when the lanes were killed at END
  (no record written): `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s0-9s1-10s1`, `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s1-9s1-10s1`,
  `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s0-9s1-10s1`; the other 2 never started.
- Every certified record has lrat-check and cake_lpr `s VERIFIED UNSAT`. No checker was killed mid-check, so there is no `none` to re-check, and no `recheck.jsonl`.
- No SAT, no proof rejection, no memory problem (peak used about 4 GB of 15), no unit ending under 72 s without a certificate.
- The certified solve times run from 674 to 899 s, all above 300 s: n = 8, min 673.8, q1 767.8, median 848.3, q3 856.9, p90 859.3, max 898.7.
  At cap 900 on 3 shared cores, most nine-bit cubes here do not close. That is far slower than the 450–662 s of `results/C3H1/X1`.
- Parents all of whose units on this machine were certified (each has 1 unit here, out of its 8 in W7.tsv):
  `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1`
  `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1`
  `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0`
  `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0`
  `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0`
  `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1`
  `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1`
  `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0`

## Per root

| root | certified | timed out | other | not reached |
|---|---|---|---|---|
| 0s0_1 | 2 | 12 | 0 | 0 |
| 0s0_2 | 1 | 14 | 0 | 0 |
| 0s0_3 | 1 | 13 | 0 | 0 |
| 0s0_4 | 4 | 1 | 0 | 5 |

## Per parent six-bit cube

| parent six-bit cube | certified | timed out | other | not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1` | 1 | 0 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` | 1 | 0 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0` | 1 | 0 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1` | 0 | 1 | 0 | 0 |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0` | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0` | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1` | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1` | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0` | 1 | 0 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0` | 0 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1` | 0 | 0 | 0 | 1 |
| `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1` | 0 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0` | 0 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | 0 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | 0 | 0 | 0 | 1 |

## Per unit

| pos | lane | W7 row | unit | result |
|---|---|---|---|---|
| 0 | 0 | 11 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | certified (solve 775.9 s, check 104.8 s) |
| 1 | 1 | 47 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | certified (solve 848.9 s, check 93.4 s) |
| 2 | 2 | 83 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.0 s) |
| 3 | 0 | 119 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 4 | 1 | 155 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 5 | 2 | 191 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 6 | 0 | 227 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 7 | 1 | 263 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 8 | 2 | 299 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 9 | 0 | 335 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 10 | 1 | 371 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 11 | 2 | 407 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 12 | 0 | 443 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 13 | 1 | 479 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 14 | 2 | 515 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | certified (solve 673.8 s, check 92.1 s) |
| 15 | 0 | 551 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 16 | 1 | 587 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 17 | 2 | 623 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 18 | 0 | 659 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 19 | 1 | 695 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 20 | 2 | 731 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 21 | 0 | 767 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 22 | 1 | 803 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 23 | 2 | 839 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 24 | 0 | 875 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 25 | 1 | 911 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 26 | 2 | 947 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 27 | 0 | 983 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 28 | 1 | 1019 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 29 | 2 | 1055 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 30 | 0 | 1091 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | certified (solve 765.1 s, check 94.0 s) |
| 31 | 1 | 1127 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 32 | 2 | 1163 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 33 | 0 | 1199 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 34 | 1 | 1235 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 35 | 2 | 1271 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 36 | 0 | 1307 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 37 | 1 | 1343 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 38 | 2 | 1379 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 39 | 0 | 1415 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 40 | 1 | 1451 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 41 | 2 | 1487 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 42 | 0 | 1523 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | timed out at 900 (900.1 s) |
| 43 | 1 | 1559 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0-8s1-9s1-10s1` | certified (solve 849.8 s, check 89.1 s) |
| 44 | 2 | 1595 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1-8s0-9s1-10s1` | certified (solve 847.7 s, check 94.7 s) |
| 45 | 0 | 1631 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1-8s1-9s1-10s1` | certified (solve 898.7 s, check 90.2 s) |
| 46 | 1 | 1667 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0-8s0-9s1-10s1` | certified (solve 859.3 s, check 90.3 s) |
| 47 | 2 | 1703 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0-8s1-9s1-10s1` | timed out at 900 (900.1 s) |
| 48 | 0 | 1739 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s0-9s1-10s1` | not reached |
| 49 | 1 | 1775 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s1-9s1-10s1` | not reached |
| 50 | 2 | 1811 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s0-9s1-10s1` | not reached |
| 51 | 0 | 1847 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s1-9s1-10s1` | not reached |
| 52 | 1 | 1883 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s0-9s1-10s1` | not reached |


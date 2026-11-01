# C3W7 Q26: nine-bit σ-cubes of the H3/one roots at cap 900

Task `results/C3W7/TASK.md` at 39bb1bac with V = Q26, LIST = W7.tsv, j = 26, N = 36, H = 4.5. Start 2026-10-25 10:46:26 UTC, lanes started 10:49:19, END 15:01:26 UTC, when all three lanes were killed (whole process groups).

## Tools and base check
- C3U2 tools at cad4e050, unmodified; CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch (sanity: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both). Details in `tools.txt`.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502e…6cd6da`, matches.
- `compose.py` not run.

## Result
53 units (W7.tsv rows ≡ 26 mod 36), 3 lanes, `--sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.

- **18 certified** (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`).
- **32 timed out at 900 s**. Each got its layer-split record (45 children each, unsolved, in `open_frontier`). None was unsplittable.
- **3 started and killed at END** (no record): see the table.
- No SAT. No proof rejection. No re-checks were needed (no `recheck.jsonl`). No checker was killed at END. No unit ended early (under 72 s without a certificate). No memory problem: at most about 5 GB of 15 GB was in use.

## Solve times of the certified units

Certified 18: min 494.0, Q1 669.2, median 780.8, Q3 847.5, p90 883.6, max 897.1; above 300 s: 18

## Per unit

| row | unit | status | solve s | check s |
|---|---|---|---|---|
| 26 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | certified | 817.1 | 107.5 |
| 62 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | certified | 790.2 | 100.7 |
| 98 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | certified | 837.6 | 94.3 |
| 134 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | certified | 672.0 | 100.8 |
| 170 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 206 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 242 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 278 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 314 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 350 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 386 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 642.1 | 91.9 |
| 422 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 458 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 838.9 | 84.3 |
| 494 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1-8s1-9s1-10s0` | certified | 763.0 | 94.6 |
| 530 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s0` | certified | 642.0 | 78.4 |
| 566 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 602 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 638 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 674 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s0` | certified | 883.6 | 105.0 |
| 710 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 746 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s0` | certified | 894.2 | 101.3 |
| 782 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s0` | certified | 873.5 | 92.5 |
| 818 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 854 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 890 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 926 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 962 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 771.4 | 87.1 |
| 998 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1034 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 660.7 | 82.6 |
| 1070 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1106 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1142 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1178 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1214 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1250 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1286 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0-8s1-9s1-10s0` | certified | 758.2 | 88.5 |
| 1322 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1358 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1394 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1430 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1466 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1502 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1538 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0-8s0-9s1-10s0` | certified | 494.0 | 67.1 |
| 1574 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0-8s1-9s1-10s0` | certified | 697.7 | 80.9 |
| 1610 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1-8s0-9s1-10s0` | certified | 798.6 | 85.6 |
| 1646 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1682 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0-8s0-9s1-10s0` | certified | 897.1 | 99.4 |
| 1718 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1754 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s0-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1790 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s1-9s1-10s0` | timed out at 900 | 900.1 |  |
| 1826 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s0-9s1-10s0` | started, killed at END |  |  |
| 1862 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s1-9s1-10s0` | started, killed at END |  |  |
| 1898 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s0-9s1-10s0` | started, killed at END |  |  |

## Totals per root and per parent six-bit cube
| root | units | certified | timed out | killed at END or not reached |
|---|---|---|---|---|
| `0s0_1` | 14 | 7 | 7 | 0 |
| `0s0_2` | 14 | 5 | 9 | 0 |
| `0s0_3` | 14 | 2 | 12 | 0 |
| `0s0_4` | 11 | 4 | 4 | 3 |

| parent | units | certified | timed out | killed at END or not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
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
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 0 | 1 |


(Every parent has exactly one unit on this machine.) Parents all of whose units on this machine were certified:

- `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1`
- `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1`
- `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0`
- `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0`
- `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0`
- `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1`
- `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1`
- `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0`
- `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0`
- `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1`
- `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1`
- `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0`
- `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1`
- `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0`
- `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0`
- `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0`
- `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1`
- `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0`

Files: `units.tsv`, `out.jsonl` (lane 0, 1, 2 records), `driver{0,1,2}.log.tail`, `lane.sh` + `lane{0,1,2}.sh`, `tools.txt`, `env.txt`.

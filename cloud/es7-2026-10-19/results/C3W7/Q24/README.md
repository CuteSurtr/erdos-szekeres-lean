# C3W7 Q24: nine-bit σ-cubes of the H3/one roots, shard 24 of 36 of W7.tsv

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q24, LIST = W7.tsv, j = 24, N = 36, H = 4.5.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:22 UTC, lanes 10:48:59 to END 15:01:22 UTC (killed 15:01:39).

## Tools (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at /opt/c3u2, used unmodified (clean). `compose.py` not run.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch. Sanity test passed: `3 0 0` on {1},{-1} rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e502e…6cdd6da (matches).

## Run

53 units (W7.tsv rows ≡ 24 mod 36, `units.tsv`), 3 lanes (`lane0.sh`–`lane2.sh`), each `close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. No seeding. `out.jsonl` = lanes 0, 1, 2 (82 lines: 49 solve records, and 33 layer-split records with 45 children each for the timed-out units, children unsolved as intended).

**Result: 16 certified, 33 timed out at 900 s, 3 killed at END, 1 not reached.**
No SAT. No proof rejection (every certified record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`; no `cake_lpr: none` record, so no recheck.jsonl). No memory problem (peak about 6 GB used of 15). No unit ended under 72 s without a certificate.
The unit killed during its cake_lpr check (`0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s0-9s0-10s0`) has no record and is open. There was no time to re-check it before the README deadline.

## Per unit

| row | lane | unit | result | solve s / check s |
|---|---|---|---|---|
| 24 | 0 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | certified | 816.1 / 97.0 |
| 60 | 1 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 96 | 2 | `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 768.7 / 96.1 |
| 132 | 0 | `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 610.0 / 92.7 |
| 168 | 1 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | certified | 815.0 / 106.3 |
| 204 | 2 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 240 | 0 | `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 276 | 1 | `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 312 | 2 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 348 | 0 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 384 | 1 | `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 619.2 / 90.1 |
| 420 | 2 | `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0-8s1-9s0-10s0` | certified | 852.3 / 103.3 |
| 456 | 0 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 860.1 / 104.4 |
| 492 | 1 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.2 / - |
| 528 | 2 | `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 628.5 / 90.7 |
| 564 | 0 | `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 600 | 1 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 636 | 2 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 672 | 0 | `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 716.1 / 94.1 |
| 708 | 1 | `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 744 | 2 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 780 | 0 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 816 | 1 | `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 852 | 2 | `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 888 | 0 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 924 | 1 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 960 | 2 | `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 996 | 0 | `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1032 | 1 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 709.4 / 90.8 |
| 1068 | 2 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1104 | 0 | `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 896.3 / 103.3 |
| 1140 | 1 | `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1176 | 2 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1212 | 0 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1248 | 1 | `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | certified | 855.2 / 108.7 |
| 1284 | 2 | `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | certified | 792.5 / 105.3 |
| 1320 | 0 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1356 | 1 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1392 | 2 | `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1428 | 0 | `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1464 | 1 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1500 | 2 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1536 | 0 | `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0-8s0-9s0-10s0` | certified | 526.3 / 85.6 |
| 1572 | 1 | `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1608 | 2 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1-8s0-9s0-10s0` | certified | 820.3 / 107.5 |
| 1644 | 0 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1680 | 1 | `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0-8s0-9s0-10s0` | certified | 857.5 / 99.0 |
| 1716 | 2 | `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1752 | 0 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1-8s0-9s0-10s0` | timed out at 900 | 900.1 / - |
| 1788 | 1 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1-8s1-9s0-10s0` | killed at END (CaDiCaL at 14.5 min, no record) |  |
| 1824 | 2 | `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0-8s0-9s0-10s0` | killed at END while cake_lpr ran (solve had ended, ~13.8 min; no record written) |  |
| 1860 | 0 | `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0-8s1-9s0-10s0` | killed at END (CaDiCaL at 3.6 min, no record) |  |
| 1896 | 1 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1-8s0-9s0-10s0` | not reached |  |

### Per root

| root | units | certified | timed out | not reached |
|---|---|---|---|---|
| 0s0_1 | 14 | 7 | 7 | 0 |
| 0s0_2 | 14 | 2 | 12 | 0 |
| 0s0_3 | 14 | 4 | 10 | 0 |
| 0s0_4 | 11 | 3 | 4 | 4 |

### Per parent six-bit cube

| parent | units here | certified | timed out | not reached |
|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s0-3s1-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_2__1s0-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_2__1s1-3s1-4s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s0-2s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 |
| `0s0_4__1s0-2s1-3s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s1` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s0-5s1-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s0-6s0-7s0` | 1 | 0 | 0 | 1 |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s1` | 1 | 0 | 0 | 1 |

Parents all of whose units on this machine were certified: `0s0_1__2s0-3s0-4s0-5s0-6s1-7s1`, `0s0_1__2s0-3s0-4s1-5s1-6s0-7s0`, `0s0_1__2s0-3s1-4s0-5s0-6s0-7s0`, `0s0_1__2s0-3s1-4s0-5s1-6s0-7s1`, `0s0_1__2s1-3s1-4s0-5s0-6s0-7s0`, `0s0_1__2s1-3s1-4s0-5s1-6s0-7s0`, `0s0_1__2s1-3s1-4s1-5s0-6s0-7s1`, `0s0_2__1s0-3s0-4s0-5s0-6s1-7s0`, `0s0_2__1s0-3s1-4s0-5s1-6s0-7s0`, `0s0_3__1s0-2s0-4s0-5s0-6s0-7s1`, `0s0_3__1s0-2s0-4s1-5s0-6s1-7s0`, `0s0_3__1s0-2s1-4s1-5s1-6s0-7s0`, `0s0_3__1s1-2s0-4s0-5s0-6s0-7s0`, `0s0_4__1s0-2s0-3s0-5s0-6s0-7s0`, `0s0_4__1s0-2s0-3s1-5s0-6s0-7s1`, `0s0_4__1s0-2s1-3s0-5s0-6s1-7s0`

Certified solve times (n=16): min 526.3, Q1 648.7, median 803.8, Q3 854.5, p90 871.0, max 896.3; certified above 300 s: 16
Check times: min 85.6, max 108.7, total 1575

Totals: {'timed out at 900': 33, 'certified': 16, 'not reached': 4}

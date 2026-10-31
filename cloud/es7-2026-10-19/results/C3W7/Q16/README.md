# C3W7 Q16: nine-bit σ-cubes of the H3/one roots at cap 900 (W7.tsv, shard 16 of 36)

Task: `results/C3W7/TASK.md` at 39bb1bac with V = Q16, LIST = W7.tsv, j = 16, N = 36, H = 4.5.
Start 2026-10-25 10:45:59 UTC, lanes started 10:48:18, END 15:00:59 (lanes killed then).

## Tools (details in `tools.txt`)
- C3U2 tools: worktree of cad4e050 at /opt/c3u2, unmodified. `compose.py` not run.
- CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc + E2 patch.
  Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 bf0e5027…dd6da (matches).

## Run
53 units (rows of W7.tsv with row ≡ 16 mod 36, `units.tsv`), 3 lanes (`lane0.sh`..`lane2.sh`), each
`close_tree.py base out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
`out.jsonl` = records of lane 0, then 1, then 2 (no seeding). Each timed-out unit has its layer-split
record (45 children, unsolved, as intended); none was σ-split.

## Result
- **16 certified, 35 timed out at 900, 2 started but killed at END (no record), 0 not reached.**
- No SAT. No proof rejection (every UNSAT record has lrat-check `c VERIFIED` and cake_lpr
  `s VERIFIED UNSAT`; no `recheck.jsonl` was needed). No memory problem (≤ 6 GB used of 15).
  No unit ended early (every timeout ran 900.0–900.2 s).
- Certified solve times (s): min 579.6, q1 643.0, median 775.2, q3 824.3, p90 876.1, max 893.4;
  all 16 above 300 s. Check times 84–113 s.
- Killed at END (to redo): row 1852 `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s1-9s0-10s0` (lane 0, started 14:58:54),
  row 1888 `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s0-9s0-10s0` (lane 1, started 15:00:52). Lane 2 finished its list at 14:56:41.
- Each parent six-bit cube has exactly one unit on this machine, so "all units here certified" holds for
  the 16 parents of the certified units (listed in the per-parent table).

## Per unit
| row | unit | result |
|---|---|---|
| 16 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | certified (solve 579.7 s, check 90.5 s) |
| 52 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 88 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 124 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 160 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | certified (solve 792.7 s, check 103.8 s) |
| 196 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 232 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 268 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 304 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | certified (solve 782.3 s, check 97.8 s) |
| 340 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 376 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 412 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 448 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | certified (solve 744.2 s, check 94.8 s) |
| 484 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s1-9s0-10s0` | certified (solve 868.7 s, check 97.1 s) |
| 520 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s0-9s0-10s0` | certified (solve 579.6 s, check 93.5 s) |
| 556 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 592 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s0-9s0-10s0` | certified (solve 828.6 s, check 99.9 s) |
| 628 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 664 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s0-9s0-10s0` | certified (solve 893.4 s, check 113.2 s) |
| 700 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 736 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s0-9s0-10s0` | certified (solve 811.5 s, check 102.7 s) |
| 772 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s1-9s0-10s0` | certified (solve 768.1 s, check 95.5 s) |
| 808 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 844 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 880 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 916 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 952 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 988 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1024 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | certified (solve 618.1 s, check 84.0 s) |
| 1060 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1096 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s0-9s0-10s0` | certified (solve 850.7 s, check 93.3 s) |
| 1132 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1168 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s0-9s0-10s0` | certified (solve 797.1 s, check 95.4 s) |
| 1204 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1240 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1276 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.0 s) |
| 1312 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | certified (solve 694.5 s, check 86.7 s) |
| 1348 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1384 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1420 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1456 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1492 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.2 s) |
| 1528 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1564 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1600 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s0-9s0-10s0` | certified (solve 625.9 s, check 85.8 s) |
| 1636 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1672 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s0-9s0-10s0` | certified (solve 740.1 s, check 89.8 s) |
| 1708 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1744 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1780 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s1-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1816 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s0-9s0-10s0` | timed out at 900 (solve 900.1 s) |
| 1852 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s1-9s0-10s0` | started, killed at END (no record) |
| 1888 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s0-9s0-10s0` | started, killed at END (no record) |

## Totals

**Per root** (units on this machine: certified / timed out / not reached or killed)

| root | units | certified | timed out | not reached | all certified |
|---|---|---|---|---|---|
| `0s0_1` | 14 | 5 | 9 | 0 |  |
| `0s0_2` | 14 | 5 | 9 | 0 |  |
| `0s0_3` | 15 | 4 | 11 | 0 |  |
| `0s0_4` | 10 | 2 | 6 | 2 |  |

**Per parent** (units on this machine: certified / timed out / not reached or killed)

| parent | units | certified | timed out | not reached | all certified |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0` | 1 | 1 | 0 | 0 | yes |
| `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1` | 1 | 1 | 0 | 0 | yes |
| `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0` | 1 | 0 | 1 | 0 |  |
| `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1` | 1 | 0 | 1 | 0 |  |
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1` | 1 | 0 | 0 | 1 |  |
| `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0` | 1 | 0 | 0 | 1 |  |

Totals: {'certified': 16, 'timeout': 35, 'killed': 2, 'notreached': 0, 'other': 0}
Parents all of whose units here were certified: ['0s0_1__2s0-3s0-4s0-5s0-6s1-7s0', '0s0_1__2s0-3s1-4s0-5s1-6s0-7s0', '0s0_1__2s1-3s0-4s0-5s1-6s1-7s0', '0s0_1__2s1-3s1-4s1-5s0-6s0-7s0', '0s0_1__2s1-3s1-4s1-5s1-6s0-7s0', '0s0_2__1s0-3s0-4s0-5s0-6s0-7s1', '0s0_2__1s0-3s0-4s1-5s0-6s1-7s0', '0s0_2__1s0-3s1-4s0-5s0-6s1-7s1', '0s0_2__1s0-3s1-4s1-5s1-6s0-7s0', '0s0_2__1s1-3s0-4s0-5s0-6s0-7s0', '0s0_3__1s0-2s0-4s0-5s0-6s0-7s0', '0s0_3__1s0-2s0-4s1-5s0-6s0-7s1', '0s0_3__1s0-2s1-4s0-5s0-6s1-7s0', '0s0_3__1s1-2s0-4s0-5s1-6s0-7s0', '0s0_4__1s0-2s0-3s1-5s0-6s0-7s0', '0s0_4__1s0-2s1-3s0-5s0-6s0-7s1']
Certified solve times (s): n=16 min 579.6 q1 643.0 median 775.2 q3 824.3 p90 876.1 max 893.4; above 300 s: 16
Flags: none

# C3W7 Q09: nine-bit σ-cubes of the H3/one roots, cap 900 (W7.tsv, shard 9 of 36)

Task: `results/C3W7/TASK.md` at 39bb1bac, with V = Q09, LIST = W7.tsv, j = 9, N = 36, H = 4.5.
One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 10:46:39 UTC; END 15:01:39 UTC.

## Tools and base check (`tools.txt`)

- C3U2 tools: worktree of cad4e050 at `/opt/c3u2`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch.
  Sanity check: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`. Matches.

## Run

53 units: the rows of `lists/W7.tsv` with row ≡ 9 (mod 36) (`units.tsv`). They ran in 3 lanes (`lane0.sh` … `lane2.sh`), each with
`close_tree.py … U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`. No records were seeded.
Each lane finished 16 units, about 15 minutes each, and started a 17th at about 14:50. The 17th was still in CaDiCaL at END. I killed the lanes' process groups at 15:01:53, so those 3 units have no record and count as "not reached". 2 more units were never started.
`out.jsonl` holds the records of lanes 0, 1 and 2 in that order: 48 solve records, plus 47 layer-split records for the timed-out units.

**Result: 1 certified, 47 timed out at 900 s, 5 not reached.** No SAT, no proof rejection, no `none` checker result, so no re-check was needed (there is no `recheck.jsonl`).
Memory peaked at about 2 GB used out of 15. No unit ended early: every unit that was not certified ran the full 900 s.

These nine-bit cubes are much harder here than in `results/C3H1/X1` (450–662 s each). Only 1 of 48 finished within 900 s, with 3 solves in parallel on 4 cores.

## Per unit

| row | unit | parent six-bit cube | result |
|---|---|---|---|
| 9 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | timed out at 900 (900.1 s) |
| 45 | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_1__2s0-3s0-4s0-5s1-6s0-7s1` | timed out at 900 (900.1 s) |
| 81 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s0` | timed out at 900 (900.2 s) |
| 117 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s0` | timed out at 900 (900.1 s) |
| 153 | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_1__2s0-3s1-4s0-5s0-6s1-7s1` | timed out at 900 (900.1 s) |
| 189 | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_1__2s0-3s1-4s0-5s1-6s1-7s1` | timed out at 900 (900.1 s) |
| 225 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s0` | timed out at 900 (900.1 s) |
| 261 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s0` | timed out at 900 (900.1 s) |
| 297 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s1` | timed out at 900 (900.1 s) |
| 333 | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_1__2s1-3s0-4s1-5s0-6s0-7s1` | timed out at 900 (900.1 s) |
| 369 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s0` | timed out at 900 (900.1 s) |
| 405 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s0` | timed out at 900 (900.1 s) |
| 441 | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_1__2s1-3s1-4s0-5s1-6s1-7s1` | timed out at 900 (900.1 s) |
| 477 | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_1__2s1-3s1-4s1-5s0-6s1-7s1` | timed out at 900 (900.1 s) |
| 513 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0` | certified (solve 811.4 s, check 107.7 s) |
| 549 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s0` | timed out at 900 (900.1 s) |
| 585 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s1` | timed out at 900 (900.1 s) |
| 621 | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_2__1s0-3s0-4s1-5s1-6s0-7s1` | timed out at 900 (900.1 s) |
| 657 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s0` | timed out at 900 (900.1 s) |
| 693 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s0` | timed out at 900 (900.1 s) |
| 729 | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_2__1s0-3s1-4s1-5s0-6s1-7s1` | timed out at 900 (900.1 s) |
| 765 | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_2__1s0-3s1-4s1-5s1-6s1-7s1` | timed out at 900 (900.1 s) |
| 801 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s0` | timed out at 900 (900.1 s) |
| 837 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s0` | timed out at 900 (900.1 s) |
| 873 | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_2__1s1-3s0-4s1-5s1-6s0-7s1` | timed out at 900 (900.1 s) |
| 909 | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_2__1s1-3s1-4s0-5s0-6s0-7s1` | timed out at 900 (900.1 s) |
| 945 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s0` | timed out at 900 (900.1 s) |
| 981 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s0` | timed out at 900 (900.1 s) |
| 1017 | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_2__1s1-3s1-4s1-5s1-6s1-7s1` | timed out at 900 (900.1 s) |
| 1053 | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_3__1s0-2s0-4s0-5s0-6s1-7s1` | timed out at 900 (900.1 s) |
| 1089 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s0` | timed out at 900 (900.1 s) |
| 1125 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s0` | timed out at 900 (900.1 s) |
| 1161 | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_3__1s0-2s1-4s0-5s0-6s0-7s1` | timed out at 900 (900.1 s) |
| 1197 | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_3__1s0-2s1-4s0-5s1-6s0-7s1` | timed out at 900 (900.1 s) |
| 1233 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s0` | timed out at 900 (900.1 s) |
| 1269 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s0` | timed out at 900 (900.1 s) |
| 1305 | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_3__1s1-2s0-4s0-5s0-6s1-7s1` | timed out at 900 (900.1 s) |
| 1341 | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1-8s1-9s0-10s1` | `0s0_3__1s1-2s0-4s0-5s1-6s1-7s1` | timed out at 900 (900.3 s) |
| 1377 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0-8s0-9s0-10s1` | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s0` | timed out at 900 (900.1 s) |
| 1413 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0-8s1-9s0-10s1` | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s0` | timed out at 900 (900.1 s) |
| 1449 | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1-8s0-9s0-10s1` | `0s0_3__1s1-2s1-4s0-5s1-6s0-7s1` | timed out at 900 (900.1 s) |
| 1485 | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1-8s1-9s0-10s1` | `0s0_3__1s1-2s1-4s1-5s0-6s0-7s1` | timed out at 900 (900.1 s) |
| 1521 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0-8s0-9s0-10s1` | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s0` | timed out at 900 (900.1 s) |
| 1557 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0-8s1-9s0-10s1` | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s0` | timed out at 900 (900.1 s) |
| 1593 | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1-8s0-9s0-10s1` | `0s0_4__1s0-2s0-3s0-5s1-6s1-7s1` | timed out at 900 (900.1 s) |
| 1629 | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1-8s1-9s0-10s1` | `0s0_4__1s0-2s0-3s1-5s0-6s1-7s1` | timed out at 900 (900.1 s) |
| 1665 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0-8s0-9s0-10s1` | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s0` | timed out at 900 (900.1 s) |
| 1701 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0-8s1-9s0-10s1` | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s0` | timed out at 900 (900.1 s) |
| 1737 | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1-8s0-9s0-10s1` | `0s0_4__1s0-2s1-3s1-5s0-6s0-7s1` | not reached |
| 1773 | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1-8s1-9s0-10s1` | `0s0_4__1s0-2s1-3s1-5s1-6s0-7s1` | not reached |
| 1809 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0-8s0-9s0-10s1` | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s0` | not reached |
| 1845 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0-8s1-9s0-10s1` | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | not reached |
| 1881 | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1-8s0-9s0-10s1` | `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | not reached |

## Totals per root

| root | units | certified | timed out | not reached | other |
|---|---|---|---|---|---|
| `0s0_1` | 14 | 0 | 14 | 0 | 0 |
| `0s0_2` | 15 | 1 | 14 | 0 | 0 |
| `0s0_3` | 14 | 0 | 14 | 0 | 0 |
| `0s0_4` | 10 | 0 | 5 | 5 | 0 |

## Totals per parent six-bit cube

This machine has one unit of each parent (8 nine-bit cubes per parent, split over 36 shards).

| parent six-bit cube | units | certified | timed out | not reached | other |
|---|---|---|---|---|---|
| `0s0_1__2s0-3s0-4s0-5s0-6s0-7s1` | 1 | 0 | 1 | 0 | 0 |
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
| `0s0_4__1s1-2s0-3s0-5s1-6s1-7s0` | 1 | 0 | 0 | 1 | 0 |
| `0s0_4__1s1-2s0-3s1-5s0-6s1-7s1` | 1 | 0 | 0 | 1 | 0 |

Parents all of whose units here were certified: `0s0_2__1s0-3s0-4s0-5s0-6s0-7s0`

## Certified solve times

Totals: 53 units; certified 1, timed out 47, not reached 5, other 0
Certified solve times: min 811.4, quartiles 811.4, 811.4, 811.4, p90 811.4, max 811.4; above 300 s: 1
Units ending in under 72 s without a certificate: none

The 47 timed-out units each have a layer-split record. Their children are unsolved and stay in `open_frontier`, as the task intends.
The 5 units that were not reached: rows 1737, 1773 and 1809 were killed in CaDiCaL at END; rows 1845 and 1881 were never started.

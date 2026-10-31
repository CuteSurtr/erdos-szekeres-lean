# C3W7 / Q19: shard 19 of 36 of `lists/W7.tsv`, nine-bit H3/one cubes at cap 900, 3 lanes

**Result: 1 of my 53 units was certified (both checkers). 47 timed out at cap 900, 3 were killed at END and 2 were not reached. No SAT, no proof rejection, no checker `none`, no memory problem, and no unit ended early without a certificate.** Every unit of roots `0s0_1`, `0s0_2` and `0s0_3` that ran (43 of 43) timed out at 900 s. The only certificate is `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s1-9s1-10s1`, which took 879.3 s of solving and 88.0 s of checking, just under the cap. The plan's estimate of 450–662 s per nine-bit cube came from C3H1/X1, a `0s0_5` cube. It does not hold for the 0s0_1–0s0_4 cubes on this machine, with 3 lanes sharing 4 cores.

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 10:46:29 UTC, END 15:01:29 UTC (H = 4.5 h minus 15 min). Task: `results/C3W7/TASK.md` at 39bb1bac.

- Tools (`tools.txt`): worktree of cad4e050 at `/opt/c3u2`, `C3U2/tools` used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e75, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc0 with the E2 patch. Sanity test: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`, which matches. Every solve record carries this `base_sha256`.
- Units: rows of `W7.tsv` with row ≡ 19 (mod 36), so 53 units (`units.tsv`), no seeding. Lane k ran positions ≡ k (mod 3): 18/18/17 units. Each lane ran `close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02` (`lane.sh`, `lane0.sh`–`lane2.sh`), started with `setsid nohup`. A watchdog killed the three lane process groups at END.
- `out.jsonl` holds 95 records: lane 0, then lane 1, then lane 2. They are 48 solve records (1 certified, 47 `UNKNOWN` at cap 900) and 47 layer-split records (`"children": 45` each) for the timed-out units. Their children are unsolved and are in each unit's `open_frontier` (45), as the task intends. No `recheck.jsonl` was needed.

## Totals per root

| root | units | certified | timed out at 900 | killed at END | not reached |
|---|---|---|---|---|---|
| 0s0_1 | 14 | 0 | 14 | 0 | 0 |
| 0s0_2 | 14 | 0 | 14 | 0 | 0 |
| 0s0_3 | 15 | 0 | 15 | 0 | 0 |
| 0s0_4 | 10 | 1 | 4 | 3 | 2 |
| **total** | **53** | **1** | **47** | **3** | **2** |

## Per parent six-bit cube

Each of my 53 units has a different parent six-bit cube (53 parents, 1 unit each on this machine). So the per-parent totals are the per-unit results below. Only one parent had all of its units on this machine certified: **`0s0_4__1s0-2s0-3s0-5s0-6s1-7s1`**, through its unit `-8s1-9s1-10s1`. The parents' other 7 nine-bit cubes are on other machines. Every other parent has a timed-out, killed or unreached unit here.

## Solve times

- Certified units: 1. Solve 879.3 s (min = quartiles = p90 = max), check 88.0 s, proof 881 MB. Certified above 300 s: 1.
- Timed-out units: 47, all at cap 900 (solve_s 900.0–900.8). None ended in under 72 s, or in under 900 s at all, without a certificate.
- Wall time per unit, including the split record: about 15 min, so a lane ran 4 units per hour.

## Killed at END / not reached

- Killed at END (started 14:50–14:51, ran about 10 min, no record written, no checker involved): `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s0-9s1-10s1`, `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s1-9s1-10s1`, `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s0-9s1-10s1`.
- Not reached: `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s1-9s1-10s1` and `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s0-9s1-10s1` (positions 51 and 52; see the table).

## Memory and disk

Sampled every ~10 min: used memory about 2 GB, available never under 12 GB. Root disk peaked at about 14 GB used, because proofs are deleted after checking. No memory problem.

## Per unit

| pos | row | unit (= parent six-bit cube + `-8sX-9sX-10sX`) | lane | result | solve s | check s |
|---|---|---|---|---|---|---|
| 0 | 19 | `0s0_1__2s0-3s0-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 1 | 55 | `0s0_1__2s0-3s0-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 2 | 91 | `0s0_1__2s0-3s0-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 3 | 127 | `0s0_1__2s0-3s0-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 4 | 163 | `0s0_1__2s0-3s1-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.3 | – |
| 5 | 199 | `0s0_1__2s0-3s1-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 6 | 235 | `0s0_1__2s0-3s1-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 7 | 271 | `0s0_1__2s1-3s0-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 8 | 307 | `0s0_1__2s1-3s0-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 9 | 343 | `0s0_1__2s1-3s0-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 10 | 379 | `0s0_1__2s1-3s0-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 11 | 415 | `0s0_1__2s1-3s1-4s0-5s0-6s1-7s1-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.0 | – |
| 12 | 451 | `0s0_1__2s1-3s1-4s1-5s0-6s0-7s0-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 13 | 487 | `0s0_1__2s1-3s1-4s1-5s1-6s0-7s0-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 14 | 523 | `0s0_2__1s0-3s0-4s0-5s0-6s0-7s1-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 15 | 559 | `0s0_2__1s0-3s0-4s0-5s1-6s0-7s1-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 16 | 595 | `0s0_2__1s0-3s0-4s1-5s0-6s1-7s0-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 17 | 631 | `0s0_2__1s0-3s0-4s1-5s1-6s1-7s0-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 18 | 667 | `0s0_2__1s0-3s1-4s0-5s0-6s1-7s1-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 19 | 703 | `0s0_2__1s0-3s1-4s0-5s1-6s1-7s1-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 20 | 739 | `0s0_2__1s0-3s1-4s1-5s1-6s0-7s0-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 21 | 775 | `0s0_2__1s1-3s0-4s0-5s0-6s0-7s0-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 22 | 811 | `0s0_2__1s1-3s0-4s0-5s1-6s0-7s1-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 23 | 847 | `0s0_2__1s1-3s0-4s1-5s0-6s0-7s1-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 24 | 883 | `0s0_2__1s1-3s0-4s1-5s1-6s1-7s0-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 25 | 919 | `0s0_2__1s1-3s1-4s0-5s0-6s1-7s0-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.8 | – |
| 26 | 955 | `0s0_2__1s1-3s1-4s0-5s1-6s1-7s1-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 27 | 991 | `0s0_2__1s1-3s1-4s1-5s0-6s1-7s1-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 28 | 1027 | `0s0_3__1s0-2s0-4s0-5s0-6s0-7s0-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 29 | 1063 | `0s0_3__1s0-2s0-4s0-5s1-6s0-7s0-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 30 | 1099 | `0s0_3__1s0-2s0-4s1-5s0-6s0-7s1-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.2 | – |
| 31 | 1135 | `0s0_3__1s0-2s0-4s1-5s1-6s0-7s1-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 32 | 1171 | `0s0_3__1s0-2s1-4s0-5s0-6s1-7s0-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 33 | 1207 | `0s0_3__1s0-2s1-4s0-5s1-6s1-7s0-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.3 | – |
| 34 | 1243 | `0s0_3__1s0-2s1-4s1-5s0-6s1-7s1-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 35 | 1279 | `0s0_3__1s0-2s1-4s1-5s1-6s1-7s1-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 36 | 1315 | `0s0_3__1s1-2s0-4s0-5s1-6s0-7s0-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 37 | 1351 | `0s0_3__1s1-2s0-4s1-5s0-6s0-7s0-8s1-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 38 | 1387 | `0s0_3__1s1-2s0-4s1-5s1-6s0-7s1-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 39 | 1423 | `0s0_3__1s1-2s1-4s0-5s0-6s0-7s1-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 40 | 1459 | `0s0_3__1s1-2s1-4s0-5s1-6s1-7s0-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 41 | 1495 | `0s0_3__1s1-2s1-4s1-5s0-6s1-7s0-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 42 | 1531 | `0s0_3__1s1-2s1-4s1-5s1-6s1-7s1-8s0-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 43 | 1567 | `0s0_4__1s0-2s0-3s0-5s0-6s1-7s1-8s1-9s1-10s1` | 1 | **certified** | 879.3 | 88.0 |
| 44 | 1603 | `0s0_4__1s0-2s0-3s1-5s0-6s0-7s0-8s0-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 45 | 1639 | `0s0_4__1s0-2s0-3s1-5s1-6s0-7s0-8s1-9s1-10s1` | 0 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 46 | 1675 | `0s0_4__1s0-2s1-3s0-5s0-6s0-7s1-8s0-9s1-10s1` | 1 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 47 | 1711 | `0s0_4__1s0-2s1-3s0-5s1-6s0-7s1-8s1-9s1-10s1` | 2 | timed out at 900 (layer split, 45 children) | 900.1 | – |
| 48 | 1747 | `0s0_4__1s0-2s1-3s1-5s0-6s1-7s0-8s0-9s1-10s1` | 0 | killed at END (started 14:50/14:51, no record) | – | – |
| 49 | 1783 | `0s0_4__1s0-2s1-3s1-5s1-6s1-7s0-8s1-9s1-10s1` | 1 | killed at END (started 14:50/14:51, no record) | – | – |
| 50 | 1819 | `0s0_4__1s1-2s0-3s0-5s0-6s1-7s1-8s0-9s1-10s1` | 2 | killed at END (started 14:50/14:51, no record) | – | – |
| 51 | 1855 | `0s0_4__1s1-2s0-3s0-5s1-6s1-7s1-8s1-9s1-10s1` | 0 | not reached | – | – |
| 52 | 1891 | `0s0_4__1s1-2s0-3s1-5s1-6s0-7s0-8s0-9s1-10s1` | 1 | not reached | – | – |

# C3SIG / G1: σ-cube pilot, shard j = 1 (rows 1, 5, 9, 13, 17)

**Result: all 5 nodes closed at K = 3, with 40 of 40 cubes certified and none open. K = 6 was never needed.
The median σ-cube cost is 0.105 of the recorded layer-split cost. No SAT and no proof rejection.**
On this shard, PLAN.md's criterion is met: the median is far below 0.5, and the open fraction at the first σ level is 0%.
No second-level (K = 6) cubes were needed, so the "under 20% of second-level cubes open" condition holds trivially (0 open).

## Setup

One cloud VM with 4 cores, 15 GB RAM and no swap (`env.txt`). The run went from 04:41 to 05:33 UTC on 2026-10-21, inside a 2-hour budget from 04:39.
The tools are exactly those of step 1 of `results/C3WAVE2/TASK.md` (`tools.txt`): the C3-S tools at 132398c, CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8,
and lrat-check 2e3b2dc with the E2 patch. Both checkers passed the sanity check. The base CNF has header `p cnf 168399 4154921`, and its sha256 `bf0e502e…` matches.
`sigma_cubes.py` was copied unmodified from `results/C3PLAN/scripts/` at 640a56c2 (sha256 `716aa57d…`).
`runner.sh` ran `sigma_cubes.py /opt/work/base.cnf out.jsonl NODE 3 300 3` for each node in turn, with a deadline equal to an even share of the time left. It would have run K = 6 (cap 300) only if a K = 3 cube had stayed open.
The σ bits are the first K free residues of each node (listed in `tools.txt`). The K = 6 bits extend the K = 3 bits, but no K = 6 run took place.

## Table (K = 3, cap 300 s, 3 jobs on 4 cores)

| row | node | cubes certified / open | solve s | check s | largest cube (solve+check) s | σ cost s | recorded_core_s | ratio |
|---|---|---|---|---|---|---|---|---|
| 1 | 0s0-1s1_3s1-4s0 | 8 / 0 | 1295.9 | 363.7 | 248.6 | 1659.6 | 16346.0 | 0.102 |
| 5 | 0s0-1s1_3s0-4s1 | 8 / 0 | 1286.4 | 353.4 | 235.2 | 1639.8 | 15626.6 | 0.105 |
| 9 | 0s0-1s1_7s1-9s0 | 8 / 0 | 1078.5 | 345.5 | 220.2 | 1424.0 | 15308.2 | 0.093 |
| 13 | 0s0-1s1_5s0-7s1 | 8 / 0 | 1346.5 | 387.4 | 268.6 | 1733.9 | 14821.7 | 0.117 |
| 17 | 0s0-1s1_5s1-7s0 | 8 / 0 | 1343.3 | 369.6 | 313.8 | 1712.9 | 14314.4 | 0.120 |

- σ cost = solve + check, summed over the 8 cubes. This is the same measure as `recorded_core_s` (solve + check summed over the layer-split subtree).
  Each node took about 10 to 11 minutes of wall time.
- **Median ratio σ-cube cost / layer-split cost: 0.105** (range 0.093 to 0.120). Total: 8,170 s, against 76,417 s recorded.
- **Open cubes: 0 of 40 (0%) at K = 3. K = 6 was not run, because no K = 3 cube was open.**
- The slowest single solve was 251.3 s, against a cap of 300 s. Per-cube solve times ran from 86 to 251 s, so there is some margin under the cap, but not much.
  The largest LRAT proof was 443 MB; proofs were deleted after checking.
- Caveat: per-cube times are CPU-contended, with 3 jobs on 4 cores. The recorded layer-split times also come from 3-job waves, so the two should be roughly comparable, but this was not controlled.

## Certification, SAT and rejections

All 40 records are `UNSATISFIABLE` with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` (`certified: true`), and each record carries its cube CNF sha256.
There was no SAT, no proof rejection and no memory problem.

## Files

`env.txt`, `tools.txt`, `nodes.tsv`, `runner.sh`, `out.jsonl` (all 40 cube records), `driver.log`, `summ.py` (the script that makes the table) and `summary.md` (its output).

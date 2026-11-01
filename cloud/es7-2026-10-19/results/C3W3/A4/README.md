# C3W3 / A4: wave 3, list A_s0.tsv, shard 4 of 8

**Result: 8 of my 37 roots are closed, 3 are partial and 26 were not reached. No SAT. No proof rejection. No memory problem.**
629 new nodes certified, each accepted by lrat-check (E2 patch, `c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`).

## Setup

- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Ran from 04:40:07 to 06:40 UTC on 2026-10-21; H = 2.0 h, END = 06:25:07.
- Tools (`tools.txt`): worktree of `132398c` at `/opt/c3s`, used unmodified. CaDiCaL 3.0.1 (c6073042). cake_lpr a36874a8, and its example prints `s VERIFIED UNSAT`. lrat-check 2e3b2dc with the E2 patch. Sanity check on {1},{-1}: both checkers reject `3 0 0` and both accept `3 0 1 2 0`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Both match.
- Roots: rows of `lists/A_s0.tsv` with row ≡ 4 (mod 8), giving 37 roots (`roots.tsv`). There were 3 lanes (`lane0.sh` to `lane2.sh`) with `--jobs 1`, `--caps 300,300,600 --cadopts=--sat --split-singles`, and S = min(0.5, hours left). Lane k took positions ≡ k (mod 3).
- Seeding: **82 records**, all in lane 0. For `0s0-5s0_1s0-2s1`: 74 records (66 certified, 8 split) from `C3S0/S2/out.jsonl`. For `0s0-5s0_1s1-4s0`: 8 split records from `C3S0/S1/out.jsonl`. No matching records were in C3WAVE1 or C3WAVE2. `out.jsonl` holds only the new records: 639 in all (629 certified, 9 split, 1 UNKNOWN at 300 s).

## Notes

- `close_tree.py` checks `--hours` only between batches, and a batch is the whole current frontier. So the three roots that started before 04:53 (lanes 0 and 2) and `0s0-2s0_1` (lane 1) ran past their 0.5 h slice, until END. At END I killed the lanes, drivers and checkers by hand (`=== KILLED at END` in the driver logs). The nodes still being solved or checked at that moment have no record and stay open. No record with `cake_lpr: none` was written, so no re-check was needed.
- Because of this, root 19 (`0s0-5s0_1s1-4s0`, partial in the list) was not reached. Its 8 seeded split records are still in C3S0/S1.

## Per root (depth = number of layers; roots are at depth 2; new records only)

| # | root | stratum | list status | lane | status | certified by depth (new) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0s0-5s0_1s0-2s1 | H6(5,0)/two | partial | 0 | partial | d3: 84, d4: 168 | 0 | 1878 | 4162 |
| 2 | 0s0-2s0_1s1-3s0 | H6(2,0)/two | untouched | 1 | **closed** | d2: 1 | 0 | 116 | 35 |
| 3 | 0s0-2s0_3s0-7s1 | H6(2,0)/two | untouched | 2 | **closed** | d2: 1 | 0 | 65 | 38 |
| 4 | 0s0-2s0_3s1-8s0 | H6(2,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 5 | 0s0-2s0_5s0-6s0 | H6(2,0)/two | untouched | 1 | **closed** | d2: 1 | 0 | 6 | 14 |
| 6 | 0s0-4s0_1s1-2s1 | H6(4,0)/two | untouched | 2 | **closed** | d2: 1 | 0 | 15 | 25 |
| 7 | 0s0-4s0_2s0-7s0 | H6(4,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 8 | 0s0-4s0_6s0-7s1 | H6(4,0)/two | untouched | 1 | **closed** | d2: 1 | 0 | 144 | 35 |
| 9 | 0s0-5s0_1s0-3s0 | H6(5,0)/two | untouched | 2 | **closed** | d2: 1 | 0 | 19 | 27 |
| 10 | 0s0-5s0_1s1-10s0 | H6(5,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 11 | 0s0-5s0_1s1-7s1 | H6(5,0)/two | untouched | 1 | **closed** | d2: 1 | 0 | 131 | 35 |
| 12 | 0s0-5s0_2s0-3s1 | H6(5,0)/two | untouched | 2 | partial | d4: 284 | 1 | 1568 | 4267 |
| 13 | 0s0-5s0_2s0-9s1 | H6(5,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 14 | 0s0-5s0_2s1-9s0 | H6(5,0)/two | untouched | 1 | **closed** | d2: 1 | 0 | 16 | 17 |
| 15 | 0s0-5s0_6s0-9s0 | H6(5,0)/two | untouched | 2 | not reached | – | 0 | 0 | 0 |
| 16 | 0s0-5s0_6s1-9s1 | H6(5,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 17 | 0s0-2s0_1 | H6(2,0)/one | untouched | 1 | partial | d3: 85 | 0 | 3524 | 1966 |
| 18 | 0s0-4s0_6 | H6(4,0)/one | untouched | 2 | not reached | – | 0 | 0 | 0 |
| 19 | 0s0-5s0_1s1-4s0 | H6(5,0)/two | partial | 0 | not reached | – | 0 | 0 | 0 |
| 20 | 0s0-2s0_1s1-8s1 | H6(2,0)/two | untouched | 1 | not reached | – | 0 | 0 | 0 |
| 21 | 0s0-2s0_5s1-8s1 | H6(2,0)/two | untouched | 2 | not reached | – | 0 | 0 | 0 |
| 22 | 0s0-2s0_7s0-10s0 | H6(2,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 23 | 0s0-2s0_8s1-10s0 | H6(2,0)/two | untouched | 1 | not reached | – | 0 | 0 | 0 |
| 24 | 0s0-4s0_2s0-3s1 | H6(4,0)/two | untouched | 2 | not reached | – | 0 | 0 | 0 |
| 25 | 0s0-4s0_5s1-10s1 | H6(4,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 26 | 0s0-4s0_8s0-10s0 | H6(4,0)/two | untouched | 1 | not reached | – | 0 | 0 | 0 |
| 27 | 0s0-4s0_9s0-10s0 | H6(4,0)/two | untouched | 2 | not reached | – | 0 | 0 | 0 |
| 28 | 0s0-5s0_3s0-10s1 | H6(5,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 29 | 0s0-5s0_3s0-9s0 | H6(5,0)/two | untouched | 1 | not reached | – | 0 | 0 | 0 |
| 30 | 0s0-5s0_3s1-7s0 | H6(5,0)/two | untouched | 2 | not reached | – | 0 | 0 | 0 |
| 31 | 0s0-5s0_4s0-6s0 | H6(5,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 32 | 0s0-5s0_4s1-10s0 | H6(5,0)/two | untouched | 1 | not reached | – | 0 | 0 | 0 |
| 33 | 0s0-5s0_4s1-9s0 | H6(5,0)/two | untouched | 2 | not reached | – | 0 | 0 | 0 |
| 34 | 0s0-5s0_8s0-10s0 | H6(5,0)/two | untouched | 0 | not reached | – | 0 | 0 | 0 |
| 35 | 0s0-5s0_9s0-10s0 | H6(5,0)/two | untouched | 1 | not reached | – | 0 | 0 | 0 |
| 36 | 0s0-3s0_9 | H6(3,0)/one | untouched | 2 | not reached | – | 0 | 0 | 0 |
| 37 | 0s0-5s0_9 | H6(5,0)/one | untouched | 0 | not reached | – | 0 | 0 | 0 |

The solve and check times are summed per node, so they are not wall-clock.
The timeout is `0s0-5s0_2s0-3s1` at depth 2 (300 s), which was then split. Partial roots: `0s0-5s0_1s0-2s1` (lane 0), `0s0-5s0_2s0-3s1` (lane 2) and `0s0-2s0_1` (lane 1); their records can be resumed.
Closed roots: `0s0-2s0_1s1-3s0`, `0s0-2s0_3s0-7s1`, `0s0-2s0_5s0-6s0`, `0s0-4s0_1s1-2s1`, `0s0-4s0_6s0-7s1`, `0s0-5s0_1s0-3s0`, `0s0-5s0_1s1-7s1` and `0s0-5s0_2s1-9s0`. Each was certified at the root in one solve.

## Totals per stratum (new records)

| stratum | closed | partial | not reached | certified (new) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|
| H6(5,0)/two | 3 | 2 | 13 | 539 | 1 | 3612 | 8508 |
| H6(2,0)/two | 3 | 0 | 5 | 3 | 0 | 187 | 87 |
| H6(4,0)/two | 2 | 0 | 5 | 2 | 0 | 159 | 60 |
| H6(2,0)/one | 0 | 1 | 0 | 85 | 0 | 3524 | 1966 |
| H6(4,0)/one | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(3,0)/one | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(5,0)/one | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

## compose.py

`compose.txt`: 629 certified nodes, `class_covered: false`, 852 uncovered frontier nodes. This is expected for one shard. compose recomputed the CNF sha256 of every certified node.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: at most about 8 GB used of 15 GB. There was no OOM.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh` to `lane2.sh`, `out.jsonl` (new records, lane by lane), `driver0.log` to `driver2.log` (the last 100 lines of each), `compose.txt`.

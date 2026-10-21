# C3W3 / A7: wave 3, list A_s0.tsv, shard 7 of 8 (3 lanes, --jobs 1, 0.5 h slices, 2 h budget)

**Result: 13 of my 36 roots are closed, 2 are partial (0s0-5s0_1s0-6s1, 0s0-3s0_4), and 21 were not reached. No SAT. No proof rejection. No memory problem.**

## Tools and base CNF (`tools.txt`)

- C3-S tools: worktree of commit 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c60730422e758ef1cebe7aeddf2dda31c996bf04); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (the example prints `s VERIFIED UNSAT`);
  drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch. Sanity check passed: `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:40:09 UTC, END 06:25:09 UTC (start + 2 h − 15 min).

## Setup

- Roots: the rows of `lists/A_s0.tsv` with row ≡ 7 (mod 8), 36 roots (`roots.tsv`). Lane k ran positions ≡ k (mod 3) (`lane0.sh`–`lane2.sh`).
- **Seeded records: 20** (19 certified, 1 split) for the one partial root `0s0-3s0_7`, all from `C3WAVE2/K17/out.jsonl`, at the start of lane 0's out file. `out.jsonl` holds only the 509 new records (lane 0, then 1, then 2).
- `close_tree.py` checks `--hours` only between batches, so a root's batch ran past its 0.5 h slice (roots 1, 9 and 17 ran from their start until END). At END I killed all lanes by hand. Three nodes were being solved or checked at that point (`0s0-2s0_1s0-10s1`, `0s0-3s0_4_7s1-9s0`, `0s0-5s0_1s0-6s1_8_2s1-9s0`). The worker processes were killed before they wrote a record, so there are no `cake_lpr: none` records to re-check. Root 19 (`0s0-2s0_1s0-10s1`) was started 28 s before END and has no records.

## Per root (depth = number of layers; certified counts and times are for new records only)

| # | root | stratum | lane | status | certified by depth | timeouts | splits | solve s | check s |
|---|------|---------|------|--------|--------------------|----------|--------|---------|---------|
| 1 | 0s0-3s0_7 | H6(3,0)/one | lane 0 | **closed** | d3: 101 | 0 | 0 | 3200 | 2441 |
| 2 | 0s0-2s0_3s0-10s0 | H6(2,0)/two | lane 1 | **closed** | d2: 1 | 0 | 0 | 82 | 37 |
| 3 | 0s0-2s0_3s0-9s1 | H6(2,0)/two | lane 2 | **closed** | d2: 1 | 0 | 0 | 16 | 29 |
| 4 | 0s0-2s0_4s0-7s0 | H6(2,0)/two | lane 0 | **closed** | d2: 1 | 0 | 0 | 6 | 14 |
| 5 | 0s0-2s0_5s0-7s1 | H6(2,0)/two | lane 1 | **closed** | d2: 1 | 0 | 0 | 91 | 37 |
| 6 | 0s0-4s0_1s1-9s1 | H6(4,0)/two | lane 2 | **closed** | d2: 1 | 0 | 0 | 179 | 45 |
| 7 | 0s0-4s0_5s0-6s1 | H6(4,0)/two | lane 0 | **closed** | d2: 1 | 0 | 0 | 270 | 41 |
| 8 | 0s0-4s0_6s1-7s1 | H6(4,0)/two | lane 1 | **closed** | d2: 1 | 0 | 0 | 12 | 22 |
| 9 | 0s0-5s0_1s0-6s1 | H6(5,0)/two | lane 2 | **partial** | d4: 284 | 1 | 8 | 1396 | 4425 |
| 10 | 0s0-5s0_1s1-2s1 | H6(5,0)/two | lane 0 | **closed** | d2: 1 | 0 | 0 | 26 | 24 |
| 11 | 0s0-5s0_1s1-9s0 | H6(5,0)/two | lane 1 | **closed** | d2: 1 | 0 | 0 | 20 | 25 |
| 12 | 0s0-5s0_2s0-7s0 | H6(5,0)/two | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |
| 13 | 0s0-5s0_2s1-3s1 | H6(5,0)/two | lane 0 | **closed** | d2: 1 | 0 | 0 | 27 | 24 |
| 14 | 0s0-5s0_6s0-10s1 | H6(5,0)/two | lane 1 | **closed** | d2: 1 | 0 | 0 | 129 | 34 |
| 15 | 0s0-5s0_6s1-7s0 | H6(5,0)/two | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |
| 16 | 0s0-5s0_7s0-9s0 | H6(5,0)/two | lane 0 | **closed** | d2: 1 | 0 | 0 | 12 | 19 |
| 17 | 0s0-3s0_4 | H6(3,0)/one | lane 1 | **partial** | d3: 102 | 0 | 1 | 3182 | 2418 |
| 18 | 0s0-5s0_2 | H6(5,0)/one | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |
| 19 | 0s0-2s0_1s0-10s1 | H6(2,0)/two | lane 0 | **not reached** | – | 0 | 0 | 0 | 0 |
| 20 | 0s0-2s0_4s1-10s1 | H6(2,0)/two | lane 1 | **not reached** | – | 0 | 0 | 0 | 0 |
| 21 | 0s0-2s0_6s0-10s1 | H6(2,0)/two | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |
| 22 | 0s0-2s0_7s1-8s0 | H6(2,0)/two | lane 0 | **not reached** | – | 0 | 0 | 0 | 0 |
| 23 | 0s0-2s0_9s0-10s0 | H6(2,0)/two | lane 1 | **not reached** | – | 0 | 0 | 0 | 0 |
| 24 | 0s0-4s0_3s0-9s1 | H6(4,0)/two | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |
| 25 | 0s0-4s0_7s1-10s0 | H6(4,0)/two | lane 0 | **not reached** | – | 0 | 0 | 0 | 0 |
| 26 | 0s0-4s0_8s0-9s1 | H6(4,0)/two | lane 1 | **not reached** | – | 0 | 0 | 0 | 0 |
| 27 | 0s0-4s0_9s1-10s1 | H6(4,0)/two | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |
| 28 | 0s0-5s0_3s0-6s1 | H6(5,0)/two | lane 0 | **not reached** | – | 0 | 0 | 0 | 0 |
| 29 | 0s0-5s0_3s1-10s1 | H6(5,0)/two | lane 1 | **not reached** | – | 0 | 0 | 0 | 0 |
| 30 | 0s0-5s0_3s1-8s1 | H6(5,0)/two | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |
| 31 | 0s0-5s0_4s0-7s1 | H6(5,0)/two | lane 0 | **not reached** | – | 0 | 0 | 0 | 0 |
| 32 | 0s0-5s0_4s1-6s1 | H6(5,0)/two | lane 1 | **not reached** | – | 0 | 0 | 0 | 0 |
| 33 | 0s0-5s0_7s0-10s0 | H6(5,0)/two | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |
| 34 | 0s0-5s0_8s0-9s1 | H6(5,0)/two | lane 0 | **not reached** | – | 0 | 0 | 0 | 0 |
| 35 | 0s0-5s0_9s1-10s1 | H6(5,0)/two | lane 1 | **not reached** | – | 0 | 0 | 0 | 0 |
| 36 | 0s0-4s0_8 | H6(4,0)/one | lane 2 | **not reached** | – | 0 | 0 | 0 | 0 |

Root 1 (`0s0-3s0_7`) was closed together with the 19 certified and 1 split seeded records from K17. Root 9 (`0s0-5s0_1s0-6s1`) has 1 timeout (600 s cap) and 8 split records (pre-splits and that timeout). Root 17 (`0s0-3s0_4`) was pre-split, and 102 of its depth-3 children are certified. Solve and check times are sums over nodes, with 3 lanes sharing 4 cores.

Closed: 0s0-3s0_7, 0s0-2s0_3s0-10s0, 0s0-2s0_3s0-9s1, 0s0-2s0_4s0-7s0, 0s0-2s0_5s0-7s1, 0s0-4s0_1s1-9s1, 0s0-4s0_5s0-6s1, 0s0-4s0_6s1-7s1, 0s0-5s0_1s1-2s1, 0s0-5s0_1s1-9s0, 0s0-5s0_2s1-3s1, 0s0-5s0_6s0-10s1, 0s0-5s0_7s0-9s0.
Partial: 0s0-5s0_1s0-6s1, 0s0-3s0_4.

## Totals per stratum (new records)

| stratum | roots | closed | partial | not reached | certified | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------|----------|---------|---------|
| H6(2,0)/two | 9 | 4 | 0 | 5 | 4 | 0 | 194 | 117 |
| H6(3,0)/one | 2 | 1 | 1 | 0 | 203 | 0 | 6382 | 4859 |
| H6(4,0)/one | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(4,0)/two | 7 | 3 | 0 | 4 | 3 | 0 | 461 | 108 |
| H6(5,0)/one | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(5,0)/two | 16 | 5 | 1 | 10 | 289 | 1 | 1608 | 4551 |
| **all** | 36 | 13 | 2 | 21 | 499 | 1 | 8646 | 9635 |

New records: 509 (499 certified, 9 split, 1 UNKNOWN timeout). Every certified node has `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr).

## compose.py

`compose.txt`: `certified_nodes: 499, class_covered: false`, as expected for one shard. It recomputed the CNF sha256 of all 499 certified nodes.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. There are no `cake_lpr: none` records (see Setup for the nodes killed at END).
- Memory: at most about 8 GB used of 15.7 GB, with no OOM.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (new records only), `driver0.log`–`driver2.log` (last 100 lines each), `compose.txt`, `README.md`.

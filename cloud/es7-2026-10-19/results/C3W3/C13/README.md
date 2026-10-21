# C3W3 / C13: wave 3, list C_s1two.tsv, shard 13 of 18, 3-fold class (m = 11, k = 7)

**Result: 19 of my 32 roots are closed, 1 is partial (stopped at END) and 12 were not reached. No SAT. No proof rejection.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:43:25 UTC on 2026-10-21, END 10:28:25 UTC (start + 6 h − 15 min).
Task: `results/C3W3/TASK.md` at 640a56c2, with V = C13, LIST = C_s1two.tsv, j = 13, N = 18, LANES = 1, JOBS = 3, SLICE = 2.0, H = 6.0.

- C3-S tools: worktree of 132398c (132398cdc801ee5df204eda8567b72abdbfc4341) at `/opt/c3s`, unmodified.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); its example prints `s VERIFIED UNSAT`.
- lrat-check from drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. Sanity check on {1},{-1}: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: the rows of `lists/C_s1two.tsv` with row ≡ 13 (mod 18), 32 roots (`roots.tsv`). One lane (`lane0.sh`), `--jobs 3`, slice min(2.0 h, time left).

**Seeded records: 1,426** (1,402 certified, 24 split) at the start of `/opt/work/out0.jsonl`, for the 3 partial roots:
`0s0-2s1_1s0-3s1` (500 certified + 8 split, from C3WAVE2/K25), `0s0-1s1_3s1-10s1` (367 + 8, C3WAVE1/C11), `0s0-1s1_9s1-10s0` (535 + 8, C3WAVE2/K12).
No matching records were in any recheck.jsonl or C3S0 file. `out.jsonl` holds only the 1,957 new records (the lines after the seeded ones).

## Per root

Status "closed" = `close_tree.py` reported `open_frontier: 0` (every leaf certified, counting the seeded records). Certified nodes, splits (pre-splits included), timeouts (UNKNOWN at the cap) and times count new records only. Depth = number of layers (roots are at depth 2). Times are summed per node, not wall clock.

| row | root | stratum | status | certified by depth | splits | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| 13 | 0s0-2s1_1s0-3s1 | H6(2,1)/two | closed | d3: 46 | 0 | 0 | 1765 | 1224 |
| 31 | 0s0-2s1_1s0-5s0 | H6(2,1)/two | closed | d2: 1 | 0 | 0 | 28 | 20 |
| 49 | 0s0-2s1_3s1-8s0 | H6(2,1)/two | closed | d2: 1 | 0 | 0 | 253 | 41 |
| 67 | 0s0-2s1_5s0-6s0 | H6(2,1)/two | closed | d2: 1 | 0 | 0 | 35 | 28 |
| 85 | 0s0-3s1_1s0-5s0 | H6(3,1)/two | closed | d2: 1 | 0 | 0 | 29 | 25 |
| 103 | 0s0-3s1_1s1-8s0 | H6(3,1)/two | closed | d2: 1 | 0 | 0 | 46 | 28 |
| 121 | 0s0-3s1_4s1-5s1 | H6(3,1)/two | closed | d2: 1 | 0 | 0 | 37 | 27 |
| 139 | 0s0-3s1_5s1-6s1 | H6(3,1)/two | closed | d2: 1 | 0 | 0 | 34 | 28 |
| 157 | 0s0-4s1_1s0-3s1 | H6(4,1)/two | closed | d3: 84, d4: 462 | 8 | 1 | 5788 | 8069 |
| 175 | 0s0-4s1_1s1-6s1 | H6(4,1)/two | closed | d2: 1 | 0 | 0 | 262 | 34 |
| 193 | 0s0-4s1_2s0-9s1 | H6(4,1)/two | closed | d2: 1 | 0 | 0 | 68 | 23 |
| 211 | 0s0-4s1_6s0-7s0 | H6(4,1)/two | closed | d2: 1 | 0 | 0 | 36 | 20 |
| 229 | 0s0-5s1_1s0-3s0 | H6(5,1)/two | closed | d2: 1 | 0 | 0 | 25 | 18 |
| 247 | 0s0-5s1_1s1-4s0 | H6(5,1)/two | closed | d3: 84, d4: 462 | 8 | 1 | 5474 | 8263 |
| 265 | 0s0-5s1_2s0-8s1 | H6(5,1)/two | closed | d2: 1 | 0 | 0 | 279 | 34 |
| 283 | 0s0-5s1_6s0-8s0 | H6(5,1)/two | closed | d2: 1 | 0 | 0 | 34 | 22 |
| 301 | 0s0-1s1_3s1-10s1 | H6(1,1)/two | closed | d3: 84, d4: 95 | 0 | 0 | 3719 | 3376 |
| 319 | 0s0-1s1_9s1-10s0 | H6(1,1)/two | closed | d3: 11 | 0 | 0 | 436 | 276 |
| 337 | 0s0-2s1_1s1-8s1 | H6(2,1)/two | closed | d3: 84, d4: 462 | 8 | 1 | 6342 | 8288 |
| 355 | 0s0-2s1_6s0-9s1 | H6(2,1)/two | partial (stopped at END) | d4: 34 | 8 | 1 | 496 | 488 |
| 373 | 0s0-2s1_7s1-9s1 | H6(2,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 391 | 0s0-3s1_2s0-5s0 | H6(3,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 409 | 0s0-3s1_2s1-8s0 | H6(3,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 427 | 0s0-3s1_6s1-9s1 | H6(3,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 445 | 0s0-3s1_8s1-10s1 | H6(3,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 463 | 0s0-4s1_2s1-7s0 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 481 | 0s0-4s1_3s1-10s0 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 499 | 0s0-4s1_7s0-10s0 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 517 | 0s0-4s1_9s0-10s1 | H6(4,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 535 | 0s0-5s1_3s0-8s1 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 553 | 0s0-5s1_4s0-6s1 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |
| 571 | 0s0-5s1_7s0-10s0 | H6(5,1)/two | not reached | – | 0 | 0 | 0 | 0 |


## Totals per stratum

| stratum | roots | closed | partial | not reached | certified | splits | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| H6(2,1)/two | 7 | 5 | 1 | 1 | 629 | 16 | 2 | 8919 | 10090 |
| H6(3,1)/two | 8 | 4 | 0 | 4 | 4 | 0 | 0 | 146 | 108 |
| H6(4,1)/two | 8 | 4 | 0 | 4 | 549 | 8 | 1 | 6154 | 8146 |
| H6(5,1)/two | 7 | 4 | 0 | 3 | 549 | 8 | 1 | 5813 | 8336 |
| H6(1,1)/two | 2 | 2 | 0 | 0 | 190 | 0 | 0 | 4155 | 3652 |


All roots kept by the H6 mirror reduction (`h6m_kept` = yes, rows 13–283) are closed; of the others, rows 301–337 are closed, 355 is partial and 373–571 were not reached.

Total new records: 1,957, of which 1,921 certified UNSAT (all with `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr), 4 UNKNOWN at the cap (each then split) and 32 split records (pre-splits included).

## Partial root

`0s0-2s1_6s0-9s1` (row 355) started 10:21:17 with a 0.119 h slice (time left before END). At END its batch of depth-4 nodes was still running; the runner and the solver/checker processes were killed at 10:30 UTC. Killed nodes wrote no record, so there is no `cake_lpr: none` record to re-check. Its 34 certified, 8 split and 1 timeout records are in `out.jsonl` and can be resumed.

## SAT / proof rejections / memory

- **SAT: none.**
- **PROOF NOT ACCEPTED: none.** Every UNSATISFIABLE record is certified by both checkers.
- Memory: no problem; used memory peaked around 10 GB of 15 GB with 3 jobs.

## compose.py

`python3 $TOOLS/compose.py /opt/work/base.cnf results/C3W3/C13/out.jsonl` (`compose.txt`; new records only, so the class is not expected to be covered):
(compose.py still running at commit time; result added in the next commit)

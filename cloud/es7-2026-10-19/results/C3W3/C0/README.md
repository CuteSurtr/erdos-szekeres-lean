# C3W3 / C0: list C_s1two.tsv, shard 0 of 18, 1 lane, --jobs 3, 2.0 h slice, 6 h budget

**Result: 5 of my 33 roots are closed. Root 6 (`0s0-3s1_1s0-9s0`) is partial, and roots 7–33 were not reached. No SAT. No proof rejection.** No memory problem was seen (free memory never dropped below about 5 GB).

## Tools and base CNF (`tools.txt`)

- C3-S tools: git worktree of commit 132398c at /opt/c3s, used unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (the bundled example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch. Sanity check: LRAT `3 0 0` on {1},{-1} is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- One VM: 4 cores, 15 GB, no swap (`env.txt`). Start 04:42:24 UTC. END = start + 6 h − 15 min = 10:27:24 UTC. At END, a watchdog in `lane0.sh` killed the running driver, solvers and checkers (10:27:31).

## Seeded records

1,301 certified or split records went into the lane-0 out file before the run: 42 for `0s0-1s1_2s0-5s1`, 525 for `0s0-2s1_3s1-4s0`, 543 for `0s0-1s1_5s1-8s0` and 191 for `0s0-3s1_2s1-6s0`. They came from 77 files (C3WAVE1/C3WAVE2 out and recheck files, and C3S0 out files). `out.jsonl` holds only the 2,206 new records.

## Per root

The counts below are new records only. "Timeouts" are UNKNOWN results at the cap, and each one was then split. Solve and check times are summed per node, so they are not wall-clock time.

| row | root | stratum | h6m | list status | status | certified by depth | timeouts (UNKNOWN) | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0s0-1s1_2s0-5s1 | H6(1,1)/two | yes | partial | closed | d3: 50, d4: 462 | 0 | 0 | 3929 | 8001 |
| 18 | 0s0-2s1_3s1-4s0 | H6(2,1)/two | yes | partial | closed | d3: 29 | 0 | 0 | 1095 | 862 |
| 36 | 0s0-2s1_3s0-4s1 | H6(2,1)/two | yes | untouched | closed | d3: 84, d4: 462 | 1 | 8 | 6226 | 9450 |
| 54 | 0s0-2s1_4s0-7s0 | H6(2,1)/two | yes | untouched | closed | d2: 1 | 0 | 0 | 36 | 21 |
| 72 | 0s0-2s1_5s0-8s1 | H6(2,1)/two | yes | untouched | closed | d3: 84, d4: 462 | 1 | 8 | 5648 | 9309 |
| 90 | 0s0-3s1_1s0-9s0 | H6(3,1)/two | yes | untouched | partial | d3: 83, d4: 462 | 1 | 8 | 5161 | 9043 |
| 108 | 0s0-3s1_4s0-10s1 | H6(3,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 126 | 0s0-3s1_4s1-8s0 | H6(3,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 144 | 0s0-3s1_5s1-9s1 | H6(3,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 162 | 0s0-4s1_1s0-7s1 | H6(4,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 180 | 0s0-4s1_1s1-9s0 | H6(4,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 198 | 0s0-4s1_5s0-7s0 | H6(4,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 216 | 0s0-4s1_6s0-9s1 | H6(4,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 234 | 0s0-5s1_1s0-6s1 | H6(5,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 252 | 0s0-5s1_1s1-8s0 | H6(5,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 270 | 0s0-5s1_2s1-3s0 | H6(5,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 288 | 0s0-5s1_6s1-7s0 | H6(5,1)/two | yes | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 306 | 0s0-1s1_5s1-8s0 | H6(1,1)/two | no | partial | not reached | – | 0 | 0 | 0 | 0 |
| 324 | 0s0-3s1_2s1-6s0 | H6(3,1)/two | no | partial | not reached | – | 0 | 0 | 0 | 0 |
| 342 | 0s0-2s1_4s1-10s1 | H6(2,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 360 | 0s0-2s1_6s1-9s0 | H6(2,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 378 | 0s0-2s1_8s1-10s0 | H6(2,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 396 | 0s0-3s1_2s0-7s1 | H6(3,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 414 | 0s0-3s1_5s0-10s0 | H6(3,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 432 | 0s0-3s1_7s0-9s0 | H6(3,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 450 | 0s0-3s1_9s1-10s0 | H6(3,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 468 | 0s0-4s1_2s1-9s1 | H6(4,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 486 | 0s0-4s1_3s1-6s1 | H6(4,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 504 | 0s0-4s1_7s1-10s1 | H6(4,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 522 | 0s0-5s1_2s0-4s1 | H6(5,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 540 | 0s0-5s1_3s1-4s0 | H6(5,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 558 | 0s0-5s1_4s0-9s0 | H6(5,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 576 | 0s0-5s1_8s0-10s0 | H6(5,1)/two | no | untouched | not reached | – | 0 | 0 | 0 | 0 |

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 2 | 1 | 0 | 1 | 512 | 0 | 3929 | 8001 |
| H6(2,1)/two | 7 | 4 | 0 | 3 | 1122 | 2 | 13005 | 19642 |
| H6(3,1)/two | 9 | 0 | 1 | 8 | 545 | 1 | 5161 | 9043 |
| H6(4,1)/two | 7 | 0 | 0 | 7 | 0 | 0 | 0 | 0 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |

All 33 roots are in the H6(k,1)/two strata. Rows 0–288 have h6m_kept = yes; rows 306–576 have no.

Overall there are 2,179 newly certified nodes. Every one has lrat-check `c VERIFIED` (E2 patch) and cake_lpr `s VERIFIED UNSAT`. There were 3 UNKNOWN timeouts, each split. No UNSAT result was left uncertified. The kill at END wrote no partial records, so there is no `cake_lpr: none` record and nothing needed a re-check (no `recheck.jsonl`).

## compose.py

`compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`): 2,179 certified nodes, `class_covered: false` (expected, since this is one shard of one list). compose recomputed the CNF sha256 of every certified node from the base CNF.

## SAT / proof rejection / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only; resume `0s0-3s1_1s0-9s0` by seeding it with these records), `driver0.log` (last 100 lines), `compose.txt`.

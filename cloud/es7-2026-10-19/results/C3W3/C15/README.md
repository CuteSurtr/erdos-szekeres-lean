# C3W3 / C15: wave 3, list C_s1two.tsv, shard 15 of 18

**Result: 16 of my 32 roots closed, 1 partial, 15 not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:43:43 UTC on 2026-10-21, END 10:28:43 UTC (6 h − 15 min).
One lane (`lane0.sh`), `close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(2.0, hours left before END).

- C3-S tools: worktree of commit 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc + E2 patch
  (sanity: `3 0 0` rejected by both, `3 0 1 2 0` accepted by both). Details in `tools.txt`.
- Base CNF: `p cnf 168399 4154921`, sha256 `bf0e502e…6cd6da`, matches.
- Roots: rows of `C3W3/lists/C_s1two.tsv` with row ≡ 15 (mod 18): 32 roots (`roots.tsv`), 3 of them partial in the list.

**Seeded records: 730** (certified or split, for the 3 partial roots: 96 from `C3WAVE1/C12/out.jsonl` for 0s0-2s1_1s0-5s1,
530 from `C3WAVE2/K10/out.jsonl` for 0s0-1s1_4s1-10s1, 104 from `C3WAVE2/K07/out.jsonl` for 0s0-2s1_1s1-7s1). `out.jsonl` holds only the 2,147 new records.

## Per root (depth = number of layers; roots are at depth 2; counts are new records only)

"splits" counts split records (timeout splits and pre-splits). Solve and check times are summed per node (3 jobs on 4 cores), not wall clock.

| row | root | stratum | list status | status | certified by depth (new) | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 15 | 0s0-2s1_1s0-5s1 | H6(2,1)/two | partial | closed | d3: 84, d4: 374 | 0 | 0 | 4061 | 7330 |
| 33 | 0s0-2s1_1s0-7s1 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 293 | 40 |
| 51 | 0s0-2s1_3s1-9s1 | H6(2,1)/two | untouched | closed | d3: 84, d4: 462 | 1 | 8 | 5567 | 9176 |
| 69 | 0s0-2s1_5s0-7s0 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 33 | 22 |
| 87 | 0s0-3s1_1s0-6s1 | H6(3,1)/two | untouched | closed | d3: 84, d4: 462 | 1 | 8 | 4791 | 8957 |
| 105 | 0s0-3s1_1s1-9s0 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 37 | 21 |
| 123 | 0s0-3s1_4s1-6s1 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 35 | 23 |
| 141 | 0s0-3s1_5s1-7s1 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 33 | 23 |
| 159 | 0s0-4s1_1s0-6s0 | H6(4,1)/two | untouched | closed | d2: 1 | 0 | 0 | 127 | 26 |
| 177 | 0s0-4s1_1s1-7s1 | H6(4,1)/two | untouched | closed | d3: 84, d4: 462 | 1 | 8 | 5031 | 8943 |
| 195 | 0s0-4s1_5s0-10s1 | H6(4,1)/two | untouched | closed | d2: 1 | 0 | 0 | 265 | 42 |
| 213 | 0s0-4s1_6s0-8s0 | H6(4,1)/two | untouched | closed | d2: 1 | 0 | 0 | 33 | 22 |
| 231 | 0s0-5s1_1s0-4s0 | H6(5,1)/two | untouched | closed | d2: 1 | 0 | 0 | 34 | 25 |
| 249 | 0s0-5s1_1s1-6s1 | H6(5,1)/two | untouched | closed | d2: 1 | 0 | 0 | 256 | 39 |
| 267 | 0s0-5s1_2s0-9s1 | H6(5,1)/two | untouched | closed | d2: 1 | 0 | 0 | 58 | 23 |
| 285 | 0s0-5s1_6s0-9s0 | H6(5,1)/two | untouched | closed | d2: 1 | 0 | 0 | 22 | 21 |
| 303 | 0s0-1s1_4s1-10s1 | H6(1,1)/two | partial | partial | d3: 12 | 0 | 0 | 407 | 319 |
| 321 | 0s0-2s1_1s1-7s1 | H6(2,1)/two | partial | not reached | – | 0 | 0 | 0 | 0 |
| 339 | 0s0-2s1_1s1-9s1 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 357 | 0s0-2s1_6s1-7s0 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 375 | 0s0-2s1_8s0-10s1 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 393 | 0s0-3s1_2s0-6s0 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 411 | 0s0-3s1_2s1-9s0 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 429 | 0s0-3s1_7s0-10s1 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 447 | 0s0-3s1_8s1-9s1 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 465 | 0s0-4s1_2s1-8s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 483 | 0s0-4s1_3s1-5s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 501 | 0s0-4s1_7s0-9s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 519 | 0s0-4s1_9s1-10s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 537 | 0s0-5s1_3s0-9s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 555 | 0s0-5s1_4s0-7s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 573 | 0s0-5s1_7s1-10s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |

| stratum | roots | closed | partial | not reached | certified (new) | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(2,1)/two | 8 | 4 | 0 | 4 | 1006 | 1 | 9953 | 16568 |
| H6(3,1)/two | 8 | 4 | 0 | 4 | 549 | 1 | 4896 | 9023 |
| H6(4,1)/two | 8 | 4 | 0 | 4 | 549 | 1 | 5456 | 9031 |
| H6(5,1)/two | 7 | 4 | 0 | 3 | 4 | 0 | 371 | 108 |
| H6(1,1)/two | 1 | 0 | 1 | 0 | 12 | 0 | 407 | 319 |


Totals: new records: 2147 certified: 2120 {2: 12, 3: 348, 4: 1760} UNKNOWN: 3 SAT: 0 uncertified UNSAT: 0

Closed roots (16): 0s0-2s1_1s0-5s1 (was partial), 0s0-2s1_1s0-7s1, 0s0-2s1_3s1-9s1, 0s0-2s1_5s0-7s0, 0s0-3s1_1s0-6s1, 0s0-3s1_1s1-9s0,
0s0-3s1_4s1-6s1, 0s0-3s1_5s1-7s1, 0s0-4s1_1s0-6s0, 0s0-4s1_1s1-7s1, 0s0-4s1_5s0-10s1, 0s0-4s1_6s0-8s0, 0s0-5s1_1s0-4s0,
0s0-5s1_1s1-6s1, 0s0-5s1_2s0-9s1, 0s0-5s1_6s0-9s0 (each has `open_frontier: 0` in `driver0.log`).
Partial: 0s0-1s1_4s1-10s1 (started 10:25:46 with a 0.049 h slice, 12 new certified depth-3 nodes). Not reached: rows 321–573 (15 roots, including partial 0s0-2s1_1s1-7s1).
The 3 timeouts (UNKNOWN at 300 s) are the root nodes 0s0-2s1_3s1-9s1, 0s0-3s1_1s0-6s1 and 0s0-4s1_1s1-7s1, all split and then fully certified.

## Stop at END

The driver for 0s0-1s1_4s1-10s1 was still in its batch at 10:29:53, past END, so I killed it at 10:30. Two solvers I killed wrote
UNKNOWN records at ~1 s (`0s0-1s1_4s1-10s1_7s1-8s0`, `0s0-1s1_4s1-10s1_7s0-8s1`), and the driver split them. Those 14 records are artefacts of the
kill, not timeouts, so I removed them from `out.jsonl` and kept them in `killed_dropped.jsonl`. Those nodes stay open. No record has `cake_lpr: none`
and no UNSAT record is uncertified, so there was nothing to re-check.

## compose.py

`compose.txt`: `certified_nodes: 2120`, `class_covered: false`, `uncovered_frontier_nodes: 856` (expected, this is one shard). compose recomputed the CNF sha256 of every certified node.

## SAT / proof rejection / memory

- SAT: none. No SAT FOUND, no SATISFIABLE record.
- PROOF NOT ACCEPTED: none. All 2,120 new certified nodes have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- Memory: peak use about 9 GB of 15 GB with 3 jobs. No OOM.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `killed_dropped.jsonl`, `compose.txt`, `README.md`.

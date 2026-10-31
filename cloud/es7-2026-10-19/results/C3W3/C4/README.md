# C3W3 / C4: list C_s1two.tsv, shard 4 of 18, one lane

**Result: 6 roots closed, 1 partial, 26 not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:42:36 UTC on 2026-10-21, H = 6.0 h, END = 10:27:36 UTC.
LANES = 1, JOBS = 3, SLICE = 2.0 h. Task file `results/C3W3/TASK.md` at 640a56c2.

- C3-S tools: worktree of 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). The bundled example prints `s VERIFIED UNSAT`.
- lrat-check from drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with the E2 patch applied. Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none`: header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

Details are in `tools.txt`.

Roots: the rows of `lists/C_s1two.tsv` with row ≡ 4 (mod 18). That gives 33 roots (`roots.tsv`); 3 were partial and 30 untouched.

**Seeded records: 1,328** (certified or split records under the 3 partial roots, taken from C3WAVE1, C3WAVE2 and C3S0 `out.jsonl`/`recheck.jsonl`):
317 for 0s0-1s1_3s0-5s1, 471 for 0s0-2s1_4s0-5s1 and 540 for 0s0-1s1_6s0-9s1. They are not in `out.jsonl`, which holds only the 1,980 new records.

## Per root

Depth is the number of layers (roots are at depth 2). Certified counts, timeouts and splits are for new records only. Solve and check times are per-node sums, not wall-clock time. A timeout is an UNKNOWN result at the cap, after which the node was split.

| row | root | stratum | was | status | new certified by depth | new timeouts (by cap) | new splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 0s0-1s1_3s0-5s1 | H6(1,1)/two | partial | **closed** | d3: 84, d4: 153 | 0 | 0 | 3860 | 4645 |
| 22 | 0s0-2s1_4s0-5s1 | H6(2,1)/two | partial | **closed** | d3: 83 | 0 | 0 | 3152 | 2362 |
| 40 | 0s0-2s1_3s0-7s1 | H6(2,1)/two | untouched | **closed** | d3: 84, d4: 462 | 1 at 300 s | 8 | 5014 | 9294 |
| 58 | 0s0-2s1_4s0-9s0 | H6(2,1)/two | untouched | **closed** | d2: 1 | 0 | 0 | 260 | 42 |
| 76 | 0s0-2s1_5s1-8s1 | H6(2,1)/two | untouched | **closed** | d2: 1 | 0 | 0 | 39 | 29 |
| 94 | 0s0-3s1_1s1-2s0 | H6(3,1)/two | untouched | **closed** | d3: 84, d4: 462 | 1 at 300 s | 8 | 5976 | 9224 |
| 112 | 0s0-3s1_4s0-6s1 | H6(3,1)/two | untouched | partial | d3: 77, d4: 462 | 1 at 300 s | 8 | 5741 | 9156 |
| 130 | 0s0-3s1_5s0-6s0 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 148 | 0s0-3s1_6s0-8s1 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 166 | 0s0-4s1_1s0-9s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 184 | 0s0-4s1_2s0-5s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 202 | 0s0-4s1_5s0-9s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 220 | 0s0-4s1_6s1-8s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 238 | 0s0-5s1_1s0-8s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 256 | 0s0-5s1_2s0-10s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 274 | 0s0-5s1_2s1-7s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 292 | 0s0-5s1_6s1-9s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 310 | 0s0-1s1_6s0-9s1 | H6(1,1)/two | partial | not reached | – | 0 | 0 | 0 | 0 |
| 328 | 0s0-1s1_8s1-9s0 | H6(1,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 346 | 0s0-2s1_5s0-9s1 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 364 | 0s0-2s1_7s0-8s0 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 382 | 0s0-2s1_9s0-10s0 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 400 | 0s0-3s1_2s0-9s1 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 418 | 0s0-3s1_5s1-9s0 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 436 | 0s0-3s1_7s1-8s0 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 454 | 0s0-4s1_2s0-3s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 472 | 0s0-4s1_3s0-5s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 490 | 0s0-4s1_3s1-8s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 508 | 0s0-4s1_8s0-10s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 526 | 0s0-5s1_3s0-10s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 544 | 0s0-5s1_3s1-7s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 562 | 0s0-5s1_4s1-6s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |
| 580 | 0s0-5s1_8s1-10s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 |

Root 112 (`0s0-3s1_4s0-6s1`) had a 1.41 h slice, ending at END. At END its last batch was still running, so I killed the runner at 10:30 UTC. The killed workers wrote no records, so there is no `cake_lpr: none` record and nothing needed a re-check. Root 0s0-1s1_6s0-9s1 (row 310, partial, 540 seeded records) was not reached.

## Totals per stratum (new records)

| stratum | roots | closed | partial | not reached | new certified | new timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 3 | 1 | 0 | 2 | 237 | 0 | 3860 | 4645 |
| H6(2,1)/two | 7 | 4 | 0 | 3 | 631 | 1 | 8466 | 11727 |
| H6(3,1)/two | 7 | 1 | 1 | 5 | 1085 | 2 | 11716 | 18380 |
| H6(4,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |

new records: 1980 certified: 1953 SAT: 0

Every new certified record has `c VERIFIED` (lrat-check with the E2 patch) and `s VERIFIED UNSAT` (cake_lpr).

## compose.py

`compose.py /opt/work/base.cnf out.jsonl` gives `certified_nodes: 1953, class_covered: false` (`compose.txt`). This is expected, because this machine holds only one shard.

## SAT / proof rejection / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: at most about 9 GB used of 15 GB, with no failures.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `compose.txt`.

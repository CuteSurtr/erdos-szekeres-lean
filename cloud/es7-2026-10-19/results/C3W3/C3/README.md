# C3W3 / C3: wave 3, list C_s1two.tsv, shard 3 of 18, 1 lane

**Result: 10 of my 33 roots are closed (every leaf certified), 0 partial, 23 not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-21 04:42:41 UTC, END 10:27:41 UTC (start + 6 h - 15 min); the runner finished its last root at 10:29:47.
Tools (`tools.txt`): C3-S tools from a worktree of commit 132398c at /opt/c3s, unmodified; CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (example prints `s VERIFIED UNSAT`);
drat-trim lrat-check 2e3b2dc with the E2 patch (sanity: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both).
Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

Roots: rows of `lists/C_s1two.tsv` with row ≡ 3 (mod 18), 33 roots (`roots.tsv`). One lane (`lane0.sh`), `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles`, slice min(2.0, hours left).

Seeded: 1,530 records at the start of /opt/work/out0.jsonl (not in the committed `out.jsonl`, which holds only the 2,299 new records):
- 0s0-1s1_2s1-8s1: 536 (528 certified, 8 split) from C3WAVE1/C16/out.jsonl
- 0s0-2s1_3s1-7s0: 497 (489 certified, 8 split) from C3WAVE2/K35/out.jsonl
- 0s0-1s1_6s0-8s1: 497 (489 certified, 8 split) from C3WAVE2/K28/out.jsonl (root not reached in this run)

## Per root (new records only; depth = number of layers, roots at depth 2)

Timeouts = UNKNOWN at the cap (then split). Solve and check seconds are summed per node (3 jobs on 4 cores, so not wall-clock).

| row | root | stratum | list status | status | new certified by depth | splits | timeouts | SAT | uncertified UNSAT | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 0s0-1s1_2s1-8s1 | H6(1,1)/two | partial | closed | d3: 18 | 0 | 0 | 0 | 0 | 323 | 410 |
| 21 | 0s0-2s1_3s1-7s0 | H6(2,1)/two | partial | closed | d3: 57 | 0 | 0 | 0 | 0 | 1191 | 1311 |
| 39 | 0s0-2s1_3s0-7s0 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0 | 0 | 97 | 26 |
| 57 | 0s0-2s1_4s0-8s1 | H6(2,1)/two | untouched | closed | d3: 84, d4: 462 | 8 | 1 | 0 | 0 | 4462 | 8417 |
| 75 | 0s0-2s1_5s1-7s1 | H6(2,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0 | 0 | 35 | 25 |
| 93 | 0s0-3s1_1s1-10s1 | H6(3,1)/two | untouched | closed | d3: 84, d4: 462 | 8 | 1 | 0 | 0 | 6210 | 9037 |
| 111 | 0s0-3s1_4s0-6s0 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0 | 0 | 32 | 20 |
| 129 | 0s0-3s1_4s1-9s1 | H6(3,1)/two | untouched | closed | d3: 84, d4: 462 | 8 | 1 | 0 | 0 | 4712 | 8653 |
| 147 | 0s0-3s1_6s0-8s0 | H6(3,1)/two | untouched | closed | d2: 1 | 0 | 0 | 0 | 0 | 31 | 22 |
| 165 | 0s0-4s1_1s0-9s0 | H6(4,1)/two | untouched | closed | d3: 84, d4: 462 | 8 | 1 | 0 | 0 | 4572 | 8515 |
| 183 | 0s0-4s1_2s0-10s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 201 | 0s0-4s1_5s0-8s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 219 | 0s0-4s1_6s1-8s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 237 | 0s0-5s1_1s0-8s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 255 | 0s0-5s1_1s1-9s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 273 | 0s0-5s1_2s1-7s0 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 291 | 0s0-5s1_6s1-8s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 309 | 0s0-1s1_6s0-8s1 | H6(1,1)/two | partial | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 327 | 0s0-1s1_8s1-10s0 | H6(1,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 345 | 0s0-2s1_5s0-9s0 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 363 | 0s0-2s1_7s0-10s1 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 381 | 0s0-2s1_8s1-9s1 | H6(2,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 399 | 0s0-3s1_2s0-9s0 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 417 | 0s0-3s1_5s1-10s1 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 435 | 0s0-3s1_7s1-10s1 | H6(3,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 453 | 0s0-4s1_2s0-3s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 471 | 0s0-4s1_3s0-5s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 489 | 0s0-4s1_3s1-8s0 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 507 | 0s0-4s1_7s1-9s1 | H6(4,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 525 | 0s0-5s1_2s1-4s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 543 | 0s0-5s1_3s1-6s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 561 | 0s0-5s1_4s1-10s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |
| 579 | 0s0-5s1_8s0-9s1 | H6(5,1)/two | untouched | not reached | – | 0 | 0 | 0 | 0 | 0 | 0 |

| stratum | roots | closed | partial | not reached | new certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 3 | 1 | 0 | 2 | 18 | 0 | 323 | 410 |
| H6(2,1)/two | 7 | 4 | 0 | 3 | 605 | 1 | 5785 | 9779 |
| H6(3,1)/two | 7 | 4 | 0 | 3 | 1094 | 2 | 10985 | 17732 |
| H6(4,1)/two | 8 | 1 | 0 | 7 | 546 | 1 | 4572 | 8515 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |

Totals: 2,299 new records, 2,263 new certified nodes (each with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`), 0 SATISFIABLE, 0 UNSAT without both checkers' acceptance, 0 `cake_lpr: none`.

Closed roots: 0s0-1s1_2s1-8s1, 0s0-2s1_3s1-7s0 (both resumed from the seeds), 0s0-2s1_3s0-7s0, 0s0-2s1_4s0-8s1, 0s0-2s1_5s1-7s1, 0s0-3s1_1s1-10s1, 0s0-3s1_4s0-6s0, 0s0-3s1_4s1-9s1, 0s0-3s1_6s0-8s0, 0s0-4s1_1s0-9s0.
Each has `open_frontier: 0` in the driver log.
Not reached: the remaining 23 rows (from row 183 on), among them the partial root 0s0-1s1_6s0-8s1 (its seeds are unchanged in the earlier waves).

## compose.py

`compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`): 2,263 certified nodes, `class_covered: false` (expected: one shard of one list, new records only).

## SAT / proof rejections / memory

None. The driver log has no `SAT FOUND`, `PROOF NOT ACCEPTED` or traceback; free memory never went below ~4 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `compose.txt`, `README.md`.

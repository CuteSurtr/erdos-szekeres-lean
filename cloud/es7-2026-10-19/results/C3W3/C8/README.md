# C3W3 / C8: list C_s1two.tsv, shard 8 of 18, 1 lane x --jobs 3, slice 2.0 h, 6 h budget

**Result: 6 of my 33 roots closed, 1 partial (`0s0-3s1_4s0-8s1`), 26 not reached. No SAT. No proof rejection. No memory problem.**

## Tools and base CNF

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:42:44 UTC (2026-10-21), END = start + 6 h - 15 min = 10:27:44 UTC.

- C3-S tools: worktree of commit 132398c at /opt/c3s, unmodified.
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1); cake_lpr a36874a8 (`make cake_lpr`, its example prints `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`. Sanity check passed: LRAT `3 0 0` on {1},{-1} rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches). Details in `tools.txt`.

## Seeded records

1,118 records seeded into `out0.jsonl` (certified or split, from C3WAVE1/C3WAVE2 out/recheck and C3S0 out):
`0s0-1s1_3s1-9s1` 208 (200 certified + 8 split), `0s0-4s1_1s0-5s1` 381 (373 + 8), `0s0-1s1_7s0-8s1` 529 (515 + 14; this root was not reached).
`out.jsonl` holds only the 2,102 new records (2,075 certified, 3 UNKNOWN timeouts, 24 split records).

## Per root (depth = number of layers; roots are at depth 2)

Columns count new records only. Splits include pre-splits (--split-singles). Solve and check times are summed per node (3 jobs share 4 cores).

| row | root | stratum | list status | status | certified by depth | timeouts | splits | solve s | check s |
|---|---|---|---|---|---|---|---|---|---|
| 8 | 0s0-1s1_3s1-9s1 | H6(1,1)/two | partial | **closed** | d3: 84, d4: 262 | – | – | 3938 | 6202 |
| 26 | 0s0-4s1_1s0-5s1 | H6(4,1)/two | partial | **closed** | d3: 84, d4: 89 | – | – | 3405 | 3643 |
| 44 | 0s0-2s1_3s1-10s1 | H6(2,1)/two | untouched | **closed** | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 6667 | 9698 |
| 62 | 0s0-2s1_4s1-7s0 | H6(2,1)/two | untouched | **closed** | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 5845 | 9556 |
| 80 | 0s0-3s1_1s0-10s1 | H6(3,1)/two | untouched | **closed** | d2: 1 | – | – | 61 | 28 |
| 98 | 0s0-3s1_1s1-5s1 | H6(3,1)/two | untouched | **closed** | d2: 1 | – | – | 61 | 32 |
| 116 | 0s0-3s1_4s0-8s1 | H6(3,1)/two | untouched | **partial** | d4: 462 | d2: 1 | d2: 1, d3: 7 | 2638 | 6871 |
| 134 | 0s0-3s1_5s0-8s0 | H6(3,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 152 | 0s0-4s1_1s0-10s0 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 170 | 0s0-4s1_1s1-2s1 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 188 | 0s0-4s1_2s0-7s0 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 206 | 0s0-4s1_5s1-6s1 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 224 | 0s0-4s1_7s1-8s1 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 242 | 0s0-5s1_1s1-10s1 | H6(5,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 260 | 0s0-5s1_2s0-6s0 | H6(5,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 278 | 0s0-5s1_2s1-9s1 | H6(5,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 296 | 0s0-5s1_7s0-9s0 | H6(5,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 314 | 0s0-1s1_7s0-8s1 | H6(1,1)/two | partial | **not reached** | – | – | – | 0 | 0 |
| 332 | 0s0-2s1_1s1-4s0 | H6(2,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 350 | 0s0-2s1_5s1-9s1 | H6(2,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 368 | 0s0-2s1_7s1-10s0 | H6(2,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 386 | 0s0-3s1_1s1-2s1 | H6(3,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 404 | 0s0-3s1_2s1-5s0 | H6(3,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 422 | 0s0-3s1_6s0-9s1 | H6(3,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 440 | 0s0-3s1_8s0-10s0 | H6(3,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 458 | 0s0-4s1_2s1-3s1 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 476 | 0s0-4s1_3s0-7s1 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 494 | 0s0-4s1_6s0-10s0 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 512 | 0s0-4s1_8s1-10s0 | H6(4,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 530 | 0s0-5s1_3s0-6s0 | H6(5,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 548 | 0s0-5s1_3s1-9s0 | H6(5,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 566 | 0s0-5s1_4s1-8s0 | H6(5,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |
| 584 | 0s0-5s1_9s0-10s0 | H6(5,1)/two | untouched | **not reached** | – | – | – | 0 | 0 |

| stratum | roots | closed | partial | not reached | certified | timeouts | solve s | check s |
|---|---|---|---|---|---|---|---|---|
| H6(1,1)/two | 2 | 1 | 0 | 1 | 346 | 0 | 3938 | 6202 |
| H6(2,1)/two | 5 | 2 | 0 | 3 | 1092 | 2 | 12512 | 19253 |
| H6(3,1)/two | 8 | 2 | 1 | 5 | 464 | 1 | 2760 | 6931 |
| H6(4,1)/two | 10 | 1 | 0 | 9 | 173 | 0 | 3405 | 3643 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |

Closed (every leaf certified, `open_frontier: 0`): `0s0-1s1_3s1-9s1`, `0s0-4s1_1s0-5s1`, `0s0-2s1_3s1-10s1`, `0s0-2s1_4s1-7s0`, `0s0-3s1_1s0-10s1`, `0s0-3s1_1s1-5s1`.

Partial: `0s0-3s1_4s0-8s1` (started 09:30:35 with a 0.953 h slice). The root timed out at 300 s and was split. Its 7 depth-3 children (single-orbit layers) were pre-split, and 462 depth-4 nodes were certified before the run was stopped at END. The depth-4 batch in progress (`close_tree.py` checks its deadline only between batches) was killed at 10:27:48. The nodes still in flight left no records, and no checker result was cut short in a record (no `cake_lpr: none`). This root's records stay in `out.jsonl` for resumption.

Not reached (26): rows 134–584 of my shard (`roots.tsv`), including the partial list root `0s0-1s1_7s0-8s1` (its 529 seed records are not in `out.jsonl`).

## compose.py

`compose.txt`: `{"certified_nodes": 2075, "class_covered": false, "uncovered_frontier_nodes": 749, ...}`. compose recomputed the CNF sha256 of all 2,075 certified nodes. As expected, the class is not covered, because this file holds only my shard's new records.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. Every UNSAT record is certified, with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- Memory: the lowest available memory sampled was 4.9 GB. There was no OOM.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `compose.txt`, `README.md`.

# C3W3 / C16: wave 3, 3-fold class (m = 11, k = 7), list C_s1two.tsv shard 16 of 18

**Result: 5 of my 32 roots are closed (every leaf certified) and 1 is partial. The other 26 were not reached. No SAT. No proof rejection. No memory problem.**

## Setup

Values: V = C16, LIST = C_s1two.tsv, j = 16, N = 18, LANES = 1, JOBS = 3, SLICE = 2.0 h, H = 6.0 h, TASK.md at 640a56c2.
Machine: one cloud VM with 4 cores, 15 GB RAM and no swap (`env.txt`). Start 04:42:53 UTC, END = 10:27:53 UTC.

- C3-S tools: worktree of 132398c at /opt/c3s, used unmodified.
- CaDiCaL 3.0.1 (c6073042) and cake_lpr a36874a8. The cake_lpr example prints `s VERIFIED UNSAT`.
- lrat-check 2e3b2dc with the E2 patch. Sanity check: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both. Details are in `tools.txt`.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. Both match.
- Roots: the rows of C_s1two.tsv with row ≡ 16 (mod 18), 32 roots (`roots.tsv`), run in one lane (`lane0.sh`) with `--jobs 3`.
- Seeded records: **1,114** certified or split records were put at the head of `out0.jsonl`:
  - 109 for `0s0-2s1_1s0-8s0` (C3WAVE1/C17);
  - 518 for `0s0-1s1_5s0-8s1` (C3WAVE2/K18);
  - 487 for `0s0-2s1_5s1-8s0` (C3WAVE2/K03).

  `out.jsonl` holds only the 2,401 new records, which are the lines after the seeded ones.

## Per root

Depth = number of layers; roots are at depth 2. Timeouts are UNKNOWN results at the cap. Times are summed per node, and three jobs share the 4 cores.

| # | row | root | stratum | h6m_kept | status | certified by depth | splits | timeouts | solve s | check s |
|---|-----|------|---------|----------|--------|--------------------|--------|----------|---------|---------|
| 1 | 16 | 0s0-2s1_1s0-8s0 | H6(2,1)/two | yes | **closed** | d3: 84, d4: 361 | – | – | 3257 | 6547 |
| 2 | 34 | 0s0-2s1_3s0-10s0 | H6(2,1)/two | yes | **closed** | d3: 84, d4: 462 | d2: 1, d3: 7 | d2: 1 | 4868 | 8873 |
| 3 | 52 | 0s0-2s1_4s0-5s0 | H6(2,1)/two | yes | **closed** | d2: 1 | – | – | 35 | 23 |
| 4 | 70 | 0s0-2s1_5s0-7s1 | H6(2,1)/two | yes | **closed** | d3: 84, d4: 462 | d2: 1, d3: 7 | d2: 1 | 6080 | 9647 |
| 5 | 88 | 0s0-3s1_1s0-7s0 | H6(3,1)/two | yes | **closed** | d3: 84, d4: 462 | d2: 1, d3: 7 | d2: 1 | 4122 | 8850 |
| 6 | 106 | 0s0-3s1_1s1-9s1 | H6(3,1)/two | yes | **partial (slice ended at END)** | d4: 281 | d2: 1, d3: 7 | d2: 1 | 2213 | 4465 |
| 7 | 124 | 0s0-3s1_4s1-7s0 | H6(3,1)/two | yes | **not reached** | – | – | – | – | – |
| 8 | 142 | 0s0-3s1_5s1-8s0 | H6(3,1)/two | yes | **not reached** | – | – | – | – | – |
| 9 | 160 | 0s0-4s1_1s0-6s1 | H6(4,1)/two | yes | **not reached** | – | – | – | – | – |
| 10 | 178 | 0s0-4s1_1s1-8s0 | H6(4,1)/two | yes | **not reached** | – | – | – | – | – |
| 11 | 196 | 0s0-4s1_5s0-6s0 | H6(4,1)/two | yes | **not reached** | – | – | – | – | – |
| 12 | 214 | 0s0-4s1_6s0-8s1 | H6(4,1)/two | yes | **not reached** | – | – | – | – | – |
| 13 | 232 | 0s0-5s1_1s0-4s1 | H6(5,1)/two | yes | **not reached** | – | – | – | – | – |
| 14 | 250 | 0s0-5s1_1s1-7s0 | H6(5,1)/two | yes | **not reached** | – | – | – | – | – |
| 15 | 268 | 0s0-5s1_2s1-10s0 | H6(5,1)/two | yes | **not reached** | – | – | – | – | – |
| 16 | 286 | 0s0-5s1_6s0-9s1 | H6(5,1)/two | yes | **not reached** | – | – | – | – | – |
| 17 | 304 | 0s0-1s1_5s0-8s1 | H6(1,1)/two | no | **not reached (partial from earlier waves)** | – | – | – | 0 | 0 |
| 18 | 322 | 0s0-2s1_5s1-8s0 | H6(2,1)/two | no | **not reached (partial from earlier waves)** | – | – | – | 0 | 0 |
| 19 | 340 | 0s0-2s1_3s1-10s0 | H6(2,1)/two | no | **not reached** | – | – | – | – | – |
| 20 | 358 | 0s0-2s1_6s1-8s0 | H6(2,1)/two | no | **not reached** | – | – | – | – | – |
| 21 | 376 | 0s0-2s1_8s0-9s0 | H6(2,1)/two | no | **not reached** | – | – | – | – | – |
| 22 | 394 | 0s0-3s1_2s0-6s1 | H6(3,1)/two | no | **not reached** | – | – | – | – | – |
| 23 | 412 | 0s0-3s1_2s1-9s1 | H6(3,1)/two | no | **not reached** | – | – | – | – | – |
| 24 | 430 | 0s0-3s1_7s0-8s0 | H6(3,1)/two | no | **not reached** | – | – | – | – | – |
| 25 | 448 | 0s0-3s1_9s0-10s0 | H6(3,1)/two | no | **not reached** | – | – | – | – | – |
| 26 | 466 | 0s0-4s1_2s1-8s1 | H6(4,1)/two | no | **not reached** | – | – | – | – | – |
| 27 | 484 | 0s0-4s1_3s1-5s1 | H6(4,1)/two | no | **not reached** | – | – | – | – | – |
| 28 | 502 | 0s0-4s1_7s0-9s1 | H6(4,1)/two | no | **not reached** | – | – | – | – | – |
| 29 | 520 | 0s0-5s1_1s1-4s1 | H6(5,1)/two | no | **not reached** | – | – | – | – | – |
| 30 | 538 | 0s0-5s1_3s1-10s0 | H6(5,1)/two | no | **not reached** | – | – | – | – | – |
| 31 | 556 | 0s0-5s1_4s0-8s0 | H6(5,1)/two | no | **not reached** | – | – | – | – | – |
| 32 | 574 | 0s0-5s1_7s1-10s1 | H6(5,1)/two | no | **not reached** | – | – | – | – | – |

Closed: `0s0-2s1_1s0-8s0` (resumed partial root), `0s0-2s1_3s0-10s0`, `0s0-2s1_4s0-5s0`, `0s0-2s1_5s0-7s1`, `0s0-3s1_1s0-7s0`.
Partial: `0s0-3s1_1s1-9s1`. It was started at 09:50:53 with a 0.617 h slice, and its records are in `out.jsonl` for resuming.

## Totals per stratum (new records only)

| stratum | roots | closed | partial | not reached | certified nodes | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------------|----------|---------|---------|
| H6(1,1)/two | 1 | 0 | 0 | 1 (partial earlier) | 0 | 0 | 0 | 0 |
| H6(2,1)/two | 8 | 4 | 0 | 4 (1 partial earlier) | 1538 | 2 | 14240 | 25090 |
| H6(3,1)/two | 8 | 1 | 1 | 6 | 827 | 2 | 6335 | 13315 |
| H6(4,1)/two | 7 | 0 | 0 | 7 | 0 | 0 | 0 | 0 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| **all** | 32 | 5 | 1 | 26 | **2365** | 4 | 20575 | 38405 |

All 2,365 certified nodes have lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. Every new UNSAT record is certified.

## compose.py

`compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`): 2,365 certified nodes, `class_covered: false`, as expected for one shard. It recomputed the CNF sha256 of every certified node.

## SAT, proof rejections, memory

- **SAT: none.**
- **PROOF NOT ACCEPTED: none.**
- **Memory:** no problem. At most 11 of 15 GB was in use.

## Incidents (these affect time only, not results)

1. **Worker restart, about 05:35 UTC.** The session's worker process restarted at about 05:35 UTC, which killed the runner while it was on root 1 (`0s0-2s1_1s0-8s0`). Every line of `out0.jsonl` was intact. Nodes that were in flight had no record, so they were solved again.
   - At 05:39:57 I restarted the runner as `lane0_resume.sh`. It is the same script, except that root 1 got only the rest of its original 2 h slice, up to 06:44:48.
   - Root 1 closed at 05:40:44.
   - `driver0.log` has a `=== RESTART` line at that point.
2. **Stopped by hand at END, 10:31:53 UTC.** At END, close_tree was still working through the frontier batch of root 6, since `--hours` is not checked within a running batch.
   - I killed the driver and its solver and checker processes at 10:31:53.
   - The nodes in flight left no records, so there are no `cake_lpr: none` records to re-check.
   - `driver0.log` has a `=== STOPPED BY HAND` line.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `lane0_resume.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `compose.txt`, `README.md`.

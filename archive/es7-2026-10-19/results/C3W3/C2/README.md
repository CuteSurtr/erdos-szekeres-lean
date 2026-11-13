# C3W3 / C2: list C_s1two.tsv, shard 2 of 18, 3-fold class (m = 11, k = 7)

**Result: 8 of my 33 roots are closed, 1 is partial (`0s0-3s1_6s0-7s1`, stopped at END) and 24 were not reached. No SAT. No proof rejection.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:42:17 UTC on 2026-10-21, END 10:27:17 UTC (start + 6 h − 15 min).
One lane (`lane0.sh`, `--jobs 3`, slice min(2.0 h, time left)), `close_tree.py ... --caps 300,300,600 --cadopts=--sat --split-singles`.

- C3-S tools: worktree of commit 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (`make cake_lpr`, example prints `s VERIFIED UNSAT`);
  lrat-check 2e3b2dc with the E2 patch. Sanity check: on {1},{-1}, `3 0 0` is rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches). Details in `tools.txt`.
- Roots: rows of `lists/C_s1two.tsv` with row ≡ 2 (mod 18): 33 roots (`roots.tsv`).
- **Seeded records: 1,559** (certified/split records of the 3 partial roots: `0s0-1s1_2s1-5s0` 513 from C3WAVE2/K00,
  `0s0-2s1_3s1-6s0` 507 from C3WAVE2/K33, `0s0-1s1_6s0-10s1` 539 from C3WAVE2/K26). They are not in `out.jsonl`,
  which holds only the 2,022 new records (1,986 certified, 4 UNKNOWN at the cap, 32 split records).

## Per root (depth = number of layers; roots are at depth 2)

Timeouts are UNKNOWN results at the cap; splits include pre-splits of single-orbit layers. Solve and check seconds are summed per node (3 jobs on 4 cores).

| row | root | stratum | h6m_kept | list status | status | certified by depth | timeouts | splits | solve s | check s |
|-----|------|---------|----------|-------------|--------|--------------------|----------|--------|---------|---------|
| 2 | 0s0-1s1_2s1-5s0 | H6(1,1)/two | yes | partial | **closed** | d3: 41 | – | – | 1411 | 1198 |
| 20 | 0s0-2s1_3s1-6s0 | H6(2,1)/two | yes | partial | **closed** | d3: 47 | – | – | 1506 | 1319 |
| 38 | 0s0-2s1_3s0-6s1 | H6(2,1)/two | yes | untouched | **closed** | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 5490 | 9031 |
| 56 | 0s0-2s1_4s0-8s0 | H6(2,1)/two | yes | untouched | **closed** | d2: 1 | – | – | 150 | 35 |
| 74 | 0s0-2s1_5s1-7s0 | H6(2,1)/two | yes | untouched | **closed** | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 5926 | 9399 |
| 92 | 0s0-3s1_1s1-10s0 | H6(3,1)/two | yes | untouched | **closed** | d2: 1 | – | – | 36 | 29 |
| 110 | 0s0-3s1_4s0-5s1 | H6(3,1)/two | yes | untouched | **closed** | d3: 84, d4: 462 | d2: 1 | d2: 1, d3: 7 | 6246 | 9691 |
| 128 | 0s0-3s1_4s1-9s0 | H6(3,1)/two | yes | untouched | **closed** | d2: 1 | – | – | 218 | 35 |
| 146 | 0s0-3s1_6s0-7s1 | H6(3,1)/two | yes | untouched | partial | d4: 257 | d2: 1 | d2: 1, d3: 7 | 1730 | 3910 |
| 164 | 0s0-4s1_1s0-8s1 | H6(4,1)/two | yes | untouched | not reached | – | – | – | 0 | 0 |
| 182 | 0s0-4s1_2s0-10s0 | H6(4,1)/two | yes | untouched | not reached | – | – | – | 0 | 0 |
| 200 | 0s0-4s1_5s0-8s0 | H6(4,1)/two | yes | untouched | not reached | – | – | – | 0 | 0 |
| 218 | 0s0-4s1_6s1-7s1 | H6(4,1)/two | yes | untouched | not reached | – | – | – | 0 | 0 |
| 236 | 0s0-5s1_1s0-7s1 | H6(5,1)/two | yes | untouched | not reached | – | – | – | 0 | 0 |
| 254 | 0s0-5s1_1s1-9s0 | H6(5,1)/two | yes | untouched | not reached | – | – | – | 0 | 0 |
| 272 | 0s0-5s1_2s1-6s1 | H6(5,1)/two | yes | untouched | not reached | – | – | – | 0 | 0 |
| 290 | 0s0-5s1_6s1-8s0 | H6(5,1)/two | yes | untouched | not reached | – | – | – | 0 | 0 |
| 308 | 0s0-1s1_6s0-10s1 | H6(1,1)/two | no | partial | not reached | – | – | – | 0 | 0 |
| 326 | 0s0-1s1_8s0-10s1 | H6(1,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 344 | 0s0-2s1_5s0-10s1 | H6(2,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 362 | 0s0-2s1_7s0-10s0 | H6(2,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 380 | 0s0-2s1_8s1-9s0 | H6(2,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 398 | 0s0-3s1_2s0-8s1 | H6(3,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 416 | 0s0-3s1_5s1-10s0 | H6(3,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 434 | 0s0-3s1_7s1-10s0 | H6(3,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 452 | 0s0-4s1_1s1-3s1 | H6(4,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 470 | 0s0-4s1_3s0-10s1 | H6(4,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 488 | 0s0-4s1_3s1-7s1 | H6(4,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 506 | 0s0-4s1_7s1-9s0 | H6(4,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 524 | 0s0-5s1_2s1-4s0 | H6(5,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 542 | 0s0-5s1_3s1-6s0 | H6(5,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 560 | 0s0-5s1_4s1-10s0 | H6(5,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |
| 578 | 0s0-5s1_8s0-9s0 | H6(5,1)/two | no | untouched | not reached | – | – | – | 0 | 0 |

The two partial roots resumed from wave 2 (`0s0-1s1_2s1-5s0`, `0s0-2s1_3s1-6s0`) were closed with 41 and 47 new depth-3 certifications.
The third partial root of my shard, `0s0-1s1_6s0-10s1` (row 308), was not reached; its 539 seeded records are unchanged and not repeated here.
`0s0-3s1_6s0-7s1` got a 0.58 h slice (time left) and was stopped at END with 257 depth-4 nodes certified; it can be resumed from `out.jsonl`.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified | solve s | check s |
|---------|-------|--------|---------|-------------|-----------|---------|---------|
| H6(1,1)/two | 3 | 1 | 0 | 2 | 41 | 1411 | 1198 |
| H6(2,1)/two | 7 | 4 | 0 | 3 | 1140 | 13072 | 19784 |
| H6(3,1)/two | 7 | 3 | 1 | 3 | 805 | 8230 | 13665 |
| H6(4,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 |
| **total** | 33 | 8 | 1 | 24 | 1986 | 22713 | 34647 |

All 1,986 certified nodes have `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr).

Closed: `0s0-1s1_2s1-5s0`, `0s0-2s1_3s1-6s0`, `0s0-2s1_3s0-6s1`, `0s0-2s1_4s0-8s0`, `0s0-2s1_5s1-7s0`, `0s0-3s1_1s1-10s0`, `0s0-3s1_4s0-5s1`, `0s0-3s1_4s1-9s0`.
Partial: `0s0-3s1_6s0-7s1`.

## compose.py

`compose.txt`: `certified_nodes: 1986, class_covered: false` (expected: one shard, and only the new records).

## SAT / proof rejections / memory

- **SAT: none.**
- **PROOF NOT ACCEPTED: none.** The lane was stopped at END while cake_lpr was running on a few depth-5 nodes of
  `0s0-3s1_6s0-7s1`; the driver was killed with them, so no record was written for them (no `cake_lpr: none` record in `out.jsonl`, nothing to re-check).
- Memory: no problem; up to about 9 GB used with 3 jobs.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (new records only), `driver0.log` (last 100 lines), `compose.txt`, `README.md`.

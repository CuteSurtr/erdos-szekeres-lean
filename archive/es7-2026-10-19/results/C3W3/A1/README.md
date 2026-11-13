# C3W3 / A1: wave 3 of the 3-fold class (m = 11, k = 7), list A_s0.tsv, shard 1 of 8

**Result: 8 of my 37 roots closed, 3 partial, 26 not reached. No SAT. No proof rejection. No memory problem.**

Values: V = A1, LIST = A_s0.tsv, j = 1, N = 8, LANES = 3, JOBS = 1, SLICE = 0.5 h, H = 2.0 h, Z = 640a56c2.
One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:40:01 UTC, END = 06:25:01 UTC (start + 2 h − 15 min).

## Tools and base CNF (`tools.txt`)

- C3-S tools: worktree of commit 132398c at /opt/c3s, unmodified.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`); its example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`.
  Sanity check passed: on {1},{-1}, LRAT `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).

## Run

Roots: rows of `lists/A_s0.tsv` with row ≡ 1 (mod 8), 37 roots (`roots.tsv`). Lane k (k = 0, 1, 2) took the
roots at positions ≡ k (mod 3) (`lane0.sh`, `lane1.sh`, `lane2.sh`), each running
`close_tree.py /opt/work/base.cnf /opt/work/out{k}.jsonl R --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`,
S = min(0.5, hours left before END).

`close_tree.py` checks its deadline only between batches (a whole tree level is one batch), so the
three roots that were split ran past their 0.5 h slice: they started at 04:42, 04:50 and 04:55 and
were still in their depth-4 batch at END. At END I killed all lanes, drivers and checkers. A killed
node writes no record, so no `cake_lpr: none` record exists and there was nothing to re-check.

**Seeded records: 96**, all in lane 0 for the partial root `0s0-4s0_1s0-9s0`, from `C3S0/S0/out.jsonl`
(1 root split, 7 depth-3 splits, 88 certified depth-4 nodes). They are not in `out.jsonl`, which holds
only the 822 new records (lane 0, then lane 1, then lane 2).

## Per root (depth = number of layers; roots are depth 2)

Certified nodes and timeouts are new records only. Solve and check times are summed per node (s).

| row | root | stratum | list status | status | certified by depth | timeouts | splits | solve s | check s |
|-----|------|---------|-------------|--------|--------------------|----------|--------|---------|---------|
| 1 | 0s0-4s0_1s0-9s0 | H6(4,0)/two | partial | **partial** | d3: 84, d4: 190 | 0 | 0 | 1734 | 4374 |
| 9 | 0s0-2s0_1s0-4s1 | H6(2,0)/two | untouched | **closed** | d2: 1 | 0 | 0 | 229 | 46 |
| 17 | 0s0-2s0_3s0-5s0 | H6(2,0)/two | untouched | **closed** | d2: 1 | 0 | 0 | 7 | 26 |
| 25 | 0s0-2s0_3s1-5s0 | H6(2,0)/two | untouched | not reached | – | – | – | – | – |
| 33 | 0s0-2s0_4s1-5s1 | H6(2,0)/two | untouched | **closed** | d2: 1 | 0 | 0 | 9 | 17 |
| 41 | 0s0-2s0_5s1-6s0 | H6(2,0)/two | untouched | **closed** | d2: 1 | 0 | 0 | 108 | 42 |
| 49 | 0s0-4s0_2s0-5s1 | H6(4,0)/two | untouched | not reached | – | – | – | – | – |
| 57 | 0s0-4s0_5s1-6s0 | H6(4,0)/two | untouched | **closed** | d2: 1 | 0 | 0 | 181 | 42 |
| 65 | 0s0-4s0_7s1-8s0 | H6(4,0)/two | untouched | **closed** | d2: 1 | 0 | 0 | 271 | 45 |
| 73 | 0s0-5s0_1s0-8s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 81 | 0s0-5s0_1s1-6s0 | H6(5,0)/two | untouched | **closed** | d2: 1 | 0 | 0 | 109 | 46 |
| 89 | 0s0-5s0_2s0-10s0 | H6(5,0)/two | untouched | **partial** | d4: 278 | d2: 1 | 8 | 1513 | 4087 |
| 97 | 0s0-5s0_2s0-8s0 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 105 | 0s0-5s0_2s1-7s1 | H6(5,0)/two | untouched | **closed** | d2: 1 | 0 | 0 | 82 | 26 |
| 113 | 0s0-5s0_6s0-7s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 121 | 0s0-5s0_6s1-8s0 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 129 | 0s0-5s0_7s1-8s0 | H6(5,0)/two | untouched | **partial** | d4: 244 | d2: 1 | 8 | 1627 | 3690 |
| 137 | 0s0-4s0_1 | H6(4,0)/one | untouched | not reached | – | – | – | – | – |
| 145 | 0s0-5s0_7 | H6(5,0)/one | untouched | not reached | – | – | – | – | – |
| 153 | 0s0-2s0_1s0-8s1 | H6(2,0)/two | untouched | not reached | – | – | – | – | – |
| 161 | 0s0-2s0_5s0-10s0 | H6(2,0)/two | untouched | not reached | – | – | – | – | – |
| 169 | 0s0-2s0_6s1-10s0 | H6(2,0)/two | untouched | not reached | – | – | – | – | – |
| 177 | 0s0-2s0_8s0-10s0 | H6(2,0)/two | untouched | not reached | – | – | – | – | – |
| 185 | 0s0-4s0_2s0-10s0 | H6(4,0)/two | untouched | not reached | – | – | – | – | – |
| 193 | 0s0-4s0_3s1-5s1 | H6(4,0)/two | untouched | not reached | – | – | – | – | – |
| 201 | 0s0-4s0_7s1-8s1 | H6(4,0)/two | untouched | not reached | – | – | – | – | – |
| 209 | 0s0-4s0_8s1-10s1 | H6(4,0)/two | untouched | not reached | – | – | – | – | – |
| 217 | 0s0-5s0_2s0-4s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 225 | 0s0-5s0_3s0-7s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 233 | 0s0-5s0_3s1-4s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 241 | 0s0-5s0_3s1-9s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 249 | 0s0-5s0_4s0-8s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 257 | 0s0-5s0_4s1-7s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 265 | 0s0-5s0_7s1-10s0 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 273 | 0s0-5s0_8s1-10s1 | H6(5,0)/two | untouched | not reached | – | – | – | – | – |
| 281 | 0s0-3s0_10 | H6(3,0)/one | untouched | not reached | – | – | – | – | – |
| 289 | 0s0-5s0_10 | H6(5,0)/one | untouched | not reached | – | – | – | – | – |

Notes on the partial roots:
- `0s0-4s0_1s0-9s0` (row 1): resumed from the 96 seeded records; 84 more depth-3 children and 190
  more depth-4 nodes certified; no timeouts so far; open at END in its depth-4 batch.
- `0s0-5s0_2s0-10s0` (row 89) and `0s0-5s0_7s1-8s0` (row 129): the root timed out at 300 s and was split
  (1 split + 7 one-orbit depth-3 pre-splits each); 278 and 244 depth-4 nodes certified, all under 600 s
  with no timeout; open at END in their depth-4 batch.

Closed roots (every leaf certified, here the root itself at depth 2): `0s0-2s0_1s0-4s1`, `0s0-2s0_3s0-5s0`,
`0s0-2s0_4s1-5s1`, `0s0-2s0_5s1-6s0`, `0s0-4s0_5s1-6s0`, `0s0-4s0_7s1-8s0`, `0s0-5s0_1s1-6s0`, `0s0-5s0_2s1-7s1`.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified (new) | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------------|----------|---------|---------|
| H6(2,0)/two | 9 | 4 | 0 | 5 | 4 | 0 | 353 | 131 |
| H6(3,0)/one | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(4,0)/one | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| H6(4,0)/two | 8 | 2 | 1 | 5 | 276 | 0 | 2185 | 4461 |
| H6(5,0)/one | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| H6(5,0)/two | 16 | 2 | 2 | 12 | 524 | 2 | 3330 | 7849 |

All: 822 new records: 804 certified (each with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`),
16 split records, 2 UNKNOWN (300 s timeouts), 0 SATISFIABLE.

## compose.py

`compose.py /opt/work/base.cnf out.jsonl` (`compose.txt`, new records only): `certified_nodes: 804`,
`class_covered: false`, `uncovered_frontier_nodes: 908` (expected: this is one shard of one list, and the
seeded records are not in this file).

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem. With 3 lanes × 1 job, use peaked at about 8 GB of 15 GB.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`–`lane2.sh`, `out.jsonl` (new records), `driver0.log`–`driver2.log`
(last 100 lines of each), `compose.txt`.

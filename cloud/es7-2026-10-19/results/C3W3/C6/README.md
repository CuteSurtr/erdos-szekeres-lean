# C3W3 C6: wave 3, list C_s1two.tsv, shard 6 of 18

Values: V = C6, LIST = C_s1two.tsv, j = 6, N = 18, LANES = 1, JOBS = 3, SLICE = 2.0 h, H = 6.0 h, Z = 640a56c2.
One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Started 04:42:37 UTC on 2026-10-21. END was 10:27:37.

## Tools and base CNF (`tools.txt`)

- C3-S tools: a worktree of 132398c at /opt/c3s, used unmodified (git status clean)
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa: the bundled example prints `s VERIFIED UNSAT`
- lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with `results/E2/tools/lrat-check-E2.patch`. The patch is in normal diff format, so I applied it with patch(1). Sanity check on the CNF {1},{-1}: both checkers reject `3 0 0` and both accept `3 0 1 2 0`.
- Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`. It matches.

## Run

Roots: rows of `C_s1two.tsv` with row ≡ 6 (mod 18), 33 roots (`roots.tsv`). One lane (`lane0.sh`) ran `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S` for each root, with S = min(2.0, hours left before END).

Seeding: 1,085 records went into the lane's out file before the run. They are the certified and split records under the 3 partial roots, taken from the wave 1 and wave 2 sources and C3S0:
- `0s0-1s1_3s1-6s0`: 486 records, from C3WAVE2/K04
- `0s0-2s1_5s1-6s0`: 175 records, from C3WAVE2/K39
- `0s0-1s1_6s1-8s0`: 424 records, from C3WAVE2/K32

`out.jsonl` holds only the 2,383 new records (lines 1086 and after of the lane file). It has 2,347 certified nodes and 4 timeouts. The rest are split records.

At END the lane was running root 7 (`0s0-3s1_4s0-7s1`), and close_tree.py does not stop a round that is already running. I killed the process group at 10:28:39, about 1 minute after END. A killed node writes no record, so no record has `cake_lpr: none` and nothing had to be re-checked.

## Per root (depth = number of layers; roots are at depth 2)

Solve and check times are summed per node, in seconds. They are not wall-clock time: 3 jobs share 4 cores.

| # | root | stratum | list status | status | new certified by depth | timeouts | splits (new) | solve s | check s |
|---|------|---------|-------------|--------|------------------------|----------|--------------|---------|---------|
| 1 | 0s0-1s1_3s1-6s0 | H6(1,1) | partial | **closed** | d4: 68 | 0 | 0 | 431 | 994 |
| 2 | 0s0-2s1_5s1-6s0 | H6(2,1) | partial | **closed** | d3: 13, d4: 366 | 0 | 0 | 2756 | 5284 |
| 3 | 0s0-2s1_3s0-9s0 | H6(2,1) | untouched | **closed** | d3: 84, d4: 462 | 1 | d2: 1, d3: 7 | 4866 | 7633 |
| 4 | 0s0-2s1_4s1-5s0 | H6(2,1) | untouched | **closed** | d3: 84, d4: 462 | 1 | d2: 1, d3: 7 | 6955 | 8713 |
| 5 | 0s0-2s1_6s0-7s1 | H6(2,1) | untouched | **closed** | d3: 84, d4: 462 | 1 | d2: 1, d3: 7 | 6715 | 8665 |
| 6 | 0s0-3s1_1s1-4s1 | H6(3,1) | untouched | **closed** | d2: 1 | 0 | 0 | 57 | 22 |
| 7 | 0s0-3s1_4s0-7s1 | H6(3,1) | untouched | partial (stopped at END) | d4: 261 | 1 | d2: 1, d3: 7 | 1662 | 3583 |
| 8–33 | rest of `roots.tsv` (including the partial root 0s0-1s1_6s1-8s0) | | | not reached | – | – | – | – | – |

A root counts as closed when `close_tree.py` reported `"open_frontier": 0` for it. For roots 1 and 2 that depends on the seeded records, so the new-only `compose.txt` shows them as covered only partly. Each timeout is the depth-2 root itself hitting the 300 s cap before it was split.

Closed (6): 0s0-1s1_3s1-6s0, 0s0-2s1_5s1-6s0, 0s0-2s1_3s0-9s0, 0s0-2s1_4s1-5s0, 0s0-2s1_6s0-7s1, 0s0-3s1_1s1-4s1.
Partial (1): 0s0-3s1_4s0-7s1.

## Totals per stratum

| stratum | roots | closed | partial | not reached | new certified | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|---------------|----------|---------|---------|
| H6(1,1)/two | 2 | 1 | 0 | 1 | 68 | 0 | 431 | 994 |
| H6(2,1)/two | 8 | 4 | 0 | 4 | 2017 | 3 | 21292 | 30295 |
| H6(3,1)/two | 7 | 1 | 1 | 5 | 262 | 1 | 1719 | 3605 |
| H6(4,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| H6(5,1)/two | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| total | 33 | 6 | 1 | 26 | 2347 | 4 | 23442 | 34894 |

## SAT, rejections, memory

- No SAT answer.
- No `PROOF NOT ACCEPTED`. Every certified record has `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`.
- No memory problem. At most about 9 GB of the 15 GB was in use.

Files: `out.jsonl` (new records only), `driver0.log` (last 100 lines of the driver log), `compose.txt`, `roots.tsv`, `lane0.sh`, `tools.txt`, `env.txt`.

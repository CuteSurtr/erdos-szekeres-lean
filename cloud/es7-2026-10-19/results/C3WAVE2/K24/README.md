# C3WAVE2 / K24: shard 24 of 40, 3-fold class (m = 11, k = 7)

**7 of my 34 roots are closed. Root 8 (`0s0-2s1_7`) is partial. Roots 9–34 were not reached. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Started 00:27:49 UTC on 2026-10-21, END = 01:42:49 (start + 1.5 h − 15 min). Task file: `C3WAVE2/TASK.md` at 852bee7.
- C3-S tools: worktree of `132398c` (8dc27c3 before the author rewrite) at `/opt/c3s`, used unmodified. Live files are in `/opt/work`.
- CaDiCaL 3.0.1 `c60730422e758ef1cebe7aeddf2dda31c996bf04`. cake_lpr `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` (`make cake_lpr`), whose example prints `s VERIFIED UNSAT`. drat-trim lrat-check `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` with `E2/tools/lrat-check-E2.patch` applied.
- Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers (lrat-check `c NOT VERIFIED`, cake_lpr `Checking failed`). `3 0 1 2 0` is accepted by both. Details are in `tools.txt`.
- Base CNF: `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da` (matches).
- Roots: `roots.tsv` rows with idx ≡ 24 (mod 40), 34 roots. Runner: `runner.sh`, a 10-minute slice per root, `--jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles`.

## Per root (roots are at depth 2)

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_5s1-8s1 | **closed** | d2: 1 | 0 | 34 | 33 |
| 2 | 0s0-2s0_1s0-7s1 | **closed** | d2: 1 | 0 | 81 | 37 |
| 3 | 0s0-2s0_3s1-9s0 | **closed** | d2: 1 | 0 | 12 | 25 |
| 4 | 0s0-2s0_6 | **closed** | d3: 120 | d2: 1 (pre-split into 120) | 3500 | 2418 |
| 5 | 0s0-2s1_1s0-3s0 | **closed** | d2: 1 | 0 | 27 | 24 |
| 6 | 0s0-2s1_3s0-8s1 | **closed** | d2: 1 | 0 | 238 | 40 |
| 7 | 0s0-2s1_4s1-9s0 | **closed** | d2: 1 | 0 | 218 | 35 |
| 8 | 0s0-2s1_7 | partial | d3: 16 | d2: 1 (pre-split into 120); d3: 8 (timeout at 300 s, each split into 91) | 4218 | 503 |
| 9–34 | 0s0-3s0_1s0-7s1 … 0s0_4s1-7s0 (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock, because 3 jobs share 4 cores.

Root 4 was pre-split into 120 depth-3 children, and all 120 were certified at the 300 s cap. Its layer took 00:33 to 01:03. The driver checks the slice deadline only between batches, so this root ran well past its 10-minute slice.

Root 8 (`0s0-2s1_7`, one-orbit layer {7}) was pre-split into 120 depth-3 children. At the stop, 24 of them had finished: 16 were certified, and 8 one-orbit nodes (`_1 _3 _4 _5 _6 _8 _9 _10`) timed out at 300 s. Each of those 8 was split into 91 depth-4 children. The slice deadline (01:27) and END (01:42:49) passed while this depth-3 batch was still running. I stopped the runner by hand at about 01:46 to leave time for the write-up. That discarded the rest of the batch, as noted in `driver.log`. Open nodes: 96 at depth 3 and 728 at depth 4 (none attempted). They can be resumed from `out.jsonl`.

## Totals

- 142 certified nodes (d2: 6, d3: 136). Every one has `c VERIFIED` (lrat-check with the E2 patch) and `s VERIFIED UNSAT` (cake_lpr).
- Splits: 2 pre-split roots, plus 8 timeout splits at depth 3.
- Solve time 8,328 s and check time 3,115 s, both summed per node.
- `compose.txt`: `certified_nodes: 142, class_covered: false` (expected, since this is 1/40 of the shards). compose recomputed the CNF sha256 of all 142 certified nodes.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem. Peak `used` seen was about 6 GB of 15 GB.

Closed: 0s0-1s1_5s1-8s1, 0s0-2s0_1s0-7s1, 0s0-2s0_3s1-9s0, 0s0-2s0_6, 0s0-2s1_1s0-3s0, 0s0-2s1_3s0-8s1, 0s0-2s1_4s1-9s0.
Partial: 0s0-2s1_7.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `summary.txt`, `compose.txt`.

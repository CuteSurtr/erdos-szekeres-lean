# C3WAVE2 / K29: shard 29 of 40 (3-fold class, m = 11, k = 7)

**Result: 5 of my 33 roots are closed. Root 6 (`0s0-2s1_3s1-4s0`) is partial. Roots 7–33 were not reached. No SAT, no proof rejection, no memory problem.**

## Setup (see `tools.txt`, `env.txt`)

One cloud VM: 4 cores, 15 GB RAM, no swap. Start 00:29:34 UTC on 2026-10-21, END (start + 1.5 h − 15 min) 01:44:34.
- C3-S tools: a worktree of `132398c` (8dc27c3 before the rewrite) at /opt/c3s, unmodified.
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (`make cake_lpr`; its example prints `s VERIFIED UNSAT`), and drat-trim lrat-check 2e3b2dc with the E2 patch.
- Sanity check: on {1},{-1}, the LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches).
- Roots: the rows of `C3WAVE2/roots.tsv` with idx ≡ 29 (mod 40), 33 roots (`roots.tsv`).
- Runner (`runner.sh`): `close_tree.py … R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours min(0.17, left)`.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_6s0-9s0 | **closed** | d2: 1 | 0 | 34 | 34 |
| 2 | 0s0-2s0_1s1-10s1 | **closed** | d2: 1 | 0 | 92 | 39 |
| 3 | 0s0-2s0_4s0-5s1 | **closed** | d2: 1 | 0 | 74 | 36 |
| 4 | 0s0-2s0_6s0-8s1 | **closed** | d2: 1 | 0 | 67 | 36 |
| 5 | 0s0-2s1_1s0-6s0 | **closed** | d2: 1 | 0 | 112 | 39 |
| 6 | 0s0-2s1_3s1-4s0 | partial | d3: 55, d4: 462 | d2: 1 (UNKNOWN at 300 s → 91 children); d3: 7 one-orbit pre-splits (66 children each) | 4317 | 7475 |
| 7–33 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node. They are not wall-clock: 3 jobs share 4 cores.

Root 6: the depth-2 node timed out at 300 s and was split into 91 children. 7 of them are one-orbit layers (`_1`, `_5`–`_10`) and were pre-split, so the next batch had 84 + 7×66 = 546 nodes. `close_tree.py` checks its `--hours` deadline only between batches, so this one batch ran far past the 10-minute slice (00:41 to 01:51). All 462 depth-4 nodes were certified. Of the 84 two-orbit depth-3 children, 55 were certified and 29 were never attempted. I killed the driver at 01:51 because the wall budget had run out. Every record of root 6 is in `out.jsonl`, so a later wave can resume it with the same command; only the 29 depth-3 children remain open.

## Totals

522 certified nodes: 5 at depth 2, 55 at depth 3 and 462 at depth 4. Each one has lrat-check `c VERIFIED` (E2 patch) and cake_lpr `s VERIFIED UNSAT`. One UNKNOWN record (the root-6 node at 300 s); every other attempted node is certified.

`compose.txt`: `certified_nodes 522, class_covered false` (expected, since this is 1/40 of the shards). compose recomputed the CNF sha256 of all 522 certified nodes.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: peak use about 7 GB of 15 GB. No problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `summary.txt`, `compose.txt`.

# C3WAVE2 / K10: shard 10 of 40, wave 2, 3-fold class (m = 11, k = 7)

**Result: no roots closed. Root 1 (`0s0-1s1_4s1-10s1`) is partial, with 522 nodes certified and 24 depth-3 nodes still open. Roots 2–34 were not reached. No SAT, no proof rejection, no memory problem.**

## Setup (`env.txt`, `tools.txt`)

One cloud VM: 4 cores, 15 GB RAM, no swap. Start 00:23:09 UTC on 2026-10-21, H = 1.5 h, END = 01:38:09.
- Tools: worktree `/opt/c3s` at 132398c (formerly 8dc27c3), used unmodified.
- CaDiCaL 3.0.1 (c6073042).
- cake_lpr a36874a8 (`make cake_lpr`). Its example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc with `lrat-check-E2.patch`. The patch is in normal diff format, so it was applied with `patch`, not `git apply`.
- Sanity check on {1},{-1}: `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF from `gen_case.py 11 7 none` (with the `-o` flag that the script requires): `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`. Both match.
- Roots: rows of `C3WAVE2/roots.tsv` with idx ≡ 10 (mod 40), 34 roots (`roots.tsv`).
- Runner: `runner.sh`, i.e. `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S` with S = min(0.17, hours left).

## The 10-minute slice did not hold

`close_tree.py` checks `--hours` only between batches (`while frontier and time.time() < deadline`). It never checks inside a batch. Root 1 ran as follows:
- Batch 1 was the root alone. It hit UNKNOWN at the 300 s cap.
- The root was split into 91 depth-3 children. The 7 single-orbit ones (`_2`, `_3`, `_5`…`_9`) were pre-split into 66 children each.
- That made batch 2 a single batch of 84 + 462 = 546 nodes, which ran from about 00:31 until END.

At 01:38 I stopped the runner and the driver by hand, as wave 1 did. Nodes that were still in flight have no record. All written records are in `out.jsonl`, so the root can be resumed. Later waves with a per-root slice will hit the same issue on every root that is split: a split root's whole child batch runs regardless of `--hours`.

## Per root

| # | root | status | certified by depth | splits | solve s | check s |
|---|------|--------|--------------------|--------|---------|---------|
| 1 | 0s0-1s1_4s1-10s1 | partial | d3: 60, d4: 462 | d2: 1 (UNKNOWN at 300 s); d3: 7 (pre-split, 66 each) | 4190 | 8012 |
| 2–34 | (`roots.tsv`) | not reached | – | – | – | – |

Solve and check times are summed per node, so they are not wall-clock: 3 jobs ran on 4 cores.

Root 1 in detail:
- All 7 pre-split single-orbit subtrees are closed: 462 of 462 depth-4 nodes are certified.
- Of the 84 remaining depth-3 nodes, 60 are certified. The other 24 have no record yet; they were not attempted or were in flight at the stop. None timed out.
- Open depth-3 nodes: 0s0-1s1_4s1-10s1_5s1-9s1, 0s0-1s1_4s1-10s1_6s0-7s1, 0s0-1s1_4s1-10s1_6s1-7s0, 0s0-1s1_4s1-10s1_6s1-7s1, 0s0-1s1_4s1-10s1_6s0-8s0, 0s0-1s1_4s1-10s1_6s0-8s1, 0s0-1s1_4s1-10s1_6s1-8s0, 0s0-1s1_4s1-10s1_6s1-8s1, 0s0-1s1_4s1-10s1_6s0-9s0, 0s0-1s1_4s1-10s1_6s0-9s1, 0s0-1s1_4s1-10s1_6s1-9s0, 0s0-1s1_4s1-10s1_6s1-9s1, 0s0-1s1_4s1-10s1_7s0-8s0, 0s0-1s1_4s1-10s1_7s0-8s1, 0s0-1s1_4s1-10s1_7s1-8s0, 0s0-1s1_4s1-10s1_7s1-8s1, 0s0-1s1_4s1-10s1_7s0-9s0, 0s0-1s1_4s1-10s1_7s0-9s1, 0s0-1s1_4s1-10s1_7s1-9s0, 0s0-1s1_4s1-10s1_7s1-9s1, 0s0-1s1_4s1-10s1_8s0-9s0, 0s0-1s1_4s1-10s1_8s0-9s1, 0s0-1s1_4s1-10s1_8s1-9s0, 0s0-1s1_4s1-10s1_8s1-9s1.

## Totals

- 522 certified nodes. Every one has `c VERIFIED` (lrat-check, E2 patch) and `s VERIFIED UNSAT` (cake_lpr).
- 1 UNKNOWN (the root, at 300 s).
- 8 split records.

`compose.txt`: `certified_nodes 522, class_covered false`, which is expected. compose recomputed the CNF sha256 of every certified node.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: at most about 7 GB used of 15 GB. No problems.

## Lists

- Closed roots: none.
- Partial roots: 0s0-1s1_4s1-10s1.
- Not reached: the other 33 roots in `roots.tsv`.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records, resumable), `driver.log` (last 200 lines), `compose.txt`, `README.md`.

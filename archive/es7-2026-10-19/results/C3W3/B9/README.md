# C3W3 / B9: wave 3, list B_h3pilot.tsv, shard 9 of 10, 3-fold class (m = 11, k = 7)

**Result: no root closed. Root 1 (`0s0_1s1-3s0`) is partial with 262 certified depth-4 nodes. Roots 2 and 3 were not reached.
No SAT. No proof rejection. No memory problem.**

Values: V = B9, LIST = B_h3pilot.tsv, j = 9, N = 10, LANES = 1, JOBS = 3, SLICE = 0.9, H = 3.0, Z = 640a56c2.

## What ran where

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:14 UTC on 2026-10-21, END (start + 3 h − 15 min) 07:26:14 UTC.

- C3-S tools: worktree of commit 132398c at /opt/c3s, unmodified (`git status` clean). Live files in /opt/work.
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its example prints `s VERIFIED UNSAT`.
- drat-trim lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with `results/E2/tools/lrat-check-E2.patch` applied. Sanity check on the CNF {1},{-1}: the LRAT `3 0 0` is rejected by both checkers, and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`. Both match.
- The roots are the rows of `lists/B_h3pilot.tsv` with row ≡ 9 (mod 10): rows 9, 19 and 29 (`roots.tsv`). All three are `untouched`, stratum `H3/two`. **Seeded records: 0**, so `out.jsonl` holds only new records.
- One lane (`lane0.sh`), `close_tree.py ... --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, with S = 0.9.

## Per root (depth = number of layers; roots are at depth 2)

| # | root | stratum | status | certified by depth | splits | timeouts | solve s | check s |
|---|------|---------|--------|--------------------|--------|----------|---------|---------|
| 1 | 0s0_1s1-3s0 | H3/two | partial | d4: 262 | d2: 1 (timeout at 300 s, 120 children); d3: 8 (pre-split, 91 children each) | d2: 1 | 20058 | 8188 |
| 2 | 0s0_2s1-7s0 | H3/two | not reached | – | – | – | – | – |
| 3 | 0s0_4s1-6s1 | H3/two | not reached | – | – | – | – | – |

Solve and check times are summed over nodes. They are not wall-clock time, because 3 jobs shared 4 cores.

Root 1 timed out at 300 s and was split into 120 depth-3 children. The 8 one-orbit children (`_2`, `_4` to `_10`) were each pre-split into 91 depth-4 nodes. The resulting batch had 840 nodes: 728 at depth 4, run first, and 112 two-orbit nodes at depth 3. Of these, 262 depth-4 nodes were certified, all at the 600 s cap: 91 under `_2`, 91 under `_4` and 80 under `_5`. The slowest took 292 s. The other 578 nodes (466 at depth 4 and 112 at depth 3) were still open at END, and none of them timed out.

**Slice note:** `close_tree.py` checks `--hours` only between batches (its `while frontier and time.time() < deadline` loop), not during one. Root 1's first post-split batch has 840 nodes, so it ran past its 0.9 h slice until END. At END I killed the lane by hand. At that moment two depth-4 nodes were solving (`0s0_1s1-3s0_5_8s1-9s0`, `_5_8s1-9s1`) and one was in cake_lpr (`_5_8s0-9s1`). None of them had written a record, so there are no `cake_lpr: none` records and nothing to re-check. At the measured rate (about 1.6 certified nodes per minute), root 1's remaining 578 nodes would take about 6 more hours, plus any splits of depth-3 nodes that time out.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts | solve s | check s |
|---------|-------|--------|---------|-------------|-----------------|----------|---------|---------|
| H3/two | 3 | 0 | 1 | 2 | 262 | 1 | 20058 | 8188 |

Every certified node has lrat-check `c VERIFIED` (E2 patch) and cake_lpr `s VERIFIED UNSAT`.

## compose.py

Running `compose.py /opt/work/base.cnf results/C3W3/B9/out.jsonl` gives `certified_nodes: 262, class_covered: false` (`compose.txt`). This is expected, since this machine holds only a small part of the class. compose recomputed the CNF sha256 of all 262 certified nodes.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: no problem. About 2–3 GB was used with 3 jobs.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (263 solve records + 9 split records), `driver0.log` (last 100 lines), `compose.txt`.

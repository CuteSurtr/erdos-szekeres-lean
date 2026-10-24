# C3W3 / B1: wave 3, list B_h3pilot.tsv, shard 1 of 10, one lane

**Result: none of my 3 roots is closed. Root `0s0_1s0-10s0` is partial (350 depth-4 nodes certified), and the other two were not reached. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:23 UTC on 2026-10-21, H = 3.0, END = 07:26:23 UTC.
Values: V = B1, LIST = B_h3pilot.tsv, j = 1, N = 10, LANES = 1, JOBS = 3, SLICE = 0.9, Z = 640a56c2.

- C3-S tools: worktree of 132398c at /opt/c3s, used unmodified
- CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8 (the example prints `s VERIFIED UNSAT`), lrat-check 2e3b2dc with the E2 patch.
  Sanity check passed: on {1},{-1}, `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches)
- Roots: rows 1, 11 and 21 of the list (`roots.tsv`). All three are `untouched`, so **0 records were seeded** and `out.jsonl` holds only new records.
- One lane (`lane0.sh`), `close_tree.py … --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours S`, S = min(0.9, hours left).

## Per root (depth = number of layers; roots are at depth 2)

| row | root | stratum | status | certified by depth | timeouts | splits | solve s | check s |
|-----|------|---------|--------|--------------------|----------|--------|---------|---------|
| 1 | 0s0_1s0-10s0 | H3/two | **partial** | d4: 350 | d2: 1 (300 s) | d2: 1 (timeout); d3: 8 (pre-split, 91 children each) | 18319 | 10089 |
| 11 | 0s0_1s1-6s1 | H3/two | not reached | – | – | – | – | – |
| 21 | 0s0_3s0-6s0 | H3/two | not reached | – | – | – | – | – |

Solve and check times are summed over nodes. They are not wall-clock time, because 3 jobs shared the 4 cores.

Root `0s0_1s0-10s0` timed out at 300 s and was split into 8 one-orbit depth-3 children `_2` … `_9`. Each was pre-split into 91 depth-4 children, for 728 depth-4 nodes in total.
`_2`, `_3` and `_4` are fully certified (91/91 each), `_5` has 77/91, and `_6` to `_9` were not attempted.
All 350 attempted depth-4 nodes were UNSAT and certified at the 600 s cap, with no timeouts. 378 depth-4 nodes are still open.

`close_tree.py` checks its `--hours` deadline only between batches, and the 728-node batch was submitted all at once, so the 0.9 h slice ran past its end. At END (07:26:36) I killed the lane's process group by hand (`=== KILLED` line in `driver0.log`). The nodes in flight left no records, and no record has `cake_lpr: none`, so nothing needed a re-check. Rows 11 and 21 were never started.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes |
|---------|-------|--------|---------|-------------|-----------------|
| H3/two | 3 | 0 | 1 | 2 | 350 |

## compose.py

`compose.txt`: `certified_nodes: 350, class_covered: false` (as expected for one shard). It recomputed the CNF sha256 of every certified node.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. All 350 certified records have `c VERIFIED` and `s VERIFIED UNSAT`.
- Memory: peak use was about 9 GB of 15 GB, with no out-of-memory events. The largest proof was 373 MB (not committed).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `lane0.sh`, `out.jsonl` (all new records; it can be used to resume root 1), `driver0.log` (last 100 lines), `compose.txt`.

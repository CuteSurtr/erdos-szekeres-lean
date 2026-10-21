# C3W3 / B2: wave 3, list B_h3pilot.tsv, shard j = 2 of N = 10 (LANES 1, JOBS 3, SLICE 0.9 h, H 3.0 h)

**Result: no root closed. Root 1 (`0s0_1s0-10s1`) is partial: 565 nodes certified. Roots 2 and 3 were not reached.
No SAT. No proof rejections. No memory problems.**

## Tools and base CNF (`tools.txt`)

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 04:41:18 UTC, END 07:26:18 UTC (start + 3 h − 15 min), all on 2026-10-21.
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified
- CaDiCaL 3.0.1, c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa; its example gives `s VERIFIED UNSAT`
- lrat-check from drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, with the E2 patch. Sanity check: both checkers reject `3 0 0` on {1},{-1}, and both accept `3 0 1 2 0`
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6da` (matches)

## Roots (`roots.tsv`)

The rows with row ≡ 2 (mod 10): rows 2, 12 and 22. All three are `untouched`, in stratum H3/two. **Seeded records: 0.**

| # | root | stratum | status | certified by depth | splits | timeouts | solve s | check s |
|---|------|---------|--------|--------------------|--------|----------|---------|---------|
| 1 | 0s0_1s0-10s1 | H3/two | **partial** | d4: 565 | d2: 1 (timeout at 300 s); d3: 8 (pre-split, one-orbit) | 1 (the root itself, at 300 s) | 16,527 | 11,936 |
| 2 | 0s0_1s1-8s1 | H3/two | not reached | – | – | – | – | – |
| 3 | 0s0_3s0-8s1 | H3/two | not reached | – | – | – | – | – |

(Depth = number of layers; roots are at depth 2.) Solve and check times are summed over nodes. They are not wall-clock time, because 3 jobs shared 4 cores.

Root 1 timed out at 300 s and was split into 120 depth-3 children. The 8 one-orbit children were pre-split into 728 depth-4 nodes.
`close_tree.py` checks `--hours` only between layers, so the 0.9 h slice ran over: the whole first frontier (840 nodes) was submitted as one layer.
I stopped the run myself at END. By then 565 depth-4 nodes were certified (each at most 110 s, under the 600 s cap), with no timeouts.
Still open: 163 depth-4 nodes, plus 112 two-orbit depth-3 nodes that were never attempted. That makes 275 open nodes, recomputed from `out.jsonl`.
The nodes running at the kill wrote no records, so no `cake_lpr: none` record exists and no re-check was needed.

## Totals per stratum

| stratum | roots | closed | partial | not reached | certified nodes | timeouts |
|---------|-------|--------|---------|-------------|-----------------|----------|
| H3/two | 3 | 0 | 1 | 2 | 565 | 1 |

All 565 certified records have `lrat_check: c VERIFIED` and `cake_lpr: s VERIFIED UNSAT`.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: there were no problems. Peak usage was about 5 GB used out of 15 GB.

## Files

`out.jsonl` (575 new records, lane 0), `driver0.log` (last 100 lines), `lane0.sh`, `roots.tsv`, `tools.txt`, `env.txt`, `compose.txt`.

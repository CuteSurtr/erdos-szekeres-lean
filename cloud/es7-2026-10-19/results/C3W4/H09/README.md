# C3W4 / H09: wave 4, list W4_H3.tsv, shard 9 of 30

**Result: 1 of 4 roots is closed (`0s0_2s0-8s1`, 314 certified nodes). Root `0s0_2` is partial, with no
certified node. Roots `0s0_3s0-5s0` and `0s0_5s0-6s1` were not reached. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:14 UTC, END 16:16:14 UTC (start + 5 h − 15 min), runner killed at 16:18 UTC.
- Tools: worktree of commit 95cafa93 at /opt/c3u (`results/C3U/tools`), used unmodified. No `compose.py` was run.
- CaDiCaL 3.0.1 c60730422e75; cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); lrat-check 2e3b2dc with the E2 patch.
  Sanity check: LRAT `3 0 0` on {1},{-1} was rejected by both checkers, and `3 0 1 2 0` was accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `W4_H3.tsv` with row ≡ 9 (mod 30) (`roots.tsv`), with no seeded records.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.0 h (`runner.sh`).

## Per root

Depth means the layers in the node name (roots have 2). The σ level is the number of σ bits fixed (0, 3 or 6).

| row | root | stratum | status | certified (layers / σ bits) | timeouts | solve s | check s |
|-----|------|---------|--------|-----------------------------|----------|---------|---------|
| 9 | 0s0_2s0-8s1 | H3/two | **closed** (open frontier 0, no childless split) | 314: d2/σ6: 59, d3/σ6: 255 | 14: root and 8 σ3 nodes at cap 1 (by design), 5 σ6 cubes at 300 s (layer-split into 255 children, all certified) | 18,397 | 8,007 |
| 39 | 0s0_2 | H3/one | **partial** | 0 | 79: root and 8 σ3 nodes at cap 1, **all 64 σ6 cubes at 300 s**, 6 d3/σ6 nodes at 600 s | 22,918 | 0 |
| 69 | 0s0_3s0-5s0 | H3/two | not reached | – | – | – | – |
| 99 | 0s0_5s0-6s1 | H3/two | not reached | – | – | – | – |

Root `0s0_2` ran from 14:03 to the kill. All 64 of its 6-bit cubes timed out at 300 s and were layer-split.
In the cap-600 batch that followed, 6 children (`0s0_2_{1,3,4,5,6,7}__1s0-3s1-4s0-5s0-6s1-7s0`) timed out
and were layer-split again (60 children each). Every split record has `children` > 0. About 4,950 nodes are
still open (never attempted), and nodes still running at the kill have no record. The σ route on 6 bits did not
crack this one-orbit root at 300 s. Root 1 ran from 11:33 to 14:03 (its slice overran by about 30 min because close_tree finishes its current batch).

Totals for stratum H3/two: 1 closed, 2 not reached. H3/one: 1 partial. 314 certified records in total. All have
lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. None has cake_lpr `none`, so no re-check was needed (no `recheck.jsonl`).
Solve and check seconds are summed per node, with 3 jobs on 4 cores.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none.
- Memory: peak use was about 9 GB of 15 GB, with no failures.

Files: `env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (500 records, resumable), `driver.log.tail`, `summary.txt`.

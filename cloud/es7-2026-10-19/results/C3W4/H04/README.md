# C3W4 / H04: W4_H3.tsv shard 4 of 30, σ-cube splitting

**Result: 1 of my 4 roots is closed (`0s0_1s0-6s0`), 1 is partial (`0s0_1s1-7s1`), 2 not reached. No SAT. No proof rejection. No memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:18 UTC on 2026-10-24, END 16:16:18 (start + 5 h − 15 min).
Runner (`runner.sh`) started at 11:33:38; at END the remaining close_tree, cadical and cake_lpr processes were killed by hand (16:16:48), so their records were never written.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, TOOLS = `/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools`, unmodified. `compose.py` was not run, as the task requires.
- CaDiCaL 3.0.1 c60730422e75…; cake_lpr a36874a8b750… (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf9… with the E2 patch. Sanity check passed: on {1},{-1} the LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both (`tools.txt`).
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).
- Roots: rows of `W4_H3.tsv` with row ≡ 4 (mod 30): rows 4, 34, 64, 94 (`roots.tsv`). No records were seeded.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.0 h.

## Per root

Notation: the root is at layer depth 2. "σ6" means a cube on 6 σ bits (root → 8 cubes on 3 bits at cap 1 → 64 cubes on 6 bits at cap 300). "d3 σ6" means a layer-split child (depth 3) of a 6-bit cube, at cap 600.

| row | root | stratum | status | certified | timeouts | splits | solve s | check s |
|-----|------|---------|--------|-----------|----------|--------|---------|---------|
| 4 | 0s0_1s0-6s0 | H3/two | **closed** (open frontier 0, no childless node) | d2 σ6: 64 | cap 1: 9 (by design); cap 300: 0 | σ: 1 + 8 | 12,506 | 3,088 |
| 34 | 0s0_1s1-7s1 | H3/two | **partial** (stopped at END) | d2 σ6: 12; d3 σ6: 293 | cap 1: 9 (by design); cap 300: 52; cap 600: 0 | σ: 1 + 8; layer: 52 (2,652 children) | 26,043 | 8,317 |
| 64 | 0s0_2s1-8s1 | H3/two | not reached | – | – | – | – | – |
| 94 | 0s0_4s1-6s0 | H3/two | not reached | – | – | – | – | – |

- Root 4 ran 11:33:38–13:01:39 (1 h 28 min): all 64 6-bit cubes were certified at 138–291 s each.
- Root 34 started at 13:01:39. Only 12 of its 64 6-bit cubes were certified at 300 s. The other 52 timed out and were layer-split into 2,652 depth-3 children at cap 600. Of those, 293 were certified (mean 27 s, max 108 s, none timed out). That closes 5 of the 52 timed-out cubes completely; 38 certified children are spread over the other 47. Open frontier at END: 2,359 depth-3 nodes, never attempted. close_tree checks the slice deadline only between batches, so the 600 s batch ran until END. All of its split records have children > 0.
- Solve and check seconds are summed per node, with 3 jobs on 4 cores.

## Totals (stratum H3/two; the only stratum in my shard)

1 closed, 1 partial, 2 not reached. 369 certified nodes, all with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. 509 records in `out.jsonl`. Solve 38,549 s, check 11,405 s. Largest proof was 404 MB (deleted after checking). Peak memory use was about 9 of 15 GB.

## SAT / proof rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. No record has cake_lpr `none`. The checkers killed at END belong to nodes with no record, so there was nothing to re-check (no `recheck.jsonl`).
- Childless split records (`"children": 0`): none.
- Memory: no problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (all records), `driver.log.tail` (last 100 lines).

# C3W4 / H17: wave 4, list W4_H3.tsv, shard 17 of 30

**Result: 1 of my 3 roots is closed (`0s0_1s0-5s0`). The other 2 are partial. There was no SAT, no proof rejection and no memory problem.**

## Setup

- One cloud VM with 4 cores, 15 GB RAM and no swap (`env.txt`). Start 11:31:12 UTC on 2026-10-24, END 16:16:12 UTC (start + 5 h − 15 min).
- Tools (`tools.txt`):
  - C3U tools from a worktree of 95cafa93 at `/opt/c3u`, unmodified.
  - CaDiCaL c6073042 (3.0.1).
  - cake_lpr a36874a8. Its example prints `s VERIFIED UNSAT`.
  - lrat-check 2e3b2dc with the E2 patch. Sanity check passed: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
  - Base CNF from `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.
- Roots: rows of `W4_H3.tsv` with row ≡ 17 (mod 30). That gives 3 roots, all `H3/two` and untouched (`roots.tsv`). No records were seeded.
- One runner (`runner.sh`) with `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, slice 2.0 h per root.
- No `compose.py` was run.

## Per root

"Layers" counts the layers in the name. "Bits" is the number of σ bits: 6 means σ level 2.

| root | status | certified | timeouts | splits | open frontier | solve s | check s |
|------|--------|-----------|----------|--------|---------------|---------|---------|
| 0s0_1s0-5s0 | **closed** (frontier 0, no childless split) | 64 at (2 layers, 6 bits) | cap 1: root + 8 at 3 bits | 9 σ | 0 | 9011 | 2815 |
| 0s0_2s0-6s1 | partial | 1 at (2, 6); 54 at (3, 6) | cap 1: 9; cap 300: 63 of 64 6-bit cubes | 9 σ, 63 layer | 3159 at (3, 6) | 20620 | 1665 |
| 0s0_3s1-4s0 | partial | 1 at (2, 6) | cap 1: 9; cap 300: 50 6-bit cubes | 9 σ, 50 layer | 2563 = 2550 at (3, 6) + 13 unattempted 6-bit cubes | 15283 | 51 |

The solve and check seconds are summed per node, with 3 jobs sharing 4 cores.

- `0s0_1s0-5s0`: closed in 67 min. All 64 6-bit cubes were certified at cap 300: solve 88–218 s (median 135 s), check median 43 s.
- `0s0_2s0-6s1`: 63 of the 64 6-bit cubes timed out at 300 s. They got the layer split, which gives 3,214 depth-3 cube children. Of these, 54 were attempted at cap 600 and all 54 were certified (solve 5–83 s, median 18 s; check median 28 s). None of them timed out. The remaining 3,159 were not attempted.
- `0s0_3s1-4s0`: 50 of the 51 6-bit cubes that finished timed out at 300 s, and 1 was certified. 13 cubes were not finished: 3 were killed in flight at END and 10 were never started. No layer child was attempted.

## Totals (stratum H3/two)

- 400 records.
- 120 certified nodes, all with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
- 149 timeouts: 27 at cap 1 by design and 113 at cap 300. There were no timeouts at cap 600.
- 131 split records, none with `"children": 0`.
- 1 root closed and 2 partial, with an open frontier of 5,722 in total.

## SAT, rejections, memory

- **SAT: none.**
- **`PROOF NOT ACCEPTED`: none.** There was no record with cake_lpr `none`, so no recheck was needed and there is no `recheck.jsonl`.
- **Memory:** no problem. Peak use was about 6 GB of 15 GB. The largest proof was 367 MB (deleted).

## Incidents (time only, not results)

`close_tree.py` checks its `--hours` deadline only between rounds. A round of layer children can therefore run far past the slice: for `0s0_2s0-6s1` that would have been about 3,200 nodes.

- I stopped `0s0_2s0-6s1` by hand at 14:50:17 UTC. Its 2 h slice had ended at 14:41:44. The root then went to `0s0_3s1-4s0`.
- I stopped `0s0_3s1-4s0` at END (16:16:28).
- Each time, only the in-flight CaDiCaL runs were killed: 2 the first time and 3 at END. No checker was running and no record was written for them. Every record in `out.jsonl` is complete.
- The open frontiers above come from expanding the split records of `out.jsonl` with the tool's own child functions. They are not from a final `open_frontier` line, because those runs were stopped by hand. Both notes are in `driver.log.tail`.

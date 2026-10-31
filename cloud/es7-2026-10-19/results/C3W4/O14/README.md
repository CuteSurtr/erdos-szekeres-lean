# C3W4 / O14: W4_one.tsv shard 14 of 16, σ-cube splitting

**Result: no SAT, no proof rejection, no memory problem. Root 1 (`0s0-2s1_3`) is partial (open frontier 782, no childless
timed-out node); root 2 (`0s0-5s0_6`) was not reached.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:20 UTC 2026-10-24, END 16:16:20 UTC (start + 5 h − 15 min).
Task file commit 3fd8a4d8.

- Tools: worktree of commit 95cafa93 at `/opt/c3u`, `results/C3U/tools` used unmodified. **No `compose.py` was run.**
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1); cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
  (example prints `s VERIFIED UNSAT`); lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 with the E2 patch.
  Sanity check passed: on {1},{-1}, LRAT `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches). Details in `tools.txt`.
- Roots (`roots.tsv`): rows 14 and 30 of `W4_one.tsv`. No seeding.
- Runner (`runner.sh`): `close_tree.py base out R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours S`,
  S = min(2.5, hours left before END).

## Per root

| row | root | stratum | status | certified (depth, σ bits) | timeouts | splits | solve s | check s |
|-----|------|---------|--------|---------------------------|----------|--------|---------|---------|
| 14 | 0s0-2s1_3 | H6(2,1)/one | **partial**, open frontier 782 | d2 σ6: 35; d3 σ6: 769 (total 804) | cap 1: 1 root + 8 σ3 cubes; cap 300: 29 of 64 σ6 cubes; cap 600: 0 | σ: 1 + 8; layer: 29 (51 children each, 1,479) | 31,920 | 17,970 |
| 30 | 0s0-5s0_6 | H6(5,0)/one | not reached | – | – | – | – | – |

Details of root 14: the root and its 8 three-bit cubes timed out at cap 1 as intended and gave 64 six-bit cubes. 35 of them
were certified at cap 300 (about 200–300 s each) and 29 timed out and were layer-split into 51 depth-3 children each.
All 769 depth-3 children that ran were certified at cap 600, the slowest in 73 s. 15 of the 29 layer-split cubes are
fully closed; 14 are open (13 with none of their 51 children run yet and one with 4 of 51), so the open frontier is
13·51 + 47 = 782 depth-3 nodes. Every split record has children > 0.

Totals (stratum H6/one, this machine): 804 certified nodes (each with lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`),
38 timeouts (9 by design at cap 1, 29 at cap 300), 0 at cap 600. Solve and check seconds are summed per node, with 3 jobs on 4 cores.

## Stop at END

`close_tree.py` checks `--hours` only between frontier waves, and the depth-3 wave of 1,479 nodes was still running when
the 2.5 h slice ended (16:04). The runner's process group (runner, close_tree, CaDiCaL, checkers) was killed at END (16:16:20).
Nodes in flight were lost without a record (they are part of the open frontier); no record with cake_lpr `none` was
written, so there was nothing to re-check (no `recheck.jsonl`). Because of this, root 30 got no time.

## SAT / rejections / memory

- SAT: none.
- PROOF NOT ACCEPTED: none. Every UNSAT record is certified by both checkers.
- Memory: peak used about 9 GB of 15 GB; no problem.

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `runner.sh`, `out.jsonl` (880 records: 842 solve, 38 split), `driver.log.tail`.

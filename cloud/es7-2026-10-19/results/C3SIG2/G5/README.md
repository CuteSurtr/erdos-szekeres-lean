# C3SIG2 G5: σ-cube pilot, shard j = 1 (rows 1, 5, 9, 13 of `nodes.tsv`), H = 2.5 h, task at 4641a656

One cloud VM, 4 cores, 15 GB, no swap (`env.txt`); 05:40 to 08:10 UTC on 2026-10-21. Tools in `tools.txt`
(C3-S worktree 132398c unmodified, `sigma_cubes.py` copied unmodified, CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8,
lrat-check 2e3b2dc + E2 patch, sanity checks passed; base CNF `p cnf 168399 4154921`, sha256 bf0e502e… matches).
Runner `runner.sh`, refinement driver `refine6.py` (imports `sigma_cubes` unmodified, calls `run((base, node, bits6, vals6, 300))`,
3 jobs), records in `out.jsonl`, table from `summ.py`. Each node got an even share (~33 min): K = 3 (cap 300, 3 jobs), then
refinement of the open K = 3 cubes in cube order until the share deadline.

All four of my nodes are **H3/two**; this shard has no one-orbit H6(a,1) node (those are rows 0, 2, 4, …, on other shards).

No SAT. No proof rejection: all 79 UNSATs certified by both checkers (lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`). No memory problem.

## Table

| row | node | stratum | K=3 cert/open | K=3 solve+check s | level 2: cert / recorded / needed | level-2 solve+check s | largest cube s | K=3 cubes closed by refinement | node closed | total s | layer split: spent_core_s / open_nodes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0s0_5s1-6s0 | H3/two | 0/8 | 2401 | 10 / 10 / 64 | 2498 | 325 | 1/8 | no | 4899 | 10336.8 / 739 |
| 5 | 0s0_1s1-3s1 | H3/two | 0/8 | 2401 | 29 / 29 / 64 | 2989 | 300 | 3/8 | no | 5390 | - |
| 9 | 0s0_2s0-8s0 | H3/two | 0/8 | 2401 | 18 / 18 / 64 | 2993 | 300 | 2/8 | no | 5393 | - |
| 13 | 0s0_3s0-8s0 | H3/two | 0/8 | 2401 | 22 / 22 / 64 | 2969 | 300 | 2/8 | no | 5370 | - |

"largest cube" 300 = a K = 3 cube at the cap; the largest certified level-2 cube is 325 s (solve 265 + check 60), on row 1.
Level-2 cubes not recorded were either not reached or still running at the share kill (`sigma_cubes`' ordered `map`
records in order, so a finished cube behind an unfinished one is lost at the kill); they count as open/unknown.
Per-node mean cost of a certified level-2 cube: row 5 103 s, row 13 135 s, row 9 166 s, row 1 250 s (overall median 129 s),
so closing all 64 level-2 cubes would need about 6.6k, 8.6k, 10.6k and 16.0k core-s.

## Per stratum

- **H3 (4 nodes)**: 0/4 closed in the share; median cost per closed node: none closed. Open fraction at K = 3: 32/32 (100%), every
  cube at the 300 s cap. At level 2 (6 bits): 0/79 recorded cubes open (all certified, all under the cap, max solve 265 s),
  177/256 not reached. Fully closed K = 3 cubes by refinement: 8 of 32 (each with 8/8 certified extensions).
- **One-orbit H6(a,1)**: no node in this shard.

Row 1 (the partial root): σ-cubes spent 4.9k core-s here (2.4k of it on K = 3 timeouts) without closing; extrapolated total
≈ 2.4k + 16.0k ≈ 18.4k core-s, versus 10.3k already spent by the layer split with 739 nodes still open, so the comparison is
not decided by this run, but the level-2 cubes behave uniformly (no timeouts) whereas the layer split's frontier is still growing.

## Judgement

For H3 roots, K = 3 at cap 300 is pure waste (0 of 32 cubes certified, 2.4k core-s per node). Depth-2 σ-cubes (6 bits, 64 cubes)
look like the right first step: every one of the 79 level-2 cubes run was certified within the cap, at roughly 100–250 s
each, so each H3 node should close in about 7k–16k core-s with no further splitting. Recommendation for the next wave:
go straight to the 64 cubes on the 6 smallest free residues for H3 (skip K = 3), with a cap of 600 s for safety, and
budget ~3–6 core-h per node; record cubes as they finish (unordered) so a share kill loses nothing. This shard says nothing about
the one-orbit H6(a,1) stratum.

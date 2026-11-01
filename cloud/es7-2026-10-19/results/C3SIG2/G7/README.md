# C3SIG2 G7: σ-cubes on four H3 roots (shard j = 3)

Task: `results/C3SIG2/TASK.md` at 4641a656, V = G7, j = 3, H = 2.5 h. Start 05:44:45Z, runner END 07:59:45Z.
Tools and the base CNF check are in `tools.txt`: C3-S tools 132398c, CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch, sanity checks passed. Base CNF `p cnf 168399 4154921`, sha256 bf0e502e… (matches).
`sigma_cubes.py` was copied unmodified (cmp identical). `refine6.py` is the step-3 refinement driver (the same file as G5's); it imports `sigma_cubes` unmodified.
All records are in `out.jsonl` and the runner is `runner.sh`.

My nodes are rows 3, 7, 11 and 15 of `nodes.tsv`. All four are **H3/two and untouched**, so this shard has no one-orbit H6(a,1) node. There is also no `spent_core_s` / `open_nodes` to compare with: none of the four is a partial root.
Each node got an even share of about 33 min of wall time on 4 cores with 3 jobs: K = 3 (8 cubes, cap 300), then refinement of the open K = 3 cubes on the 6 smallest free residues (8 × open cubes, cap 300), in lexicographic order, killed at the share deadline. A cube that was still running at the deadline has no record and counts as open.

No SAT. No proof was rejected: every UNSAT was accepted by both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`).

## Table

| row | node | stratum | K=3 cert/open | K=6 tried/cert/open (of 8×open K=3) | solve s | check s | largest cube s | closed | prior spent_core_s / open_nodes |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 0s0_1s0-5s0 | H3/two | 0/8 | 22/22/0 of 64 (not run 42) | 4424 | 926 | 300 | no | - / - |
| 7 | 0s0_1s1-9s1 | H3/two | 0/8 | 9/8/1 of 64 (not run 55) | 4513 | 423 | 340 | no | - / - |
| 11 | 0s0_2s1-8s1 | H3/two | 0/8 | 10/9/1 of 64 (not run 54) | 4596 | 491 | 338 | no | - / - |
| 15 | 0s0_4s0-7s1 | H3/two | 0/8 | 9/9/0 of 64 (not run 55) | 4440 | 508 | 334 | no | - / - |

Times are core-seconds summed over that node's cubes, K = 3 and K = 6 together. "largest cube" means solve + check.

Which K = 3 cubes were fully refined (8 of 8 extensions certified):
- 0s0_1s0-5s0: 000 and 001 are both closed. 010 has 6 of 8 extensions certified.
- 0s0_4s0-7s1: 000 is closed.
- The other two nodes: 000 has 7 of 8 certified, and one extension (…,1,1,1) timed out at 300 s.

Certified K = 6 cubes, solve + check: median 205 s, mean 211 s, max 340 s over 48 cubes. Per node the medians were 132 s, 278 s, 243 s and 276 s.

## Per stratum

- **One-orbit H6(a,1)**: no nodes in this shard.
- **H3** (4 nodes):
  - Nodes closed: 0 of 4. The median cost per closed node is undefined.
  - K = 3: 32 of 32 cubes open (all timed out at 300 s), at 2,400 core-s per node.
  - K = 6: 2 open of the 50 that ran (4%). The other 206 of 256 did not run within the share.
  - Projected cost of a full depth-6 split, from the mean certified cube times and not counting the K = 3 pass: about 8.6k, 17.9k, 17.0k and 18.1k core-s. Adding the 2.4k K = 3 pass gives the `proj` figures of 11.0k, 20.3k, 19.4k and 20.5k core-s. These are lower bounds, because the open cubes need a further split.

## Judgement

For H3 roots, a K = 3 σ split at cap 300 is wasted work: 32 of 32 cubes timed out, costing 2,400 core-s per node with nothing gained.
The 6-bit σ cubes behave well: 96% certify within 300 s, mostly in 130–290 s. One node (0s0_1s0-5s0) had a 100% rate with a median of 132 s.
So σ-cubes at depth 2 should be the first step for H3 in the next wave, but at 6 bits directly (64 cubes, cap 300, with K = 9 refinement of the few open cubes), not at K = 3.
At about 9–18k core-s per root that is a substantial but bounded cost. I cannot compare it with the layer split here, because none of these roots has layer-split data. The comparison should come from the H3 partial root 0s0_5s1-6s0 (G5, 10,337 core-s spent, 739 nodes still open).
This shard says nothing about one-orbit roots.

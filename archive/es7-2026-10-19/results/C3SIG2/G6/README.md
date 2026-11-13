# C3SIG2 G6: σ-cube pilot, shard j = 2 (rows 2, 6, 10, 14 of `C3SIG2/nodes.tsv`)

Task `results/C3SIG2/TASK.md` at 4641a656, with V = G6, j = 2, H = 2.5. Machine: one cloud VM with 4 cores and 15 GB RAM, no swap (`env.txt`).
The run went from 05:44:17Z to 07:57:04Z on 2026-10-21. Tools are in `tools.txt`: C3-S tools from a worktree of 132398c, used
unmodified, plus sigma_cubes.py copied unmodified; CaDiCaL 3.0.1 c6073042; cake_lpr a36874a8; lrat-check 2e3b2dc with the E2
patch. The sanity check passed. The base CNF is `p cnf 168399 4154921`, sha256 bf0e502e…dd6da, which matches.

How it ran: `runner.sh` gave each node an even share of the time to 07:57Z, about 33 min. It ran `sigma_cubes.py BASE out.jsonl NODE 3 300 3`.
Then `refine.py` (my own driver, which imports `sigma_cubes` unmodified and calls `run((base, node, bits6, vals6, 300))`) ran the
8 extensions of each open K = 3 cube on the next 3 free residues, 3 jobs at a time, in cube order. It was killed at the share deadline. A cube that was not recorded by then counts as open/unrun.
All records are in `out.jsonl`, and the table is `summary.tsv` (`summarize.py out.jsonl nodes.tsv`).

**Checks:** there was no SAT and no proof rejection. Every UNSAT record (49) has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

## Table

| row | node | stratum | K=3 cert/open | depth-6 run / cert / open / unrun | K=3 cubes closed by refinement | solve s | check s | largest cube s (certified) | closed | layer split: spent_core_s / open_nodes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 0s0-2s1_1 | H6(2,1)/one | 0 / 8 | 11 / 11 / 0 / 53 | 1/8 | 4729.7 | 582.4 | 300.1 (295.7) | no | 16356.8 / 743 |
| 6 | 0s0-3s1_1 | H6(3,1)/one | 0 / 8 | 12 / 12 / 0 / 52 | 1/8 | 4963.1 | 567.8 | 300.2 (296.6) | no | untouched |
| 10 | 0s0-4s1_1 | H6(4,1)/one | 0 / 8 | 12 / 12 / 0 / 52 | 1/8 | 4818.6 | 577.8 | 300.1 (287.2) | no | untouched |
| 14 | 0s0-5s1_1 | H6(5,1)/one | 0 / 8 | 14 / 14 / 0 / 50 | 1/8 | 4695.3 | 621.7 | 300.1 (265.3) | no | untouched |

Depth-6 cubes use the 6 smallest free residues: (3,4,5,6,7,8) for row 2 and (2,r,…,8) skipping the layer residue for the others. In every
node, the first K = 3 cube (000) was refined into 8 cubes and all 8 were certified. The next cube's children were certified as far as they got
before the deadline.

## Per stratum

- **One-orbit H6(a,1)** (4 nodes, the only stratum in this shard): **0 of 4** nodes closed, so there is no median cost per closed node.
  - K = 3: **32 of 32 cubes open (100%)**. Every cube timed out at 300 s.
  - Depth 6: **49 of 49 cubes that ran were certified (0% open)**. 207 of 256 were not reached. Median certified cube 247 s solve + check
    (mean 244 s, max 297 s, all just under the cap).
  - Of the 32 K = 3 cubes, 4 were closed by refinement (one per node, each by all 8 children).
- **H3**: none in this shard (rows 1, 3, 5, … belong to other shards).

Estimate, not a measurement: if the rest of the depth-6 cubes behave like these 49, a node costs about 8 × 300 s (failed K = 3) + 64 × 244 s ≈ 18,000 s
core. That is about 6 core hours, or about 2 h wall at 3 jobs. For 0s0-2s1_1, this is about the 16,357 s the layer split has already spent, with
743 nodes still open there. All depth-6 cubes sit close to the 300 s cap, so some later ones may time out, and the estimate is optimistic on that side.

## Judgement

Depth-2 σ-cubes at K = 3 are useless for this stratum: 0 of 32 closed at 300 s, which wasted 2,400 s per node. Depth-6 σ-cubes, on the other hand, look
uniform and reliable: 49 of 49 certified, with no open cube. They should be the first step for one-orbit H6(a,1) roots in the next wave, but at **K = 6 directly**
(64 cubes, cap 300 or a bit above, since the cube times cluster at 150–300 s). Skip the K = 3 round. The per-node budget has to be about 2 h wall at
3 jobs, not the ~33 min used here. That is why no node closed in this pilot: the time ran out, not the method. Raising the cap to 600 s at K = 6
would guard against the tail near 300 s. For H3 I have no data.

# C3SIG2 G4: σ-cube pilot, shard j = 0 (rows 0, 4, 8, 12), H = 2.5 h, task at 4641a656

Tools exactly as in `tools.txt` (C3-S tools 132398c unmodified, CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 with its
example `s VERIFIED UNSAT`, lrat-check 2e3b2dc + E2 patch with the sanity check passed, `sigma_cubes.py` copied
unmodified; base CNF `p cnf 168399 4154921`, sha256 bf0e502e…6da, matches). Runner `runner.sh`, refinement driver
`refine.py` (imports `sigma_cubes` unmodified, calls `run((base, node, bits6, vals6, 300))`, 3 jobs). Each node got an even
share (~33 min wall, 3 jobs) and was killed at its share deadline; cubes not finished by then are unrecorded (= open,
not run). All records in `out.jsonl`; `summary.py` → `summary.tsv`.

No SAT. No proof rejection: all 45 UNSAT cubes accepted by both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`).
No memory problem (4 cores, 15 GB).

## Table

All four of my rows are in the one-orbit H6(a,1) stratum; no H3 node was in this shard.

| row | node | stratum | K=3 cert / open | refined: run / cert / open-of-run / not run | solve s | check s | largest cube s | closed | layer split: spent_core_s / open_nodes |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0s0-1s1_4 | H6(1,1)/one | 0 / 8 (all 300 s timeouts) | 12 / 12 / 0 / 52 | 4677.7 | 596.4 | 300.1 (K=3 timeout); 248.2+check refined | no | 28419.2 / 4299 (partial) |
| 4 | 0s0-2s1_3 | H6(2,1)/one | 0 / 8 | 11 / 11 / 0 / 53 | 4637.5 | 562.0 | 301.6 | no | untouched |
| 8 | 0s0-3s1_4 | H6(3,1)/one | 0 / 8 | 12 / 12 / 0 / 52 | 4974.6 | 626.4 | 315.7 | no | untouched |
| 12 | 0s0-4s1_5 | H6(4,1)/one | 0 / 8 | 10 / 10 / 0 / 54 | 4430.9 | 464.1 | 329.6 | no | untouched |

(solve s includes the 8 × ~300 s of K=3 timeouts per node. Largest cube = max solve+check over the node's records.)

Refined cubes (6 bits: residues 2,3,5,6,7,8 / 1,4,5,6,7,8 / 1,2,5,6,7,8 / 1,2,3,6,7,8): 45 run, 45 certified, 0 timed
out at cap 300. Cost per refined cube solve+check: median 250.6 s, mean 252.6 s, min 169.9, max 329.6 (check ~50 s).
They come only from the first two K=3 cubes of each node ((0,0,0) and (0,0,1) on the first three free residues), so
they are a sample of 2 of 8 parent cubes per node.

## Per stratum

- One-orbit H6(a,1): 0 of 4 nodes closed (no median cost per closed node). Open fraction at K=3: 32/32 = 100%.
  At the refined level: 0/45 of the cubes run stayed open (0%); 211 of 256 refined cubes were not reached in the time.
- H3: no nodes in this shard (rows 1, 3, 5, … are on other machines).

Projection (not measured): if the other refined cubes behave like the 45 sampled ones, a node costs about
8 × 300 (wasted K=3 timeouts) + 64 × 253 ≈ 18,600 core-s (~1.7 h wall at 3 jobs, ~1.3 h if K=3 is skipped:
64 × 253 ≈ 16,200 core-s). For 0s0-1s1_4 that is about 0.65 of what the layer split has already spent (28,419 s)
without closing it (4,299 nodes still open).

## Judgement

On one-orbit H6(a,1) roots, K = 3 at cap 300 is useless (0/32 certified, every cube times out), while the 6-bit cubes
are uniformly tractable (45/45 certified, all under 330 s, very low variance). So σ-cubes at depth 2 look like the right
first step for this stratum in the next wave, but directly at K = 6 (64 cubes, cap 300) rather than K = 3 followed by
refinement: that saves the ~2,400 core-s of K=3 timeouts per node, and the projected ~16,000 core-s per node is well below
the layer split's cost on 0s0-1s1_4. Caveats: no node was closed here, the refined sample covers only the parent cubes
(0,0,0) and (0,0,1), and the share per node (~33 min wall) was far too short for 64 cubes; the next wave should budget
~1.5 h wall per node at 3 jobs (or spread a node's 64 cubes over machines). For H3 see the other shards.

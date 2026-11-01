# C3SIG G3: σ-cube pilot, shard j = 3

Machine G3: 4 cores, 15 GB RAM, no swap (`env.txt`). Budget H = 2.0 h starting 04:39 UTC on 2026-10-21. The task file is at 640a56c2. The runner started at 04:42:37 and finished at 05:33:42.
Tools are listed in `tools.txt`: the C3-S worktree at 132398c (unmodified), `sigma_cubes.py` copied unmodified from `results/C3PLAN/scripts/`, CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, and drat-trim lrat-check 2e3b2dc with the E2 patch. The sanity checks passed. The base CNF has header `p cnf 168399 4154921` and sha256 `bf0e502e…6da` (matches).

My nodes are rows 3, 7, 11, 15 and 19 of `results/C3W3/lists/S_sigma_nodes.tsv` (`nodes.tsv`). `runner.sh` ran `sigma_cubes.py BASE out.jsonl NODE 3 300 3` on each node, with a per-node deadline equal to an even share of the time left. The rule was to run K = 6 only if a K = 3 cube stayed open. None did, so **K = 6 was never run**.

## Results

Cost means solve + check seconds summed over the cubes, the same measure as `recorded_core_s` (solve + check summed over the layer-split subtree). "max cube s" is solve + check of the most expensive cube.

| row | node | K | cubes | certified | open | solve s | check s | max cube s | σ-cube cost s | recorded_core_s | ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 0s0-1s1_2s1-9s1 | 3 | 8 | 8 | 0 | 995.9 | 318.0 | 239.2 | 1313.9 | 15828.2 | 0.083 |
| 7 | 0s0-1s1_6s0-7s1 | 3 | 8 | 8 | 0 | 1603.2 | 355.4 | 269.5 | 1958.6 | 15564.5 | 0.126 |
| 11 | 0s0-1s1_2s1-4s0 | 3 | 8 | 8 | 0 | 1326.7 | 334.4 | 288.1 | 1661.1 | 15137.8 | 0.110 |
| 15 | 0s0-1s1_2s0-4s1 | 3 | 8 | 8 | 0 | 1406.1 | 338.0 | 247.9 | 1744.1 | 14658.8 | 0.119 |
| 19 | 0s0-1s1_7s0-10s1 | 3 | 8 | 8 | 0 | 1097.3 | 311.8 | 227.6 | 1409.1 | 14156.6 | 0.100 |

- **Median ratio σ-cube cost / layer-split cost: 0.110.** The range is 0.083 to 0.126, so the σ split was about 8 to 12 times cheaper on every node.
- **Open cubes at K = 3: 0 of 40 (0%).** At K = 6 no cubes were run, since nothing needed refining.
- Every one of the 40 cubes is UNSATISFIABLE. Both checkers accepted all 40 proofs: lrat-check E2 printed `c VERIFIED` and cake_lpr printed exactly `s VERIFIED UNSAT`. There was no SAT, no proof rejection and no memory problem.
- The slowest single solve took 236.6 s (cap 300). The slowest check took 52.9 s. The largest LRAT proof was about 385 MB; proofs were deleted after checking. Each node's wall time with 3 jobs was 8.6 to 12.1 min.
- The σ bits were the K smallest free residues. For K = 3 these were {3,4,5} (row 3), {2,3,4} (row 7), {3,5,6} (rows 11 and 15) and {2,3,4} (row 19).

## PLAN.md criterion

The criterion has two parts: the median must be below half of the layer-split cost, and under 20% of second-level cubes may be open.
- The median part is **met**: 0.110 is well below 0.5.
- The second-level part is **met vacuously**. No first-level cube stayed open, so no second-level (K = 6) cubes were needed and none were measured. The open fraction at K = 3 is already 0%.
- One caveat on headroom: the slowest cube used 79% of the 300 s cap. Harder nodes in the other shards may leave K = 3 cubes open.

Files: `out.jsonl` (all records), `summary.md` (output of the summary script), `driver_tail.log`, `runner.sh`, `nodes.tsv`, `tools.txt`, `env.txt`.

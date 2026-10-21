# C3SIG G2: σ-cube pilot, shard j = 2 (rows 2, 6, 10, 14, 18)

Task: `results/C3SIG/TASK.md` at 640a56c2, V = G2, j = 2, H = 2.0. One cloud VM, 4 cores, 15 GB, no swap (`env.txt`), started 04:39 UTC on 2026-10-21. The runner finished at 05:28 UTC.

Tools (`tools.txt`): C3-S tools from a worktree of 132398c, unmodified. `sigma_cubes.py` was copied unmodified from `results/C3PLAN/scripts/`. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), and drat-trim lrat-check 2e3b2dc with the E2 patch. The sanity check passed: `3 0 0` was rejected and `3 0 1 2 0` accepted. The base CNF `gen_case.py 11 7 none` has header `p cnf 168399 4154921` and sha256 `bf0e502e…dd6da`, both matching.

Run (`runner.sh`): for each node, `sigma_cubes.py /opt/work/base.cnf out.jsonl NODE K 300 3` with K = 3. K = 6 would have run only if a K = 3 cube had stayed open, and none did. Each node had a rolling even share of the time left, and every node finished well inside its share (about 8–10 min wall each).

## Result

All 5 nodes were closed at K = 3. All 40 cubes are UNSAT, and both checkers accepted every proof (lrat-check `c VERIFIED` and cake_lpr exactly `s VERIFIED UNSAT`). There was no SAT, no proof rejection and no memory problem.

| row | node | K | cubes run | certified | open | solve s | check s | total s | max cube s (solve+check) | recorded_core_s | ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 0s0-1s1_4s0-6s1 | 3 | 8/8 | 8 | 0 | 1285.1 | 325.3 | 1610.4 | 265.7 | 16139.4 | 0.100 |
| 6 | 0s0-1s1_4s1-6s0 | 3 | 8/8 | 8 | 0 | 1198.8 | 333.8 | 1532.6 | 252.4 | 15568.3 | 0.098 |
| 10 | 0s0-1s1_2s1-3s0 | 3 | 8/8 | 8 | 0 | 931.0 | 342.9 | 1273.9 | 183.8 | 15281.9 | 0.083 |
| 14 | 0s0-1s1_4s0-7s1 | 3 | 8/8 | 8 | 0 | 977.2 | 324.2 | 1301.4 | 207.8 | 14805.9 | 0.088 |
| 18 | 0s0-1s1_5s1-6s0 | 3 | 8/8 | 8 | 0 | 1302.0 | 364.2 | 1666.2 | 235.1 | 14295.3 | 0.117 |

The ratio is (σ-cube solve + check) / `recorded_core_s` (layer-split solve + check over the subtree). Times are summed per cube and are not wall clock: 3 jobs shared 4 cores, as in the waves. Largest cube: 222.3 s solve, 265.7 s solve + check.

- **Median ratio σ-cube / layer split: 0.098** (range 0.083–0.117), so the σ split is about 10× cheaper on these nodes.
- **Open cubes: K = 3: 0 of 40 (0%). K = 6: not run** (no open K = 3 cube, so no second-level cubes were needed: 0 open).
- **PLAN.md criterion:** the median is below half the layer-split cost (0.098 < 0.5), so that part is **met**. The second-level open fraction is under 20% only trivially: no first-level cube was open, so no second level was generated (0%). K = 6 timing was not measured on this shard.

Files: `out.jsonl` (40 cube records with cnf sha256, solve and check times, and both checker outputs), `driver_tail.log`, `nodes.tsv`, `runner.sh`, `tools.txt`, `env.txt`.

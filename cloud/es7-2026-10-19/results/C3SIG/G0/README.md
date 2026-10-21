# C3SIG G0 (shard j = 0): σ-cube pilot on hard two-orbit nodes

Task `results/C3SIG/TASK.md` at 640a56c2, V = G0, j = 0, H = 2.0. Run 2026-10-21 04:39–05:21 UTC on one cloud VM
(4 cores, 15 GB, no swap; `env.txt`).

## Tools (`tools.txt`)
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified; `sigma_cubes.py` copied from `results/C3PLAN/scripts/` unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc + E2 patch.
  Sanity: LRAT `3 0 0` on {1},{-1} rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).

## Run
Nodes: rows 0, 4, 8, 12, 16 of `results/C3W3/lists/S_sigma_nodes.tsv` (`nodes.tsv`). `runner.sh` ran
`sigma_cubes.py base out.jsonl NODE 3 300 3` per node, with an even time share per node and K = 6 only if a K = 3
cube stayed open. No cube stayed open, so **K = 6 was not run on any node** (no share deadline was reached).
Every one of the 40 cubes is UNSAT and certified by both checkers (lrat-check `c VERIFIED` and
cake_lpr exactly `s VERIFIED UNSAT`; checked over all records of `out.jsonl`). No SAT, no proof rejection,
no memory problem (peak about 3 GB used; largest LRAT proof 382 MB).

## Results (K = 3, cap 300, 3 jobs; `summary.tsv`, `out.jsonl`)

| row | node | σ bits | certified / open | solve s | check s | largest cube (solve + check) s | layer split `recorded_core_s` | ratio |
|---|---|---|---|---|---|---|---|---|
| 0 | `0s0-1s1_2s0-9s0` | 3,4,5 | 8 / 0 | 673.5 | 315.4 | 147.0 | 16,389.6 | 0.060 (16.6× less) |
| 4 | `0s0-1s1_4s1-5s0` | 2,3,6 | 8 / 0 | 1,305.4 | 354.0 | 234.9 | 15,792.7 | 0.105 (9.5× less) |
| 8 | `0s0-1s1_2s0-3s1` | 4,5,6 | 8 / 0 | 1,027.1 | 345.7 | 212.0 | 15,397.8 | 0.089 (11.2× less) |
| 12 | `0s0-1s1_3s0-10s0` | 2,4,5 | 8 / 0 | 673.3 | 330.4 | 156.2 | 15,074.1 | 0.067 (15.0× less) |
| 16 | `0s0-1s1_2s0-6s1` | 3,4,5 | 8 / 0 | 742.8 | 303.9 | 156.4 | 14,618.7 | 0.072 (14.0× less) |

K = 6: not run (nothing open at K = 3).

- Median ratio σ-cube cost / layer-split cost: **0.072** (range 0.060–0.105). Largest single cube solve: 189.6 s (under the 300 s cap).
- Open cubes: K = 3: **0 / 40 (0%)**; K = 6: not run, 0 / 0.
- PLAN.md criterion (median below half the layer-split cost; under 20% of second-level cubes open): the median part is
  met by a wide margin (0.072 < 0.5). The second-level part is met trivially on this shard: no second level was needed,
  since 0% of the first-level (K = 3) cubes were open.
- All 5 nodes are closed by their 8 σ-cubes (the cubes cover every assignment of the 3 bits). This differs from the PLAN §3b
  pilot (cap 150/120), where 2 of 3 nodes kept open cubes; at cap 300 none did here.

Files: `env.txt`, `tools.txt`, `nodes.tsv`, `runner.sh`, `out.jsonl` (per cube records plus one `meta: run` record per
node and K), `summary.tsv`, `driver.log`.

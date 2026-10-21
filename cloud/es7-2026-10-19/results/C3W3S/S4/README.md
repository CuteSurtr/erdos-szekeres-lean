# C3W3S S4: σ-cube closure of mirror-kept two-orbit s = 1 roots, from the end of the list

Task `results/C3W3S/TASK.md` at 5f9d1dba, V = S4, j = 4, N = 12, H = 4.0. Run 2026-10-21 06:03–07:44 UTC on one cloud VM
(4 cores, 15 GB, no swap; `env.txt`). The driver finished all its roots at 07:43:49, well before END (09:48:34).

## Tools and base check (`tools.txt`)
- C3-S tools: worktree of 132398c at /opt/c3s, unmodified; `sigma_cubes.py` copied from `results/C3PLAN/scripts/` unmodified.
- CaDiCaL 3.0.1 (c6073042); cake_lpr a36874a8 (example: `s VERIFIED UNSAT`); drat-trim lrat-check 2e3b2dc + E2 patch.
  Sanity: LRAT `3 0 0` on {1},{-1} rejected by both, `3 0 1 2 0` accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…0cdd6da` (matches).

## Run
Roots (`roots.tsv`): the 301 rows of `C3W3/lists/C_s1two.tsv` with `h6m_kept` = yes, sorted by decreasing row; positions ≡ 4 (mod 12)
(0-based): 25 roots. `s4driver.py` (setsid nohup) kept 3 worker processes busy, root by root in that order, with earlier roots first:
(a) `close_node.py BASE out 300 R`, its record appended to `out_direct.jsonl`; (b) if not certified, the 8 cubes on the 3 smallest
free residues via `sigma_cubes.run((base, R, bits3, vals3, 300))` (the call `sigma_cubes.py BASE OUT R 3 300 3` makes, scheduled
in the shared 3-worker pool); (c) for each open level-1 cube, the 8 extending cubes on the 6 smallest free residues via
`sigma_cubes.run((base, R, bits6, vals6, 300))`. Records of (b) and (c) are in `out_sigma.jsonl` in the `sigma_cubes.py` format.
Before starting each root the driver fetched origin/es7-cloud and applied the skip rule of step 3 (`skip.log`).

## Per root (`summary.tsv`; solve/check seconds summed over all of the root's records)

| pos | row | root | result | solve s | check s |
|---|---|---|---|---|---|
| 4 | 296 | 0s0-5s1_7s0-9s0 | closed directly | 41.4 | 37.4 |
| 16 | 284 | 0s0-5s1_6s0-8s1 | closed at σ level 1 (8/8) | 1505.9 | 383.9 |
| 28 | 272 | 0s0-5s1_2s1-6s1 | closed directly | 95.2 | 43.1 |
| 40 | 260 | 0s0-5s1_2s0-6s0 | closed directly | 41.2 | 35.5 |
| 52 | 248 | 0s0-5s1_1s1-6s0 | closed at σ level 1 (8/8) | 798.5 | 275.1 |
| 64 | 236 | 0s0-5s1_1s0-7s1 | closed directly | 280.3 | 40.9 |
| 76 | 224 | 0s0-4s1_7s1-8s1 | closed directly | 43.7 | 29.1 |
| 88 | 212 | 0s0-4s1_6s0-7s1 | closed at σ level 1 (8/8) | 1687.9 | 311.2 |
| 100 | 200 | 0s0-4s1_5s0-8s0 | closed directly | 45.3 | 29.0 |
| 112 | 188 | 0s0-4s1_2s0-7s0 | closed directly | 166.6 | 36.5 |
| 124 | 176 | 0s0-4s1_1s1-7s0 | closed directly | 227.3 | 40.6 |
| 136 | 164 | 0s0-4s1_1s0-8s1 | closed directly | 93.6 | 33.5 |
| 148 | 152 | 0s0-4s1_1s0-10s0 | closed at σ level 1 (8/8) | 1057.9 | 313.9 |
| 160 | 140 | 0s0-3s1_5s1-7s0 | closed at σ level 2 (level 1: 7/8; cube {1:1,2:0,4:1} split on 6,8,9: 8/8) | 2101.7 | 564.8 |
| 172 | 128 | 0s0-3s1_4s1-9s0 | closed at σ level 1 (8/8) | 670.8 | 260.7 |
| 184 | 116 | 0s0-3s1_4s0-8s1 | closed at σ level 1 (8/8) | 1126.9 | 299.1 |
| 196 | 104 | 0s0-3s1_1s1-8s1 | closed at σ level 1 (8/8) | 1341.1 | 300.4 |
| 208 | 92 | 0s0-3s1_1s1-10s0 | closed directly | 54.8 | 31.6 |
| 220 | 80 | 0s0-3s1_1s0-10s1 | closed directly | 101.8 | 26.3 |
| 232 | 68 | 0s0-2s1_5s0-6s1 | closed at σ level 1 (8/8) | 1736.1 | 328.3 |
| 244 | 56 | 0s0-2s1_4s0-8s0 | skipped (record in C3W3/C2/out.jsonl) | – | – |
| 256 | 44 | 0s0-2s1_3s1-10s1 | skipped (record in C3W3/C8/out.jsonl) | – | – |
| 268 | 32 | 0s0-2s1_1s0-6s1 | skipped (record in C3W3/C14/out.jsonl) | – | – |
| 280 | 20 | 0s0-2s1_3s1-6s0 | skipped (record in C3W3/C2/out.jsonl) | – | – |
| 292 | 8 | 0s0-1s1_3s1-9s1 | skipped (record in C3W3/C8/out.jsonl) | – | – |

## Totals
- 20 roots run, all 20 closed: 11 directly, 8 at σ level 1, 1 at σ level 2; 0 open. 5 roots skipped (C machines had reached them).
- Records: 20 direct (11 certified, 9 timeouts at 300 s), 72 level-1 cubes (71 certified, 1 timeout), 8 level-2 cubes (8 certified).
  Every UNSAT record is certified by both checkers (lrat-check `c VERIFIED` and cake_lpr exactly `s VERIFIED UNSAT`).
- Solve 13,218.0 s, check 3,420.9 s (CPU-process seconds, all records). Largest LRAT proof 383 MB.
- No SAT, no proof rejection (no `recheck.jsonl`), no memory problem (about 6 GB peak used of 15).

Files: `env.txt`, `tools.txt`, `roots.tsv`, `s4driver.py`, `out_direct.jsonl`, `out_sigma.jsonl`, `skip.log`, `summary.tsv`, `driver.log.tail`.

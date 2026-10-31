# C2P5 M82: list C2P5B.tsv, shard 32 of 50

Task: `results/C2P5/TASK.md` at commit 81cb025f, with V = M82, LIST = C2P5B.tsv, j = 32, N = 50, H = 5.25.
Start 2026-10-31 15:11:03 UTC (epoch 1793459463), END 20:11:03 UTC. The lane finished all units at 18:23:35 UTC.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` only (manifest: all 196 files match):
  CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code was cloned or downloaded.
- Sanity: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`, both as expected.
- Cubes: `l2cubes.py` for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19: rows of C2P5B.tsv with idx ≡ 32 mod 50)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| total | | 19 | 19 | 0 | 0 | 0 |

All 19 are UNSATISFIABLE and certified: lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT` for every one.

Certified units (min / median / max):
- solve: 19.8 / 274.6 / 1210.0 s (largest P3_7-12, Q, cap 8000)
- lrat-check: 12.1 / 51.0 / 69.9 s
- cake_lpr: 108.2 / 297.7 / 408.1 s
- proof size: 0.22 / 3.27 / 4.58 GB

| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|
| P2_5-7 | Q | 387.1 | 49.3 | 305.1 | 3.35 | 4368 |
| P1_4-5 | Q | 369.7 | 48.1 | 290.7 | 3.26 | 4378 |
| P2_1-4-12 | H | 426.2 | 53.2 | 318.7 | 3.58 | 4416 |
| P2_3-4-14 | H | 308.9 | 55.9 | 314.6 | 3.41 | 4382 |
| P2_3-8-14 | H | 508.8 | 58.4 | 335.8 | 3.64 | 4388 |
| P2_4-6-10 | H | 82.7 | 23.9 | 170.9 | 1.26 | 3202 |
| P2_5-6-8 | H | 26.3 | 12.3 | 110.6 | 0.22 | 2680 |
| P2_6-8-10 | H | 26.5 | 12.8 | 111.3 | 0.22 | 2648 |
| P1_2-5-10 | H | 210.3 | 51.0 | 291.4 | 3.19 | 4353 |
| P1_2-12-13 | H | 274.6 | 52.3 | 310.0 | 3.39 | 4416 |
| P1_3-8-15 | H | 478.1 | 55.7 | 330.4 | 3.66 | 4426 |
| P1_4-9-13 | H | 245.0 | 52.1 | 297.7 | 3.27 | 4408 |
| P1_7-9-11 | H | 23.2 | 12.1 | 108.2 | 0.22 | 2647 |
| P3_7-12 | Q | 1210.0 | 69.9 | 408.1 | 4.58 | 4379 |
| P3_1-7-10 | H | 370.4 | 53.1 | 313.2 | 3.35 | 4397 |
| P3_4-5-7 | H | 98.9 | 27.7 | 175.0 | 1.49 | 3404 |
| P3_4-10-11 | H | 191.3 | 45.6 | 274.6 | 3.03 | 4342 |
| P3_5-9-14 | H | 299.8 | 55.7 | 309.9 | 3.33 | 4380 |
| P3_7-9-11 | H | 19.8 | 12.4 | 109.8 | 0.22 | 2659 |

Largest solver RSS: 4426 MB (P1_3-8-15).

## Problems
No SAT, no proof rejection, no ERROR status, no memory problem.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

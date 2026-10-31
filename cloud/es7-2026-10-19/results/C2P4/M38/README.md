# C2P4 M38

TASK `results/C2P4/TASK.md` at a46b478d, with V = M38, LIST = C2P4.tsv, j = 38, N = 50, H = 2.5. Start 13:01:21Z (epoch 1793451681). The lane ran from 13:03:08Z to 15:10:17Z, with END = 1793459781 (15:16:21Z). Machine: 4 CPUs, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) from the vendored `vendor/tools-src.tar.xz`. The manifest check passed: all 196 files match. Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match the expected values.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19 rows of C2P4.tsv with idx ≡ 38 mod 50)
- **Certified (UNSAT; lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`): 9.**
  - P5: 6 (Q 1: P5_7-10; H 5: P5_1-3-14, P5_2-6-13, P5_6-7-9, P5_6-14-15, P5_8-11-13).
  - P4: 3 (Q 1: P4_5-10; H 2: P4_1-3-10, P4_1-9-15).
- Timed out (UNKNOWN): 0.
- Not reached: 10.
  - P4: 3 H (P4_2-7-9, P4_5-9-12, P4_6-10-13).
  - P3: 1 Q (P3_1-14) and 6 H (P3_1-2-9, P3_1-8-9, P3_4-5-14, P3_4-11-13, P3_5-11-12, P3_8-9-10).
  - The lane stopped at 15:10:17Z with 363 s left before END.
- Errors, `certified: false` records, proof rejections: none.
- SAT: none. Memory: no problem.
- The lane capped the solves of the last three units below their list caps (P4_5-10 at 3534 s, P4_1-3-10 at 1413 s, P4_1-9-15 at 654 s). All three finished within those caps.

| quantity (certified units) | min / median / max |
|---|---|
| solve s | 25.4 / 359.6 / 1566.6 |
| lrat-check s | 13.4 / 57.8 / 80.4 |
| cake_lpr s | 116.6 / 329.1 / 446.0 |
| proof size GB | 0.2 / 3.4 / 4.8 |

Largest solver RSS: 4411 MB.

| unit | case | kind | cap s | solve s | proof GB | lrat-check s | cake_lpr s | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P5_7-10 | P5 | Q | 6000 | 744.46 | 3.73 | 62.0 | 358.2 | 4411 |
| P5_1-3-14 | P5 | H | 1800 | 258.15 | 3.22 | 55.7 | 314.8 | 4360 |
| P5_2-6-13 | P5 | H | 1800 | 572.76 | 3.66 | 66.3 | 356.4 | 4376 |
| P5_6-7-9 | P5 | H | 1800 | 25.97 | 0.22 | 13.7 | 116.6 | 2650 |
| P5_6-14-15 | P5 | H | 1800 | 310.39 | 3.28 | 57.8 | 327.8 | 4357 |
| P5_8-11-13 | P5 | H | 1800 | 25.39 | 0.22 | 13.4 | 118.0 | 2645 |
| P4_5-10 | P4 | Q | 3534 | 1566.63 | 4.82 | 80.4 | 446.0 | 4371 |
| P4_1-3-10 | P4 | H | 1413 | 359.55 | 3.37 | 56.7 | 329.1 | 4411 |
| P4_1-9-15 | P4 | H | 654 | 470.04 | 3.54 | 61.1 | 346.2 | 4404 |

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (one record per unit), `lane.log.tail`.

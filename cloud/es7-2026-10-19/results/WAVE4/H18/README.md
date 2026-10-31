# WAVE4 H18: case U_L2

- Case U_L2 (U = "", L = "2"), CASE.cnf sha256 1d26b947...aaa53 (matches cases.jsonl); F sha256 69c1dc8f...f932d (matches).
- Cubes given: 324 (tasks/H18.json @ e0f250b), written to `U_L2/top.icnf` (324 lines).
- Driver: unmodified copy of WAVE2/F2/close_march.py (see driver.diff), `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.21`,
  started 2026-10-20T12:55:50Z, ended about 13:33Z with `open 0`.
- Verified leaves: 387 (every one with cake_lpr `s VERIFIED UNSAT`), listed in `U_L2/leaves.icnf`.
- Cubes split: 1 (timed out at 300 s; march_cu split depth 6 gave 64 sub-cubes, 0 refuted, 94 s; all 64 closed).
  323 given cubes closed directly.
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Cover: every given cube is covered by the leaves (checked: each top cube is a leaf, or its 64 sub-cubes are all leaves
  and cover the cube under a full case split).
- Solve time (CaDiCaL, 387 UNSAT leaves): sum 5001.1 s, median 10.51 s, max 99.1 s (plus one 300 s timeout before the split).
- Check time (cake_lpr): sum 1640.0 s, median 3.79 s, max 15.46 s.
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record.

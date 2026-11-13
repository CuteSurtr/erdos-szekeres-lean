# WAVE4 H13: U_L2

- Case: U_L2 (U = none, L = 2); case CNF sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53 (matches cases.jsonl); F sha256 69c1dc8f...ff932d checked.
- Cubes given: 324 (results/WAVE4/tasks/H13.json at e0f250b), written to top.icnf in file order (324 lines; top_sha256 b4270b9b6b4613438448a3ebc8bbdc42fe60a31e3e64bec0d67620a3302db924).
- Driver: results/WAVE4/H13/close_march.py (byte copy of WAVE2/F2, see driver.diff), --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.216, started 12:55:47Z, ended about 14:12Z with "open 0".
- Verified leaves: 632 (every one with cake_lpr "s VERIFIED UNSAT"); leaves.icnf has 632 lines.
- Cubes split: 5 (300 s timeouts), into 63, 64, 64, 58 and 64 sub-cubes (march_cu split times 385.4, 163.0, 91.1, 586.8, 165.1 s).
- Cubes still open: 0 (open.icnf is empty).
- Cover: every one of the 324 given cubes is covered by the verified leaves (checked over the split tree recorded in leaves.jsonl: 324 - 5 + 313 = 632 leaves).
- Solve time (CaDiCaL, 637 runs incl. the 5 timeouts): sum 14201.2 s, median 10.89 s, max 300.03 s.
- Check time (cake_lpr, 632 runs): sum 2463.2 s, median 2.77 s, max 22.23 s.
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record.
- Tools: see tools.txt (CaDiCaL 3.0.1 c6073042, march_cu 705b60c6 with -fcommon, cake_lpr a36874a8; example prints s VERIFIED UNSAT).

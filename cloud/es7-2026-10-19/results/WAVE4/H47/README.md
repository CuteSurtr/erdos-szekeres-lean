# WAVE4 H47 (mop-up round 2): U_L2

- Case: U_L2 (CASE.cnf sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53, matches cases.jsonl; F.cnf sha256 69c1dc8f...932d checked).
- Cubes given: 151 (`results/WAVE4/tasks/H47.json` at 3ed048e), written in order to `U_L2/top.icnf` (151 lines, sha256 088baff70f0bbe9c11f784d7960219b1c945b6745ec132286f2aa1fbee9f8a9b).
- Driver: byte-for-byte copy of WAVE2/F2/close_march.py (see driver.diff), --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.2, started 14:20:14 UTC, ended about 14:52 UTC with `open 0`.
- Verified leaves: 273 (every one with cake_lpr `s VERIFIED UNSAT`), in `U_L2/leaves.icnf`.
- Cubes split: 2 (march_cu: 64 sub-cubes, 0 refuted; 60 sub-cubes, 4 refuted).
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Cover: every one of the 151 given cubes is covered by the verified leaves alone (checked per cube with CaDiCaL: cube units plus the negated leaves is UNSAT for all 151).
- Solve time (275 CaDiCaL runs, incl. the 2 that timed out and were split): sum 4003.6 s, median 8.73 s, max 300.02 s.
- Check time (273 cake_lpr runs): sum 1025.8 s, median 3.16 s, max 15.88 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

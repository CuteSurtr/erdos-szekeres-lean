# WAVE4 H44 (U3_L, mop-up round 2)

- Case: U3_L (case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823, matches cases.jsonl).
- Cubes given: 190 (`results/WAVE4/tasks/H44.json` at 3ed048e; `U3_L/top.icnf`, 190 lines, sha256 2ffde648...).
- Driver: `close_march.py` (byte copy of WAVE2/F2), `--depth 7 --timeout 300 --split-depth 6 --jobs 4`,
  started 2026-10-20T14:19:32Z, ended about 14:58Z with `open 0`.
- Verified leaves: 250 (all 250 UNSAT records have cake_lpr `s VERIFIED UNSAT`; `U3_L/leaves.icnf` has 250 lines).
- Cubes split: 1 (timed out at 300 s, split by march_cu into 61 sub-cubes in 405 s; all 61 closed).
- Cubes still open: 0 (`U3_L/open.icnf` is empty).
- Coverage: every one of the 190 given cubes is covered by these leaves (189 directly by a leaf that is a
  subset of the cube, 1 through its split children, all covered).
- Solve time (CaDiCaL, 251 runs including the one 300 s timeout): sum 3747.0 s, median 9.84 s, max 300.02 s.
- Check time (cake_lpr, 250 runs): sum 1025.3 s, median 3.52 s, max 13.61 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

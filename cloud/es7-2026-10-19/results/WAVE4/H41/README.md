# WAVE4 H41 (mop-up round 2): case U3_L

- Case: U3_L (CASE.cnf sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823, matches cases.jsonl; F sha256 matches).
- Cubes given: 191 (`tasks/H41.json` at 3ed048e), written in order to `U3_L/top.icnf` (191 lines).
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record. No TIMEOUT record.
- Verified leaves: 253, each with cake_lpr `s VERIFIED UNSAT` (`U3_L/leaves.icnf`).
  - 190 given cubes closed directly.
  - 1 given cube split (CaDiCaL hit the 300 s cap): march_cu -d 6 gave 63 sub-cubes ("number of cubes 63, including 1 refuted", split 344.7 s); all 63 closed. I checked separately that the OR of the 63 sub-cubes is a tautology.
- Cubes still open: 0 (`U3_L/open.icnf` is empty; the driver printed `open 0`).
- Every given cube is covered by my leaves: yes (checked: each top cube is a leaf, or its split children cube+sub are all leaves).
- Times over the 253 verified leaves: solve sum 4574.2 s, median 14.17 s, max 239.07 s; cake_lpr check sum 1082.9 s, median 3.48 s, max 19.92 s. Child CPU sum over all records 23833.1 s.
- Run: driver started 2026-10-20 14:21:22 UTC with `--hours 2.2`, ended about 14:50 UTC (4 jobs).
- Files: env.txt, tools.txt, close_march.py (byte copy of WAVE2/F2, see driver.diff), driver.diff, U3_L/{top,leaves,open}.icnf, U3_L/leaves.jsonl.

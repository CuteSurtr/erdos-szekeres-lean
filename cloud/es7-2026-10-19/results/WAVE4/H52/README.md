# WAVE4 H52: case U3_L (task file results/WAVE4/tasks/H52.json at 94cc404)

- Case: U3_L (U = 3, L = none); case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823 (matches cases.jsonl). F sha256 69c1dc8f...932d checked.
- Cubes given: 218 (top.icnf, 218 lines, sha256 de349207051c70e6f12cdf7f8c5ac76196b80b7356b1a594ce19a63240fe0550).
- Verified leaves: 344, every one with cake_lpr `s VERIFIED UNSAT` (leaves.icnf, 344 lines).
- Cubes split: 2 (both hit the 300 s cap; march_cu -d 6 gave 64 sub-cubes each, 0 refuted). All 128 sub-cubes closed.
- Cubes still open: 0 (open.icnf is empty). Driver printed `open 0`.
- Cover: every one of the 218 given cubes is covered by these leaves (216 directly as leaves, 2 through their 64 split children each), checked by walking the SPLIT records against leaves.icnf.
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record. No TIMEOUT record.
- Times over the 344 leaves: CaDiCaL solve sum 5436.8 s, median 9.79 s, max 215.48 s; cake_lpr check sum 1341.3 s, median 3.00 s, max 19.33 s; solve+check sum 6778.0 s, median 12.86 s, max 232.2 s. The 2 split cubes spent 300.0 s each in CaDiCaL and 415.8 s / 221.0 s in march_cu. Child CPU total 30641 s.
- Wall time: driver ran 14:38:34 to about 15:15 UTC with 4 jobs (budget 1.5 h; --hours 1.21).
- Tools: tools.txt. Driver: close_march.py, byte-identical copy of results/WAVE2/F2/close_march.py (driver.diff).

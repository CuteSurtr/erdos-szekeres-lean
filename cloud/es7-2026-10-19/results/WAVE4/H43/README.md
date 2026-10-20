# WAVE4 H43: U3_L

Case U3_L (U = [3], L = []), case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823
(matches cases.jsonl); F sha256 69c1dc8f...932d checked. The cube list is `results/WAVE4/tasks/H43.json`
(at 3ed048e). The driver is a byte-for-byte copy of WAVE2/F2/close_march.py (see driver.diff); tools are listed in tools.txt.

The driver ran from 14:19:23Z to 14:42:08Z (2026-10-20), with --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.21.

- Cubes given: 190 (top.icnf, 190 lines).
- Verified leaves: 253 (leaves.icnf). cake_lpr printed `s VERIFIED UNSAT` on every one.
- Cubes split: 1, top cube #132 (0-based), which timed out at 300 s. march_cu (depth 6) split it into
  64 subcubes, none refuted by march itself, and all 64 closed.
  The other 189 top cubes closed directly.
- Cubes still open: 0 (open.icnf is empty).
- Coverage: every one of the 190 given cubes is covered by the leaves, either as a leaf itself or through its
  split subcubes (checked from leaves.jsonl).
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Solve time (CaDiCaL, 254 runs including the one 300 s timeout): sum 3588.0 s, median 11.36 s, max 300.01 s.
- Check time (cake_lpr, 253 proofs): sum 1078.7 s, median 3.99 s, max 17.38 s.
- Split time (march_cu): 223.8 s. Total child CPU: 18062.2 s.

# WAVE4 H66: U3_L

- Case: U3_L (CASE.cnf sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823, matches cases.jsonl).
- Cubes given: 204 (results/WAVE4/tasks/H66.json at 1d3a72c); top.icnf has 204 lines.
- Verified leaves: 204, each with cake_lpr `s VERIFIED UNSAT`.
- Cubes split: 0. Cubes timed out: 0. Cubes still open: 0 (open.icnf is empty).
- Cover: every given cube is covered. leaves.icnf holds exactly the 204 given cubes (same set as top.icnf, written in completion order), every line ends with `0`.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Solve time (CaDiCaL): sum 4509.2 s, median 14.99 s, max 275.30 s.
- Check time (cake_lpr): sum 1149.7 s, median 4.52 s, max 20.88 s.
- Driver: close_march.py (byte-for-byte copy of results/WAVE2/F2/close_march.py), run 15:07:17 to about 15:32 UTC with
  `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.15` on 4 cores. Tools and checks: tools.txt, driver.diff.
- Files: U3_L/leaves.icnf, U3_L/open.icnf, U3_L/top.icnf, U3_L/leaves.jsonl.

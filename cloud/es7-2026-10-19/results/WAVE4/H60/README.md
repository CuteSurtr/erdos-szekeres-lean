# WAVE4 H60: case U3_L

Task file `results/WAVE4/tasks/H60.json` (commit 1d3a72c), case U3_L (U="3", L=""), case CNF sha256 7ab00d97…f0e823 (matches cases.jsonl).
Driver `close_march.py` (byte copy of WAVE2/F2, see driver.diff), run 15:03:03 to 15:41 UTC on 4 cores with
`--top top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.17`.

- Cubes given: 205 (top.icnf, 205 lines, sha256 c4cd43a5…ebfd6).
- Verified leaves: 331, every one with cake_lpr `s VERIFIED UNSAT` (leaves.icnf).
- Cubes split: 2 (each hit the 300 s cap; march_cu split depth 6 gave 64 sub-cubes each, all 128 closed).
- Cubes still open: 0 (open.icnf is empty).
- Cover: every given cube is covered by my leaves (203 directly, 2 by their 64 sub-cube leaves each). Checked with a separate script that also rejects lines not ending in ` 0`.
- Solve time over the 331 leaves: sum 5486.6 s, median 9.52 s, max 157.77 s. Check time (cake_lpr): sum 1389.7 s, median 2.92 s, max 16.93 s. The 2 split cubes used 300 s each of solving, plus 212.3 s and 371.1 s of march_cu.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

Files: `U3_L/top.icnf`, `U3_L/leaves.icnf`, `U3_L/open.icnf`, `U3_L/leaves.jsonl`; tools in tools.txt, environment in env.txt.

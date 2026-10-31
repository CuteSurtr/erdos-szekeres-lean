# WAVE4 H45: U3_L mop-up round 2 (6/6)

Task file `results/WAVE4/tasks/H45.json` (committed at 3ed048e), case **U3_L** (U = 3, L = none; case CNF sha256 7ab00d97…f823, matches cases.jsonl; F sha256 69c1dc8f…932d checked).
Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`); tools in `tools.txt`.
Run: `--top top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.15`, 14:22:10 to about 15:02 UTC. The driver ended on its own with `open 0`.

- Cubes given: 190 (`U3_L/top.icnf`, 190 lines, in the task file's order).
- Verified leaves: 252 (`U3_L/leaves.icnf`), each with cake_lpr `s VERIFIED UNSAT`.
  - 189 of the given cubes were closed directly.
  - 1 given cube timed out at 300 s and was split by march_cu at depth 6 into 63 sub-cubes ("number of cubes 63, including 1 refuted", 661.5 s). All 63 were closed.
- Cubes split: 1. Cubes still open: 0 (`U3_L/open.icnf` is empty).
- Cover: all 190 given cubes are covered by my leaves. 189 of them are leaves themselves. The split cube is covered by its 63 march_cu children, which are all leaves. That step assumes march_cu's children partition the cube, which the later case cover check re-checks.
- Solve time (CaDiCaL, 252 UNSAT runs): sum 3837.9 s, median 11.3 s, max 88.1 s (plus one 300 s timeout before the split).
- Check time (cake_lpr): sum 1140.2 s, median 3.7 s, max 13.9 s. No heap retries.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

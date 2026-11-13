# WAVE4 H28: case U4_L

Task `results/WAVE4/tasks/H28.json` (at e0f250b): case U4_L, 190 open cubes.
Case CNF sha256 ab7286828ae500e47de8236b6c6953c8ac9a3e776d71991cca253246090ff991 (= cases.jsonl).
Driver: `close_march.py`, a byte-for-byte copy of WAVE2/F2 (see `driver.diff`); tools in `tools.txt`.
Run 13:20:48 to 13:49 UTC 2026-10-20, 4 jobs, timeout 300 s, split depth 6.

Result (all in `U4_L/`):
- cubes given: 190 (`top.icnf`, sha256 b2d57468...)
- verified leaves: 316 (`leaves.icnf`), each with cake_lpr `s VERIFIED UNSAT`
- cubes split: 2 (each timed out at 300 s; march_cu -d 6 gave 64 sub-cubes, 0 refuted, all 128 closed)
- cubes still open: 0 (`open.icnf` is empty)
- every given cube is covered by the leaves: yes (188 are leaves themselves; the 2 split cubes are covered
  by their 64 sub-cube leaves each, per the SPLIT records in `leaves.jsonl`)
- solve time of verified leaves: sum 3205.4 s, median 6.62 s, max 208.68 s
  (plus 2 x 300 s timeouts and 472.9 s + 514.2 s march_cu splitting)
- check time (cake_lpr): sum 1088.2 s, median 2.68 s, max 22.83 s
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

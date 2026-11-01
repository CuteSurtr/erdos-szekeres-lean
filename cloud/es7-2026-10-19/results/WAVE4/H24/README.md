# WAVE4 H24: case U3_L

Task file `results/WAVE4/tasks/H24.json` at e0f250b. Driver `close_march.py` = byte copy of
`results/WAVE2/F2/close_march.py` (sha256 2e0975aa…c855, see `driver.diff`); tools in `tools.txt`.
Run: 2026-10-20 12:57:29Z to about 15:07Z, `--top top.icnf --depth 7 --timeout 300 --split-depth 6
--jobs 4 --hours 2.21`, 4 cores. Case CNF sha256 7ab00d97…f823 (matches cases.jsonl).

Results (files in `U3_L/`):
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT record.
- Cubes given: 318 (top.icnf, sha256 14d2fb22…e35f, same order as the task list).
- Verified leaves: 836 (`leaves.icnf`; each has cake_lpr `s VERIFIED UNSAT` in leaves.jsonl).
- Cubes split: 18 (14 given cubes, 4 of their children), giving 1148 sub-cubes (march_cu -d 6).
- Cubes still open: 612 (`open.icnf`), all below 10 given cubes (0-based line index in top.icnf:
  count) 101:64, 102:64, 103:63, 104:61, 108:40, 181:64, 213:64, 292:64, 300:64, 304:64.
- Covered: 308 of the 318 given cubes are fully covered by my verified leaves; the 10 above are not.
  Not every given cube is covered.
- open.icnf check: I rebuilt the frontier independently from top.icnf, the SPLIT records and
  leaves.icnf; it equals open.icnf exactly (612 cubes, same order), and no open cube contains
  a verified leaf. Every line of the three .icnf files is `a ... 0`.
- Times (solver runs, n = 854 incl. 18 runs that hit the 300 s cap and were split):
  solve sum 21901.2 s, median 14.0 s, max 300.1 s; verified leaves only: sum 16500.7 s,
  median 13.8 s, max 260.4 s. cake_lpr checks (n = 836): sum 3451.2 s, median 3.3 s, max 23.3 s.
  march_cu splits: sum 5405.6 s.

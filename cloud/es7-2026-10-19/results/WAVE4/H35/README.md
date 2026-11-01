# WAVE4 H35 — case U_L7

Task: `results/WAVE4/tasks/H35.json` (commit 4bfd8e7), case U_L7, 197 open cubes.
Driver: unmodified `close_march.py` (copy of WAVE2/F2, sha256 2e0975aa…, see driver.diff), run
13:32–14:20 UTC with `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.213`.
Case CNF sha256 c6d1c840… matches cases.jsonl; F sha256 69c1dc8f… matches. Tools in tools.txt.

Results (`U_L7/`):
- Cubes given: 197 (top.icnf, 197 lines, in the task file's order).
- Verified leaves: 319 (every one `s VERIFIED UNSAT` from cake_lpr; leaves.icnf has 319 lines).
- Cubes split: 2 (each hit the 300 s cap; march_cu -d 6 gave 64 sub-cubes, 0 refuted, and
  60 sub-cubes, 4 refuted).
- Cubes still open: 0 (open.icnf is empty; the driver printed `open 0`).
- Cover: every one of the 197 given cubes is covered by the leaves (directly, or through its
  SPLIT record's sub-cubes, all of which are verified leaves). Every leaf extends a given cube.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
- Solve time (CaDiCaL, 321 runs incl. the 2 timeouts): sum 6228.5 s, median 7.14 s, max 300.02 s;
  UNSAT runs only: sum 5628.5 s, median 6.85 s, max 232.32 s.
- Check time (cake_lpr, 319 proofs): sum 1346.2 s, median 2.65 s, max 20.37 s.
- march_cu split time: 287.3 s and 496.5 s (sum 783.8 s).
- Largest LRAT proof: 168.5 MB (not committed).

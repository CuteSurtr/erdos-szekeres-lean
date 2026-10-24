# WAVE4 H33: case U_L2

Task: `results/WAVE4/tasks/H33.json` (committed at 4bfd8e7), case U_L2, 326 open cubes.
Machine: 4 cores, 15 GB (env.txt). Tools: tools.txt. Driver: close_march.py, a byte-for-byte copy of
results/WAVE2/F2/close_march.py (driver.diff).

- F regenerated, sha256 69c1dc8f…932d (matches). U_L2 case CNF (`hullsplit.py case F "" "2"`), sha256
  1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53 (matches cases.jsonl).
- top.icnf: the 326 cubes in the order given, one `a … 0` line each (326 lines), sha256 77e521e2…e004b.
- Run: `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.2`, 13:36:54 to 14:09 UTC (about 32 min).

Results:
- Cubes given: 326.
- Verified leaves: 326. Every cube was closed directly by CaDiCaL, and cake_lpr printed `s VERIFIED UNSAT` for each one.
- Cubes split: 0. Cubes still open: 0 (open.icnf is empty; the driver printed `open 0`).
- Coverage: every given cube is covered. The set of cubes in leaves.icnf equals the set in top.icnf
  (they are in a different order, since the leaves are listed in finishing order).
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no cake_lpr heap retry.
- Solve time (CaDiCaL wall, s): sum 6169.8, median 13.81, max 243.15.
- Check time (cake_lpr wall, s): sum 1673.0, median 4.41, max 23.28.
- Solve plus check per cube (s): sum 7842.8, median 18.25, max 262.59. Largest LRAT proof: 217 MB (not committed).

Files in U_L2/: top.icnf, leaves.icnf, open.icnf, leaves.jsonl (copied from /opt/work/out/U_L2 after the driver ended).

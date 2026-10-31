# WAVE4 H26: case U_L7

Task: `results/WAVE4/tasks/H26.json` at e0f250b, which lists 195 open cubes of case U_L7 (U = "", L = "7").
Budget 2.5 h. Start 13:14 UTC. Driver ran 13:17 to 15:11 UTC (it ended on its own with `open 0`).

- Case CNF sha256 c6d1c840…f099, equal to cnf_sha256 in cases.jsonl. F.cnf sha256 69c1dc8f…932d (match).
- Tools and their hashes are in `tools.txt`; the driver check is in `driver.diff` (byte-identical copy of WAVE2/F2/close_march.py, sha256 2e0975aa…c855).
- Run: `close_march.py /opt/work/CASE.cnf /opt/work/out/U_L7 --name U_L7 --top /opt/work/top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.206`, with BIN=/opt/work/bin and WORK=/opt/work/tmp. One run, no restart (1 resume record).

## Result
- Cubes given: 195. `U_L7/top.icnf` has exactly those cubes, one line per cube in file order, sha256 b1933628…1262.
- Verified leaves: **916**. Each one has CaDiCaL exit 20 and cake_lpr printed exactly `s VERIFIED UNSAT`. All 916 are listed in `U_L7/leaves.icnf`.
- Cubes split: 12, after a 300 s timeout. Split sizes from march_cu -d 6 were 64, 58, 62, 63, 64, 63, 64, 64, 57, 55, 55, 64.
- Cubes still open: **0**. `U_L7/open.icnf` is empty.
- Coverage: every given cube is covered by my leaves. This was checked from leaves.jsonl. Each top cube is either a leaf, or a SPLIT whose sub-cubes are all covered, applied recursively. The sub-cube set of each split is a complete binary decision tree, so the leaves under it are exhaustive. Every line of leaves.icnf and top.icnf ends in ` 0`.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. No cake_lpr heap retry was needed.
- Times for the 916 verified leaves:
  - solve: sum 16339.4 s, median 7.08 s, max 286.66 s.
  - check: sum 3499.0 s, median 2.46 s, max 28.02 s.
  - largest LRAT proof: 296 MB (not committed).
- The 12 split cubes cost 3600.2 s of solving that timed out, plus 3925.2 s of march_cu.

Files in `U_L7/`: `top.icnf`, `leaves.icnf`, `open.icnf` and `leaves.jsonl`, copied from the driver's output directory after it ended. No CNF or proof files are committed.

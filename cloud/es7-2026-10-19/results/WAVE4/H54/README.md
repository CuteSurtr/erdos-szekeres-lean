# WAVE4 H54: U3_L (task file tasks/H54.json at 94cc404)

- Case U3_L (U=3, L=none), CASE.cnf sha256 7ab00d97...f823 (matches cases.jsonl); F sha256 69c1dc8f...932d (matches).
- Cubes given: 217 (top.icnf, 217 lines, sha256 84595a53456d51fe79f667479c93fdc5d9c1229d4900edcca2bbcf0ed7fe9730).
- Driver: close_march.py, byte-for-byte copy of WAVE2/F2 (see driver.diff); `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.22`, run 14:39-15:38 UTC, printed `open 0`.
- Verified leaves: 532, each with cake_lpr `s VERIFIED UNSAT` (no cake_lpr heap retries).
  215 given cubes closed directly; 5 cubes split (2 given cubes at depth 25, then 3 of their children at depth 31; march_cu depth 6, 64 sub-cubes each, 0 refuted).
- Cubes still open: 0 (open.icnf is empty).
- Cover: every one of the 217 given cubes is covered by leaves.icnf (checked per top cube with the covercheck.py `cover` function on the leaves restricted to that cube; all lines end in ` 0`). Every leaf extends a given cube.
- Time over the 532 verified leaves: solve sum 8655.3 s, median 12.32 s, max 288.62 s; cake_lpr check sum 1893.6 s, median 2.73 s, max 24.57 s.
  Split cubes: 5 x 300 s solver timeout (1500.1 s) + march_cu 1678.4 s. Total child CPU 53322 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
- Files: U3_L/{top.icnf, leaves.icnf, open.icnf, leaves.jsonl}; env.txt, tools.txt, driver.diff, close_march.py.

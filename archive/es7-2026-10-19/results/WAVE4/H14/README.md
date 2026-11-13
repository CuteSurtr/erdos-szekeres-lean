# WAVE4 H14: case U_L2

Result: all 324 given cubes are closed. No SAT result, no cake_lpr rejection, and no UNSAT_UNCHECKED record.

- Case: U_L2 (U = [], L = [2]). CASE.cnf sha256 1d26b947...f15aaa53 matches cases.jsonl. F sha256 69c1dc8f...ffff932d matches.
- Cubes given: 324 (`results/WAVE4/tasks/H14.json`, commit e0f250b). Written in file order to `U_L2/top.icnf`, top_sha256 ebf0b104...49bf06e.
- Verified leaves: 823. Each one has cake_lpr output exactly `s VERIFIED UNSAT`. 318 of them are given cubes solved directly; the other 505 are sub-cubes.
- Cubes split: 8. Six were given cubes and two were sub-cubes. Each split was `march_cu -d 6` and gave 62–64 children, all closed.
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Cover: every given cube is covered by the leaves. I checked this separately from the driver: each given cube is either a verified leaf, or a split cube whose children (from the SPLIT `subs`) are all covered in the same way. leaves.icnf is exactly the set of verified UNSAT records. Every line in the .icnf files ends in ` 0`.
- Time over the 823 verified leaves:
  - CaDiCaL solve: sum 15167 s, median 10.22 s, max 274.11 s.
  - cake_lpr check: sum 2889 s, median 2.64 s, max 24.58 s.
  - The 8 split cubes also used 2400 s of solver time (300 s timeouts) and 2129 s in march.
  - Total child CPU was 87723 s.
- Wall time: the driver ran from 12:55 to 14:30 UTC, 4 jobs on 4 cores.

Files: `env.txt`, `tools.txt` (tool commits and hashes), `driver.diff` (the driver is an identical copy of WAVE2/F2/close_march.py, sha256 2e0975aa...7c855), `close_march.py`, and `U_L2/{top,leaves,open}.icnf` and `U_L2/leaves.jsonl`.

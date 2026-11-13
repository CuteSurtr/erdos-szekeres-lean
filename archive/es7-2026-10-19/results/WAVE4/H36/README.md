# WAVE4 H36: U_L7 helper

Case U_L7 (U="", L="7", CNF sha256 c6d1c840d97921426e0f2d1d34213fb94293cc1783296ec2357d7883b804f099, matches cases.jsonl).
Task list `results/WAVE4/tasks/H36.json` (commit 4bfd8e7): 196 cubes, written in order to `U_L7/top.icnf` (196 lines).

Driver: `close_march.py` (byte-for-byte copy of WAVE2/F2, sha256 2e0975aa...; see driver.diff), run
13:35:03-14:25:32 UTC with --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.224. Final line: `open 0`.

Result:
- SAT results: none.
- cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
- Verified leaves: 322, all with `s VERIFIED UNSAT` from cake_lpr (`U_L7/leaves.icnf`, 322 lines).
- Cubes split: 2 (each hit the 300 s cap and march_cu -d 6 split it into 64 sub-cubes, 0 refuted).
  The second split cube is one of the sub-cubes of the first. 195 given cubes were closed directly.
  The 196th was closed through the two splits: 63 + 64 = 127 leaves.
- Cubes still open: 0 (`U_L7/open.icnf` is empty).
- Every given cube is covered by my leaves: yes. For each top cube I checked that it is a verified
  leaf, or that it was split and all its sub-cubes are covered, recursively.
- Times over the 322 verified leaves: solve sum 7446.6 s, median 7.73 s, max 300.03 s (that max is a split record).
  cake_lpr check sum 1638.0 s, median 2.88 s, max 31.16 s.
  Solve+check per leaf: sum 8484.6 s, median 10.51 s, max 286.4 s. march_cu splits took 452.8 s and 367.1 s.

Files: env.txt, tools.txt, driver.diff, close_march.py, U_L7/{top.icnf, leaves.icnf, open.icnf, leaves.jsonl}.

# WAVE4 H40: U3_L (mop-up round 2, 1/6)

- Case: U3_L (U=[3], L=[]); case CNF sha256 7ab00d97…f0e823, which matches cases.jsonl. F sha256 69c1dc8f…ffff932d, which matches.
- Cubes given: 191 (`tasks/H40.json` at 3ed048e). `U3_L/top.icnf` has 191 lines (sha256 0bf20507…6438e1).
- Driver: `close_march.py`, a byte-for-byte copy of WAVE2/F2 (see driver.diff). Run with `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.15` from 14:18 to about 15:12 UTC, when it ended with `open 0`.
- Verified leaves: 380, each with cake_lpr `s VERIFIED UNSAT` (`U3_L/leaves.icnf`).
- Cubes split: 3. Two given cubes (length 25) timed out at 300 s and were split by march_cu -d 6 into 64 sub-cubes each. One of those sub-cubes (length 31) timed out as well and was split into 64 more. No march output had refuted cubes.
- Cubes still open: 0 (`U3_L/open.icnf` is empty).
- Cover: I checked this separately from leaves.jsonl. All 191 given cubes are covered by my verified leaves: each given cube, or else every child of its splits, recursively, contains a leaf of leaves.icnf as a subset.
- Solve time over the 380 UNSAT leaves: sum 5910.7 s, median 7.45 s, max 246.35 s. The 3 split cubes took about 300 s each to time out, plus 196–234 s of march.
- cake_lpr check time: sum 1507.5 s, median 2.92 s, max 23.99 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
- Tools: see tools.txt (CaDiCaL 3.0.1 c6073042, march_cu CnC 705b60c6 with -fcommon, cake_lpr a36874a8).

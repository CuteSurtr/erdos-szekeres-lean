# WAVE4 H46: case U_L2 (mop-up round 2, list 1 of 3)

- Case: U_L2 (CNF sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53, matches cases.jsonl; F sha256 69c1dc8f... checked).
- Cubes given: 151 (`results/WAVE4/tasks/H46.json` at 3ed048e), written in order to `U_L2/top.icnf` (151 lines, sha256 cac3f9fa21f63c6972672e2c2cf76f578587624d6a45684758707489ab1e7403).
- Driver: `close_march.py`, a byte-for-byte copy of WAVE2/F2 (see driver.diff). Ran 14:17:34-14:47 UTC with `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.15`. It printed `open 0`.
- Verified leaves: 212. Every UNSAT record has cake_lpr `s VERIFIED UNSAT`.
- Cubes split: 1 (top cube index 41, timed out at 300 s; march_cu -d 6 gave 62 sub-cubes ("number of cubes 62, including 2 refuted"), all 62 closed by verified leaves).
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Cover: all 151 given cubes are covered by my leaves (each top cube is a verified leaf, or its split children all are; checked from leaves.icnf, top.icnf and the SPLIT record in leaves.jsonl).
- Solve time over the 212 leaves: sum 2954.3 s, median 8.51 s, max 190.83 s (plus 300.01 s for the one timed-out cube and 368.5 s for its split). cake_lpr check time: sum 728.8 s, median 2.67 s, max 18.03 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.
- Tools: tools.txt (CaDiCaL 3.0.1 c6073042, march_cu 705b60c6 with -fcommon, cake_lpr a36874a8; bundled example prints `s VERIFIED UNSAT`).

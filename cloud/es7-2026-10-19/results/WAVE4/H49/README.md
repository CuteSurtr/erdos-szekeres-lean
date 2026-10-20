# WAVE4 H49 (mop-up round 2, U_L7)

- Case: U_L7 (case CNF sha256 c6d1c840d97921426e0f2d1d34213fb94293cc1783296ec2357d7883b804f099, matches cases.jsonl).
- Cubes given: 136 (`tasks/H49.json` at 3ed048e), written in order to `U_L7/top.icnf` (136 lines).
- SAT results: none.
- cake_lpr rejections / UNSAT_UNCHECKED records: none. All 604 UNSAT records have `cake_lpr: "s VERIFIED UNSAT"`.
- Verified leaves: 604 (`U_L7/leaves.icnf`).
- Cubes split: 8 (each timed out at 300 s; march_cu -d 6 gave 49-64 sub-cubes each, 516 in total, 13 of them refuted by march; every sub-cube was solved and checked).
- Cubes still open: 0 (`U_L7/open.icnf` is empty; the driver printed `open 0`).
- Every given cube is covered: yes. Checked from leaves.jsonl: each of the 136 top cubes is either a verified leaf or a SPLIT whose sub-cubes are all (recursively) covered by verified leaves.
- Time on verified leaves: solve sum 8829 s, median 6.0 s, max 250.2 s; check sum 2209 s, median 2.4 s, max 29.3 s; solve+check sum 11038 s, median 8.7 s, max 279.6 s. The 8 split cubes used 2400 s of timed-out solving plus march time (5505 s with splitting).
- Run: driver started 14:17 UTC with --hours 2.212 and --jobs 4, finished at about 15:26 UTC with all cubes closed.
- Tools and checks: `tools.txt`, `driver.diff`, `env.txt`. `close_march.py` is a byte-for-byte copy of `results/WAVE2/F2/close_march.py`.

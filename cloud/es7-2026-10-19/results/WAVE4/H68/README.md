# WAVE4 H68: U_L7 mop-up round 4 (1/3)

Case U_L7 (U = [], L = [7]); case CNF sha256 c6d1c840d97921426e0f2d1d34213fb94293cc1783296ec2357d7883b804f099 (matches cases.jsonl). Task list `results/WAVE4/tasks/H68.json` (commit 1d3a72c).

- Cubes given: 125 (top.icnf, 125 lines, sha256 0c4a27c6f66aa21e7a8bde8e0b25cc88c3e17289eabe98d2742036d5adb6fc2c).
- Verified leaves: 235 (every one with cake_lpr `s VERIFIED UNSAT`), listed in `U_L7/leaves.icnf`.
- Cubes split: 2 (CaDiCaL 300 s timeout; march_cu -d 6 gave 61 and 51 sub-cubes, all closed).
- Cubes still open: 0 (`U_L7/open.icnf` is empty).
- Every given cube is covered by my leaves: yes (checked: each top cube has a leaf that is a subset of it, or is split and every child is covered).
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record.
- Solve time over the 235 leaves: sum 2403.2 s, median 4.82 s, max 193.01 s (plus 2 x 300 s timeouts on the split cubes and 1004 s of march_cu splitting).
- Check time (cake_lpr): sum 876.5 s, median 2.64 s, max 25.1 s.
- Driver ran 15:07:26-15:29 UTC with 4 jobs (`close_march.py`, byte-identical to WAVE2/F2, see driver.diff). Tools in tools.txt, environment in env.txt.

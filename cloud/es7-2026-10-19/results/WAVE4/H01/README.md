# WAVE4 H01: U_L2

Task: close the 325 open cubes of hull case U_L2 listed in `results/WAVE4/tasks/H01.json` (committed at e0f250b).

- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT record, no cake_lpr heap retry.
- Case CNF: `hullsplit.py case F.cnf "" "2"`, sha256 1d26b947...f3aaa53 = cases.jsonl. F sha256 69c1dc8f...ffff932d.
- Driver: `close_march.py`, a byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see `driver.diff`), run with
  `--top top.icnf --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.221`, output outside the checkout.
  Started 12:53:07 UTC, ended about 14:47 UTC with `open 0` (one run, no resume).
- Tools: `tools.txt` (CaDiCaL 3.0.1 c6073042, march_cu CnC 705b60c6 with -fcommon, cake_lpr a36874a8; example verified).

## Results (`U_L2/`)
- Cubes given: 325 (`U_L2/top.icnf`, sha256 5006dbcc...68382, same order as the task list).
- Verified leaves: 888 (`U_L2/leaves.icnf`), each with cake_lpr printing exactly `s VERIFIED UNSAT`.
  319 of the given cubes were closed directly.
- Cubes split: 9 (6 given cubes plus 3 of their sub-cubes; march_cu -d 6 gave 63, 62, 64, 64, 64, 64, 64, 64, 63
  sub-cubes, 4 of them march-refuted, which were still solved and checked as leaves).
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Cover: every given cube is covered by the verified leaves (`final_check.py`: for each given cube, the leaves
  consistent with it, restricted to it, cover all assignments; 0 uncovered). All icnf lines end in ` 0`.
- Time over the 888 verified leaves: CaDiCaL solve sum 17304.0 s, median 11.38 s, max 268.08 s;
  cake_lpr check sum 3416.3 s, median 2.84 s, max 27.88 s. The 9 split cubes used 2700.2 s of timed-out solving and
  2187.7 s of march_cu. Largest LRAT proof 191.9 MB (not committed).

# WAVE4 H19: U_L6

- Task: `results/WAVE4/tasks/H19.json` at e0f250b; case U_L6 (U = [], L = [6]); CASE.cnf sha256
  741c7fe0917c292eb9401859b03204fd879df0b38a737819360924e44a105424 (matches cases.jsonl);
  F.cnf sha256 69c1dc8f...932d (matches).
- Cubes given: 196 (`U_L6/top.icnf`, 196 lines, file order).
- Driver: `close_march.py` = byte copy of `results/WAVE2/F2/close_march.py` (see driver.diff); tools in tools.txt.
  Run 12:55:58 to 13:34:33 UTC with `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.224`;
  it ended by itself with `open 0`.
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record.
- Verified leaves: 316 (each with cake_lpr `s VERIFIED UNSAT`; `U_L6/leaves.icnf` equals the set of
  verified records in `U_L6/leaves.jsonl`, no duplicates, every line ends in ` 0`).
  194 given cubes closed directly; 2 timed out (300 s) and were split by march_cu -d 6
  into 62 (2 refuted by march) and 60 (3 refuted by march) sub-cubes, all of which were closed.
- Cubes still open: 0 (`U_L6/open.icnf` is empty).
- Cover: every given cube is either a verified leaf or a split cube whose march_cu sub-cubes are all
  verified leaves (196/196). The 5 cubes march_cu refuted during the two splits are not in
  leaves.icnf, as in waves 1-3; the cover re-check must account for them.
- Times (318 solver runs incl. the 2 timeouts; 316 checks):
  solve sum 6290.0 s, median 9.39 s, max 300.02 s;
  cake_lpr check sum 1268.9 s, median 2.85 s, max 24.15 s.

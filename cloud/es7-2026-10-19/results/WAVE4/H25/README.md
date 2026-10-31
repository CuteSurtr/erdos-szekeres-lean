# WAVE4 H25: case U3_L

Task file `results/WAVE4/tasks/H25.json` at e0f250b: case U3_L, 317 cubes (top.icnf, 317 lines).
CASE.cnf sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823 (matches cases.jsonl);
F.cnf sha256 69c1dc8f...ffff932d (matches). Driver: close_march.py, byte copy of WAVE2/F2 (see driver.diff),
run 13:10-15:19 UTC with --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.23.

Results (U3_L/leaves.jsonl):
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED, no TIMEOUT record.
- Verified leaves (cake_lpr `s VERIFIED UNSAT`): 525 (leaves.icnf, 525 lines).
- Cubes split: 32 (31 given top cubes + 1 sub-cube), 2048 sub-cubes created.
- Given cubes: 286 closed directly by a verified leaf, 2 covered via their split sub-cubes,
  29 still open. Every given cube was attempted (solved or split); not every given cube is covered.
- Cubes still open: 1808 (open.icnf), all of them sub-cubes of the 29 open given cubes that the
  driver did not reach before its deadline. I recomputed the frontier from leaves.jsonl and it
  equals open.icnf exactly.
- Solve time over verified leaves: sum 11185.8 s, median 10.98 s, max 271.13 s.
- Check time (cake_lpr): sum 2156.7 s, median 2.75 s, max 24.11 s.

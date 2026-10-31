# WAVE4 H55: U3_L

Task: `results/WAVE4/tasks/H55.json` (committed at 94cc404), case U3_L, 217 cubes (all of depth 25).
Run by TASK.md (e0f250b) with the byte-for-byte copy of `results/WAVE2/F2/close_march.py`
(see `driver.diff`, `tools.txt`, `env.txt`).

- Case CNF: `hullsplit.py case F.cnf 3 ""`, sha256 7ab00d97…f823, matches cases.jsonl. F sha256 matches.
- top.icnf: 217 lines = 217 cubes of the task list, in its order (sha256 dcae63bd…557e).
- Driver: `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.2`, started 2026-10-20T14:39:16Z,
  ended 15:01:36Z with `open 0` (all cubes closed well before the deadline).

Results (`U3_L/`):
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record.
- Verified leaves: 280, each with cake_lpr `s VERIFIED UNSAT` (`leaves.icnf`, 280 lines, all well formed).
- Cubes split: 1 (a depth-25 cube that hit the 300 s cap; march_cu -d 6 gave 64 sub-cubes, 0 refuted;
  all 64 closed).
- Cubes still open: 0 (`open.icnf` is empty).
- Cover: every one of the 217 given cubes is covered by my leaves (216 are leaves themselves; the split
  one is covered by its 64 verified children). Checked by rebuilding the tree from leaves.jsonl.
- Solve time (CaDiCaL wall, 280 UNSAT leaves): sum 3651.6 s, median 9.8 s, max 146.8 s
  (plus 300.0 s for the split cube's timeout).
- Check time (cake_lpr wall, 280 leaves): sum 1177.0 s, median 3.4 s, max 17.5 s.
- Solve + check per leaf: sum 4828.6 s, median 13.8 s, max 164.3 s.

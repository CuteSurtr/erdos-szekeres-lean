# WAVE4 H27: case U_L7

Task: the 194 cubes in `results/WAVE4/tasks/H27.json` (at e0f250b), case U_L7 (U = {}, L = {7}).

- Case CNF from hullsplit.py: sha256 c6d1c840…f099, equal to cases.jsonl. F sha256 69c1dc8f…932d.
- top.icnf: 194 lines in the task file's order (sha256 921d2acb13c38135dd6a34f726941658b84375c15a71adf4a357c1a731a96438).
- Driver: `close_march.py`, a byte-for-byte copy of WAVE2/F2 (see `driver.diff`), with `--timeout 300 --split-depth 6 --jobs 4`.
  It ran from 13:23:01 to 13:51 UTC.

Results:
- Cubes given: 194
- Verified leaves: 194. Each is a given cube solved directly by CaDiCaL, and cake_lpr printed `s VERIFIED UNSAT` on every proof.
- Cubes split: 0
- Cubes still open: 0 (`open.icnf` is empty)
- Covered: yes. leaves.icnf equals the given list as a set, so every given cube is covered by its own leaf.
- Solve time: sum 5229.1 s, median 13.04 s, max 253.98 s
- Check time (cake_lpr): sum 1150.7 s, median 4.78 s, max 23.52 s. No heap retries were needed. The largest proof was 178 MB.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

Files: `U_L7/{top.icnf, leaves.icnf, open.icnf, leaves.jsonl}`, `env.txt`, `tools.txt`, `driver.diff`, `close_march.py`.

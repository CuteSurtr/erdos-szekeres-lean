# WAVE4 H03 — case U_L2

Task file `results/WAVE4/tasks/H03.json` (commit e0f250b): case **U_L2** (U = {}, L = {2}), **325 cubes**.
Case CNF sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53 (matches cases.jsonl);
F.cnf sha256 69c1dc8f…f932d (matches). top.icnf = the 325 cubes in file order (325 lines, all distinct),
sha256 9dc6cedaa170ae1dac155701799f418aaeecc46fb0c90d263480b1dd107f76a4.

Driver: `close_march.py` (byte copy of WAVE2/F2, see driver.diff), `--depth 7 --timeout 300 --split-depth 6
--jobs 4 --hours 2.213`, started 12:53:32 UTC, ended 14:31 UTC with `open 0` (all cubes closed before the deadline).
Tools: tools.txt; environment: env.txt (4 cores, 15 GB).

Results (U_L2/leaves.jsonl, leaves.icnf, open.icnf, top.icnf):
- **No SAT result.** No cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT record.
- Verified leaves: **763** (every one with cake_lpr `s VERIFIED UNSAT`; leaves.icnf has 763 distinct lines).
- Cubes split: **7** (300 s timeouts; march_cu -d 6 gave 64, 62, 64, 63, 64, 64, 64 sub-cubes); no sub-cube needed a further split.
- Cubes still open: **0** (open.icnf is empty).
- Cover: every one of the 325 given cubes is covered by the leaves in leaves.icnf (checked with an independent
  recursive split check over leaves.icnf and top.icnf).
- Solve time (770 CaDiCaL runs, incl. the 7 timeouts): sum 14848 s, median 9.95 s, max 300.03 s;
  UNSAT runs only: sum 12748 s, median 9.91 s, max 230.23 s.
- Check time (763 cake_lpr runs): sum 2900 s, median 2.87 s, max 23.69 s.
- march_cu split time: 200.5, 384.6, 98.2, 601.2, 383.7, 314.3, 230.4 s.

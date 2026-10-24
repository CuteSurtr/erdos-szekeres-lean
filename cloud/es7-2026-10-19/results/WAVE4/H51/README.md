# WAVE4 H51: case U3_L

Task file `results/WAVE4/tasks/H51.json` (commit 94cc404), TASK.md at e0f250b. Budget 1.5 h; 4 cores.

- Case: U3_L (U=3, L=empty), case CNF sha256 7ab00d97…f823 (matches cases.jsonl); F sha256 69c1dc8f…932d.
- Cubes given: 218 (all depth 25), written to `U3_L/top.icnf` in file order (218 lines).
- Verified leaves: 218 (every one with cake_lpr `s VERIFIED UNSAT`).
- Cubes split: 0. Cubes still open: 0 (`U3_L/open.icnf` is empty).
- Cover: every given cube is covered by a verified leaf (each leaf equals its top cube; checked by subset test, all lines well formed).
- Solve time (CaDiCaL, wall): sum 3632.9 s, median 11.0 s, max 291.2 s.
- Check time (cake_lpr): sum 1039.3 s, median 4.2 s, max 23.7 s.
- No SAT result, no cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT.
- Driver run 14:38:35 to 14:58 UTC (`--hours 1.222`); output directory /opt/work/out/U3_L outside the checkout.

Files: `env.txt`, `tools.txt`, `close_march.py` (byte-identical copy of WAVE2/F2), `driver.diff`,
`U3_L/{top.icnf,leaves.icnf,open.icnf,leaves.jsonl}`.

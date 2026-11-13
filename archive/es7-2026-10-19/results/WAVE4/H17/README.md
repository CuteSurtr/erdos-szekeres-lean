# WAVE4 H17: case U_L2

- Task: `results/WAVE4/tasks/H17.json` (at e0f250b), case **U_L2**, **324 cubes** given (top.icnf, 324 lines, sha256 1d2444f9d0530207b849d2e071e3a0ea94a006533ae1c850eb17ab35f41cbbb6).
- Case CNF sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53 (matches cases.jsonl); F sha256 69c1dc8f…932d (matches).
- Driver: byte-for-byte copy of `results/WAVE2/F2/close_march.py` (see driver.diff), `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.22`; ran 12:55:35 to 13:32:29 UTC (about 37 min wall time) and ended with `open 0`.

Results (U_L2/leaves.jsonl):
- **No SAT result.** No cake_lpr rejection and no UNSAT_UNCHECKED record.
- Verified leaves: **387** (each with cake_lpr `s VERIFIED UNSAT`); `U_L2/leaves.icnf` has 387 lines.
- Cubes split: **1** (a 19-literal top cube timed out at 300 s; march_cu -d 6 gave 64 sub-cubes, 0 refuted, split time 82.8 s; all 64 were closed).
- Cubes still open: **0** (`U_L2/open.icnf` is empty).
- Cover: every one of the 324 given cubes is covered by the verified leaves. An independent re-check found that each top cube contains a leaf, or was split and all its sub-cubes contain a leaf. Every icnf line was checked to end in ` 0`.
- Solve time over verified leaves: sum 6178.8 s, median 11.83 s, max 228.4 s (+ 300.02 s for the one timed-out cube).
- cake_lpr check time: sum 1744.8 s, median 3.94 s, max 20.65 s.

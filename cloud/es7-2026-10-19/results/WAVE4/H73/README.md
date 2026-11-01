# WAVE4 H73: U3_L

- Case: U3_L (case CNF sha256 7ab00d97d5047e0003bd8d254560dc8464d880d7165c6d7f0e01fab79ee0f823, matches cases.jsonl).
- Cubes given: 207 (results/WAVE4/tasks/H73.json, committed at 754b984; top.icnf has 207 lines).
- Driver: close_march.py (byte-identical copy of WAVE2/F2), started 2026-10-20T15:19:17Z with --hours 1.2,
  --depth 7 --timeout 300 --split-depth 6 --jobs 4. Ended about 15:44 UTC with "open 0".
- Verified leaves: 269. Each has cake_lpr "s VERIFIED UNSAT", and leaves.icnf equals the set of verified UNSAT records in leaves.jsonl.
- Cubes split: 1 (it timed out at 300 s; march_cu split it into 63 sub-cubes, 1 of them refuted by march, in 378.6 s). All 63 children are closed.
- Cubes still open: 0 (open.icnf is empty).
- Cover: all 207 given cubes are covered by these leaves. Each cube has a verified leaf whose literals are a subset of the cube's, or it was split and every parent+sub cube is covered in turn. Checked by a script over leaves.jsonl.
- Solve time over the 269 leaves: sum 3066.6 s, median 6.46 s, max 191.59 s (the split cube's 300 s timeout is not included).
- cake_lpr check time: sum 928.8 s, median 2.58 s, max 19.52 s.
- No SAT result. No cake_lpr rejection. No UNSAT_UNCHECKED record.

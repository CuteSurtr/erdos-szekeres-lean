# WAVE3 G17: open cubes of U_L9

Task `results/WAVE3/tasks/G17.json` (commit 9a26cc2): case U_L9, 64 open cubes (each 7 literals).
Run 2026-10-20, 11:20 to 11:44 UTC, 4 cores (`env.txt`). Tools and hashes are in `tools.txt`.
The driver `close_march.py` is the WAVE2/F2 driver, copied unchanged. The review is in `driver.diff`.

| case | cubes given | verified leaves | cubes still open | every given cube covered | SAT | cake_lpr rejections |
|---|---|---|---|---|---|---|
| U_L9 | 64 | 127 | 0 | yes (closed) | none | none |

- Case CNF sha256 887d573e…928fb4 matches cases.jsonl. F sha256 69c1dc8f…ffff932d.
- `top.icnf` holds the 64 given cubes, in the file's order (sha256 4b3a486b…bc04).
- 63 given cubes were solved directly. One cube hit the 300 s cap and was split by `march_cu -d 6` into 64 sub-cubes (0 refuted). All 64 sub-cubes were then solved.
- Every one of the 127 UNSAT leaves got `s VERIFIED UNSAT` from cake_lpr. No result was SAT, UNSAT_UNCHECKED or TIMEOUT.
- Time:
  - CaDiCaL: 2548 s wall over the 127 leaves, plus 300 s on the cube that timed out.
  - cake_lpr: 656 s.
  - march split: 132 s.
  - Wall clock: about 24 min.
  - Largest LRAT proof: 214 MB (not committed).
- Cover check: `cover_g17.py` is my own case-splitting checker. It rejects lines that do not end in ` 0`. It reports that all 64 given cubes are covered by `leaves.icnf`. As a mutation test, removing one leaf makes it report 1 cube not covered.
- `open.icnf` is empty. `leaves.jsonl` starts with `{"case": "U_L9", "case_sha256": …}`.

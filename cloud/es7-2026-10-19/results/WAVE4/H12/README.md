# WAVE4 H12: case U_L2

Task file `results/WAVE4/tasks/H12.json` at e0f250b (unchanged at the checked-out head): case U_L2, 324 open cubes.
Machine: 4 cores, 15 GB (`env.txt`). Tools and hashes: `tools.txt`. Driver: byte-for-byte copy of
`results/WAVE2/F2/close_march.py` (`driver.diff`).

- F.cnf sha256 69c1dc8f…ffff932d and U_L2 case CNF sha256 1d26b947…3f15aaa53 both match.
- `top.icnf`: the 324 cubes in file order (324 lines), sha256 f2e831c8…6e595f.
- Run: `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.225`, 12:54 to 13:23 UTC on 2026-10-20.

Result:
- Cubes given: 324.
- Verified leaves: 324 (every cube solved directly by CaDiCaL; cake_lpr printed `s VERIFIED UNSAT` on all 324 LRAT proofs).
- Cubes split: 0. Cubes still open: 0 (`open.icnf` is empty).
- Every given cube is covered by a leaf (the leaves are exactly the 324 given cubes).
- No SAT result, no cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT.
- CaDiCaL solve time: sum 4934.7 s, median 11.96 s, max 175.49 s.
- cake_lpr check time: sum 1414.7 s, median 4.03 s, max 19.86 s. Largest proof 134 MB (not committed).

Files in `U_L2/`: `top.icnf`, `leaves.icnf` (324), `open.icnf` (empty), `leaves.jsonl` (first record names the case and its sha256).

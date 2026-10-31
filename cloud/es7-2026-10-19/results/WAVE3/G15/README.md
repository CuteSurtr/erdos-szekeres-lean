# G15: wave 3, close the open cubes of U_L7 (tasks/G15.json @ 9a26cc2)

Run 2026-10-20 10:56-11:45 UTC on one cloud VM, 4 cores, 15 GB (`env.txt`). Branch es7-cloud.

**Result: every given cube of U_L7 is covered by verified leaves. Nothing is open. No SAT. No cake_lpr rejection.**

| case | cubes given | verified leaves | splits | cubes still open | every given cube covered |
|---|---|---|---|---|---|
| U_L7 | 64 | 252 | 3 | 0 | **yes** |

Time (from `leaves.jsonl`): CaDiCaL 6206 s total (the 3 split cubes hit the 300 s cap), cake_lpr 1065 s,
march_cu splits 728 s; wall time 10:59-11:42 UTC with `--jobs 4`. Largest LRAT proof 236 MB (not committed).

## Setup
- Tools (`tools.txt`): CaDiCaL c6073042 (3.0.1), march_cu CnC 705b60c6 (`-fcommon`), cake_lpr a36874a8
  (the bundled example gives `s VERIFIED UNSAT`, cake_lpr.S sha256 2f3af32d...).
- F regenerated (gen_etv.py + mirgen.py --interior --yflip-unit): sha256 69c1dc8f...f932d, matches.
- U_L7 case CNF (`hullsplit.py case F "" "7"`): sha256 c6d1c840...04f099, matches cases.jsonl.
- Driver `close_march.py` = byte-identical copy of WAVE2/F2/close_march.py; what I checked is in `driver.diff`
  (fresh mkdtemp per job, atomic leaves.icnf/open.icnf, `case`/`case_sha256` first record, a leaf only on the
  exact line `s VERIFIED UNSAT`).
- Run: `close_march.py U_L7.cnf G15/U_L7 --name U_L7 --top <64 cubes of G15.json in file order>
  --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.7`. `U_L7/top.icnf` is that given-cube file
  (sha256 9e65c648...a060d).

## Splits
Three cubes timed out at 300 s and were split by march_cu -d 6 on case CNF + cube: one top cube (64 sub-cubes),
then two 13-literal sub-cubes (64 sub-cubes; 63 sub-cubes, 1 refuted by march). All sub-cubes were then
solved and verified.

## Checks after the run
- `leaves.icnf` has 252 distinct lines, all of the form `a ... 0`, and is exactly the set of
  `leaves.jsonl` records with status UNSAT and `cake_lpr == "s VERIFIED UNSAT"`.
- My own cover check (branching on leaf literals, independent of the driver's frontier code) shows that
  each of the 64 given cubes is covered by the leaves. `open.icnf` is empty.
- No SAT and no UNSAT_UNCHECKED records.

## Files
`U_L7/leaves.icnf` (verified leaves, full cubes over F's variables), `U_L7/leaves.jsonl` (all records),
`U_L7/open.icnf` (empty), `U_L7/top.icnf` (the given cubes), `close_march.py`, `driver.diff`, `tools.txt`,
`env.txt`. No CNF or LRAT files are committed.

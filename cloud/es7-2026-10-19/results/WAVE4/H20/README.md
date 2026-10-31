# WAVE4 H20: U_L6

- Case: U_L6 (CASE.cnf sha256 741c7fe0917c292eb9401859b03204fd879df0b38a737819360924e44a105424, matches cases.jsonl).
- Cubes given: 196 (tasks/H20.json at e0f250b; U_L6/top.icnf has 196 lines, identical to the list).
- Driver: close_march.py (byte copy of WAVE2/F2, see driver.diff), --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.207,
  started 2026-10-20 12:57:13 UTC, ended by itself at about 13:30 UTC with `open 0`.
- Verified leaves: 257, every one with cake_lpr `s VERIFIED UNSAT` (no cake_lpr retry needed).
- Cubes split: 1 (a 25-literal top cube timed out at 300 s; march_cu -d 6 gave 62 sub-cubes, 2 of them refuted by march; all 62 closed).
- Cubes still open: 0 (U_L6/open.icnf is empty).
- Cover: every given cube is covered by the leaves: 195 top cubes are themselves leaves, and the split cube's 62 children are all leaves.
- Solve time (CaDiCaL, 257 UNSAT leaves): sum 4188.7 s, median 10.69 s, max 210.32 s (plus 300.01 s for the one timeout, and 534.4 s march split).
- Check time (cake_lpr): sum 1179.9 s, median 3.62 s, max 25.62 s. Solve+check per leaf: sum 5368.6 s, median 14.41 s, max 235.94 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none. TIMEOUT records: none.

Files: U_L6/leaves.icnf, open.icnf, top.icnf, leaves.jsonl copied from /opt/work/out/U_L6 after the driver ended.

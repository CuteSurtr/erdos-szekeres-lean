# WAVE4 H22: case U_L6

Task: close the 196 cubes in `results/WAVE4/tasks/H22.json` (committed at e0f250b), case U_L6
(CASE.cnf sha256 741c7fe0917c292eb9401859b03204fd879df0b38a737819360924e44a105424, matches cases.jsonl).

Result: every given cube is closed directly. No SAT result, no cake_lpr rejection, no UNSAT_UNCHECKED record.

- cubes given: 196 (top.icnf, sha256 e05cc94bf25a578ee054e1a495495faf01168d19659783d5e68cb963ee79916c)
- verified leaves: 196 (each with cake_lpr `s VERIFIED UNSAT`); leaves.icnf = the 196 given cubes
- cubes split: 0 (no cube hit the 300 s cap)
- cubes still open: 0 (open.icnf is empty)
- every given cube is covered by the leaves: yes (each leaf is a given cube itself)
- CaDiCaL solve time: sum 3472.9 s, median 13.3 s, max 229.3 s
- cake_lpr check time: sum 993.1 s, median 4.2 s, max 30.3 s
- largest LRAT proof: 222.6 MB (not committed)

Run: driver started 2026-10-20 12:56:25 UTC with --jobs 4 --hours 2.22 and ended about 13:25 UTC
with `open 0`. Tools, hashes and driver check: `tools.txt`, `driver.diff`, `env.txt`.
Files in `U_L6/`: leaves.icnf, open.icnf, top.icnf, leaves.jsonl, copied from /opt/work/out/U_L6 after the driver ended.

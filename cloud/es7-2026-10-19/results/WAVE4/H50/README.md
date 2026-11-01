# WAVE4 H50: case U_L6 (mop-up round 2)

- Case: U_L6 (CNF sha256 741c7fe0917c292eb9401859b03204fd879df0b38a737819360924e44a105424, matches cases.jsonl).
- Cubes given: 189 (`results/WAVE4/tasks/H50.json` at 3ed048e; `U_L6/top.icnf`, sha256 a54c3002…00bc).
- Driver: `close_march.py` (byte copy of WAVE2/F2), `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.15`,
  started 14:21:09 UTC, ended 14:32 UTC (printed `open 0`).
- Verified leaves: 189. Every leaf is a given top cube itself; every one has cake_lpr `s VERIFIED UNSAT`.
- Cubes split: 0. Cubes still open: 0 (`U_L6/open.icnf` is empty).
- Every given cube is covered by my leaves: yes (`leaves.icnf` equals `top.icnf` as a set of lines).
- Solve time (CaDiCaL, wall): sum 1984.4 s, median 1.83 s, max 153.1 s.
- Check time (cake_lpr): sum 703.9 s, median 2.55 s, max 20.68 s. Solve+check: sum 2688.3 s, median 4.8 s, max 173.8 s.
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no heap retry, no TIMEOUT.

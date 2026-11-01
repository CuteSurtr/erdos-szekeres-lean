# WAVE4 H56 — U_L2 (mop-up round 3)

- Case: U_L2 (CASE.cnf sha256 1d26b947…aa53, matches cases.jsonl). Task list `tasks/H56.json` at 94cc404: 215 cubes (depth 37), written in order to `U_L2/top.icnf` (215 lines).
- Driver: `close_march.py`, byte-for-byte copy of WAVE2/F2 (see driver.diff), run with
  `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.2`, started 14:38:45 UTC, finished about 15:01 UTC (`open 0`).
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT record.
- Verified leaves: 278 (every one `s VERIFIED UNSAT` from cake_lpr): 214 of the given cubes directly, plus 64 children of the one split cube.
- Cubes split: 1 (a given cube timed out at 300 s; march_cu -d 6 gave 64 sub-cubes, 1 refuted by march; all 64 closed by CaDiCaL + cake_lpr).
- Cubes still open: 0 (`U_L2/open.icnf` is empty).
- Cover: every one of the 215 given cubes is covered by the verified leaves in `U_L2/leaves.icnf` (checked by walking each cube and its SPLIT children against leaf subsets; every leaves.icnf line ends in ` 0`).
- Solve time over the 278 verified leaves: sum 3091.5 s, median 7.46 s, max 93.01 s (plus 300.02 s for the split cube and 309.2 s for its march split).
- Check time (cake_lpr): sum 968.2 s, median 2.97 s, max 14.49 s.

# C2P M06 (LIST=C2P.tsv, j=6, N=42, H=3.0, TASK.md at 01909a07)

Restart of M06: the earlier attempt (TASK.md at fb2c59af) stopped at step 1, so its files were replaced.
Start 2026-10-31 03:22:45Z, END 06:07:45Z (`run.sh`); the lane ran 03:35–06:00Z and stopped with 431 s left.

## Tools and checks (`tools.txt`)

- Built with `vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check from drat-trim 2e3b2dc with the E2 patch.
- Sanity: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, both sha256 match. Cubes P1..P8: byte-identical.

## Units (`units.tsv`, idx ≡ 6 mod 42: 54 units, 46 H at cap 1800 s, 8 Q at cap 2400 s, no cover)

Certified 10, timed out (UNKNOWN) 1 (P8_2-12, Q, at 2384 s), not reached 43, errors 0.

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P8 | H | 5 | 5 | 0 | 0 | 0 |
| P8 | Q | 1 | 0 | 1 | 0 | 0 |
| P7 | H | 5 | 4 | 0 | 1 | 0 |
| P7 | Q | 1 | 1 | 0 | 0 | 0 |
| P6 | H | 6 | 0 | 0 | 6 | 0 |
| P6 | Q | 1 | 0 | 0 | 1 | 0 |
| P5 | H | 6 | 0 | 0 | 6 | 0 |
| P5 | Q | 1 | 0 | 0 | 1 | 0 |
| P4 | H | 5 | 0 | 0 | 5 | 0 |
| P4 | Q | 2 | 0 | 0 | 2 | 0 |
| P3 | H | 6 | 0 | 0 | 6 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 |
| P2 | H | 5 | 0 | 0 | 5 | 0 |
| P2 | Q | 2 | 0 | 0 | 2 | 0 |
| P1 | H | 6 | 0 | 0 | 6 | 0 |
| P1 | Q | 1 | 0 | 0 | 1 | 0 |
| **all** | | 54 | 10 | 1 | 43 | 0 |

Certified units (min / median / max), n=10:

- solve s: 21.6 / 232.8 / 1408.7
- lrat-check s: 11.5 / 46.0 / 71.8
- cake_lpr s: 98.7 / 270.3 / 386.7
- proof size GB: 0.22 / 3.21 / 5.02

Largest solver RSS: 4411 MB (P8_3-9-16); cake_lpr heap 8000 MB for every check.

| unit | kind | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P8_3-15-16 | H | UNSATISFIABLE (certified) | 215.55 | 46.1 | 271.5 | 3.18 | 4351 |
| P8_2-4-5 | H | UNSATISFIABLE (certified) | 22.96 | 11.5 | 104.3 | 0.22 | 2648 |
| P8_4-11-13 | H | UNSATISFIABLE (certified) | 283.97 | 48.3 | 279.8 | 3.3 | 4361 |
| P8_2-12 | Q | UNKNOWN | 2384.05 | - | - | - | 4375 |
| P8_3-5-9 | H | UNSATISFIABLE (certified) | 207.22 | 44.7 | 266.7 | 3.2 | 4362 |
| P8_3-9-16 | H | UNSATISFIABLE (certified) | 411.85 | 50.4 | 296.2 | 3.62 | 4411 |
| P7_2-11-12 | H | UNSATISFIABLE (certified) | 255.71 | 45.9 | 276.4 | 3.25 | 4361 |
| P7_2-3-9 | H | UNSATISFIABLE (certified) | 209.4 | 44.6 | 263.9 | 3.19 | 4398 |
| P7_2-12-14 | H | UNSATISFIABLE (certified) | 249.98 | 46.1 | 269.1 | 3.22 | 4364 |
| P7_1-3-4 | H | UNSATISFIABLE (certified) | 21.6 | 11.5 | 98.7 | 0.22 | 2648 |
| P7_10-14 | Q | UNSATISFIABLE (certified) | 1408.72 | 71.8 | 386.7 | 5.02 | 4358 |

Not reached, in order: P7_3-8-15 and every P6..P1 unit of `units.tsv`.

## Problems

- No SAT (`/opt/work/SAT_FOUND` never appeared). No proof rejection: every UNSAT proof was accepted by both checkers.
  No record with `"certified": false` or an ERROR status. No memory problem (solver RSS at most ~4.4 GB).
- Process notes: about 12 minutes were lost at step 1 because the first base CNF run was wrapped in `/usr/bin/time`,
  which is not installed here; it was re-run without it. One push hit a transient HTTP 403 and succeeded on retry.

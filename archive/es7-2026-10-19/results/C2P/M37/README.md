# C2P M37 (LIST C2P.tsv, j = 37, N = 42, H = 3.0, TASK.md at 01909a07)

This run replaces an earlier attempt (TASK.md at fb2c59af) that stopped at step 1 because the tool build was blocked.
Start 03:22:45Z, lane END 06:07:45Z (start + 3 h − 15 min). The lane ran from 03:24:55Z and stopped at 05:55:16Z,
when 748 s were left (it starts no unit with under 15 minutes to go).

## Tools and checks (tools.txt)
- Built with `vendor/build_tools.sh` from the vendored sources only; all 196 manifest hashes match.
  CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, drat-trim lrat-check 2e3b2dc + E2 patch.
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and accept the good one, and the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; the sha256 of base.cnf and base.json both match.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (53: idx ≡ 37 mod 42; 42 H at cap 1800 s, 11 Q at cap 2400 s)
| | certified | UNKNOWN (timed out) | not reached | errors |
|---|---|---|---|---|
| total | 5 | 2 | 46 | 0 |
| P8 | 3 H | 2 Q (P8_3-13, P8_9-16; 2381 s each at cap 2400) | 0 | 0 |
| P7 | 2 H | 0 | 4 H, 1 Q | 0 |
| P1 | 0 | 0 | 5 H, 2 Q | 0 |
| P2 | 0 | 0 | 6 H, 1 Q | 0 |
| P3 | 0 | 0 | 5 H, 2 Q | 0 |
| P4 | 0 | 0 | 6 H, 1 Q | 0 |
| P5 | 0 | 0 | 5 H, 1 Q | 0 |
| P6 | 0 | 0 | 6 H, 1 Q | 0 |

Certified units: P8_1-3-9, P8_1-6-11, P8_2-6-10, P7_2-11-15, P7_3-10-15 (all H). P7_3-10-15 ran at a reduced cap of 1172 s and was solved in 607 s.
For each, lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT`. The proofs were deleted after checking.

| certified (5) | min | median | max |
|---|---|---|---|
| solve s | 290.0 | 390.3 | 606.8 |
| lrat-check s | 52.3 | 56.0 | 61.4 |
| cake_lpr s | 308.1 | 320.5 | 342.8 |
| proof size | 3.25 GB | 3.50 GB | 3.74 GB |

- Largest solver RSS: 4415 MB, on P8_3-13. cake_lpr heap: 8000 MB.
- No SAT. No proof rejection, no `certified: false` record and no ERROR status. No memory problem.
- Both Q units timed out. The 46 units not reached (rows 9..54 of units.tsv, from P7_9-11 onward) still need a machine.

Files: env.txt, tools.txt, units.tsv, run.sh, out.jsonl (7 records), lane.log.tail.

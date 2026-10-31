# C2P3 M22

Task `results/C2P3/TASK.md` (commit 4f653319), LIST = C2P3.tsv, j = 22, N = 50, H = 2.5. One lane, start 09:42:46Z, END 11:57:46Z (epoch 1793447866). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources only: manifest, all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch).
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: `p cnf 838032 16653336`, sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…bf472b48, both match.
- Cubes P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 assigned, `units.tsv`)

| unit | case | kind | status | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_3-11 | P6 | Q | certified UNSAT | 6000 | 3629.4 | 114.0 | 609.0 | 7.12 | 4372 |
| P6_1-13-14 | P6 | H | certified UNSAT | 1800 | 233.9 | 54.1 | 306.3 | 3.20 | 4358 |
| P6_3-8-14 | P6 | H | certified UNSAT | 1800 | 592.5 | 58.6 | 342.0 | 3.75 | 4368 |
| P6_8-10-15 | P6 | H | certified UNSAT | 1337 | 213.7 | 53.2 | 296.6 | 3.12 | 4349 |
| P5_1-6 | P5 | Q | UNKNOWN (timed out) | 765 | 757.7 | – | – | – | 4378 |

- Certified: 4 (P6: 1 Q, 3 H). All four of my P6 units are closed, including the quadrilateral P6_3-11.
- Timed out: 1 (P5 Q: P5_1-6, at a cap of only 765 s cut short by END; not a real attempt at its 2400 s cap).
- Not reached: 5 (P5 H: P5_1-11-16, P5_2-8-14, P5_6-8-9, P5_7-9-11; P5 Q: P5_9-13).
- Errors: none. No record with `"certified": false`.
- Certified units, min / median / max: solve 213.7 / 413.2 / 3629.4 s; lrat-check 53.2 / 56.4 / 114.0 s; cake_lpr 296.6 / 324.2 / 609.0 s; proof 3.12 / 3.47 / 7.12 GB.
- Largest solver RSS: 4378 MB.
- No SAT, no proof rejection, no memory problem. The disk stayed at 21 GB or more free throughout.

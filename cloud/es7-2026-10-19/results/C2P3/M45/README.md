# C2P3 M45 (LIST = C2P3.tsv, j = 45, N = 50, H = 2.5, Z = 4f653319)

Start 2026-10-31 09:42:50Z (epoch 1793439770), END 1793447870 (11:57:50Z). One lane, `run.sh`.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as expected.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (9, idx ≡ 45 mod 50)

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|---|---|---|---|
| P6_7-12 | P6 | Q | 6000 | certified UNSAT | 2072.6 | 90.0 | 481.1 | 5.78 |
| P6_2-9-15 | P6 | H | 1800 | certified UNSAT | 466.1 | 54.7 | 312.4 | 3.62 |
| P6_7-10-11 | P6 | H | 1800 | certified UNSAT | 22.4 | 11.9 | 102.1 | 0.22 |
| P5_1-2-9 | P5 | H | 1800 | certified UNSAT | 283.8 | 51.9 | 284.4 | 3.28 |
| P5_1-8-10 | P5 | H | 1800 | certified UNSAT | 293.5 | 51.0 | 288.8 | 3.30 |
| P5_2-6 | P5 | Q | 2400 (run at 2382, lane time cap) | certified UNSAT | 1532.0 | 80.6 | 433.5 | 5.39 |
| P5_2-11-16 | P5 | H | 1800 (run at 309, lane time cap) | UNKNOWN (time-capped) | 305.1 | – | – | – |
| P5_6-11 | P5 | Q | 2400 | not reached | | | | |
| P5_8-9 | P5 | Q | 2400 | not reached | | | | |

By case and kind:
- P6: Q 1/1 certified; H 2/2 certified.
- P5: Q 1 certified, 2 not reached; H 2 certified, 1 UNKNOWN (only 309 s of its 1800 s cap were available before END, so it is not a real timeout at its cap and should be re-run).

Certified (6): solve 22.4 / 379.8 / 2072.6 s, lrat-check 11.9 / 53.3 / 90.0 s, cake_lpr 102.1 / 300.6 / 481.1 s, proof 0.22 / 3.45 / 5.78 GB (min / median / max). All proofs accepted by both checkers (`c VERIFIED`, `s VERIFIED UNSAT`) and deleted.

Largest solver RSS: 4418 MB. No SAT, no proof rejection, no ERROR record, no memory or disk problem.

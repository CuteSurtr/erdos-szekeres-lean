# C2P3 M01: shard j = 1 of N = 50 of `lists/C2P3.tsv` (H = 2.5, task commit 4f653319)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 09:42:47Z, END 11:57:47Z (start + 2.5 h − 15 min).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: manifest of all 196 vendored files matches; CaDiCaL 3.0.1, cake_lpr and lrat-check (E2 patch) built from the vendored sources, nothing downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`): header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10: idx ≡ 1 mod 50, `units.tsv`; run command in `run.sh`)

| idx | unit | case | kind | cap used (s) | status | solve s | RSS MB | proof GB | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | P7_1-13 | P7 | Q | 6000 | certified UNSAT | 2455.4 | 4408 | 5.46 | 77.5 | 490.6 |
| 51 | P7_3-8-15 | P7 | H | 1800 | certified UNSAT | 665.4 | 4418 | 3.70 | 55.1 | 339.9 |
| 101 | P6_2-11-15 | P6 | H | 1800 | certified UNSAT | 464.2 | 4402 | 3.43 | 51.3 | 329.1 |
| 151 | P6_7-11-12 | P6 | H | 1800 | certified UNSAT | 88.5 | 3119 | 1.17 | 23.5 | 167.7 |
| 201 | P5_1-2-15 | P5 | H | 1800 | certified UNSAT | 249.8 | 4395 | 3.19 | 45.8 | 307.5 |
| 251 | P5_1-8-16 | P5 | H | 1463 (shortened by END) | certified UNSAT | 508.8 | 4374 | 3.56 | 50.8 | 329.6 |
| 301 | P5_2-6-12 | P5 | H | 560 (shortened by END; list cap 1800) | UNKNOWN (timeout) | 554.4 | 4364 | – | – | – |
| 351 | P5_2-13 | P5 | Q | – | not reached | | | | | |
| 401 | P5_6-12 | P5 | Q | – | not reached | | | | | |
| 451 | P5_8-10 | P5 | Q | – | not reached | | | | | |

Counts by case and kind:
- P7: Q 1 certified; H 1 certified.
- P6: H 2 certified.
- P5: H 2 certified, 1 timed out (only 560 s of its 1800 s cap were available); Q 3 not reached.
- Total: 6 certified, 1 UNKNOWN, 3 not reached, 0 errors.

Certified units (6), min / median / max:
- solve: 88.5 / 486.5 / 2455.4 s
- lrat-check: 23.5 / 51.1 / 77.5 s
- cake_lpr: 167.7 / 329.4 / 490.6 s (heap 8000 MB every time; no retry needed)
- proof size: 1.17 / 3.49 / 5.46 GB (all proofs deleted after checking)

Largest solver RSS: 4418 MB (P7_3-8-15).

No SAT, no proof rejection, no `certified: false` or ERROR record, no memory problem. P5_2-6-12 is open from this machine only because its cap was cut to 560 s by END; it should be re-run with its full cap.

# C2P2 M38 (LIST C2P2.tsv, j = 38, N = 42, H = 2.5, Z = d266d2c3)

Start 2026-10-31 06:46:42Z (epoch 1793429202), END 1793437302 (08:41:42Z). One lane (`run.sh`), 4 CPUs, 15 GB RAM.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (18; `units.tsv`)
| case | kind | units | certified | UNKNOWN (timed out) | not reached | errors |
|---|---|---|---|---|---|---|
| P7 | H | 10 | 8 | 0 | 2 (P7_8-12-15, P7_9-12-15) | 0 |
| P7 | Q | 1 | 0 | 1 (P7_3-10, cap cut to 1394 s by END) | 0 | 0 |
| P3 | cover | 1 | 0 | 0 | 1 (P3_cover) | 0 |
| P6 | H | 3 | 0 | 0 | 3 (P6_1-5-9, P6_7-9-13, P6_8-11-13) | 0 |
| P6 | Q | 3 | 0 | 0 | 3 (P6_1-12, P6_2-8, P6_2-16) | 0 |
| total | | 18 | 8 | 1 | 8 | 0 |

Certified (all UNSAT, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`): P7_1-2-8, P7_1-4-13, P7_1-6-9, P7_1-10-11, P7_1-12-15, P7_2-5-11, P7_2-11-16, P7_3-8-11.

| certified (8 H units) | min | median | max |
|---|---|---|---|
| solve s | 252.5 | 385.9 | 408.1 |
| lrat-check s | 52.1 | 56.5 | 58.3 |
| cake_lpr s | 303.0 | 327.4 | 348.9 |
| proof GB | 3.19 | 3.41 | 3.45 |

P7_3-10 (Q, list cap 2400 s) got only 1394 s because of END and returned UNKNOWN after 1381 s; it remains open.

Largest solver RSS: 4412 MB (P7_3-8-11). No SAT, no proof rejection, no `certified: false` or ERROR record, no memory problem.

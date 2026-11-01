# C2P5 M38 (list C2P5C.tsv, shard j = 1 of N = 13, H = 4.5, task commit 81cb025f)

## Tools and checks
- `C2P/vendor/build_tools.sh`: all 196 vendored files match MANIFEST.sha256; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch), built from `vendor/tools-src.tar.xz`, nothing downloaded.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both checkers, good LRAT accepted by both.
- Base CNF `p cnf 838032 16653336`, sha256 base.cnf b0061e90…8ff1 and base.json 2476faff…2b48: both match.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details in `tools.txt`.

## Units (2: rows idx 1 and 14)
| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P2_7-9 | P2 | Q | 8000 | UNSAT, certified | 447.95 | 44.6 | 298.0 | 3,252,785,802 | 4361 |
| P3_4-8-10 | P3 | H | 2400 | UNSAT, certified | 82.17 | 21.7 | 164.8 | 1,110,576,864 | 3149 |

- Certified: 2 (P2 Q: 1, P3 H: 1). Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.
- Certified units (n = 2, so median = mean of the two): solve 82.17 / 265.06 / 447.95 s; lrat-check 21.7 / 33.15 / 44.6 s; cake_lpr 164.8 / 231.4 / 298.0 s; proof 1.11 / 2.18 / 3.25 GB (min / median / max).
- Largest solver RSS: 4361 MB.
- No SAT, no proof rejection, no memory problem. The lane finished at 20:26:37Z, well before END.

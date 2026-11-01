# C2P5 M41: list C2P5C.tsv, shard j = 4 of N = 13, H = 4.5 (TASK commit 81cb025f)

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: rows with idx ≡ 4 mod 13)
| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P3_1-11-14 | P3 | H | 2400 | UNSAT, certified | 307.02 | 54.1 | 329.8 | 3,272,229,219 | 4460 |
| P3_5-7-14 | P3 | H | 2400 | UNSAT, certified | 278.53 | 60.1 | 334.5 | 3,204,082,988 | 4397 |

- Counts: P3 / H: 2 certified, 0 timed out (UNKNOWN), 0 not reached, 0 errors. No other cases or kinds on this shard.
- Certified (n = 2): solve 278.53 / 292.78 / 307.02 s (min / median / max); lrat-check 54.1 / 57.1 / 60.1 s; cake_lpr 329.8 / 332.15 / 334.5 s; proof 3.20 / 3.24 / 3.27 GB.
- Largest solver RSS: 4460 MB.
- No SAT, no proof rejection, no `certified: false` or ERROR record, no memory problem. The lane finished all units at 20:32:24Z, well before END (1793492498).

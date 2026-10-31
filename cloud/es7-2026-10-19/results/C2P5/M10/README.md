# C2P5 M10: LIST = C2P5A.tsv, shard j = 10 of N = 37, H = 4.5, TASK commit 81cb025f

## Tools and checks
- Tools built from the vendored sources with `C2P/vendor/build_tools.sh`: CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Manifest: all 196 files match. Sanity checks as expected: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`. Nothing was cloned or downloaded.
- Base CNF: header `p cnf 838032 16653336`. sha256 b0061e90…d8ff1 (base.cnf) and 2476faff…b48 (base.json) both match.
- Cubes P1..P8: each byte-identical to `C2P/cubes/P<a>_cubes.txt` (560 lines each).
- Details are in `tools.txt`.

## Units (rows of C2P5A.tsv with idx ≡ 10 mod 37)
Start 18:39:39Z (epoch 1793471979), END 1793487279. The lane finished all units at 19:29:32Z.

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_6-10 | P4 | Q | 8000 | UNSAT, certified | 951.93 | 65.3 | 365.5 | 4242283168 | 4403 |
| P4_5-7-14 | P4 | H | 2400 | UNSAT, certified | 292.26 | 52.0 | 312.8 | 3266128859 | 4367 |
| P4_6-7-15 | P4 | H | 2400 | UNSAT, certified | 255.90 | 54.6 | 312.0 | 3231780994 | 4365 |
| P4_7-10-13 | P4 | H | 2400 | UNSAT, certified | 29.03 | 12.9 | 114.0 | 217859721 | 2646 |

Counts:
- Certified: 4 of 4. That is P4 Q: 1 and P4 H: 3.
- Timed out (UNKNOWN): 0.
- Not reached: 0.
- Errors: 0.

For the 4 certified units (minimum / median / maximum):
- solve: 29.03 / 274.08 / 951.93 s.
- lrat-check: 12.9 / 53.3 / 65.3 s.
- cake_lpr: 114.0 / 312.4 / 365.5 s.
- proof size: 0.22 / 3.25 / 4.24 GB.

The largest solver RSS was 4403 MB (P4_6-10).

No SAT, no proof rejection and no memory or disk problem. Both checkers accepted every proof, and the proofs were deleted afterwards.

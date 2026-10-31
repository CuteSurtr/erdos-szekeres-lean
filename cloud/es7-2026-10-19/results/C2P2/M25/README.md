# C2P2 M25 (LIST C2P2.tsv, j = 25, N = 42, H = 2.5, task commit d266d2c3)

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476fafff…2b48`, both as expected.
- Cubes: `l2cubes.py` output byte-identical to `C2P/cubes/P{a}_cubes.txt` for a = 1..8.
- Details are in `tools.txt`.

## Units (7 in this shard; lane run from 06:49Z to 08:52Z, END = 1793437347)

| idx | unit | case | kind | cap | result |
|---|---|---|---|---|---|
| 25 | P7_1-12 | P7 | Q | 6000 | **certified** UNSAT |
| 67 | P6_1-4 | P6 | Q | 2400 | **certified** UNSAT |
| 109 | P6_1-10 | P6 | Q | 2400 | timed out (UNKNOWN) at a reduced cap of 1705 s, which was set by END |
| 151 | P6_2-4-8 | P6 | H | 1800 | not reached |
| 193 | P6_2-12 | P6 | Q | 2400 | not reached |
| 235 | P6_3-11-12 | P6 | H | 1800 | not reached |
| 277 | P6_8-9-11 | P6 | H | 1800 | not reached |

By case and kind:
- P7 Q: 1 certified.
- P6 Q: 1 certified, 1 timed out, 1 not reached.
- P6 H: 3 not reached.
- Totals: 2 certified, 1 UNKNOWN, 4 not reached, 0 errors.

Certified units (min / median / max over 2):
- solve: 1003.9 / 2212.4 / 3420.9 s
- lrat-check: 65.8 / 87.7 / 109.5 s
- cake_lpr: 419.6 / 504.6 / 589.5 s
- proof size: 4.38 / 5.84 / 7.30 GB (4378814615 and 7298811846 bytes)

Largest solver RSS: 4369.7 MB (P6_1-10).

No SAT result, no proof was rejected, no record has `"certified": false` or an ERROR status, and there were no memory problems. Proofs were deleted after checking.

# C2P2 M36: shard j = 36 of N = 42 of C2P2.tsv, H = 2.5 h, task commit d266d2c3

## Tools and checks
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) from the vendored sources. All 196 manifest hashes matched. Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…d8ff1) and base.json (2476faff…2b48) both match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units (19, idx ≡ 36 mod 42)
| case | kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P6 | cover | 1 (P6_cover) | 0 | 0 | 0 |
| P7 | H | 6 | 0 | 3 (P7_3-9-14, P7_8-10-12, P7_10-11-13) | 0 |
| P7 | Q | 1 (P7_2-15) | 0 | 1 (P7_9-11) | 0 |
| P5 | cover | 0 | 0 | 1 (P5_cover) | 0 |
| P6 | Q | 0 | 0 | 3 (P6_1-5, P6_2-15, P6_8-11) | 0 |
| P6 | H | 0 | 0 | 3 (P6_1-11-15, P6_2-7-15, P6_7-9-11) | 0 |
| **total** | | **8** | **0** | **11** | **0** |

The 6 certified P7 H units are P7_1-4-9, P7_1-5-13, P7_1-9-10, P7_1-11-16, P7_2-3-14 and P7_2-9-14. P7_2-15 ran with a reduced cap of 1413 s because END was close, and it solved in 1245 s. The lane then stopped with 264 s left before END.

Statistics for the 8 certified units (minimum / median / maximum):
- solve: 243.6 / 400.2 / 1245.1 s
- lrat-check: 52.1 / 56.8 / 76.9 s
- cake_lpr: 303.3 / 318.1 / 452.1 s
- proof size: 3.20 / 3.50 / 4.98 GB

Every proof gave `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr, and was deleted afterwards.

## Other
- Largest solver RSS: 4465 MB (P6_cover).
- No SAT, no proof rejection, no memory problem.

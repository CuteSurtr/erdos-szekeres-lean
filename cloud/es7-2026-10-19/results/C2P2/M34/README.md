# C2P2 M34 (LIST = C2P2.tsv, j = 34, N = 42, H = 2.5, task commit d266d2c3)

## Tools and checks

- Built with `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. No code was cloned or downloaded.
- Sanity: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…2b48 both match.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`. Details are in `tools.txt`.

## Units (7 = idx ≡ 34 mod 42)

| idx | unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 34 | P7_9-15 | P7 | Q | 6000 | certified | 4285.44 | 144.3 | 683.0 | 8.22 | 4369 |
| 76 | P6_1-4-15 | P6 | H | 1800 | certified | 265.56 | 53.9 | 318.1 | 3.23 | 4399 |
| 118 | P6_1-11-13 | P6 | H | 1522 | certified | 259.34 | 55.0 | 307.7 | 3.23 | 4394 |
| 160 | P6_2-7-13 | P6 | H | 889 | certified | 587.95 | 62.2 | 359.6 | 3.75 | 4381 |
| 202 | P6_2-14-15 | P6 | H | 1800 | not reached | | | | | |
| 244 | P6_7-9 | P6 | Q | 2400 | not reached | | | | | |
| 286 | P6_8-10-14 | P6 | H | 1800 | not reached | | | | | |

**Summary:** 4 certified (P6 H: 3, P7 Q: 1). 0 timed out (UNKNOWN). 3 not reached (P6 H: 2, P6 Q: 1). 0 errors.

Certified units (min / median / max):
- solve s: 259.3 / 426.8 / 4285.4
- lrat-check s: 53.9 / 58.6 / 144.3
- cake_lpr s: 307.7 / 338.9 / 683.0
- proof GB: 3.2 / 3.5 / 8.2

Largest solver RSS: 4399 MB.

Highlight: P7_9-15 (Q, cap 6000) took 4285 s and was certified. Its 8.2 GB proof passed lrat-check in 144 s and cake_lpr in 683 s.

The lane stopped at 08:54:07Z with 464 s left before END, so it started no further unit. The not-reached units are P6_2-14-15, P6_7-9 and P6_8-10-14.

No SAT, no proof rejection, no memory problem. Peak disk use was about 20 GB of the allowance, while the 8.2 GB proof was on disk.

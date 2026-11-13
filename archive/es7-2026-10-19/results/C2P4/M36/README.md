# C2P4 M36

Values: V = M36, LIST = C2P4.tsv, j = 36, N = 50, H = 2.5, Z = a46b478d.
Started 2026-10-31 13:01:58 UTC (epoch 1793451718). END = 1793459818 (15:16:58 UTC).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only: all 196 manifest files match. The tools are CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, and lrat-check 2e3b2dc with the E2 patch. No code was cloned or downloaded.
- Sanity checks:
  - The cake_lpr example prints `s VERIFIED UNSAT`.
  - Bad LRAT: both checkers reject it.
  - Good LRAT: both checkers accept it.
- Base CNF: the header is `p cnf 838032 16653336`.
  - base.cnf sha256 `b0061e90…d8ff1` matches.
  - base.json sha256 `2476faff…bf472b48` matches.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (19 rows of C2P4.tsv with idx ≡ 36 mod 50)
Certified (UNSAT; lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`): **9**

| case | kind | certified | timed out | not reached | errors |
|---|---|---|---|---|---|
| P5 | Q | 1 (P5_7-8) | 0 | 0 | 0 |
| P5 | H | 5 (P5_1-3-8, P5_2-6-11, P5_2-14-16, P5_6-13-14, P5_8-10-14) | 0 | 0 | 0 |
| P4 | Q | 1 (P4_5-8) | 0 | 0 | 0 |
| P4 | H | 2 (P4_1-3-8, P4_1-9-13) | 0 | 3 (P4_2-6-15, P4_5-9-10, P4_6-10-11) | 0 |
| P3 | Q | 0 | 0 | 1 (P3_1-12) | 0 |
| P3 | H | 0 | 0 | 6 (P3_1-2-7, P3_1-7-15, P3_4-5-12, P3_4-10-16, P3_5-10-14, P3_7-10-13) | 0 |

There were no timeouts (status UNKNOWN), no errors, and no `"certified": false` records. 10 units were not reached. The lane stopped at 15:07:56Z with 541 s left before END.

Two units ran with a cap lowered by the END rule: P4_5-8 (cap 2833 s) and P4_1-9-13 (cap 803 s). Both still finished well within their caps.

Certified units (min / median / max):
- solve: 30.3 / 348.3 / 800.2 s
- lrat-check: 15.0 / 60.3 / 71.1 s
- cake_lpr: 131.4 / 342.3 / 388.0 s
- proof size: 0.22 / 3.30 / 3.68 GB (215558095 / 3297712080 / 3682630354 bytes)

Largest solver RSS: 4421 MB (P5_1-3-8). cake_lpr heap: 8000 MB.

There was no SAT answer, no proof rejection and no memory problem.

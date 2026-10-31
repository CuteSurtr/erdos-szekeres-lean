# C2P5 M09: list C2P5A.tsv, shard j = 9 of N = 37, H = 4.5 h, task commit 81cb025f

## Tools and checks
- I built the tools with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz`, and all 196 manifest files matched. The tools are CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks:
  - Both checkers rejected the bad LRAT. lrat-check printed `c FAILED`, and cake_lpr printed `Checking failed ... pivot must be non-zero`.
  - Both accepted the good LRAT, with `c VERIFIED` and `s VERIFIED UNSAT`.
  - The cake_lpr example printed `s VERIFIED UNSAT`.
- The base CNF header is `p cnf 838032 16653336`. Its sha256 matches `b0061e90…d8ff1` for base.cnf and `2476faff…b48` for base.json.
- The cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units (4 rows, idx ≡ 9 mod 37): all 4 certified
| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_5-16 | P4 | Q | 8000 | UNSAT, certified | 3441.5 | 125.4 | 645.4 | 7,731,804,857 | 4386 |
| P4_5-7-13 | P4 | H | 2400 | UNSAT, certified | 233.3 | 53.6 | 302.0 | 3,159,325,432 | 4364 |
| P4_6-7-14 | P4 | H | 2400 | UNSAT, certified | 216.6 | 52.7 | 299.8 | 3,141,178,593 | 4399 |
| P4_7-10-12 | P4 | H | 2400 | UNSAT, certified | 28.5 | 13.1 | 115.1 | 217,604,627 | 2660 |

**Counts:**
- P4 Q: 1 certified.
- P4 H: 3 certified.
- Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.

**Certified units** (minimum / median / maximum):
- solve: 28.5 / 225.0 / 3441.5 s
- lrat-check: 13.1 / 53.2 / 125.4 s
- cake_lpr: 115.1 / 300.9 / 645.4 s
- proof size: 0.22 / 3.15 / 7.73 GB

The median of the four is the mean of the middle two values.

## Problems
- **Largest solver RSS:** 4399 MB (P4_6-7-14).
- No SAT.
- No proof was rejected. There are no `certified: false` or ERROR records. cake_lpr needed only the 8000 MB heap.
- No memory problem. No disk problem: at least 23 GB stayed free while the 7.7 GB proof was being written.
- The lane finished all its units at 20:00:05Z, well before END (1793486406).

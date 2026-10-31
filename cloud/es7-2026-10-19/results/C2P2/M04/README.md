# C2P2 M04 (LIST = C2P2.tsv, j = 4, N = 42, H = 2.5, TASK commit d266d2c3)

Start 2026-10-31 06:47:37 UTC (epoch 1793429257); lane END = 1793437357 (09:02:37 UTC). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…f2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: idx ≡ 4 mod 42, 8 units)

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof | solver RSS |
|---|---|---|---|---|---|---|---|---|---|
| P8_1-12 | P8 | Q | 6000 | UNSAT, certified | 3403.7 | 114.6 | 612.7 | 7.41 GB | 4414 MB |
| P6_1-2-9 | P6 | H | 1800 | UNSAT, certified | 308.6 | 52.4 | 307.6 | 3.28 GB | 4402 MB |
| P6_1-7-12 | P6 | H | 1800 | UNSAT, certified | 606.2 | 60.0 | 337.4 | 3.75 GB | 4369 MB |
| P6_1-13-16 | P6 | H | 1533* | UNSAT, certified | 223.6 | 50.6 | 296.6 | 3.22 GB | 4351 MB |
| P6_2-8-16 | P6 | H | 952* | UNSAT, certified | 404.1 | 56.4 | 330.1 | 3.55 GB | 4411 MB |
| P6_3-7-14 | P6 | H | 1800 | not reached | | | | | |
| P6_7-10-15 | P6 | H | 1800 | not reached | | | | | |
| P6_8-14 | P6 | Q | 2400 | not reached | | | | | |

\* cap reduced by lane.py to fit before END. Both units still finished well below their reduced caps.

**Counts:**
- Certified: 5. By case and kind: P8 Q 1, P6 H 4.
- Timed out (UNKNOWN): 0.
- Errors / `certified: false`: 0.
- Not reached: 3 (P6 H 2: P6_3-7-14 and P6_7-10-15; P6 Q 1: P6_8-14). The lane stopped at 08:50:05 with 751 s left, which is under the 15-minute minimum to start a unit.

**Certified units, min / median / max:**
- Solve: 223.6 / 404.1 / 3403.7 s.
- lrat-check: 50.6 / 56.4 / 114.6 s.
- cake_lpr: 296.6 / 330.1 / 612.7 s.
- Proof size: 3.22 / 3.55 / 7.41 GB.

The P8_1-12 quadrilateral subcase timed out at its full cap in the first wave. Here it is UNSAT and certified, in 3404 s.

## Resources and problems
- Largest solver RSS: 4414 MB (P8_1-12). cake_lpr ran with an 8000 MB heap (RSS about 8.2 GB).
- Disk: the largest proof was 7.4 GB, with at least 21 GB left free throughout. No memory problems.
- No SAT, no proof rejection, no errors.

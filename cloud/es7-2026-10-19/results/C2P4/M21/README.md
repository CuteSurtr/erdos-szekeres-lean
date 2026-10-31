# C2P4 M21: shard j=21 of N=50 of lists/C2P4.tsv (H = 2.5 h, task commit a46b478d)

## Tools and checks
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored sources. Manifest: all 196 files match.
- Sanity: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: `p cnf 838032 16653336`. sha256 base.cnf b0061e90...d8ff1 and base.json 2476faff...2b48 both match.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P*_cubes.txt`.
- Details are in `tools.txt`.

## Units (19)
Started 13:01:36Z. END was 1793459796 (15:16:36Z). The lane ran one unit at a time.

| case | kind | units | certified | UNKNOWN | not reached |
|---|---|---|---|---|---|
| P5 | Q | 1 | 1 (P5_2-7) | 0 | 0 |
| P5 | H | 4 | 4 | 0 | 0 |
| P6 | H | 1 | 1 | 0 | 0 |
| P4 | Q | 1 | 0 | 1 (P4_1-10) | 0 |
| P4 | H | 6 | 0 | 0 | 6 |
| P3 | Q | 1 | 0 | 0 | 1 |
| P3 | H | 5 | 0 | 0 | 5 |
| **total** | | 19 | 6 | 1 | 12 |

- Certified: P5_2-7, P6_2-7-14, P5_1-10-12, P5_2-9-10, P5_6-9-12 and P5_7-10-15. All are UNSAT, with `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr.
- UNKNOWN: P4_1-10 (Q). The time left before END cut its cap to 1021 s, instead of the listed 6000 s, and it stopped at 1010.9 s. It is still open.
- Not reached: P4_1-2-5, P4_1-7-13, P4_2-5-10, P4_5-7-10, P4_6-7-14, P4_8-10-11, P3_7-8, P3_1-6-15, P3_1-14-15, P3_4-9-13, P3_5-9-10 and P3_7-8-11.

Certified units, as min / median / max:
- solve: 26.0 / 327.0 / 2499.2 s (P5_2-7 Q: 2499.2 s; the H units: 26.0–655.3 s)
- lrat-check: 10.3 / 48.3 / 82.1 s
- cake_lpr: 108.1 / 300.1 / 519.3 s
- proof size: 0.22 / 3.27 / 5.95 GB (deleted after the checks)

Largest solver RSS: 4405 MB (P5_2-7).

## Problems
No SAT answer, no proof rejection, no ERROR record and no memory problem.

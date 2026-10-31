# C2P5 M32 (LIST = C2P5A.tsv, j = 32, N = 37, H = 4.5, TASK commit 81cb025f)

Start 2026-10-31 19:25:50Z (epoch 1793474750), END 1793490050 (23:40:50Z). The lane finished all units at 21:06:28Z.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match):
  CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`; sha256 of base.cnf (b0061e90…) and base.json (2476faff…) match.
- Cubes P1..P8 from `C2C34/l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, `out.jsonl`)
10 units (rows of C2P5A.tsv with idx ≡ 32 mod 37), all case P4, kind H, cap 2400 s.

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | H | 10 | 10 | 0 | 0 | 0 |

Certified (both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`):
P4_1-2-8, P4_1-5-7, P4_1-6-8, P4_1-8-11, P4_1-10-12, P4_1-12-14, P4_2-6-15, P4_5-8-16, P4_6-9-12, P4_8-11-12.

| quantity | min | median | max |
|---|---|---|---|
| solve s | 26.06 | 281.84 | 451.55 |
| lrat-check s | 12.9 | 49.95 | 58.2 |
| cake_lpr s | 113.4 | 295.45 | 337.3 |
| proof size (bytes) | 219,916,658 | 3,301,395,525 | 3,627,650,932 |

Largest solver RSS: 4410.59 MB (P4_5-8-16).

## Problems
No SAT, no proof rejection, no `certified: false` record, no ERROR status, no memory problem.
All proofs were deleted after checking.

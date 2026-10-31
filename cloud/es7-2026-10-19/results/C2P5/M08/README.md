# C2P5 M08: list C2P5A.tsv, shard j = 8 of N = 37, H = 4.5 h (task commit 81cb025f)

All 4 units are **certified UNSAT**. Both checkers accepted every proof. There was no SAT, no timeout, no error, no proof rejection and no memory problem. The lane finished at 19:49:21Z, well before END (1793486404 = 22:40:04Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built the tools from the vendored sources: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). The manifest check passed for all 196 files, and nothing was downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…8ff1) and of base.json (2476faff…2b48) match the expected values.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Units are the rows of `lists/C2P5A.tsv` with idx ≡ 8 (mod 37). This is the list file as it is on es7-cloud; it was last changed in 92a2b58ad, which is after Z.

## Units

| idx | unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 8 | P4_5-15 | P4 | Q | 8000 | certified | 3421.23 | 109.1 | 603.9 | 7,842,492,900 | 4390 |
| 45 | P4_5-7-12 | P4 | H | 2400 | certified | 79.25 | 26.0 | 165.5 | 1,289,263,516 | 3412 |
| 82 | P4_6-7-13 | P4 | H | 2400 | certified | 101.0 | 27.9 | 180.8 | 1,511,910,563 | 3414 |
| 119 | P4_7-10-11 | P4 | H | 2400 | certified | 22.81 | 12.6 | 107.7 | 215,853,428 | 2647 |

Counts by case and kind:
- P4 / Q: 1 certified, 0 timed out (UNKNOWN), 0 not reached, 0 errors.
- P4 / H: 3 certified, 0 timed out (UNKNOWN), 0 not reached, 0 errors.

Certified units, given as minimum / median / maximum:
- All 4 units:
  - solve: 22.81 / 90.13 / 3421.23 s
  - lrat-check: 12.6 / 26.95 / 109.1 s
  - cake_lpr: 107.7 / 173.15 / 603.9 s
  - proof size: 0.22 / 1.40 / 7.84 GB
- The 3 H units:
  - solve: 22.81 / 79.25 / 101.0 s
  - lrat-check: 12.6 / 26.0 / 27.9 s
  - cake_lpr: 107.7 / 165.5 / 180.8 s
  - proof size: 0.22 / 1.29 / 1.51 GB

The largest solver RSS was 4390 MB (P4_5-15), on a 15 GB machine. Peak disk use was about 19 GB of the session allowance.

No SAT, no certified=false record, no ERROR status and no memory problem. Proofs were deleted after checking. `out.jsonl` has the full records and `lane.log.tail` has the lane log.

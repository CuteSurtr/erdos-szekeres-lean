# C2P5 M87: LIST C2P5B.tsv, shard j = 37 of N = 50, H = 5.25 h, TASK commit 81cb025f

**Result: all 14 units are UNSAT and certified. Both lrat-check and cake_lpr accepted every proof.** There was no SAT, no timeout, no error, no proof rejection and no memory problem.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `vendor/tools-src.tar.xz`. The manifest check passed: all 196 files match. Sources: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. No code was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF from `SYMZ/zcnf.py rot 17 7 --m 2 --hull`:
  - header `p cnf 838032 16653336`
  - base.cnf sha256 `b0061e90…d8ff1` (matches)
  - base.json sha256 `2476faff…72b48` (matches)
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 37 mod 50, 14 units)
| case | kind | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|
| P2 | Q | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 0 | 0 | 0 |
| P3 | Q | 2 | 0 | 0 | 0 |
| **total** | | **14** | 0 | 0 | 0 |

Certified units: P2_5-12, P1_4-10, P2_1-5-7, P2_3-5-8, P2_3-9-12, P2_4-6-15, P2_5-6-13, P2_6-9-11, P1_2-5-15, P1_2-14-15, P1_3-9-14, P1_4-11-12, P3_1-6, P3_8-12.

Statistics over the 14 certified units (min / median / max):
- solve: 25.1 / 295.9 / 1525.4 s
  - Q only: 822.8 / 1274.3 / 1525.4 s
  - H only: 25.1 / 262.5 / 473.5 s
- lrat-check: 12.2 / 55.0 / 84.4 s
- cake_lpr: 112.1 / 316.8 / 428.7 s (heap 8000 MB every time; no retry with 11000 MB was needed)
- proof size: 0.22 / 3.39 / 5.11 GB

Largest solver RSS: 4420 MB, on P3_1-6. Free disk never went below 23 GB.

The lane started at 15:13Z and finished at 18:39Z, well before END (20:10:27Z). Per-unit records are in `out.jsonl`, and the end of the lane log is in `lane.log.tail`.

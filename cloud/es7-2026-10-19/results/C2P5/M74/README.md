# C2P5 M74: LIST = C2P5B.tsv, shard j = 24 of N = 50, H = 5.25, TASK commit 81cb025f

**Result: all 19 units are certified UNSAT. Both checkers accepted every proof. There was no SAT answer, no proof rejection, no error and no memory problem.**

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 manifest files matched. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) from the vendored sources. No code was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`): header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both match.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows of C2P5B.tsv with idx ≡ 24 mod 50: 19 units)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **19** | **19** | 0 | 0 | 0 |

Every record shows lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

Certified units, min / median / max:
- solve: 20.6 / 310.0 / 1510.8 s. The longest was P3_6-11 (Q). P2_4-9 took 973 s and P1_3-8 took 819 s. All were far below their caps.
- lrat-check: 12.7 / 58.7 / 76.8 s
- cake_lpr: 120.8 / 336.0 / 428.5 s
- proof size: 0.22 / 3.40 / 4.62 GB

The largest solver RSS was 4419 MB, for P2_4-9. cake_lpr ran with an 8000 MB heap. The machine has 15 GB and there were no memory problems.

The lane started at 15:13Z and finished at 19:13Z (`lane done`), before END = 1793477418. The full records are in `out.jsonl` and the log tail is in `lane.log.tail`.

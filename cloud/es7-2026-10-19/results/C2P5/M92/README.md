# C2P5 M92: list C2P5B.tsv, shard j = 42 of N = 50, H = 5.25 h (TASK.md at 81cb025f)

**Result: all 18 units certified UNSAT. Both checkers accepted every proof. No SAT, no timeouts, no errors, no proof rejections.**

## Tools and checks (details in `tools.txt`)
- Built with `C2P/vendor/build_tools.sh`, using only the vendored sources: all 196 MANIFEST files matched. CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`): header `p cnf 838032 16653336`. Both sha256 values match: base.cnf `b0061e90…d8ff1` and base.json `2476faff…bf472b48`.
- Cubes: `C2C34/l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Run
- One lane (`run.sh`), END = 1793477430 (start 15:10:30Z + 5.25 h − 15 min). The lane started 15:12:55Z and finished all units at 18:47:24Z, well before END.
- Units: rows of C2P5B.tsv with idx ≡ 42 (mod 50) (`units.tsv`, 18 units).

## Units
| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 4 | 0 | 0 | 0 |
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **18** | **18** | 0 | 0 | 0 |

Certified: P2_6-9, P1_5-6, P3_1-11 (Q, cap 8000); P2_1-5-12, P2_3-5-13, P2_3-10-11, P2_4-7-12, P2_5-7-11, P2_6-11-12, P1_2-6-10, P1_3-4-9, P1_3-10-14, P1_5-6-9, P3_1-2-6, P3_1-7-14, P3_4-5-11, P3_4-10-15, P3_5-10-13 (H, cap 2400).

### Times and proof sizes of certified units (min / median / max)
| | all 18 | Q (3) | H (15) |
|---|---|---|---|
| solve s | 19.3 / 243.3 / 2317.4 | 334.1 / 532.1 / 2317.4 | 19.3 / 227.8 / 595.7 |
| lrat-check s | 13.2 / 53.7 / 90.2 | 48.7 / 56.9 / 90.2 | 13.2 / 53.8 / 61.8 |
| cake_lpr s | 112.6 / 310.2 / 507.7 | 298.7 / 319.9 / 507.7 | 112.6 / 311.4 / 369.7 |
| proof GB | 0.22 / 3.23 / 5.66 | 3.24 / 3.43 / 5.66 | 0.22 / 3.25 / 3.75 |

The slowest unit was P3_1-11 (Q): solve 2317 s, proof 5.66 GB, lrat-check 90 s, cake_lpr 508 s.

## Resources
- Largest solver RSS: 4405 MB (P2_6-9). cake_lpr heap: 8000 MB. No memory problems.
- The disk peaked at about 17 GB used, with 22 GB free. Every proof was deleted after it was checked.

## SAT / rejections / errors
None. `/opt/work/SAT_FOUND` never appeared. Every record has `"certified": true` with `c VERIFIED` and `s VERIFIED UNSAT`.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (18 records), `lane.log.tail`.

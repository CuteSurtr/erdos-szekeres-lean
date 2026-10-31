# C2P5 M27: list C2P5A.tsv, shard j = 27 of N = 37, H = 4.5 (TASK.md at 81cb025f)

**Result: all 5 units certified UNSAT (lrat-check and cake_lpr both accepted every proof). No SAT, no timeout, no error, no proof rejection, no memory problem.**

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf `b0061e90…d8ff1` and of base.json `2476faff…2b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: idx ≡ 27 mod 37)
| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P4 | Q (cap 8000) | 1 | 1 | 0 | 0 | 0 |
| P4 | H (cap 2400) | 4 | 4 | 0 | 0 | 0 |
| total | | 5 | 5 | 0 | 0 | 0 |

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|
| P4_10-11 | Q | 438.96 | 56.2 | 331.8 | 3305520915 | 4356.5 |
| P4_2-6-10 | H | 405.07 | 61.0 | 354.9 | 3438393701 | 4360.5 |
| P4_5-6-10 | H | 79.17 | 27.3 | 182.4 | 1128936081 | 3144.2 |
| P4_5-11-15 | H | 487.14 | 65.9 | 355.4 | 3514499665 | 4368.4 |
| P4_7-8-10 | H | 26.40 | 13.7 | 121.0 | 221054951 | 2644.6 |

Certified units (all 5), min / median / max:
- solve: 26.40 / 405.07 / 487.14 s
- lrat-check: 13.7 / 56.2 / 65.9 s
- cake_lpr (heap 8000 MB, no retry needed): 121.0 / 331.8 / 355.4 s
- proof size: 0.22 / 3.31 / 3.51 GB (221054951 / 3305520915 / 3514499665 bytes)

Largest solver RSS: 4368.4 MB (P4_5-11-15), well under the 15 GB of the machine.

The lane started 19:12:56Z and finished all units at 20:03:49Z (END was 23:26:08Z). Records: `out.jsonl`; log tail: `lane.log.tail`; command: `run.sh`.

# C2P2 M16: list C2P2.tsv, shard j = 16 of N = 42, H = 2.5 h (TASK at d266d2c3)

Start 2026-10-31T06:47:43Z (epoch 1793429263); END = start + 2.5 h - 15 min = 1793437363 (09:02:43Z).
One lane (`run.sh`), started 06:50:57Z, finished 08:47:45Z ("stop: 897 s left", i.e. under the 15 min start margin).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources (no download): manifest all 196 files match;
  CaDiCaL 3.0.1 (c6073042), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`);
  cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90...d8ff1` and base.json `2476faff...2b48`, both as expected.
- Cubes: `l2cubes.py` output for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (8 rows, idx ≡ 16 mod 42)
| idx | unit | case | kind | cap | result |
|---|---|---|---|---|---|
| 16 | P8_9-14 | P8 | Q | 6000 | certified UNSAT |
| 58 | P6_1-3-8 | P6 | H | 1800 | certified UNSAT |
| 100 | P6_1-8-16 | P6 | H | 1800 | certified UNSAT |
| 142 | P6_2-3-10 | P6 | H | 1800 | certified UNSAT |
| 184 | P6_2-10-14 | P6 | H | 1800 (run with cap 1118 by the time limit) | certified UNSAT |
| 226 | P6_3-9-11 | P6 | H | 1800 | not reached |
| 268 | P6_7-13 | P6 | Q | 2400 | not reached |
| 310 | P6_9-13 | P6 | Q | 2400 | not reached |

Counts by case and kind:
- P8 Q: 1 certified.
- P6 H: 4 certified, 1 not reached.
- P6 Q: 2 not reached.
- Totals: 5 certified, 0 timed out (UNKNOWN), 3 not reached, 0 errors.

Certified units (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT` for all, cake heap 8000 MB):

| unit | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|
| P8_9-14 | 3286.04 | 112.4 | 584.6 | 7150310544 | 4348.8 |
| P6_1-3-8 | 232.85 | 51.4 | 297.4 | 3228068076 | 4387.4 |
| P6_1-8-16 | 477.43 | 58.2 | 324.1 | 3552202892 | 4405.5 |
| P6_2-3-10 | 319.40 | 55.8 | 309.6 | 3265467425 | 4347.4 |
| P6_2-10-14 | 426.40 | 58.7 | 324.1 | 3506561508 | 4399.0 |

min / median / max: solve 232.85 / 426.40 / 3286.04 s; lrat-check 51.4 / 58.2 / 112.4 s;
cake_lpr 297.4 / 324.1 / 584.6 s; proof 3.23 / 3.51 / 7.15 GB.

P8_9-14 (one of the first-wave quadrilateral timeouts) closed at 3286 s, within the 6000 s cap.

Largest solver RSS: 4405 MB (P6_1-8-16). cake_lpr peaked at about 8.2 GB RSS.

No SAT, no proof rejection, no memory problem. Proofs were deleted by lane.py after checking.
Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

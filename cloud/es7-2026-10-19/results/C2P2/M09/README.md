# C2P2 M09: shard j = 9 of N = 42 of `C2P2.tsv` (H = 2.5 h, task commit d266d2c3)

Start 2026-10-31T06:47:53Z (epoch 1793429273), END = 1793437373 (09:02:53Z). One lane (`run.sh`), `lane.py` from `results/C2P/tools` unmodified.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch). No code was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; the cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`. Both match.
- Cubes: `l2cubes.py` output for a = 1..8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (8 rows, idx ≡ 9 mod 42; `units.tsv`)
| idx | unit | case | kind | cap | result |
|---|---|---|---|---|---|
| 9 | P8_3-10 | P8 | Q | 6000 | **certified** UNSAT |
| 51 | P6_1-2-14 | P6 | H | 1800 | **certified** UNSAT |
| 93 | P6_1-8 | P6 | Q | 2400 | UNKNOWN (timed out at the lane-reduced cap of 1214 s) |
| 135 | P6_1-15-16 | P6 | H | 1800 | not reached |
| 177 | P6_2-9-14 | P6 | H | 1800 | not reached |
| 219 | P6_3-8-11 | P6 | H | 1800 | not reached |
| 261 | P6_7-11-14 | P6 | H | 1800 | not reached |
| 303 | P6_9-10-14 | P6 | H | 1800 | not reached |

Counts:
- certified 2: P8 Q 1, P6 H 1;
- timed out 1: P6 Q 1. Its cap was 1214 s, not 2400 s, so this is not a full-cap timeout;
- not reached 5: all P6 H;
- errors 0.

## Certified units
| unit | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|
| P8_3-10 | 4637.24 | 132.7 | 691.2 | 8,555,598,452 | 4371 |
| P6_1-2-14 | 235.54 | 52.5 | 305.2 | 3,200,210,949 | 4388 |

There are only two certified units, so the median equals the mean:
- solve: 235.5 / 2436.4 / 4637.2 s (min / median / max);
- lrat-check: 52.5 / 92.6 / 132.7 s;
- cake_lpr: 305.2 / 498.2 / 691.2 s;
- proof size: 3.20 / 5.88 / 8.56 GB.

cake_lpr ran with an 8000 MB heap in both cases.

P8_3-10 is one of the first-wave quadrilateral units that timed out at the full cap. It is now refuted and certified, in 4637 s.

## Resources and anomalies
- Largest solver RSS: 4388 MB (P6_1-2-14). Peak disk use for a proof: 8.6 GB.
- No SAT, no proof rejection, no memory problem, no ERROR records.

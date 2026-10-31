# C2P2 M19

Task `results/C2P2/TASK.md` (commit d266d2c3), V = M19, LIST = C2P2.tsv, j = 19, N = 42, H = 2.5.
Start 2026-10-31 06:47:05 UTC (epoch 1793429225), END = 1793437325 (09:02:05 UTC). One lane (`run.sh`).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8)
  and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded. All 196 files matched the manifest.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) matched.
- Cubes: `l2cubes.py` output for P1..P8 was byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (8 rows with idx ≡ 19 mod 42)
| unit | case | kind | cap | result | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P8_10-15 | P8 | Q | 6000 | certified | 3808.5 | 119.4 | 640.7 | 7563202939 | 4416 |
| P6_1-3-11 | P6 | H | 1800 | certified | 344.0 | 55.5 | 325.4 | 3359579825 | 4417 |
| P6_1-9-11 | P6 | H | 1800 | certified | 313.5 | 54.6 | 321.8 | 3292516023 | 4363 |
| P6_2-3-13 | P6 | H | 1800 (cut to 1253 by END) | certified | 282.0 | 54.3 | 313.1 | 3209634522 | 4362 |
| P6_2-11 | P6 | Q | 2400 (cut to 593 by END) | UNKNOWN at 593 s | 587.8 | – | – | – | 4413 |
| P6_3-9-14 | P6 | H | 1800 | not reached | | | | | |
| P6_7-14 | P6 | Q | 2400 | not reached | | | | | |
| P6_10-11-12 | P6 | H | 1800 | not reached | | | | | |

Counts:
- Certified: 4. P8 Q: 1 (P8_10-15). P6 H: 3.
- Timed out: 1, P6 Q (P6_2-11). The lane cut its cap from 2400 s to 593 s so that 10 minutes remained before END.
  This is not a timeout at the full cap, so the unit should be run again with its full cap.
- Not reached: 3. P6 H: 2. P6 Q: 1.
- Errors: 0. Every certified record has `c VERIFIED` from lrat-check and `s VERIFIED UNSAT` from cake_lpr.

Over the 4 certified units (min / median / max):
- solve: 282.0 / 328.7 / 3808.5 s
- lrat-check: 54.3 / 55.1 / 119.4 s
- cake_lpr: 313.1 / 323.6 / 640.7 s
- proof size: 3.21 / 3.33 / 7.56 GB

Largest solver RSS: 4417 MB (P6_1-3-11). cake_lpr peaked at about 8.2 GB RSS (heap 8000 MB).

No SAT. No proof was rejected. No memory problems and no OOM.
The largest proof (7.6 GB) left at least 20 GB of disk free.

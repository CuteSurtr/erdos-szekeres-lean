# C2P2 M35 — LIST C2P2.tsv, shard j = 35 of N = 42, H = 2.5 h, TASK.md commit d266d2c3

Start 2026-10-31 06:47:41Z (epoch 1793429261); END = start + 2.5 h − 15 min = 1793437361 (09:02:41Z).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (no clone or download):
  CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch). Manifest: all 196 files match.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (b0061e90…) and base.json (2476faff…) as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 7 units: idx ≡ 35 mod 42)

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | solver RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P8_7-16 | P8 | Q | 6000 | UNKNOWN (timeout) | 5945.68 | – | – | – | 4379 |
| P6_1-4-16 | P6 | H | 1800 (run at 1335) | certified | 243.18 | 52.8 | 301.3 | 3 255 418 039 | 4405 |
| P6_1-11-14 | P6 | H | 1800 (run at 727) | certified | 263.4 | 52.1 | 303.1 | 3 249 169 267 | 4359 |
| P6_2-7-14 | P6 | H | 1800 | not reached | | | | | |
| P6_2-14-16 | P6 | H | 1800 | not reached | | | | | |
| P6_7-9-10 | P6 | H | 1800 | not reached | | | | | |
| P6_8-10-15 | P6 | H | 1800 | not reached | | | | | |

Counts by case and kind:
- P8 Q: 1 unit — 0 certified, 1 timed out (UNKNOWN at the full 6000 s cap).
- P6 H: 6 units — 2 certified, 0 timed out, 4 not reached (lane stopped at 08:51:02Z with 698 s left before END).
- Errors: none. Every certified record has `lrat_check` = `c VERIFIED` and `cake_lpr` = `s VERIFIED UNSAT`.

Certified units (n = 2; min / median / max):
- solve: 243.18 / 253.29 / 263.4 s
- lrat-check: 52.1 / 52.45 / 52.8 s
- cake_lpr: 301.3 / 302.2 / 303.1 s (heap 8000 MB)
- proof size: 3.249 / 3.252 / 3.255 GB

Note: P8_7-16, the reflection partner of the hardest first-wave subcase, also timed out at 6000 s; its LRAT
proof had reached about 10.3 GB at the cap and was deleted by lane.py.

## Resources and outcomes
- Largest solver RSS: 4404.5 MB (P6_1-4-16). No memory problem (peak system use ≈ 8 GB of 15 GB during checks).
- No SAT. No proof rejection. No `certified: false` or ERROR records.
- Disk: peak use about 22 GB of 39 GB available, during the P8_7-16 solve.

# C2P3 M44

Values: V = M44, LIST = C2P3.tsv, j = 44, N = 50, H = 2.5, Z = 4f653319. Start 2026-10-31 09:42:53Z, END 11:57:53Z (epoch 1793447873). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: the manifest matched (all 196 files). It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch) from the vendored sources. No code was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and of base.json (2476faff…) both match the expected values.
- Cubes: for P1..P8, `l2cubes.py` output was byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, 9 rows with idx ≡ 44 mod 50)

| status | count | by case/kind |
|---|---|---|
| certified UNSAT | 8 | P6 Q: 1 (P6_7-11); P6 H: 2 (P6_2-9-14, P6_7-9-16); P5 H: 5 (P5_1-2-8, P5_1-8-9, P5_2-3-11, P5_2-11-15, P5_6-10-16) |
| timed out (UNKNOWN) | 0 | |
| not reached | 1 | P5 Q: 1 (P5_7-15, cap 2400; the lane stopped with 550 s left before END) |
| errors / not certified | 0 | |

Certified units (min / median / max):
- solve: 296.0 / 397.3 / 1336.6 s (the quadrilateral P6_7-11 took 1336.6 s of its 6000 s cap; the hexagonal units took 296–566 s)
- lrat-check: 54.5 / 57.4 / 77.4 s
- cake_lpr: 318.4 / 331.1 / 418.0 s (heap 8000 MB)
- proof size: 3.27 / 3.38 / 4.50 GB (3267585361 / 3377744953 / 4501188147 bytes)

The largest solver RSS was 4411 MB, on P6_7-9-16.

There was no SAT result, no proof rejection and no memory problem. Disk use peaked at about 16 GB used, 23 GB free.

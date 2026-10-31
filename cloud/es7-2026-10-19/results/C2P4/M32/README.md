# C2P4 M32: list C2P4.tsv, shard j = 32 of N = 50, H = 2.5 h, task commit a46b478d

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing was cloned or downloaded.
- Sanity: cake_lpr example `s VERIFIED UNSAT`; both checkers reject the bad LRAT and accept the good one.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14 in `units.tsv`; lane start 13:06:12Z, END 15:16:38Z)

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P5_6-13 | P5 | Q | 6000 | certified UNSAT | 4008.78 | 140.5 | 686.2 | 7400145142 | 4370 |
| P6_8-9-12 | P6 | H | 1800 | certified UNSAT | 102.37 | 35.0 | 200.4 | 1398787065 | 3405 |
| P5_2-6-7 | P5 | H | 1800 | certified UNSAT | 288.47 | 54.2 | 342.3 | 3235741164 | 4364 |
| P5_2-12-16 | P5 | H | 1800 | certified UNSAT | 406.14 | 60.4 | 358.0 | 3344743466 | 4369 |
| P5_6-11-16 | P5 | H | 451 (cut by END) | UNKNOWN | 447.01 | – | – | – | 4369 |

- Certified: 4. P5: 1 Q, 2 H. P6: 1 H.
- Timed out (UNKNOWN): 1, P5_6-11-16 (P5, H). The lane cut its cap to 451 s so that the checks could still finish before END, so this is not a timeout at its full 1800 s cap. It stays open.
- Not reached: 9.
  - P5 H: P5_8-9-14.
  - P4: P4_2-9 (Q); P4_1-2-16, P4_1-8-16, P4_2-6-11, P4_5-8-13 and P4_6-9-12 (H).
  - P3: P3_1-8 and P3_9-11 (Q).
- Errors: 0. Proofs rejected (`certified: false`): 0.
- Certified units, min / median / max:
  - solve: 102.4 / 347.3 / 4008.8 s
  - lrat-check: 35.0 / 57.3 / 140.5 s
  - cake_lpr: 200.4 / 350.2 / 686.2 s
  - proof size: 1.40 / 3.29 / 7.40 GB
- Largest solver RSS: 4370 MB. cake_lpr peaked at about 8.2 GB RSS with an 8000 MB heap. There were no memory problems.
- No SAT. `/opt/work/SAT_FOUND` never appeared.

# C2P3 M06: shard j = 6 of N = 50 of `lists/C2P3.tsv`, H = 2.5 h

Task: `results/C2P3/TASK.md` (commit 4f653319). One machine with 4 cores and 15 GB of RAM (`env.txt`). Start 09:42:50Z (epoch 1793439770), END 11:57:50Z (epoch 1793447870). The lane ran from 09:46:40Z to 11:50:07Z.

## Tools and checks (`tools.txt`)
- The tools were built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` only. Nothing was cloned or downloaded.
  - All 196 files matched `MANIFEST.sha256`.
  - CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), and lrat-check (2e3b2dc) with the E2 patch.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`.
  - sha256 of base.cnf is `b0061e90…d8ff1`, and of base.json is `2476faff…f2b48`. Both match the expected values.
- Cubes: for a = 1..8, `l2cubes.py` produced files byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`: 10 rows with idx ≡ 6 mod 50)
| status | count | by case and kind |
|---|---|---|
| certified (UNSAT, both checkers accept) | 3 | P7 Q: 1 (P7_3-12); P6 H: 2 (P6_1-5-8, P6_2-13-16) |
| timed out (UNKNOWN) | 0 | |
| not reached | 7 | P6 H: 1 (P6_7-12-13); P5 H: 4 (P5_1-3-8, P5_1-9-13, P5_2-14-15, P5_6-13-14); P5 Q: 2 (P5_2-7, P5_8-11) |
| errors / not certified | 0 | |

Certified units (seconds; the solve caps were 6000, 1332 and 529, the last two shortened by END):
| unit | kind | solve | lrat-check | cake_lpr | proof (bytes) |
|---|---|---|---|---|---|
| P7_3-12 | Q | 4991.39 | 137.1 | 729.3 | 8,069,142,901 |
| P6_1-5-8 | H | 389.78 | 57.2 | 341.8 | 3,379,416,624 |
| P6_2-13-16 | H | 274.02 | 55.9 | 324.8 | 3,231,530,100 |

Min / median / max over the 3 certified units:
- solve: 274.02 / 389.78 / 4991.39 s
- lrat-check: 55.9 / 57.2 / 137.1 s
- cake_lpr: 324.8 / 341.8 / 729.3 s, all with the 8000 MB heap
- proof size: 3.23 / 3.38 / 8.07 GB

The proofs were deleted after checking. Their sizes and sha256 are in `out.jsonl`.

## Other
- The largest solver RSS was 4410 MB (P7_3-12). The largest cake_lpr RSS seen was about 7.9 GB. There were no memory problems.
- No SAT result, no proof rejections and no ERROR records.
- After P6_2-13-16 the lane stopped with 462 s left before END, below the 900 s needed to start a unit. The remaining 7 units were not started.

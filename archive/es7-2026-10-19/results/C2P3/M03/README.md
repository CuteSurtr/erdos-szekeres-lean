# C2P3 M03 (LIST C2P3.tsv, j = 3, N = 50, H = 2.5, task commit 4f653319)

Machine: 4 cores, 15 GB RAM (`env.txt`). Start 09:42:53Z (epoch 1793439773), lane END 1793447873 (11:57:53Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources: manifest 196/196 files match; CaDiCaL 3.0.1 (c6073042),
  cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by both
  checkers, good LRAT accepted by both. Nothing cloned or downloaded.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1`,
  base.json `2476faff…2b48` — both as expected.
- `C2C34/l2cubes.py` for a = 1..8: byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (`units.tsv`, 11 rows with idx ≡ 3 mod 50)

| idx | unit | case | kind | cap | result |
|---|---|---|---|---|---|
| 3 | P7_2-12 | P7 | Q | 6000 | certified UNSAT |
| 53 | P6_8-9 | P6 | Q | 4800 (run with 2963) | certified UNSAT |
| 103 | P7_3-9-14 | P7 | H | 1800 | certified UNSAT |
| 153 | P6_2-12-14 | P6 | H | 1800 (run with 825) | certified UNSAT |
| 203, 253, 303, 353, 403, 453, 503 | P6_7-11-14, P5_1-3, P5_1-9-10, P5_2-6-14, P5_2-13-15, P5_6-12-14, P5_8-10-12 | | | | not reached |

(The lane shortens caps to the time left before END; both shortened units finished well within the shortened cap.)

Counts by case and kind:
- Certified: 4. P7 Q 1, P7 H 1, P6 Q 1, P6 H 1.
- Timed out (UNKNOWN): 0.
- Errors / `certified: false`: 0.
- Not reached: 7. P6 H 1, P5 Q 1, P5 H 5. The lane stopped at 11:44:51Z with 781 s left, which is under the 900 s minimum to start a unit.

Certified units:

| unit | solve s | lrat-check s | cake_lpr s (heap 8000 MB) | proof bytes |
|---|---|---|---|---|
| P7_2-12 | 3591.17 | 116.4 | 616.3 | 7 372 160 841 |
| P6_8-9 | 690.66 | 59.7 | 337.7 | 3 572 242 351 |
| P7_3-9-14 | 607.69 | 63.4 | 348.7 | 3 720 152 818 |
| P6_2-12-14 | 264.47 | 55.6 | 314.0 | 3 219 279 330 |
| min / median / max | 264.47 / 649.18 / 3591.17 | 55.6 / 61.6 / 116.4 | 314.0 / 343.2 / 616.3 | 3.22 / 3.65 / 7.37 GB |

Every proof was accepted by lrat-check (`c VERIFIED`) and by cake_lpr (`s VERIFIED UNSAT`) on the first try, with no retry at 11000 MB heap. Proofs were deleted after the checks, and their sha256 values are in `out.jsonl`.

## Other observations
- Largest solver RSS: 4417 MB (P7_2-12). cake_lpr peaked at about 8.2 GB RSS. There were no memory problems.
- SAT: none. Proof rejections: none.
- Disk peaked at about 7.4 GB for the largest proof, with about 22 GB still free.

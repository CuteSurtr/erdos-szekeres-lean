# C2P3 M18 (LIST = C2P3.tsv, j = 18, N = 50, H = 2.5, task commit 4f653319)

Start 09:42:55Z (epoch 1793439775), END 1793447875 (11:57:55Z). One lane (`run.sh`), lane.py from `results/C2P/tools` unmodified.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources: manifest 196/196 files match; CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as required.
- Cubes P1..P8 from `l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 rows, idx ≡ 18 mod 50)
| unit | case | kind | status | solve s | proof GB | lrat-check s | cake_lpr s | RSS MB |
|---|---|---|---|---|---|---|---|---|
| P6_2-10 | P6 | Q | certified | 3927.4 | 7.67 | 117.1 | 639.4 | 4383 |
| P6_1-11-16 | P6 | H | certified | 326.7 | 3.34 | 55.4 | 323.2 | 4359 |
| P6_3-8-10 | P6 | H | certified | 257.0 | 3.23 | 52.2 | 309.7 | 4414 |
| P6_8-10-11 | P6 | H | certified | 25.8 | 0.22 | 12.6 | 116.2 | 2647 |
| P5_1-4-8 | P5 | H | certified | 328.6 | 3.32 | 55.9 | 324.1 | 4366 |
| P5_1-11-12 | P5 | H | certified | 264.9 | 3.20 | 51.9 | 302.2 | 4400 |
| P5_2-8-10, P5_6-7-14, P5_7-8-14 | P5 | H | not reached | | | | | |
| P5_9-11 | P5 | Q | not reached | | | | | |

Counts by case and kind:
- Certified 6: P6 Q 1, P6 H 3, P5 H 2.
- Timed out (UNKNOWN): 0.
- Not reached 4: P5 H 3, P5 Q 1 (the lane stopped at 11:51:41Z with 373 s left before END).
- Errors / `certified: false`: 0.

Certified units (min / median / max):
- solve: 25.8 / 295.8 / 3927.4 s
- lrat-check: 12.6 / 53.8 / 117.1 s
- cake_lpr: 116.2 / 316.5 / 639.4 s (all at heap 8000 MB)
- proof size: 0.22 / 3.28 / 7.67 GB (proofs deleted after checking; sizes and sha256 in `out.jsonl`)

Largest solver RSS: 4414 MB (P6_3-8-10). cake_lpr peaked at about 8.2 GB RSS.

No SAT, no proof rejection, and no memory or disk problem. The lowest free disk was about 20 GB, during the P6_2-10 proof.

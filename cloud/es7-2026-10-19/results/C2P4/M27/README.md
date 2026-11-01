# C2P4 M27

Machine M27: list `C2P4.tsv`, shard j = 27 of N = 50, H = 2.5 h, task commit Z = a46b478d. 4 cores, 15 GB RAM (`env.txt`).
Start 13:01:25Z (epoch 1793451685). END = start + 2.5 h - 15 min = 1793459785 (15:16:25Z).

## Tools and checks (`tools.txt`)

- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (all 196 files match `MANIFEST.sha256`): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check with the E2 patch (2e3b2dc). Nothing was cloned or downloaded.
- Sanity checks as expected: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match: base.cnf `b0061e90…d8ff1`, base.json `2476faff…f2b48`.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 14 rows with idx ≡ 27 mod 50)

| status | P3 | P4 | P5 | P6 | total |
|---|---|---|---|---|---|
| certified | – | 1 Q | 1 Q + 4 H | 1 H | **7** (2 Q, 5 H) |
| timed out (UNKNOWN) | – | – | – | – | 0 |
| not reached | 2 Q | 5 H | – | – | 7 |
| error / not certified | – | – | – | – | 0 |

Certified: P5_2-16 (Q), P6_7-10-15, P5_1-12-15, P5_2-10-14, P5_6-10-12, P5_7-12-14 (H), P4_1-16 (Q).
P4_1-16 got a solve cap of only 1859 s because of the time left before END (its list cap was 6000 s). It still finished UNSAT at 1762 s and was certified.

Not reached (the lane stopped at 15:13:54Z with 150 s left): P4_1-2-11, P4_1-8-11, P4_2-5-16, P4_5-7-16, P4_6-8-13 (H), and P3_1-2, P3_8-9 (Q).

Per certified unit (all 7 were accepted by both lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`, cake heap 8000 MB):

| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|
| P5_2-16 | Q | 1711.7 | 74.9 | 448.1 | 4.93 | 4375 |
| P6_7-10-15 | H | 276.6 | 48.0 | 310.5 | 3.16 | 4349 |
| P5_1-12-15 | H | 278.9 | 50.0 | 319.8 | 3.24 | 4416 |
| P5_2-10-14 | H | 531.0 | 53.0 | 336.3 | 3.51 | 4356 |
| P5_6-10-12 | H | 92.6 | 23.2 | 175.9 | 1.17 | 3156 |
| P5_7-12-14 | H | 243.6 | 49.3 | 306.5 | 3.09 | 4334 |
| P4_1-16 | Q | 1762.3 | 72.8 | 441.1 | 5.03 | 4416 |

Min / median / max: solve 92.6 / 278.9 / 1762.3 s, lrat-check 23.2 / 50.0 / 74.9 s, cake_lpr 175.9 / 319.8 / 448.1 s, proof 1.17 / 3.24 / 5.03 GB.

Largest solver RSS: 4416 MB.

## Problems

None. There was no SAT, no proof rejection, no error record and no memory problem. Free disk never went below about 23 GB.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

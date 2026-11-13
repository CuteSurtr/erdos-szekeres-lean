# C2P4 M45 (LIST = C2P4.tsv, j = 45, N = 50, H = 2.5, TASK @ a46b478d)

Start 2026-10-31 13:02:09Z (epoch 1793451729), END 1793459829 (15:17:09Z). Lane started 13:03:59Z, finished 15:03:27Z
("stop: 821 s left": fewer than 15 minutes before END, so the next unit was not started).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from vendored sources (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042),
  cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1`, base.json `2476faff…2b48`: both match.
- Cubes P1..P8 from `l2cubes.py`: all byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (18 = rows of C2P4.tsv with idx ≡ 45 mod 50)

| case | kind | units | certified UNSAT | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P5 | Q | 1 | 1 | 0 | 0 | 0 |
| P5 | H | 5 | 5 | 0 | 0 | 0 |
| P4 | Q | 1 | 1 | 0 | 0 | 0 |
| P4 | H | 5 | 3 | 0 | 2 | 0 |
| P3 | Q | 1 | 0 | 0 | 1 | 0 |
| P3 | H | 5 | 0 | 0 | 5 | 0 |
| **total** | | **18** | **10** | **0** | **8** | **0** |

Certified (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`): P5_8-11, P5_1-7-9, P5_2-7-14, P5_6-7-16,
P5_7-8-15, P5_9-11-13, P4_6-7, P4_1-5-12, P4_1-10-16, P4_2-8-10.

Not reached: P4_5-10-13, P4_6-12-14 (H), P3_4-9 (Q), P3_1-4-10, P3_1-8-16, P3_4-6-11, P3_4-13-15, P3_6-7-9 (H).

Certified units, min / median / max:
- solve: 23.66 / 358.5 / 607.57 s (Q: P5_8-11 607.57, P4_6-7 471.73)
- lrat-check: 13.6 / 53.1 / 60.7 s
- cake_lpr: 116.9 / 309.6 / 350.8 s
- proof size: 0.218 / 3.41 / 3.73 GB (217926384 / 3410032625.5 / 3726005719 bytes)

Largest solver RSS: 4406 MB (P5_1-7-9). No memory problem.

No SAT, no proof rejection, no `certified: false` record, no ERROR status.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (10 records), `lane.log.tail`.

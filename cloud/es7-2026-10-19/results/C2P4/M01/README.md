# C2P4 M01

Machine M01 of the fourth wave on the parallelogram cases (task `results/C2P4/TASK.md`, commit a46b478d), with LIST = `C2P4.tsv`, shard j = 1 of N = 50, budget H = 2.5 h. Start 2026-10-31 13:01:30Z (epoch 1793451690), END = 1793459790 (15:16:30Z). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)

- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity checks as expected: cake_lpr example `s VERIFIED UNSAT`; the bad LRAT is rejected by both checkers and the good one accepted by both.
- Base CNF `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: header `p cnf 838032 16653336`, sha256 of base.cnf (b0061e90…) and base.json (2476faff…) as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 13 rows with idx ≡ 1 mod 50)

One lane (`run.sh`), records in `out.jsonl`, log in `lane.log.tail`.

| unit | case | kind | cap | result | solve s | lrat-check s | cake_lpr s | proof | solver RSS |
|---|---|---|---|---|---|---|---|---|---|
| P6_8-13 | P6 | Q | 7000 | **certified UNSAT** (c VERIFIED, s VERIFIED UNSAT, heap 8000 MB) | 4487.9 | 108.2 | 593.6 | 6.23 GB (6233149508 B) | 4472 MB |
| P4_6-12 | P4 | Q | 6000 (lane capped it at 2092) | UNKNOWN (timed out at 2092 s) | 2074.1 | – | – | – | 4377 MB |
| 11 others | P4 ×5, P3 ×6 | P4: 5 H; P3: 1 Q + 5 H | | not reached | | | | | |

By case and kind:
- P6: Q certified 1 (P6_8-13).
- P4: Q timed out 1 (P4_6-12, only 2092 s of its 6000 s cap, because the lane limits each solve to the time left before END − 10 min); H not reached 5 (P4_1-6-7, P4_1-11-16, P4_2-9-11, P4_5-11-13, P4_7-9-11).
- P3: Q not reached 1 (P3_5-9); H not reached 5 (P3_1-5-10, P3_1-10-14, P3_4-7-13, P3_5-7-8, P3_6-8-14).
- Totals: 1 certified, 1 UNKNOWN, 11 not reached, 0 errors.

Certified units (only one, so minimum = median = maximum): solve 4487.9 s, lrat-check 108.2 s, cake_lpr 593.6 s, proof 6.23 GB. The proof was deleted after the checks (sha256 89fa5703… in `out.jsonl`).

Note on P4_6-12: its UNKNOWN is a budget cut at 2092 s, not a timeout at its full 6000 s cap, so it is still open at the full cap.

## Other

- Largest solver RSS: 4472 MB (P6_8-13); no memory problem. Disk stayed above 22 GB free.
- No SAT, no proof rejection, no `ERROR` status, no `"certified": false` record.

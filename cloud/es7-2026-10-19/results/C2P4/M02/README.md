# C2P4 M02 — fourth wave on the parallelogram cases, shard j = 2 of N = 50 of `lists/C2P4.tsv`

Task: `results/C2P4/TASK.md` at commit a46b478d; H = 2.5 h. Start 2026-10-31 13:01:35Z (epoch 1793451695),
END = start + 2.5 h − 15 min = 1793459795 (15:16:35Z). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources: manifest all 196 files match; CaDiCaL 3.0.1 (c6073042),
  cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`);
  cake_lpr example `s VERIFIED UNSAT`.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`): header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1`,
  base.json `2476faff…bf472b48`. Both match.
- Cubes P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (15 = rows with idx ≡ 2 mod 50; `units.tsv`)

| status | count | by case / kind |
|---|---|---|
| certified (UNSAT, both checkers accepted) | 1 | P6 Q: P6_8-14 |
| timed out (UNKNOWN) | 1 | P4 Q: P4_6-13 (cap cut to 2222 s by the time left; list cap 6000 s) |
| not reached | 13 | P4 H: 5 (P4_1-6-8, P4_1-12-13, P4_2-9-12, P4_5-11-14, P4_7-9-12); P3 Q: 1 (P3_5-10); P3 H: 5 (P3_1-5-11, P3_1-10-15, P3_4-7-14, P3_5-7-9, P3_6-9-10). |
| errors / certified false | 0 | — |

Certified unit (only one, so min = median = max):
- P6_8-14 (Q, cap 7000 s): solve 4246.42 s (wall 4283.8 s); lrat-check 135.8 s `c VERIFIED`; cake_lpr 695.2 s
  (heap 8000 MB) `s VERIFIED UNSAT`; proof 7,734,661,804 bytes (7.7 GB, text LRAT), sha256 `354f069f…40b9ff90`;
  CNF sha256 `01bd0d03…f6ab1cd2`. The proof was deleted after the checks.

P4_6-13 stays open: it ran 2199.57 s of solve time (wall 2222.3 s) at a cap reduced by the lane's 10-minute check reserve,
far below its 6000 s list cap, so this attempt does not count as a full-cap timeout.

## Resources and problems
- Largest solver RSS: 4386.14 MB (P4_6-13); P6_8-14 4356.47 MB. No memory problem.
- Disk: the largest proof was 7.7 GB; at least 19 GB stayed free.
- No SAT, no proof rejection, no error. The lane stopped at 15:06:42Z (592 s left before END, below the 15-minute start threshold).

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh` (lane command), `out.jsonl` (2 records), `lane.log.tail`.

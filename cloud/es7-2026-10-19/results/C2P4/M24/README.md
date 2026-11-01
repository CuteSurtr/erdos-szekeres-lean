# C2P4 M24: shard 24 of 50 of `lists/C2P4.tsv` (H = 2.5 h, task commit a46b478d)

One lane, `run.sh`. Started 13:01:22Z; END = start + 2.5 h − 15 min = 15:16:22Z. The machine had 4 cores and 15 GB RAM, with no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` checked all 196 files of the vendored sources against `MANIFEST.sha256`. It then built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). No code was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…d8ff1) and of base.json (2476faff…bb48) match the expected values.
- Cubes: `l2cubes.py` for P1..P8 was byte-identical to `C2P/cubes/P{a}_cubes.txt` (560 lines each).

## Units (19: idx ≡ 24 mod 50)
| status | count | by case / kind |
|---|---|---|
| certified (UNSAT, both checkers accepted) | 6 | P5: 1 Q + 4 H; P6: 1 H |
| timed out (UNKNOWN) | 1 | P4_1-13 (Q), but only at a cap shortened to 946 s by the END budget (see below) |
| not reached | 12 | P4: 6 H; P3: 1 Q + 5 H |
| errors / certified false | 0 | |

| unit | kind | cap s | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|
| P5_2-13 | Q | 6000 | 2307.6 | 99.6 | 530.6 | 5,679,035,423 | 4377 |
| P6_3-10-11 | H | 1800 | 275.3 | 54.6 | 312.8 | 3,250,112,412 | 4395 |
| P5_1-10-15 | H | 1800 | 380.9 | 57.8 | 329.5 | 3,451,705,014 | 4408 |
| P5_2-9-13 | H | 1800 | 469.8 | 60.2 | 352.3 | 3,577,580,325 | 4414 |
| P5_6-9-15 | H | 1800 | 342.0 | 64.1 | 341.3 | 3,321,023,526 | 4368 |
| P5_7-11-14 | H | 1266* | 100.9 | 29.1 | 185.1 | 1,314,124,413 | 3412 |
| P4_1-13 | Q | 946* | UNKNOWN at 937.7 | – | – | – | 4386 |

\* The lane cut the cap to fit before END.

Certified units (min / median / max):
- solve: 100.9 / 361.4 / 2307.6 s
- lrat-check: 29.1 / 59.0 / 99.6 s
- cake_lpr: 185.1 / 335.4 / 530.6 s
- proof size: 1.31 / 3.39 / 5.68 GB

Not reached:
- P4: P4_1-2-8, P4_1-7-16, P4_2-5-13, P4_5-7-13, P4_6-8-10, P4_8-11-12 (all H)
- P3: P3_7-11 (Q), P3_1-7-9, P3_4-5-6, P3_4-9-16, P3_5-9-13, P3_7-9-10 (H)

P4_1-13 is still open. It timed out only at the shortened 946 s cap, not at its full 6000 s cap, so it should be run again at its full cap.

## Other
- Largest solver RSS: 4414 MB. The cake_lpr heap was 8000 MB, and free memory was ~7 GB during the checks. There were no memory problems.
- No SAT, no proof rejection and no ERROR records.

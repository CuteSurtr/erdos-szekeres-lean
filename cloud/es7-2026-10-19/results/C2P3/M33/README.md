# C2P3 M33 — shard j=33 of N=50 of `lists/C2P3.tsv` (task commit 4f653319, H = 2.5)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 09:42:54Z, END 11:57:54Z (epoch 1793447874), see `run.sh`.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources. The manifest matched (all 196 files). CaDiCaL is 3.0.1, cake_lpr a36874a8, and lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity checks:
  - Both checkers rejected the bad LRAT and accepted the good one.
  - The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336`. The sha256 of base.cnf and of base.json both match the expected values.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 in shard: idx 33, 83, ..., 483)
| unit | case | kind | cap | result |
|---|---|---|---|---|
| P6_2-8 | P6 | Q | 6000 | **certified** UNSAT |
| P6_9-14 | P6 | Q | 4800 (lane cut it to 2945) | timed out (UNKNOWN) after solve 2913.65 s |
| P6_2-7-14, P6_7-8-11, P6_9-11-12 | P6 | H | 1800 | not reached |
| P5_1-7, P5_2-10, P5_7-11 | P5 | Q | 2400 | not reached |
| P5_1-14-15, P5_6-9-12 | P5 | H | 1800 | not reached |

Counts by case and kind:
- P6 Q: 1 certified, 1 timed out.
- P6 H: 3 not reached.
- P5 Q: 3 not reached.
- P5 H: 2 not reached.

Errors: none.

Certified unit (only one, so the minimum, median and maximum are all this unit):
- P6_2-8:
  - solve 3549.83 s (wall 3585.7 s);
  - lrat-check 121.9 s, `c VERIFIED`;
  - cake_lpr 660.0 s, `s VERIFIED UNSAT`;
  - proof 7,564,119,949 bytes (sha256 ab986177…7bb1), deleted after the checks.

Largest solver RSS: 4413 MB (P6_2-8). P6_9-14 reached 4359 MB. cake_lpr peaked at about 8 GB.

There was no SAT, no proof rejection and no memory problem. At most 49% of the disk was used.

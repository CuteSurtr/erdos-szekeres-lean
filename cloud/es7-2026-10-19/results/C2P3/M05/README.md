# C2P3 M05: shard j = 5 of N = 50 of `lists/C2P3.tsv`, H = 2.5 h (TASK commit 4f653319)

Started 09:42:41 UTC on 2026-10-31. Lane END = 11:57:41 UTC (start + 2.5 h − 15 min). The machine had 4 cores and 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources: all 196 MANIFEST files matched. The tools are CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, and lrat-check from drat-trim 2e3b2dc with the E2 patch. No code was downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example gave `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values match the expected ones (base.cnf b0061e90…, base.json 2476faff…).
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 in `units.tsv`)
| result | count | by case and kind |
|---|---|---|
| certified UNSAT | 7 | P7 Q: 1 (P7_3-10); P6 H: 3 (P6_1-2-5, P6_2-13-14, P6_7-11-16); P5 H: 3 (P5_1-3-7, P5_1-9-12, P5_2-6-16) |
| timed out (UNKNOWN) | 0 | – |
| not reached | 3 | P5 Q: 2 (P5_2-14, P5_6-13); P5 H: 1 (P5_8-10-14). The lane stopped at 11:52:09 with 331 s left before END |
| errors / certified false | 0 | – |

Certified units (all `c VERIFIED` and `s VERIFIED UNSAT`):

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|
| P7_3-10 | Q | 3252.62 | 105.1 | 558.0 | 7412360993 | 4392.91 |
| P6_1-2-5 | H | 65.40 | 22.0 | 153.0 | 1110699132 | 3126.27 |
| P6_2-13-14 | H | 223.05 | 47.6 | 288.4 | 3200734645 | 4383.83 |
| P6_7-11-16 | H | 390.94 | 55.7 | 323.7 | 3380869944 | 4392.50 |
| P5_1-3-7 | H | 265.50 | 54.4 | 300.5 | 3243282486 | 4427.44 |
| P5_1-9-12 | H | 340.42 | 53.2 | 307.1 | 3385410508 | 4358.74 |
| P5_2-6-16 | H | 357.95 | 50.8 | 305.5 | 3551015077 | 4421.04 |

Min / median / max over the 7 certified units:
- solve: 65.4 / 340.4 / 3252.6 s
- lrat-check: 22.0 / 53.2 / 105.1 s
- cake_lpr: 153.0 / 305.5 / 558.0 s
- proof: 1.11 / 3.38 / 7.41 GB

Largest solver RSS: 4427 MB (P5_1-3-7).

Problems: no SAT, no proof rejections and no memory problems. Disk peaked at about 19 GB used, with about 21 GB free, during the 7.4 GB P7_3-10 proof.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.

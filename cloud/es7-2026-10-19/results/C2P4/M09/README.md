# C2P4 M09: shard j = 9 of N = 50 of `lists/C2P4.tsv`

Task: `results/C2P4/TASK.md` at commit a46b478d. V = M09, LIST = C2P4.tsv, j = 9, N = 50, H = 2.5.
Start 2026-10-31 13:01:26 UTC (epoch 1793451686). END = 1793459786 (15:16:26 UTC). Machine: 4 cores, 15 GB RAM, no swap (`env.txt`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only. All 196 manifest hashes matched.
  The sources are CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 and lrat-check 2e3b2dc with the E2 patch.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- The cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (13: idx ≡ 9 mod 50, `units.tsv`)

| idx | unit | case | kind | cap | result |
|---|---|---|---|---|---|
| 9 | P5_1-12 | P5 | Q | 7000 | **certified UNSAT** (solve 2788.2 s) |
| 59 | P4_7-12 | P4 | Q | 6000 (lane cap 3846) | **certified UNSAT** (solve 1655.1 s) |
| 109 | P4_1-6-15 | P4 | H | 1800 (lane cap 1649) | **certified UNSAT** (solve 460.1 s) |
| 159 | P4_1-14-15 | P4 | H | 1800 (lane cap 782) | **certified UNSAT** (solve 238.5 s) |
| 209 | P4_5-6-12 | P4 | H | 1800 | not reached |
| 259 | P4_5-14-15 | P4 | H | 1800 | not reached |
| 309 | P4_7-11-12 | P4 | H | 1800 | not reached |
| 359 | P3_6-8 | P3 | Q | 6000 | not reached |
| 409 | P3_1-6-8 | P3 | H | 1800 | not reached |
| 459 | P3_1-12-13 | P3 | H | 1800 | not reached |
| 509 | P3_4-8-13 | P3 | H | 1800 | not reached |
| 559 | P3_5-8-9 | P3 | H | 1800 | not reached |
| 609 | P3_6-10-13 | P3 | H | 1800 | not reached |

Note: the shard has 13 units (not 14). The lane stopped at 15:03:39 with 766 s left, which is under 15 minutes, so it started nothing more.

Counts by case and kind:
- Certified: 4. These are P5 Q 1, P4 Q 1 and P4 H 2.
- Timed out (UNKNOWN): 0.
- Errors: 0.
- Not reached: 9. These are P4 H 3, P3 Q 1 and P3 H 5.

Certified units (min / median / max):
- solve: 238.5 / 1057.6 / 2788.2 s
- lrat-check: 53.5 / 69.6 / 105.4 s, all `c VERIFIED`
- cake_lpr: 312.8 / 383.4 / 547.0 s, all `s VERIFIED UNSAT`, heap 8000 MB
- proof size: 3.24 / 4.30 / 6.06 GB (3235448580 / 4304204016 / 6057993282 bytes). Each proof was deleted after both checks.

Largest solver RSS: 4405.8 MB (P4_7-12).

No SAT, no proof rejection, no `certified: false` record, no ERROR status and no memory problem.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (4 records) and `lane.log.tail`.

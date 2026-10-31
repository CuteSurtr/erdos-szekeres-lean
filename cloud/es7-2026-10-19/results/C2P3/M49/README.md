# C2P3 M49: shard j=49 of N=50 of lists/C2P3.tsv (task commit 4f653319, H = 2.5)

The machine has 4 cores, 15 GB RAM and no swap (`env.txt`). Start time 09:42:51Z (epoch 1793439771). Lane END = 1793447871 (11:57:51Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources (`manifest: all 196 files match`): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: the header is `p cnf 838032 16653336` and both sha256 values match (base.cnf b0061e90…, base.json 2476faff…).
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (9 assigned, `units.tsv`)
| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P6_7-16 | P6 | Q | 6000 | UNSAT, **certified** | 5462.9 | 146.6 | 770.1 | 9.86 GB | 4380 |
| P6_2-11-13 | P6 | H | 864 (cap cut to fit before END) | UNSAT, **certified** | 289.6 | 50.8 | 297.9 | 3.25 GB | 4451 |
| P6_7-10-15, P5_1-2-13, P5_1-8-14, P5_2-6-10, P5_2-12-15, P5_6-11-15, P5_8-9-13 | P6 ×1 H, P5 ×6 H | H | 1800 | not reached | | | | | |

Counts by case and kind:
- Certified: 2 (P6 Q: 1, P6 H: 1).
- Timed out (UNKNOWN): 0.
- Errors: 0.
- Not reached: 7 (P6 H: 1, P5 H: 6). The lane stopped at 11:44:17Z with 813 s left, which is under the 15-minute margin.

Certified units, minimum / median / maximum over the 2 units (with two values, the median is their mean):
- solve: 289.6 / 2876.2 / 5462.9 s
- lrat-check: 50.8 / 98.7 / 146.6 s
- cake_lpr: 297.9 / 534.0 / 770.1 s
- proof size: 3.25 / 6.55 / 9.86 GB

Largest solver RSS: 4451 MB.

No SAT, no proof rejection and no memory problem. Disk was never below 18 GB free. Every proof was deleted after its checks.

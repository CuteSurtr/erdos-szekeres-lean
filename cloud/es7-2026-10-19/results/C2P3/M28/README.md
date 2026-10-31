# C2P3 M28 (LIST = C2P3.tsv, j = 28, N = 50, H = 2.5, Z = 4f653319)

Start 2026-10-31 09:42:49Z (epoch 1793439769), END = 1793447869 (12:07:49Z). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built from the vendored sources only. All files matched `MANIFEST.sha256`. Builds: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch).
- Sanity checks: the cake_lpr example printed `s VERIFIED UNSAT`. Both checkers rejected the bad LRAT and accepted the good one.
- Base CNF: header `p cnf 838032 16653336`. The sha256 values of base.cnf (b0061e90…d8ff1) and base.json (2476faff…bb48) match.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (10 assigned, `units.tsv`)
| unit | case | kind | cap | result |
|---|---|---|---|---|
| P6_1-12 | P6 | Q | 6000 | **certified UNSAT**: solve 3676.7 s, lrat-check 97.3 s, cake_lpr 573.8 s, proof 6.60 GB (6601937666 B) |
| P6_8-14 | P6 | Q | 4800 (reduced to 2936 by END) | UNKNOWN (timed out at 2906.5 s) |
| P6_2-4-7, P6_3-10-11, P6_8-12-14 | P6 | H | 1800 | not reached |
| P5_1-6-12, P5_2-9-12, P5_6-8-15, P5_7-10-11 | P5 | H | 1800 | not reached |
| P5_1-13 | P5 | Q | 2400 | not reached |

Counts by case and kind:
- Certified: 1 (P6 Q).
- Timed out: 1 (P6 Q).
- Not reached: 8 (P6 H 3, P5 H 4, P5 Q 1).
- Errors: 0.

There is only one certified unit, so its min = median = max: solve 3676.7 s, lrat-check 97.3 s, cake_lpr 573.8 s (heap 8000 MB), proof 6.60 GB.

- Largest solver RSS: 4373 MB (P6_1-12). P6_8-14 reached 4356 MB.
- No SAT, no proof rejection, no `certified: false` record, and no memory or disk problem. Disk use peaked at about 18 GB used with 21 GB still free.
- Note: P6_8-14 got only 2936 s instead of its 4800 s cap, because the lane caps each solve to leave 10 minutes before END. It is still open.

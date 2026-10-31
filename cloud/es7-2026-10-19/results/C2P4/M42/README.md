# C2P4 M42 (LIST = C2P4.tsv, j = 42, N = 50, H = 2.5, task commit a46b478d)

## Tools and checks
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Manifest: all 196 files match.
- Sanity: both checkers rejected the bad LRAT and accepted the good one; the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 of base.cnf (b0061e90…) and base.json (2476fafff…) both match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`. Machine: 4 cores, 15 GB RAM (`env.txt`).

## Units (19 assigned: P5 1 Q + 5 H, P4 1 Q + 5 H, P3 1 Q + 6 H)
Lane start 13:03:37Z, END 1793459786 (15:16:26Z).

| unit | case | kind | status | cap | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|---|---|---|
| P5_7-15 | P5 | Q | **UNSAT, certified** | 6000 | 5748.9 | 128.7 | 746.0 | 8,161,228,210 |
| P5_1-6-11 | P5 | H | UNKNOWN (timeout at cap reduced to 665 s by END) | 665 | 659.1 | – | – | – |

- **Certified: 1.** P5 Q: 1. With only one certified unit, the minimum, median and maximum are all that unit: solve 5748.9 s, lrat-check 128.7 s, cake_lpr 746.0 s, proof 8.16 GB.
- **Timed out (UNKNOWN): 1.** P5 H: 1 (P5_1-6-11). It ran under a 665 s cap, not its full 1800 s cap, so this is not a real 1800 s timeout.
- **Not reached: 17.**
  - P5 H: 4 (P5_2-7-11, P5_6-7-13, P5_7-8-12, P5_9-10-12).
  - P4: 1 Q (P4_5-14) and 5 H (P4_1-5-9, P4_1-10-13, P4_2-7-13, P4_5-9-16, P4_6-11-13).
  - P3: 1 Q (P3_4-6) and 6 H (P3_1-4-7, P3_1-8-13, P3_4-6-8, P3_4-12-14, P3_5-12-14, P3_8-10-12).
- **Errors / certified false: none.**

## Resources
- Largest solver RSS: 4380 MB (P5_7-15). No memory problems.
- No SAT and no proof rejections.

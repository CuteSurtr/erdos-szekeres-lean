# C2P4 M23 (LIST = C2P4.tsv, shard j = 23 of N = 50, H = 2.5 h, task commit a46b478d)

## Tools and checks
- `C2P/vendor/build_tools.sh` built everything from the vendored `tools-src.tar.xz`: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). The manifest check reported all 196 files matching.
- Sanity: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. Both sha256 values matched: base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Details are in `tools.txt`.

## Units (20 assigned: P5 1 Q + 4 H, P6 1 H, P4 1 Q + 6 H, P3 1 Q + 5 H)
- One lane (`run.sh`) started 13:04:34Z with END 15:16:33Z. It stopped at 15:05:02Z with 690 s left.
- **Certified (UNSAT, both checkers accepted): 5**
  - P5 Q: P5_2-12
  - P5 H: P5_1-10-14, P5_2-9-12, P5_6-9-14
  - P6 H: P6_3-9-14
- **Timed out (UNKNOWN): 0.**
- **Errors or certified=false: 0.**
- **Not reached: 15**

| case | Q not reached | H not reached |
|---|---|---|
| P5 | – | P5_7-11-13 |
| P4 | P4_1-12 | P4_1-2-7, P4_1-7-15, P4_2-5-12, P4_5-7-12, P4_6-8-9, P4_8-10-13 |
| P3 | P3_7-10 | P3_1-7-8, P3_1-15-16, P3_4-9-15, P3_5-9-12, P3_7-8-13 |

| unit | kind | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|
| P5_2-12 | Q | 3127.56 | 86.4 | 549.6 | 6155280349 |
| P6_3-9-14 | H | 772.84 | 56.2 | 361.8 | 3753717801 |
| P5_1-10-14 | H | 428.92 | 47.9 | 314.2 | 3414670070 |
| P5_2-9-12 | H | 400.87 | 47.9 | 312.0 | 3398765749 |
| P5_6-9-14 | H | 269.56 | 42.4 | 303.1 | 3175410798 |

Certified units (min / median / max):
- solve: 269.6 / 428.9 / 3127.6 s
- lrat-check: 42.4 / 47.9 / 86.4 s
- cake_lpr: 303.1 / 314.2 / 549.6 s
- proof: 3.18 / 3.40 / 6.16 GB

## Memory, SAT, rejections
- Largest solver RSS: 4409.8 MB (P5_6-9-14). cake_lpr ran with an 8000 MB heap, at about 8.2 GB RSS.
- There were no memory problems. Disk stayed at 22 GB or more free.
- No SAT. No proof was rejected.

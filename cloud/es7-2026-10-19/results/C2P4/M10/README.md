# C2P4 M10

Task `results/C2P4/TASK.md` (commit a46b478d), V = M10, LIST = C2P4.tsv, j = 10, N = 50, H = 2.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 13:01 UTC, lane 13:05:17Z, END = 1793459783 (15:16:23Z); lane done 15:01:51Z.

## Tools and checks (`tools.txt`)
- Built by `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code cloned or downloaded.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`; sha256 base.cnf `b0061e90…d8ff1` and base.json `2476fafff…bf472b48`, both as expected.
- Cubes P1..P8 from `C2C34/l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (13 = rows idx ≡ 10 mod 50, `units.tsv`)

| status | count | units |
|---|---|---|
| certified (UNSAT, both checkers accept) | 3 | P5_2-8 (Q), P4_7-13 (Q), P4_1-6-16 (H) |
| timed out (UNKNOWN) | 0 | |
| not reached (stop at 15:01:51Z, 871 s left < 15 min) | 10 | P4: 6-7-8, 1-14-16, 5-6-13, 7-11-13 (H); P3: 6-9 (Q), 1-6-9, 1-12-14, 4-8-14, 5-8-10, 6-10-14 (H) |
| errors / not certified | 0 | |

By case and kind: P5 Q certified 1/1; P4 Q certified 1/1; P4 H certified 1/5 (4 not reached); P3 Q 0/1 and P3 H 0/5 (all not reached).

Certified units:

| unit | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P5_2-8 | Q | 7000 | 2512.1 | 111.7 | 560.8 | 6.02 | 4418 |
| P4_7-13 | Q | 4042 | 2304.1 | 94.0 | 531.5 | 5.86 | 4358 |
| P4_1-6-16 | H | 1075 | 394.1 | 58.6 | 338.5 | 3.57 | 4418 |

Min / median / max: solve 394.1 / 2304.1 / 2512.1 s; lrat-check 58.6 / 94.0 / 111.7 s; cake_lpr 338.5 / 531.5 / 560.8 s; proof 3.57 / 5.86 / 6.02 GB.
(The caps of P4_7-13 and P4_1-6-16 were reduced by lane.py to fit before END.)

Largest solver RSS: 4418 MB (P4_1-6-16). No SAT, no proof rejection, no memory or disk problem (min free disk 22 GB). All proofs deleted after checking.

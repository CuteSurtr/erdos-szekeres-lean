# C2P5 M19

Machine M19, LIST `C2P5A.tsv`, j = 19, N = 37, H = 4.5, Z = 81cb025f. Start 18:50:31Z, END 23:05:31Z (epoch 1793487931). The lane finished all units at 20:23:21Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored sources: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, with the E2 patch). Manifest: all 196 files match.
- Sanity checks as expected: both checkers rejected the bad LRAT and accepted the good one, and the cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- l2cubes.py output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (idx ≡ 19 mod 37 of C2P5A.tsv): 5 units, all case P4
| unit | kind | cap | status | solve s | RSS MB | proof bytes | lrat-check s | cake_lpr s | certified |
|---|---|---|---|---|---|---|---|---|---|
| P4_2-10 | Q | 8000 | UNSAT | 2257.76 | 4420 | 5561404968 | 96.7 | 515.1 | true |
| P4_2-5-12 | H | 2400 | UNSAT | 469.41 | 4419 | 3611100299 | 59.4 | 351.5 | true |
| P4_2-8-11 | H | 2400 | UNSAT | 353.52 | 4401 | 3334140882 | 58.6 | 332.9 | true |
| P4_5-10-11 | H | 2400 | UNSAT | 26.47 | 2646 | 216632420 | 13.8 | 117.6 | true |
| P4_6-10-15 | H | 2400 | UNSAT | 324.73 | 4360 | 3301518478 | 58.1 | 331.3 | true |

Counts by case and kind:
- P4 Q: 1 certified.
- P4 H: 4 certified.
- 0 timed out (UNKNOWN), 0 not reached, 0 errors.

Certified units, min / median / max:
- solve s: 26.47 / 353.52 / 2257.76
- lrat-check s: 13.8 / 58.6 / 96.7
- cake_lpr s: 117.6 / 332.9 / 515.1
- proof bytes: 216632420 / 3334140882 / 5561404968 (0.22 / 3.33 / 5.56 GB)

Largest solver RSS: 4420 MB (P4_2-10). cake_lpr ran with an 8000 MB heap.

There was no SAT answer, no proof rejection and no memory problem. Disk use peaked at about 17 GB of 39 GB, during the P4_2-10 proof.

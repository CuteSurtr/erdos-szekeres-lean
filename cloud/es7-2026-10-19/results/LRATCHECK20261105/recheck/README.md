# cake_lpr re-checks of lrat-check-only claims (5 November 2026, 13:19–13:30 KST)

These items come from `../AUDIT.md` §4. For each one:
1. The CNFs were regenerated with the record's own generator, and their SHA-256 was compared with the recorded hash.
2. Each was solved with CaDiCaL 2.1.3.
3. Each was checked with cake_lpr; the verdict counts only if the log contains the exact line `s VERIFIED UNSAT`.
4. Every artifact was kept outside Git (`<recheck-dir>`, 1.5 GB), with SHA-256 in `*/all_hashes.txt`.

The coordinator re-checked every verdict line and every hash file.

| Item | Instances | Hash match | cake_lpr VERIFIED | Note |
|---|---:|---:|---:|---|
| PRIMEFOLD Theorem E (`clsat.py`, `clsat2.py`) | 7 | 7 (full hash) | 7 | **The only headline item the audit flagged. Now certified by cake_lpr.** Lemma 1, Proposition C (i) and the encoding remain written arguments. |
| PRIMEFOLD, independent encoder `enc_te.py` | 10 UNSAT + 5 SAT controls | 10 (prefix) | 10 | The 5 SAT controls have models checked against every clause. |
| C7UPPER calibration (m,K) = (3,4)…(6,7) | 4 | 4 | 4 | |
| ES8SYM single-orbit bounds (m = 6, n = 10; m = 5, n = 11) | 2 | 2 | 2 | |
| MIRRORETV, N(7,4,7) <= 16 at 17 points | 2 of 4 encodings | 2 | 2 | No generator exists for the other two (never committed). The Lean proof from Baek's theorem is unaffected. |
| ROT456, layer-5 patterns of cube d111111 | 11 | base CNF full hash | 11 | |
| C/C2 encoding controls | 7 | 7 (sibling records Mi-0/Mii-3) | 7 | C and C2 recorded no CNF hashes. |
| E, n18k6m3 control (3 cubes) | 3 | base CNF full hash | 3 | |

The proofs differ from the recorded ones where the original runs used CaDiCaL 3.0.1. The CNFs are the bound
objects, so a different proof of the same CNF certifies the same claim. SYM5 L2 was not re-checked: it is
redundant, since P1 and L1 settle Theorem 5 and both were accepted by cake_lpr.

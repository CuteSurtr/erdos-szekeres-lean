# C2P5 M18

Task: `results/C2P5/TASK.md` (commit 81cb025f) with V = M18, LIST = C2P5A.tsv, j = 18, N = 37, H = 4.5.
Start 1793472622 (2026-10-31 18:50:22Z), END 1793487922. Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc, E2 patch).
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 of base.cnf and base.json match the expected values.
- Cubes P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.
- Note: the sha256 of the built cadical binary (268d1bfc…) differs from the one recorded by M65; the build is not byte-reproducible across machines, but the source manifest matched.

## Units (rows of C2P5A.tsv with idx ≡ 18 mod 37)
| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P4_2-9 | P4 | Q | 8000 | UNSAT, certified | 2000.73 | 88.5 | 476.2 | 5508610539 | 4412 |
| P4_2-5-11 | P4 | H | 2400 | UNSAT, certified | 437.77 | 56.4 | 325.7 | 3536670491 | 4415 |
| P4_2-8-9 | P4 | H | 2400 | UNSAT, certified | 270.27 | 53.2 | 302.1 | 3211442865 | 4369 |
| P4_5-9-16 | P4 | H | 2400 | UNSAT, certified | 493.80 | 54.8 | 331.0 | 3611899976 | 4386 |
| P4_6-10-14 | P4 | H | 2400 | UNSAT, certified | 238.03 | 50.7 | 309.9 | 3171672725 | 4351 |

Counts: 5 of 5 certified (P4: Q 1/1, H 4/4); 0 timed out (UNKNOWN); 0 not reached; 0 errors.

Certified units, min / median / max:
- solve: 238.03 / 437.77 / 2000.73 s
- lrat-check: 50.7 / 54.8 / 88.5 s
- cake_lpr: 302.1 / 325.7 / 476.2 s
- proof size: 3.17 / 3.54 / 5.51 GB (all proofs deleted after checking)

Largest solver RSS: 4415 MB (P4_2-5-11).

No SAT, no proof rejection, no memory problem. The lane finished all units at 20:25:12Z, well before END.
Files: `out.jsonl` (one record per unit), `lane.log.tail`, `units.tsv`, `run.sh`, `tools.txt`, `env.txt`.

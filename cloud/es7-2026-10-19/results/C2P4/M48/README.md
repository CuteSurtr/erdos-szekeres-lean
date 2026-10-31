# C2P4 M48 (LIST = C2P4.tsv, j = 48, N = 50, H = 2.5, Z = a46b478d)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 13:01:25 UTC, END 15:16:25 UTC (epoch 1793459785).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources: manifest all 196 files match; CaDiCaL 3.0.1, cake_lpr, lrat-check (E2 patch) built and linked into `/opt/work/bin/`.
- Sanity: bad LRAT rejected by both checkers, good LRAT accepted by both (`c VERIFIED`, `s VERIFIED UNSAT`); cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 base.cnf `b0061e90…d8ff1` and base.json `2476faff…2b48`, both as expected.
- Cubes: `l2cubes.py` for P1..P8 byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14 rows of C2P4.tsv with idx ≡ 48 mod 50; one lane, `run.sh`)

| unit | case | kind | cap | status | solve s | lrat-check s | cake_lpr s | proof bytes |
|---|---|---|---|---|---|---|---|---|
| P5_8-14 | P5 | Q | 6000 | certified | 3037.0 | 116.5 | 573.3 | 6725788044 |
| P5_1-8-14 | P5 | H | 1800 | certified | 532.8 | 60.0 | 342.2 | 3662366315 |
| P5_2-8-9 | P5 | H | 1800 | certified | 245.8 | 49.9 | 307.0 | 3205199219 |
| P5_6-8-13 | P5 | H | 1800 | certified | 113.3 | 29.7 | 201.2 | 1263346350 |
| P5_7-9-14 | P5 | H | 1800 | certified | 280.7 | 62.7 | 341.6 | 3083902602 |
| P4_1-5 | P4 | Q | 6000 (lane-capped to 965) | UNKNOWN (timed out at END cap, 953.6 s) | | | | |

Not reached (8): P4_9-10 (Q), P4_7-8-13 (H), P3_5-6 (Q), P3_1-5-7, P3_1-10-11, P3_4-7-10, P3_5-6-13, P3_6-8-11 (H).

Counts by case and kind:
- P5: Q 1 certified; H 4 certified.
- P4: Q 1 UNKNOWN (cap shortened by END, not a real 6000 s timeout), 1 not reached; H 1 not reached.
- P3: Q 1 not reached; H 5 not reached.
- Total: 5 certified, 1 UNKNOWN, 8 not reached, 0 errors.

Certified (5): solve min/median/max 113.3 / 280.7 / 3037.0 s; lrat-check 29.7 / 60.0 / 116.5 s; cake_lpr 201.2 / 341.6 / 573.3 s; proof size 1.26 / 3.21 / 6.73 GB.

Largest solver RSS: 4414 MB (P4_1-5); certified units at most 4393 MB.

No SAT, no proof rejection, no `certified: false` or ERROR record, no memory problem. With these, P5_8-14 and the four P5 hexagonal subcases are closed; P4_1-5 got only 965 s and remains open.

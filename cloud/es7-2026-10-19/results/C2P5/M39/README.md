# C2P5 M39

Machine M39 of the fifth wave on the parallelogram cases: LIST = `C2P5C.tsv`, shard j = 2 of N = 13, H = 4.5 h, task commit Z = 81cb025f.
Start 2026-10-31 20:06:50Z (epoch 1793477210), END = 1793492510. The lane started at 20:09:06Z and finished both units at 20:29:18Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored `tools-src.tar.xz`, and all 196 manifest files matched. That gave CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch). Nothing was cloned or downloaded.
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…d8ff1) and base.json (2476faff…2b48) match the expected values.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, idx ≡ 2 mod 13)

| unit | case | kind | cap s | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P3_4-5 | P3 | Q | 8000 | UNSAT, certified | 529.41 | 48.3 | 318.5 | 3,398,591,451 | 4410 |
| P3_4-8-11 | P3 | H | 2400 | UNSAT, certified | 103.6 | 21.4 | 167.4 | 1,121,260,228 | 3171 |

Counts:
- Certified: 2, both in case P3 (1 Q, 1 H).
- Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.

Statistics over the 2 certified units:
- Solve seconds: min 103.6, median 316.5, max 529.4.
- lrat-check seconds: min 21.4, median 34.85, max 48.3.
- cake_lpr seconds: min 167.4, median 242.95, max 318.5.
- Proof size: min 1.12 GB, median 2.26 GB, max 3.40 GB.

Largest solver RSS: 4410 MB.

No SAT result, no proof rejection and no memory problem. Both proofs were deleted after both checkers accepted them.

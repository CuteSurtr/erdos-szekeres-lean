# primefold-E: PRIMEFOLD Theorem E re-certified with cake_lpr (5 Nov 2026)

**Result: 7 of 7 CNFs regenerated with the recorded SHA-256 (full 64-hex match), 7 of 7 UNSAT (CaDiCaL 2.1.3),
7 of 7 `s VERIFIED UNSAT` from cake_lpr.** Theorem E's certificates no longer depend on lrat-check.

Claim (PRIMEFOLD/README.md §4, Theorem E): the SAT relaxation of Proposition C (i) is UNSAT for
(m, n) = (4,3), (5,4), (6,6), (7,10), (8,15). The CNFs come from `cluster/clsat.py` (five) and the DP form
`cluster/clsat2.py m n 0` (two), exactly as in `cluster/sat/run_all.sh`. The recorded hashes are the full SHA-256 in
`cluster/sat/SHA256SUMS.txt` (the 16-hex prefixes in `cluster/sat/rerun.log` agree).

| instance | generator | vars / clauses | CNF SHA-256 = recorded | CaDiCaL 2.1.3 | LRAT bytes | cake_lpr |
|---|---|---|---|---|---|---|
| m4_n3 | clsat.py 4 3 | 16 / 43 | yes (`245f03f5…`) | UNSAT | 241 | VERIFIED |
| m5_n4 | clsat.py 5 4 | 40 / 172 | yes (`a535be1a…`) | UNSAT | 518 | VERIFIED |
| m6_n6 | clsat.py 6 6 | 115 / 1,031 | yes (`e5bdc398…`) | UNSAT | 2,266 | VERIFIED |
| m7_n10 | clsat.py 7 10 | 408 / 13,945 | yes (`1a73cebb…`) | UNSAT | 12,776 | VERIFIED |
| m8_n15 | clsat.py 8 15 | 1,176 / 295,749 | yes (`03329897…`) | UNSAT | 23,320,261 | VERIFIED |
| dp_m7_n10 | clsat2.py 7 10 0 | 822 / 6,253 | yes (`bfd0d81f…`) | UNSAT | 24,435 | VERIFIED |
| dp_m8_n15 | clsat2.py 8 15 0 | 2,338 / 24,248 | yes (`4a4e2ad4…`) | UNSAT | 3,647,213 | VERIFIED |

VERIFIED means `grep -x 's VERIFIED UNSAT' X.cake.log` matched (cake_lpr exits 0 even when it rejects a proof).
lrat-check was not used. The proofs differ from the recorded ones (`SHA256SUMS.txt` lists CaDiCaL 3.0.1 proofs,
e.g. 25,378,109 bytes for m8_n15). That's expected, because a different solver version was used. The CNFs are
byte-identical.

## Independent encoder (`enc_te/`)

`cluster/check/enc_te.py` instances from `cluster/check/sat_results.log`:
- **UNSAT, with (s1) and without (s0) the signotope axiom, at n = 3, 4, 6, 10, 15 for m = 4..8:** all 10 CNFs match
  their recorded 16-hex hash prefix, all are UNSAT, and cake_lpr gives `s VERIFIED UNSAT` for all 10.
  te_m4_n3_s0 and te_m4_n3_s1 are byte-identical: n = 3 has no 4-subsets, and the record shows the same hash for both.
- **SAT controls at n−1 (s1):** all 5 are SAT, and every model satisfies every clause (`verify_model.py`). No CNF hash
  is recorded for these 5.

See `enc_te/README.md` and `enc_te/results.tsv`.

## Controls (`control/`)

- `bogus`: the satisfiable `p cnf 1 1 / 1 0` with the proof `2 0 0`. cake_lpr prints only
  "c Checking failed ... pivot must be non-zero" on stderr, exits 0, and prints no verdict line, so the verdict is
  not VERIFIED.
- `trunc_m7_n10`: the m7_n10 proof from this run with its last (empty-clause) line removed. cake_lpr says "c empty
  clause not derived at end of proof" and prints no verdict line.
- `flipped_te_m8_n14_s1`: the SAT model with every literal negated. `verify_model.py` reports MODEL_FAIL.

## Files

- Per instance X: `X.cnf`, `X.gen.out` (generator stdout), `X.lrat`, `X.solver.out`/`.err`, `X.cake.log`/`.err`, and
  `X.hashes.txt` (sha256sum of all of them). SAT instances also have `X.model.log`.
- `results.tsv` (instance, cnf_hash_match, solver, verdict), `details.tsv` (adds the recorded and actual hash, proof size
  and times), `run.log`, and `tools.txt` (tool paths and SHA-256, generator source hashes, repo commit).
- Scripts: `run_inst.sh` (one instance), `run_E.sh` (this item), `run_te.sh` (enc_te), and `verify_model.py`.
- Run on 5 Nov 2026 between 13:19 and 13:21 KST, sequentially on one core. Nothing in the repository was modified.

## What this does not cover

Theorem E also rests on Lemma 1, Proposition C (i) and the soundness of the encoding. These are written arguments
that have not been refereed, and this check does not touch them. It certifies only that the regenerated CNFs are
unsatisfiable.

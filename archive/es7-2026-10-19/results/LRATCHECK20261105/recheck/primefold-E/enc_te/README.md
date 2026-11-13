# primefold-E / enc_te: the independent Theorem E encoder re-checked with cake_lpr (5 Nov 2026)

Generator: `PRIMEFOLD/cluster/check/enc_te.py m n sig out.cnf`. The instance list comes from
`PRIMEFOLD/cluster/check/sat_results.log`, which records 16-hex CNF hash prefixes for the UNSAT rows only.

**Result: 15 instances. All 10 UNSAT CNFs match their recorded prefix, are UNSAT, and get `s VERIFIED UNSAT` from
cake_lpr. All 5 SAT controls at n−1 are SAT, and their models satisfy every clause (no recorded hash to compare).**

| m | n | UNSAT s1 (signotope) | UNSAT s0 (no signotope) | SAT control n−1, s1 |
|---|---|---|---|---|
| 4 | 3 | hash yes, VERIFIED | hash yes, VERIFIED | n=2: SAT, model OK |
| 5 | 4 | hash yes, VERIFIED | hash yes, VERIFIED | n=3: SAT, model OK |
| 6 | 6 | hash yes, VERIFIED | hash yes, VERIFIED | n=5: SAT, model OK |
| 7 | 10 | hash yes, VERIFIED | hash yes, VERIFIED | n=9: SAT, model OK |
| 8 | 15 | hash yes, VERIFIED | hash yes, VERIFIED | n=14: SAT, model OK |

- Solver: `cadical --lrat --binary=false -q` (CaDiCaL 2.1.3). Checker: `cake_lpr --CML_HEAP_SIZE=12000`. VERIFIED
  only if `grep -x 's VERIFIED UNSAT'` matches the log.
- Models were checked by `../verify_model.py`. It requires every variable to be assigned exactly once and every clause
  to contain a true literal.
- te_m4_n3_s0 is byte-identical to te_m4_n3_s1, because n = 3 has no 4-subsets. The record shows the same prefix
  `b2ed0fa2…` for both.
- Not run: the `ng_*` rows of `sat_results.log` (10 SAT rows). They are not produced by `enc_te.py`, and no script in
  `cluster/check/` produces them.
- Hash matching for the UNSAT rows is by 64-bit prefix only, because that is all the record keeps.

Files: per instance `X.cnf`, `X.gen.out`, `X.lrat`, `X.solver.out`/`.err`, `X.cake.log`/`.err` (UNSAT) or `X.model.log`
(SAT), and `X.hashes.txt`. Also `results.tsv`, `details.tsv` and `run.log`.

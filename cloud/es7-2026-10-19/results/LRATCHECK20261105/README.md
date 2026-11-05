# LRATCHECK20261105: the lrat-check build used in this project is unsound (5 November 2026)

**Finding (exact, reproducible with `reproduce.sh`).** `lrat-check` from drat-trim (github marijnheule/drat-trim,
commit `2e3b2dc`, 2024-11-25, the build in `~/.local/bin` on the Linux machine) accepts a proof of a *satisfiable*
formula:

```
$ cat sat_formula.cnf      p cnf 1 1 / 1 0
$ cat bogus_proof.lrat     2 0 0
$ lrat-check sat_formula.cnf bogus_proof.lrat
c VERIFIED                 (exit code 0)
```

The step "2 0 0" claims the empty clause with no hints. In `lrat-check.c`, the `RATs == 0` branch
(`lrat-check_c_lines155-165.txt`) has its rejection line commented out:
`// if (res == SUCCESS) return FAILED; // No RAT and no conflict is FAILED`. A lemma whose hints reach no conflict
and which has no RAT candidates is therefore accepted. The defect was found by an independent reviewer of the
5 November supervisor and confirmed by the coordinator.

**cake_lpr (the verified CakeML checker) behaves correctly.** It rejects the bogus proof ("Checking failed at line:
0. Reason: pivot must be non-zero") and prints `s VERIFIED UNSAT` for a genuine CaDiCaL proof. **It exits 0 in both
cases**, so only the printed line can serve as a verdict.

**A second pitfall.** On failure lrat-check prints `c NOT VERIFIED`, and `grep -E 'VERIFIED|FAILED'` matches that
line. A script in the 5 November campaign (`ROT45CHORD20261105/tools/implane.sh`) fell into this. It also deleted
the files it had "verified".

## Consequences

- A statement whose LRAT proofs were accepted **only** by lrat-check is **not certified**. It is not shown false:
  proofs produced by CaDiCaL are very likely valid. Re-check them with cake_lpr, or with a fixed checker.
- Statements whose proofs cake_lpr also accepted are **unaffected**. This includes the `C6UPPER` and `C7UPPER`
  certificates, both checkers for both encoders, and therefore the sixfold value 60 of `SIX60`.
- From now on, the verdict is cake_lpr's `s VERIFIED UNSAT` line. The 5 November supervisor v2 does this
  (`ROT45CHORD20261105/tools/check_wrapper.sh`).
- The project-wide audit of which earlier claims rest on lrat-check alone is in `AUDIT.md` (added when complete).

## In the 5 November campaign

| Claim | Before | Now |
|---|---|---|
| 60 transitivity patterns of the 5-/4-fold covers | lrat-check plus the grep pitfall; artifacts deleted | regenerated and re-checked with cake_lpr (`ROT45CHORD20261105/logs/imp2_results.tsv`) |
| Record sets do not extend by one layer (`SIX10LINUX20261105` §5) | lrat-check only | all 94 proofs regenerated (identical hashes) and accepted by cake_lpr |
| Threshold cubes (`ROT45CHORD20261105`) | none finished before the switch | cake_lpr verdict since 13:01 KST |

Reporting the defect upstream is left to the author.

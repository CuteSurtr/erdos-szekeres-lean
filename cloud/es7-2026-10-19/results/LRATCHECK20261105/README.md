# LRATCHECK20261105: the lrat-check on the Linux machine is the unpatched, unsound build (5 November 2026)

**This defect was already known.** `E2` found it on 20 October 2026 and patched it:
- the record is `E2/logs/lrat_check_soundness.md`;
- the patch is `E2/tools/lrat-check-E2.patch`;
- `WRITEUP/CERTIFICATES.md` pins the patched binary.

The headline results of the project are anchored on cake_lpr (see `AUDIT.md`). This record documents a
**rediscovery**, made on 5 November by an independent reviewer of the threshold-run supervisor and confirmed by the
coordinator, who at first did not know of E2. It also records what is new:

1. **The Linux machine builds the unpatched checker.** The only drat-trim on the host (commit `2e3b2dc`, built
   4 November 21:42, `~/.local/bin/lrat-check`) lacks the E2 patch. The "Setting up on Linux" section of
   `STATUS20261104` does not mention the patch. Every lrat-check verdict on this machine before 13:01 KST on
   5 November used that build.
2. **Reproduction** (`reproduce.sh`, `reproduce.log`): for the satisfiable `p cnf 1 1 / 1 0` and the proof `2 0 0`,
   it prints `c VERIFIED` and exits 0. cake_lpr rejects the same proof ("pivot must be non-zero") but **also exits
   0**, so only its line `s VERIFIED UNSAT` counts.
3. **Scope** (from reading the source, `lrat-check_c_lines155-165.txt`; the audit's reading, not tested further). The
   unsound path is the empty clause: its pivot has intro[] = 0, so an empty clause with non-conflicting hints is
   accepted. A non-empty lemma accepted without RAT candidates is a blocked clause, which preserves satisfiability.
   E2's patch closes the empty-clause path.
4. **Two parsers matched "VERIFIED" inside `c NOT VERIFIED`.** They are `Mi-2/scripts/shard.py:65` and
   `ROT45CHORD20261105/tools/implane.sh`. No cake_lpr driver in the project has this problem.

## Consequences

- A statement whose LRAT proofs were accepted **only** by lrat-check is **not certified**. It is not shown false:
  proofs produced by CaDiCaL are very likely valid. Re-check them with cake_lpr, or with a fixed checker.
- Statements whose proofs cake_lpr also accepted are **unaffected**. This includes the `C6UPPER` and `C7UPPER`
  certificates, both checkers for both encoders, and therefore the sixfold value 60 of `SIX60`.
- From now on, the verdict is cake_lpr's `s VERIFIED UNSAT` line. The 5 November supervisor v2 does this
  (`ROT45CHORD20261105/tools/check_wrapper.sh`).
- **Project-wide audit (`AUDIT.md`).** Every headline result is anchored on cake_lpr: threefold 33, the mirror cases,
  central 34, fivefold 35, fourfold 28, threefold hexagon-free 13, sixfold 60, sevenfold 64 and mirror 46.
  - **One exception: PRIMEFOLD Theorem E** (cited in the note's abstract) was accepted by lrat-check only. Its
    re-check with cake_lpr was started on 5 November, together with the other small lrat-check-only items listed
    in `AUDIT.md` §4.
  - Recommendation: always install drat-trim with the E2 patch, log the checker binary's SHA-256 in every run, and
    anchor every certificate on cake_lpr.

## In the 5 November campaign

| Claim | Before | Now |
|---|---|---|
| 60 transitivity patterns of the 5-/4-fold covers | lrat-check plus the grep pitfall; artifacts deleted | regenerated and re-checked with cake_lpr (`ROT45CHORD20261105/logs/imp2_results.tsv`) |
| Record sets do not extend by one layer (`SIX10LINUX20261105` §5) | lrat-check only | all 94 proofs regenerated (identical hashes) and accepted by cake_lpr |
| Threshold cubes (`ROT45CHORD20261105`) | none finished before the switch | cake_lpr verdict since 13:01 KST |

Reporting the defect upstream is left to the author.

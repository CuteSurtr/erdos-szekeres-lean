# lean_es7_corr: fivefold and fourfold ES(7) corollaries of the layer lemma

4 November 2026 (KST). The file is `ES7Corollaries.lean` (1233 lines, SHA-256 `5883c8eb…`).
- **Lines 1–1147** are an exact copy of `LAYERLEAN/LayerLemma.lean`. The coordinator confirmed this with `diff`.
- **Section 11** adds the definitions `Fivefold35` and `Fourfold32`, copied verbatim from `SYMLEAN/SymmetricReduction.lean`,
  followed by the corollaries.
- **Checks.** The coordinator re-checked the build (exit 0, no messages), the `sorry`/`admit`/`axiom` scan (none) and
  the axioms independently.

## Lean-checked

All five theorems depend only on [propext, Classical.choice, Quot.sound].

| Theorem | Hypotheses | Conclusion |
|---|---|---|
| `fivefold_heptagon_of_erase` | `Fivefold35`, more than 30 points other than the centre | convex 7-gon |
| `fivefold_heptagon` | `Fivefold35`, at least 32 points | convex 7-gon |
| `fivefold_heptagon_of_centre_not_mem` | `Fivefold35`, centre not in S, at least 31 points | convex 7-gon |
| `fourfold_heptagon_of_erase` | `Fourfold32`, more than 28 points other than the centre | convex 7-gon |
| `fourfold_heptagon` | `Fourfold32`, at least 29 points (centre excluded by even order) | convex 7-gon |

**Mutants.** Lowering the thresholds (32 → 31 in the fivefold case, 29 → 28 in the fourfold case) makes the proof fail
at `omega`.

## Consequences

The first two consequences rely on the case classes, which are certified in `SYM5` (`Fivefold35`) and `C4CUT`
(`Fourfold32`):
- **Fivefold.** The 7-gon-free maximum is 31: the upper bound from these theorems, the lower bound from
  `SYMMAX/c5_31points.txt`.
- **Fourfold.** The maximum is 28: the upper bound from these theorems, the lower bound from `SYMMAX/c4_28points.txt`.
- **Not re-verified here.** The two examples were not re-checked in this run.

## Open issues

- **Hypotheses.** `Fivefold35` and `Fourfold32` remain hypotheses, resting on the SAT certificates.
- **SYMLEAN link.** SYMLEAN's `case_odd_prime` and `case_fourfold` use `crot`. Linking them needs the `rotAbout_eq_crot`
  bridge, which is not done.

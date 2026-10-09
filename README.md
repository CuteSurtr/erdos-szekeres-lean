# Erdős–Szekeres in Lean

Lean proofs of two published upper bounds for **finite point sets in the real
plane in general position** (no three distinct points collinear), together with
separately identified computational research. Polygons need not be empty.

**The Erdős–Szekeres conjecture is not proved or disproved here. ES(8) ≤ 317 and
an improvement of HMPT's asymptotic coefficient remain unproved.** A restricted
geometric bound of 192 points is checked below; no priority or best-bound claim
is made.

## Finished formalizations

All logarithms below are to base 2. The floor is the natural-number floor.

| Published result | Proved statement | Main Lean theorem | Source |
| --- | --- | --- | --- |
| Suk 2016, Theorem 1.1 | For all sufficiently large `n`, at least `⌊2^(n + 6 n^(2/3) log₂ n)⌋` points force a convex `n`-gon. | `ErdosSzekeres.Suk.theorem2016 : ErdosSzekeres.Suk.Theorem2016` | [Suk/Asymptotic.lean](ErdosSzekeres/Suk/Asymptotic.lean); [statement and threshold](ErdosSzekeres/Suk/Statement.lean) |
| HMPT 2020, Theorem 1.3 / Remark 1.4, **ordinary real-point specialization** | For every `ε > 0` and all sufficiently large `n`, at least `⌊2^(n + (8√2/3 + ε)√(n log₂ n))⌋` points force a convex `n`-gon. | `ErdosSzekeres.HMPT.theorem2020 : ErdosSzekeres.HMPT.Theorem2020` | [HMPT/Asymptotic.lean](ErdosSzekeres/HMPT/Asymptotic.lean); [statement and threshold](ErdosSzekeres/HMPT/Statement.lean) |

Both final theorems have complete proofs with no unproved geometric assumptions.
Their quantifiers are eventual: they do not assert these formulas for every
small `n`. [Definitions.lean](ErdosSzekeres/Definitions.lean) uses `Point := Fin 2 → ℝ`
and `ForcesConvexNGon N n`, which quantifies over every general-position finite
set with **at least** `N` points and supplies a convex subset of exactly `n` points.
Convex position is Mathlib's `ConvexIndependent`.

These are completed upper-bound formalizations, not verbatim formalizations of
every statement in either paper. Suk's proof uses a checked extraction variant
with different intermediate constants. HMPT's pseudo-configuration and convex-body
extensions are outside the implemented scope. The [paper-to-Lean tables](docs/PAPER_MAP.md)
list every numbered result and distinguish exact results, replacement arguments,
restricted specializations, and statements not formalized.

- [Suk proof ledger](docs/SUK.md): geometric cases, extraction, integer estimates and limits.
- [HMPT proof ledger](docs/HMPT.md): cap budgets, counting ratios, two scales and optimization.
- [Third-party provenance and licenses](docs/THIRD_PARTY.md): adapted prerequisites and research data.

## Completed balanced geometric subcase — 9 October 2026

For actual real points in general position, ordered by **strictly increasing
x-coordinates**, absence of a 7-cup, a 7-cap and a convex octagon implies **at
most 192 points**. Cups and caps require the appropriate sign on every increasing
triple of the selected points. The exact theorem is
`OmissionBalanced.real_configuration_bound`, in the separately checked
[BalancedGeometry.lean](experiments/omission-balanced-geometry-2026-10-09/BalancedGeometry.lean).
Its hypotheses are geometric; no catalog-row constraints are assumed.

The proof includes the actual-point state assignment, all **2,685 geometric row
checks**, and the complete balanced arithmetic certificate. It tightens the
source archive's balanced-case bound of 193 by one point. The state/cycle method
and adapted prerequisites are credited to Michael Schroeder's version-1 archive;
the stronger arithmetic certificate and local geometric connections are described
in the [proof map](docs/OMISSION_GEOMETRY.md) and
[reproducible artifact](experiments/omission-balanced-geometry-2026-10-09/README.md).
This subcase's extra cup/cap restrictions cannot be dropped. The residual bound
and partition argument needed for the global octagon bound are unfinished.

## Completed projective reduction — 9 October 2026

Every nonempty octagon-free real set in general position has a root-deletion
chart with exactly one fewer point, no 7-cap and no convex octagon. The theorem
`ErdosSzekeres.Omission.exists_cap_free_chart` retains the actual coordinate
maps; it imposes no coordinate-order assumption on the original set. The key
geometric lemma proves that a chart 7-cap and its deleted root form an octagon.
These results live in [ProjectiveTransfer.lean](ErdosSzekeres/Omission/ProjectiveTransfer.lean).

The resulting `forces_317_of_asymmetric_315` proves the conditional implication
`AsymmetricBound 315 → ForcesConvexNGon 317 8`. **`AsymmetricBound 315` is still
unproved**: it permits 7-cups, unlike the completed balanced subcase.

Combining the two completed steps also proves that every octagon-free set of
at least **194 points** has such a chart containing a **7-cup**. This structural
consequence is checked separately as
`OmissionBalanced.large_avoiding_set_has_chart_cup`; it does not assert
ES(8) ≤ 194. See the [projective proof map](docs/OMISSION_PROJECTIVE.md) and
[check record](experiments/omission-projective-transfer-2026-10-09/README.md).

## Verification

Pinned versions: **Lean 4.24.0**, **Mathlib v4.24.0**; dependency revisions are in
[lake-manifest.json](lake-manifest.json).

The current library passes `lake build --wfail`. The
[full saved axiom audit](docs/validation/axiom-audit-projective-2026-10-09.txt) checks **277 named
theorems**, including both main theorems and their transitive axiom dependencies.
Only `propext`, `Classical.choice`, and `Quot.sound` are allowed. There is no
`sorry`, `admit`, `sorryAx`, or `native_decide` in the maintained Lean sources,
including the finished results and vendored Lean prerequisites. The
[validation record](docs/VALIDATION.md) gives the scope, commands and source hashes.

```sh
lake exe cache get
lake build --wfail
python3 scripts/check_axioms.py
python3 -m unittest discover -s scripts -v
```

The default Python suite needs only the standard library; solver-specific tests
skip when their optional dependencies are unavailable. This Mac checkout has a
workspace-local toolchain, so use `ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place
of `lake`. `.cache/`, `.lake/`, `.elan/` and compiled outputs are ignored and are
not committed. Standalone research certificates have separate reproduction
instructions and are not silently counted as default-library CI checks.

## In-progress research — resumed 9 October 2026

This material is separate from the finished Suk and HMPT formalizations.

- **Residual omission system:** a complete exact integer certificate gives the
  auxiliary occupancy target 123, with independent arithmetic replays. Lean has
  checked the first **330 of 3,411 parts**, covering **13,827 of 145,474 leaves**.
  The residual root and its geometric row requirements remain unfinished.
- **Global finite octagon target:** the balanced geometric theorem and the
  projective/root transfer are complete. The residual bound and minimum-slope
  partition must still establish the remaining `AsymmetricBound 315` hypothesis.
  Consequently **ES(8) ≤ 317 is not a theorem of this repository**.
- **Other retained experiments:** exact-coordinate searches, SAT/SMT attempts and
  a Lean-checked counterexample to a proposed mixed-cap lemma. None improves the
  published global geometric upper bounds; timeout results remain inconclusive.

See [the ES(8) remaining-work estimate](docs/ES8_REMAINING.md),
[omission certificate record](docs/OMISSION.md), [mixed-cap result](docs/MIXED_CAPS.md),
[SAT record](docs/SAT.md), and [historical research log](docs/RESEARCH.md).
The open conjecture and `HMPT.StrictImprovement` are proposition definitions,
not assumed axioms or unfinished proof declarations. Research certificates
remain separate from the completed geometric formalizations.

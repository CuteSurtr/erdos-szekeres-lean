# Erdős–Szekeres in Lean

Lean proofs of two published upper bounds for **finite point sets in the real
plane in general position** (no three distinct points collinear), together with
separately identified computational research. Polygons need not be empty.

**ES(8) ≤ 316 is now proved in Lean:** every set of at least 316 real planar
points in general position contains eight points in convex position. The
finished Suk 2016 and HMPT 2020 asymptotic bounds are also formalized below.
The Erdős–Szekeres conjecture and an improvement of HMPT's asymptotic
coefficient remain open in this project. No priority or best-known-bound claim
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

## Completed finite octagon bound — 10 October 2026

The closed theorem is `ErdosSzekeres.Omission.forces_convex_octagon_316 :
ForcesConvexNGon 316 8`. Its explicit real-point form,
`ErdosSzekeres.Omission.convex_octagon_of_card_ge_316`, quantifies over every
finite set `S : Finset (Fin 2 → ℝ)` in general position with `316 ≤ S.card`,
and supplies `T ⊆ S` of cardinality eight with `ConvexIndependent ℝ`.
Both live in [FinalCover316.lean](experiments/omission-global-assembly-2026-10-10/FinalCover316.lean).
There are no remaining row, arithmetic, coordinate-order or cup/cap assumptions
on the original point set.

The proof combines the checked projective/root transfer and minimum-slope
partition with balanced population bound 191 and residual bound 123.
The partition's configurations have additional geometric restrictions, all
proved by the reduction. Their 2,685 balanced and 1,187 residual row constraints
are established for actual points. Checked rounding cuts compress the arithmetic
exclusions to 3,954 and 4,686 leaves. Every leaf, complete tree root, literal
catalog bridge and final composition has passed Lean with only `propext`,
`Classical.choice` and `Quot.sound`.

- [Complete assembly record, theorem audit and reproduction](experiments/omission-global-assembly-2026-10-10/README.md).
- [Arithmetic source archives and exact cut certificates](experiments/omission-cover-certificates-2026-10-10/README.md).
- [Balanced geometry](docs/OMISSION_GEOMETRY.md), [projective transfer](docs/OMISSION_PROJECTIVE.md), [partition](docs/OMISSION_PARTITION.md) and [residual geometry](docs/OMISSION_RESIDUAL.md).

The omission method, original state catalogs and adapted prerequisites are
credited to Michael Schroeder's version-1 archive (19 September 2026), which
claims an octagon threshold of 319. This repository proves the smaller threshold
316 using stronger arithmetic certificates and ordinary kernel checking.
That comparison is to the pinned archive, not a claim of literature priority.
See [provenance and licenses](docs/THIRD_PARTY.md).

## Other completed research results

`Omission.AdditionalResidualRows.all_rows` proves 21 additional geometric rows;
`Omission.GeneralResidualBlocks.all_rows` proves another 24. The former have
separate row-by-row independence witnesses. A [Lean-checked abstract witness](experiments/omission-cover-certificates-2026-10-10/ResidualCountermodel.lean)
satisfies all 1,187 original rows and all 45 additions with 32 holes. Thus these
constraints alone cannot exclude that assignment; no real-point realization
of it is claimed.

Two further coupled constraints are now proved for actual residual configurations:
`Omission.CoupledCore13.hole_bound` in
[CoupledObstruction.lean](ErdosSzekeres/Omission/CoupledObstruction.lean), and
`Omission.CoupledCoreSecond.hole_bound` in
[CoupledSecondObstruction.lean](ErdosSzekeres/Omission/CoupledSecondObstruction.lean).
Each excludes simultaneous occupation of thirteen specified states by using
their common chronological order, actual pair ranks and orientation signs.
The first constraint excludes the preceding 32-hole witness, with that strict
strengthening also proved in Lean. The [first](experiments/omission-coupled-core-2026-10-10/README.md)
and [second](experiments/omission-coupled-next-2026-10-10/README.md) proof bundles
preserve the literal kernel-checked refutations and independent replay controls.
Their compatible families have 42 and 35 checked rows, with 20 shared supports:
57 distinct constraints in total. The [complete Lean classification](experiments/omission-coupled-union-2026-10-10/README.md)
proves that 48 follow from original rows and nine are independent additions
relative to this frozen system.

`Omission.CoupledCoreThird.hole_bound` and
`Omission.CoupledCoreFourth.hole_bound` and
`Omission.CoupledCoreFifth.hole_bound` add three more checked obstructions.
The third and fourth templates supply three and 24 checked variants,
respectively, through `CoupledThirdVariants.all_rows` and
`CoupledFourthVariants.all_rows`. `CoupledFifthVariants.all_rows` adds 28
further checked maps. Smaller eleven- and nine-state obstructions are proved
by `CoupledCoreEleven.hole_bound` and `CoupledCoreNine.hole_bound`; their
[eleven-state](experiments/omission-coupled-eleven-2026-10-10/README.md) and
[nine-state](experiments/omission-coupled-nine-2026-10-10/README.md) bundles
preserve the geometric proofs and independent certificate controls.
[CoupledDemandTwo.lean](ErdosSzekeres/Omission/CoupledDemandTwo.lean) proves
`Omission.CoupledDemandTwo.hole_bound`: at least two states are missing from
one specified 14-state set. Given the earlier rows, that formulation is
equivalent to the third obstruction; it is not a second independent discovery.
These geometric extensions are separate from the completed 316-point
arithmetic route and do not yet lower its threshold.

[DyadicScale.lean](ErdosSzekeres/HMPT/DyadicScale.lean) extends the finite HMPT
counting argument to any number of doubling stages.
`HMPT.positive_dyadic_leading_budget_iff` proves that its explicit idealized
leading expression becomes positive exactly above `8√2/3`. This is an
algebraic limitation of this proof family, not a universal barrier to better
Erdős–Szekeres bounds. [EndpointBarrier.lean](ErdosSzekeres/HMPT/EndpointBarrier.lean) also proves
that the existing entropy budget is eventually negative at every fixed positive
scale for coefficients at or below `8√2/3`, including equality. That statement
concerns this budget only. See the [research report](docs/RESEARCH_2026-10-10.md).

[BinomialRefinement.lean](ErdosSzekeres/HMPT/BinomialRefinement.lean) strengthens
the finite HMPT counting interface by retaining the exact subset count.
`HMPT.two_scale_binomial_bound` gives a strictly smaller density threshold;
`HMPT.suk_two_scale_factorial_bound` supplies a closed real-point bound with
a factorial saving in its exponent. This standard counting refinement leaves
the asymptotic coefficient unchanged and carries no novelty claim. The
[proof artifact](experiments/hmpt-binomial-refinement-2026-10-10/README.md)
states the formulas, hypotheses and a checked strictness example.

## Verification

Pinned versions: **Lean 4.24.0**, **Mathlib v4.24.0**; dependency revisions are in
[lake-manifest.json](lake-manifest.json).

The current library passes `lake build --wfail`. The
[full saved axiom audit](docs/validation/axiom-audit-recovery-2026-10-10.txt) checks **544 named
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

## In-progress research — 10 October 2026

The 315- and 314-point targets are **not yet proved**. Complete exact arithmetic
certificates with 22,318 balanced and 50,945 residual leaves are undergoing Lean
checking. Further geometric constraints are being investigated using explicit
Boolean witnesses and shared-order/rank/orientation obstructions. Neither solver
UNSAT output nor a partially checked certificate is counted as a theorem.

The [current work estimate](docs/ES8_REMAINING.md) separates these stronger
targets from the completed 316-point result. The earlier complete 317-point
proof and its records remain available. Earlier partial certificates and
failed searches are retained as dated research records. They do not invalidate
or replace the complete new proof route. The finished asymptotic theorem still
has HMPT's published coefficient `8√2/3`.

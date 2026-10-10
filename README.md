# Erdős–Szekeres in Lean

Lean proofs of two published upper bounds for **finite point sets in the real
plane in general position** (no three distinct points collinear), together with
separately identified computational research. Polygons need not be empty.

**ES(8) ≤ 314 is now proved in Lean:** every set of at least 314 real planar
points in general position contains eight points in convex position. The
finished Suk 2016 and HMPT 2020 asymptotic bounds are also formalized below.
The Erdős–Szekeres conjecture and an improvement of HMPT's asymptotic
coefficient remain open in this project. No priority or best-known-bound claim
is made.

Start with the [formal mathematical companion](math.md): precise
definitions, quantified statements, proof arguments and direct Lean declaration
references for the asymptotic bounds, the finite proof of 314 and the gap to 313.

Original project contributions are licensed under [Apache-2.0](LICENSE).
Third-party code and data retain their own licenses; see the
[license scope](docs/LICENSING.md) and [attribution notice](NOTICE).

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

The closed theorem is `ErdosSzekeres.Omission.forces_convex_octagon_314 :
ForcesConvexNGon 314 8`. Its explicit real-point form,
`ErdosSzekeres.Omission.convex_octagon_of_card_ge_314`, quantifies over every
finite set `S : Finset (Fin 2 → ℝ)` in general position with `314 ≤ S.card`,
and supplies `T ⊆ S` of cardinality eight with `ConvexIndependent ℝ`.
Both live in [FinalCover314B61FusedR31Fused.lean](experiments/omission-global-assembly-2026-10-10/FinalCover314B61FusedR31Fused.lean).
There are no remaining row, arithmetic, coordinate-order or cup/cap assumptions
on the original point set.

The proof combines the checked projective/root transfer and minimum-slope
partition with balanced population bound 190 and residual bound 122.
The partition's configurations have additional geometric restrictions, all
proved by the reduction. Their 2,685 balanced and 1,187 residual row constraints
are established for actual points. Checked rounding cuts compress the arithmetic
exclusions to 22,318 and 50,945 leaves. Every leaf, complete tree root, literal
catalog bridge and final composition has passed Lean with only `propext`,
`Classical.choice` and `Quot.sound`.

- [Complete assembly record, theorem audit and reproduction](experiments/omission-global-assembly-2026-10-10/README.md).
- [Arithmetic source archives and exact cut certificates](experiments/omission-cover-certificates-2026-10-10/README.md).
- [Balanced geometry](docs/OMISSION_GEOMETRY.md), [projective transfer](docs/OMISSION_PROJECTIVE.md), [partition](docs/OMISSION_PARTITION.md) and [residual geometry](docs/OMISSION_RESIDUAL.md).

The omission method, original state catalogs and adapted prerequisites are
credited to Michael Schroeder's version-1 archive (19 September 2026), which
claims an octagon threshold of 319. This repository proves the smaller threshold
314 using stronger arithmetic certificates and ordinary kernel checking.
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
[CoupledNineVariant.lean](ErdosSzekeres/Omission/CoupledNineVariant.lean)
checks a second nine-state support using the same generic refutation.
[CoupledDemandTwo.lean](ErdosSzekeres/Omission/CoupledDemandTwo.lean) proves
`Omission.CoupledDemandTwo.hole_bound`: at least two states are missing from
one specified 14-state set. Given the earlier rows, that formulation is
equivalent to the third obstruction; it is not a second independent discovery.
These geometric extensions are separate from the completed 314-point
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

[FactorialSaving.lean](ErdosSzekeres/HMPT/FactorialSaving.lean) makes that
strictness uniform: whenever the old exponent exceeds its auxiliary floor,
`HMPT.integer_two_scale_bound_one_bit_smaller` halves the sufficient
power-of-two threshold using the same auxiliary-polygon input. The
[precise finite condition and audit](experiments/hmpt-factorial-saving-2026-10-10/README.md)
are explicit; this does not change the asymptotic coefficient.

[VisibleEdgeInsertion.lean](ErdosSzekeres/VisibleEdgeInsertion.lean) proves
a reusable convex-polygon insertion lemma: a new point outside one supporting
edge and inside the others preserves all vertices when the retained edges
cover them. [CoupledNineStructural.lean](ErdosSzekeres/Omission/CoupledNineStructural.lean)
uses it to reprove the original nine-state obstruction geometrically, without
invoking its SAT refutation. The same construction proves two more supports
in [CoupledNineStructuralVariants.lean](ErdosSzekeres/Omission/CoupledNineStructuralVariants.lean).
The [structural proof artifact](experiments/omission-coupled-nine-structural-2026-10-10/README.md)
contains the readable argument and all three checked instances.

The enlarged **2,469-row residual catalog now has a complete geometric
transfer** in [Transfer.lean](experiments/omission-residual32-transfer-2026-10-10/Transfer.lean).
`OmissionResidual32Transfer.all_rows` proves every literal constraint for one
actual residual assignment; `feasible_holes` also gives its exact population
complement. Five conditional arithmetic exclusions are checked in the
[context-certificate bundle](experiments/omission-residual32-context-certificates-2026-10-10/README.md),
and [ContextGeometry.lean](experiments/omission-residual32-transfer-2026-10-10/ContextGeometry.lean)
applies them to actual configurations of at least 122 points, including two
merged-parent exclusions. A separate [zero-state theorem](experiments/omission-residual32-context-certificates-2026-10-10/ZeroState.lean)
proves that every nonempty actual residual configuration occupies state zero.
Six further closed subtrees and their actual-configuration corollaries are
checked in the [resumed Lean bundle](experiments/omission-residual32-resume-lean-2026-10-10/README.md),
covering all 44 splits and 50 weighted leaves in those six trees.
These are finished standalone proofs; they do not establish a global bound
below 314.

The latest continuation resolves an important limitation of that search:
a [Lean-checked 32-hole witness](experiments/omission-residual32-case4-2026-10-10/README.md)
satisfies **all 2,469 rows**. `OmissionResidual32Case4.no_universal_thirty_three_hole_bound`
proves that the old catalog cannot supply the needed arithmetic exclusion.
This assignment is not a real-point counterexample.

A new [thirteen-state geometric obstruction](experiments/omission-residual32-witness-coupled-2026-10-10/README.md)
excludes it. In namespace `ErdosSzekeres.Omission.CoupledCoreSixth`,
`hole_bound`, `strict_strengthening`, and `countermodel_not_realizable`
prove the new row, its independence from the old catalog, and nonrealizability
of that witness. Its 376-clause formula and 258-step refutation are checked
by Lean. A [128-row Fourth-template family](experiments/omission-residual32-fourth-global-variants-2026-10-10/README.md)
is also proved for actual configurations by
`ErdosSzekeres.Omission.CoupledFourthGlobalVariants.all_rows`.
The [exact 129-row addition](experiments/omission-residual32-added-rows-2026-10-10/README.md)
is geometrically bound by `ErdosSzekeres.Omission.Residual32AddedRows.all_rows`.
The [generic Sixth template](experiments/omission-residual32-sixth-variants-2026-10-10/README.md)
is proved separately. These strengthen the geometric toolbox; they do not yet
prove the 313-point theorem.

## Verification

Pinned versions: **Lean 4.24.0**, **Mathlib v4.24.0**; dependency revisions are in
[lake-manifest.json](lake-manifest.json).

The current library passes `lake build --wfail`. The
[full saved axiom audit](docs/validation/axiom-audit-structural-2026-10-10.txt) checks **571 named
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
lake env python3 scripts/check_residual32_continuation.py
```

The default Python suite needs only the standard library; solver-specific tests
skip when their optional dependencies are unavailable. This Mac checkout has a
workspace-local toolchain, so use `ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place
of `lake`. `.cache/`, `.lake/`, `.elan/` and compiled outputs are ignored and are
not committed. The last command freshly compiles the new residual32 witness
and geometric refinements and is an explicit hosted CI step. Other standalone
research certificates retain their separate reproduction instructions; they
are not implicitly included in the default library build.

## In-progress research — 10 October 2026

The 313-point target is **not proved**. The bounded balanced 62-hole searches,
including a separate [ten-minute SAT run](experiments/omission-balanced62-sat-2026-10-10/README.md),
were inconclusive. The [resumed residual search](experiments/omission-residual32-resume-2026-10-10/README.md)
previously had eight pending frontier leaves within three original contexts.
Continuing case 4 produced the old catalog's 32-hole witness above; cases 2
and 7 remain partial. Eleven earlier contexts have Lean proofs and ten more
have integer-replayed subtrees, but no complete old-catalog exclusion is
possible. The new search catalog adds 129 geometric rows, for **2,598 rows**
in total. Bounded integer and repair searches are inconclusive: the best
recorded 32-hole near-model still violates one row. No exclusion certificate
or feasible assignment for all 2,598 rows has been established.

The [current work estimate](docs/ES8_REMAINING.md) separates these stronger
targets from the completed 314-point result. The earlier complete 315-, 316-
and 317-point proofs and their records remain available. Earlier partial
certificates and failed searches are retained as dated research records. They do not invalidate
or replace the complete new proof route. The finished asymptotic theorem still
has HMPT's published coefficient `8√2/3`.

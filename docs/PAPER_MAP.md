# Paper-to-Lean correspondence

This is a coverage map, not a claim that every paper statement has been
formalized verbatim. Numbering is pinned to
[Suk, arXiv:1604.08657v2 (27 August 2016)](https://arxiv.org/pdf/1604.08657v2)
and [HMPT, arXiv:1710.11415v3 (3 August 2020)](https://arxiv.org/pdf/1710.11415v3),
the version corresponding to the final 2020 coefficient.

**Exact** means the relevant stated upper-bound conclusion is proved.
**Replacement** means a different checked lemma serves that step; it is not a
proof of the original intermediate statement. **Real only** excludes the
paper's pseudo-configurations. **Not formalized** means there is no corresponding
proved declaration. These distinctions matter even though the two final
real-point upper bounds are complete.

In the tables, prepend `ErdosSzekeres.` to names beginning `Suk.` or `HMPT.`.
Links identify the actual Lean source file. All numbered results in these two
versions, all numbered sections, and the principal unnumbered proof stages are
covered below. Background citations are not additional completed theorems.

## Suk

| Paper location | Lean files and declarations | Coverage / difference |
| --- | --- | --- |
| §1, definitions and conjecture | [Definitions.lean](../ErdosSzekeres/Definitions.lean): `GeneralPosition`, `ConvexPosition`, `ForcesConvexNGon`, `ErdosSzekeresConjecture` | Definitions for real finite sets; the conjecture is not asserted. |
| §1, Theorem 1.1 | [Suk/Asymptotic.lean](../ErdosSzekeres/Suk/Asymptotic.lean): `Suk.theorem2016`; [Statement.lean](../ErdosSzekeres/Suk/Statement.lean): `Suk.Theorem2016` | **Exact upper bound**, including coefficient 6 and the proof's floor convention. |
| §2, Lemma 2.1 | [FourPoint.lean](../ErdosSzekeres/Suk/FourPoint.lean): `Suk.convexPosition_of_four_subsets`, `Suk.convexPosition_of_subsets_card_le_four` | Four-point criterion, from Mathlib's Carathéodory theorem. |
| §2, Theorem 2.2 | [CupsCaps.lean](../ErdosSzekeres/Suk/CupsCaps.lean): `Suk.cups_caps`, `Suk.classical_upper_bound` | Upper-bound direction for target sizes at least three. The matching extremal lower bound is **not formalized**. |
| §2, Theorem 2.3 | [TransitiveColoring.lean](../ErdosSzekeres/Suk/TransitiveColoring.lean): `Suk.transitive_cups_caps`, `Suk.transitive_path_clique` | Transitive-coloring upper bound. Equality/lower-bound construction is **not formalized**. |
| §2, Theorem 2.4 | [DenseCapExtraction.lean](../ErdosSzekeres/Suk/DenseCapExtraction.lean): `Suk.rich_support_of_dense_caps`; [SupportCoarsening.lean](../ErdosSzekeres/Suk/SupportCoarsening.lean): `Suk.ClockwiseAnchors.extract_rich_spikes`; [IntegerParameters.lean](../ErdosSzekeres/Suk/IntegerParameters.lean): `Suk.cubic_log_bound` | **Replacement** extraction argument. The literal `32k` constant is **not formalized**; the checked exponent loss is `64(k+5)`, absorbed in the final estimate. |
| §2, support-region setup | [SpikeGeometry.lean](../ErdosSzekeres/Suk/SpikeGeometry.lean), [SupportSequence.lean](../ErdosSzekeres/Suk/SupportSequence.lean): `Suk.ClockwiseAnchors.adjacent_frames` | Open halfplane support frames in a horizontal clockwise sequence, with explicit endpoints. |
| §3, initial extraction and symmetry | [ExtractionCounting.lean](../ErdosSzekeres/Suk/ExtractionCounting.lean): `Suk.convex_subsets_count_classical`; [FiniteDensityBound.lean](../ErdosSzekeres/Suk/FiniteDensityBound.lean): `Suk.horizontal_finite_density_bound`; [CoordinateNormalization.lean](../ErdosSzekeres/Suk/CoordinateNormalization.lean): `Suk.exists_horizontal_image` | **Replacement** counting/extraction proof; reflection and rotation discharge coordinate restrictions. |
| §3, partial order and Dilworth step | [TriangleOrder.lean](../ErdosSzekeres/Suk/TriangleOrder.lean): `Suk.triangleOrder_iff`; [BaseOrder.lean](../ErdosSzekeres/Suk/BaseOrder.lean): `Suk.AboveBase.le_iff`; [ChainAntichain.lean](../ErdosSzekeres/Suk/ChainAntichain.lean): `Suk.chain_or_antichain` | Actual geometric order and finite chain/antichain dichotomy. Integer size parameters replace fractional powers in the paper's dichotomy. |
| §3, Case 1: separation and extraction | [SpikeSeparation.lean](../ErdosSzekeres/Suk/SpikeSeparation.lean): `Suk.ClockwiseAnchors.incomparable_pair_nonadjacent_same_side`; [AntichainExtraction.lean](../ErdosSzekeres/Suk/AntichainExtraction.lean): `Suk.CapFrame.antichain_cup_cap` | Geometric separation and supported-cap extraction. |
| §3, Case 1: union and conclusion | [AntichainCaps.lean](../ErdosSzekeres/Suk/AntichainCaps.lean): `Suk.ClockwiseAnchors.convexPosition_union_antichain_caps_of_supports`; [AntichainCase.lean](../ErdosSzekeres/Suk/AntichainCase.lean): `Suk.ClockwiseAnchors.antichain_case` | Nonadjacent supported caps glue; cardinalities are additive. |
| §3, Case 2: chain coloring | [ChainColoring.lean](../ErdosSzekeres/Suk/ChainColoring.lean): `Suk.chain_orientation_clique`; [ChainCaps.lean](../ErdosSzekeres/Suk/ChainCaps.lean) | Transitivity is proved geometrically before applying the abstract bound. |
| §3, Observation 3.1 | [AdjacentCaps.lean](../ErdosSzekeres/Suk/AdjacentCaps.lean): `Suk.AdjacentCapFrames.glue_caps`; [ChainCase.lean](../ErdosSzekeres/Suk/ChainCase.lean): `Suk.glue_neighboring_chain_caps` | Facing-cap gluing for total size at least four and the explicit general-position hypotheses. Small terminal cases are handled separately. |
| §3, Observation 3.1 proof, four-point replacement | [Quadrilateral.lean](../ErdosSzekeres/Suk/Quadrilateral.lean): `Suk.convexPosition_four_same_cell`, `Suk.convexPosition_four_iff_pair_separation` | Determinant-based replacement and separation lemmas. |
| §3, Case 2: iteration, equations (1)–(2) | [CapGrowth.lean](../ErdosSzekeres/Suk/CapGrowth.lean): `Suk.iterated_cap_growth`; [SupportSequence.lean](../ErdosSzekeres/Suk/SupportSequence.lean): `Suk.ClockwiseAnchors.chain_case_finsets`; [IntegerParameters.lean](../ErdosSzekeres/Suk/IntegerParameters.lean): `Suk.spike_budget_le_power` | **Replacement** explicit integer estimates and capped growth, rather than the paper's identical intermediate inequalities. |
| §3, assembly and eventual cutoff | [FiniteSupport.lean](../ErdosSzekeres/Suk/FiniteSupport.lean): `Suk.ClockwiseAnchors.finite_support_bound`; [FiniteBound.lean](../ErdosSzekeres/Suk/FiniteBound.lean): `Suk.finite_density_bound`; [Asymptotic.lean](../ErdosSzekeres/Suk/Asymptotic.lean): `Suk.integer_parameters_fit_exponent`, `Suk.coefficient_six_bound`, `Suk.theorem2016` | Complete real-point theorem. The cutoff exists; a sharp numerical cutoff is not claimed. |
| §4, concluding remark | [HMPT/Asymptotic.lean](../ErdosSzekeres/HMPT/Asymptotic.lean): `HMPT.theorem2020` | The later real-point bound is proved separately. This does not formalize the historical attribution as a proposition. |
| Acknowledgments and bibliography | [THIRD_PARTY.md](THIRD_PARTY.md) | Attribution, not proof obligations. |

The detailed implementation dependencies are in [SUK.md](SUK.md). The final
result does not depend on the omission-search data or its experimental checks.

## HMPT

The paper has three numbered sections and uses numbered **Observations** and
**Proposition 3.8**, rather than standalone numbered lemmas. Its ambient setting
is broader than this repository's `Point := Fin 2 → ℝ`. Entries marked real-only
must not be read as proofs of the full paper statements.

| Paper location | Lean files and declarations | Coverage / difference |
| --- | --- | --- |
| §1, ordinary point-set setup | [Definitions.lean](../ErdosSzekeres/Definitions.lean), [HMPT/Statement.lean](../ErdosSzekeres/HMPT/Statement.lean): `HMPT.Theorem2020` | Real points only; pseudoline arrangements and families of bodies are not defined. |
| §1, Theorem 1.1 | [Suk/Asymptotic.lean](../ErdosSzekeres/Suk/Asymptotic.lean): `Suk.theorem2016` | The cited Suk bound is independently completed in this library. |
| §1, Theorem 1.2 | [Suk/ExtractionCounting.lean](../ErdosSzekeres/Suk/ExtractionCounting.lean): `Suk.classical_exponential_bound` | **Real only.** No pseudo-configuration theorem. |
| §1, Theorem 1.3 | [HMPT/Asymptotic.lean](../ErdosSzekeres/HMPT/Asymptotic.lean): `HMPT.theorem2020` | Completed **real-point specialization**, in the stronger precise coefficient formulation below. |
| §1, Remark 1.4 | [Statement.lean](../ErdosSzekeres/HMPT/Statement.lean): `HMPT.publishedCoefficient`; [Asymptotic.lean](../ErdosSzekeres/HMPT/Asymptotic.lean): `HMPT.theorem2020` | **Real only**, coefficient `8√2/3` with every positive epsilon. |
| §1, Theorem 1.5 | None | **Not formalized:** convex-body existence theorem. |
| §1, Theorem 1.6 | None | **Not formalized:** transfer between convex bodies and pseudo-configurations. |
| §1, Theorem 1.7 | None | **Not formalized:** convex-body upper bound. |
| §2, Theorem 2.1 / equation (2.1) | [Suk/TransitiveColoring.lean](../ErdosSzekeres/Suk/TransitiveColoring.lean): `Suk.transitive_cups_caps` | Abstract transitive-coloring upper bound. |
| §2, Observation 2.2(i) | Mathlib `convexHull_mono`; [Basic.lean](../ErdosSzekeres/Basic.lean): `GeneralPosition.mono`, `ConvexPosition.mono` | Ordinary real convexity; no separate pseudo-hull monotonicity theorem. |
| §2, Observation 2.2(ii)–(iv) | No corresponding paper statement | **Not formalized** as a topological or cyclic pseudo-hull package. The implemented support-frame proof does not need that package. |
| §2, Observation 2.3(i) | [Suk/SpikeSeparation.lean](../ErdosSzekeres/Suk/SpikeSeparation.lean): `Suk.ClockwiseAnchors.spike_left_boundary`, `Suk.ClockwiseAnchors.spike_right_boundary`, `Suk.ClockwiseAnchors.nonadjacent_spikes_disjoint`; [HorizontalSpike.lean](../ErdosSzekeres/Suk/HorizontalSpike.lean): `Suk.CapFrame.spike_x_bounds` | **Replacement**, for the selected linear support path; not the full cyclic statement. |
| §2, Observation 2.3(ii) | [Suk/AlternatingAnchors.lean](../ErdosSzekeres/Suk/AlternatingAnchors.lean): `Suk.ClockwiseAnchors.odd_mem_even_spike`; [Quadrilateral.lean](../ErdosSzekeres/Suk/Quadrilateral.lean): `Suk.convexPosition_four_same_cell` | Checked insertion/separation steps needed by the proof. The original global cyclic iff is **not formalized**. |
| §2, Theorem 2.4 / equation (2.2) | [Suk/SupportFiber.lean](../ErdosSzekeres/Suk/SupportFiber.lean): `Suk.support_fiber_card_le`; [HMPT/FiniteBound.lean](../ErdosSzekeres/HMPT/FiniteBound.lean): `HMPT.cap_family_bound`, `HMPT.finite_product_bound` | **Replacement** via linear paths, with explicit endpoint factors. The original cyclic positive-product statement is not asserted. |
| §3, Observation 3.1(i)–(ii) | [Suk/TriangleOrder.lean](../ErdosSzekeres/Suk/TriangleOrder.lean): `Suk.triangleOrder_iff`; [BaseOrder.lean](../ErdosSzekeres/Suk/BaseOrder.lean): `Suk.AboveBase.le_iff`; [HMPT/Maxima.lean](../ErdosSzekeres/HMPT/Maxima.lean): `HMPT.SpikeAntichain`, `HMPT.exists_max_chain_antichain` | **Replacement:** use chains and antichains of one actual partial order. The second complementary order is not separately formalized. |
| §3, equation (3.1) | [Maxima.lean](../ErdosSzekeres/HMPT/Maxima.lean): `HMPT.exists_max_chain_antichain` | Attained witnesses and the size-product inequality, including empty sets. |
| §3, Observation 3.2 | No identical declaration; [Suk/AdjacentSpikes.lean](../ErdosSzekeres/Suk/AdjacentSpikes.lean), [SpikeSeparation.lean](../ErdosSzekeres/Suk/SpikeSeparation.lean) supply the needed local consequences | The global two-spike intersection assertion is **not formalized**. |
| §3, Observation 3.3 | [Suk/AdjacentSpikes.lean](../ErdosSzekeres/Suk/AdjacentSpikes.lean): `Suk.AdjacentCapFrames.ordered_pair_right`, `Suk.AdjacentCapFrames.ordered_pair_left` | **Replacement**, the oriented local separation needed for adjacent gluing. |
| §3, Observation 3.4 | [Suk/SpikeSeparation.lean](../ErdosSzekeres/Suk/SpikeSeparation.lean): `Suk.ClockwiseAnchors.incomparable_pair_nonadjacent_same_side` | **Real only**, on a linear support sequence. |
| §3, vertical chains / equation (3.2) | [ChainCapacity.lean](../ErdosSzekeres/HMPT/ChainCapacity.lean): `HMPT.exists_chainCapacities`, `HMPT.ChainCapacities.length_le_binomial` | Attained maxima; parameters are padded for small cases. |
| §3, Observation 3.5 / equation (3.4) | [Suk/AdjacentCaps.lean](../ErdosSzekeres/Suk/AdjacentCaps.lean): `Suk.AdjacentCapFrames.glue_caps`; [HMPT/ChainCapacity.lean](../ErdosSzekeres/HMPT/ChainCapacity.lean): `HMPT.adjacent_cap_budget` | **Real only**, with explicit finite-path and small-case handling. |
| §3, Observation 3.6(i) | [Suk/AntichainExtraction.lean](../ErdosSzekeres/Suk/AntichainExtraction.lean): `Suk.CapFrame.antichain_cup_cap` | **Replacement** by ordinary geometric cups-caps; not the stated pseudo-chain coloring theorem. |
| §3, Observation 3.6(ii) / equation (3.3) | [AntichainCapacity.lean](../ErdosSzekeres/HMPT/AntichainCapacity.lean): `HMPT.InnerCap.convexPosition`, `HMPT.AntichainCapacity.card_le_binomial`, `HMPT.AntichainCapacity.card_lt` | Supported real caps and the sufficient binomial inequality, with padding. |
| §3, Observation 3.7 / equation (3.5) | [Suk/AntichainCaps.lean](../ErdosSzekeres/Suk/AntichainCaps.lean): `Suk.ClockwiseAnchors.convexPosition_union_antichain_caps_of_supports`; [HMPT/AntichainCapacity.lean](../ErdosSzekeres/HMPT/AntichainCapacity.lean): `HMPT.separated_cap_budget`, `HMPT.parity_cap_budget` | **Real only**, arbitrary nonadjacent subfamilies and even/odd budgets on a path. |
| §3, equations (3.6)–(3.8), first bound | [RegionProduct.lean](../ErdosSzekeres/HMPT/RegionProduct.lean): `HMPT.region_product_le`, `HMPT.vertical_budget_le`, `HMPT.support_product_bound`; [ExponentialBound.lean](../ErdosSzekeres/HMPT/ExponentialBound.lean): `HMPT.integer_product_bound` | **Replacement** finite formulas explicitly retain path endpoints and padding losses. |
| §3, Proposition 3.8 | [FanCounting.lean](../ErdosSzekeres/HMPT/FanCounting.lean): `HMPT.convex_family_ratio_bound`; [TwoScale.lean](../ErdosSzekeres/HMPT/TwoScale.lean): `HMPT.convex_two_scale_ratio_bound`, `HMPT.integer_two_scale_bound` | **Replacement** by direct telescoping; the proposition's two-way cyclic alternative is not asserted. |
| §3, equation (3.9) | [Entropy.lean](../ErdosSzekeres/HMPT/Entropy.lean): `HMPT.choose_le_four_mul_pow`, `HMPT.twoScaleProduct_le_common_entropy`, `HMPT.real_entropy_two_scale_bound` | **Replacement** factorial-sensitive estimates and a precise floor bridge. |
| §3, final optimization | [AsymptoticInput.lean](../ErdosSzekeres/HMPT/AsymptoticInput.lean), [ScaleLimits.lean](../ErdosSzekeres/HMPT/ScaleLimits.lean), [Asymptotic.lean](../ErdosSzekeres/HMPT/Asymptotic.lean): `HMPT.normalizedBudget_tendsto`, `HMPT.eventual_bound_of_positive_slack`, `HMPT.theorem2020` | Completed final coefficient for ordinary real points, despite changed intermediate formulas. |
| Acknowledgments and bibliography | [THIRD_PARTY.md](THIRD_PARTY.md) | Attribution, not proof obligations. |

Additional implementation bridges have no separately numbered counterpart:
[HMPT/Projective.lean](../ErdosSzekeres/HMPT/Projective.lean)
(`HMPT.generalPosition_projectFrom`, `HMPT.hasConvexNGon_of_projectFrom`),
[ProjectedCaps.lean](../ErdosSzekeres/HMPT/ProjectedCaps.lean)
(`HMPT.exists_projected_cap`), and [ConvexFan.lean](../ErdosSzekeres/HMPT/ConvexFan.lean)
(`HMPT.ConvexFan.vertices_injective`). They justify applying the linear support-path
counting argument to arbitrary real convex subsets. See [HMPT.md](HMPT.md).

The supplementary [ParameterBarrier.lean](../ErdosSzekeres/HMPT/ParameterBarrier.lean)
has no separately numbered paper counterpart. Its
`HMPT.positive_leading_slack_iff` and
`HMPT.budget_eventually_negative_below_published` exactly delimit retuning
the implemented fixed-scale budget; they do not assert a stronger extremal bound.

The supplementary [DyadicScale.lean](../ErdosSzekeres/HMPT/DyadicScale.lean)
extends the implementation's Proposition 3.8 replacement to a finite number of
doubling stages: `HMPT.convex_dyadic_scale_ratio_bound`,
`HMPT.convex_dyadic_scale_bound`, and `HMPT.dyadic_scale_bound`.
`HMPT.positive_dyadic_leading_budget_iff` optimizes an explicit leading
expression over the integer stage count and positive real scale. These are
supplementary results, not additional claims from HMPT's paper or a stronger
asymptotic coefficient.

The supplementary [BinomialRefinement.lean](../ErdosSzekeres/HMPT/BinomialRefinement.lean)
retains `choose(N,m+1)` at the initial scale of the Proposition 3.8 replacement.
`HMPT.two_scale_binomial_bound`, `HMPT.two_scale_factorial_exponential_bound`,
and `HMPT.suk_two_scale_factorial_bound` strengthen the implemented finite
criteria. `HMPT.twoScaleFactorialExponent_le` compares closed exponents.
The paper already uses binomial subset counting elsewhere; this is a standard
refinement of this finite interface, without an asymptotic or priority claim.

[EndpointBarrier.lean](../ErdosSzekeres/HMPT/EndpointBarrier.lean) adds
`HMPT.normalizedBudget_neg_at_endpoint` and
`HMPT.budget_eventually_negative_at_or_below_published`: the existing entropy
budget fails at equality too, for every fixed positive scale. This is an
analysis of that explicit interface, with no universal impossibility claim
and no assertion about the newer factorial criterion.

## Supplementary project results: coupled residual obstructions

These results have no numbered counterpart in Suk or HMPT and are project
additions, not additional paper formalizations or claims of literature priority.
The declarations below are in `ErdosSzekeres.Omission`. They concern actual
residual configurations of real points in general position with strict horizontal
order, no 6-cap, no convex octagon and no incoming 6-cup/outgoing 5-cap junction.
Their shared order, rank and orientation clauses are proved necessary before
applying kernel-checked finite refutations.

| Project result | Lean files and declarations | Checked scope |
| --- | --- | --- |
| First thirteen-state core | [CoupledObstruction.lean](../ErdosSzekeres/Omission/CoupledObstruction.lean): `CoupledCore13.hole_bound` | At least one specified state is absent. |
| Second thirteen-state core | [CoupledSecondObstruction.lean](../ErdosSzekeres/Omission/CoupledSecondObstruction.lean): `CoupledCoreSecond.hole_bound` | At least one specified state is absent. |
| Third thirteen-state core | [CoupledThirdObstruction.lean](../ErdosSzekeres/Omission/CoupledThirdObstruction.lean): `CoupledCoreThird.hole_bound` | At least one specified state is absent. |
| Fourth thirteen-state core | [CoupledFourthObstruction.lean](../ErdosSzekeres/Omission/CoupledFourthObstruction.lean): `CoupledCoreFourth.hole_bound` | At least one specified state is absent. |
| Fifth thirteen-state core | [CoupledFifthObstruction.lean](../ErdosSzekeres/Omission/CoupledFifthObstruction.lean): `CoupledCoreFifth.hole_bound` | At least one specified state is absent. |
| First and second template families | [CoupledVariants.lean](../ErdosSzekeres/Omission/CoupledVariants.lean): `CoupledVariants.all_rows`; [CoupledSecondVariants.lean](../ErdosSzekeres/Omission/CoupledSecondVariants.lean): `CoupledSecondVariants.all_rows` | 42 and 35 checked supports, with 20 duplicates: **57 distinct rows**. |
| Classification of that frozen union | [UnionCatalog.lean](../experiments/omission-coupled-union-2026-10-10/UnionCatalog.lean): `CoupledUnion.all_rows`; [Independence.lean](../experiments/omission-coupled-union-2026-10-10/Independence.lean): `CoupledUnion.independent_each_selected_row`; [Redundancy.lean](../experiments/omission-coupled-union-2026-10-10/Redundancy.lean): `CoupledUnion.redundant_rows_implied` | Nine rows are individually independent of the original 1,187 rows, prior 45 additions and other 56 union rows; 48 follow from original rows. Independence witnesses have 141 holes, without a realizability claim. Later additions can change independence. |
| Third and fourth template families | [CoupledThirdVariants.lean](../ErdosSzekeres/Omission/CoupledThirdVariants.lean): `CoupledThirdVariants.all_rows`; [CoupledFourthVariants.lean](../ErdosSzekeres/Omission/CoupledFourthVariants.lean): `CoupledFourthVariants.all_rows` | Three selected third-core variants and 24 fourth-core variants; the latter include the fourth core itself. |
| Fifth template family | [CoupledFifthVariants.lean](../ErdosSzekeres/Omission/CoupledFifthVariants.lean): `CoupledFifthVariants.all_rows` | 28 further checked support maps. |
| Eleven-state core | [CoupledElevenObstruction.lean](../ErdosSzekeres/Omission/CoupledElevenObstruction.lean): `CoupledCoreEleven.hole_bound` | At least one of eleven specified states is absent. |
| Nine-state core | [CoupledNineObstruction.lean](../ErdosSzekeres/Omission/CoupledNineObstruction.lean): `CoupledCoreNine.hole_bound` | At least one of nine specified states is absent. |
| Second nine-state support | [CoupledNineVariant.lean](../ErdosSzekeres/Omission/CoupledNineVariant.lean): `CoupledNineVariant.hole_bound` | The same refutation applies after kernel-checking every prerequisite of a new support. No independence claim. |
| Structural nine-state proof and two further rows | [CoupledNineStructural.lean](../ErdosSzekeres/Omission/CoupledNineStructural.lean): `StructuralNine.hole_bound`; [CoupledNineStructuralVariants.lean](../ErdosSzekeres/Omission/CoupledNineStructuralVariants.lean): `StructuralNine111.hole_bound`, `StructuralNineShifted111.hole_bound` | A geometric proof without invoking the CNF refutation; its two further instances give valid nine-state omission rows. |
| Fourteen-state capacity improvement | [CoupledDemandTwo.lean](../ErdosSzekeres/Omission/CoupledDemandTwo.lean): `CoupledDemandTwo.hole_bound`; [TwoHoleAssembly.lean](../ErdosSzekeres/Omission/TwoHoleAssembly.lean): `two_holes_of_deletions` | At least two of fourteen states are absent, using the third core and earlier rows. This is another formulation of the third obstruction relative to those premises, not a second independent discovery. |

These finite geometric constraints do not by themselves establish a new global
octagon bound or improve either paper's asymptotic coefficient. Proof inputs,
axiom audits and discovery provenance are linked from the
[third-party attribution](THIRD_PARTY.md#coupled-residual-obstructions--10-october-2026).

Two further project additions have no numbered paper counterpart.
`ErdosSzekeres.HMPT.integer_two_scale_bound_one_bit_smaller` in
[FactorialSaving.lean](../ErdosSzekeres/HMPT/FactorialSaving.lean): the finite
power-of-two threshold can be halved when its counting term exceeds the
auxiliary floor. [VisibleEdgeInsertion.lean](../ErdosSzekeres/VisibleEdgeInsertion.lean)
proves `VisibleEdgeInsertion.convexPosition_insert_of_one_visible_edge` for an
explicit supporting-edge family with retained vertex coverage.

## Supplementary finite octagon theorem

`ErdosSzekeres.Omission.forces_convex_octagon_314` and
`convex_octagon_of_card_ge_314` in
[FinalCover314B61FusedR31Fused.lean](../experiments/omission-global-assembly-2026-10-10/FinalCover314B61FusedR31Fused.lean)
prove the 314-point ordinary real-plane bound. This is a separate computational
route using the omission method and state catalogs credited to Schroeder's
pinned 2026 archive; it has no numbered counterpart in Suk or HMPT. The
[assembly ledger](../experiments/omission-global-assembly-2026-10-10/README.md)
maps the arithmetic certificates, geometric transfers and final declarations.
It does not change either paper's asymptotic coefficient.

## Supplementary residual32 transfer and branch proofs

These project results have no numbered counterpart in Suk or HMPT.

| Result | Lean file and theorem | Scope |
| --- | --- | --- |
| Full enlarged catalog transfer | [Transfer.lean](../experiments/omission-residual32-transfer-2026-10-10/Transfer.lean): `OmissionResidual32Transfer.all_rows`, `feasible_holes` | All 2,469 exact rows hold for the same actual residual assignment; holes plus points equal 154. |
| Conditional arithmetic interface | Same file: `residual_bound_of_hole_budget` | Converts an explicit, separately proved hole-budget exclusion to a population bound; no 32-hole exclusion is asserted. |
| Five arithmetic contexts | [Context bundle](../experiments/omission-residual32-context-certificates-2026-10-10/README.md): `OmissionResidual32Contexts.node492360`, `node492359`, `node485523`, `node485522`, `node30` | Exclude their stated contexts under explicit literal row validity and at most 32 holes. |
| Actual geometric contexts | [ContextGeometry.lean](../experiments/omission-residual32-transfer-2026-10-10/ContextGeometry.lean): `geometric_node492360`, `geometric_node492359`, `geometric_node485523`, `geometric_node485522`, `geometric_node30`, `geometric_parent492360`, `geometric_parent485523`, all in `OmissionResidual32Transfer` | Discharge row validity for actual residual configurations of at least 122 points; the two parent results eliminate one split assumption each. |
| Mandatory zero state | [ZeroState.lean](../experiments/omission-residual32-context-certificates-2026-10-10/ZeroState.lean): `OmissionResidualZeroState.zero_mem_residualOccupied` | Every nonempty actual residual configuration occupies catalog state zero. |
| Six newly closed subtrees | [Resumed Lean bundle](../experiments/omission-residual32-resume-lean-2026-10-10/README.md): `OmissionResidual32Resume.Context492357.excludes_context`, and corresponding declarations for `Context29`, `Context485519`, `Context492355`, `Context485517`, `Context24` | Each proves its full inherited context impossible at 32 holes; the same bundle's `Geometry.lean` discharges row validity for actual configurations with at least 122 points. All 44 splits and 50 weighted leaves are checked. |

The precise 2,469-row provenance table is in the
[transfer bundle](../experiments/omission-residual32-transfer-2026-10-10/README.md).
These theorems do not complete the 313-point target.

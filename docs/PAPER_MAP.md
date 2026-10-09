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

# Review of the geometric boundary and certificate linking

The closed `FinalCover316` and earlier `FinalCover317` compositions have passed
the complete gate and standard-axiom audits; see their separate
`global-cover-316-check.json` and `global-cover-317-check.json` records. This review explains
their mathematical boundary. Historical `Final317`/`Final318` routes and stronger
candidate assemblies are distinct and retain their separately stated status.

* `Point` is `Fin 2 → ℝ`. `GeneralPosition` rules out collinearity of every
  triple of distinct members of the original finite set. No ordering,
  rational-coordinate, realizability, or additional genericity assumption is
  imposed on that set.
* `HasConvexNGon 8 S` supplies an eight-element subset of `S` whose members
  are `ConvexIndependent ℝ`. Other points may lie inside its convex hull;
  this is the ordinary convex-octagon problem, not the empty-octagon problem.
* `exists_cap_free_chart` retains the exact equation `S.card = n + 1`.
  The configuration comes from an invertible linear normalization, one
  deleted root, and a projective chart. Both cap and octagon avoidance are
  derived from octagon avoidance in the original real point set.
* `Partition.exists_partition` proves coverage, disjointness, and the exact
  cardinality sum. Its balanced part avoids 7-caps, 7-cups, and octagons.
  Its residual part avoids 6-caps and octagons, and satisfies the proved
  no-junction restriction. These restrictions are not final hypotheses.
* `OmissionResidual.feasible_holes` maps every actual residual configuration
  into a Boolean hole vector satisfying all 1,187 geometric inequalities,
  with `sum holes + n = 154`. Excluding total at most 29 therefore gives
  residual population at most 124. Excluding at most 30 gives at most 123.
* The root and the strict forcing threshold contribute one point each:
  balanced 192 plus residual 124 permits at most 317 avoiding points and
  forces an octagon at 318. Residual 123 gives the threshold 317; balanced 191 plus residual 123 gives 316.
* Historical fallback catalogs use different packing
  bases. `OmissionResidual124.catalog_matches` checks equality of the
  geometric supports and demands; the exclusion transfer uses precisely
  these equalities. Equality of the irrelevant packed codes is not assumed.
* The checked cover route derives 402 residual and 220 balanced inequalities
  from the original rows using nonnegative integer sums and Boolean upper
  bounds. Its two bridges kernel-check every original and added support and
  demand before transferring the compressed exclusions. No additional
  geometric or realizability premise is introduced by these arithmetic cuts.
* The final source statements have no free population-bound variables or
  arithmetic hypotheses. Their only geometric hypotheses are general
  position and the asserted cardinality threshold. Both `FinalCover316` and
  `FinalCover317` passed
  compilation and the final audit, with only `propext`, `Classical.choice`,
  and `Quot.sound`; stronger candidate files still require their own checks.

The assembly checker binds each selected catalog and compiled geometry
dependency to the record that checked it. It rejects partial families,
changed source/object hashes, wrong arithmetic targets, mismatched toolchains,
nonstandard axioms, and unlisted compiled objects that might shadow another
family's imports. Fourteen global-gate and versioned-profile controls pass. A historical attempt
at threshold 318 correctly refused the incomplete residual124 family before
launching an assembly compilation.

The maintained proof sources reviewed here are `Definitions.lean`,
`Omission/Realization.lean`, `Omission/ProjectiveTransfer.lean`,
`Omission/Partition.lean`, and `Omission/PopulationBounds.lean`, together with
the checked `ResidualReduction`, `ResidualBudgets`, `BalancedBudgets`, both
cover catalog bridges, and the closed `FinalCover317` source in this directory.

# Erdős–Szekeres in Lean

A starting formalization of the convex polygon conjecture:

> For every integer n ≥ 3, every set of at least 2^(n−2) + 1 points in the real
> plane, with no three collinear, contains n points in convex position.

**This repository does not prove or disprove the open conjecture.** The conjecture
is a `Prop` definition, not an assumed axiom or an unfinished theorem. Polygons
here need not be empty: unselected points may lie inside them.

Local validation: `lake build --wfail` passes, and all fifteen core Python tests
pass (plus four optional Z3 tests locally). The principal geometric lemmas and rational-area bridge were inspected with
`#print axioms`; CI also audits 139 geometric and combinatorial milestones. Only `propext`, `Classical.choice`, and `Quot.sound` occur.
The project contains no proof placeholders or additional axioms.

## Current contents

- `ErdosSzekeres/Definitions.lean`: real plane, general position, convex position,
  containment of an n-gon, sufficient bounds, full conjecture and the 33-point case.
- `ErdosSzekeres/Basic.lean`: subset monotonicity, cardinality bounds, equivalence
  of exact and at-least cardinalities, affine-to-convex independence, the n = 3
  case, and the implication from a geometric counterexample to refutation.
- `ErdosSzekeres/Orientation.lean`: signed area over a commutative ring, permutation
  and translation identities, and preservation of rational signed area in ℝ.
- `ErdosSzekeres/OrientationGeometry.lean`: signed area is zero exactly when the
  triple is collinear, and rational general position transfers to the real plane.
- `ErdosSzekeres/Counting.lean`: exact binomial budget inequalities, with geometric
  assumptions kept explicit.
- `ErdosSzekeres/DyadicModel.lean`: telescoping and an exact all-scale coefficient
  inequality for a restricted counting model.
- `ErdosSzekeres/Suk/`: checked four-point criterion, classical cups-caps bound,
  Dilworth consequence, transitive-coloring clique bound, arbitrary-base triangle
  order with antichain separation, geometric chain-color transitivity, region
  selection, convex-subset counting, triangle membership and four-point gluing
  criteria. The finite geometric chain case is checked, including cap extraction,
  adjacent-chain gluing, growth to n vertices, and terminal small-cap cases.
  Finite-set chains and a clockwise support sequence supply the ordering and
  adjacency data. The quadrilateral proof exhausts all sixteen orientation-sign cases.
  The finite antichain case is also checked: extraction supplies its local
  supporting edges, and nonadjacent caps glue with additive cardinality.
  `FiniteSupport.lean` combines both cases and Dilworth into one geometric
  theorem for a sufficiently populated horizontal support configuration.
  The extraction bridge is now checked: cup/cap density, alternating anchors,
  product counting, coarsening of support regions, reflection, and rotation.
  `FiniteBound.lean` gives an unconditional geometric conclusion under explicit
  integer inequalities. `IntegerParameters.lean` specializes it to a closed
  exponential bound with cubic parameters (see `docs/SUK.md`).
  `Asymptotic.lean` proves **Suk's 2016 Theorem 1.1**: for all sufficiently
  large n, at least floor(2^(n + 6 n^(2/3) log₂ n)) points in general position
  force a convex n-gon. The theorem is `ErdosSzekeres.Suk.theorem2016`.
- `ErdosSzekeres/HMPT/Statement.lean`: precise targets for the final 2020
  coefficient and a strict improvement; these are propositions, not proved bounds.
- `ErdosSzekeres/HMPT/`: the finite product method is now checked for real point
  sets, including attained geometric maxima, adjacent and parity cap budgets,
  product counting, and extraction. `integer_product_bound` gives a computable
  sufficient exponent for every n ≥ 4 and positive region count. Endpoint and
  padding losses are explicit; the final 2020 coefficient is still unproved.
  See `docs/HMPT.md` for the exact formula and remaining dependencies.
  A projective normalization now connects general convex-subset counts to the
  support paths. `suk_bootstrap_bound` feeds the proved finite Suk result through
  this bridge. The genuine convex-subset ratio and its two-scale composition
  are now proved, as are the factorial-sensitive binomial estimate and the
  exact floor bridge. `suk_entropy_two_scale_bound` gives a closed exponent
  without binomial coefficients; the final eventual optimization remains.
- `scripts/repair_near_miss.py`: recorded single-vertex repair attempts on
  configurations with a small number of forbidden polygons.
- `scripts/product_bound_search.py`: exact integer search of the proved finite
  product formula, with independent checks of the original density inequality.
- `scripts/search.py`: exact integer-coordinate grid search using convex hulls.
- `scripts/extend_configuration.py`: full-plane extension and point replacement
  for fixed realizable configurations, with exact candidate verification.
- `scripts/joint_vertical_repair.py`: simultaneous point moves with fixed x
  coordinates, exact linear cuts and exhaustive final candidate checks.
- `scripts/mutation_campaign.py`: bounded, recorded exploration of point moves.
- `scripts/replay_smt.py`: corroboration of extension formulas with cvc5.
- `scripts/test_search.py`: geometric fixtures and an independent triangle-based
  convexity cross-check over small configurations.
- `experiments/`: reproducible bounded-search results, explicitly not Lean proofs.
- `docs/SUK.md`: dependency ledger for the full 2016 theorem.
- `docs/THIRD_PARTY.md`: attribution and licenses for adapted prerequisites.
- `docs/RESEARCH.md`: dependency map, references, computational limits and next steps.
- `docs/COUNTING.md`: final HMPT benchmark, arithmetic experiments, and recent
  research directions. These experiments have not improved the published bound.
- `docs/SAT.md`: known-case SAT reproduction, certificate hashes, coordinate
  realization, and the placeholder-axiom gap found in the upstream CNF conversion.

## Build

Pinned to Lean **4.24.0** and Mathlib **v4.24.0**; `lake-manifest.json` fixes the
dependency commits. These are deliberate reproducible baseline versions.

With Lean's `elan` toolchain manager installed:

```sh
lake exe cache get
lake build
python3 -m unittest discover -s scripts -v
python3 scripts/search.py --grid 4 --points 5 --gon 4
```

The initial Mac setup installed `elan` inside this workspace, without modifying
shell configuration. In this checkout, invoke Lake with:

```sh
ELAN_HOME="$PWD/.elan" .elan/bin/lake build
```

Python uses only the standard library. The core tests do not require a SAT solver.
Ignored local inspection tools include CaDiCaL, drat-trim, and the pinned
EmptyHexagonLean development; these are separate from the main Lean dependency.

## First experiments

The 4×4 integer grid has 4,368 five-point subsets. Of these, 1,668 are in general
position, and every one contains a convex quadrilateral. Separately, the search
finds a four-point general-position configuration with no convex quadrilateral:
`(0,0), (0,1), (1,1), (3,2)`.

These are small regression experiments. Exhausting one grid does not exhaust
all planar configurations, and the four-point example is below the conjectured
five-point threshold. Neither experiment resolves an open case.

## Current milestone

Suk's 2016 upper bound is now fully proved for arbitrary real point sets in
general position. The proof includes a variant of positive-fraction extraction,
the finite chain/antichain argument, integer rounding, and the final eventual
estimate. See `docs/SUK.md` for the dependency ledger and exact scope.

The research goal now continues toward an improvement over final HMPT 2020.
The geometric product argument now yields a complete finite upper-bound formula.
Neither the final 2020 asymptotic theorem nor a strict improvement has been proved.
The completed Suk formalization is not a new published-bound improvement.

The rational witness checker and end-to-end SAT certificate conversion remain
separate unfinished work; the upstream CNF conversion needs repair before its
UNSAT results can become complete Lean proofs. Search timeouts are inconclusive.

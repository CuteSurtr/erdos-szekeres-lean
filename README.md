# Erdős–Szekeres in Lean

A starting formalization of the convex polygon conjecture:

> For every integer n ≥ 3, every set of at least 2^(n−2) + 1 points in the real
> plane, with no three collinear, contains n points in convex position.

**This repository does not prove or disprove the open conjecture.** The conjecture
is a `Prop` definition, not an assumed axiom or an unfinished theorem. Polygons
here need not be empty: unselected points may lie inside them.

Initial local validation: `lake build --wfail` passes, and all four Python tests
pass. The principal geometric lemmas and rational-area bridge were inspected with
`#print axioms`: only `propext`, `Classical.choice`, and `Quot.sound` occur.
The project contains no proof placeholders or additional axioms.

## Current contents

- `ErdosSzekeres/Definitions.lean`: real plane, general position, convex position,
  containment of an n-gon, sufficient bounds, full conjecture and the 33-point case.
- `ErdosSzekeres/Basic.lean`: subset monotonicity, cardinality bounds, equivalence
  of exact and at-least cardinalities, affine-to-convex independence, the n = 3
  case, and the implication from a geometric counterexample to refutation.
- `ErdosSzekeres/Orientation.lean`: signed area over a commutative ring, permutation
  and translation identities, and preservation of rational signed area in ℝ.
- `scripts/search.py`: exact integer-coordinate grid search using convex hulls.
- `scripts/test_search.py`: geometric fixtures and an independent triangle-based
  convexity cross-check over small configurations.
- `experiments/`: reproducible bounded-search results, explicitly not Lean proofs.
- `docs/RESEARCH.md`: dependency map, references, computational limits and next steps.

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

Python uses only the standard library. No SAT solver is required yet.

## First experiments

The 4×4 integer grid has 4,368 five-point subsets. Of these, 1,668 are in general
position, and every one contains a convex quadrilateral. Separately, the search
finds a four-point general-position configuration with no convex quadrilateral:
`(0,0), (0,1), (1,1), (3,2)`.

These are small regression experiments. Exhausting one grid does not exhaust
all planar configurations, and the four-point example is below the conjectured
five-point threshold. Neither experiment resolves an open case.

## Next milestone

Connect the determinant computation to Mathlib's `Collinear` and `convexHull`,
then build a Lean-verified checker for rational witnesses. For universal finite
cases, assess porting the existing ordinary-polygon SAT reduction in
[EmptyHexagonLean](https://github.com/bsubercaseaux/EmptyHexagonLean), starting
with known cases before attempting 33 points.

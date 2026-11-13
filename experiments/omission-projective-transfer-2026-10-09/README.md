# Balanced bound combined with the projective transfer

[BalancedProjective.lean](BalancedProjective.lean) proves:

> An octagon-free real point set in general position with at least 194 points
> has an actual root-deletion chart containing a 7-cup. The chart avoids 7-caps
> and convex octagons and has exactly one fewer point than the original set.

The theorem is `OmissionBalanced.large_avoiding_set_has_chart_cup`.
`IsRootDeletionChart` retains witnesses for the invertible linear normalization,
the root, the positive-denominator domain, and the exact projected point set.
This is **not ES(8) ≤ 194 or ES(8) ≤ 317**. It identifies the cup-containing
case that the remaining asymmetric population argument must control.

The [projective proof map](../../docs/OMISSION_PROJECTIVE.md) gives the main
library declarations. `forces_317_of_asymmetric_315` is conditional on the
still-unproved proposition `AsymmetricBound 315`.

## Reproduce

Build the main library. Reproduce the complete
[balanced arithmetic certificate](../omission-balanced-lean-2026-10-09/README.md)
and [balanced geometry certificate](../omission-balanced-geometry-2026-10-09/README.md)
first. Using the output directories from those READMEs:

```sh
lake env sh -c 'LEAN_PATH="$PWD/.cache/omission-balanced-geometry-replay:$PWD/.cache/omission-balanced-lean:$LEAN_PATH" lean -j 1 -s 32768 -M 6000 experiments/omission-projective-transfer-2026-10-09/BalancedProjective.lean'
```

On the original Mac, use `ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place of
`lake`. The large certificate prerequisites were already checked; this checkpoint
composes them with the new library result rather than rebuilding their trees.
The source and input hashes, current axiom output, and main-library checks are
recorded in `validation.json` and `axioms.txt`. Compiled objects remain ignored.

## Attribution

The root/chart argument follows Michael Schroeder's version-1 archive,
19 September 2026, [DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
The main library's adapted argument is MIT; the previous balanced catalog and
cycle data are CC BY 4.0. The cardinality composition in this file is added here.
See [THIRD_PARTY.md](../../docs/THIRD_PARTY.md) for exact provenance. No priority
or best-bound claim is made for this structural consequence.

# Balanced certificate combined with the completed partition

[BalancedPartition.lean](BalancedPartition.lean) connects the separately checked
192-point balanced theorem to the completed minimum-slope partition and
projective/root transfer.

| Theorem in `OmissionBalanced` | Checked conclusion |
| --- | --- |
| `balanced_bound_192` | Supplies the actual balanced population bound with no additional hypothesis. |
| `asymmetric_315_of_residual_123` | `Partition.ResidualBound 123 → AsymmetricBound 315`. |
| `forces_317_of_residual_123` | `Partition.ResidualBound 123 → ForcesConvexNGon 317 8`. |
| `large_avoiding_set_has_residual` | Any octagon-free general-position set of at least 317 real points has an actual root-deletion chart with an induced residual subset of at least 124 points, no 6-cap, no octagon and no six-cup/five-cap junction. |

**The residual bound of 123 remains unproved. This does not prove ES(8) ≤ 317.**
The partition and projective steps are complete, so the remaining hypothesis
now refers only to residual configurations. See the
[proof map](../../docs/OMISSION_PARTITION.md) for its exact definition.

## Reproduce

Build the pinned main library, then reproduce the
[balanced arithmetic certificate](../omission-balanced-lean-2026-10-09/README.md)
and [balanced geometry certificate](../omission-balanced-geometry-2026-10-09/README.md).
Using the output directories from those READMEs:

```sh
lake env sh -c 'LEAN_PATH="$PWD/.cache/omission-balanced-geometry-replay:$PWD/.cache/omission-balanced-lean:$LEAN_PATH" lean -j 1 -s 32768 -M 6000 experiments/omission-partition-2026-10-09/BalancedPartition.lean'
```

On the original Mac, use `ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place of
`lake`. This checkpoint composes the previously checked balanced objects with
the new partition proofs; it does not rebuild their large proof trees.
The exact axiom output is in [axioms.txt](axioms.txt). The
[validation manifest](validation.json) records sources, prerequisite bindings,
compiled-object hashes and main-library checks. Compiled objects are ignored.

## Attribution

The minimum-slope partition and three-chain strategy follow Michael Schroeder's
version-1 archive, 19 September 2026,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
Adapted proof code is MIT; the balanced catalog/cycle data are CC BY 4.0.
The composition in this file is added here. See
[THIRD_PARTY.md](../../docs/THIRD_PARTY.md) for module mappings and licenses.

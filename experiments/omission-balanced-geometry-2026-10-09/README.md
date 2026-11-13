# Balanced geometric bound: proof sources and reproduction

This bundle connects the balanced omission certificate to actual real points.
**All checks completed successfully on 9 October 2026.** The 86 module checks
(occupancy, 84 row blocks, final assembly) took about 22.6 minutes on the original
Mac. The [full build record](kernel-check.json), [final axiom output](final-axioms.txt)
and [validation manifest](validation.json) record the exact checked files.
Its final statement, in [BalancedGeometry.lean](BalancedGeometry.lean), is:

```lean
OmissionBalanced.real_configuration_bound
  {n : ℕ} (c : ErdosSzekeres.Omission.Configuration n)
  (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
  (noOctagon : ¬ ErdosSzekeres.HasConvexNGon 8 (Finset.univ.image c.point)) :
  n ≤ 192
```

`Configuration` means actual real points, strictly increasing x-coordinates,
and nonzero orientations of all increasing triples. Cups and caps use the signs
of **all** increasing triples of the selected points. The configuration cannot
contain a convex octagon, a 7-cup, or a 7-cap. See the
[geometric proof map](../../docs/OMISSION_GEOMETRY.md).

This is a restricted geometric statement. **It does not prove ES(8) ≤ 317** or
improve HMPT's asymptotic coefficient. The residual geometry and global
partition/projective transfer are still separate obligations.

## What the check does

The archive contains 85 Lean source files: 84 blocks covering all 2,685 cycles,
and the final assembly. Each block proves that its literal cycle orders satisfy
the geometric sign condition, that their supports equal the arithmetic catalog
rows, and that their lengths minus seven equal the row demands. These finite
checks use `decide +kernel`. The generic geometric theorem then derives every
row from the actual-point hypotheses.

The final theorem combines all rows with the previously checked
`OmissionBalanced.occupied_card_le`. The balanced arithmetic tree is in the
[separate arithmetic bundle](../omission-balanced-lean-2026-10-09/README.md):
9,862 leaves, 898 parts, and the root. It is a prerequisite, not duplicated here.

`export.json` records source generation only, hence `lean_checked: false`.
Completed checks are recorded separately in `kernel-check.json`; generation
and successful kernel checking are different events. Compiled objects are not
included. The loose `BalancedGeometry.lean` is a review copy of the identically
hashed source inside the archive.

## Reproduce

Build the pinned main library and the entire arithmetic bundle first, following
its README. Then, from the repository root:

```sh
mkdir -p .cache/omission-balanced-geometry-replay
tar -xzf experiments/omission-balanced-geometry-2026-10-09/sources.tar.gz \
  -C .cache/omission-balanced-geometry-replay
cp experiments/omission-balanced-geometry-2026-10-09/export.json \
  .cache/omission-balanced-geometry-replay/export.json
lake env python3 scripts/check_omission_geometry.py \
  .cache/omission-balanced-geometry-replay \
  --arithmetic .cache/omission-balanced-lean --resume
```

The checker also compiles the arithmetic bundle's `Occupancy.lean`, then checks
all geometry blocks sequentially and the final assembly. Each step requires
the expected axiom report, allowing only `propext`, `Classical.choice`, and
`Quot.sound`. Resume records bind source manifests, the pinned toolchain,
compiled local prerequisites and compiled outputs. Run under `lake env` so
the correct Lean and Mathlib are selected. The original Mac uses
`ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place of `lake`.

For regeneration from the original version-1 archive:

```sh
python3 scripts/omission_geometry_export.py /path/to/es7_es8_bounds_81_319_v1 \
  --output .cache/omission-balanced-geometry-regenerated
```

Use a fresh output directory. The exporter checks the cycle/support matching
before emitting code, but its output is untrusted until Lean accepts it.
The default CI builds the generic geometry and first-row theorem and exercises
a valid cycle and a deliberately corrupted cycle. It does not rebuild the
large standalone certificates.

## Attribution

The exact 2,685 cyclic orders and catalog indices come from Michael Schroeder,
[*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*, version 1,
19 September 2026](https://doi.org/10.5281/zenodo.22842891), under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This adaptation keeps
those orders and adds local kernel checks, row equalities and geometric
composition. The archive's weaker balanced capacity was 193; the stronger
arithmetic certificate here excludes one further point in the balanced subcase.
No priority, best-bound or author-endorsement claim is made.

Several maintained geometric proof modules adapt MIT code from that archive;
the precise mapping and local additions are listed in
[THIRD_PARTY.md](../../docs/THIRD_PARTY.md), with the complete
[MIT license](../../docs/SCHROEDER-MIT.txt). The final proof uses computed boxes
whose correctness is proved uniformly, rather than the upstream literal box
table or its native-evaluation validators.

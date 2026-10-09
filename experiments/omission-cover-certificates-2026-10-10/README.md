# Exact cover cuts and compressed omission certificates

This artifact records arithmetic consequences of the pinned omission catalogs.
The catalogs, states and original geometric method are from Michael Schroeder,
version 1, 19 September 2026, [DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
Original data are CC BY 4.0; adapted code attribution remains in
[THIRD_PARTY.md](../../docs/THIRD_PARTY.md).

## Checked rounding cuts

`ResidualCoverCuts.all_rows` derives 402 additional arithmetic rows from all
1,187 original residual rows. `BalancedCoverCuts.all_rows` derives 220 rows
from the 2,685 original balanced rows. Both complete transfer modules passed
Lean 4.24.0 and their transitive axiom audits report only `propext`,
`Classical.choice` and `Quot.sound`. The saved sources and check records are
beside this README. They assume Boolean holes and the original row inequalities;
they add no geometric hypothesis.

The generic proof is `OmissionCertificates.rounded_cover_cut` in
[CoverCuts.lean](../../ErdosSzekeres/Omission/CoverCuts.lean). A nonnegative integer
weighted sum of existing rows, together with the Boolean upper bounds, gives
an upper capacity for a chosen support. A strict integer margin rules out
one fewer hole than the asserted target. Derived rows may be used as premises
of later rows; the saved cut DAG fixes a topological order. Numerical solvers
propose the multipliers, but Lean rechecks the full integer inequality.

## Complete arithmetic roots and stronger candidates

| Original catalog | Excluded hole budget | Complete exact tree | Previous tree for this budget | Lean arithmetic status |
| --- | ---: | ---: | ---: | --- |
| Residual, 154 states |30|4,686 leaves|145,474 leaves|Complete: 149 parts, catalog and root|
| Balanced, 252 states |59|711 leaves|9,862 leaves|Complete: 17 parts, catalog and root|
| Balanced, 252 states |60|3,954 leaves|No completed previous tree|Complete: 92 parts, catalog and root|

The residual30 and balanced60 roots have now been composed with all geometric
prerequisites into **`ForcesConvexNGon 316 8`**. The earlier complete317 proof
using balanced59 remains available. All three successful kernel records and
source-only archives are saved here; no proof obligation remains for either
closed threshold.

`ResidualCountermodel.lean` is a separate checked result: one explicit 32-hole
assignment satisfies all 1,187 original rows, all 21 earlier additions, and all
24 new block rows. Its six audited results use only standard axioms. Exact
integer replay also verifies all 402 derived cuts; those cuts follow from the
original rows. This abstract 122-occupied-state model has no claimed real-point
realization. It shows that the stated arithmetic system cannot exclude 32 holes,
not that a residual geometric configuration of that size exists.

## Reproduction

Use the pinned original archive catalogs described in
[OMISSION.md](../../docs/OMISSION.md), the repository's Lean toolchain, and
Mathlib dependencies. Set `source_dir` to the archive's `certificates` directory.
Output directories must be new; generated code and objects stay in `.cache/`.

```sh
python3 scripts/omission_cover_export.py "$source_dir/residual.json" \
  experiments/omission-cover-certificates-2026-10-10/residual-cuts.json \
  --family residual --output .cache/reproduce-cover-residual
python3 scripts/omission_cover_export.py "$source_dir/balanced.json" \
  experiments/omission-cover-certificates-2026-10-10/balanced-cuts.json \
  --family balanced --output .cache/reproduce-cover-balanced
python3 scripts/omission_lean_export.py .cache/reproduce-cover-residual/source.json \
  experiments/omission-cover-certificates-2026-10-10/residual-30-tree.json.gz \
  --output .cache/reproduce-cover-residual-tree \
  --namespace OmissionResidualCover --module-prefix ResidualCoverProof --leaf-limit 48
python3 scripts/omission_lean_export.py .cache/reproduce-cover-balanced/source.json \
  experiments/omission-cover-certificates-2026-10-10/balanced-59-tree.json.gz \
  --output .cache/reproduce-cover-balanced-tree \
  --namespace OmissionBalancedCover --module-prefix BalancedCoverProof --leaf-limit 64
lake env python3 scripts/check_omission_lean.py \
  .cache/reproduce-cover-residual-tree --resume --workers 2 --memory 2200
lake env python3 scripts/check_omission_lean.py \
  .cache/reproduce-cover-balanced-tree --resume --workers 2 --memory 2200
```

The exporter replays the exact cut DAG before writing anything and reproduces
the stored augmented source bytes. The tree exporter independently checks the
complete branch cover and every integer leaf margin. Neither Python check is
counted as a Lean proof. See the
[global assembly guide](../omission-global-assembly-2026-10-10/README.md)
for the original catalog, geometric rows, cut-transfer checks and final gate.
The workspace-local invocation on this Mac is
`ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place of `lake`.

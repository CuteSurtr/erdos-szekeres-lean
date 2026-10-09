# Additional residual rows and irredundancy

The maintained theorem
`ErdosSzekeres.Omission.AdditionalResidualRows.all_rows` proves 20 cycle
inequalities and one capacity-22 block inequality for actual residual
configurations of real points. It is part of the default library build.
The exact hypotheses are no 6-cap, no convex octagon and no incoming-6-cup /
outgoing-5-cap junction, in a strictly x-ordered general-position configuration.

`AdditionalResidualStrictness.independent_each_additional_row`, in
[Irredundancy.lean](Irredundancy.lean), proves that each added row excludes an
abstract occupied set satisfying all 1,187 original rows and every other
added row. [CycleIndependence.lean](CycleIndependence.lean) checks the 20
cycle witnesses against the original catalog; [BlockIndependence.lean](BlockIndependence.lean)
checks the 23-state block witness. None of these witnesses is claimed to be
geometrically realizable. No total population or global ES bound follows just
from irredundancy.

The [kernel record](kernel-check.json) saves source/object hashes and all
10 axiom reports, including the reused catalog's report. Only `propext`,
`Classical.choice` and `Quot.sound` are allowed. Compiled objects remain ignored.
The exact candidate data is in [the adjacent JSON](../omission-additional-rows-2026-10-10.json).
[Search results](search-results.json) distinguish numerical observations and
exact Python checks from the Lean theorems. See the [research report](../../docs/RESEARCH_2026-10-10.md).

## Reproduction

From the repository root, with its pinned Lean/Mathlib 4.24.0 installation:

```sh
lake build --wfail
lake env python3 scripts/check_additional_residual_rows.py \
  --work .cache/additional-rows-reproduction \
  --output .cache/additional-rows-check.json
ERDOS_LEAN_EXPORT_TEST=1 lake env python3 -m unittest discover \
  -s scripts -p test_additional_residual_rows.py -v
```

If using the repository-local toolchain, set `ELAN_HOME="$PWD/.elan"` and use
`.elan/bin/lake` in place of `lake`. The reproduction script decompresses the
attributed, hash-pinned `Catalog.lean.gz` from the earlier residual artifact,
checks it afresh, and then checks the three proof files above. It does not
need the 145,474-leaf arithmetic tree or the discovery scripts.

The tests compare every candidate literal with the maintained Lean source,
verify all 21 separating assignments with exact integer arithmetic, and
check that Lean rejects a reversed cycle and collapsed block thresholds.

The optional `lp_pruning_probe.py` repeats the bounded LP-assisted pruning
experiment using the preserved row JSON and tree, with `highspy` and `numpy`
installed. Run it from the repository root. It writes only to `.cache/` and
does not generate or certify a new Lean tree.

## Provenance

State numbering and geometric methods derive from Michael Schroeder,
*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*, version 1,
19 September 2026, [DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
The original residual catalog SHA-256 is
`bccd12477064d8a490bbe863ae49dbc8d9dfececf7a65426ba36f7537c66293a`.
The reused catalog and derived state-index data retain [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
attribution. These 21 rows were found locally outside that pinned row list;
no priority or endorsement claim is made. Their geometry uses the separately
attributed MIT adaptations and Baek Apache-2.0 port described in
[THIRD_PARTY.md](../../docs/THIRD_PARTY.md).

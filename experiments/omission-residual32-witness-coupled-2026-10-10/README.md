# A new obstruction to the case-4 witness

All three Lean modules are complete. The new demand-one row is

```text
{25,43,53,65,74,85,89,91,96,107,110,111,125} : at least one hole.
```

It holds for every actual residual configuration: real planar points in
general position and strict x-order, no six-cap, no convex octagon, and no
six-cup/five-cap junction. All selected owners belong to the same configuration.
The [case-4 witness](../omission-residual32-case4-2026-10-10/README.md) occupies
all thirteen states while satisfying all 2,469 old rows. Thus the new inequality
strictly strengthens that Boolean relaxation. It does **not** establish a
33-hole minimum or ES(8) ≤ 313.

| File | Namespace under `ErdosSzekeres.Omission` | Conclusions |
| --- | --- | --- |
| `LeanCore.lean` | `CoupledCoreSixth` | `context_impossible`: the literal coupled formula contradicts the shared geometric context |
| `Geometry.lean` | `CoupledCoreSixth` | `exists_missing_state`, `hole_bound`, `strict_strengthening`, `countermodel_not_realizable`, plus finite injectivity and violation checks |
| `TemplateRow.lean` | `CoupledFourthWitnessVariant` | `checked`, `hole_bound`, `witness_violates_row`, `strict_strengthening` for the map below |

The second checked support comes from the existing Fourth template, with
ordered substitution `[6,14,20,21,11,27,29,32,17,37,41,45,65]`. It also excludes
the witness. This is row zero of the separately checked
[128-map family](../omission-residual32-fourth-global-variants-2026-10-10/README.md),
so it is not counted twice in the strengthened catalog.

## Certificate and checks

`core13.json`, `core13.cnf`, and `core13.lrat` preserve **337 variables,
376 clauses and 258 positive-hint RUP steps**. The Lean exporter connects
every retained clause to actual order, ranks and orientations, and Mathlib's
LRAT proof-term generator checks the refutation through Lean's kernel.
`kernel-check.json` records all three successful modules and eleven audited
conclusions; `axioms.txt` contains only `propext`, `Classical.choice`, and
`Quot.sound`. No proof placeholder, custom axiom or native-evaluation oracle
is used.

The independent standard-library checker replays every RUP step and thirteen
one-state-deletion models, binding the models' state profiles to the frozen
source. The deletion assignments satisfy the necessary discovery constraints;
they are not real-point realizations or a Lean minimality theorem. Seven
negative/replay controls include damaged formula, damaged derivation, and
mismatched core, profiles and source identity.

```sh
python3 experiments/omission-residual32-witness-coupled-2026-10-10/check.py
python3 experiments/omission-residual32-witness-coupled-2026-10-10/test_check.py
lake build --wfail
lake env python3 scripts/check_residual32_continuation.py
```

The final command is the portable CI gate. It compiles prerequisite experiment
sources into fresh ignored cache and checks their axiom output; it does not
reuse Mac object hashes. `check_lean.py` preserves the original local check
and expects the case-4/catalog objects matching their saved records. This Mac
uses `ELAN_HOME="$PWD/.elan" .elan/bin/lake` in place of `lake`.

## Discovery and provenance

`probe.py` searches small subsets of the witness's 122 occupied states using
one shared order/rank/orientation model. Its eighth candidate was a forbidden
16-state support. `minimize.py` reduced that support to thirteen; `cnf_export.py`
and `trim.py` preserve the encoding and refutation-reduction code. Their
bounded exploratory outputs are in `discovery-results.json` and
`discovery-minimal-core.json`. Large raw formulas, solver outputs and compiled
objects remain in ignored `.cache/`.

Discovery scripts use the recorded workspace cache paths. To rerun discovery,
materialize `experiments/omission-residual32-research-2026-10-10/source.json.gz`
as `.cache/residual32-resume-2026-10-10-b/source.json`, then run `probe.py`,
`minimize.py`, and `cnf_export.py` from the repository root with Z3 and NumPy
installed. CaDiCaL produces the raw textual LRAT proof before `trim.py` runs.
Replaying the committed certificates needs none of these solver dependencies.

`model-provenance.json` identifies the archived earlier coupled model and
the exact pair-domain helper source used to construct the self-contained
`model.py`. The old helper need not be present for replay or discovery.
Schroeder's state numbering and derived catalog data retain their CC BY 4.0
attribution; the adapted geometric interfaces retain their original MIT
notices. See [THIRD_PARTY.md](../../docs/THIRD_PARTY.md). CaDiCaL, Z3 and
third-party solver binaries are not vendored. No priority claim is made.

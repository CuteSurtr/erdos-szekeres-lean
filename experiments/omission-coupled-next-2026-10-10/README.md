# A second coupled geometric obstruction

`ErdosSzekeres.Omission.CoupledCoreSecond.hole_bound`, in
[CoupledSecondObstruction.lean](../../ErdosSzekeres/Omission/CoupledSecondObstruction.lean),
proves that every actual residual configuration omits at least one state from

`[16,25,30,39,43,50,53,62,65,77,79,91,110]`.

The hypotheses are the existing residual reduction's real-point general
position and strict horizontal order, absence of a 6-cap and convex octagon,
and absence of an incoming 6-cup/outgoing 5-cap junction. The owners, their
distinctness and their nonzero triple orientations are extracted from the
configuration in Lean. The public theorem has no external SAT or realizability
assumption.

The proof uses the same shared-order, shared-rank and orientation semantics as
the [first coupled obstruction](../omission-coupled-core-2026-10-10/README.md).
This separate core has 429 Boolean atoms and 520 geometrically justified
clauses. Mathlib's LRAT elaborator translates its 435-step refutation into
ordinary kernel-checked proof terms. The final audit uses only `propext`,
`Classical.choice` and `Quot.sound`; see [axiom-audit.txt](axiom-audit.txt) and
[validation.json](validation.json).

This is a necessary geometric constraint. By itself it does not exclude every
32-hole Boolean assignment, improve the global octagon bound, or improve the
HMPT asymptotic coefficient.

## Reproduction

```sh
lake build ErdosSzekeres.Omission.CoupledSecondObstruction --wfail
python3 scripts/check_omission_coupled_second.py
python3 scripts/export_omission_coupled_second.py --output /tmp/CoreSecond.lean
```

The exporter reproduces the maintained source byte-for-byte. The independent
standard-library checker replays the complete RUP proof and all thirteen
single-state deletion witnesses. These witnesses show minimality under deleting
one selected state in this necessary-condition model, not realizability by
real points or global minimum support size. Discovery inputs, source snapshots,
the original sixteen-state search and the final thirteen-state core are
preserved alongside their hashes. Compiled objects remain ignored.

The underlying state catalogs and adapted prerequisites come from Michael
Schroeder's version-1 archive, 19 September 2026,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
The original data remain CC BY 4.0; see [THIRD_PARTY.md](../../docs/THIRD_PARTY.md)
for the code licenses and Baek prerequisites. This obstruction is a local
addition, with no literature priority claim.

## Strictness and related rows

[Strictness.lean](Strictness.lean) proves
`CoupledCoreSecond.strict_strengthening`: the exact Boolean witness in
[SecondResidualCountermodel.lean](SecondResidualCountermodel.lean) has 32 holes
and satisfies all 1,187 original rows, all 45 earlier geometric rows and all
42 first-template rows, but violates this second core's row.
`CoupledCoreSecond.countermodel_not_realizable` proves that this missing-state
set cannot come from an actual configuration with the residual hypotheses.

`CoupledSecondVariants.all_rows`, in
[CoupledSecondVariants.lean](../../ErdosSzekeres/Omission/CoupledSecondVariants.lean),
certifies 35 supports using the same refutation and 190 finite compatibility
checks per support. They share 20 supports with the first family of 42, giving
**57 distinct necessary constraints** in the two families. This does not claim
that every row is independent of the others or improve a global numerical bound.
See [template-validation.json](template-validation.json) and
[template-axiom-audit.txt](template-axiom-audit.txt).

The compatibility checks use named maps and a Boolean list checker whose
soundness is proved in Lean. The entire second family checked in about 144
seconds under the compiler's `-M1200` option; all public audit roots use only
the three standard axioms listed above.

An exact finite arithmetic review distinguishes distinct supports from new
information. Of these 57 rows, **48 already follow from an original catalog
row**. For the remaining nine, complement-of-support witnesses satisfy all
1,187 original rows, all 45 earlier rows and every other row in this union,
but violate the selected row. Both parts of this classification are now kernel-checked by
`CoupledUnion.independent_each_selected_row` and `redundant_rows_implied`;
see the [union proof bundle](../omission-coupled-union-2026-10-10/README.md).
Its witnesses have 141 holes; the two separate core strictness theorems above
use 32-hole witnesses. The classification concerns this frozen 57-row union;
later constraints can change independence of earlier rows. The exact scope is
also recorded in the `finite_redundancy_review` field of the template validation.

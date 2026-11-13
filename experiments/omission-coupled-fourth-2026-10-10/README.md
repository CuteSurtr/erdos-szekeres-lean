# A fourth coupled geometric obstruction

The fourth selected support is

`[1,4,7,8,11,12,14,16,17,20,23,25,43]`.

The theorem, `CoupledCoreFourth.hole_bound` in
[CoupledFourthObstruction.lean](../../ErdosSzekeres/Omission/CoupledFourthObstruction.lean),
states that every actual residual configuration omits at least one selected
state. The core and actual-residual theorem passed `lake build --wfail`
with only `propext`, `Classical.choice` and `Quot.sound`; see
[axiom-audit.txt](axiom-audit.txt). The hypotheses are the existing real-point general position and
strict horizontal order, no 6-cap, no convex octagon, and no incoming
6-cup/outgoing 5-cap junction.

The direct CNF uses the shared-owner chronology, incoming ranks, orientation
packets and convex-four criterion from the first three cores. Its refutation
has been reduced to 425 atoms, 544 justified clauses and 477 RUP steps. The
standard-library checker independently replays every RUP step and all thirteen
single-state deletion assignments. The latter satisfy the full necessary model,
including every eight-subset check; they are not realizations by real points.
All proof obligations are discharged in Lean from actual residual owners;
no external solver or realizability assumption is added to the theorem.

## Separation and scope

The selected states are all occupied in the saved
[32-hole witness](separated-32-hole-witness.json). Independent exact integer
replay confirms that witness satisfies all 2,397 prior rows, including the
57 distinct prior coupled supports, but violates this new row.
The source hash and the complete check result are in
[validation.json](validation.json). This witness separation is currently a
Python diagnostic, not a Lean strictness theorem.

The initial fourteen-state support included state 0. Deletion minimization
removed that state, and each remaining one-state deletion was SAT. This proves
minimality under single deletions only in the necessary-condition model;
it does not prove minimum support size. The initial and final SMT inputs,
discovery source snapshots, exact CNF/LRAT proof and deletion witnesses are
preserved here. The retained source code is discovery material, not trusted
proof infrastructure.

```sh
python3 scripts/check_omission_coupled_fourth.py
python3 scripts/export_omission_coupled_fourth.py --output /tmp/CoreFourth.lean
lake build ErdosSzekeres.Omission.CoupledFourthObstruction --wfail
```

The exporter reproduces the maintained Lean source byte-for-byte. This local
constraint alone gives no new global octagon bound or asymptotic coefficient.

The underlying state catalogs and adapted prerequisites come from Michael
Schroeder's version-1 archive, 19 September 2026,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
The original data remain CC BY 4.0; see [THIRD_PARTY.md](../../docs/THIRD_PARTY.md)
for the code licenses and Baek prerequisites. This local addition makes no
literature priority claim. Build objects remain ignored.

## Reusing the proof on related supports

`CoupledFourthVariants.all_rows` in
[CoupledFourthVariants.lean](../../ErdosSzekeres/Omission/CoupledFourthVariants.lean)
certifies 24 literal supports through the same refutation. Each passes 173
state-dependent compatibility checks in Lean. One support is the original
fourth core; another replaces state 20 by state 30 and excludes a subsequent
32-hole candidate. No second SAT refutation is needed for those variants.

Against the frozen 2,400-row snapshot, 23 variants have exact Boolean
complement-of-support separating witnesses. That selection diagnostic is not
a Lean independence theorem and imposes no 32-hole cardinality restriction.
See [template-validation.json](template-validation.json) for the precise scope.

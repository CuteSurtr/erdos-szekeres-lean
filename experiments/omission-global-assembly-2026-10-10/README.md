# Parameterized global assembly

**The closed bound `ES(8) ≤ 316` is Lean-checked.**
[`FinalCover316.lean`](FinalCover316.lean) proves
`ErdosSzekeres.Omission.forces_convex_octagon_316 : ForcesConvexNGon 316 8`.
Equivalently, every finite set of at least 316 points in `ℝ²` in general
position contains eight points in convex position. No arithmetic-certificate,
population-bound, rational-coordinate, or realizability hypothesis remains.

The [complete final record](global-cover-316-check.json) verifies both
compressed arithmetic roots, both cut-transfer proofs, all geometric rows,
both catalog identifications, and the final theorem. The
[axiom output](global-cover-316-axioms.txt) reports only `propext`,
`Classical.choice`, and `Quot.sound` for each final root. This is an ordinary
convex octagon result, not an empty-octagon result or an asymptotic improvement.
No priority claim for the finite bound is made here.

The older `Final317.lean` source uses a different, unfinished arithmetic
route; it is not needed by the checked rounded-cover proof. The earlier 317
cover proof remains checked and preserved. Stronger 315 and 314 candidates
below remain pending their own complete final checks.

## Checked statements

The maintained module
[`PopulationBounds.lean`](../../ErdosSzekeres/Omission/PopulationBounds.lean)
proves `Partition.asymmetric_of_bounds`,
`Partition.forces_of_population_bounds`, and
`Partition.avoiding_card_le_of_population_bounds`: balanced bound `B` and
residual bound `R`, with `1 ≤ B + R`, give an avoiding-set bound `B + R + 1`
and forcing threshold `B + R + 2`. All points are ordinary real points in
general position. The partition and projective transfer are fully proved.

[`ResidualBudgets.lean`](ResidualBudgets.lean) proves
`OmissionResidual.residual_bound_of_hole_budget`: exclusion of Boolean hole
vectors of total at most `budget`, subject to all 1,187 rows, gives the
actual residual population bound `153 - budget`.
`forces_318_of_twenty_nine_holes` and `forces_317_of_thirty_holes` are
conditional specializations with the balanced bound 192. The arithmetic
exclusions remain explicit arguments.

The [conditional check record](conditional-check.json) binds the checked
sources, prerequisite sources, compiled objects, and toolchain. The
[axiom audit](conditional-axioms.txt) covers all ten new bridge theorems and
reports only `propext`, `Classical.choice`, and `Quot.sound`.

The [cover preliminary check](cover-preliminary-check.json) additionally
records successful checks of `BalancedBudgets.lean`, `ResidualCoverBridge.lean`,
and `BalancedCoverBridge.lean`. The corresponding
[axiom output](cover-preliminary-axioms.txt) contains no nonstandard axioms.
Its scope is explicitly preliminary: it does not claim a closed global bound.
The complete 85-module balanced row family is preserved as
[source archive](balanced-rows-sources.tar.gz),
[export manifest](balanced-rows-export.json), and
[kernel record](balanced-rows-kernel-check.json).

## Reproduce the conditional check

After building the maintained library and the two completed residual geometry
families, run from the repository root:

```sh
lake env python3 scripts/check_omission_global.py \
  --conditional-only --output .cache/omission-global-assembly \
  --residual-arithmetic .cache/omission-lean-full/residual \
  --residual-cycles .cache/omission-residual-geometry \
  --residual-blocks .cache/omission-residual-blocks
```

On this Mac, replace `lake` by
`ELAN_HOME="$PWD/.elan" .elan/bin/lake`.

## Original arithmetic route (not required by the checked result)

`Final317.lean` composes the unconditional balanced geometry theorem and the
residual arithmetic root into
`ErdosSzekeres.Omission.forces_convex_octagon_317`.
Its second statement, `convex_octagon_of_card_ge_317`, exposes the conclusion
as an eight-element subset with `ConvexIndependent` over `ℝ`, retaining only
the general-position and cardinality hypotheses on the original point set.

When both arithmetic families and the linked balanced geometry are complete,
run the same command without `--conditional-only`, adding:

```sh
  --balanced-arithmetic .cache/omission-balanced-linked \
  --balanced-geometry .cache/omission-balanced-geometry-linked
```

The checker refuses incomplete families, altered sources or objects,
nonstandard axiom reports, mismatched import dependencies, and wrong
arithmetic targets. It compiles only new assembly objects in the isolated
output directory; existing prerequisites are read-only. The final report
must have `complete: true` before this alternative route is reported as checked.

## Smaller fallback certificate

`residual-29.json.gz` contains the original 7,315-leaf 29-hole residual tree,
unchanged apart from the wrapper identifying its source hash. Its separate
export uses namespace `OmissionResidual124` and module prefix `Residual124`,
so it can coexist with the stronger residual family. The packing bases differ;
`Residual124Bridge.lean` checks equality of all 1,187 supports and demands
before transferring the arithmetic exclusion to the existing real geometry.
Both `catalog_matches` and `exclusion_transfer` have passed Lean with only
standard axioms. The original tree data retain the source archive's CC BY 4.0
attribution; they are not newly generated research results.

To reproduce the original arithmetic export and start its check:

```sh
python3 scripts/omission_lean_export.py \
  /path/to/es7_es8_bounds_81_319_v1/certificates/residual.json \
  experiments/omission-global-assembly-2026-10-10/residual-29.json.gz \
  --output .cache/omission-residual124-linked \
  --namespace OmissionResidual124 --module-prefix Residual124 --leaf-limit 64

lake env python3 scripts/check_omission_lean.py \
  .cache/omission-residual124-linked --resume --workers 1 --memory 2500
```

After that separate root is complete, `Final318.lean` supplies the fallback
assembly. Use a separate output directory and add `--bound 318` and
`--residual124-arithmetic .cache/omission-residual124-linked` to the full
assembly command. Threshold 318 does not require the stronger 30-hole root,
but it still requires the completed balanced 192 bound and every geometric
row. No closed 318 theorem is claimed until that assembly passes.

The finite row catalog and geometric reduction are attributed to Michael
Schroeder's version-1 archive, DOI
[10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891), as detailed
in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md). This assembly changes the
population bookkeeping; it does not change the scope of that geometric
reduction or claim priority for a finite numerical bound.

The balanced row archive preserves the same attributed state/cycle data
under CC BY 4.0 and contains 85 generated Lean source files only. The adapted
geometric library retains Schroeder's MIT notice and Baek's Apache-2.0 notice
as described in `THIRD_PARTY.md`. All archives are source/data bundles; compiled
objects remain outside Git. The local `manifest.json` records every packaged
file hash and distinguishes the checked 316 and 317 chains from historical
and pending alternatives. Absolute paths in check records identify the observed build;
their object hashes are evidence, not bundled binaries or portable resume records.

## Compressed arithmetic routes: checked 317 and 316

The six-hour continuation found exact certificates with 4,686 residual leaves
and 711 balanced leaves for 317, followed by 3,954 balanced leaves for 316,
after adjoining 402 and 220 rounded arithmetic rows, respectively. Both
cut-transfer modules are proved from the original catalogs. Python replay
alone does not establish the real-point theorem.

`scripts/omission_balanced_rows.py` copies all 84 balanced geometry blocks
unchanged and makes `BalancedRows.lean` aggregate their 2,685 row implications.
This 85-module family imports the original `BalancedProof.Catalog` without
requiring its old arithmetic root. `BalancedBudgets.lean` then transfers any
proved hole-budget exclusion to the actual balanced population bound.

`ResidualCoverBridge.lean` and `BalancedCoverBridge.lean` check both pieces of
each extended catalog: every original row and every derived cut. Only then do
they transfer the compressed root's exclusion back to the original catalogs
used by geometry. `FinalCover317.lean` assembles the two population estimates.

After every compressed arithmetic, cut-transfer, and geometric family passes,
run:

```sh
lake env python3 scripts/check_omission_global.py \
  --output .cache/omission-global-cover-317 \
  --residual-arithmetic .cache/omission-lean-full/residual \
  --residual-cycles .cache/omission-residual-geometry \
  --residual-blocks .cache/omission-residual-blocks \
  --balanced-arithmetic .cache/omission-balanced-linked \
  --balanced-geometry .cache/omission-balanced-rows-only \
  --residual-cover-arithmetic .cache/omission-residual-cover-linked \
  --residual-cover-cuts .cache/omission-cover-transfer-residual \
  --balanced-cover-arithmetic .cache/omission-balanced-cover-linked \
  --balanced-cover-cuts .cache/omission-cover-transfer-balanced
```

The original arithmetic directories supply their already-checked literal
catalogs in this command. Their old full roots are not prerequisites of this
route. Both new compressed roots, both cut-transfer modules, all geometry,
both catalog equalities, and the closed global statement still are.

The same 220-cut balanced catalog has a complete Lean-checked 3,954-leaf
certificate for hole budget 60 (92 parts, catalog and root). The complete
316 assembly and audit are preserved at the top of this document. To
reproduce it, use
`--bound 316 --balanced-cover-budget 60` and change the balanced compressed
arithmetic directory to `.cache/omission-balanced-cover60-linked`.
The selected sources become `BalancedCover60Bridge.lean` and
`FinalCover316.lean`, giving checked populations 191 and 123.

The older prospective `ResidualCover31Bridge.lean` and `FinalCover315.lean`
refer to the 402-cut residual catalog. No completed residual31 certificate
on that catalog is available; those sources must not be combined with the
new 1,108-cut residual catalog.

## Versioned stronger candidates

The balanced61 candidate has 22,112 exact leaves on a new 446-cut catalog.
`BalancedCover61Bridge.lean` identifies its 3,131 rows with the original
2,685 geometric rows and `BalancedCoverCutsV2`'s 446 arithmetic consequences.
`FinalCover315B61R30.lean` would combine its population 190 with the existing
residual population 123. These stronger sources are prepared, not yet checked.

The separate `scripts/check_omission_global_profile.py` pins the precise
arithmetic and cut-transfer manifest hashes in
`profile-balanced61-v2-residual30-v1.json`. This keeps the original 317 gate
unchanged and prevents catalog versions with different row counts from being
substituted. It retains all source, object, dependency, toolchain, complete-root,
catalog-equality, and axiom checks. To check this candidate, use the compressed
command above with the new script, replace its balanced arithmetic directory
by `.cache/omission-balanced-cover61-linked`, replace its balanced cut directory
by `.cache/omission-cover-transfer-balanced-v2`, choose a separate output, and
add `--profile experiments/omission-global-assembly-2026-10-10/profile-balanced61-v2-residual30-v1.json`.

The checker enforces the exact threshold identity
`406 - balancedBudget - residualBudget`. Preparing a profile or replaying a
tree in Python does not establish a stronger global bound.

## Fused leaf proofs: checked optimization, pending production tree

`scripts/omission_fused_export.py` is a separately versioned exporter. Its
generic helper composes the same packed-column and strict-margin lemmas as the
original exporter. A single conjunction retains all five arithmetic checks;
the change removes the intermediate per-leaf load theorem and its repeated
type checking. The helper is embedded in each new catalog, so the normal
catalog/part/root checker still binds every proof source and dependency.
The original exporter and all completed 317 inputs remain unchanged.

The [benchmark and kernel controls](fused-packing-benchmark.json) record a
same-host comparison of the same 47-leaf part: 132.120 seconds for the original
proofs and 81.154 seconds for the fused proofs (128.066 versus 79.149 seconds of
user CPU). Both conclude the same theorem with only standard axioms. Changing
one packed coefficient from 951 to 952 made Lean reject the proof. A complete
tiny tree and a second corrupted-leaf control also passed the exporter tests.
This is a bounded throughput measurement, not a guaranteed whole-build speedup.

The selected production candidate additionally uses a smaller-weight tree with
22,318 leaves and packing base 524,288. Its frozen export is
`OmissionBalancedCover61Fused` / `BalancedCover61FusedProof`, with 502 parts and
the same 3,131 rows and 446-cut transfer. The profile
`profile-balanced61-fused-v2-residual30-v1.json` pins its exact identities;
`BalancedCover61FusedBridge.lean` and `FinalCover315B61FusedR30.lean` prepare the
315 assembly. This candidate remains pending its complete production tree and
final proof checks. The checked 316 and 317 results remain separately preserved.

## Bounded direct-CNF experiment

A [direct residual31 CNF attempt](direct-residual31-cnf-attempt.json) encoded
the frozen 2,295-row system without a Z3 translation. Its auxiliary variables
have explicit prefix-cardinality meanings. Small exhaustive controls checked
both directions, and the known 32-hole witness satisfied the same encoding at
budget 32. These are implementation controls, not a Lean encoding theorem.

The budget31 CaDiCaL run returned no SAT or UNSAT conclusion within its bound.
It was stopped after 582.997 seconds at 498,330,365 bytes of partial LRAT
(2,110,180 lines). Thus this run did not provide a compact alternative to the
weighted certificates. The large trace, CNF and literal metadata remain in
ignored cache; the preserved record contains their hashes and the bounded
outcome. No semantic Lean transfer or LRAT formalization was started.

The selected residual31 fused certificate has 50,945 exact leaves in 1,216
parts, packing base 262,144, and the 2,295-row catalog containing 1,108 derived
cuts. Its frozen namespace and prefix are `OmissionResidualCover31Fused` and
`ResidualCover31FusedProof`. Exact Python replay completed; its full Lean
arithmetic root is pending. The 1,108-cut transfer is already kernel checked.
`ResidualCover31FusedBridge.lean` prepares the exact catalog bridge.
`FinalCover315B60R31Fused.lean` and `FinalCover314B61FusedR31Fused.lean` prepare
the corresponding compositions. The profiles
`profile-balanced60-v1-residual31-fused-v2.json` and
`profile-balanced61-fused-v2-residual31-fused-v2.json` now pin their exact frozen
manifest identities. None of these pending assemblies establishes a stronger
bound until its full arithmetic roots and final Lean theorem pass.

## Bounded part-conjunction prototype

A [later bounded probe](part-conjunction-attempt.json) combined all fused leaf
checks in a proof part into one conjunction. The 47-leaf version failed
decidable-instance synthesis after 122.783 seconds, so it yielded no checked
full-part proof. A four-leaf control passed in 11.879 seconds with standard
axioms; changing 951 to 952 in one packed coefficient was correctly rejected.
The earlier individual fused proofs took 81.154 seconds for the same 47 leaves
and 8.566 seconds for the same four leaves. These historical comparisons have
different concurrent load and memory settings; they establish no speedup.
The experiment was stopped, and all production exporters and sources remain
unchanged.

# A third coupled core and a two-hole constraint

The third thirteen-state support is

`[16,30,39,43,50,53,62,65,68,77,89,91,101]`.

Its direct propositional encoding has a refutation reduced to 515 atoms,
578 geometrically justified clauses and 465 RUP steps. The independent
standard-library checker replays the complete refutation and all thirteen
single-state deletion witnesses. The third core and its actual-residual theorem passed Lean kernel checking
with only `propext`, `Classical.choice` and `Quot.sound`. The final two-hole assembly also passed `lake build --wfail`.

The public theorem is `CoupledCoreThird.hole_bound` in
[CoupledThirdObstruction.lean](../../ErdosSzekeres/Omission/CoupledThirdObstruction.lean).
It uses the same residual hypotheses as the first two cores: a configuration
of real points in general position and strict horizontal order, no 6-cap,
no convex octagon, and no incoming 6-cup/outgoing 5-cap junction. The owners and
all orientation assumptions are extracted from that configuration by
the same checked semantic bridge. No solver result is accepted as an axiom.

## The fourteen-state support

Adding state 25 gives

`[16,25,30,39,43,50,53,62,65,68,77,89,91,101]`.

Every one-state deletion is forbidden in an actual residual configuration
by the checked third core and existing rows. The deletion of 25 is the new core. The other
thirteen deletion exclusions follow from two already checked original cycle
rows and first-template row 24. This proves that
at least two states in the fourteen-state set are absent. The original rows
used are catalog row 136, the eight-cycle
`[16,30,39,50,62,89,68,25]`, and catalog row 984, the nine-cycle
`[25,43,53,65,77,89,110,101,91]`.

The exact coverage is preserved in [discovery-results.json](discovery-results.json).
The closed theorem is `CoupledDemandTwo.hole_bound` in
[CoupledDemandTwo.lean](../../ErdosSzekeres/Omission/CoupledDemandTwo.lean),
using the finite argument in
[TwoHoleAssembly.lean](../../ErdosSzekeres/Omission/TwoHoleAssembly.lean). Neither a new
global octagon bound nor an improved asymptotic coefficient follows from this
local result alone.

## Discovery and replay

The first candidate, obtained by adding nearby state 89 to the first checked
core, needed only one new deletion test. That test was UNSAT in about 1.8
seconds. Greedy deletion found all thirteen twelve-state subsets SAT; every
assignment passed all shared-rank, chronological packet and fixed-sign
constraints and an exhaustive test of all eight-subsets. These are models of
necessary conditions, not realizations by points in the real plane.

A complete backtracking compatibility check found no assignment of the new
support to either earlier template. A fresh direct CNF was therefore produced
and refuted by CaDiCaL. The source snapshots, full inputs, refutation and all
deletions are preserved here; `discovery-sources.json.gz` also records source
hashes. Only finite exact replay and Lean proof terms are relevant to proof
validity; the solver and the discovery scripts are untrusted.

```sh
python3 scripts/check_omission_coupled_third.py
python3 scripts/export_omission_coupled_third.py --output /tmp/CoreThird.lean
lake build ErdosSzekeres.Omission.CoupledThirdObstruction --wfail
```

[finite-strictness-diagnostic.json](finite-strictness-diagnostic.json) records
an independent Python diagnostic: occupying exactly the third core's states
and omitting the other 141 satisfies all 2,397 current rows, including the
57 distinct prior coupled supports. It violates both new rows. This
is an independence check without a 32-hole restriction; it is not a Lean
independence theorem or a geometric realization.

The underlying state catalogs and adapted prerequisites come from Michael
Schroeder's version-1 archive, 19 September 2026,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
The original data remain CC BY 4.0; see [THIRD_PARTY.md](../../docs/THIRD_PARTY.md)
for the code licenses and Baek prerequisites. This local addition makes no
literature priority claim. Build objects remain ignored.

The thirteen-state row and its fourteen-state demand-two formulation encode
the same additional obstruction given the earlier premises. They should not
be counted as two independent geometric discoveries.

## Three checked variants

`CoupledThirdVariants.all_rows` certifies three further thirteen-state
supports by reusing this refutation. Each passes 195 finite compatibility
checks in Lean. They were selected from eight candidate maps by a finite
separation diagnostic against the frozen 2,400-row snapshot. This selection
is not a Lean independence theorem and does not change the numerical bound.
See [template-validation.json](template-validation.json) and
[template-axiom-audit.txt](template-axiom-audit.txt).

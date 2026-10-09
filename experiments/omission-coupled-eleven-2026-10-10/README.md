# Eleven-state coupled geometric obstruction

The ordinary Lean theorem `ErdosSzekeres.Omission.CoupledCoreEleven.hole_bound`
in [CoupledElevenObstruction.lean](../../ErdosSzekeres/Omission/CoupledElevenObstruction.lean)
proves that every residual configuration omits at least one of

`[67, 77, 79, 96, 105, 114, 123, 130, 133, 137, 138]`.

The hypotheses are real planar points in general position, strictly ordered by
x-coordinate, with no 6-cap, no convex octagon, and no incoming-6-cup/outgoing-5-cap
junction. The projective partition proves these restrictions for its residual
part; this local theorem alone gives no improved total population bound.

The proof extracts eleven distinct owners from one ambient configuration. Its
452 propositional atoms share their order, actual pair ranks and orientations.
Every one of 615 retained clauses follows from proved geometric facts. Mathlib's
LRAT builder constructs a kernel-checked refutation with 501 RUP steps.
`context_impossible`, `exists_missing_state` and `hole_bound` use only standard
Lean axioms. No solver verdict, proof placeholder, or native-evaluation axiom
is assumed. The ordinary Lake build passed with warnings treated as errors.

The preserved 33-hole Boolean witness satisfies all 2,455 earlier constraints
and fully occupies this eleven-state set. Its exact integer replay proves a
strict strengthening of that Boolean model as a computational diagnostic;
that independence statement is not a Lean theorem or a point realization.
Deleting any one of the eleven states gives a satisfiable necessary model:
all eleven complete deletion assignments were independently replayed. Minimality
is relative to this frozen necessary model, not to every possible geometric fact.

Reproduce the supplemental exact checks with:

```sh
python3 scripts/check_omission_coupled_eleven.py
python3 scripts/export_omission_coupled_sized.py \
  --source experiments/omission-coupled-eleven-2026-10-10/core11.json \
  --output ErdosSzekeres/Omission/CoupledCoreEleven.lean \
  --namespace CoupledCoreEleven \
  --artifact omission-coupled-eleven-2026-10-10 --stem core11
lake build ErdosSzekeres.Omission.CoupledElevenObstruction --wfail
```

Discovery files retain the status and hashes recorded before formalization.
The current proof status is in `validation.json` and its saved axiom audit.
State profiles and original omission rows derive from Michael Schroeder's
[version-1 release](https://doi.org/10.5281/zenodo.22842891), attributed under
CC BY 4.0. CaDiCaL was an untrusted certificate producer; Mathlib's LRAT code
builds ordinary proof terms. No literature-priority claim is made.

# Nine-state coupled geometric obstruction

The ordinary Lean theorem `ErdosSzekeres.Omission.CoupledCoreNine.hole_bound`
in [CoupledNineObstruction.lean](../../ErdosSzekeres/Omission/CoupledNineObstruction.lean)
proves that every residual configuration omits at least one of

`[33, 43, 64, 68, 75, 87, 91, 99, 118]`.

The hypotheses are real planar points in general position, strictly ordered by
x-coordinate, with no 6-cap, no convex octagon, and no incoming-6-cup/outgoing-5-cap
junction. The projective partition proves these restrictions for its residual
part; this local theorem alone gives no improved total population bound.

The proof extracts nine distinct owners from one ambient configuration. Its
243 propositional atoms share their order, actual pair ranks and orientations.
Every one of 280 retained clauses follows from proved geometric facts. Mathlib's
LRAT builder constructs a kernel-checked refutation with 215 RUP steps.
`context_impossible`, `exists_missing_state` and `hole_bound` use only standard
Lean axioms. No solver verdict, proof placeholder, or native-evaluation axiom
is assumed. The ordinary Lake build passed with warnings treated as errors.

The preserved 33-hole Boolean witness satisfies all 2,456 earlier constraints
and fully occupies this nine-state set. Its exact integer replay proves a
strict strengthening of that Boolean model as a computational diagnostic;
that independence statement is not a Lean theorem or a point realization.
Deleting any one of the nine states gives a satisfiable necessary model:
all nine complete deletion assignments were independently replayed. Minimality
is relative to this frozen necessary model, not to every possible geometric fact.

Reproduce the supplemental exact checks with:

```sh
python3 scripts/check_omission_coupled_nine.py
python3 scripts/export_omission_coupled_sized.py \
  --source experiments/omission-coupled-nine-2026-10-10/core9.json \
  --output ErdosSzekeres/Omission/CoupledCoreNine.lean \
  --namespace CoupledCoreNine \
  --artifact omission-coupled-nine-2026-10-10 --stem core9
lake build ErdosSzekeres.Omission.CoupledNineObstruction --wfail
```

Discovery files retain the status and hashes recorded before formalization.
The current proof status is in `validation.json` and its saved axiom audit.
State profiles and original omission rows derive from Michael Schroeder's
[version-1 release](https://doi.org/10.5281/zenodo.22842891), attributed under
CC BY 4.0. CaDiCaL was an untrusted certificate producer; Mathlib's LRAT code
builds ordinary proof terms. No literature-priority claim is made.

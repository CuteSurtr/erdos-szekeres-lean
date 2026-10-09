# A coupled geometric obstruction on thirteen residual states

The maintained theorem `ErdosSzekeres.Omission.CoupledCore13.hole_bound`, in
[CoupledObstruction.lean](../../ErdosSzekeres/Omission/CoupledObstruction.lean),
proves that every actual residual configuration omits at least one state from

`[16,25,30,39,43,50,53,62,65,68,77,91,101]`.

The hypotheses are real points in general position and strict horizontal order,
no 6-cap, no convex octagon, and the same no incoming 6-cup/outgoing 5-cap junction
used by the completed partition. These conditions are inherited from the
existing residual reduction. Distinct owners and their orientation nondegeneracy
are extracted in the proof, not assumed from an external encoding.

[Strictness.lean](Strictness.lean) proves `strict_strengthening`: one explicit
Boolean 32-hole assignment satisfies all 1,187 original rows and all 45 previously
added geometric rows but violates this new row. The same file proves
`countermodel_not_realizable`. This establishes a strict necessary geometric
constraint. It does not exclude every 32-hole assignment or improve the global
numerical bound by itself.

## What the finite proof checks

All selected owners share one chronological order, one pair of actual attained
ranks for each unordered pair, and one orientation sign for each triple.
[CoupledSemantics.lean](../../ErdosSzekeres/Omission/CoupledSemantics.lean) proves
necessity of the eight clause families: directed state domains, order
transitivity, rank growth, forced signs, four-point orientation packets,
quadrilateral convexity, empty directions, and octagon exclusions.

The literal core has 389 Boolean atoms and 407 clauses. Its 343-step LRAT
refutation is translated into ordinary proof terms using Mathlib's existing
`FromLRAT` machinery. The thin wrapper in
[CoupledLrat.lean](../../ErdosSzekeres/Omission/CoupledLrat.lean) adds those terms
as declarations checked by Lean's kernel. It does not declare an axiom or use
native evaluation to prove a proposition. The exact source formula is identified
with all 407 geometrically justified clauses inside Lean.

The final geometric theorems and the strictness theorem use only `propext`,
`Classical.choice` and `Quot.sound`. Their unabridged reports and source hashes
are in [axiom-audit.txt](axiom-audit.txt) and [validation.json](validation.json).

## Reproduction and limits

After the main library dependencies are available:

```sh
lake build ErdosSzekeres.Omission.CoupledObstruction --wfail
python3 scripts/check_omission_coupled_core.py
python3 scripts/export_omission_coupled_core.py --output /tmp/Core13.lean
```

The exporter reproduces the maintained core source byte-for-byte. Its JSON and
external solver are untrusted proof-discovery inputs. The standard-library
checker independently replays all 343 derivation steps and all 13 single-point
deletion assignments. The deletion tests establish minimality under deleting
one of these selected states within the necessary-condition model; they do
not establish real-point realizability or global minimum support size.

For the separate strictness file, first reproduce the checked residual catalog
and `ResidualCountermodel.lean` as described in the adjacent
[cover artifact](../omission-cover-certificates-2026-10-10/README.md), and include
their generated object directories in `LEAN_PATH`. The exact dependencies are
recorded in validation.json. Compiled objects remain ignored.

The state IDs and catalog geometry are adaptations of Michael Schroeder's
version-1 archive, 19 September 2026,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
The original data remain CC BY 4.0; adapted geometric code and the separate Baek
prerequisites retain their attributed licenses in
[THIRD_PARTY.md](../../docs/THIRD_PARTY.md). This coupled constraint and its proof
are local additions. No literature priority claim is made.

# A fifth coupled geometric obstruction

The selected support is

`[16,25,30,43,50,53,62,68,77,79,91,101,110]`.

The theorem `CoupledCoreFifth.hole_bound`, in
[CoupledFifthObstruction.lean](../../ErdosSzekeres/Omission/CoupledFifthObstruction.lean),
states that every actual residual configuration omits at least one selected
state. Its Lean kernel check passed with only `propext`, `Classical.choice` and
`Quot.sound`; see [axiom-audit.txt](axiom-audit.txt). It uses the standard hypotheses:
real points in general position and strict horizontal order, no 6-cap,
no convex octagon, and no incoming 6-cup/outgoing 5-cap junction.

The direct propositional proof has 383 atoms, 425 justified clauses and
339 RUP steps. Every RUP step and all thirteen one-state deletion assignments
have passed independent exact replay. Earlier SAT assignments were restricted
to the final twelve-state deletions before replay; each restricted assignment
was checked on every eight-subset. These satisfy a necessary-condition model
and do not establish realizability by real points.

## Provenance and scope

The support is fully occupied in the saved
[32-hole witness](separated-32-hole-witness.json), which passed all 2,400 rows
of its frozen source. That source includes the first 57 distinct coupled rows,
the third core and its two-hole formulation, and the fourth core. A complete
finite compatibility search found no assignment of this support to any of
those four core templates. A separate candidate from the same research stage
was covered by the fourth template and is not counted as a fifth core here.

The literal proof therefore uses a fresh direct CNF and refutation. Its Lean
necessity bridge uses exactly the same already checked clause-family lemmas;
no additional solver or realizability assumption is introduced. This row
alone does not improve a total residual population, the global octagon bound,
or an asymptotic coefficient. The witness separation is an exact Python
diagnostic until separately checked in Lean.

```sh
python3 scripts/check_omission_coupled_fifth.py
python3 scripts/export_omission_coupled_fifth.py --output /tmp/CoreFifth.lean
lake build ErdosSzekeres.Omission.CoupledFifthObstruction --wfail
```

The frozen source snapshots, initial sixteen-state and final thirteen-state
SMT inputs, direct proof and deletion witnesses are preserved here. Discovery
code and solvers are untrusted; the final theorem depends on ordinary Lean
proof terms. Minimality is only under one selected-state deletion in the
necessary-condition model, not minimum support size over all possibilities.

The underlying state catalogs and adapted prerequisites come from Michael
Schroeder's version-1 archive, 19 September 2026,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
The original data remain CC BY 4.0; see [THIRD_PARTY.md](../../docs/THIRD_PARTY.md)
for the code licenses and Baek prerequisites. This local addition makes no
literature priority claim. Build objects remain ignored.

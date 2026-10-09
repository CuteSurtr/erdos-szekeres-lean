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

# Finite octagon status and remaining work

**10 October 2026: ES(8) ≤ 317 is proved. No geometric transfer or arithmetic
obligation remains for that theorem.** The former estimate of 40–60 hours for
the old residual proof tree is superseded by a compressed, completely checked
certificate route.

The closed results are `ErdosSzekeres.Omission.forces_convex_octagon_317` and
`convex_octagon_of_card_ge_317`, in
[FinalCover317.lean](../experiments/omission-global-assembly-2026-10-10/FinalCover317.lean).
The [complete check record](../experiments/omission-global-assembly-2026-10-10/global-cover-317-check.json)
binds all dependencies and contains successful final axiom reports. It uses
only the three standard Lean axioms. Its scope is arbitrary finite real planar
point sets in general position, with no emptiness requirement for the polygon.

## What closed the geometric transfer

The projective chart removes one point and excludes 7-caps. The minimum-slope
partition gives balanced and residual induced configurations with all needed
avoidance and junction conditions. Actual attained ranks inject those points
into the 252- and 154-state catalogs. All 2,685 balanced and 1,187 residual
constraints are proved for those assignments, including the Baek block bound
and its supporting-line transfer to convex real polygons.

The checked arithmetic exclusions rule out at most 59 balanced holes and at
most 30 residual holes, giving populations at most 192 and 123. Thus an
avoiding original set has at most `192 + 123 + 1 = 316` points. The next integer
317 is the forcing threshold. No abstract-model realizability assumption is
used in that implication.

## Stronger research targets, not completed bounds

| Target | Required work | Unknowns and rough size |
| --- | --- | --- |
| 316 | Finish the stronger balanced 60-hole exclusion and final composition with the completed residual 30-hole exclusion. | A complete exact 3,954-leaf tree exists; its Lean build is in progress. No new geometric theorem is required. Roughly hours of certificate checking on this machine, subject to kernel resource limits. |
| 315 | Finish the balanced 61-hole exclusion, its larger cut transfer and final composition with residual 30. | A complete exact 22,112-leaf tree exists. Hundreds of proof parts remain to check; several hours to a day at current observed rates, with compression being explored. This is a planning range, not a promise. |
| 314 | Also finish a residual 31-hole exclusion and the matching catalog interfaces. | Complete exact trees exist but have tens of thousands of leaves. Compression and full Lean checking dominate the work; roughly a day or more for the current trees. |
| Stronger geometric constraints | Connect a checked 13-state propositional obstruction to the actual residual point assignment and all finite clause instances. | General semantic lemmas compile, but the full finite transfer is not yet checked. Likely hundreds of lines plus generated finite proof data; its effect on global certificate size or bounds is still unknown. |

A Lean-checked 32-hole abstract witness satisfies all 1,187 original residual
rows and all 45 separately added geometric rows. It shows a limitation of that
finite model. It does not provide a real 122-point residual configuration or
an Erdős–Szekeres lower bound.

The source method and comparison remain Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891). No currently-best-bound
or priority claim is made. These finite targets do not improve HMPT's asymptotic
coefficient.

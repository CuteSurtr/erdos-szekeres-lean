# Finite octagon status and remaining work

**10 October 2026: ES(8) ≤ 315 is proved. No geometric transfer or arithmetic
obligation remains for that theorem.** The former estimate of 40–60 hours for
the old residual proof tree is superseded by a compressed, completely checked
certificate route.

The closed results are `ErdosSzekeres.Omission.forces_convex_octagon_315` and
`convex_octagon_of_card_ge_315`, in
[FinalCover315B61FusedR30.lean](../experiments/omission-global-assembly-2026-10-10/FinalCover315B61FusedR30.lean).
The [complete check record](../experiments/omission-global-assembly-2026-10-10/global-cover-315-check.json)
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

The checked arithmetic exclusions rule out at most 61 balanced holes and at
most 30 residual holes, giving populations at most 190 and 123. Thus an
avoiding original set has at most `190 + 123 + 1 = 314` points. The next integer
315 is the forcing threshold. No abstract-model realizability assumption is
used in that implication.

## Stronger research targets, not completed bounds

| Target | Required work | Unknowns and rough size |
| --- | --- | --- |
| 314 | Finish residual31 and its final composition with the completed balanced61 proof. | The residual proof has 50,945 leaves in 1,216 parts; roughly 980 parts were recorded when 315 closed. Its 1,108-cut transfer is complete. At recent rates, the remaining checking is on the order of half an hour with six workers, followed by final linking. Memory pressure and long-tail parts can change that estimate. No new geometric argument is needed. |
| Beyond these targets | Find and prove more necessary constraints or a stronger counting argument. | Five 13-state obstructions and a 14-state demand-two formulation are geometrically proved. The first two families contain 57 distinct valid rows; Lean proves nine independent additions and 48 redundant rows in that frozen system. Three third-template, 24 fourth-template and 28 fifth-template variants are checked, as are newer eleven- and nine-state obstructions. New constraints alone do not establish a better population bound. There is no reliable estimate for a new global improvement. |

A Lean-checked 32-hole abstract witness satisfies all 1,187 original residual
rows and all 45 earlier additions. Later exact integer searches found further
32-hole witnesses satisfying the 57 coupled rows and still newer constraints.
These expose limitations of the respective Boolean models; they do not provide
real 122-point residual configurations or Erdős–Szekeres lower bounds.

The source method and comparison remain Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891). No currently-best-bound
or priority claim is made. These finite targets do not improve HMPT's asymptotic
coefficient.

# Finite octagon status and remaining work

**10 October 2026: ES(8) ≤ 316 is proved. No geometric transfer or arithmetic
obligation remains for that theorem.** The former estimate of 40–60 hours for
the old residual proof tree is superseded by a compressed, completely checked
certificate route.

The closed results are `ErdosSzekeres.Omission.forces_convex_octagon_316` and
`convex_octagon_of_card_ge_316`, in
[FinalCover316.lean](../experiments/omission-global-assembly-2026-10-10/FinalCover316.lean).
The [complete check record](../experiments/omission-global-assembly-2026-10-10/global-cover-316-check.json)
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

The checked arithmetic exclusions rule out at most 60 balanced holes and at
most 30 residual holes, giving populations at most 191 and 123. Thus an
avoiding original set has at most `191 + 123 + 1 = 315` points. The next integer
316 is the forcing threshold. No abstract-model realizability assumption is
used in that implication.

## Stronger research targets, not completed bounds

| Target | Required work | Unknowns and rough size |
| --- | --- | --- |
| 315 | Finish either balanced61 with residual30, or balanced60 with residual31, and their final composition. | The balanced61 fused proof has 22,318 leaves in 502 parts. Its 446-cut transfer is complete. Several hours of kernel checking remain at this checkpoint; no new geometric argument is required. |
| 314 | Finish both balanced61 and residual31 and their matching final composition. | The residual31 fused proof has 50,945 leaves in 1,216 parts. Its 1,108-cut transfer is complete. At observed first-block rates, the remaining arithmetic is on the order of a few hours with several workers; long-tail blocks, memory pressure and final linking can change that estimate. |
| Beyond these targets | Find and prove more necessary constraints or a stronger counting argument. | Five 13-state obstructions and a 14-state demand-two formulation are geometrically proved. The first two families contain 57 distinct valid rows; Lean proves nine independent additions and 48 redundant rows in that frozen system. Three third-template and 24 fourth-template variants are also checked. New constraints alone do not establish a better population bound. There is no reliable estimate for a new global improvement. |

A Lean-checked 32-hole abstract witness satisfies all 1,187 original residual
rows and all 45 earlier additions. Later exact integer searches found further
32-hole witnesses satisfying the 57 coupled rows and still newer constraints.
These expose limitations of the respective Boolean models; they do not provide
real 122-point residual configurations or Erdős–Szekeres lower bounds.

The source method and comparison remain Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891). No currently-best-bound
or priority claim is made. These finite targets do not improve HMPT's asymptotic
coefficient.

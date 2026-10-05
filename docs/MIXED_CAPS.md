# A checked obstruction to mixed-cap addition

Research checkpoint: 2026-10-05. This result rejects a candidate strengthening;
it does not improve the Erdős–Szekeres upper bound.

The final [HMPT paper, §3](https://arxiv.org/html/1710.11415v3)
uses two different gluing arguments: neighboring vertical caps and nonadjacent
horizontal inner caps. We tested an additional claim: a vertical cap and an
inner cap in nonadjacent spikes should have a combined size below n whenever
their ambient configuration avoids a convex n-gon.

That claim is false under the geometric hypotheses in our counterexample,
even when the ambient configuration contains every support anchor. The Lean
theorem is `ErdosSzekeres.HMPT.MixedCap.mixed_cap_budget_counterexample`.
The word `LeftCap` below follows this repository's convention: a cap facing
the next spike, with the right edge endpoint adjoined.

## Exact configuration

Use these integer coordinates, interpreted as real points:

| Group | Formula | Index range |
| --- | --- | --- |
| Anchors Aᵢ | (10000i, −100000i²) | 0 ≤ i < 6 |
| Vertical cap Cₜ | (15000+100t, −200000−4900t+t²) | 0 ≤ t < 8 |
| Inner cap Tₜ | (35000+100t, −1200000−7000t−t²) | 0 ≤ t < 8 |

Let P contain all 22 points. The clockwise support sequence determines three
spikes. C lies in frame (A₀,A₁,A₂,A₃), and T in frame (A₂,A₃,A₄,A₅);
their frame indices are 0 and 2, so they are nonadjacent.

Lean proves all of the following:

- P is in general position, has distinct x-coordinates, and has cardinality 22.
- All support frames satisfy the horizontal ordering condition.
- C is an actual `SpikeChain` in the outer-base triangle order, with a `LeftCap 8`.
- T has cardinality 8, lies in its spike, and satisfies both `SpikeAntichain`
  and `InnerCap` from the existing HMPT development.
- Every support anchor and both caps belong to P.
- P contains a convex 15-gon and contains no convex 16-gon.

Thus the two cap sizes sum to 16 although P avoids a convex 16-gon. A witness
for the 15-gon consists of all six anchors, all eight points of T, and C₇.

## Short certificate for the upper bound

There are two families of strict triangle containments:

    Cⱼ ∈ interior triangle(Cᵢ, Cₖ, Tₜ)   for i < j < k,
    Cⱼ ∈ interior triangle(Cᵢ, A₂, Tₜ)   for i < j.

These give 448 and 224 exact integer certificates, respectively. A convex
subset cannot contain a certified interior point together with its enclosing
triangle. Consequently, a convex subset Q of P obeys:

| Case | Cardinality bound |
| --- | --- |
| Q contains no T vertex | 6 anchors + 8 C vertices = 14 |
| Q contains a T vertex and A₂ | At most 1 C vertex, hence at most 6+1+8 = 15 |
| Q contains a T vertex but not A₂ | At most 2 C vertices, hence at most 5+2+8 = 15 |

`IntegerCertificates.lean` proves that the determinant certificates imply
membership in Mathlib's real convex hull, and that such membership obstructs
`ConvexPosition`. It also transfers supporting-edge certificates to real convex
position. `MixedCapData.lean` checks the finite integer predicates using
`decide +kernel`. `MixedCapObstruction.lean` proves the cardinality argument,
and `MixedCapGeometry.lean` connects every hypothesis to the existing geometric
definitions. The final theorem depends only on standard Lean axioms.

The separate Python replay checks all 74,613 sixteen-point subsets with a
convex hull algorithm, checks the 672 interior certificates, and corroborates
the maximum with the existing dynamic program. These calculations are not
dependencies of the Lean theorem.

```sh
python3 scripts/mixed_cap_certificate.py
python3 -m unittest discover -s scripts -v
lake build --wfail
python3 scripts/check_axioms.py
```

The saved replay is `experiments/mixed-cap-obstruction-2026-10-05.json`.

## What this rules out

An unconditional additive constraint on these two cap sizes is unavailable.
Simply including the support anchors does not repair it. The triangle
certificates locate the missing compatibility: the inner cap can put a middle
vertical-chain point inside a triangle formed by the other selected vertices.

This example does not rule out constraints that use further information, such
as orientations between the caps, restrictions on other populated spikes, or
joint extremality conditions. Those hypotheses must be established from the
extraction argument before a stronger counting bound can use them. We have
not established a strict improvement over HMPT's coefficient 8√2/3.

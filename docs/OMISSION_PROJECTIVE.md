# Projective reduction to the asymmetric bound

**Completed, 9 October 2026:** the root-deletion and projective transfer is now
proved for arbitrary finite real point sets in general position. The original
set has no coordinate-order assumption. The finite population hypothesis needed
to obtain ES(8) ≤ 317 remains unproved.

The implementation is
[ProjectiveTransfer.lean](../ErdosSzekeres/Omission/ProjectiveTransfer.lean).
Prepend `ErdosSzekeres.Omission.` to the names below.

| Declaration | Exact role |
| --- | --- |
| `root_cap_polygon` | For any `k ≥ 3`, a `k`-cap in the positive projective chart, together with the retained root, forms a convex `(k+1)`-gon in the original set. Strict ray order and the projected cap signs supply every cyclic orientation. |
| `exists_configuration` | Enumerates a finite real set with distinct x-coordinates as a `Configuration`, retaining every point and the exact cardinality. |
| `Configuration.no_cap_of_projected_image` | An avoided `(k+1)`-gon rules out a `k`-cap in any such chart. |
| `exists_projective_chart` | Projects all points to the right of the root and orders the image. Octagon avoidance implies both octagon and 7-cap avoidance in the chart. |
| `IsRootDeletionChart` | Records the actual invertible linear normalization, retained root, positive-denominator domain, and equality of the configuration's point set with the projected root-deleted set. |
| `exists_cap_free_chart` | Every nonempty octagon-free general-position set has such a chart with exactly one fewer point, no 7-cap, and no convex octagon. |
| `avoiding_card_le_of_asymmetric_bound` | A chart population bound `B` gives at most `B+1` original points in an octagon-free set. |
| `forces_of_asymmetric_bound` | The same hypothesis implies `ForcesConvexNGon (B+2) 8`. |
| `forces_317_of_asymmetric_315` | Specializes the conditional transfer to the target: `AsymmetricBound 315 → ForcesConvexNGon 317 8`. |

`AsymmetricBound B` is a defined proposition:

```lean
∀ n : ℕ, ∀ c : Configuration n,
  ¬ c.HasCap 7 →
  ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B
```

There is **no theorem proving `AsymmetricBound 315` yet**. In particular, a
7-cup is allowed in this remaining obligation. The finished balanced theorem
requires that there be no 7-cup as well, so it cannot be substituted directly.
The [completed partition](OMISSION_PARTITION.md) now proves all the splitting
and avoidance hypotheses needed to combine balanced and residual bounds as
`192 + 123 = 315`. The residual bound remains unproved; after importing the
finished balanced certificate, it is the only remaining population hypothesis.
The two extra points in the global threshold are exactly the deleted root and
the strict forcing threshold.

## Consequence of the completed balanced bound

The separately checked theorem
`OmissionBalanced.large_avoiding_set_has_chart_cup`, in
[BalancedProjective.lean](../experiments/omission-projective-transfer-2026-10-09/BalancedProjective.lean),
shows that every octagon-free general-position set of **at least 194 points**
has an actual root-deletion chart containing a **7-cup**. The chart still has
no 7-cap and no convex octagon. Its explicit relation to the original set is
part of the conclusion through `IsRootDeletionChart`.

Indeed, the chart has at least 193 points; if it also had no 7-cup, the completed
balanced bound of 192 would contradict its size. This is a structural statement
about an octagon-free set, **not** an assertion that 194 points force an octagon.
See the [standalone check record](../experiments/omission-projective-transfer-2026-10-09/README.md).

## Provenance and trust

The root/chart argument follows Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891), particularly
`ES8ProjectiveTransfer` and `ES8Final`. The adaptation is attributed under MIT;
the [copyright and license](SCHROEDER-MIT.txt) are retained. This implementation
uses the already checked `HMPT.projectFrom` lemmas, `Suk.exists_horizontal_image`,
and this project's finite-set polygon predicate. It generalizes the root-cap
lemma to every `k ≥ 3` and exposes the coordinate maps in the chart witness.

The reduction module is in the default library and axiom audit. Its finite
capacity assumptions are explicit theorem parameters, not custom axioms. The
194-point structural consequence additionally imports the large balanced proof
artifact and is checked separately. Neither result establishes a new global
octagon bound or an improvement of HMPT's asymptotic coefficient.

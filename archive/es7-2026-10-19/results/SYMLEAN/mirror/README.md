# SYMLEAN/mirror: the mirror classes proved in Lean, without SAT

1 November 2026 (UTC).

**Statement.** `ReductionThreeClasses.lean` proves two theorems in the namespace `ErdosSzekeres.SymReduction`:
- `heptagon_of_nontrivial_isometry_3`: assume only the classes `HalfTurn34`, `Threefold33` and `Fivefold35` of
  `../SymmetricReduction.lean`. Then every finite set of at least 33 points in general position that a Euclidean
  isometry other than the identity maps into itself contains 7 points in convex position.
- `heptagon_of_nontrivial_affineEquiv_3`: the same for affine bijections other than the identity.

The two mirror classes of `../SymmetricReduction.lean` are now theorems (`mirrorOneAxis33_proved`,
`mirrorNoAxis34_proved`). Their proofs use no SAT certificate.

## 1. The mirror bound

`MirrorOdd.mirror_seven_line` says: a finite set in general position that is invariant under the reflection in any line
and has no 7 points in convex position has at most 32 points. The proof follows the mirror reduction:
- a rigid motion takes the line to the x-axis, and |S| = 2|R| + |A|, where R is the set of points above the axis and A
  the set of points on it (|A| <= 2 by general position);
- a subset T of R together with at most one point of A has distinct x-coordinates and no 4-cap: a 4-cap strictly above
  the axis together with its mirror image is a convex octagon, and a 4-cap with an end point on the axis gives a convex
  heptagon;
- by Baek's theorem with n = 7 (no 4-cap and no convex 7-gon allow at most C(6,2) + 1 = 16 points), |S| <= 32.

The octagon analogue `mirror_eight_line` gives at most 46 points, using n = 8 (22 points).

**Baek's theorem in Lean.** The repository contains a formalization of Baek's theorem in `ErdosSzekeres/Vendor/ETV`
(theorem `main`: a set with no 4-cap of at least C(n+2,2) + 2 points contains a convex (n+3)-gon). The file uses it
at n = 4 (`capacity16`, proved in this file) and through the repository's `Omission.BaekGeometry.geometric_capacity22`
at n = 5.

**Credit.** The bound N_mirror(7) = 32, and with it Theorem 2 of `WRITEUP/SYMMETRIC.md`, is a consequence of Baek's
theorem (J. Baek, Eur. J. Combin. 124 (2025) 104085; arXiv:2206.04260, Theorem 1.6) and the mirror reduction. The SAT
proofs in `SYMZ` and the Lean chain of `WRITEUP/MIRROR.md` are independent confirmations of it.

## 2. The file

`ReductionThreeClasses.lean` (4,322 lines, SHA-256 `0cc83994fe8c2c48…`):
- lines 38–1559 are lines 12–1533 of `../AffineReduction.lean`, unchanged;
- lines 1562–4236 are the mirror development (namespace `MirrorOdd`), unchanged from its reviewed source;
- lines 4237–4322 (Part C) are the connecting lemmas: `reflLine_eq_lineRefl` (the two reflection maps agree),
  `card_le_32_of_reflLine`, the two class proofs and the two `_3` theorems; the first lines are the union of the
  imports.

`axioms.out` is the `#print axioms` output.

## 3. Checks

- Compiled from the repository root with `lake env lean --threads=1` (Lean 4.24.0, Mathlib `f897ebcf`): exit 0,
  121 linter warnings (unused simp arguments), no errors, about 106 s and 3.75 GB.
- Every new theorem, and `MirrorOdd.mirror_seven_line`, depends only on `[propext, Classical.choice, Quot.sound]`.
  The file contains no `sorry`, `admit` or `native_decide`.
- An independent review recompiled the file, listed the binders of the two `_3` theorems (only `HalfTurn34`,
  `Threefold33` and `Fivefold35` appear), checked that both source parts are byte-identical to their originals,
  and confirmed the reflection maps agree (a Lean lemma and an exact polynomial check).
- A separate review of the mirror development on its own re-sent the 497 repository constants its theorems depend on
  to the Lean kernel (all accepted, no axioms).
- The imported repository modules (`Definitions`, `Basic`, `ConvexCycleCuts`, `Omission/Baek`,
  `Omission/BaekGeometry`, `Omission/BoundaryGeometry`, `Omission/ListGeometry` and `Vendor/ETV`) are identical on
  this branch and on `main`.

## 4. Scope

`HalfTurn34`, `Threefold33` and `Fivefold35` remain hypotheses. They rest on the computer-assisted certificates
(`C2FINAL` with `C2C34`, `C3FINAL` with `C3LEAN`, `SYM5`) and on the written soundness proofs of their encoders.

## Reproduction

```sh
lake env lean --threads=1 cloud/es7-2026-10-19/results/SYMLEAN/mirror/ReductionThreeClasses.lean
```

Run from the repository root; it needs the repository's built library and its Mathlib.

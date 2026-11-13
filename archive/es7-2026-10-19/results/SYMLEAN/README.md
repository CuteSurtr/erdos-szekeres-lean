# SYMLEAN: Lean check of the symmetry reduction behind Corollary 3

Local work on an Apple M5 Pro, 1 November 2026 (UTC).

**Statement (the implication is Lean-checked).** Assume five case classes, stated in Lean as propositions:
`HalfTurn34`, `Threefold33`, `Fivefold35`, `MirrorOneAxis33` and `MirrorNoAxis34` (§2). Then every finite set of at
least 33 points in general position that is mapped into itself by a Euclidean isometry other than the identity
contains 7 points in convex position. The same holds with an affine bijection in place of the isometry (§4).

**Status.**
- In the files of §1 only the implication is Lean-checked: Lean 4.24.0, Mathlib `f897ebcf`, axioms `propext`,
  `Classical.choice` and `Quot.sound`, no `sorry`.
- The classes are hypotheses of the theorems, not axioms, and none is proved in the files of §1. They rest on SAT
  certificates and on written soundness proofs of the encoders (§5). `MirrorOneAxis33` is also equivalent to a
  statement that H3 and V2-L derive in Lean from CNF facts (§5).
- The two mirror classes are proved in Lean, without SAT input, in `SYMLEAN/mirror` (`mirrorOneAxis33_proved`,
  `mirrorNoAxis34_proved`). They follow from Baek's theorem (J. Baek, Eur. J. Combin. 124 (2025) 104085;
  arXiv:2206.04260) by the mirror reduction. That directory restates the main theorem and its affine version with
  only `HalfTurn34`, `Threefold33` and `Fivefold35` as hypotheses.
- The central 34-point statement, the class `HalfTurn34`, is claimed in `C2FINAL` (computer-assisted), with the
  composition check, the random re-solve sample and the re-checks of 1–2 November 2026 (totals in `C2RECHECK`). The
  unconditional forms of §2 and §4 are then computer-assisted: they rest on the certificates of `HalfTurn34`,
  `Threefold33` and `Fivefold35` and on the written proofs listed with them in §5. The implication and the two mirror
  classes are Lean-checked; the other three classes are not.
- The variant `halfTurn_of_symmetric_counterexample` (§3) does not use `HalfTurn34`. It uses the fourfold class
  `Fourfold32` (`C4CUT`). It concludes that every symmetry other than the identity of a heptagon-free set of at least
  33 points in general position is a half-turn about a point outside the set, and that the set then has an even
  number of points, at least 34.
- A review of the definitions (§6) found that each class states what its certificate proves. It also proved in Lean
  that no class is vacuous.

## 1. Files

| file | lines | SHA-256 | content |
|---|---:|---|---|
| `SymmetricReduction.lean` | 1,059 | `6d5ec90a…` | the classes, the main theorem (§2), the variant (§3) |
| `SymmetricReductionAxioms.lean` | 1,062 | `7bf809cb…` | the same, with two `#print axioms` lines appended |
| `AffineReduction.lean` | 1,533 | `41cfc0b6…` | lines 1–1,058 of `SymmetricReduction.lean`, then the affine version (§4) |
| `AffineReductionAxioms.lean` | 1,544 | `f6cb9372…` | the same, with `#print axioms` and `#check` lines appended |
| `review/ReviewSanity.lean` | 1,657 | `ec251368…` | lines 1–1,059 of `SymmetricReduction.lean`, then 71 review theorems and 8 definitions (§6) |
| `review/VariantChecks.lean` | 1,306 | `4b823bb6…` | lines 1–1,059 of `SymmetricReduction.lean`, then three checks of the variant (§3) |
| `review/SupMetric.lean` | 159 | `7c634244…` | the sup-metric check (§6.4) |
| `logs/` | | | compiler output of each file, and `runs.tsv` (§8) |

- `lake env lean` imports only modules that are already built, not a sibling file, so the later files repeat the main
  file. The shared lines are byte-identical (see Reproduction).
- The `review` files come from the reviews. In `ReviewSanity.lean` one comment sentence (two lines) was changed to
  name the file in this directory. `VariantChecks.lean` collects a selection of checks from two separate reviews, and
  `SupMetric.lean` is the check of a third. In both, names, namespaces and comments were changed (in
  `VariantChecks.lean` also the `open` lines); the statements and proofs were not.

## 2. The main theorem

```lean
theorem heptagon_of_nontrivial_isometry
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point → Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hg : IsEucIsometry g) (hne : g ≠ id) (hinv : Invariant g S) : HasConvexNGon 7 S
```

**Definitions.**
- `Point`, `GeneralPosition` and `HasConvexNGon` are the repository's (`ErdosSzekeres/Definitions.lean` at the
  repository root). General position: no three distinct points are collinear. `HasConvexNGon 7 S`: some 7 points
  of S are in convex position (Mathlib `ConvexIndependent`).
- `eDist2 p q = (p₀ − q₀)² + (p₁ − q₁)²`. `IsEucIsometry g`: g preserves `eDist2`. `Invariant g S`: g maps S into S.

**The classes.** Each one is quantified over every set S in general position of the given size and every centre c
(every line through a with unit direction u). Each concludes `HasConvexNGon 7 S`.

| class | size | symmetry | further hypothesis |
|---|---:|---|---|
| `HalfTurn34` | 34 | `halfTurn c`: p ↦ 2c − p | c ∉ S |
| `Threefold33` | 33 | `rotAbout c (2π/3)` | c ∉ S |
| `Fivefold35` | 35 | `rotAbout c (2π/5)` | c ∉ S |
| `MirrorOneAxis33` | 33 | `reflLine a u`, u₀² + u₁² = 1 | exactly one point of S on the mirror |
| `MirrorNoAxis34` | 34 | `reflLine a u`, u₀² + u₁² = 1 | no point of S on the mirror |
| `Fourfold32` (§3 only) | 32 | `rotAbout c (2π/4)` | c ∉ S |

`rotAbout c θ` is the rotation by θ about c, written with cos and sin. `reflLine` is `Mir.reflLine` of
`H3/MirrorEncoding/Line.lean`, copied verbatim.

**Proof outline.**
1. In complex coordinates an isometry is z ↦ az + b or z ↦ a·z̄ + b with |a| = 1. This comes from Mathlib
   (`Isometry.affineIsometryOfStrictConvexSpace`, `linear_isometry_complex`).
2. S is finite, so the iterates of a point repeat. This excludes translations and glide reflections. For z ↦ az + b,
   a is then a root of unity and g is the rotation about b/(1 − a). For z ↦ a·z̄ + b, g is a `reflLine`
   (`isometry_structure`).
3. Rotation of even order (orders 4 and 6 included): a power of g is the half-turn. By general position its centre is
   not in S, so |S| is even and at least 34. Keep 17 orbits; `HalfTurn34` applies.
4. Rotation of odd order: a power of g has prime order p, the smallest prime factor. For p = 3 or 5, remove the centre
   if it is in S. At least 32 points remain, in orbits of p points, so at least 33 or 35. Keep 11 or 7 whole orbits
   (`orbit_select`). For p ≥ 7, one orbit is a regular p-gon, which is in convex position
   (`convexPosition_of_concyclic`).
5. Reflection: by general position at most two points lie on the mirror. With none, keep 17 pairs
   (`MirrorNoAxis34`). Otherwise keep 16 pairs and one mirror point (`MirrorOneAxis33`).

## 3. The variant without `HalfTurn34`

```lean
theorem halfTurn_of_symmetric_counterexample
    (h3 : Threefold33) (h4 : Fourfold32) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point → Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hg : IsEucIsometry g) (hne : g ≠ id) (hinv : Invariant g S) (hno : ¬ HasConvexNGon 7 S) :
    ∃ c : Point, g = halfTurn c ∧ c ∉ S ∧ 2 ∣ S.card ∧ 34 ≤ S.card
```

- This is the Euclidean part of Corollary 3 of `WRITEUP/SYMMETRIC.md`, which assumes the fourfold exclusion instead
  of a central class.
- Orders with an odd prime factor go as in step 4 of §2. Powers of 2 from 4 on go to `Fourfold32` (keep 8 orbits).
  Order 2 is the conclusion.
- The file calls this theorem "Corollary 3 exactly as written". Two reviews found that too strong. The file is left
  unchanged so that its hash stays valid.
  - Corollary 3 says the symmetry group is exactly C2, while the theorem speaks of one symmetry at a time. The group
    form follows because two half-turns about different centres compose to a nonzero translation, which the theorem
    excludes. `review/VariantChecks.lean` proves it (`group_form`).
  - The affine sentence of Corollary 3 is formalized for the main theorem (§4), not for this variant.
- `VariantChecks.lean` also restates the variant with every definition of `SymmetricReduction.lean` written out as
  coordinate formulas, and derives the restatement from the theorem (`variant_unfolded`).
- A 36-point fourfold class is enough here. A fourfold set in general position avoids its centre, so its size is a
  multiple of 4, and 33 points force 36. `VariantChecks.lean` proves `Fourfold32 → Fourfold36` and the variant with
  `Fourfold36` (`variant_with_fourfold36`). The 32-point strength of `C4CUT` is still what gives N(C4) = 28, that is,
  the largest fourfold-symmetric set without a convex 7-gon has 28 points (`C4CUT` §5).
- The main theorem needs no fourfold class, because `HalfTurn34` covers every even order.

## 4. Affine symmetries (`AffineReduction.lean`)

```lean
theorem heptagon_of_nontrivial_affineEquiv
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point ≃ᵃ[ℝ] Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hne : g ≠ AffineEquiv.refl ℝ Point) (hinv : Invariant g S) : HasConvexNGon 7 S
```

Variants with the same five hypotheses:
- `heptagon_of_nontrivial_affineEquiv_image`: invariance written as g '' S ⊆ S;
- `heptagon_of_nontrivial_affineMap`: an injective Mathlib affine map;
- `heptagon_of_nontrivial_affine`: p ↦ Lp + b, injective;
- `heptagon_of_nontrivial_affine_coords`: (x, y) ↦ (ax + by + e, cx + dy + f) with ad − bc ≠ 0.

**The route** (`hasConvexNGon_of_affine_symmetry`, for any N ≥ 3 and any n):
1. g permutes S, so three non-collinear points of S have a common period m ≥ 1. Then L^m = 1.
2. The averaged form q(z) = Σ_{k<m} |L^k z|² is L-invariant and positive definite.
3. With its explicit Cholesky factor T, h = T ∘ g ∘ T⁻¹ preserves `eDist2`. T keeps general position (orientations
   scale by det T > 0) and the number of points.
4. The Euclidean theorem gives a convex 7-gon in T(S), and T⁻¹ carries it back to S.

## 5. The classes and their certificates

| class | certificate | how it is certified | caveat |
|---|---|---|---|
| `HalfTurn34` | `C2C34` (encoder, hull cover, 120 hexagonal hulls), `C2P`–`C2P5` (parallelogram subcases), `C2FINAL` (composition) | hull cover, second-layer covers and each closed piece: certificate accepted by both checkers; encoder, and reductions A and B: written proofs (reviewed, `C2C34` §5 and `C2P/review`); composition: exact computation, its bookkeeping Lean-checked | claimed in `C2FINAL` (computer-assisted), with the random re-solve sample and the re-checks of 1–2 November 2026 (totals in `C2RECHECK`). The original proofs of the parallelogram pieces were deleted after both checks, so most of these pieces rest on recorded verdicts |
| `Threefold33` | `C3FINAL`, with the normal form `C3-S/soundness.md` and the encoding `C3a` | 116,883 pieces, each certificate accepted by both checkers when solved; composition: exact computation (two composers); normal form and encoding: written proofs (reviewed, `C3AUDIT`–`C3AUDIT4`) | the proofs were not retained; 2,120 random pieces were re-solved and accepted again (`C3SPOT`) |
| `Fivefold35` | `SYM5` | two encodings, each certificate accepted by both checkers, proofs P1 and L1 retained; encoders and layer lemma: written proofs (reviewed) | |
| `MirrorOneAxis33` | `SYMZ`, Theorem 2a | certificate accepted by both checkers, proof retained; encoder: written proof (reviewed) | |
| | `H3` and `V2-L`: `Mir.MirrorExclusionLine` | Lean-checked, with 1 + 121 + 1,198 + 74,000 CNF facts as hypotheses, each with a recorded cake_lpr verdict (`WRITEUP/MIRROR.md`) | the proof files were not retained (`WRITEUP/CERTIFICATES.md`) |
| | `SYMLEAN/mirror`: `mirrorOneAxis33_proved` | Lean-checked, no SAT input: Baek's theorem (formalized in the repository, `ErdosSzekeres/Vendor/ETV`) and the mirror reduction | |
| `MirrorNoAxis34` | `SYMZ`, Theorem 2b | certificate accepted by both checkers, proof retained; encoder: written proof (reviewed in two audits) | |
| | `SYMLEAN/mirror`: `mirrorNoAxis34_proved` | Lean-checked, no SAT input, as for `MirrorOneAxis33` | |
| `Fourfold32` (§3 only) | `C4CUT` | final certificate accepted by both checkers; six cuts: exact computation (independent verifier); encoder: written proof (reviewed, `C4CUT/review`) | the review found no blocking or major finding (`C4CUT/review/README.md`) |

**Credit.** The statement of `Fourfold32` is from Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224v1, §6.2);
`C4CUT` adds a checkable certificate. The fivefold upper bound is implied by an earlier reported computation of
B. C. Dumitru (arXiv:2512.24061, §7), which has priority; `SYM5` records the overlap. The two mirror classes are
implied by Baek's theorem (J. Baek, Eur. J. Combin. 124 (2025) 104085; arXiv:2206.04260, Theorem 1.6 in the arXiv
numbering) through the mirror reduction (`SYMLEAN/mirror`, `MIRRORETV`). The certificates of `SYMZ` confirm both
independently, and the H3 chain, conditional on its CNF facts, confirms `MirrorOneAxis33`. The Lean proof in
`SYMLEAN/mirror` uses the repository's formalization of Baek's theorem, adapted from Baek's Lean 4 code, and bridge
lemmas adapted from M. Schroeder's archive (`docs/THIRD_PARTY.md` at the repository root).

**The bridge to H3.** `MirrorExclusionLineCopy` in the Lean file is the text of `Mir.MirrorExclusionLine`
(`H3/MirrorEncoding/Line.lean`), over the same `reflLine`.
- `mirrorOneAxis33_of_exclusionLine` proves `MirrorExclusionLineCopy → MirrorOneAxis33`.
- `review/ReviewSanity.lean` proves the converse, hence `mirrorOneAxis33_iff_exclusionLine`. For 33 points in
  general position, "exactly one point on the mirror" is automatic.
- A separate check built H3 from its sources and proved `Mir.reflLine = reflLine` and
  `Mir.MirrorExclusionLine = MirrorExclusionLineCopy` by `rfl`. Three mutated statements were rejected. That file
  is not in this directory.
- The docstring of `MirrorExclusionLineCopy` says "Lean-verified there from CNF facts". It should be read as:
  Lean-checked, conditional on those CNF facts.

## 6. Review of the definitions

An independent review read the six class definitions against the statements their certificates prove. Its Lean
lemmas are in `review/ReviewSanity.lean`. Lines 1–1,059 are the main file byte for byte, so the lemmas are about the
definitions used there; 71 theorems and 8 auxiliary definitions follow.

**Verdict: all six classes match their certificates.** No class is stronger than its certificate, and none is
vacuous. For `Threefold33` and `Fivefold35` the match uses a written proof by perturbation (§6.5, item 3). The match
itself was checked by reading: no formal link joins a Lean class to its CNF.

### 6.1 The maps (Lean-checked)

- `rotAbout c θ`, `halfTurn c` and `reflLine a u` (with |u| = 1) preserve `eDist2`, and `halfTurn c = rotAbout c π`.
- The rotations by 2π/3, 2π/4 and 2π/5 have exact orders 3, 4 and 5. Explicit forms: cos(2π/3) = −1/2 and
  sin(2π/3) = √3/2; the quarter turn is p ↦ c + J(p − c) with J(x, y) = (−y, x).
- `reflLine a u` is an involution, fixes exactly the points of the line a + ℝu, and is not the identity.
- `orient c p (rotAbout c θ p) = sin θ · eDist2 p c`, so an angle in (0, π) turns counter-clockwise, as the encoders
  assume.
- Not Lean-checked (written argument): an injective map that sends a finite set into itself permutes it, so
  invariance under R is the same as invariance under R⁻¹, and the classes do not depend on this convention.

### 6.2 Non-vacuity (Lean-checked)

- The hypotheses of the main theorem hold for 33 points on the parabola y = x² (x = −16, …, 16) with the mirror
  x ↦ −x, and for the regular 33-gon with the rotation by 2π/3.
- The hypotheses of each class hold: the regular 34-, 33-, 35- and 32-gon for the rotation classes; 33 parabola
  points (one on the mirror) and 34 parabola points (x = ±1, …, ±17, none on the mirror) for the mirror classes.
- The repository notions are not trivial. Three collinear points are not in general position, and a point inside a
  triangle gives four points with no convex quadrilateral. Convex position implies general position. General
  position survives a shear, which is not a Euclidean isometry.
- By their definitions (Mathlib `Collinear` and `ConvexIndependent`), these notions use only the affine structure.
- A fully qualified `#print` shows that every class refers to `ErdosSzekeres.Point`,
  `ErdosSzekeres.GeneralPosition` and `ErdosSzekeres.HasConvexNGon` (`logs/ReviewSanity.out`).

### 6.3 Redundant hypotheses

- `c ∉ S` follows from general position in `HalfTurn34` and `Fourfold32`: the centre would be collinear with an
  antipodal pair (for the fourfold class, the square of the rotation is the half-turn). This is Lean-checked in the
  main file (`center_not_mem_of_halfTurn`, used in `case_fourfold`). In `Threefold33` and `Fivefold35` it follows
  from the size (written argument): 32 is not a multiple of 3, and 34 is not a multiple of 5.
- "Exactly one point on the mirror" in `MirrorOneAxis33` follows from |S| = 33 and general position (Lean-checked,
  §5).
- Such hypotheses make a class easier to prove. They never make it stronger than its certificate.

### 6.4 The sup metric (Lean-checked, `review/SupMetric.lean`)

- The file repeats the five definitions it uses (`eDist2`, `IsEucIsometry`, `rotAbout`, `halfTurn`, `reflLine`)
  verbatim from `SymmetricReduction.lean` instead of importing it.
- `Point = Fin 2 → ℝ` carries Mathlib's sup metric: `dist ![0,0] ![3,4] = 4`, not 5.
- So a hypothesis written as Mathlib `Isometry g` would silently drop cases. For every centre, the rotations by 2π/3
  and 2π/5 are not `Isometry`s of `Point`. Neither is the reflection in the line through the origin with direction
  (3/5, 4/5). The half-turn and the quarter turn are.
- The theorems therefore use the explicit `eDist2`, and these rotations do satisfy `IsEucIsometry`. By their
  definitions, general position and convex position are affine notions and do not involve the metric (§6.2).
- The header of the main file adds that a sup isometry of the plane is a symmetry of the square followed by a
  translation. That remark is not Lean-checked.

### 6.5 Findings about status and documents (all minor)

1. When the review ran, `HalfTurn34` was not yet claimed; it is now claimed in `C2FINAL` (§5). The main theorem uses
   it for every rotation of even order. The variant avoids it. The Lean file itself calls the classes hypotheses and
   does not overclaim.
2. When the review ran, the documents disagreed on `Fourfold32`. `C4CUT/README.md` said its review was pending,
   while `C4CUT/review/README.md` reports no blocking or major finding. `SYM5/README.md` §4 and `WRITEUP/SYMMETRIC.md`
   cited the arXiv:2506.00224 enumeration.
3. `Threefold33` and `Fivefold35` include sets whose centre lies on a line through two points of different orbits.
   The encoders exclude such sets. A perturbation argument closes the gap (written proof, reviewed): it is explicit
   in `SYM5` §1 and one sentence in `C3a/README.md`, `C3b/DERIVATION.md` and `C3-S/soundness.md`. For the other
   classes, general position alone forces the degenerate triples that the encoders use.
4. Two wordings in the main file are too strong: "Corollary 3 exactly as written" (§3) and the docstring about H3
   (§5).

## 7. Further checks of the main file

A second round of checks reviewed nine of the ten claims made about `SymmetricReduction.lean`, each one separately
and with its own scripts. None found an error in the implication. Apart from the files in `review/`, their files are
not in this directory. The tenth claim, a floating-point check that the map formulas send the project's example sets
onto themselves (computational evidence), was not checked again.
- **Build.** The file compiled with exit 0 and no messages. Four checks rebuilt the imported repository modules from
  the sources at 471d5f63a (one of them together with H and H3, §5) and compiled the file against them. One of them
  re-sent all 114 compiled constants (95 theorems, 19 definitions, auxiliaries included) to the kernel. All were
  accepted, and a mismatched proof was rejected.
- **Statements.** The main theorem and the variant were restated with explicit coordinate formulas outside the
  file's namespace and derived from the theorems. The variant's restatement is kept (`variant_unfolded`, §3).
- **Isometry structure.** Proved again in Lean by a different route, without Mathlib's isometry theorems.
- **Concyclic points.** Proved again in Lean with a half-plane argument. Exact rational tests on 400 random
  concyclic sets gave 0 failures (computational evidence).
- **Orbit selection.** An exhaustive test over all self-maps of sets with at most 6 elements, 688,369 instances, gave
  0 failures (exact computation). The lemma's injectivity hypothesis is redundant.
- **H3 bridge** (§5) and **sup metric** (§6.4).
- **Corrections.** "Exactly as written" overstates the variant (§3). A remark that `C4CUT` is "needed only for the
  variant" was refuted as worded: `C4CUT` also gives N(C4) = 28, and the variant needs only a 36-point fourfold class
  (§3).

## 8. Compilation (`logs/`)

All seven files were compiled again on 1 November 2026 (UTC), one at a time, with `lake env lean <file>` from the
repository root (Lean 4.24.0, Mathlib `f897ebcf`). The Mac was also running SAT jobs, so wall times vary.

| file | exit | output | wall s | max RSS GB |
|---|---:|---|---:|---:|
| `SymmetricReduction.lean` | 0 | none | 12.5 | 2.17 |
| `SymmetricReductionAxioms.lean` | 0 | axioms of the two theorems | 5.3 | 2.22 |
| `AffineReduction.lean` | 0 | none | 4.8 | 2.21 |
| `AffineReductionAxioms.lean` | 0 | axioms of 9 theorems, one `#check` | 11.2 | 2.22 |
| `review/ReviewSanity.lean` | 0 | one linter warning (unused `simp` argument), axioms of 12 theorems, 7 `#print`, 2 `#check` | 24.2 | 2.18 |
| `review/VariantChecks.lean` | 0 | one `ring` fallback message (`ring_nf` closes the goal), one linter warning, axioms of 4 theorems | 17.6 | 2.16 |
| `review/SupMetric.lean` | 0 | axioms of 10 theorems | 16.0 | 1.91 |

- Every `#print axioms` line reads `[propext, Classical.choice, Quot.sound]`. No log contains an error or `sorryAx`.
- For `SymmetricReductionAxioms`, `AffineReduction`, `AffineReductionAxioms` and `ReviewSanity` the output equals the
  output recorded by the reviews, up to file paths. For `SupMetric` it equals its source's output up to the namespace
  name.
- The max RSS is mostly memory-mapped Mathlib files. The reviews measured a private footprint of at most 0.47 GB.
- The imported repository modules (`Definitions`, `Basic`, `Orientation`, `OrientationGeometry`, `Suk/TriangleOrder`,
  `Suk/BaseChart`, `Suk/BaseOrder`, `Suk/SupportingLines`) are byte-identical in the checkout used and on
  `es7-cloud` at 471d5f63a.
- Paths in the logs are relative to `cloud/es7-2026-10-19/results`. `logs/runs.tsv` adds start times and CPU times.
- `review/VariantChecks.lean` was compiled once more in the review of this directory, with the same output (14.9 s,
  2.24 GB).

## 9. What is not checked

- `HalfTurn34`, `Threefold33`, `Fivefold35` and `Fourfold32` are not proved in Lean. Each rests on SAT certificates and
  on a written soundness proof of its encoder. The two mirror classes are proved in Lean from Baek's theorem, without
  SAT input (`SYMLEAN/mirror`); `MirrorOneAxis33` also has a Lean chain through H3, conditional on CNF facts.
- `HalfTurn34` is claimed in `C2FINAL` (computer-assisted). The unconditional forms of §2 and §4 rest on it and on
  the certificates of `Threefold33` and `Fivefold35`, so they are computer-assisted and not Lean-checked as a whole.
- Some proofs were deleted after both checkers accepted them, so only recorded verdicts remain: the 116,883 pieces of
  `Threefold33` (2,120 re-solved, `C3SPOT`) and the parallelogram pieces of `HalfTurn34` (samples re-solved, `C2FINAL`
  §4–§5). The proof files of the H3 chain were not retained either; `SYMZ` gives `MirrorOneAxis33` a retained
  certificate.
- The SAT solver is not trusted; the checkers lrat-check and cake_lpr are (`WRITEUP/SYMMETRIC.md` §3).
- The symmetry must be a map of the whole plane: a Euclidean isometry or an affine bijection. A distance-preserving
  permutation of S alone is not treated.
- The affine version of the variant is not formalized.
- Trusted: the Lean kernel, Mathlib at `f897ebcf`, and the repository definitions `Point`, `GeneralPosition`,
  `ConvexPosition` and `HasConvexNGon`. That each class states what its certificate proves rests on the review of §6,
  which compared them by reading.

## Reproduction

From `cloud/es7-2026-10-19/results` (bash):

```bash
shasum -a 256 SYMLEAN/*.lean SYMLEAN/review/*.lean
diff <(head -n 1058 SYMLEAN/AffineReduction.lean) <(head -n 1058 SYMLEAN/SymmetricReduction.lean)
for f in ReviewSanity VariantChecks; do head -n 1059 SYMLEAN/review/$f.lean | cmp - SYMLEAN/SymmetricReduction.lean; done
cd ../../..    # the repository root, with its pinned Lean 4.24.0 and Mathlib f897ebcf
lake exe cache get    # prebuilt Mathlib files, if they are not there yet
lake build +ErdosSzekeres.Basic +ErdosSzekeres.OrientationGeometry +ErdosSzekeres.Suk.SupportingLines
R=cloud/es7-2026-10-19/results/SYMLEAN
lake env lean $R/SymmetricReduction.lean           # no output
lake env lean $R/SymmetricReductionAxioms.lean     # compare logs/SymmetricReductionAxioms.out
lake env lean $R/AffineReduction.lean              # no output
lake env lean $R/AffineReductionAxioms.lean        # compare logs/AffineReductionAxioms.out
lake env lean $R/review/ReviewSanity.lean          # compare logs/ReviewSanity.out
lake env lean $R/review/VariantChecks.lean         # compare logs/VariantChecks.out
lake env lean $R/review/SupMetric.lean             # compare logs/SupMetric.out
```

Each Lean run took about 5 to 25 s and about 2.2 GB of resident memory.

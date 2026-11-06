import ES8Geo.ModelOfLabelling

/-! # M6/M8: the sixfold case of `ES(8) = 65` from the encoder-B verdicts

* `sixfold66_of_no_model`: if no `EncB.Model 6 8 11` exists, `Sixfold66` holds. A 66-point sixfold
  counterexample has a polar labelling (M5, `labelling_of_counterexample`), whose intended model
  (M6, `modelOfLabelling`) is a `Model 6 8 11`.
* `sixfold66_of_unsat`, `sixfold66_of_cubes64`: the same from the unsatisfiability of `encB 6 8 11`
  (M3, `encB_satisfiable_6811`), resp. of its 64 cubes (H3, `encB_unsat_of_cubesUnsat64`).
* `sixfold_es8`, `sixfold_es8_of_texts`: every set of at least 61 points in general position that is
  invariant under the counterclockwise rotation by `2π/6` about some point has a convex octagon
  (`sixfold_octagon`), given `CubesUnsat64`, resp. given the meaning of cake_lpr's 64 verdicts on the
  64 printed texts (trust item E3; the hypothesis of `EncB.no_model_6811_of_texts`, copied verbatim).
* `sixfold_es8_order6`, `sixfold_es8_order6_of_texts`: the same for a rotation of order 6 in either
  direction, i.e. by `2π/6` or by `2π·5/6` (`= -(2π/6)` mod `2π`, `rotAbout_neg_sixth`): invariance
  under `ρ⁵` gives invariance under `ρ⁵⁵ = ρ` (`invariant_sixth_of_five`).

The formula `encB 6 8 11` (2.4M clauses) is only ever named, never evaluated. Every declaration below
that mentions the instance (or `Model 6 8 11`, `CubesUnsat64`, ...) is a term with no tactic block;
the numeral side conditions (`3 ≤ 6`, `Even 6`, ...) and the angle arithmetic are separate lemmas in
`EncB.Geo.MainAux` that never mention it (cf. EncB/Satisfiable.lean:43; checked by
scripts/audit_geo.sh, check 5). -/

namespace EncB.Geo
open ErdosSzekeres ErdosSzekeres.LayerLemma

namespace MainAux

/-- The numeral side conditions of the (6,8,11) instance (`m = 6`, `K = 8`, `t = 11`, `66 = m·t`). -/
theorem numerals : 3 ≤ 6 ∧ 2 ≤ 6 ∧ Even 6 ∧ 4 ≤ 8 ∧ 8 ≤ 2 * 6 ∧ 66 = 6 * 11 :=
  ⟨by norm_num, by norm_num, by decide, by norm_num, by norm_num, by norm_num⟩

/-- `Sixfold66` writes the angle with the real numeral `6`; M5/M6 take `((6 : ℕ) : ℝ)`. -/
theorem invariant_cast_six {T : Finset Point} {c : Point}
    (h : Invariant (rotAbout c (2 * Real.pi / 6)) T) :
    Invariant (rotAbout c (2 * Real.pi / ((6 : ℕ) : ℝ))) T := by
  exact_mod_cast h

/-- `rotAbout` is `2π`-periodic in the angle. -/
theorem rotAbout_add_nat_mul_two_pi (c : Point) (θ : ℝ) (n : ℕ) :
    rotAbout c (θ + n * (2 * Real.pi)) = rotAbout c θ := by
  funext p
  simp only [rotAbout, Real.cos_add_nat_mul_two_pi, Real.sin_add_nat_mul_two_pi]

end MainAux

open MainAux in
/-- The rotation by `2π·5/6` is the clockwise rotation by `2π/6`. -/
theorem rotAbout_neg_sixth (c : Point) :
    rotAbout c (-(2 * Real.pi / 6)) = rotAbout c (2 * Real.pi * 5 / 6) := by
  rw [← rotAbout_add_nat_mul_two_pi c (-(2 * Real.pi / 6)) 1]
  congr 1
  push_cast
  ring

open MainAux in
/-- **Invariance under `ρ⁵` gives invariance under `ρ`**, `ρ` the rotation by `2π/6`: `(ρ⁵)⁵ = ρ²⁵ = ρ`.
No finiteness is needed. -/
theorem invariant_sixth_of_five {S : Finset Point} {c : Point}
    (h : Invariant (rotAbout c (2 * Real.pi * 5 / 6)) S) :
    Invariant (rotAbout c (2 * Real.pi / 6)) S := by
  intro p hp
  have h5 := iterate_mem h hp 5
  rw [rotAbout_iterate] at h5
  have e : ((5 : ℕ) : ℝ) * (2 * Real.pi * 5 / 6) = 2 * Real.pi / 6 + (4 : ℕ) * (2 * Real.pi) := by
    push_cast
    ring
  rwa [e, rotAbout_add_nat_mul_two_pi] at h5

/-- Invariance under a rotation of order 6 about `c` (by `2π/6` or by `2π·5/6`) gives invariance under
the rotation by `2π/6`. -/
theorem invariant_sixth_of_order6 {S : Finset Point} {c : Point}
    (h : Invariant (rotAbout c (2 * Real.pi / 6)) S ∨ Invariant (rotAbout c (2 * Real.pi * 5 / 6)) S) :
    Invariant (rotAbout c (2 * Real.pi / 6)) S :=
  h.elim id invariant_sixth_of_five

/-- **No model, no 66-point sixfold counterexample.** -/
theorem sixfold66_of_no_model (h : EncB.Model 6 8 11 → False) : Sixfold66 :=
  fun _T _c hgp hc hinv hcard => Classical.byContradiction fun hno =>
    (labelling_of_counterexample (m := 6) (K := 8) (t := 11) MainAux.numerals.2.1
        MainAux.numerals.2.2.1 MainAux.numerals.2.2.2.2.1 hgp hc (MainAux.invariant_cast_six hinv) hno
        (hcard.trans MainAux.numerals.2.2.2.2.2)).elim fun L =>
      h (modelOfLabelling MainAux.numerals.1 MainAux.numerals.2.2.1 MainAux.numerals.2.2.2.1
        MainAux.numerals.2.2.2.2.1 hgp hc (MainAux.invariant_cast_six hinv) hno L)

/-- **`Sixfold66` from the unsatisfiability of the encoder-B formula.** -/
theorem sixfold66_of_unsat (h : ¬ EncB.DimacsSatisfiable (EncB.encB 6 8 11)) : Sixfold66 :=
  sixfold66_of_no_model fun M => h (EncB.encB_satisfiable_6811 M)

/-- **`Sixfold66` from the unsatisfiability of the 64 cubes.** -/
theorem sixfold66_of_cubes64 (h : EncB.CubesUnsat64) : Sixfold66 :=
  sixfold66_of_unsat (EncB.encB_unsat_of_cubesUnsat64 h)

/-- **The sixfold case of `ES(8) = 65`, given `CubesUnsat64`.** -/
theorem sixfold_es8 (h : EncB.CubesUnsat64) (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 6)) S) (hcard : 61 ≤ S.card) :
    HasConvexNGon 8 S :=
  sixfold_octagon (sixfold66_of_cubes64 h) S c hgp hinv hcard

/-- **The sixfold case of `ES(8) = 65`, given what cake_lpr's 64 verdicts on the 64 texts printed by
`twin-cube64 6 8 11 i` mean** (trust item E3): each text parses to an unsatisfiable clause list. -/
theorem sixfold_es8_of_texts
    (h : ∀ (i : Nat) (hi : i < EncB.cubes64.length) (nv : Nat) (G : List (List Int)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
        ¬EncB.DimacsSatisfiable G)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 6)) S) (hcard : 61 ≤ S.card) :
    HasConvexNGon 8 S :=
  sixfold_octagon (sixfold66_of_no_model (EncB.no_model_6811_of_texts h)) S c hgp hinv hcard

/-- **`sixfold_es8` for a rotation of order 6 in either direction** (by `2π/6` or by `2π·5/6`, the
latter equal to the rotation by `-(2π/6)`, `rotAbout_neg_sixth`). -/
theorem sixfold_es8_order6 (h : EncB.CubesUnsat64) (S : Finset Point) (c : Point)
    (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 6)) S ∨ Invariant (rotAbout c (2 * Real.pi * 5 / 6)) S)
    (hcard : 61 ≤ S.card) : HasConvexNGon 8 S :=
  sixfold_es8 h S c hgp (invariant_sixth_of_order6 hinv) hcard

/-- **`sixfold_es8_of_texts` for a rotation of order 6 in either direction.** -/
theorem sixfold_es8_order6_of_texts
    (h : ∀ (i : Nat) (hi : i < EncB.cubes64.length) (nv : Nat) (G : List (List Int)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
        ¬EncB.DimacsSatisfiable G)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 6)) S ∨ Invariant (rotAbout c (2 * Real.pi * 5 / 6)) S)
    (hcard : 61 ≤ S.card) : HasConvexNGon 8 S :=
  sixfold_es8_of_texts h S c hgp (invariant_sixth_of_order6 hinv) hcard

end EncB.Geo

#print axioms EncB.Geo.sixfold66_of_no_model
#print axioms EncB.Geo.sixfold66_of_unsat
#print axioms EncB.Geo.sixfold66_of_cubes64
#print axioms EncB.Geo.sixfold_es8
#print axioms EncB.Geo.sixfold_es8_of_texts
#print axioms EncB.Geo.sixfold_es8_order6
#print axioms EncB.Geo.sixfold_es8_order6_of_texts
#print axioms EncB.Geo.rotAbout_neg_sixth

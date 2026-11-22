import ES8Geo.Capstone2
import EncBO.Compose7
import Geo7.ModelOfLab

/-!
# The sevenfold octagon theorem from the cake_lpr verdict on `twin-base 7 8 10`

* `Geo7Bridge` (the geometric half for m = 7: a 70-point sevenfold counterexample yields a `ModelO 7 8 10`) is
  **proved**: `geo7Bridge`, from `modelO_of_counterexample` (Geo7/ModelOfLab.lean) at `m = 7, K = 8, t = 10`.
* `sevenfold70_of_unsat : ¬ DimacsSatisfiable (encB 7 8 10) → Sevenfold70` (M3 for odd m + `geo7Bridge`).
* `sevenfold_es8_of_text`: every set of at least 65 points in general position that is invariant under the
  rotation by `2π/7` about some point has a convex octagon, given that the text printed by
  `encb_dimacs twin-base 7 8 10` (`cnfText (encode 7 8 10) []`) parses to an unsatisfiable clause list — what
  cake_lpr's verdict on the hash-bound file is taken to mean (trust items E1–E3); `EncB.text7810_iff` shows the
  hypothesis is equivalent to `¬ DimacsSatisfiable (encB 7 8 10)`.

Every declaration that mentions the instance (`7 8 10`, `ModelO 7 8 10`) is a term; numerals and the cast of the
angle are separate lemmas (`numerals7`, `invariant_cast_seven`).
-/

namespace EncB.Geo7
open ErdosSzekeres ErdosSzekeres.LayerLemma

/-- **The geometric half for m = 7**: every centre-free 70-point set in general position, invariant under the
rotation by `2π/7` about `c`, with no convex octagon, yields a `ModelO 7 8 10`. -/
def Geo7Bridge : Prop :=
  ∀ (T : Finset Point) (c : Point), GeneralPosition T → c ∉ T →
    Invariant (rotAbout c (2 * Real.pi / 7)) T → T.card = 70 → ¬ HasConvexNGon 8 T →
      Nonempty (EncB.ModelO 7 8 10)

/-- The numeral side conditions of (7,8,10). -/
theorem numerals7 : 3 ≤ 7 ∧ 4 ≤ 8 ∧ 8 ≤ 2 * 7 ∧ (70 : ℕ) = 7 * 10 := by norm_num

/-- `Sevenfold70` writes the angle with the real numeral `7`; M5/M6 take `((7 : ℕ) : ℝ)`. -/
theorem invariant_cast_seven {T : Finset Point} {c : Point}
    (h : Invariant (rotAbout c (2 * Real.pi / 7)) T) :
    Invariant (rotAbout c (2 * Real.pi / ((7 : ℕ) : ℝ))) T := by
  exact_mod_cast h

/-- **`Geo7Bridge` holds.** -/
theorem geo7Bridge : Geo7Bridge :=
  fun _T _c hgp hc hinv hcard hno =>
    modelO_of_counterexample (m := 7) (K := 8) (t := 10) numerals7.1 numerals7.2.1 numerals7.2.2.1 hgp hc
      (invariant_cast_seven hinv) hno (hcard.trans numerals7.2.2.2)

/-- `Sevenfold70` from the absence of a `ModelO 7 8 10`. -/
theorem sevenfold70_of_no_modelO (h : EncB.ModelO 7 8 10 → False) : Sevenfold70 :=
  fun T c hgp hc hinv hcard =>
    Classical.byContradiction fun hno => (geo7Bridge T c hgp hc hinv hcard hno).elim h

/-- **`Sevenfold70` from `¬ DimacsSatisfiable (encB 7 8 10)`.** -/
theorem sevenfold70_of_unsat (h : ¬ EncB.DimacsSatisfiable (EncB.encB 7 8 10)) : Sevenfold70 :=
  sevenfold70_of_no_modelO fun M => h (EncB.encB_satisfiable_7810 M)

/-- **The sevenfold case of ES(8) = 65 from the unsatisfiability of `encB 7 8 10`.** -/
theorem sevenfold_es8 (h : ¬ EncB.DimacsSatisfiable (EncB.encB 7 8 10))
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 7)) S) (hcard : 65 ≤ S.card) : HasConvexNGon 8 S :=
  sevenfold_octagon (sevenfold70_of_unsat h) S c hgp hinv hcard

/-- **The sevenfold case of ES(8) = 65 from the verdict on the text.** Every set of at least 65 points in general
position that is invariant under the rotation by `2π/7` about some point has a convex octagon, provided the text
printed by `twin-base 7 8 10` parses to an unsatisfiable clause list. -/
theorem sevenfold_es8_of_text
    (h : ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬ EncB.DimacsSatisfiable G)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 7)) S) (hcard : 65 ≤ S.card) : HasConvexNGon 8 S :=
  sevenfold_octagon (sevenfold70_of_no_modelO (EncB.no_modelO_7810_of_text h)) S c hgp hinv hcard

/-! ## Any rotation of order 7 -/

/-- `rotAbout` is `2π`-periodic in the angle (as ENCBLEAN's `MainAux.rotAbout_add_nat_mul_two_pi`). -/
theorem rotAbout_add_nat_mul_two_pi' (c : Point) (θ : ℝ) (n : ℕ) :
    rotAbout c (θ + n * (2 * Real.pi)) = rotAbout c θ := by
  funext p
  simp only [rotAbout, Real.cos_add_nat_mul_two_pi, Real.sin_add_nat_mul_two_pi]

/-- Invariance under `ρ^j` gives invariance under `ρ` when `j·j' = 1 + 7n` (`ρ` the rotation by `2π/7`). -/
theorem invariant_of_inverse {S : Finset Point} {c : Point} {j j' n : ℕ} (hjj : j * j' = 1 + 7 * n)
    (h : Invariant (rotAbout c (2 * Real.pi * j / 7)) S) : Invariant (rotAbout c (2 * Real.pi / 7)) S := by
  intro p hp
  have hit := iterate_mem h hp j'
  rw [rotAbout_iterate] at hit
  have e : (j' : ℝ) * (2 * Real.pi * j / 7) = 2 * Real.pi / 7 + (n : ℝ) * (2 * Real.pi) := by
    have : (j : ℝ) * j' = 1 + 7 * n := by exact_mod_cast hjj
    linear_combination (2 * Real.pi / 7) * this
  rwa [e, rotAbout_add_nat_mul_two_pi'] at hit

/-- **A rotation of order 7** about `c` (by `2πj/7`, `1 ≤ j ≤ 6`) gives invariance under the rotation by `2π/7`. -/
theorem invariant_seventh_of_order7 {S : Finset Point} {c : Point} {j : ℕ} (hj : 1 ≤ j ∧ j ≤ 6)
    (h : Invariant (rotAbout c (2 * Real.pi * j / 7)) S) : Invariant (rotAbout c (2 * Real.pi / 7)) S := by
  obtain ⟨h1, h6⟩ := hj
  interval_cases j
  · exact invariant_of_inverse (j' := 1) (n := 0) (by norm_num) h
  · exact invariant_of_inverse (j' := 4) (n := 1) (by norm_num) h
  · exact invariant_of_inverse (j' := 5) (n := 2) (by norm_num) h
  · exact invariant_of_inverse (j' := 2) (n := 1) (by norm_num) h
  · exact invariant_of_inverse (j' := 3) (n := 2) (by norm_num) h
  · exact invariant_of_inverse (j' := 6) (n := 5) (by norm_num) h

/-- **The sevenfold case of ES(8) = 65 for any rotation of order 7**, from the verdict on the text. -/
theorem sevenfold_es8_order7_of_text
    (h : ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬ EncB.DimacsSatisfiable G)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S) (j : ℕ) (hj : 1 ≤ j ∧ j ≤ 6)
    (hinv : Invariant (rotAbout c (2 * Real.pi * j / 7)) S) (hcard : 65 ≤ S.card) : HasConvexNGon 8 S :=
  sevenfold_es8_of_text h S c hgp (invariant_seventh_of_order7 hj hinv) hcard

end EncB.Geo7

/-! ## Pins: statements and axioms (the build fails if either changes) -/

/--
info: EncB.Geo7.sevenfold_es8_of_text
  (h :
    ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G)
  (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point) (hgp : ErdosSzekeres.GeneralPosition S)
  (hinv : ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 7)) S)
  (hcard : 65 ≤ S.card) : ErdosSzekeres.HasConvexNGon 8 S
-/
#guard_msgs in #check EncB.Geo7.sevenfold_es8_of_text
/--
info: EncB.Geo7.sevenfold70_of_unsat (h : ¬EncB.DimacsSatisfiable (EncB.encB 7 8 10)) : ErdosSzekeres.LayerLemma.Sevenfold70
-/
#guard_msgs in #check EncB.Geo7.sevenfold70_of_unsat
/--
info: EncB.Geo7.sevenfold_es8_order7_of_text
  (h :
    ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G)
  (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point) (hgp : ErdosSzekeres.GeneralPosition S) (j : ℕ)
  (hj : 1 ≤ j ∧ j ≤ 6)
  (hinv : ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi * ↑j / 7)) S)
  (hcard : 65 ≤ S.card) : ErdosSzekeres.HasConvexNGon 8 S
-/
#guard_msgs in #check EncB.Geo7.sevenfold_es8_order7_of_text

/-- info: 'EncB.Geo7.geo7Bridge' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo7.geo7Bridge

/-- info: 'EncB.Geo7.sevenfold70_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo7.sevenfold70_of_unsat

/-- info: 'EncB.Geo7.sevenfold_es8' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo7.sevenfold_es8

/-- info: 'EncB.Geo7.sevenfold_es8_of_text' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo7.sevenfold_es8_of_text

/-- info: 'EncB.Geo7.sevenfold_es8_order7_of_text' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo7.sevenfold_es8_order7_of_text

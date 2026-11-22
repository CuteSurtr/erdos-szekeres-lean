import ErdosSzekeres.Omission.CoupledSemantics
import RowGeo.Decode

/-!
# RowGeo.Bridge: the Std-only literals as the library's `Coupled.Expr`

`toExpr hk : Lit → Coupled.Expr k` reads indices modulo `k` (and atoms through `Atm.norm`). For indices below
`k ≤ 16` the helpers of `RowEnc.Enc` become the library's helpers: `toExpr_befL`, `toExpr_geL`, `toExpr_posL`,
`toExpr_neg`, `toExpr_disagreeL`. `holds_toExpr`: a literal holds in a context iff it holds for the meaning `μ C`.
-/

namespace RowGeo
open RowEnc ErdosSzekeres ErdosSzekeres.Omission Coupled

variable {k : ℕ} (hk : 0 < k)

def fk (i : ℕ) : Fin k := ⟨i % k, Nat.mod_lt _ hk⟩

def toAtom : Atm → Atom k
  | .bef i j => .before (fk hk i) (fk hk j)
  | .cap i j t => .capGe (fk hk i) (fk hk j) t
  | .cup i j t => .cupGe (fk hk i) (fk hk j) t
  | .ori i j l => .positive (fk hk i) (fk hk j) (fk hk l)
  | .cvx i j l m => .convex (fk hk i) (fk hk j) (fk hk l) (fk hk m)

def toExpr : Lit → Expr k
  | .const b => .constant b
  | .atom a b => .atom (toAtom hk a.norm) b

theorem fk_val {i : ℕ} (hi : i < k) : (fk hk i).val = i := Nat.mod_eq_of_lt hi

theorem fk_eq {i : ℕ} (hi : i < k) : fk hk i = ⟨i, hi⟩ := Fin.ext (fk_val hk hi)

theorem fk_lt_iff {i j : ℕ} (hi : i < k) (hj : j < k) : fk hk i < fk hk j ↔ i < j := by
  rw [Fin.lt_def, fk_val hk hi, fk_val hk hj]

theorem fk_min {i j : ℕ} (hi : i < k) (hj : j < k) : fk hk (min i j) = min (fk hk i) (fk hk j) := by
  rcases le_total i j with h | h
  · rw [min_eq_left h, min_eq_left (Fin.le_def.2 (by rw [fk_val hk hi, fk_val hk hj]; exact h))]
  · rw [min_eq_right h, min_eq_right (Fin.le_def.2 (by rw [fk_val hk hi, fk_val hk hj]; exact h))]

theorem fk_max {i j : ℕ} (hi : i < k) (hj : j < k) : fk hk (max i j) = max (fk hk i) (fk hk j) := by
  rcases le_total i j with h | h
  · rw [max_eq_right h, max_eq_right (Fin.le_def.2 (by rw [fk_val hk hi, fk_val hk hj]; exact h))]
  · rw [max_eq_left h, max_eq_left (Fin.le_def.2 (by rw [fk_val hk hi, fk_val hk hj]; exact h))]

theorem toExpr_neg (e : Lit) : toExpr hk e.neg = (toExpr hk e).neg := by
  cases e <;> rfl

theorem toExpr_disagreeL (e : Lit) (b : Bool) : toExpr hk (disagreeL e b) = disagree (toExpr hk e) b := by
  cases b <;> simp [disagreeL, disagree, toExpr_neg]

section bounded
variable (h16 : k ≤ 16)
include h16

theorem toExpr_bef {i j : ℕ} (hi : i < k) (hj : j < k) (b : Bool) :
    toExpr hk (.atom (.bef i j) b) = .atom (.before (fk hk i) (fk hk j)) b := by
  simp only [toExpr, Atm.norm, toAtom, Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hi h16),
    Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hj h16)]

theorem toExpr_befL {i j : ℕ} (hi : i < k) (hj : j < k) :
    toExpr hk (befL i j) = before (fk hk i) (fk hk j) := by
  unfold befL before
  by_cases h : i < j
  · rw [if_pos h, if_pos ((fk_lt_iff hk hi hj).2 h), toExpr_bef hk h16 hi hj]
  · rw [if_neg h, if_neg (fun h' => h ((fk_lt_iff hk hi hj).1 h')), toExpr_bef hk h16 hj hi]

theorem toExpr_geL (cup : Bool) {i j : ℕ} (hi : i < k) (hj : j < k) (t : ℕ) :
    toExpr hk (geL cup i j t) = ge cup (fk hk i) (fk hk j) t := by
  have hmin : min i j < k := lt_of_le_of_lt (min_le_left _ _) hi
  have hmax : max i j < k := max_lt hi hj
  have m1 : min i j % 16 = min i j := Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hmin h16)
  have m2 : max i j % 16 = max i j := Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hmax h16)
  unfold geL ge
  by_cases h1 : t ≤ 1
  · rw [if_pos h1, if_pos h1]; rfl
  rw [if_neg h1, if_neg h1]
  cases cup
  · simp only [Bool.false_eq_true, if_false]
    by_cases h2 : 4 < t
    · rw [if_pos h2, if_pos h2]; rfl
    · rw [if_neg h2, if_neg h2]
      simp only [toExpr, Atm.norm, toAtom, m1, m2, Nat.mod_eq_of_lt (show t < 8 by omega),
        fk_min hk hi hj, fk_max hk hi hj]
  · simp only [if_true]
    by_cases h2 : 6 < t
    · rw [if_pos h2, if_pos h2]; rfl
    · rw [if_neg h2, if_neg h2]
      simp only [toExpr, Atm.norm, toAtom, m1, m2, Nat.mod_eq_of_lt (show t < 8 by omega),
        fk_min hk hi hj, fk_max hk hi hj]

theorem toExpr_ori {i j l : ℕ} (hi : i < k) (hj : j < k) (hl : l < k) (b : Bool) :
    toExpr hk (.atom (.ori i j l) b) = .atom (.positive (fk hk i) (fk hk j) (fk hk l)) b := by
  simp only [toExpr, Atm.norm, toAtom, Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hi h16),
    Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hj h16), Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hl h16)]

theorem toExpr_posL {i j l : ℕ} (hi : i < k) (hj : j < k) (hl : l < k) :
    toExpr hk (posL i j l) = positive (fk hk i) (fk hk j) (fk hk l) := by
  have e1 := fk_lt_iff hk hi hj
  have e2 := fk_lt_iff hk hj hl
  have e3 := fk_lt_iff hk hi hl
  have e4 := fk_lt_iff hk hj hi
  have e5 := fk_lt_iff hk hl hi
  have e6 := fk_lt_iff hk hl hj
  unfold posL positive
  by_cases a1 : i < j <;> by_cases a2 : j < l <;> by_cases a3 : i < l <;>
    simp only [a1, a2, a3, e1, e2, e3, if_true, if_false, toExpr_ori hk h16 hi hj hl,
      toExpr_ori hk h16 hi hl hj, toExpr_ori hk h16 hl hi hj, toExpr_ori hk h16 hj hi hl,
      toExpr_ori hk h16 hj hl hi, toExpr_ori hk h16 hl hj hi]

theorem toExpr_cvx {i j l m : ℕ} (hi : i < k) (hj : j < k) (hl : l < k) (hm : m < k) (b : Bool) :
    toExpr hk (.atom (.cvx i j l m) b) = .atom (.convex (fk hk i) (fk hk j) (fk hk l) (fk hk m)) b := by
  simp only [toExpr, Atm.norm, toAtom, Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hi h16),
    Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hj h16), Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hl h16),
    Nat.mod_eq_of_lt (Nat.lt_of_lt_of_le hm h16)]

end bounded

/-! ## Meaning of the literals in a context -/

section
variable {n : ℕ} {states : Fin k → Fin 154} (C : Context k n states)

open Classical in
/-- The meaning of the atoms in the context `C`. -/
noncomputable def μ (a : Atm) : Bool := decide (C.atom (toAtom hk a))

theorem holds_toExpr (e : Lit) : C.holds (toExpr hk e) ↔ LSem (μ hk C) e := by
  cases e with
  | const b => exact Iff.rfl
  | atom a b =>
    cases b <;> simp [toExpr, LSem, μ, Context.holds]

theorem lsem_of_clause (cl : List Lit) (h : C.clause (cl.map (toExpr hk))) : ∃ e ∈ cl, LSem (μ hk C) e := by
  obtain ⟨x, hx, hh⟩ := h
  obtain ⟨e, he, rfl⟩ := List.mem_map.1 hx
  exact ⟨e, he, (holds_toExpr hk C e).1 hh⟩

end

end RowGeo

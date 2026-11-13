/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, formal/sources/ES8CycleSigns.lean.
MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: project real-point type, namespaces/imports, Lean/Mathlib 4.24.
-/
import ErdosSzekeres.Omission.BoundingBoxes
import ErdosSzekeres.OrientationGeometry

namespace ErdosSzekeres.Omission.CycleSigns
open StateInterface Domains

/-- Empty directed differences rule out an order. Otherwise the required
coordinate separation must force the desired chronological triple color. -/
def Safe (ab bc ac : Box) (want : Bool) : Prop :=
  ab.present=false ∨ bc.present=false ∨ ac.present=false ∨
  (if want then bc.xmax ≤ ab.xmin else bc.ymax ≤ ab.ymin)
instance (ab bc ac : Box) (want : Bool) : Decidable (Safe ab bc ac want) := by unfold Safe; infer_instance

def CheckTriple (table : Nat → Nat → Box) (a b c : Nat) : Bool := decide (
  Safe (table a b) (table b c) (table a c) true ∧
  Safe (table a c) (table c b) (table a b) false ∧
  Safe (table b a) (table a c) (table b c) false ∧
  Safe (table b c) (table c a) (table b a) true ∧
  Safe (table c a) (table a b) (table c b) true ∧
  Safe (table c b) (table b a) (table c a) false)

theorem safe_force (n : Nat) (cup : Nat → Nat → Nat → Bool) (d : Nat → Nat → Label)
    (growth : IncreasingLabels n cup d) (u v w : Fin n) (uv : u < v) (vw : v < w)
    (ab bc ac : Box) (hab : Fits ab (d u v)) (hbc : Fits bc (d v w)) (hac : Fits ac (d u w))
    (want : Bool) (safe : Safe ab bc ac want) : cup u v w=want := by
  have separation : if want then bc.xmax ≤ ab.xmin else bc.ymax ≤ ab.ymin := by
    simpa [Safe,hab.1,hbc.1,hac.1] using safe
  have g := growth u v w uv vw w.isLt
  cases want with
  | false =>
    cases hc : cup u v w with
    | false => rfl
    | true =>
      have step := g.2 hc
      dsimp at separation
      rcases hab with ⟨_,_,_,hlo,_⟩
      rcases hbc with ⟨_,_,_,_,hhi⟩
      omega
  | true =>
    cases hc : cup u v w with
    | true => rfl
    | false =>
      have step := g.1 hc
      dsimp at separation
      rcases hab with ⟨_,hlo,_,_,_⟩
      rcases hbc with ⟨_,_,hhi,_,_⟩
      omega

theorem orient_rotate (p q r : Point) : orient p q r = orient q r p := (orient_cycle p q r).symm

theorem orient_swap12 (p q r : Point) : orient q p r = -orient p q r := by unfold orient; ring

theorem orient_swap23 (p q r : Point) : orient p r q = -orient p q r := by unfold orient; ring

theorem orient_reverse (p q r : Point) : orient r q p = -orient p q r := by unfold orient; ring

/-- All six chronological possibilities are discharged. Nothing assumes that
state IDs, cyclic positions, and chronological owner indices have the same order. -/
theorem checked_triple_positive (n : Nat) (table : Nat → Nat → Box) (index : Fin n → Nat)
    (cup : Nat → Nat → Nat → Bool) (d : Nat → Nat → Label) (p : Fin n → Point)
    (growth : IncreasingLabels n cup d)
    (pairs : ∀ u v : Fin n, u < v → Fits (table (index u) (index v)) (d u v))
    (signs : ∀ u v w : Fin n, u < v → v < w → (cup u v w=true ↔ 0 < orient (p u) (p v) (p w)))
    (nonzero : ∀ u v w : Fin n, u < v → v < w → orient (p u) (p v) (p w) ≠ 0)
    (u v w : Fin n) (uv : u ≠ v) (vw : v ≠ w) (uw : u ≠ w)
    (checked : CheckTriple table (index u) (index v) (index w)=true) :
    0 < orient (p u) (p v) (p w) := by
  have hc := of_decide_eq_true checked
  rcases hc with ⟨h1,h2,h3,h4,h5,h6⟩
  have pos (a b c : Fin n) (ab : a < b) (bc : b < c)
      (safe : Safe (table (index a) (index b)) (table (index b) (index c)) (table (index a) (index c)) true) :
      0 < orient (p a) (p b) (p c) := by
    apply (signs a b c ab bc).mp
    exact safe_force n cup d growth a b c ab bc _ _ _ (pairs a b ab) (pairs b c bc) (pairs a c (lt_trans ab bc)) true safe
  have neg (a b c : Fin n) (ab : a < b) (bc : b < c)
      (safe : Safe (table (index a) (index b)) (table (index b) (index c)) (table (index a) (index c)) false) :
      orient (p a) (p b) (p c) < 0 := by
    have color := safe_force n cup d growth a b c ab bc _ _ _ (pairs a b ab) (pairs b c bc) (pairs a c (lt_trans ab bc)) false safe
    have nz := nonzero a b c ab bc
    have notPos : ¬ 0 < orient (p a) (p b) (p c) := by
      intro hp
      have ht := (signs a b c ab bc).mpr hp
      rw [color] at ht
      contradiction
    exact lt_of_le_of_ne (le_of_not_gt notPos) nz
  rcases lt_or_gt_of_ne uv with huv | hvu
  · rcases lt_or_gt_of_ne vw with hvw | hwv
    · exact pos u v w huv hvw h1
    · rcases lt_or_gt_of_ne uw with huw | hwu
      · have h := neg u w v huw hwv h2
        rw [orient_swap23] at h
        linarith
      · have h := pos w u v hwu huv h5
        rwa [orient_rotate] at h
  · rcases lt_or_gt_of_ne uw with huw | hwu
    · have h := neg v u w hvu huw h3
      rw [orient_swap12] at h
      linarith
    · rcases lt_or_gt_of_ne vw with hvw | hwv
      · have h := pos v w u hvw hwu h4
        rwa [orient_rotate,orient_rotate] at h
      · have h := neg w v u hwv hvu h6
        rw [orient_reverse] at h
        linarith

end ErdosSzekeres.Omission.CycleSigns

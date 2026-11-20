/-
Lemma Z (ES305N20261119 §3) in Lean.

Z = the catalog states f with f(0) ≤ 4 and f(4) = 0 (70 states; `Z_eq` pins the exact index set used by the
budget-66 tree, `zrow.json`). The owners of Z-states contain no 6-cap and no 6-cup, so N66 bounds them, and the
Z-row holds in the form of `OmissionBalanced.all_geometric_rows`: `15 ≤ (Z \ c.occupied).card`.
N66 enters only as the hypothesis `N66Bound 55` (CERTIFIED by SAT in N66N20261113, not in Lean).
-/
import ErdosSzekeres.Omission.CycleGeometry
import ErdosSzekeres.Omission.Subsets
import ErdosSzekeres.Omission.SlopePartition

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks
  ErdosSzekeres.Omission.BalancedCatalog ErdosSzekeres.Omission.Ferrers
  ErdosSzekeres.Omission.Subsets ErdosSzekeres.Omission.SlopePartition

namespace OmissionZRow

/-- N66 as a population statement, in the style of `Partition.BalancedBound`. -/
def N66Bound (B : ℕ) : Prop :=
  ∀ n : ℕ, ∀ c : Configuration n, ¬ c.HasCap 6 → ¬ c.HasCup 6 →
    ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B

/-- A catalog profile lies in Z iff f(0) ≤ 4 and f(4) = 0. -/
def zProfile (xs : List ℕ) : Bool := decide (xs.getD 0 0 ≤ 4) && decide (xs.getD 4 0 = 0)

def Z : Finset (Fin 252) := Finset.univ.filter (fun i => zProfile (catalog.getD i.val []) = true)

/-- The exact support of the Z-row in `zrow.json` / `balz.rows`. -/
def zIndices : List ℕ := [0,1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,20,21,22,23,24,25,26,29,31,32,33,34,35,
  36,40,42,43,44,46,47,48,49,55,57,58,60,61,62,63,72,73,75,77,78,79,80,90,93,94,96,97,108,112,114,115,116,
  130,133,134,151,153,170,187]

theorem Z_eq : ∀ i : Fin 252, i ∈ Z ↔ i.val ∈ zIndices := by
  unfold Z; simp only [Finset.mem_filter, Finset.mem_univ, true_and]; decide +kernel

theorem Z_card : Z.card = 70 := by decide +kernel

/-- Six points of a monochromatic chain give an attained ending path of length 6. -/
theorem path_of_six {cup : ℕ → ℕ → ℕ → Bool} {color : Bool} {p1 p2 p3 p4 p5 p6 : ℕ}
    (h : (colorConfig cup color).Cup [p1, p2, p3, p4, p5, p6]) :
    p5 < p6 ∧ EndingPath cup color p5 p6 6 := by
  simp only [Config.Cup.cons3, Config.Cup.pair, colorConfig] at h
  obtain ⟨h12, c123, h23, c234, h34, c345, h45, c456, h56⟩ := h
  exact ⟨h56, .step (.step (.step (.step (.pair h12) h23 c123) h34 c234) h45 c345) h56 c456⟩

/-- A 6-cup ending with (u, v): cupLabel ≥ 5 and capLabel ≥ 1, so f_v(0) ≥ 5. -/
theorem five_le_column_of_cup {cup : ℕ → ℕ → ℕ → Bool} {u v : ℕ} (huv : u < v)
    (path : EndingPath cup true u v 6) : 5 ≤ column cup v 0 := by
  have r1 := rank_ge path
  have r2 := rank_ge (EndingPath.pair (cup := cup) (color := false) huv)
  unfold column
  refine Finset.le_sup_of_le (Finset.mem_range.mpr huv) ?_
  simp only [labels]
  rw [if_pos (by omega)]
  omega

/-- A 6-cap ending with (u, v): capLabel ≥ 5 and cupLabel ≥ 1, so f_v(4) ≥ 1. -/
theorem one_le_column_of_cap {cup : ℕ → ℕ → ℕ → Bool} {u v : ℕ} (huv : u < v)
    (path : EndingPath cup false u v 6) : 1 ≤ column cup v 4 := by
  have r1 := rank_ge path
  have r2 := rank_ge (EndingPath.pair (cup := cup) (color := true) huv)
  unfold column
  refine Finset.le_sup_of_le (Finset.mem_range.mpr huv) ?_
  simp only [labels]
  rw [if_pos (by omega)]
  omega

/-- The catalog profile of an owner is its column vector. -/
theorem owner_profile {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (v : Fin n) :
    catalog.getD (c.balancedOwner noCap noCup v).val [] =
      List.ofFn (fun i : Fin 5 => column c.cup v i) := by
  have h := ownerIndex_profile n c.cup (c.avoids_of_noCap noCap) (c.avoids_of_noCup noCup) v
  rw [List.getD_eq_getElem _ _ (by rw [catalog_length]; exact (c.balancedOwner noCap noCup v).isLt)]
  exact h

theorem owner_mem_Z {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (v : Fin n) (h : c.balancedOwner noCap noCup v ∈ Z) :
    column c.cup v 0 ≤ 4 ∧ column c.cup v 4 = 0 := by
  simp only [Z, Finset.mem_filter, Finset.mem_univ, true_and, owner_profile c noCap noCup v, zProfile,
    Bool.and_eq_true, decide_eq_true_eq] at h
  simpa [List.ofFn_succ] using h

/-- The owners of Z-states. -/
noncomputable def zOwners {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) : Finset (Fin n) :=
  Finset.univ.filter (fun v => c.balancedOwner noCap noCup v ∈ Z)

theorem zOwner_columns {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    {a : ℕ} (ha : a ∈ natSet (zOwners c noCap noCup)) :
    column c.cup a 0 ≤ 4 ∧ column c.cup a 4 = 0 := by
  have an := Finset.mem_range.mp (natSet_bounded _ ha)
  have hmem := (natSet_member _ ⟨a, an⟩).mp ha
  exact owner_mem_Z c noCap noCup ⟨a, an⟩ (Finset.mem_filter.mp hmem).2

theorem six_list {xs : List ℕ} (len : xs.length = 6) :
    ∃ p1 p2 p3 p4 p5 p6, xs = [p1, p2, p3, p4, p5, p6] := by
  rcases xs with _ | ⟨p1, _ | ⟨p2, _ | ⟨p3, _ | ⟨p4, _ | ⟨p5, _ | ⟨p6, _ | ⟨p7, xs⟩⟩⟩⟩⟩⟩⟩ <;>
    simp at len
  exact ⟨p1, p2, p3, p4, p5, p6, rfl⟩

/-- Lemma Z, cup half: the Z-owners contain no 6-cup. -/
theorem zOwners_no_cup {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) :
    ¬ (colorConfig c.cup true).HasNCup 6 (natSet (zOwners c noCap noCup)) := by
  rintro ⟨xs, ⟨cup, len⟩, inside⟩
  obtain ⟨p1, p2, p3, p4, p5, p6, rfl⟩ := six_list len
  obtain ⟨h56, path⟩ := path_of_six cup
  have hz := zOwner_columns c noCap noCup (inside p6 (by simp))
  have := five_le_column_of_cup h56 path
  omega

/-- Lemma Z, cap half: the Z-owners contain no 6-cap. -/
theorem zOwners_no_cap {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) :
    ¬ (colorConfig c.cup true).HasNCap 6 (natSet (zOwners c noCap noCup)) := by
  rintro ⟨xs, ⟨cap, len⟩, inside⟩
  have cup := (false_cup_iff_cap c.cup xs).mpr cap
  obtain ⟨p1, p2, p3, p4, p5, p6, rfl⟩ := six_list len
  obtain ⟨h56, path⟩ := path_of_six cup
  have hz := zOwner_columns c noCap noCup (inside p6 (by simp))
  have := one_le_column_of_cap h56 path
  omega

theorem zOwners_card_le {n : ℕ} (n66 : N66Bound 55) (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    (zOwners c noCap noCup).card ≤ 55 :=
  n66 _ (restrict c _) (restrict_no_cap c _ (zOwners_no_cap c noCap noCup))
    (restrict_no_cup c _ (zOwners_no_cup c noCap noCup)) (restrict_no_octagon c _ noOctagon)

theorem Z_inter_occupied {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) :
    Z ∩ c.occupied noCap noCup = (zOwners c noCap noCup).image (c.balancedOwner noCap noCup) := by
  ext i
  simp only [Finset.mem_inter, Configuration.occupied, zOwners, Finset.mem_image, Finset.mem_filter,
    Finset.mem_univ, true_and]
  constructor
  · rintro ⟨hz, v, rfl⟩
    exact ⟨v, hz, rfl⟩
  · rintro ⟨v, hz, rfl⟩
    exact ⟨hz, v, rfl⟩

/-- **The Z-row**, in the form of `OmissionBalanced.all_geometric_rows` (demand 15, support Z). -/
theorem z_row {n : ℕ} (n66 : N66Bound 55) (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    15 ≤ (Z \ c.occupied noCap noCup).card := by
  have h1 := Finset.card_sdiff_add_card_inter Z (c.occupied noCap noCup)
  rw [Z_inter_occupied, Finset.card_image_of_injective _ (c.balancedOwner_injective noCap noCup),
    Z_card] at h1
  have h2 := zOwners_card_le n66 c noCap noCup noOctagon
  omega

end OmissionZRow

#print axioms OmissionZRow.Z_eq
#print axioms OmissionZRow.z_row

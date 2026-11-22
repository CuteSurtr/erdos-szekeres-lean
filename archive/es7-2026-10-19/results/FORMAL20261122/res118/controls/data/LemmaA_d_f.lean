/-
res118-lean (22 November 2026): Lemma A, Lo half, in Lean.

Written source: THEORY310N20261113 §2, Lemma A (ii) ("R \ R₆ has no 6-cup (and no 6-cap)"); the 308 bridge
(LO33N20261113/budget34/bridge/README.md §2, eq. (A): h(Lo) ≥ 70 − N66); checked against the Lean definitions in
VERIFY_LO §2.6. Pattern: `OmissionZRow.z_row` (ES305N20261119/LemmaZ.lean).

* `Lo` = the residual catalog states whose first height f₁ (column 0) is at most 4, `F` = the others (f₁ ≥ 5).
  `Lo_eq` / `F_eq` pin them to the literal index lists of the capacity rows of every slice tree (rows 1 and 0 of
  each extra.json); `Lo_card = 70`, `F_card = 84`.
* An owner in `Lo` has f₁ ≤ 4. The last point of a 6-cup has f₁ ≥ 5 (`five_le_column_of_cup`), so the Lo-owners
  contain no 6-cup; the residual configuration has no 6-cap at all. Hence an N66 bound `B` (the predicate
  `OmissionZRow.N66Bound` of LemmaZ.lean, the one `composition_304_z` takes) bounds the Lo-owners, and
  `lo_row : N66Bound B → 70 − B ≤ (Lo \ residualOccupied).card`.
-/
import ErdosSzekeres.Omission.ResidualCycleGeometry
import ErdosSzekeres.Omission.SlopePartition
import LemmaZ

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks
  ErdosSzekeres.Omission.Subsets ErdosSzekeres.Omission.SlopePartition

namespace Res118

/-- A residual catalog profile lies in Lo iff its first height f₁ is at most 4. -/
def loProfile (xs : List ℕ) : Bool := decide (xs.getD 0 0 ≤ 4)

/-- State `i` lies in Lo. -/
def InLo (i : Fin 154) : Prop := loProfile (ResidualCatalog.catalog.getD i.val []) = true

instance : DecidablePred InLo := fun _ => inferInstanceAs (Decidable (_ = true))

/-- The 70 residual states with f₁ ≤ 4. -/
def Lo : Finset (Fin 154) := Finset.univ.filter InLo

/-- The 84 residual states with f₁ ≥ 5. -/
def F : Finset (Fin 154) := Finset.univ.filter (fun i => ¬ InLo i)

/-- Support of the Lo capacity row in every slice row file (extra.json row 1). -/
def loIndices : List ℕ := [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 26,
  27, 28, 29, 30, 31, 32, 35, 36, 37, 38, 39, 40, 41, 42, 46, 47, 48, 49, 50, 51, 52, 57, 58, 59, 60, 61, 62, 63, 69,
  70, 71, 72, 73, 80, 81, 82, 83, 84, 92, 93, 94, 102, 103, 112, 120]

/-- Support of the F capacity row in every slice row file (extra.json row 0). -/
def fIndices : List ℕ := [17, 25, 33, 34, 43, 44, 45, 53, 54, 55, 56, 64, 65, 66, 67, 68, 74, 75, 76, 77, 78, 79, 85,
  86, 87, 88, 89, 90, 91, 95, 96, 97, 98, 99, 100, 101, 104, 105, 106, 107, 108, 109, 110, 111, 113, 114, 115, 116,
  117, 118, 119, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
  141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 120]

theorem Lo_eq : ∀ i : Fin 154, i ∈ Lo ↔ i.val ∈ loIndices := by
  unfold Lo InLo; simp only [Finset.mem_filter, Finset.mem_univ, true_and]; decide +kernel

theorem F_eq : ∀ i : Fin 154, i ∈ F ↔ i.val ∈ fIndices := by
  unfold F InLo; simp only [Finset.mem_filter, Finset.mem_univ, true_and]; decide +kernel

theorem Lo_card : Lo.card = 70 := by decide +kernel

theorem F_card : F.card = 84 := by decide +kernel

/-- F and Lo partition the 154 states. -/
theorem sum_Lo_add_sum_F (h : Fin 154 → ℕ) : ∑ i ∈ Lo, h i + ∑ i ∈ F, h i = ∑ i, h i :=
  Finset.sum_filter_add_sum_filter_not Finset.univ InLo h

/-- The catalog profile of a residual owner is its column vector followed by 0. -/
theorem owner_profile {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) (v : Fin n) :
    ResidualCatalog.catalog.getD (c.residualOwner noCap noOctagon noJunction v).val [] =
      List.ofFn (fun i : Fin 4 => ResidualStates.column n c.cup v i) ++ [0] := by
  have h := ResidualCatalog.ownerIndex_profile n c.cup (fun h => noCap (ListGeometry.hasCap_of_list c h))
    (c.residual_avoids_cup noOctagon) (ResidualRanks.noJunction_of_lists n c.cup noJunction) v
  rw [List.getD_eq_getElem _ _ (by
    rw [ResidualCatalog.catalog_length]; exact (c.residualOwner noCap noOctagon noJunction v).isLt)]
  exact h

theorem owner_mem_Lo {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) (v : Fin n)
    (h : c.residualOwner noCap noOctagon noJunction v ∈ Lo) :
    ResidualStates.column n c.cup v 0 ≤ 4 := by
  simp only [Lo, InLo, Finset.mem_filter, Finset.mem_univ, true_and,
    owner_profile c noCap noOctagon noJunction v, loProfile, decide_eq_true_eq] at h
  simpa [List.ofFn_succ] using h

/-- A 6-cup ending with (u, v) in a residual configuration (no 6-cap): the cap label of (u, v) is at least 1 and
its cup label at least 5, so f₁(v) = column 0 is at least 5. -/
theorem five_le_column_of_cup {n : ℕ} {cup : ℕ → ℕ → ℕ → Bool}
    (noCap : ¬ (colorConfig cup true).HasNCap 6 (Finset.range n)) {u v : ℕ} (huv : u < v) (hvn : v < n)
    (path : EndingPath cup true u v 6) : 5 ≤ ResidualStates.column n cup v 0 := by
  have r1 := ActualRanks.rank_ge path
  have r2 := ResidualRanks.rank_lt_no_cap n cup u v noCap huv hvn
  unfold ResidualStates.column
  refine Finset.le_sup_of_le (Finset.mem_range.mpr huv) ?_
  simp only [ResidualRanks.labels]
  rw [if_pos (by omega)]
  omega

/-- The owners of Lo-states. -/
noncomputable def loOwners {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) : Finset (Fin n) :=
  Finset.univ.filter (fun v => c.residualOwner noCap noOctagon noJunction v ∈ Lo)

theorem loOwner_column {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n))
    {a : ℕ} (ha : a ∈ natSet (loOwners c noCap noOctagon noJunction)) :
    ResidualStates.column n c.cup a 0 ≤ 4 ∧ a < n := by
  have an := Finset.mem_range.mp (natSet_bounded _ ha)
  have hmem := (natSet_member _ ⟨a, an⟩).mp ha
  exact ⟨owner_mem_Lo c noCap noOctagon noJunction ⟨a, an⟩ (Finset.mem_filter.mp hmem).2, an⟩

/-- Lemma A (ii), cup half: the Lo-owners contain no 6-cup. -/
theorem loOwners_no_cup {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) :
    ¬ (colorConfig c.cup true).HasNCup 6 (natSet (loOwners c noCap noOctagon noJunction)) := by
  rintro ⟨xs, ⟨cup, len⟩, inside⟩
  obtain ⟨p1, p2, p3, p4, p5, p6, rfl⟩ := OmissionZRow.six_list len
  obtain ⟨h56, path⟩ := OmissionZRow.path_of_six cup
  obtain ⟨hz, hn⟩ := loOwner_column c noCap noOctagon noJunction (inside p6 (by simp))
  have := five_le_column_of_cup (fun h => noCap (ListGeometry.hasCap_of_list c h)) h56 hn path
  omega

/-- Lemma A (ii), cap half: the Lo-owners contain no 6-cap (the whole residual configuration has none). -/
theorem loOwners_no_cap {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) :
    ¬ (colorConfig c.cup true).HasNCap 6 (natSet (loOwners c noCap noOctagon noJunction)) := by
  rintro ⟨xs, hcap, inside⟩
  exact noCap (ListGeometry.hasCap_of_list c ⟨xs, hcap, fun a ha => natSet_bounded _ (inside a ha)⟩)

/-- An N66 bound `B` bounds the Lo-owners (they form an octagon-free set with no 6-cap and no 6-cup). -/
theorem loOwners_card_le {B n : ℕ} (n66 : OmissionZRow.N66Bound B) (c : Configuration n)
    (noCap : ¬ c.HasCap 6) (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) :
    (loOwners c noCap noOctagon noJunction).card ≤ B :=
  n66 _ (restrict c _) (restrict_no_cap c _ (loOwners_no_cap c noCap noOctagon noJunction))
    (restrict_no_cup c _ (loOwners_no_cup c noCap noOctagon noJunction)) (restrict_no_octagon c _ noOctagon)

theorem Lo_inter_occupied {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) :
    Lo ∩ c.residualOccupied noCap noOctagon noJunction =
      (loOwners c noCap noOctagon noJunction).image (c.residualOwner noCap noOctagon noJunction) := by
  ext i
  simp only [Finset.mem_inter, Configuration.residualOccupied, loOwners, Finset.mem_image,
    Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · rintro ⟨hz, v, rfl⟩
    exact ⟨v, hz, rfl⟩
  · rintro ⟨v, hz, rfl⟩
    exact ⟨hz, v, rfl⟩

/-- **Lemma A, Lo half** (the Lo-row): at least 70 − B of the 70 Lo-states are unoccupied. -/
theorem lo_row {B n : ℕ} (n66 : OmissionZRow.N66Bound B) (c : Configuration n)
    (noCap : ¬ c.HasCap 6) (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) :
    70 - B ≤ (Lo \ c.residualOccupied noCap noOctagon noJunction).card := by
  have h1 := Finset.card_sdiff_add_card_inter Lo (c.residualOccupied noCap noOctagon noJunction)
  rw [Lo_inter_occupied, Finset.card_image_of_injective _ (c.residualOwner_injective noCap noOctagon noJunction),
    Lo_card] at h1
  have h2 := loOwners_card_le n66 c noCap noOctagon noJunction
  omega

end Res118

#print axioms Res118.Lo_eq
#print axioms Res118.F_eq
#print axioms Res118.Lo_card
#print axioms Res118.F_card
#print axioms Res118.sum_Lo_add_sum_F
#print axioms Res118.loOwners_no_cup
#print axioms Res118.loOwners_no_cap
#print axioms Res118.lo_row

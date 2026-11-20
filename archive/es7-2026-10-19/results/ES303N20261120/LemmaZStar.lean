/-
Lemma Z* (ES305N20261119 §8, 20 Nov 2026) in Lean.

Z* = the catalog states f with f(0) = 5 and f(4) ≥ 1 (70 states; `Zs_eq` pins the exact index set of
`zstar.json` / `balzs.rows`). Their owners are the points where a 6-cup and a 6-cap of the balanced set end. By
THEORY310N Lemma B (both halves) they contain no 6-cap and no 6-cup: a 6-cap (6-cup) y1 … y6 among them, together with
the 6-cup (6-cap) of the configuration that ends with an edge (u, y1), gives a 7-cup or a 7-cap, depending on the turn
(u, y1, y2). So N66 bounds them, and the Z*-row holds: 15 ≤ (Zs \ c.occupied).card.
N66 enters only as the hypothesis `N66Bound 55` (CERTIFIED by SAT in N66N20261113, not in Lean).
-/
import LemmaZ

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks
  ErdosSzekeres.Omission.BalancedCatalog ErdosSzekeres.Omission.Ferrers
  ErdosSzekeres.Omission.Subsets ErdosSzekeres.Omission.SlopePartition OmissionZRow

namespace OmissionZStarRow

/-- A catalog profile lies in Z* iff f(0) = 5 and f(4) ≥ 1. -/
def zsProfile (xs : List ℕ) : Bool := decide (xs.getD 0 0 = 5) && decide (1 ≤ xs.getD 4 0)

def Zs : Finset (Fin 252) := Finset.univ.filter (fun i => zsProfile (catalog.getD i.val []) = true)

/-- The exact support of the Z*-row in `zstar.json` / `balzs.rows`. -/
def zsIndices : List ℕ := [64,81,98,100,117,118,121,135,136,137,139,143,154,155,157,158,161,171,172,173,174,176,178,179,188,189,190,191,193,194,196,202,203,204,205,207,208,209,211,215,216,217,218,219,220,222,225,226,227,228,229,230,231,234,235,236,237,238,240,241,242,243,244,245,246,247,248,249,250,251]

theorem Zs_eq : ∀ i : Fin 252, i ∈ Zs ↔ i.val ∈ zsIndices := by
  unfold Zs; simp only [Finset.mem_filter, Finset.mem_univ, true_and]; decide +kernel

theorem Zs_card : Zs.card = 70 := by decide +kernel

/-- A positive column value is attained by an incoming edge. -/
theorem column_witness {cup : ℕ → ℕ → ℕ → Bool} {v i k : ℕ} (hk : 1 ≤ k) (h : k ≤ column cup v i) :
    ∃ u, u < v ∧ i + 1 ≤ (labels cup u v).1 ∧ k ≤ (labels cup u v).2 := by
  unfold column at h
  obtain ⟨u, hu, hle⟩ := (Finset.le_sup_iff (show (⊥ : ℕ) < k from hk)).mp h
  refine ⟨u, Finset.mem_range.mp hu, ?_⟩
  split_ifs at hle with hc
  · exact ⟨hc, hle⟩
  · omega

theorem owner_mem_Zs {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (v : Fin n) (h : c.balancedOwner noCap noCup v ∈ Zs) :
    column c.cup v 0 = 5 ∧ 1 ≤ column c.cup v 4 := by
  simp only [Zs, Finset.mem_filter, Finset.mem_univ, true_and, owner_profile c noCap noCup v, zsProfile,
    Bool.and_eq_true, decide_eq_true_eq] at h
  simpa [List.ofFn_succ] using h

/-- The owners of Z*-states. -/
noncomputable def zsOwners {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) : Finset (Fin n) :=
  Finset.univ.filter (fun v => c.balancedOwner noCap noCup v ∈ Zs)

theorem zsOwner_columns {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    {a : ℕ} (ha : a ∈ natSet (zsOwners c noCap noCup)) :
    a < n ∧ column c.cup a 0 = 5 ∧ 1 ≤ column c.cup a 4 := by
  have an := Finset.mem_range.mp (natSet_bounded _ ha)
  have hmem := (natSet_member _ ⟨a, an⟩).mp ha
  exact ⟨an, owner_mem_Zs c noCap noCup ⟨a, an⟩ (Finset.mem_filter.mp hmem).2⟩

/-- A Z*-owner ends a 6-cup of the configuration with some edge (u, a). -/
theorem six_cup_into {n : ℕ} (c : Configuration n) (noCup : ¬ c.HasCup 7) {a : ℕ} (an : a < n)
    (h0 : column c.cup a 0 = 5) : ∃ u, u < a ∧ EndingPath c.cup true u a 6 := by
  obtain ⟨u, hu, -, hl⟩ := column_witness (by norm_num) (show 5 ≤ column c.cup a 0 by omega)
  have lt := rank_lt_of_avoids n c.cup true 7 (by omega) (c.avoids_of_noCup noCup) u a hu an
  have r6 : rank c.cup true u a = 6 := by simp only [labels] at hl; omega
  exact ⟨u, hu, r6 ▸ rank_attained c.cup true u a hu⟩

/-- A Z*-owner ends a 6-cap of the configuration with some edge (u, a). -/
theorem six_cap_into {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7) {a : ℕ} (an : a < n)
    (h4 : 1 ≤ column c.cup a 4) : ∃ u, u < a ∧ EndingPath c.cup false u a 6 := by
  obtain ⟨u, hu, hl, -⟩ := column_witness (le_refl 1) h4
  have lt := rank_lt_of_avoids n c.cup false 7 (by omega) (c.avoids_of_noCap noCap) u a hu an
  have r6 : rank c.cup false u a = 6 := by simp only [labels] at hl; omega
  exact ⟨u, hu, r6 ▸ rank_attained c.cup false u a hu⟩

/-- Lemma Z*, cap half (THEORY310N Lemma B: where a 6-cup ends there is no 6-cap). -/
theorem zsOwners_no_cap {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) :
    ¬ (colorConfig c.cup true).HasNCap 6 (natSet (zsOwners c noCap noCup)) := by
  rintro ⟨xs, ⟨cap, len⟩, inside⟩
  have cupF := (false_cup_iff_cap c.cup xs).mpr cap
  obtain ⟨p1, p2, p3, p4, p5, p6, rfl⟩ := six_list len
  simp only [Config.Cup.cons3, Config.Cup.pair, colorConfig] at cupF
  obtain ⟨h12, c123, h23, c234, h34, c345, h45, c456, h56⟩ := cupF
  obtain ⟨p1n, h0, -⟩ := zsOwner_columns c noCap noCup (inside p1 (by simp))
  obtain ⟨p6n, -, -⟩ := zsOwner_columns c noCap noCup (inside p6 (by simp))
  obtain ⟨p2n, -, -⟩ := zsOwner_columns c noCap noCup (inside p2 (by simp))
  obtain ⟨u, hu, path⟩ := six_cup_into c noCup p1n h0
  cases hcol : c.cup u p1 p2
  · exact c.avoids_of_noCap noCap p5 p6 p6n
      (.step (.step (.step (.step (.step (.pair hu) h12 hcol) h23 c123) h34 c234) h45 c345) h56 c456)
  · exact c.avoids_of_noCup noCup p1 p2 p2n (.step path h12 hcol)

/-- Lemma Z*, cup half (mirror: where a 6-cap ends there is no 6-cup). -/
theorem zsOwners_no_cup {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) :
    ¬ (colorConfig c.cup true).HasNCup 6 (natSet (zsOwners c noCap noCup)) := by
  rintro ⟨xs, ⟨cup, len⟩, inside⟩
  obtain ⟨p1, p2, p3, p4, p5, p6, rfl⟩ := six_list len
  simp only [Config.Cup.cons3, Config.Cup.pair, colorConfig] at cup
  obtain ⟨h12, c123, h23, c234, h34, c345, h45, c456, h56⟩ := cup
  obtain ⟨p1n, -, h4⟩ := zsOwner_columns c noCap noCup (inside p1 (by simp))
  obtain ⟨p6n, -, -⟩ := zsOwner_columns c noCap noCup (inside p6 (by simp))
  obtain ⟨p2n, -, -⟩ := zsOwner_columns c noCap noCup (inside p2 (by simp))
  obtain ⟨u, hu, path⟩ := six_cap_into c noCap p1n h4
  cases hcol : c.cup u p1 p2
  · exact c.avoids_of_noCap noCap p1 p2 p2n (.step path h12 hcol)
  · exact c.avoids_of_noCup noCup p5 p6 p6n
      (.step (.step (.step (.step (.step (.pair hu) h12 hcol) h23 c123) h34 c234) h45 c345) h56 c456)

theorem zsOwners_card_le {n : ℕ} (n66 : N66Bound 55) (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    (zsOwners c noCap noCup).card ≤ 55 :=
  n66 _ (restrict c _) (restrict_no_cap c _ (zsOwners_no_cap c noCap noCup))
    (restrict_no_cup c _ (zsOwners_no_cup c noCap noCup)) (restrict_no_octagon c _ noOctagon)

theorem Zs_inter_occupied {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) :
    Zs ∩ c.occupied noCap noCup = (zsOwners c noCap noCup).image (c.balancedOwner noCap noCup) := by
  ext i
  simp only [Finset.mem_inter, Configuration.occupied, zsOwners, Finset.mem_image, Finset.mem_filter,
    Finset.mem_univ, true_and]
  constructor
  · rintro ⟨hz, v, rfl⟩
    exact ⟨v, hz, rfl⟩
  · rintro ⟨v, hz, rfl⟩
    exact ⟨hz, v, rfl⟩

/-- **The Z*-row** (demand 15, support Z*), in the form of `OmissionZRow.z_row`. -/
theorem zs_row {n : ℕ} (n66 : N66Bound 55) (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    15 ≤ (Zs \ c.occupied noCap noCup).card := by
  have h1 := Finset.card_sdiff_add_card_inter Zs (c.occupied noCap noCup)
  rw [Zs_inter_occupied, Finset.card_image_of_injective _ (c.balancedOwner_injective noCap noCup),
    Zs_card] at h1
  have h2 := zsOwners_card_le n66 c noCap noCup noOctagon
  omega

end OmissionZStarRow

#print axioms OmissionZStarRow.Zs_eq
#print axioms OmissionZStarRow.zs_row

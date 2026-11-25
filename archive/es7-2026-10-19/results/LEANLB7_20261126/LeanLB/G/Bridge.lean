import LeanLB.G.Sound

/-!
# The abstract checker and the repository's definitions

`LeanLB.G.lowerBound`: hypotheses
* `hop`: for points of `L`, `op a b c = true` implies `0 < orient (φ a) (φ b) (φ c)` (a certified
  positive orientation);
* `hcyc`: `op b c a = op a b c`;
* `hab`: for points of `L`, `ab p q = true` implies `hgt p < hgt q` for a map `hgt` into a linear
  order;
* `gpOK op ab L = true` and `checkAll op ab B L = true` (kernel evaluation).
Conclusion: the image of `L` has `L.length` points, is in general position and has no `B + 2` points
in convex position.
-/

namespace LeanLB.G

open ErdosSzekeres

variable {P : Type}

theorem convexSigns_of_convexPosition [DecidableEq P] {op : P → P → P → Bool} {φ : P → Point}
    (U : Finset P)
    (hop : ∀ a ∈ U, ∀ b ∈ U, ∀ c ∈ U, op a b c = true → 0 < orient (φ a) (φ b) (φ c))
    (hdec : ∀ a ∈ U, ∀ b ∈ U, ∀ c ∈ U, a ≠ b → a ≠ c → b ≠ c → (op a b c || op a c b) = true)
    (hconv : ConvexPosition (U.image φ)) : ConvexSigns op U := by
  classical
  intro p hp a ha b hb c hc h1 h2 h3
  by_contra hneg
  have o1 := hop _ hp _ ha _ hb h1
  have o2 := hop _ hp _ ha _ hc h2
  have o3 := hop _ hp _ hb _ hc h3
  have hab : a ≠ b := by rintro rfl; rw [orient_self23] at o1; exact lt_irrefl _ o1
  have hac : a ≠ c := by rintro rfl; rw [orient_self23] at o2; exact lt_irrefl _ o2
  have hbc : b ≠ c := by rintro rfl; rw [orient_self23] at o3; exact lt_irrefl _ o3
  have hd := hdec a ha b hb c hc hab hac hbc
  rw [Bool.not_eq_true] at hneg
  rw [hneg, Bool.false_or] at hd
  have o4 := hop _ ha _ hc _ hb hd
  have hpac : orient (φ p) (φ a) (φ c) ≠ 0 := o2.ne'
  have hmem : φ b ∈ convexHull ℝ ({φ p, φ a, φ c} : Set Point) := by
    rw [Suk.mem_triangle_iff_orient_products _ _ _ _ hpac]
    have q4 : 0 < orient (φ c) (φ p) (φ b) := by rw [orient_cycle, orient_cycle]; exact o3
    refine ⟨?_, ?_, ?_⟩ <;> positivity
  have hpb : φ p ≠ φ b := by
    intro h; rw [h, orient_self13] at o1; exact lt_irrefl _ o1
  have hab' : φ a ≠ φ b := by
    intro h; rw [h, orient_self23] at o1; exact lt_irrefl _ o1
  have hcb : φ c ≠ φ b := by
    intro h; rw [h, orient_self23] at o3; exact lt_irrefl _ o3
  have hsub : ({φ p, φ a, φ c} : Set Point) ⊆ ((U.image φ : Finset Point) : Set Point) \ {φ b} := by
    intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl | rfl
    · exact ⟨Finset.mem_coe.mpr (Finset.mem_image_of_mem φ hp), hpb⟩
    · exact ⟨Finset.mem_coe.mpr (Finset.mem_image_of_mem φ ha), hab'⟩
    · exact ⟨Finset.mem_coe.mpr (Finset.mem_image_of_mem φ hc), hcb⟩
  exact (convexPosition_iff _).mp hconv (φ b)
    (Finset.mem_coe.mpr (Finset.mem_image_of_mem φ hb)) (convexHull_mono hsub hmem)

theorem exists_third [DecidableEq P] {L : List P} (hnd : L.Nodup) (h3 : 3 ≤ L.length) (a b : P) :
    ∃ c ∈ L, c ≠ a ∧ c ≠ b := by
  have hcard : 3 ≤ L.toFinset.card := by rw [List.toFinset_card_of_nodup hnd]; exact h3
  have h1 : 1 ≤ ((L.toFinset.erase a).erase b).card := by
    have := Finset.pred_card_le_card_erase (s := L.toFinset.erase a) (a := b)
    have := Finset.pred_card_le_card_erase (s := L.toFinset) (a := a)
    omega
  obtain ⟨c, hc⟩ := Finset.card_pos.mp (by omega : 0 < ((L.toFinset.erase a).erase b).card)
  simp only [Finset.mem_erase, List.mem_toFinset] at hc
  exact ⟨c, hc.2.2, hc.2.1, hc.1⟩

/-- **The bridge** for the abstract checker. -/
theorem lowerBound [DecidableEq P] {H : Type} [LinearOrder H] {op : P → P → P → Bool}
    {ab : P → P → Bool} {φ : P → Point} {hgt : P → H} {L : List P}
    (hop : ∀ a ∈ L, ∀ b ∈ L, ∀ c ∈ L, op a b c = true → 0 < orient (φ a) (φ b) (φ c))
    (hcyc : ∀ a b c, op b c a = op a b c)
    (hab : ∀ p ∈ L, ∀ q ∈ L, ab p q = true → hgt p < hgt q)
    {B : ℕ} (hB : 1 ≤ B) (h3 : 3 ≤ L.length)
    (hgp : gpOK op ab L = true) (hchk : checkAll op ab B L = true) :
    ((L.map φ).toFinset).card = L.length ∧ GeneralPosition (L.map φ).toFinset ∧
      ¬ HasConvexNGon (B + 2) (L.map φ).toFinset := by
  classical
  obtain ⟨hpair, hdec⟩ := gpOK_sound hcyc L hgp
  have hnd : L.Nodup := hpair.imp_of_mem (fun {a b} ha _ h => by
    rintro rfl
    rw [Bool.or_self] at h
    exact lt_irrefl _ (hab a ha a ha h))
  have hne_orient : ∀ a ∈ L, ∀ b ∈ L, ∀ c ∈ L, a ≠ b → a ≠ c → b ≠ c →
      orient (φ a) (φ b) (φ c) ≠ 0 := by
    intro a ha b hb c hc hab' hac hbc
    have hd := hdec a ha b hb c hc hab' hac hbc
    rw [Bool.or_eq_true] at hd
    rcases hd with hd | hd
    · exact (hop _ ha _ hb _ hc hd).ne'
    · have := hop _ ha _ hc _ hb hd
      rw [orient_swap] at this
      linarith
  have hinj : ∀ x ∈ L, ∀ y ∈ L, φ x = φ y → x = y := by
    intro x hx y hy hxy
    by_contra hne
    obtain ⟨c, hc, hca, hcb⟩ := exists_third hnd h3 x y
    have h := hne_orient x hx y hy c hc hne hca.symm hcb.symm
    rw [hxy, orient_self12] at h
    exact h rfl
  refine ⟨?_, ?_, ?_⟩
  · rw [List.toFinset_card_of_nodup (hnd.map_on hinj), List.length_map]
  · rw [generalPosition_iff_orient_ne_zero]
    intro x hx y hy z hz hxy hxz hyz
    simp only [List.mem_toFinset, List.mem_map] at hx hy hz
    obtain ⟨a, ha, rfl⟩ := hx
    obtain ⟨b, hb, rfl⟩ := hy
    obtain ⟨c, hc, rfl⟩ := hz
    exact hne_orient a ha b hb c hc (fun h => hxy (h ▸ rfl)) (fun h => hxz (h ▸ rfl))
      (fun h => hyz (h ▸ rfl))
  · rintro ⟨T, hTS, hTcard, hTconv⟩
    set U : Finset P := L.toFinset.filter (fun x => φ x ∈ T) with hU
    have himg : U.image φ = T := by
      ext t
      simp only [hU, Finset.mem_image, Finset.mem_filter, List.mem_toFinset]
      constructor
      · rintro ⟨x, ⟨_, hx⟩, rfl⟩; exact hx
      · intro ht
        have := hTS ht
        simp only [List.mem_toFinset, List.mem_map] at this
        obtain ⟨x, hx, rfl⟩ := this
        exact ⟨x, ⟨hx, ht⟩, rfl⟩
    have hUL : ∀ x ∈ U, x ∈ L := fun x hx => by
      simp only [hU, Finset.mem_filter, List.mem_toFinset] at hx; exact hx.1
    have hcs : ConvexSigns op U := by
      refine convexSigns_of_convexPosition U
        (fun a ha b hb c hc => hop a (hUL a ha) b (hUL b hb) c (hUL c hc)) ?_ (himg ▸ hTconv)
      intro a ha b hb c hc hab' hac hbc
      exact hdec a (hUL a ha) b (hUL b hb) c (hUL c hc) hab' hac hbc
    have htot : ∀ p ∈ U, ∀ q ∈ U, p ≠ q → ab p q = true ∨ ab q p = true := by
      intro p hp q hq hpq
      have := hpair.forall (fun {a b} h => by rw [Bool.or_comm]; exact h) (hUL p hp) (hUL q hq) hpq
      rw [Bool.or_eq_true] at this
      exact this
    have hne : ∀ p ∈ L, ∀ a ∈ L, ∀ b ∈ L, op p a b = true → a ≠ b := by
      intro p hp a ha b hb h
      rintro rfl
      have := hop _ hp _ ha _ ha h
      rw [orient_self23] at this
      exact lt_irrefl _ this
    have hle := card_le_of_check hab hne hB hchk U hUL htot hcs
    have hge : T.card ≤ U.card := by rw [← himg]; exact Finset.card_image_le
    omega

end LeanLB.G

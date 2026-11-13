import ErdosSzekeres.Omission.ResidualCycleGeometry

/-! Finite set lemmas used to combine one-hole exclusions into a two-hole row.
No geometric configuration or total population is assumed in these lemmas. -/
namespace ErdosSzekeres.Omission

/-- If an original row cannot meet its demand outside S, it forces a hole in S. -/
theorem hole_of_card_deficit {α : Type*} [DecidableEq α]
    (R S occupied : Finset α) (d : ℕ)
    (hrow : d ≤ (R \ occupied).card) (hdef : (R \ S).card < d) :
    1 ≤ (S \ occupied).card := by
  by_contra hn
  have hz : (S \ occupied).card = 0 := by omega
  have hsub : S ⊆ occupied :=
    Finset.sdiff_eq_empty_iff_subset.mp (Finset.card_eq_zero.mp hz)
  have hle : (R \ occupied).card ≤ (R \ S).card := by
    apply Finset.card_le_card
    intro x hx
    obtain ⟨hxR, hxO⟩ := Finset.mem_sdiff.mp hx
    exact Finset.mem_sdiff.mpr ⟨hxR, fun hxS => hxO (hsub hxS)⟩
  omega

/-- Excluding full occupation of every one-point deletion forces two holes. -/
theorem two_holes_of_deletions {α : Type*} [DecidableEq α]
    (T occupied : Finset α) (hne : T.Nonempty)
    (h : ∀ p ∈ T, 1 ≤ (T.erase p \ occupied).card) :
    2 ≤ (T \ occupied).card := by
  by_contra hn
  have hle : (T \ occupied).card ≤ 1 := by omega
  obtain ⟨p, hp⟩ := hne
  obtain ⟨q, hq⟩ := Finset.card_pos.mp (show 0 < (T.erase p \ occupied).card by
    have := h p hp
    omega)
  have hqT : q ∈ T := (Finset.mem_erase.mp (Finset.mem_sdiff.mp hq).1).2
  have hqO : q ∉ occupied := (Finset.mem_sdiff.mp hq).2
  obtain ⟨r, hr⟩ := Finset.card_pos.mp (show 0 < (T.erase q \ occupied).card by
    have := h q hqT
    omega)
  have hrT : r ∈ T := (Finset.mem_erase.mp (Finset.mem_sdiff.mp hr).1).2
  have hrO : r ∉ occupied := (Finset.mem_sdiff.mp hr).2
  have heq : r = q := (Finset.card_le_one.mp hle) r
    (Finset.mem_sdiff.mpr ⟨hrT, hrO⟩) q (Finset.mem_sdiff.mpr ⟨hqT, hqO⟩)
  exact (Finset.mem_erase.mp (Finset.mem_sdiff.mp hr).1).1 heq

end ErdosSzekeres.Omission

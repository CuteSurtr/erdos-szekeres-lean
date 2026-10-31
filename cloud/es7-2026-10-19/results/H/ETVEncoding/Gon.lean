import ETVEncoding.Signotope
import Mathlib.Data.Finset.Card

/-!
# The vertex set of a gon

Let a cap `l₁` and a cup `l₂` run from `x` to `y` in a signotope. For any three vertices
`p < q < r` of the gon, the sign of `pqr` is the sign of the chain containing the middle
vertex `q` (cap: `false`, cup: `true`). Consequently every increasing quadruple
`a < b < c < d` of vertices satisfies `σabc = σabd` and `σacd = σbcd`, which is the
convex-quadrilateral sign pattern for x-sorted points. The two chains share only `x` and
`y`, so the gon has exactly `K` vertices.
-/

namespace ETV

variable {σ : Sig} {N : ℕ}

/-- The middle-vertex rule for a cap/cup pair (stated for a chain `L` of sign `t` and a chain
`L'` of sign `!t` with the same ends `x` and `y`). -/
theorem gon_middle (hσ : IsSignotope N σ) {t : Bool} {L L' : List ℕ} {x y : ℕ}
    (hL : AllTriples σ t L) (hL' : AllTriples σ (!t) L')
    (hxL : x ∈ L) (hyL : y ∈ L) (hxL' : x ∈ L') (hyL' : y ∈ L')
    (hrange : ∀ p, p ∈ L ∨ p ∈ L' → x ≤ p ∧ p ≤ y) (hN : ∀ p, p ∈ L ∨ p ∈ L' → p < N)
    {p q r : ℕ} (hp : p ∈ L ∨ p ∈ L') (hq : q ∈ L) (hr : r ∈ L ∨ r ∈ L')
    (hpq : p < q) (hqr : q < r) : σ p q r = t := by
  have hxq : x < q := lt_of_le_of_lt (hrange p hp).1 hpq
  have hqy : q < y := lt_of_lt_of_le hqr (hrange r hr).2
  have hyN : y < N := hN y (Or.inl hyL)
  have hxqy : σ x q y = t := hL x hxL q hq y hyL hxq hqy
  have hne : t ≠ !t := by cases t <;> decide
  have stepP : p ∉ L → x < p ∧ σ x p q = !t ∧ σ p q y = t := by
    intro hpL
    have hpL' : p ∈ L' := hp.resolve_left hpL
    have hxp : x < p := lt_of_le_of_ne (hrange p hp).1 (fun h => hpL (h ▸ hxL))
    have hpy : p < y := lt_trans hpq hqy
    have hxpy : σ x p y = !t := hL' x hxL' p hpL' y hyL' hxp hpy
    have pk := hσ x p q y hxp hpq hqy hyN
    have := pv_ne23 pk (by rw [hxpy, hxqy]; exact hne.symm)
    exact ⟨hxp, this.1.trans hxpy, this.2.trans hxqy⟩
  have stepR : r ∉ L → r < y ∧ σ x q r = t ∧ σ q r y = !t := by
    intro hrL
    have hrL' : r ∈ L' := hr.resolve_left hrL
    have hry : r < y := lt_of_le_of_ne (hrange r hr).2 (fun h => hrL (h ▸ hyL))
    have hxr : x < r := lt_trans hxq hqr
    have hxry : σ x r y = !t := hL' x hxL' r hrL' y hyL' hxr hry
    have pk := hσ x q r y hxq hqr hry hyN
    have := pv_ne23 pk (by rw [hxqy, hxry]; exact hne)
    exact ⟨hry, this.1.trans hxqy, this.2.trans hxry⟩
  by_cases hpL : p ∈ L <;> by_cases hrL : r ∈ L
  · exact hL p hpL q hq r hrL hpq hqr
  · obtain ⟨hry, hxqr, hqry⟩ := stepR hrL
    rcases eq_or_lt_of_le (hrange p hp).1 with hxp | hxp
    · subst hxp
      exact hxqr
    · have hpqy : σ p q y = t := hL p hpL q hq y hyL hpq hqy
      have pk := hσ p q r y hpq hqr hry hyN
      exact (pv_ne24 pk (by rw [hpqy, hqry]; exact hne)).trans hpqy
  · obtain ⟨hxp, hxpq, hpqy⟩ := stepP hpL
    rcases eq_or_lt_of_le (hrange r hr).2 with hry | hry
    · subst hry
      exact hpqy
    · have hxqr : σ x q r = t := hL x hxL q hq r hrL hxq hqr
      have pk := hσ x p q r hxp hpq hqr (hN r hr)
      exact (pv_ne13 pk (by rw [hxpq, hxqr]; exact hne.symm)).trans hxqr
  · obtain ⟨hxp, hxpq, -⟩ := stepP hpL
    obtain ⟨-, hxqr, -⟩ := stepR hrL
    have pk := hσ x p q r hxp hpq hqr (hN r hr)
    exact (pv_ne13 pk (by rw [hxpq, hxqr]; exact hne.symm)).trans hxqr

theorem range_of_pairwise {l : List ℕ} (hs : l.Pairwise (· < ·)) {x y : ℕ}
    (hx : l.head? = some x) (hy : l.getLast? = some y) : ∀ p ∈ l, x ≤ p ∧ p ≤ y := by
  intro p hp
  constructor
  · obtain ⟨ys, rfl⟩ := List.head?_eq_some_iff.1 hx
    rcases List.mem_cons.1 hp with rfl | hp
    · exact le_refl _
    · exact ((List.pairwise_cons.1 hs).1 p hp).le
  · obtain ⟨zs, hz⟩ := List.getLast?_eq_some_iff.1 hy
    rw [hz] at hs hp
    rcases List.mem_append.1 hp with hp | hp
    · exact ((List.pairwise_append.1 hs).2.2 p hp y (by simp)).le
    · simp only [List.mem_singleton] at hp
      omega

/-- **The vertices of a `K`-gon.** A `K`-gon in a signotope has a set of exactly `K` vertices
below `N`, every increasing quadruple of which has the convex sign pattern
`σabc = σabd ∧ σacd = σbcd`. -/
theorem HasGon.vertices (hσ : IsSignotope N σ) {K : ℕ} (h : HasGon σ N K) :
    ∃ G : Finset ℕ, G.card = K ∧ (∀ p ∈ G, p < N) ∧
      ∀ a ∈ G, ∀ b ∈ G, ∀ c ∈ G, ∀ d ∈ G, a < b → b < c → c < d →
        σ a b c = σ a b d ∧ σ a c d = σ b c d := by
  classical
  obtain ⟨l₁, l₂, h1, h2, hl1, hl2, hhead, hlast, hK, hN1, hN2⟩ := h
  obtain ⟨x, hx1⟩ : ∃ x, l₁.head? = some x := by
    cases l₁ with
    | nil => simp at hl1
    | cons a l => exact ⟨a, rfl⟩
  obtain ⟨y, hy1⟩ : ∃ y, l₁.getLast? = some y := by
    cases hl : l₁.getLast? with
    | none => simp [List.getLast?_eq_none_iff] at hl; simp [hl] at hl1
    | some y => exact ⟨y, rfl⟩
  have hx2 : l₂.head? = some x := hhead ▸ hx1
  have hy2 : l₂.getLast? = some y := hlast ▸ hy1
  have hs1 := h1.pairwise
  have hs2 := h2.pairwise
  have hr1 := range_of_pairwise hs1 hx1 hy1
  have hr2 := range_of_pairwise hs2 hx2 hy2
  have hxl1 : x ∈ l₁ := List.mem_of_mem_head? hx1
  have hxl2 : x ∈ l₂ := List.mem_of_mem_head? hx2
  have hyl1 : y ∈ l₁ := List.mem_of_mem_getLast? hy1
  have hyl2 : y ∈ l₂ := List.mem_of_mem_getLast? hy2
  have hA1 := h1.allTriples hσ hN1
  have hA2 := h2.allTriples hσ hN2
  have hrange : ∀ p, p ∈ l₁ ∨ p ∈ l₂ → x ≤ p ∧ p ≤ y := by
    rintro p (hp | hp)
    · exact hr1 p hp
    · exact hr2 p hp
  have hN : ∀ p, p ∈ l₁ ∨ p ∈ l₂ → p < N := by
    rintro p (hp | hp)
    · exact hN1 p hp
    · exact hN2 p hp
  have hrange' : ∀ p, p ∈ l₂ ∨ p ∈ l₁ → x ≤ p ∧ p ≤ y := fun p hp => hrange p hp.symm
  have hN' : ∀ p, p ∈ l₂ ∨ p ∈ l₁ → p < N := fun p hp => hN p hp.symm
  -- the middle-vertex rule for both chains
  have mid : ∀ p q r, p ∈ l₁ ∨ p ∈ l₂ → q ∈ l₁ ∨ q ∈ l₂ → r ∈ l₁ ∨ r ∈ l₂ → p < q → q < r →
      σ p q r = !(decide (q ∈ l₁)) := by
    intro p q r hp hq hr hpq hqr
    by_cases hq1 : q ∈ l₁
    · rw [decide_eq_true hq1]
      exact gon_middle (t := false) hσ hA1 hA2 hxl1 hyl1 hxl2 hyl2 hrange hN hp hq1 hr hpq hqr
    · rw [decide_eq_false hq1]
      exact gon_middle (t := true) hσ hA2 hA1 hxl2 hyl2 hxl1 hyl1 hrange' hN' hp.symm
        (hq.resolve_left hq1) hr.symm hpq hqr
  -- the two chains share only the ends
  have hnd1 : l₁.Nodup := hs1.imp (fun h => ne_of_lt h)
  have hnd2 : l₂.Nodup := hs2.imp (fun h => ne_of_lt h)
  have hxy : x < y := by
    rcases eq_or_lt_of_le (hr1 x hxl1).2 with hxy | hxy
    · exfalso
      have hsub : l₁.toFinset ⊆ {x} := by
        intro p hp
        rw [List.mem_toFinset] at hp
        have := hr1 p hp
        rw [Finset.mem_singleton]
        omega
      have := Finset.card_le_card hsub
      rw [List.toFinset_card_of_nodup hnd1, Finset.card_singleton] at this
      omega
    · exact hxy
  have hinter : l₁.toFinset ∩ l₂.toFinset = {x, y} := by
    ext q
    simp only [Finset.mem_inter, List.mem_toFinset, Finset.mem_insert, Finset.mem_singleton]
    constructor
    · rintro ⟨hq1, hq2⟩
      by_contra hne
      push_neg at hne
      have hxq : x < q := lt_of_le_of_ne (hr1 q hq1).1 (Ne.symm hne.1)
      have hqy : q < y := lt_of_le_of_ne (hr1 q hq1).2 hne.2
      have e1 := hA1 x hxl1 q hq1 y hyl1 hxq hqy
      have e2 := hA2 x hxl2 q hq2 y hyl2 hxq hqy
      rw [e1] at e2
      exact Bool.false_ne_true e2
    · rintro (rfl | rfl)
      · exact ⟨hxl1, hxl2⟩
      · exact ⟨hyl1, hyl2⟩
  refine ⟨l₁.toFinset ∪ l₂.toFinset, ?_, ?_, ?_⟩
  · have h := Finset.card_union_add_card_inter l₁.toFinset l₂.toFinset
    rw [hinter, Finset.card_pair (ne_of_lt hxy), List.toFinset_card_of_nodup hnd1,
      List.toFinset_card_of_nodup hnd2] at h
    omega
  · intro p hp
    simp only [Finset.mem_union, List.mem_toFinset] at hp
    exact hN p hp
  · intro a ha b hb c hc d hd hab hbc hcd
    simp only [Finset.mem_union, List.mem_toFinset] at ha hb hc hd
    exact ⟨(mid a b c ha hb hc hab hbc).trans (mid a b d ha hb hd hab (lt_trans hbc hcd)).symm,
      (mid a c d ha hc hd (lt_trans hab hbc) hcd).trans (mid b c d hb hc hd hbc hcd).symm⟩

end ETV

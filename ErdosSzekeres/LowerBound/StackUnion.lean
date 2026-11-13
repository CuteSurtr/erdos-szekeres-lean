import ErdosSzekeres.LowerBound.Defs

/-! Disjointness, cardinality, distinct abscissae and general position of a
stacked union. Mixed triples are nondegenerate because their orientation signs
are prescribed. -/

namespace ErdosSzekeres.LowerBound

variable {σ : ℝ} {A B : Finset Point}

theorem Stacked.disjoint (h : Stacked σ A B) : Disjoint A B :=
  Finset.disjoint_left.2 fun x hxA hxB => lt_irrefl _ (h.left_lt x hxA x hxB)

theorem Stacked.card_union (h : Stacked σ A B) : (A ∪ B).card = A.card + B.card :=
  Finset.card_union_of_disjoint h.disjoint

theorem Stacked.distinctX_union (h : Stacked σ A B) (hA : DistinctX A) (hB : DistinctX B) :
    DistinctX (A ∪ B) := by
  intro p hp q hq hpq
  rw [Finset.mem_coe, Finset.mem_union] at hp hq
  rcases hp with hp | hp <;> rcases hq with hq | hq
  · exact hA hp hq hpq
  · exact absurd hpq (h.left_lt p hp q hq).ne
  · exact absurd hpq (h.left_lt q hq p hp).ne'
  · exact hB hp hq hpq

/-- With distinct abscissae, nondegeneracy of all triples follows from nondegeneracy of
the horizontally sorted ones, since permuting a triple only changes the orientation's sign. -/
private theorem orient_ne_zero_of_sorted {s : Finset Point} (hs : DistinctX s)
    (key : ∀ x ∈ s, ∀ y ∈ s, ∀ z ∈ s, x 0 < y 0 → y 0 < z 0 → orient x y z ≠ 0) :
    ∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s, a ≠ b → a ≠ c → b ≠ c → orient a b c ≠ 0 := by
  intro a ha b hb c hc hab hac hbc h0
  have hx : ∀ {p q : Point}, p ∈ s → q ∈ s → p ≠ q → p 0 ≠ q 0 :=
    fun hp hq hpq e => hpq (hs hp hq e)
  have := orient_cycle a b c
  have := orient_cycle b c a
  have := orient_swap a b c
  have := orient_swap b c a
  have := orient_swap c a b
  rcases lt_or_gt_of_ne (hx ha hb hab) with h1 | h1 <;>
    rcases lt_or_gt_of_ne (hx ha hc hac) with h2 | h2 <;>
    rcases lt_or_gt_of_ne (hx hb hc hbc) with h3 | h3
  all_goals first
    | linarith
    | exact key a ha b hb c hc ‹_› ‹_› (by linarith)
    | exact key a ha c hc b hb ‹_› ‹_› (by linarith)
    | exact key b hb a ha c hc ‹_› ‹_› (by linarith)
    | exact key b hb c hc a ha ‹_› ‹_› (by linarith)
    | exact key c hc a ha b hb ‹_› ‹_› (by linarith)
    | exact key c hc b hb a ha ‹_› ‹_› (by linarith)

theorem Stacked.generalPosition_union (h : Stacked σ A B)
    (hA : GeneralPosition A) (hB : GeneralPosition B)
    (hAx : DistinctX A) (hBx : DistinctX B) :
    GeneralPosition (A ∪ B) := by
  rw [generalPosition_iff_orient_ne_zero] at hA hB ⊢
  refine orient_ne_zero_of_sorted (h.distinctX_union hAx hBx) ?_
  intro x hx y hy z hz hxy hyz
  have hne : ∀ {p q : Point}, p 0 < q 0 → p ≠ q := by rintro p q hpq rfl; exact lt_irrefl _ hpq
  rw [Finset.mem_union] at hx hy hz
  rcases hx with hx | hx <;> rcases hy with hy | hy <;> rcases hz with hz | hz
  · exact hA x hx y hy z hz (hne hxy) (hne (hxy.trans hyz)) (hne hyz)
  · exact right_ne_zero_of_mul (h.pair_left x hx y hy z hz hxy).ne'
  · exact absurd (h.left_lt z hz y hy) (lt_asymm hyz)
  · exact right_ne_zero_of_mul (h.pair_right x hx y hy z hz hyz).ne
  · exact absurd (h.left_lt y hy x hx) (lt_asymm hxy)
  · exact absurd (h.left_lt y hy x hx) (lt_asymm hxy)
  · exact absurd (h.left_lt z hz x hx) (lt_asymm (hxy.trans hyz))
  · exact hB x hx y hy z hz (hne hxy) (hne (hxy.trans hyz)) (hne hyz)

end ErdosSzekeres.LowerBound

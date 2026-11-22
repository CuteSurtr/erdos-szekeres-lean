import RowEnc.Enc

/-!
# RowGeo.Members: what the enumerations of the generator produce (core only)

Soundness needs only that every tuple the loops produce has distinct indices below the support size (and, for the
octagon clauses, that `combs 4 eight` contains every increasing 4-subset of the 8-list). Completeness or order of
the enumerations is never used (byte identity checks them).
-/

namespace RowGeo
open RowEnc

theorem mem_combs : ∀ {k : Nat} {l t : List Nat}, t ∈ combs k l → t.Sublist l ∧ t.length = k
  | 0, l, t, h => by
    simp only [combs, List.mem_cons, List.not_mem_nil, or_false] at h
    subst h; exact ⟨List.nil_sublist _, rfl⟩
  | k + 1, [], t, h => by simp [combs] at h
  | k + 1, x :: xs, t, h => by
    simp only [combs, List.mem_append, List.mem_map] at h
    rcases h with ⟨t', ht', rfl⟩ | h
    · obtain ⟨h1, h2⟩ := mem_combs ht'
      exact ⟨h1.cons₂ x, by simp [h2]⟩
    · obtain ⟨h1, h2⟩ := mem_combs h
      exact ⟨h1.cons x, h2⟩

theorem combs_of_sublist : ∀ {k : Nat} {l t : List Nat}, t.Sublist l → t.length = k → t ∈ combs k l
  | 0, l, t, _, hl => by
    rw [List.length_eq_zero_iff] at hl; subst hl; simp [combs]
  | k + 1, [], t, hs, hl => by
    rw [List.sublist_nil] at hs; subst hs; simp at hl
  | k + 1, x :: xs, t, hs, hl => by
    simp only [combs, List.mem_append, List.mem_map]
    cases hs with
    | cons _ h => exact Or.inr (combs_of_sublist h hl)
    | cons₂ _ h => exact Or.inl ⟨_, combs_of_sublist h (by simpa using hl), rfl⟩

theorem sub_range {n : Nat} {t : List Nat} (h : t.Sublist (List.range n)) :
    t.Pairwise (· < ·) ∧ ∀ x ∈ t, x < n :=
  ⟨List.Pairwise.sublist h List.pairwise_lt_range, fun x hx => List.mem_range.1 (h.subset hx)⟩

theorem range_facts {n k : Nat} {t : List Nat} (h : t ∈ combs k (List.range n)) :
    t.Pairwise (· < ·) ∧ (∀ x ∈ t, x < n) ∧ t.length = k :=
  ⟨(sub_range (mem_combs h).1).1, (sub_range (mem_combs h).1).2, (mem_combs h).2⟩

theorem pair_facts {n i j : Nat} (h : [i, j] ∈ combs 2 (List.range n)) : i < j ∧ j < n := by
  obtain ⟨hp, hm, -⟩ := range_facts h
  simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false, forall_eq,
    List.Pairwise.nil, and_true, false_implies, implies_true] at hp
  exact ⟨hp, hm j (by simp)⟩

theorem triple_facts {n i j l : Nat} (h : [i, j, l] ∈ combs 3 (List.range n)) : i < j ∧ j < l ∧ l < n := by
  obtain ⟨hp, hm, -⟩ := range_facts h
  simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq,
    List.Pairwise.nil, and_true, false_implies, implies_true] at hp
  exact ⟨hp.1.1, hp.2, hm l (by simp)⟩

theorem quad_facts {n a b c d : Nat} (h : [a, b, c, d] ∈ combs 4 (List.range n)) :
    a < b ∧ b < c ∧ c < d ∧ d < n := by
  obtain ⟨hp, hm, -⟩ := range_facts h
  simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq,
    List.Pairwise.nil, and_true, false_implies, implies_true] at hp
  exact ⟨hp.1.1, hp.2.1.1, hp.2.2, hm d (by simp)⟩

theorem perm3_facts {n a b c : Nat} (h : (a, b, c) ∈ perm3 n) :
    a < n ∧ b < n ∧ c < n ∧ a ≠ b ∧ a ≠ c ∧ b ≠ c := by
  simp only [perm3, List.mem_flatMap, List.mem_filter, List.mem_map, List.mem_range, Prod.mk.injEq,
    bne_iff_ne, ne_eq, Bool.and_eq_true] at h
  obtain ⟨a', ha, b', ⟨hb, hba⟩, c', ⟨hc, hca, hcb⟩, rfl, rfl, rfl⟩ := h
  exact ⟨ha, hb, hc, fun e => hba e.symm, fun e => hca e.symm, fun e => hcb e.symm⟩

theorem perm4_facts {a b c d : Nat} (hab : a < b) (hbc : b < c) (hcd : c < d) {q : Nat × Nat × Nat × Nat}
    (h : q ∈ perm4 a b c d) :
    q.1 ≠ q.2.1 ∧ q.1 ≠ q.2.2.1 ∧ q.1 ≠ q.2.2.2 ∧ q.2.1 ≠ q.2.2.1 ∧ q.2.1 ≠ q.2.2.2 ∧ q.2.2.1 ≠ q.2.2.2 ∧
      q.1 ≤ d ∧ q.2.1 ≤ d ∧ q.2.2.1 ≤ d ∧ q.2.2.2 ≤ d := by
  simp only [perm4, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl|rfl <;>
    simp only <;> omega

/-- An increasing list of members of an increasing list is a sublist of it. -/
theorem sublist_of_sorted : ∀ {l t : List Nat}, l.Pairwise (· < ·) → t.Pairwise (· < ·) → (∀ x ∈ t, x ∈ l) →
    t.Sublist l
  | [], t, _, _, h => by
    cases t with
    | nil => exact List.Sublist.slnil
    | cons x _ => exact absurd (h x List.mem_cons_self) (by simp)
  | y :: ys, [], _, _, _ => List.nil_sublist _
  | y :: ys, x :: ts, hl, ht, h => by
    rw [List.pairwise_cons] at hl ht
    by_cases hxy : x = y
    · subst hxy
      refine (sublist_of_sorted hl.2 ht.2 fun z hz => ?_).cons₂ x
      rcases List.mem_cons.1 (h z (List.mem_cons_of_mem _ hz)) with rfl | hz'
      · exact absurd (ht.1 _ hz) (Nat.lt_irrefl _)
      · exact hz'
    · have hx : x ∈ ys := by
        rcases List.mem_cons.1 (h x List.mem_cons_self) with e | e
        · exact absurd e hxy
        · exact e
      refine (sublist_of_sorted hl.2 (List.pairwise_cons.2 ht) fun z hz => ?_).cons y
      rcases List.mem_cons.1 (h z hz) with rfl | hz'
      · rcases List.mem_cons.1 hz with rfl | hz
        · exact absurd rfl hxy
        · exact absurd (Nat.lt_trans (hl.1 _ hx) (ht.1 _ hz)) (Nat.lt_irrefl _)
      · exact hz'

end RowGeo

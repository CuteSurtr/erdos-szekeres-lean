import D3Encoding.Clauses

/-!
# The triple variables

For a sign function `χ` on triples that is alternating and equivariant under the six maps of
`group t`, the table `triples t` assigns to every increasing triple `(x, y, z)` with
`z < 3 t + 1` a variable `v ≥ 1` and a sign `s = ±1` such that `s · χ(x, y, z)` only
depends on `v`. So `ν v := (s · χ(x, y, z) = 1)` is well defined, and the DIMACS literal
`lit tv a b c` is true under `ν` exactly when `χ(a, b, c) = 1`.
-/

namespace D3

/-! ### `combs` -/

theorem mem_combs {L : List Nat} {k : Nat} {l : List Nat} :
    l ∈ combs L k ↔ l.Sublist L ∧ l.length = k := by
  induction L generalizing k l with
  | nil =>
    cases k with
    | zero => simp [combs]
    | succ k =>
      simp only [combs, List.not_mem_nil, false_iff, not_and]
      intro h; rw [List.sublist_nil.1 h]; simp
  | cons x xs ih =>
    cases k with
    | zero =>
      simp only [combs, List.mem_singleton]
      constructor
      · rintro rfl; simp
      · rintro ⟨-, h⟩; exact List.length_eq_zero_iff.1 h
    | succ k =>
      simp only [combs, List.mem_append, List.mem_map, ih, List.sublist_cons_iff]
      constructor
      · rintro (⟨r, ⟨hr, hl⟩, rfl⟩ | ⟨hs, hl⟩)
        · exact ⟨Or.inr ⟨r, rfl, hr⟩, by simp [hl]⟩
        · exact ⟨Or.inl hs, hl⟩
      · rintro ⟨(hs | ⟨r, rfl, hr⟩), hl⟩
        · exact Or.inr ⟨hs, hl⟩
        · exact Or.inl ⟨r, ⟨hr, by simpa using hl⟩, rfl⟩

theorem sublist_range'_of_pairwise :
    ∀ (m lo : Nat) (l : List Nat), l.Pairwise (· < ·) → (∀ x ∈ l, lo ≤ x ∧ x < lo + m) →
      l.Sublist (List.range' lo m)
  | 0, lo, [], _, _ => by simp
  | 0, lo, x :: _, _, h => by have := h x (by simp); omega
  | m + 1, lo, l, hp, h => by
    rw [List.range'_succ]
    cases l with
    | nil => simp
    | cons y l =>
      rw [List.pairwise_cons] at hp
      by_cases hy : y = lo
      · subst hy
        refine List.Sublist.cons₂ _ (sublist_range'_of_pairwise m (y + 1) l hp.2 ?_)
        intro x hx
        have h1 := hp.1 x hx
        have h2 := h x (by simp [hx])
        omega
      · refine List.Sublist.cons _ (sublist_range'_of_pairwise m (lo + 1) (y :: l)
          (List.pairwise_cons.2 hp) ?_)
        intro x hx
        have h2 := h x hx
        rcases List.mem_cons.1 hx with rfl | hx
        · omega
        · have h1 := hp.1 x hx
          have h3 := h y (by simp)
          omega

/-- Increasing lists of numbers below `n` are exactly the sublists of `range n`. -/
theorem sublist_range_iff {n : Nat} {l : List Nat} :
    l.Sublist (List.range n) ↔ l.Pairwise (· < ·) ∧ ∀ x ∈ l, x < n := by
  constructor
  · intro h
    refine ⟨List.Pairwise.sublist h List.pairwise_lt_range, fun x hx => ?_⟩
    exact List.mem_range.1 (h.subset hx)
  · rintro ⟨hp, hl⟩
    rw [List.range_eq_range']
    exact sublist_range'_of_pairwise n 0 l hp (fun x hx => ⟨Nat.zero_le _, by simpa using hl x hx⟩)

theorem mem_combs_range {n k : Nat} {l : List Nat} :
    l ∈ combs (List.range n) k ↔ l.Pairwise (· < ·) ∧ (∀ x ∈ l, x < n) ∧ l.length = k := by
  rw [mem_combs, sublist_range_iff, and_assoc]

theorem mem_combs3 {n : Nat} {l : List Nat} :
    l ∈ combs (List.range n) 3 ↔ ∃ a b c, l = [a, b, c] ∧ a < b ∧ b < c ∧ c < n := by
  rw [mem_combs_range]
  constructor
  · rintro ⟨hp, hl, hlen⟩
    match l, hlen with
    | [a, b, c], _ =>
      simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false,
        forall_eq_or_imp, forall_eq, List.Pairwise.nil] at hp hl
      exact ⟨a, b, c, rfl, hp.1.1, hp.2.1, hl.2.2⟩
  · rintro ⟨a, b, c, rfl, h1, h2, h3⟩
    refine ⟨?_, ?_, rfl⟩ <;> simp <;> omega

/-! ### Chirotopes -/

/-- A valid key of the triple table. -/
def ValidT (P : Nat) (S : Nat × Nat × Nat) : Prop := S.1 < S.2.1 ∧ S.2.1 < S.2.2 ∧ S.2.2 < P

def chiT (χ : Nat → Nat → Nat → Int) (S : Nat × Nat × Nat) : Int := χ S.1 S.2.1 S.2.2

/-- The combinatorial hypotheses on `χ` used by the triple table: alternating, `±1` on
distinct points below `P = 3 t + 1`, and equivariant under the six maps of `group t`. -/
structure Chirotope (t : Nat) (χ : Nat → Nat → Nat → Int) : Prop where
  swap12 : ∀ a b c, χ b a c = -χ a b c
  swap23 : ∀ a b c, χ a c b = -χ a b c
  sign : ∀ a b c, a < 3 * t + 1 → b < 3 * t + 1 → c < 3 * t + 1 → a ≠ b → a ≠ c → b ≠ c →
    χ a b c = 1 ∨ χ a b c = -1
  equiv : ∀ g ∈ group t, ∀ a b c, a < 3 * t + 1 → b < 3 * t + 1 → c < 3 * t + 1 →
    χ (g.1 a) (g.1 b) (g.1 c) = g.2 * χ a b c

theorem rot_lt {t k i : Nat} (h : i < 3 * t + 1) : rot (3 * t) k i < 3 * t + 1 := by
  unfold rot; split <;> omega

theorem rot_lt' {t k i : Nat} (h : i < 3 * t) : rot (3 * t) k i < 3 * t := by
  unfold rot; split <;> omega

theorem rot_inj {t k i j : Nat} (hi : i < 3 * t + 1) (hj : j < 3 * t + 1)
    (h : rot (3 * t) k i = rot (3 * t) k j) : i = j := by
  unfold rot at h; split at h <;> split at h <;> omega

theorem sigma_lt {t i : Nat} (h : i < 3 * t + 1) : sigma t (3 * t) i < 3 * t + 1 := by
  unfold sigma; split
  · omega
  · split <;> omega

theorem sigma_lt' {t i : Nat} (h : i < 3 * t) : sigma t (3 * t) i < 3 * t := by
  unfold sigma; split
  · omega
  · split <;> omega

theorem sigma_inj {t i j : Nat} (hi : i < 3 * t + 1) (hj : j < 3 * t + 1)
    (h : sigma t (3 * t) i = sigma t (3 * t) j) : i = j := by
  unfold sigma at h
  split at h <;> split at h <;> (try split at h) <;> (try split at h) <;> omega

/-- The maps of `group t` are injective on `0, …, 3 t` and preserve it (and the set
points `0, …, 3 t - 1`). -/
theorem group_perm {t : Nat} : ∀ g ∈ group t,
    (∀ i, i < 3 * t + 1 → g.1 i < 3 * t + 1) ∧ (∀ i, i < 3 * t → g.1 i < 3 * t) ∧
    (∀ i j, i < 3 * t + 1 → j < 3 * t + 1 → g.1 i = g.1 j → i = j) ∧ (g.2 = 1 ∨ g.2 = -1) := by
  intro g hg
  simp only [group, List.mem_cons, List.not_mem_nil, or_false] at hg
  rcases hg with rfl | rfl | rfl | rfl | rfl | rfl <;> refine ⟨?_, ?_, ?_, by simp⟩
  all_goals first
    | exact fun i hi => rot_lt hi
    | exact fun i hi => rot_lt' hi
    | exact fun i j hi hj h => rot_inj hi hj h
    | exact fun i hi => rot_lt (sigma_lt hi)
    | exact fun i hi => rot_lt' (sigma_lt' hi)
    | exact fun i j hi hj h => sigma_inj hi hj (rot_inj (sigma_lt hi) (sigma_lt hj) h)

theorem paritySort_spec {P : Nat} {a b c : Nat} (ha : a < P) (hb : b < P) (hc : c < P)
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) :
    ValidT P (paritySort a b c).1 ∧ ((paritySort a b c).2 = 1 ∨ (paritySort a b c).2 = -1) ∧
      ∀ χ : Nat → Nat → Nat → Int, (∀ a b c, χ b a c = -χ a b c) →
        (∀ a b c, χ a c b = -χ a b c) →
        χ a b c = (paritySort a b c).2 * chiT χ (paritySort a b c).1 := by
  by_cases h1 : a < b <;> by_cases h2 : b < c <;> by_cases h3 : a < c <;>
    simp only [paritySort, h1, h2, h3, if_true, if_false, ValidT, chiT, true_and, and_true] <;>
    refine ⟨by omega, by simp, fun χ h12 h23 => ?_⟩ <;>
    have := h12 a b c <;> have := h23 a b c <;> have := h12 a c b <;> have := h23 b a c <;>
    have := h12 b c a <;> omega

end D3

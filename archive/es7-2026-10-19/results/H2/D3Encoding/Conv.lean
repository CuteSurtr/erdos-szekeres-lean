import D3Encoding.Canon

/-!
# Convexity in the chirotope

`Ins χ x p q r`: `x` lies inside the triangle `p q r` (the three orientations `pqx`, `qrx`,
`rpx` agree). `ConvAll χ X`: no point of `X` lies inside a triangle of three others, i.e.
`X` is in convex position. Both are invariant under the six maps (the reflections flip all
signs, which preserves `Ins`).
-/

namespace D3

def Ins (χ : Nat → Nat → Nat → Int) (x p q r : Nat) : Prop :=
  χ p q x = χ q r x ∧ χ q r x = χ r p x

/-- No point of `X` lies inside a triangle of three other points of `X` (the triangle is
written with increasing labels; `ins_sort` shows that the order does not matter). -/
def ConvAll (χ : Nat → Nat → Nat → Int) (X : List Nat) : Prop :=
  ∀ x ∈ X, ∀ p ∈ X, ∀ q ∈ X, ∀ r ∈ X, x ≠ p → x ≠ q → x ≠ r → p < q → q < r →
    ¬Ins χ x p q r

section
variable {t : Nat} {χ : Nat → Nat → Nat → Int}

theorem ins_cyc {x p q r : Nat} (h : Ins χ x p q r) : Ins χ x q r p := by
  unfold Ins at *; omega

theorem ins_swap (hχ : Chirotope t χ) {x p q r : Nat} (h : Ins χ x p q r) : Ins χ x q p r := by
  unfold Ins at *
  rw [hχ.swap12 p q x, hχ.swap12 r p x, hχ.swap12 q r x]
  omega

/-- A triangle containing `x` can be relabelled increasingly. -/
theorem ins_sort (hχ : Chirotope t χ) {x p q r : Nat} (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r)
    (h : Ins χ x p q r) : ∃ p' q' r', p' ∈ [p, q, r] ∧ q' ∈ [p, q, r] ∧ r' ∈ [p, q, r] ∧
      p' < q' ∧ q' < r' ∧ Ins χ x p' q' r' := by
  rcases Nat.lt_or_gt_of_ne hpq with h1 | h1 <;> rcases Nat.lt_or_gt_of_ne hpr with h2 | h2 <;>
    rcases Nat.lt_or_gt_of_ne hqr with h3 | h3
  · exact ⟨p, q, r, by simp, by simp, by simp, h1, h3, h⟩
  · exact ⟨p, r, q, by simp, by simp, by simp, h2, h3, ins_cyc (ins_swap hχ h)⟩
  · omega
  · exact ⟨r, p, q, by simp, by simp, by simp, h2, h1, ins_cyc (ins_cyc h)⟩
  · exact ⟨q, p, r, by simp, by simp, by simp, h1, h2, ins_swap hχ h⟩
  · omega
  · exact ⟨q, r, p, by simp, by simp, by simp, h3, h2, ins_cyc h⟩
  · exact ⟨r, q, p, by simp, by simp, by simp, h3, h1, ins_swap hχ (ins_cyc h)⟩

theorem ins_image (hχ : Chirotope t χ) {g : (Nat → Nat) × Int} (hg : g ∈ group t)
    {x p q r : Nat} (hx : x < 3 * t + 1) (hp : p < 3 * t + 1) (hq : q < 3 * t + 1)
    (hr : r < 3 * t + 1) : Ins χ (g.1 x) (g.1 p) (g.1 q) (g.1 r) ↔ Ins χ x p q r := by
  unfold Ins
  rw [hχ.equiv g hg _ _ _ hp hq hx, hχ.equiv g hg _ _ _ hq hr hx, hχ.equiv g hg _ _ _ hr hp hx]
  obtain ⟨-, -, -, hs⟩ := group_perm g hg
  rcases hs with h | h <;> rw [h] <;> omega

/-- `ConvAll` of an image gives `ConvAll` of the set. -/
theorem convAll_of_image (hχ : Chirotope t χ) {g : (Nat → Nat) × Int} (hg : g ∈ group t)
    {X : List Nat} (hX : ∀ x ∈ X, x < 3 * t + 1) (h : ConvAll χ (sortL (X.map g.1))) :
    ConvAll χ X := by
  obtain ⟨-, -, hinj, -⟩ := group_perm g hg
  intro x hx p hp q hq r hr h1 h2 h3 h4 h5 hins
  have m : ∀ y ∈ X, g.1 y ∈ sortL (X.map g.1) := fun y hy =>
    mem_sortL.2 (List.mem_map_of_mem hy)
  have ne : ∀ a ∈ X, ∀ b ∈ X, a ≠ b → g.1 a ≠ g.1 b := fun a ha b hb hab e =>
    hab (hinj a b (hX a ha) (hX b hb) e)
  have hins' := (ins_image hχ hg (hX x hx) (hX p hp) (hX q hq) (hX r hr)).2 hins
  obtain ⟨p', q', r', hp', hq', hr', l1, l2, hI⟩ := ins_sort hχ (ne p hp q hq (by omega))
    (ne p hp r hr (by omega)) (ne q hq r hr (by omega)) hins'
  have mem3 : ∀ y ∈ [g.1 p, g.1 q, g.1 r], y ∈ sortL (X.map g.1) ∧ g.1 x ≠ y := by
    intro y hy
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hy
    rcases hy with rfl | rfl | rfl
    · exact ⟨m p hp, ne x hx p hp h1⟩
    · exact ⟨m q hq, ne x hx q hq h2⟩
    · exact ⟨m r hr, ne x hx r hr h3⟩
  exact h _ (m x hx) _ (mem3 p' hp').1 _ (mem3 q' hq').1 _ (mem3 r' hr').1 (mem3 p' hp').2
    (mem3 q' hq').2 (mem3 r' hr').2 l1 l2 hI

/-- `ConvAll` of `canon Y` gives `ConvAll Y`. -/
theorem convAll_of_canon (hχ : Chirotope t χ) {Y : List Nat} (hY : Y.Pairwise (· < ·))
    (hYP : ∀ y ∈ Y, y < 3 * t + 1) (h : ConvAll χ (canon t Y)) : ConvAll χ Y := by
  obtain ⟨hm, -⟩ := canon_spec hY hYP
  obtain ⟨g, hg, he⟩ := image_of_mem_orbit hm
  rw [he] at h
  exact convAll_of_image hχ hg hYP h

theorem length_le_of_nodup_subset : ∀ {l m : List Nat}, l.Nodup → (∀ y ∈ l, y ∈ m) →
    l.length ≤ m.length
  | [], _, _, _ => Nat.zero_le _
  | a :: l, m, hnd, hs => by
    have ha : a ∈ m := hs a (by simp)
    rw [List.nodup_cons] at hnd
    have := length_le_of_nodup_subset hnd.2 (m := m.erase a) fun y hy =>
      (List.mem_erase_of_ne (fun e => by subst e; exact hnd.1 hy)).2 (hs y (by simp [hy]))
    rw [List.length_erase_of_mem ha] at this
    have := List.length_pos_of_mem ha
    simp only [List.length_cons]
    omega

/-- If every `S ∖ Sᵢ` is convex and `|S| ≥ 5`, then `S` is convex. -/
theorem convAll_of_erase {S : List Nat} (hS : S.Nodup) (hlen : 5 ≤ S.length)
    (h : ∀ i, i < S.length → ConvAll χ (S.eraseIdx i)) : ConvAll χ S := by
  intro x hx p hp q hq r hr h1 h2 h3 h4 h5
  have : ∃ y ∈ S, y ∉ [x, p, q, r] := by
    refine Classical.byContradiction fun hn => ?_
    have hsub : ∀ y ∈ S, y ∈ [x, p, q, r] := fun y hy =>
      Classical.byContradiction fun hy' => hn ⟨y, hy, hy'⟩
    have := length_le_of_nodup_subset hS hsub
    simp at this
    omega
  obtain ⟨y, hy, hyn⟩ := this
  simp only [List.mem_cons, List.not_mem_nil, or_false, not_or] at hyn
  obtain ⟨i, hi, rfl⟩ := List.getElem_of_mem hy
  have mem : ∀ z ∈ S, z ≠ S[i] → z ∈ S.eraseIdx i := by
    intro z hz hne
    obtain ⟨j, hj, rfl⟩ := List.getElem_of_mem hz
    exact List.mem_eraseIdx_iff_getElem.2 ⟨j, hj, fun e => hne (by subst e; rfl), rfl⟩
  exact h i hi x (mem x hx (Ne.symm hyn.1)) p (mem p hp (Ne.symm hyn.2.1))
    q (mem q hq (Ne.symm hyn.2.2.1)) r (mem r hr (Ne.symm hyn.2.2.2)) h1 h2 h3 h4 h5

/-- The six labelled patterns are convex. -/
theorem convAll_of_pattern (hχ : Chirotope t χ) {a b c d : Nat} (hab : a < b) (hbc : b < c)
    (hcd : c < d) (pat : List Int) (hpat : pat ∈ convexPatterns)
    (h : [χ a b c, χ a b d, χ a c d, χ b c d] = pat) : ConvAll χ [a, b, c, d] := by
  have s12 := hχ.swap12
  have s23 := hχ.swap23
  have F : ¬Ins χ d a b c ∧ ¬Ins χ c a b d ∧ ¬Ins χ b a c d ∧ ¬Ins χ a b c d := by
    unfold Ins
    have e1 := s12 a c d
    have e2 := s12 a c b
    have e3 := s23 a b c
    have e4 := s12 a d b
    have e5 := s23 a b d
    have e6 := s12 b d c
    have e7 := s23 b c d
    have e8 := s12 b d a
    have e9 := s23 b a d
    have e10 := s12 a b d
    have e11 := s12 a c b
    have e12 := s12 c d a
    have e13 := s23 c a d
    have e14 := s12 a c d
    have e15 := s12 b c a
    have e16 := s23 b a c
    have e17 := s12 a b c
    have e18 := s12 a d c
    have e19 := s23 a c d
    have e20 := s23 c b d
    have e21 := s12 b c d
    simp only [convexPatterns, List.mem_cons, List.not_mem_nil, or_false] at hpat
    rcases hpat with rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp only [List.cons.injEq, and_true] at h <;> omega
  obtain ⟨F1, F2, F3, F4⟩ := F
  intro x hx p hp q hq r hr n1 n2 n3 n4 n5
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hx hp hq hr
  rcases hx with rfl | rfl | rfl | rfl <;> rcases hp with rfl | rfl | rfl | rfl <;>
    rcases hq with rfl | rfl | rfl | rfl <;> rcases hr with rfl | rfl | rfl | rfl <;>
    first | omega | assumption

end

end D3

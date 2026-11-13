import EncB.Model

/-! # U0 shared lemmas (prototype): literal semantics, list membership, `chi` under permutations -/

namespace EncB

/-! ### Literal semantics -/

theorem codeLitHolds_neg {τc : Nat → Prop} {x : Int} (hx : x ≠ 0) :
    CodeLitHolds τc (-x) ↔ ¬ CodeLitHolds τc x := by
  unfold CodeLitHolds
  rw [Int.natAbs_neg]
  constructor
  · rintro (⟨h1, h2⟩ | ⟨h1, h2⟩) <;> intro h <;> rcases h with ⟨h3, h4⟩ | ⟨h3, h4⟩ <;> first | omega | exact h2 h4 | exact h4 h2
  · intro h
    rcases Int.lt_or_gt_of_ne hx with hlt | hgt
    · left; exact ⟨by omega, Classical.byContradiction fun hn => h (Or.inr ⟨hlt, hn⟩)⟩
    · right; exact ⟨by omega, fun hn => h (Or.inl ⟨hgt, hn⟩)⟩

theorem codeLitHolds_pos {τc : Nat → Prop} {n : Nat} (hn : 0 < n) :
    CodeLitHolds τc (n : Int) ↔ τc n := by
  unfold CodeLitHolds
  rw [Int.natAbs_natCast]
  constructor
  · rintro (⟨_, h⟩ | ⟨h, _⟩)
    · exact h
    · omega
  · intro h; exact Or.inl ⟨by omega, h⟩

theorem Model.τc_code {m K t : Nat} (M : Model m K t) {v : Var} (hv : v.Valid m K t) :
    M.τc (v.code m K t) = M.τ v := by
  simp only [Model.τc, decodeCode_code hv]

theorem holds_y {m K t : Nat} (M : Model m K t) {i j : Nat} (hi : i < t) (hj : j < t) :
    CodeLitHolds M.τc (yLit t i j) ↔ M.psiLt i j = true := by
  have h := M.τc_code (v := .y i j) ⟨hi, hj⟩
  simp only [Var.code] at h
  rw [yLit, codeLitHolds_pos (by simp only [yCode]; omega), h]
  rfl

theorem holds_orb {m K t : Nat} (M : Model m K t) {a b d : Pt} (ha : PtOk m t a) (hb : PtOk m t b)
    (hd : PtOk m t d) : CodeLitHolds M.τc (orbCode m t [a, b, d] : Int) ↔ M.chi a b d = true := by
  have h := M.τc_code (v := .orb [a, b, d]) ⟨a, b, d, rfl, ha, hb, hd⟩
  simp only [Var.code] at h
  rw [codeLitHolds_pos (by simp only [orbCode, oBase]; omega), h]
  rfl

theorem holds_f {m K t : Nat} (M : Model m K t) {i l : Nat} {a b : Pt} (hi : i < t) (hl : l < chainFL K)
    (ha : PtOk m t a) (hb : PtOk m t b) :
    CodeLitHolds M.τc (fCode m K t i l a b : Int) ↔ ChainFrom m t M.chi i l a b := by
  have h := M.τc_code (v := .f i l a b) ⟨hi, hl, ha, hb⟩
  simp only [Var.code] at h
  rw [codeLitHolds_pos (by simp only [fCode, fBase, oBase]; omega), h]
  rfl

/-! ### `chi` under the six orders of a triple -/

theorem perm012_cases {s : List Nat} (hs : s.Perm [0, 1, 2]) :
    s = [0, 1, 2] ∨ s = [0, 2, 1] ∨ s = [1, 0, 2] ∨ s = [1, 2, 0] ∨ s = [2, 0, 1] ∨ s = [2, 1, 0] := by
  have hl := hs.length_eq
  have hnd : s.Nodup := hs.nodup_iff.2 (by decide)
  have hmem : ∀ x ∈ s, x < 3 := fun x hx => by
    have := hs.mem_iff.1 hx
    simp at this; omega
  match s, hl with
  | [x, y, z], _ =>
    have hx := hmem x (by simp)
    have hy := hmem y (by simp)
    have hz := hmem z (by simp)
    simp only [List.nodup_cons, List.mem_cons, List.not_mem_nil, or_false, List.nodup_nil,
      and_true, not_or] at hnd
    obtain ⟨⟨hxy, hxz⟩, hyz⟩ := hnd
    have : x = 0 ∨ x = 1 ∨ x = 2 := by omega
    have : y = 0 ∨ y = 1 ∨ y = 2 := by omega
    have : z = 0 ∨ z = 1 ∨ z = 2 := by omega
    rcases ‹x = 0 ∨ _› with rfl | rfl | rfl <;> rcases ‹y = 0 ∨ _› with rfl | rfl | rfl <;>
      rcases ‹z = 0 ∨ _› with rfl | rfl | rfl <;> simp_all

/-- `chi` of a reordered triple: the sign of the order (`permSign`, gen_b2.py:56-62). -/
theorem chi_perm3 {m K t : Nat} (M : Model m K t) {c0 c1 c2 : Pt} (h0 : PtOk m t c0) (h1 : PtOk m t c1)
    (h2 : PtOk m t c2) (hd : Distinct3 c0 c1 c2) {s : List Nat} (hs : s.Perm [0, 1, 2]) :
    M.chi ([c0, c1, c2].getD (s.getD 0 0) (0, 0)) ([c0, c1, c2].getD (s.getD 1 0) (0, 0))
        ([c0, c1, c2].getD (s.getD 2 0) (0, 0)) =
      (if permSign s > 0 then M.chi c0 c1 c2 else !M.chi c0 c1 c2) := by
  obtain ⟨d01, d02, d12⟩ := hd
  have cyc := M.chi_cycle
  have swp := M.chi_swap
  rcases perm012_cases hs with rfl | rfl | rfl | rfl | rfl | rfl
  · rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [swp c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩]; rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    -- chi c1 c0 c2 = chi c0 c2 c1 (cycle) = !chi c0 c1 c2 (swap)
    rw [← cyc c1 c0 c2 h1 h0 h2 ⟨Ne.symm d01, d12, d02⟩, swp c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩]; rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [cyc c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩]; rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [← cyc c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩, cyc c1 c2 c0 h1 h2 h0 ⟨d12, Ne.symm d01, Ne.symm d02⟩]; rfl
  · simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some]
    rw [swp c2 c0 c1 h2 h0 h1 ⟨Ne.symm d02, Ne.symm d12, d01⟩,
      ← cyc c0 c1 c2 h0 h1 h2 ⟨d01, d02, d12⟩, cyc c1 c2 c0 h1 h2 h0 ⟨d12, Ne.symm d01, Ne.symm d02⟩]; rfl

/-! ### Membership in the enumerations -/

theorem mem_rng {a b x : Nat} : x ∈ rng a b ↔ a ≤ x ∧ x < b := by
  simp only [rng, List.mem_range']
  constructor
  · rintro ⟨i, hi, rfl⟩; omega
  · intro h; exact ⟨x - a, by omega, by omega⟩

theorem mem_labels {m t : Nat} {p : Pt} : p ∈ labels m t ↔ PtOk m t p := by
  obtain ⟨i, k⟩ := p
  simp only [labels, List.mem_flatMap, List.mem_map, mem_rng, PtOk, Prod.mk.injEq]
  constructor
  · rintro ⟨i', hi, k', hk, rfl, rfl⟩; omega
  · intro h; exact ⟨i, by omega, k, by omega, rfl, rfl⟩

theorem mem_chainQ {m t i : Nat} {a : Pt} : a ∈ chainQ m t i ↔ InQ m t i a := by
  obtain ⟨j, k⟩ := a
  simp only [chainQ, List.mem_filter, List.mem_flatMap, List.mem_map, mem_rng, InQ, Prod.mk.injEq,
    bne_iff_ne, ne_eq]
  constructor
  · rintro ⟨⟨j', hj, k', hk, rfl, rfl⟩, hne⟩; exact ⟨by omega, by omega, by omega, hne⟩
  · rintro ⟨h1, h2, h3, hne⟩; exact ⟨⟨j, by omega, k, by omega, rfl, rfl⟩, hne⟩

theorem sublist_of_mem_pairs {α : Type} : ∀ {l : List α} {x y : α}, (x, y) ∈ pairs l → [x, y].Sublist l
  | [], _, _, h => absurd h List.not_mem_nil
  | a :: l, x, y, h => by
    simp only [pairs, List.mem_append, List.mem_map, Prod.mk.injEq] at h
    rcases h with ⟨b, hb, rfl, rfl⟩ | h
    · exact List.Sublist.cons₂ _ (List.singleton_sublist.2 hb)
    · exact List.Sublist.cons _ (sublist_of_mem_pairs h)

theorem mem_pairs_of_ne {α : Type} : ∀ {l : List α} {x y : α}, x ∈ l → y ∈ l → x ≠ y →
    (x, y) ∈ pairs l ∨ (y, x) ∈ pairs l
  | [], _, _, h, _, _ => absurd h List.not_mem_nil
  | a :: l, x, y, hx, hy, hne => by
    simp only [pairs, List.mem_append, List.mem_map, Prod.mk.injEq]
    rcases List.mem_cons.1 hx with rfl | hx' <;> rcases List.mem_cons.1 hy with rfl | hy'
    · exact absurd rfl hne
    · exact Or.inl (Or.inl ⟨y, hy', rfl, rfl⟩)
    · exact Or.inr (Or.inl ⟨x, hx', rfl, rfl⟩)
    · rcases mem_pairs_of_ne hx' hy' hne with h | h
      · exact Or.inl (Or.inr h)
      · exact Or.inr (Or.inr h)

theorem sublist_of_mem_triples {α : Type} : ∀ {l : List α} {x y z : α}, (x, y, z) ∈ triples l →
    [x, y, z].Sublist l
  | [], _, _, _, h => absurd h List.not_mem_nil
  | a :: l, x, y, z, h => by
    simp only [triples, List.mem_append, List.mem_map, Prod.mk.injEq] at h
    rcases h with ⟨yz, hyz, rfl, rfl, rfl⟩ | h
    · exact List.Sublist.cons₂ _ (sublist_of_mem_pairs hyz)
    · exact List.Sublist.cons _ (sublist_of_mem_triples h)

theorem rng_pairwise (a b : Nat) : (rng a b).Pairwise (· < ·) := by
  rw [List.pairwise_iff_getElem]
  intro i j hi hj hij
  simp only [rng, List.getElem_range']
  omega

end EncB

import N66Geo.Sem

/-!
# N66Geo.Triple: soundness of transitivity, growth with ceilings and chain starts (4.5-4.7) for every `Model`

Every clause of `tripleClausesAt a b c` carries the guards of `a, b, c` and the literals `¬before(a,b)`,
`¬before(b,c)`; with owners `x, y, z` in x-order the remaining literals are the transitivity of `<`, label growth
(`ActualRanks.labels_increasing`) with the ceilings `label ≤ 4` (no 6-cap / 6-cup), and the 3-paths.
-/

namespace N66Geo
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks ErdosSzekeres.Omission.StateInterface
  N66Enc

/-- If the three guards are in the clause, it suffices to treat the case where all three states have owners. -/
theorem holds_of_owners3 {M : Model} {a b c : Fin 70} {cl : List SLit}
    (hg : guard a ∈ cl ∧ guard b ∈ cl ∧ guard c ∈ cl)
    (h : ∀ x y z, x < M.n → y < M.n → z < M.n → idxOf M.cup x = a.val → idxOf M.cup y = b.val →
      idxOf M.cup z = c.val → ∃ l ∈ cl, Agree M l) : ∃ l ∈ cl, Agree M l := by
  by_cases ha : M.occ a
  · by_cases hb : M.occ b
    · by_cases hc : M.occ c
      · obtain ⟨x, hx, hxa⟩ := ha
        obtain ⟨y, hy, hyb⟩ := hb
        obtain ⟨z, hz, hzc⟩ := hc
        exact h x y z hx hy hz hxa hyb hzc
      · exact ⟨guard c, hg.2.2, (agree_guard M c).2 hc⟩
    · exact ⟨guard b, hg.2.1, (agree_guard M b).2 hb⟩
  · exact ⟨guard a, hg.1, (agree_guard M a).2 ha⟩

/-- If `¬before(a,b)` and `¬before(b,c)` are in the clause, it suffices to treat owners in x-order. -/
theorem holds_of_order3 {M : Model} {a b c : Fin 70} {x y z : ℕ} (hab : a ≠ b) (hbc : b ≠ c)
    (hx : x < M.n) (hy : y < M.n) (hz : z < M.n)
    (ha : idxOf M.cup x = a.val) (hb : idxOf M.cup y = b.val) (hc : idxOf M.cup z = c.val) {cl : List SLit}
    (h1 : (befLit a b).neg ∈ cl) (h2 : (befLit b c).neg ∈ cl)
    (h : x < y → y < z → ∃ l ∈ cl, Agree M l) : ∃ l ∈ cl, Agree M l := by
  by_cases hxy : x < y
  · by_cases hyz : y < z
    · exact h hxy hyz
    · exact ⟨_, h2, (agree_neg M _).2 (fun hh => hyz ((agree_befLit M hbc hy hz hb hc).1 hh))⟩
  · exact ⟨_, h1, (agree_neg M _).2 (fun hh => hxy ((agree_befLit M hab hx hy ha hb).1 hh))⟩

theorem agree_geAtom_false (M : Model) (cup : Bool) {a b : Fin 70} {x y : ℕ} (hxy : x < y) (hy : y < M.n)
    (ha : idxOf M.cup x = a.val) (hb : idxOf M.cup y = b.val) {k : ℕ} (hk : k < 5) :
    Agree M (false, geAtom cup a b k) ↔ ¬ k ≤ (if cup then (labels M.cup x y).2 else (labels M.cup x y).1) := by
  rw [← agree_geAtom M cup hxy hy ha hb hk]
  unfold Agree
  cases M.meaning (geAtom cup a b k) <;> simp

theorem agree_geAtom_true (M : Model) (cup : Bool) {a b : Fin 70} {x y : ℕ} (hxy : x < y) (hy : y < M.n)
    (ha : idxOf M.cup x = a.val) (hb : idxOf M.cup y = b.val) {k : ℕ} (hk : k < 5) :
    Agree M (true, geAtom cup a b k) ↔ k ≤ (if cup then (labels M.cup x y).2 else (labels M.cup x y).1) :=
  agree_geAtom M cup hxy hy ha hb hk

theorem chain3 (M : Model) {color : Bool} {a b c : Fin 70} {x y z : ℕ} (hxy : x < y) (hyz : y < z)
    (hz : z < M.n) (ha : idxOf M.cup x = a.val) (hb : idxOf M.cup y = b.val) (hc : idxOf M.cup z = c.val)
    (hcol : M.cup x y z = color) : M.Chain color 3 a b c :=
  ⟨x, y, z, hz, ha, hb, hc, SEPath.step (SEPath.two hxy) hyz hcol⟩

open Classical in
theorem agree_chain (M : Model) (color : Bool) (k : Fin 6) (a b c : Fin 70) :
    Agree M (true, if color then Atom.chU k a b c else Atom.chC k a b c) ↔ M.Chain color k.val a b c := by
  cases color <;> simp [Agree, meaning_chC, meaning_chU]

/-- **4.5-4.7** for one permutation. -/
theorem holds_tripleAt (M : Model) (a b c : Fin 70) (hab : a ≠ b) (hbc : b ≠ c) (hac : a ≠ c) :
    M.Holds (tripleClausesAt a b c) := by
  classical
  have hgen : ∀ (pre : List SLit), (befLit a b).neg ∈ pre → (befLit b c).neg ∈ pre →
      (∀ x y z, x < M.n → y < M.n → z < M.n → idxOf M.cup x = a.val → idxOf M.cup y = b.val →
        idxOf M.cup z = c.val → x < y → y < z → ∃ l ∈ pre ++ [guard a, guard b, guard c], Agree M l) →
      ∃ l ∈ pre ++ [guard a, guard b, guard c], Agree M l := by
    intro pre h1 h2 h
    apply holds_of_owners3 (a := a) (b := b) (c := c) (by simp)
    intro x y z hx hy hz ha hb hc
    exact holds_of_order3 hab hbc hx hy hz ha hb hc (List.mem_append_left _ h1) (List.mem_append_left _ h2)
      (h x y z hx hy hz ha hb hc)
  have htrans : ∃ l ∈ [(befLit a b).neg, (befLit b c).neg, befLit a c] ++ [guard a, guard b, guard c],
      Agree M l := by
    apply hgen _ (by simp) (by simp)
    intro x y z hx hy hz ha hb hc hxy hyz
    exact ⟨befLit a c, by simp, (agree_befLit M hac hx hz ha hc).2 (lt_trans hxy hyz)⟩
  intro cl hcl
  unfold tripleClausesAt at hcl
  dsimp only at hcl
  split at hcl
  · simp at hcl
  split at hcl
  · simp only [List.mem_singleton] at hcl
    subst hcl
    exact htrans
  rcases List.mem_append.1 hcl with hcl | hcl
  · rcases List.mem_append.1 hcl with hcl | hcl
    · simp only [List.mem_singleton] at hcl
      subst hcl
      exact htrans
    · -- growth
      obtain ⟨cup, -, hcl⟩ := List.mem_flatMap.1 hcl
      obtain ⟨k, hk, rfl⟩ := List.mem_map.1 hcl
      have hk4 : k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 := by simpa using hk
      apply hgen _ (by simp) (by simp)
      intro x y z hx hy hz ha hb hc hxy hyz
      have hinc := (labels_increasing M.n M.cup) x y z hxy hyz hz
      have bxy := label_bounds6 M hxy hy
      have byz := label_bounds6 M hyz hz
      have hori := agree_oriLit M hab hbc hac hx hy hz ha hb hc
      rw [ori3_lt M.cup hxy hyz] at hori
      cases cup with
      | false =>
        by_cases hcol : M.cup x y z = true
        · exact ⟨oriLit a b c, by simp, hori.2 hcol⟩
        · have hg := hinc.1 (by simpa using hcol)
          rcases hk4 with rfl | rfl | rfl | rfl
          · exact ⟨(true, geAtom false b c 2), by simp,
              (agree_geAtom_true M false hyz hz hb hc (by decide)).2 (by simp; omega)⟩
          · by_cases hx2 : 2 ≤ (labels M.cup x y).1
            · exact ⟨(true, geAtom false b c 3), by simp,
                (agree_geAtom_true M false hyz hz hb hc (by decide)).2 (by simp; omega)⟩
            · exact ⟨(false, geAtom false a b 2), by simp,
                (agree_geAtom_false M false hxy hy ha hb (by decide)).2 (by simpa using hx2)⟩
          · by_cases hx3 : 3 ≤ (labels M.cup x y).1
            · exact ⟨(true, geAtom false b c 4), by simp,
                (agree_geAtom_true M false hyz hz hb hc (by decide)).2 (by simp; omega)⟩
            · exact ⟨(false, geAtom false a b 3), by simp,
                (agree_geAtom_false M false hxy hy ha hb (by decide)).2 (by simpa using hx3)⟩
          · exact ⟨(false, geAtom false a b 4), by simp,
              (agree_geAtom_false M false hxy hy ha hb (by decide)).2 (by simp; omega)⟩
      | true =>
        by_cases hcol : M.cup x y z = true
        · have hg := hinc.2 hcol
          rcases hk4 with rfl | rfl | rfl | rfl
          · exact ⟨(true, geAtom true b c 2), by simp,
              (agree_geAtom_true M true hyz hz hb hc (by decide)).2 (by simp; omega)⟩
          · by_cases hx2 : 2 ≤ (labels M.cup x y).2
            · exact ⟨(true, geAtom true b c 3), by simp,
                (agree_geAtom_true M true hyz hz hb hc (by decide)).2 (by simp; omega)⟩
            · exact ⟨(false, geAtom true a b 2), by simp,
                (agree_geAtom_false M true hxy hy ha hb (by decide)).2 (by simpa using hx2)⟩
          · by_cases hx3 : 3 ≤ (labels M.cup x y).2
            · exact ⟨(true, geAtom true b c 4), by simp,
                (agree_geAtom_true M true hyz hz hb hc (by decide)).2 (by simp; omega)⟩
            · exact ⟨(false, geAtom true a b 3), by simp,
                (agree_geAtom_false M true hxy hy ha hb (by decide)).2 (by simpa using hx3)⟩
          · exact ⟨(false, geAtom true a b 4), by simp,
              (agree_geAtom_false M true hxy hy ha hb (by decide)).2 (by simp; omega)⟩
        · exact ⟨(oriLit a b c).neg, by simp, (agree_neg M _).2 (fun hh => hcol (hori.1 hh))⟩
  · simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hcl
    rcases hcl with rfl | rfl
    · -- C3
      apply hgen _ (by simp) (by simp)
      intro x y z hx hy hz ha hb hc hxy hyz
      have hori := agree_oriLit M hab hbc hac hx hy hz ha hb hc
      rw [ori3_lt M.cup hxy hyz] at hori
      by_cases hcol : M.cup x y z = true
      · exact ⟨oriLit a b c, by simp, hori.2 hcol⟩
      · refine ⟨(true, Atom.chC 3 a b c), by simp, ?_⟩
        have := (agree_chain M false 3 a b c).2 (chain3 M hxy hyz hz ha hb hc (by simpa using hcol))
        simpa using this
    · -- U3
      apply hgen _ (by simp) (by simp)
      intro x y z hx hy hz ha hb hc hxy hyz
      have hori := agree_oriLit M hab hbc hac hx hy hz ha hb hc
      rw [ori3_lt M.cup hxy hyz] at hori
      by_cases hcol : M.cup x y z = true
      · refine ⟨(true, Atom.chU 3 a b c), by simp, ?_⟩
        have := (agree_chain M true 3 a b c).2 (chain3 M hxy hyz hz ha hb hc hcol)
        simpa using this
      · exact ⟨(oriLit a b c).neg, by simp, (agree_neg M _).2 (fun hh => hcol (hori.1 hh))⟩

theorem mem_perm3 {t : Fin 70 × Fin 70 × Fin 70} (h : t ∈ perm3) : t.1 ≠ t.2.1 ∧ t.2.1 ≠ t.2.2 ∧ t.1 ≠ t.2.2 := by
  unfold perm3 at h
  simp only [List.mem_flatMap, List.mem_filterMap] at h
  obtain ⟨a, -, b, -, c, -, hc⟩ := h
  split at hc
  · rename_i hd
    simp only [Option.some.injEq] at hc
    subst hc
    exact hd
  · simp at hc

/-- **4.5-4.7.** -/
theorem holds_triple (M : Model) : M.Holds (tripleClauses ()) := by
  intro cl hcl
  unfold tripleClauses at hcl
  obtain ⟨t, ht, hcl⟩ := List.mem_flatMap.1 hcl
  obtain ⟨h1, h2, h3⟩ := mem_perm3 ht
  exact holds_tripleAt M t.1 t.2.1 t.2.2 h1 h2 h3 cl hcl

end N66Geo

#print axioms N66Geo.holds_triple

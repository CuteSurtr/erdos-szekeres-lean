import N66Geo.Triple

/-!
# N66Geo.Quad: soundness of the chain steps and signotope packets (4.9-4.10) for every `Model`

For an ordered quadruple `(a, b, c, d)` with owners `x, y, z, w`:
* the 8 packet clauses exclude, for `x < y < z < w`, the orientation patterns with two or more sign changes
  (`Model.signotope` gives `PacketValid`, and `bad4` lists exactly the 8 invalid patterns);
* the 4 chain-step clauses extend a k-path ending with `(y, z)` by `w` (definition of `SEPath`).
-/

namespace N66Geo
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks N66Enc

theorem SEPath.last_lt {cup : ℕ → ℕ → ℕ → Bool} {color : Bool} {p u v k : ℕ}
    (h : SEPath cup color p u v k) : u < v := by
  cases h with
  | two hv => exact hv
  | step _ huv _ => exact huv

theorem holds_of_owners4 {M : Model} {a b c d : Fin 70} {cl : List SLit}
    (hg : guard a ∈ cl ∧ guard b ∈ cl ∧ guard c ∈ cl ∧ guard d ∈ cl)
    (h : ∀ x y z w, x < M.n → y < M.n → z < M.n → w < M.n → idxOf M.cup x = a.val → idxOf M.cup y = b.val →
      idxOf M.cup z = c.val → idxOf M.cup w = d.val → ∃ l ∈ cl, Agree M l) : ∃ l ∈ cl, Agree M l := by
  by_cases ha : M.occ a
  · by_cases hb : M.occ b
    · by_cases hc : M.occ c
      · by_cases hd : M.occ d
        · obtain ⟨x, hx, hxa⟩ := ha
          obtain ⟨y, hy, hyb⟩ := hb
          obtain ⟨z, hz, hzc⟩ := hc
          obtain ⟨w, hw, hwd⟩ := hd
          exact h x y z w hx hy hz hw hxa hyb hzc hwd
        · exact ⟨guard d, hg.2.2.2, (agree_guard M d).2 hd⟩
      · exact ⟨guard c, hg.2.2.1, (agree_guard M c).2 hc⟩
    · exact ⟨guard b, hg.2.1, (agree_guard M b).2 hb⟩
  · exact ⟨guard a, hg.1, (agree_guard M a).2 ha⟩

/-- The 8 patterns of `bad4` are exactly the invalid packets. -/
theorem packet_ne_bad : ∀ p0 p1 p2 p3 : Bool, PacketValid p0 p1 p2 p3 →
    ∀ q ∈ bad4, ¬ (p0 = q.1 ∧ p1 = q.2.1 ∧ p2 = q.2.2.1 ∧ p3 = q.2.2.2) := by
  intro p0 p1 p2 p3 hp q hq heq
  obtain ⟨h0, h1, h2, h3⟩ := heq
  simp only [bad4, List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hq
  rcases hq with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> (subst h0 h1 h2 h3; revert hp; decide)

theorem agree_flipIf (M : Model) (bit : Bool) (t : SLit) (v : Bool) (ht : Agree M t ↔ v = true) :
    Agree M (flipIf bit t) ↔ v ≠ bit := by
  unfold flipIf
  cases bit
  · simp only [Bool.false_eq_true, if_false, ne_eq]
    rw [ht]
    cases v <;> simp
  · simp only [if_true, ne_eq]
    rw [agree_neg, ht]

theorem mem_perm4' {q : Fin 70 × Fin 70 × Fin 70 × Fin 70} (h : q ∈ perm4) : okQuad q.1 q.2.1 q.2.2.1 q.2.2.2 = true := by
  unfold perm4 at h
  simp only [List.mem_flatMap, List.mem_filterMap] at h
  obtain ⟨a, -, b, -, c, -, d, -, hd⟩ := h
  split at hd
  · rename_i hq
    simp only [Option.some.injEq] at hd
    subst hd
    exact hq
  · simp at hd

theorem okQuad_distinct {a b c d : Fin 70} (h : okQuad a b c d = true) :
    a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ b ≠ c ∧ b ≠ d ∧ c ≠ d := by
  unfold okQuad at h
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h
  exact h.1.1.1.1.1.1

/-- **4.9-4.10** for one ordered quadruple. -/
theorem holds_quadAt (M : Model) (a b c d : Fin 70) (hq : okQuad a b c d = true) :
    M.Holds (quadClauses a b c d) := by
  classical
  obtain ⟨hab, hac, had, hbc, hbd, hcd⟩ := okQuad_distinct hq
  intro cl hcl
  unfold quadClauses at hcl
  dsimp only at hcl
  rcases List.mem_append.1 hcl with hcl | hcl
  · -- packets
    obtain ⟨bits, hbits, rfl⟩ := List.mem_map.1 hcl
    apply holds_of_owners4 (a := a) (b := b) (c := c) (d := d) (by simp)
    intro x y z w hx hy hz hw ha hb hc hd
    by_cases hxy : x < y
    · by_cases hyz : y < z
      · by_cases hzw : z < w
        · have t0 := agree_oriLit M hab hbc hac hx hy hz ha hb hc
          have t1 := agree_oriLit M hab hbd had hx hy hw ha hb hd
          have t2 := agree_oriLit M hac hcd had hx hz hw ha hc hd
          have t3 := agree_oriLit M hbc hcd hbd hy hz hw hb hc hd
          rw [ori3_lt M.cup hxy hyz] at t0
          rw [ori3_lt M.cup hxy (lt_trans hyz hzw)] at t1
          rw [ori3_lt M.cup (lt_trans hxy hyz) hzw] at t2
          rw [ori3_lt M.cup hyz hzw] at t3
          have hp := M.signotope x y z w hxy hyz hzw hw
          have hne := packet_ne_bad _ _ _ _ hp bits hbits
          by_cases e0 : M.cup x y z = bits.1
          · by_cases e1 : M.cup x y w = bits.2.1
            · by_cases e2 : M.cup x z w = bits.2.2.1
              · have e3 : M.cup y z w ≠ bits.2.2.2 := fun e3 => hne ⟨e0, e1, e2, e3⟩
                exact ⟨_, by simp, (agree_flipIf M _ _ _ t3).2 e3⟩
              · exact ⟨_, by simp, (agree_flipIf M _ _ _ t2).2 e2⟩
            · exact ⟨_, by simp, (agree_flipIf M _ _ _ t1).2 e1⟩
          · exact ⟨_, by simp, (agree_flipIf M _ _ _ t0).2 e0⟩
        · exact ⟨(befLit c d).neg, by simp,
            (agree_neg M _).2 (fun hh => hzw ((agree_befLit M hcd hz hw hc hd).1 hh))⟩
      · exact ⟨(befLit b c).neg, by simp,
          (agree_neg M _).2 (fun hh => hyz ((agree_befLit M hbc hy hz hb hc).1 hh))⟩
    · exact ⟨(befLit a b).neg, by simp,
        (agree_neg M _).2 (fun hh => hxy ((agree_befLit M hab hx hy ha hb).1 hh))⟩
  · -- chain steps
    simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hcl
    have step : ∀ (color : Bool) (k : Fin 6) (k' : Fin 6), k'.val = k.val + 1 →
        ∀ cl', cl' = [(false, if color then Atom.chU k a b c else Atom.chC k a b c), (befLit c d).neg,
          (if color then (oriLit b c d).neg else oriLit b c d),
          (true, if color then Atom.chU k' a c d else Atom.chC k' a c d)] ++
          [guard a, guard b, guard c, guard d] → ∃ l ∈ cl', Agree M l := by
      intro color k k' hk' cl' hcl'
      subst hcl'
      by_cases hch : M.Chain color k.val a b c
      · obtain ⟨p, u, v, hv, hp, hu, hvc, hpath⟩ := hch
        apply holds_of_owners4 (a := a) (b := b) (c := c) (d := d) (by simp)
        intro x y z w hx hy hz hw ha hb hc hd
        have huy : u = y := owner_unique M (lt_trans hpath.last_lt hv) hy hu hb
        have hvz : v = z := owner_unique M hv hz hvc hc
        subst huy; subst hvz
        have hyz := hpath.last_lt
        by_cases hzw : v < w
        · have t3 := agree_oriLit M hbc hcd hbd hy hz hw hb hc hd
          rw [ori3_lt M.cup hyz hzw] at t3
          cases color with
          | false =>
            by_cases hcol : M.cup u v w = true
            · exact ⟨oriLit b c d, by simp, t3.2 hcol⟩
            · refine ⟨(true, Atom.chC k' a c d), by simp, ?_⟩
              have hc' : M.Chain false k'.val a c d :=
                ⟨p, v, w, hw, hp, hc, hd, by rw [hk']; exact SEPath.step hpath hzw (by simpa using hcol)⟩
              simpa using (agree_chain M false k' a c d).2 hc'
          | true =>
            by_cases hcol : M.cup u v w = true
            · refine ⟨(true, Atom.chU k' a c d), by simp, ?_⟩
              have hc' : M.Chain true k'.val a c d :=
                ⟨p, v, w, hw, hp, hc, hd, by rw [hk']; exact SEPath.step hpath hzw hcol⟩
              simpa using (agree_chain M true k' a c d).2 hc'
            · exact ⟨(oriLit b c d).neg, by simp, (agree_neg M _).2 (fun hh => hcol (t3.1 hh))⟩
        · exact ⟨(befLit c d).neg, by simp,
            (agree_neg M _).2 (fun hh => hzw ((agree_befLit M hcd hz hw hc hd).1 hh))⟩
      · refine ⟨(false, if color then Atom.chU k a b c else Atom.chC k a b c), by simp, ?_⟩
        have := (agree_chain M color k a b c)
        unfold Agree at this ⊢
        cases hm : M.meaning (if color then Atom.chU k a b c else Atom.chC k a b c)
        · rfl
        · exact absurd (this.1 hm) hch
    rcases hcl with rfl | rfl | rfl | rfl
    · exact step false 3 4 rfl _ (by simp)
    · exact step true 3 4 rfl _ (by simp)
    · exact step false 4 5 rfl _ (by simp)
    · exact step true 4 5 rfl _ (by simp)

/-- **4.9-4.10.** -/
theorem holds_quad (M : Model) : M.Holds quadStream := by
  intro cl hcl
  unfold quadStream at hcl
  obtain ⟨q, hq, hcl⟩ := List.mem_flatMap.1 hcl
  exact holds_quadAt M q.1 q.2.1 q.2.2.1 q.2.2.2 (mem_perm4' hq) cl hcl

end N66Geo

#print axioms N66Geo.holds_quad

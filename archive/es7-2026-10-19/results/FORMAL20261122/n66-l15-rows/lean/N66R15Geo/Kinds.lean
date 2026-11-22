import N66R15Geo.Row

/-!
# N66R15Geo.Kinds: cores, mirror images, cycle rows

* `allTests_ok`, `allTests_good`: the generated tests of a core are well formed and good for its own states, so a
  core certificate refutes its own support (`rowValid_core`).
* `rowValid_tau`: the mirror lemma (N66 README §2.8) from n66enc's `mirror_holds`.
* `rowValid_mono`: a row with fewer states is stronger.
* `rowValid_cycle`: eight states whose list-order triples all pass the six-order test (N66 README §2.6).
-/

namespace N66R15Geo
open N66R15Enc N66G15 ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

theorem allTests_ok (S : List (Fin 70)) : ∀ x ∈ allTests S, testOk S.length x = true := by
  intro x hx
  unfold allTests at hx
  simp only [List.mem_append, List.mem_flatMap, List.mem_filterMap] at hx
  rcases hx with ⟨p, hp, hx⟩ | ⟨p, hp, hx⟩
  · obtain ⟨i, j, rfl, hij, hjn⟩ := combs2_shape hp
    simp only [List.mem_flatMap, List.mem_cons, List.not_mem_nil, or_false] at hx
    obtain ⟨uv, huv, hx⟩ := hx
    rcases huv with rfl | rfl <;> (split at hx
                                   · simp only [List.mem_cons, List.not_mem_nil, or_false] at hx; subst hx
                                     simp [testOk]; omega
                                   · obtain ⟨z, -, hz⟩ := List.mem_filterMap.1 hx
                                     split at hz
                                     · cases hz
                                     · simp only [Option.some.injEq] at hz; subst hz; simp [testOk]; omega)
  · obtain ⟨i, j, k, rfl, hij, hjk, hkn⟩ := combs3_shape hp
    simp only at hx
    split at hx
    · simp only [Option.some.injEq] at hx; subst hx; simp [testOk]; omega
    · split at hx
      · simp only [Option.some.injEq] at hx; subst hx; simp [testOk]; omega
      · cases hx

theorem allTests_good (S : List (Fin 70)) : ∀ x ∈ allTests S, Good (fun i => S.getD i 0) x := by
  intro x hx
  unfold allTests at hx
  simp only [List.mem_append, List.mem_flatMap, List.mem_filterMap] at hx
  rcases hx with ⟨p, hp, hx⟩ | ⟨p, hp, hx⟩
  · obtain ⟨i, j, rfl, hij, hjn⟩ := combs2_shape hp
    simp only [List.mem_flatMap, List.mem_cons, List.not_mem_nil, or_false] at hx
    obtain ⟨uv, -, hx⟩ := hx
    split at hx
    · rename_i hc
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hx; subst hx
      simpa [Good] using hc
    · obtain ⟨z, -, hz⟩ := List.mem_filterMap.1 hx
      split at hz
      · cases hz
      · rename_i hd
        simp only [Option.some.injEq] at hz; subst hz
        simpa [Good] using hd
  · obtain ⟨i, j, k, rfl, hij, hjk, hkn⟩ := combs3_shape hp
    simp only at hx
    split at hx
    · rename_i h; simp only [Option.some.injEq] at hx; subst hx; exact h
    · split at hx
      · rename_i _ h; simp only [Option.some.injEq] at hx; subst hx; exact h
      · cases hx

theorem rowValid_mono {S T : List (Fin 70)} (h : RowValid S) (hsub : ∀ x ∈ S, x ∈ T) : RowValid T := by
  intro N c hc
  obtain ⟨s, hs, hno⟩ := h N c hc
  exact ⟨s, hsub s hs, hno⟩

/-- **Mirror lemma.** -/
theorem rowValid_tau {S : List (Fin 70)} (h : RowValid S) : RowValid (S.map tau) := by
  intro N c hc
  obtain ⟨c', hc', hocc⟩ := mirror_holds N c hc
  obtain ⟨s, hs, hno⟩ := h N c' hc'
  exact ⟨tau s, List.mem_map_of_mem hs, fun hcs => hno ((hocc s).2 hcs)⟩

theorem ori3_orient {N : ℕ} (c : Configuration N) {x y z : ℕ} (hx : x < N) (hy : y < N) (hz : z < N)
    (hxy : x ≠ y) (hyz : y ≠ z) (hxz : x ≠ z) (h : ori3 c.cup x y z = true) :
    0 < orient (ptOf c x) (ptOf c y) (ptOf c z) := by
  rcases Nat.lt_or_gt_of_ne hxy with a1 | a1 <;> rcases Nat.lt_or_gt_of_ne hyz with a2 | a2 <;>
    rcases Nat.lt_or_gt_of_ne hxz with a3 | a3
  · simp [ori3, a1, a2] at h; exact ptOf_pos c a1 a2 hz h
  · omega
  · -- x < z < y
    simp [ori3, a1, Nat.not_lt_of_gt a2, a3] at h
    have := ptOf_neg c a3 a2 hy h
    rw [CycleSigns.orient_swap23]; linarith
  · -- z < x < y
    simp [ori3, a1, Nat.not_lt_of_gt a2, Nat.not_lt_of_gt a3] at h
    have := ptOf_pos c a3 a1 hy h
    rw [CycleSigns.orient_rotate, CycleSigns.orient_rotate]; exact this
  · -- y < x < z
    simp [ori3, Nat.not_lt_of_gt a1, a3] at h
    have := ptOf_neg c a1 a3 hz h
    rw [CycleSigns.orient_swap12]; linarith
  · -- y < z < x
    simp [ori3, Nat.not_lt_of_gt a1, Nat.not_lt_of_gt a3, a2] at h
    have := ptOf_pos c a2 a3 hx h
    rw [CycleSigns.orient_rotate]; exact this
  · omega
  · -- z < y < x
    simp [ori3, Nat.not_lt_of_gt a1, Nat.not_lt_of_gt a3, Nat.not_lt_of_gt a2] at h
    have := ptOf_neg c a2 a1 hx h
    rw [CycleSigns.orient_reverse]; linarith

/-- **Cycle rows.** -/
theorem rowValid_cycle (L : List (Fin 70)) (hL : L.length = 8) (hnd : L.Nodup)
    (htt : ∀ i j k : ℕ, i < j → j < k → k < 8 → N66E15.tt (L.getD i 0) (L.getD j 0) (L.getD k 0) = true) :
    RowValid L := by
  intro N c hc
  by_contra hno
  push_neg at hno
  obtain ⟨o, ho, hσ⟩ := owners_of_occ c hc L hnd hno
  rw [hL] at ho hσ
  apply hc.2.2
  let e : Fin 8 ↪ Fin N := ⟨fun i => ⟨o i, ho.lt i i.isLt⟩, fun i j h => Fin.ext (ho.inj _ _ i.isLt j.isLt
    (congrArg Fin.val h))⟩
  refine hasConvexNGon_of_positive_cycle (by norm_num) c.point
    (fun a b h => c.xOrder.injective (congrArg (fun p : Point => p 0) h)) e
    (fun i => Finset.mem_image_of_mem _ (Finset.mem_univ _)) ?_
  intro i j l hij hjl
  have hij' : i.val < j.val := hij
  have hjl' : j.val < l.val := hjl
  have hs := tt_sound (modelOf c hc (capCup55_holds N c hc.2.2)) (ho.lt i i.isLt) (ho.lt j j.isLt)
    (ho.lt l l.isLt) (hσ i i.isLt) (hσ j j.isLt) (hσ l l.isLt) (htt i j l hij' hjl' l.isLt)
  have hp := ori3_orient c (ho.lt i i.isLt) (ho.lt j j.isLt) (ho.lt l l.isLt)
    (ho.ne i.isLt j.isLt (by omega)) (ho.ne j.isLt l.isLt (by omega)) (ho.ne i.isLt l.isLt (by omega)) hs
  rw [ptOf_eq c (ho.lt i i.isLt), ptOf_eq c (ho.lt j j.isLt), ptOf_eq c (ho.lt l l.isLt)] at hp
  exact hp

end N66R15Geo

import V182Geo.Sound

/-!
# V182Geo.Cover: the 4,404 pieces cover every normalised rainbow 5-colouring (M3)

`exists_piece`: for a rainbow `ψ`, the colours on the Y1 star (mask 47) form some permutation `π_n` (five pairwise
conflicting edges), so `ind ψ` satisfies the units of Y1 cube `n`; if `n` is split, the same for the Y2 star
(mask 55) and some `m`. The piece `(n, ·)` is listed in `pieces` by construction. `no_normal_colouring`: with the
verdicts, no rainbow 5-colouring satisfies the units.
-/

namespace V182Geo
open V182Enc

/-- `permsOf k l` contains every permutation of `l` (`l.length = k`). -/
theorem mem_permsOf : ∀ (k : ℕ) (l p : List ℕ), l.length = k → p.Perm l → p ∈ permsOf k l
  | 0, l, p, hl, hp => by
    have h1 : l = [] := List.length_eq_zero_iff.1 hl
    subst h1
    have h2 : p = [] := hp.eq_nil
    subst h2
    simp [permsOf]
  | k + 1, l, p, hl, hp => by
    cases p with
    | nil =>
      have := hp.length_eq
      simp only [List.length_nil] at this
      omega
    | cons a p' =>
      have ha : a ∈ l := hp.subset List.mem_cons_self
      have h1 : p'.Perm (l.erase a) := (hp.trans (List.perm_cons_erase ha)).cons_inv
      have h2 : (l.erase a).length = k := by rw [List.length_erase_of_mem ha, hl]; rfl
      simp only [permsOf]
      exact List.mem_flatMap.2 ⟨a, ha, List.mem_map.2 ⟨p', mem_permsOf k _ _ h2 h1, rfl⟩⟩

/-- Five distinct values below 5, as a list, are one of the 120 permutations. -/
theorem mem_perms5 {L : List ℕ} (hnd : L.Nodup) (hlen : L.length = 5) (hlt : ∀ x ∈ L, x < 5) : L ∈ perms5 := by
  apply mem_permsOf 5 (List.range 5) L List.length_range
  apply List.perm_of_nodup_nodup_toFinset_eq hnd List.nodup_range
  ext x
  simp only [List.mem_toFinset, List.mem_range]
  exact ⟨hlt x, fun hx => five_complete hnd hlen hlt hx⟩

theorem perms5_length : perms5.length = 120 := by decide +kernel

theorem y1Star_conf : allConf y1Star = true := by decide +kernel
theorem y2Star_conf : allConf y2Star = true := by decide +kernel
theorem y1Star_nodup : y1Star.Nodup := by decide
theorem y2Star_nodup : y2Star.Nodup := by decide

theorem zipWith_lit_map (S : List ℕ) (g : ℕ → ℕ) : List.zipWith lit S (S.map g) = S.map fun e => lit e (g e) := by
  induction S with
  | nil => rfl
  | cons e S ih => simp only [List.map_cons, List.zipWith_cons_cons, ih]

/-- The colours of a star of 5 pairwise conflicting edges are a permutation `π_n`, and `ind ψ` satisfies the
units of cube `n` on that star. -/
theorem star_cube {ψ : Sym2 V → Fin 5} (hψ : IsRainbowS ψ) {S : List ℕ} (hS : S.Nodup) (hconf : allConf S = true)
    (hlen : S.length = 5) : ∃ n < 120, ∀ l ∈ starUnits S n, EncB.LitSat (ind ψ) l := by
  set L := S.map fun e => ((ψ (edgeOfIdx e)) : ℕ) with hL
  have hnd : L.Nodup := nodup_colours hψ hS (allConf_spec hconf)
  have hlt : ∀ x ∈ L, x < 5 := by
    intro x hx
    obtain ⟨e, -, rfl⟩ := List.mem_map.1 hx
    exact (ψ (edgeOfIdx e)).2
  have hmem : L ∈ perms5 := mem_perms5 hnd (by rw [hL, List.length_map, hlen]) hlt
  have hi := List.idxOf_lt_length_of_mem hmem
  refine ⟨perms5.idxOf L, by rw [← perms5_length]; exact hi, ?_⟩
  have hget : perms5.getD (perms5.idxOf L) [] = L := by
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi, Option.getD_some]
    exact EncB.getElem_idxOf _
  intro l hl
  unfold starUnits at hl
  rw [hget, hL, zipWith_lit_map] at hl
  obtain ⟨e, -, rfl⟩ := List.mem_map.1 hl
  exact (litSat_lit ψ (ψ (edgeOfIdx e)).2).2 rfl

/-- **M3 (cover).** Every rainbow 5-colouring satisfies the units of some listed piece. -/
theorem exists_piece {ψ : Sym2 V → Fin 5} (hψ : IsRainbowS ψ) :
    ∃ q ∈ pieces, ∀ l ∈ pieceCube q, EncB.LitSat (ind ψ) l := by
  obtain ⟨n, hn, hY1⟩ := star_cube hψ y1Star_nodup y1Star_conf rfl
  by_cases hs : splitSet.contains n = true
  · obtain ⟨m, hm, hY2⟩ := star_cube hψ y2Star_nodup y2Star_conf rfl
    refine ⟨(n, some m), ?_, ?_⟩
    · unfold pieces
      refine List.mem_flatMap.2 ⟨n, List.mem_range.2 hn, ?_⟩
      rw [if_pos hs]
      exact List.mem_map.2 ⟨m, List.mem_range.2 hm, rfl⟩
    · intro l hl
      rcases List.mem_append.1 hl with h | h
      · exact hY1 l h
      · exact hY2 l h
  · refine ⟨(n, none), ?_, hY1⟩
    unfold pieces
    refine List.mem_flatMap.2 ⟨n, List.mem_range.2 hn, ?_⟩
    rw [if_neg hs]
    exact List.mem_singleton.2 rfl

/-- **No normalised rainbow 5-colouring** (modulo the verdicts). -/
theorem no_normal_colouring (h : PieceVerdicts) {ψ : Sym2 V → Fin 5} (hψ : IsRainbowS ψ) (hu : UnitsHold ψ) :
    False := by
  obtain ⟨q, hq, hsat⟩ := exists_piece hψ
  apply piece_unsat h hq
  refine ⟨ind ψ, ?_⟩
  intro cl hcl
  unfold EncB.cubeCnf at hcl
  rcases List.mem_append.1 hcl with h1 | h2
  · exact baseCnf_sat hψ hu cl h1
  · obtain ⟨z, hz, rfl⟩ := List.mem_map.1 h2
    exact ⟨z, List.mem_singleton.2 rfl, hsat z hz⟩

end V182Geo

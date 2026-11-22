import EncBO.ModelO
import EncB.SoundOrbit
import EncB.SoundChain

/-!
# The m-generic clause families under `ModelO`: ψ-order transitivity, nesting units, chains

Copies of ENCBLEAN's `transCl_sound`, `nestLits_sound` (SoundOrbit.lean) and `Chain.base_sound`,
`Chain.ext_sound`, `chainCl_sound` (SoundChain.lean) with `Model` replaced by `ModelO` and each `Model` lemma by its
`O` copy (ModelO.lean). The proof texts are otherwise unchanged; the helpers of `EncB.Orbit`/`EncB.Chain` that do
not mention a model are used as they are.
-/

namespace EncB

theorem holds_nyO {m K t : Nat} (M : ModelO m K t) {i j : Nat} (hi : i < t) (hj : j < t) :
    CodeLitHolds M.τc (-(yLit t i j)) ↔ M.psiLt i j = false := by
  rw [codeLitHolds_neg (Orbit.yLit_ne t i j), holds_yO M hi hj, Bool.not_eq_true]

theorem transCl_soundO {m K t : Nat} (M : ModelO m K t) :
    ∀ cl ∈ transCl t, ∃ x ∈ cl, CodeLitHolds M.τc x := by
  intro cl hcl
  simp only [transCl, List.mem_flatMap, List.mem_cons, List.not_mem_nil, or_false] at hcl
  obtain ⟨⟨i, j, k⟩, hijk, hcl⟩ := hcl
  have hsub := sublist_of_mem_triples hijk
  have hpw := (rng_pairwise 1 t).sublist hsub
  simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq,
    List.Pairwise.nil, and_true] at hpw
  have hk : k ∈ rng 1 t := hsub.subset (by simp)
  rw [mem_rng] at hk
  have hi : i < t := by omega
  have hj : j < t := by omega
  have hk : k < t := hk.2
  rcases hcl with rfl | rfl
  · -- `[-Y(i,j), -Y(j,k), Y(i,k)]`
    cases hij : M.psiLt i j
    · exact ⟨_, List.mem_cons_self, (holds_nyO M hi hj).2 hij⟩
    cases hjk : M.psiLt j k
    · exact ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, (holds_nyO M hj hk).2 hjk⟩
    exact ⟨_, by simp, (holds_yO M hi hk).2 (M.psiLt_trans i j k hij hjk)⟩
  · -- `[Y(i,j), Y(j,k), -Y(i,k)]`
    cases hij : M.psiLt i j
    · cases hjk : M.psiLt j k
      · refine ⟨_, by simp, (holds_nyO M hi hk).2 ?_⟩
        cases hik : M.psiLt i k
        · rfl
        · exfalso
          have hji : M.psiLt j i = true :=
            (M.psiLt_total i j hi hj (by omega)).resolve_left (Bool.eq_false_iff.1 hij)
          have hkj : M.psiLt k j = true :=
            (M.psiLt_total j k hj hk (by omega)).resolve_left (Bool.eq_false_iff.1 hjk)
          have hii := M.psiLt_trans i k i hik (M.psiLt_trans k j i hkj hji)
          rw [M.psiLt_irrefl] at hii
          exact Bool.false_ne_true hii
      · exact ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, (holds_yO M hj hk).2 hjk⟩
    · exact ⟨_, List.mem_cons_self, (holds_yO M hi hj).2 hij⟩

theorem nestLits_soundO {m K t : Nat} (M : ModelO m K t) (hm : 2 ≤ m) :
    ∀ l ∈ nestLits m t, CodeLitHolds M.τc l := by
  intro l hl
  simp only [nestLits, List.mem_flatMap, List.mem_filterMap, mem_rng] at hl
  obtain ⟨i, hi, j, hj, k, hk, h⟩ := hl
  have h0 : PtOk m t (i, 0) := show i < t ∧ 0 < m from ⟨by omega, by omega⟩
  have h1 : PtOk m t (i, 1) := show i < t ∧ 1 < m from ⟨by omega, by omega⟩
  have h2 : PtOk m t (j, k) := show j < t ∧ k < m from ⟨by omega, by omega⟩
  exact ((olitSpecO M (i, 0) (i, 1) (j, k) l h0 h1 h2 h).2).2 (M.nest i j k (by omega) (by omega) (by omega))

namespace Chain

open EncB

/-- Base clause `[F₂(a,b), -l]` with `l = olit (i,0) a b` (copy of `Chain.base_sound`). -/
theorem base_soundO {m K t : Nat} (M : ModelO m K t) {isF : Int → Bool} {i : Nat} (hi : i < t)
    {e : Pt × Pt × Int} (he : e ∈ okList m t i (chainQ m t i) isF) :
    ∃ x ∈ [(fCode m K t i 2 e.1 e.2.1 : Int), -e.2.2], CodeLitHolds M.τc x := by
  obtain ⟨ha, hb, _, hl⟩ := mem_okList he
  have ha' := mem_chainQ.1 ha
  have hb' := mem_chainQ.1 hb
  obtain ⟨hl0, hlh⟩ :=
    olitSpecO M _ _ _ _ (ptOk_pivot hi ha') (ptOk_of_inQ ha') (ptOk_of_inQ hb') hl
  by_cases hc : M.chi (i, 0) e.1 e.2.1 = true
  · refine ⟨_, List.mem_cons_self, ?_⟩
    rw [holds_fO M hi (lt_chainFL (Or.inr (by omega))) (ptOk_of_inQ ha') (ptOk_of_inQ hb')]
    exact chainFrom_two ha' hb' hc
  · refine ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, ?_⟩
    rw [codeLitHolds_neg hl0, hlh]
    exact hc

/-- Extension and closing clauses (copy of `Chain.ext_sound`). -/
theorem ext_soundO {m K t : Nat} (M : ModelO m K t) {isF : Int → Bool} {i lev : Nat} (hi : i < t)
    (hlev : lev ∈ rng 2 (K - 1)) {e : Pt × Pt × Int} (he : e ∈ okList m t i (chainQ m t i) isF)
    {a : Pt} (ha : a ∈ chainQ m t i) {lab lt : Int}
    (hlab : olit m (orbVarC m t) (i, 0) a e.1 = some lab)
    (hlt : olit m (orbVarC m t) a e.1 e.2.1 = some lt) :
    ∃ x ∈ (if lev + 1 < K - 1 then [-(fCode m K t i lev e.1 e.2.1 : Int), -lab, -lt,
                (fCode m K t i (lev + 1) a e.1 : Int)]
            else [-(fCode m K t i lev e.1 e.2.1 : Int), -lab, -lt]), CodeLitHolds M.τc x := by
  obtain ⟨hb, hc, -, -⟩ := mem_okList he
  have ha' := mem_chainQ.1 ha
  have hb' := mem_chainQ.1 hb
  have hc' := mem_chainQ.1 hc
  have hpa := ptOk_of_inQ ha'
  have hpb := ptOk_of_inQ hb'
  have hpc := ptOk_of_inQ hc'
  obtain ⟨hlab0, hlabh⟩ := olitSpecO M _ _ _ _ (ptOk_pivot hi ha') hpa hpb hlab
  obtain ⟨hlt0, hlth⟩ := olitSpecO M _ _ _ _ hpa hpb hpc hlt
  have hlevb := mem_rng.1 hlev
  by_cases h1 : ChainFrom m t M.chi i lev e.1 e.2.1
  · by_cases h2 : M.chi (i, 0) a e.1 = true
    · by_cases h3 : M.chi a e.1 e.2.1 = true
      · have hext := chainFrom_cons h1 ha' h2 h3
        split
        · next hlt' =>
          refine ⟨_, List.mem_cons_of_mem _ (List.mem_cons_of_mem _ (List.mem_cons_of_mem _
            List.mem_cons_self)), ?_⟩
          rw [holds_fO M hi (lt_chainFL (Or.inl hlt')) hpa hpb]
          exact hext
        · next hge =>
          exfalso
          obtain ⟨q, -, -, hQ, hP, hT⟩ := hext
          exact M.noChain i hi q (fun s hs => hQ s (by omega)) (fun s hs => hP s (by omega))
            (fun s hs => hT s (by omega))
      · refine ⟨_, mem_ite3 (Or.inr (Or.inr rfl)), ?_⟩
        rw [codeLitHolds_neg hlt0, hlth]
        exact h3
    · refine ⟨_, mem_ite3 (Or.inr (Or.inl rfl)), ?_⟩
      rw [codeLitHolds_neg hlab0, hlabh]
      exact h2
  · refine ⟨_, mem_ite3 (Or.inl rfl), ?_⟩
    rw [codeLitHolds_neg fCode_ne_zero, holds_fO M hi (lt_chainFL (Or.inl hlevb.2)) hpb hpc]
    exact h1

end Chain

/-- Every chain clause (base, extension, closing) of every pivot holds under `M.τc`, for any `isF`
(copy of `chainCl_sound`). -/
theorem chainCl_soundO {m K t : Nat} (M : ModelO m K t) (isF : Int → Bool) :
    ∀ i ∈ rng 0 t, ∀ cl ∈ chainCl m K t isF i, ∃ x ∈ cl, CodeLitHolds M.τc x := by
  intro i hi cl hcl
  have hit : i < t := (mem_rng.1 hi).2
  simp only [chainCl, List.mem_append, List.mem_map] at hcl
  rcases hcl with ⟨e, he, rfl⟩ | hcl
  · exact Chain.base_soundO M hit he
  · rcases Chain.mem_levels _ _ cl hcl with h | ⟨lev, hlev, keys, hk⟩
    · exact absurd h List.not_mem_nil
    · obtain ⟨e, he, a, ha, lab, lt, -, -, hlab, hlt, rfl⟩ := Chain.mem_extItems hk
      exact Chain.ext_soundO M hit hlev he ha hlab hlt

/-- info: 'EncB.transCl_soundO' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms transCl_soundO

/-- info: 'EncB.nestLits_soundO' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms nestLits_soundO

/-- info: 'EncB.chainCl_soundO' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms chainCl_soundO

end EncB

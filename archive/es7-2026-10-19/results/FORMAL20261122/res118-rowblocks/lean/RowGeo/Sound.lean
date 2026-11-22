import RowGeo.Bridge
import RowGeo.Members
import RowGeo.Geo

/-!
# RowGeo.Sound: an actual residual configuration occupying a support satisfies its row CNF

`missing_of_unsat`: if `rowCnf S` is unsatisfiable (a cake_lpr verdict on its printed text, trust items E1-E3),
then every actual residual configuration (as in `Partition.ResidualBound`) leaves some state of `S` unoccupied.
Proof: otherwise choose owners of the states of `S` (`Coupled.Context`, as `CoupledTemplate.exists_missing_index`
does for 13 states); every raw clause holds in the context (families F1-F10, `raw_holds`), so `decodeWith` of the
context's meaning satisfies `rowCnf S` (`RowGeo.Decode.rowCnf_sat`).
Generic in `S`; nothing is evaluated on a concrete support.
-/

namespace RowGeo
open RowEnc ErdosSzekeres ErdosSzekeres.Omission Coupled

/-- Well-formed supports: strictly increasing state indices below 154, between 1 and 16 of them. -/
def WF (S : List ℕ) : Prop := S.Pairwise (· < ·) ∧ (∀ x ∈ S, x < 154) ∧ S.length ≤ 16 ∧ 0 < S.length

instance (S : List ℕ) : Decidable (WF S) := by unfold WF; infer_instance

def statesOf (S : List ℕ) (h : ∀ x ∈ S, x < 154) : Fin S.length → Fin 154 :=
  fun i => ⟨S[i.val], h _ (List.getElem_mem _)⟩

/-! ## Context-level clause families not in the library -/

section families
variable {k n : ℕ} {states : Fin k → Fin 154} (C : Context k n states)

theorem clause_thresh (cup : Bool) (i j : Fin k) (hij : i ≠ j) (t : ℕ) :
    C.clause [(ge cup i j (t + 1)).neg, ge cup i j t] := by
  simp only [Context.clause_cons, Context.clause_nil, or_false, C.holds_neg, C.holds_ge cup i j hij]
  by_cases h : t ≤ (if cup = true then (C.edge i j).2 else (C.edge i j).1)
  · exact Or.inr h
  · exact Or.inl fun h' => h (by omega)

/-- **F2** in a context. -/
theorem clause_source (u v : Fin k) (huv : u ≠ v) :
    C.clause [(before u v).neg, (ge true u v (h1 (states u) + 2)).neg] := by
  simp only [Context.clause_cons, Context.clause_nil, or_false, C.holds_neg, C.holds_before u v huv,
    C.holds_ge true u v huv, if_true]
  by_contra hcon
  rw [not_or, not_not, not_not] at hcon
  obtain ⟨hlt, hle⟩ := hcon
  have hb := cup_label_le_h1 C.config C.noCap C.noOctagon C.noJunction (C.owner u) (C.owner v) hlt
  rw [C.edge_of_lt hlt] at hle
  rw [C.owner_state u] at hb
  have e : h1 (states u) = (ResidualDomains.shape (states u)).getD 0 0 := by
    unfold h1; rw [st_eq_shape]
  omega

/-- **F7** in a context, positive case. -/
theorem clause_fixed_pos (i j l : Fin k) (hij : i ≠ j) (hjl : j ≠ l) (hil : i ≠ l)
    (h : ttB (states i) (states j) (states l) = true) : C.clause [positive i j l] := by
  simp only [Context.clause_cons, Context.clause_nil, or_false, C.holds_positive i j l hij hil hjl]
  apply positive_of_ttB C.config C.noCap C.noOctagon C.noJunction (C.owner i) (C.owner j) (C.owner l)
    (C.injective.ne hij) (C.injective.ne hjl) (C.injective.ne hil)
  simpa only [C.owner_state] using h

/-- **F7** in a context, negative case. -/
theorem clause_fixed_neg (i j l : Fin k) (hij : i ≠ j) (hjl : j ≠ l) (hil : i ≠ l)
    (h : ttB (states i) (states l) (states j) = true) : C.clause [(positive i j l).neg] := by
  have hp := clause_fixed_pos C i l j hil hjl.symm hij h
  simp only [Context.clause_cons, Context.clause_nil, or_false, C.holds_positive i l j hil hij hjl.symm,
    orient_swap (C.point i) (C.point j) (C.point l)] at hp
  simp only [Context.clause_cons, Context.clause_nil, or_false, C.holds_neg,
    C.holds_positive i j l hij hil hjl]
  linarith

end families

/-! ## The raw clauses of a support hold in its context -/

section raw
variable {S : List ℕ} (hS : WF S) {n : ℕ} (C : Context S.length n (statesOf S hS.2.1))

include hS in
theorem states_fk {u : ℕ} (hu : u < S.length) :
    ((statesOf S hS.2.1 (fk hS.2.2.2 u)) : ℕ) = S.getD u 0 := by
  simp only [statesOf, fk_eq hS.2.2.2 hu, List.getD_eq_getElem _ _ hu]

theorem fk_ne {k : ℕ} (hk : 0 < k) {u v : ℕ} (hu : u < k) (hv : v < k) (h : u ≠ v) : fk hk u ≠ fk hk v :=
  fun e => h (by have := congrArg Fin.val e; rwa [fk_val hk hu, fk_val hk hv] at this)

theorem dir_holds {u v : ℕ} (hu : u < S.length) (hv : v < S.length) (huv : u ≠ v) :
    ∀ cl ∈ dirPart S u v, C.clause (cl.map (toExpr hS.2.2.2)) := by
  have hk := hS.2.2.2
  have h16 := hS.2.2.1
  have hne := fk_ne hk hu hv huv
  intro cl hcl
  unfold dirPart at hcl
  rcases List.mem_cons.1 hcl with rfl | hcl
  · have := clause_source C (fk hk u) (fk hk v) hne
    rw [states_fk hS hu] at this
    simpa only [sourceClause, List.map_cons, List.map_nil, toExpr_neg, toExpr_befL hk h16 hu hv,
      toExpr_geL hk h16 true hu hv] using this
  · split at hcl
    · next he =>
      rw [List.mem_singleton] at hcl; subst hcl
      have he' : emptyB (statesOf S hS.2.1 (fk hk u)) (statesOf S hS.2.1 (fk hk v)) = true := by
        rw [states_fk hS hu, states_fk hS hv]; exact he
      simpa only [emptyClause, List.map_cons, List.map_nil, toExpr_neg, toExpr_befL hk h16 hu hv] using
        C.empty_clause (fk hk u) (fk hk v) hne (emptyB_spec _ _ _ he')
    · obtain ⟨z, hz, rfl⟩ := List.mem_map.1 hcl
      have hz' := (List.mem_filter.1 hz).2
      have hna : ¬ Allowed (statesOf S hS.2.1) (fk hk u) (fk hk v) (z.1, z.2) := by
        intro ha
        have := (allowedB_iff (statesOf S hS.2.1) (fk hk u) (fk hk v) (z.1, z.2)).2 ha
        rw [states_fk hS hu, states_fk hS hv, Prod.mk.eta] at this
        rw [this] at hz'
        exact absurd hz' (by decide)
      simpa only [RowEnc.domainClause, Coupled.domainClause, List.map_cons, List.map_nil, toExpr_neg,
        toExpr_befL hk h16 hu hv, toExpr_geL hk h16 _ hu hv] using
        C.domain_clause (fk hk u) (fk hk v) hne z.1 z.2 hna

theorem pair_holds : ∀ cl ∈ pairPart S, C.clause (cl.map (toExpr hS.2.2.2)) := by
  have hk := hS.2.2.2
  have h16 := hS.2.2.1
  intro cl hcl
  obtain ⟨p, hp, hcl⟩ := List.mem_flatMap.1 hcl
  rcases p with _ | ⟨i, _ | ⟨j, _ | ⟨x, t⟩⟩⟩ <;> simp only [List.not_mem_nil] at hcl
  obtain ⟨hij, hjk⟩ := pair_facts hp
  have hik : i < S.length := lt_trans hij hjk
  have hne := fk_ne hk hik hjk (Nat.ne_of_lt hij)
  simp only [pairClauses, List.mem_append, List.mem_cons, List.not_mem_nil, or_false] at hcl
  have th : ∀ cup t, C.clause ((threshClause cup i j t).map (toExpr hk)) := fun cup t => by
    simpa only [threshClause, List.map_cons, List.map_nil, toExpr_neg, toExpr_geL hk h16 cup hik hjk] using
      clause_thresh C cup (fk hk i) (fk hk j) hne t
  rcases hcl with ((rfl | rfl | rfl | rfl | rfl | rfl) | h) | h
  all_goals first
    | exact th _ _
    | exact dir_holds hS C hik hjk (Nat.ne_of_lt hij) _ h
    | exact dir_holds hS C hjk hik (Nat.ne_of_lt hij).symm _ h

theorem triple_holds : ∀ cl ∈ triplePart S.length, C.clause (cl.map (toExpr hS.2.2.2)) := by
  have hk := hS.2.2.2
  have h16 := hS.2.2.1
  intro cl hcl
  obtain ⟨⟨a, b, c⟩, ht, hcl⟩ := List.mem_flatMap.1 hcl
  obtain ⟨ha, hb, hc, hab, hac, hbc⟩ := perm3_facts ht
  have n1 := fk_ne hk ha hb hab
  have n2 := fk_ne hk hb hc hbc
  have n3 := fk_ne hk ha hc hac
  simp only [tripleClauses, List.mem_cons, List.mem_append, List.mem_map, List.not_mem_nil, or_false] at hcl
  rcases hcl with rfl | ⟨t, -, rfl⟩ | ⟨t, -, rfl⟩
  · simpa only [transClause, List.map_cons, List.map_nil, toExpr_neg, toExpr_befL hk h16 ha hb,
      toExpr_befL hk h16 hb hc, toExpr_befL hk h16 ha hc] using
      C.transitive_clause (fk hk a) (fk hk b) (fk hk c) n1 n2 n3
  · simpa only [RowEnc.growthClause, Coupled.growthClause, List.map_cons, List.map_nil, toExpr_neg,
      toExpr_befL hk h16 ha hb, toExpr_befL hk h16 hb hc, toExpr_posL hk h16 ha hb hc,
      toExpr_geL hk h16 _ ha hb, toExpr_geL hk h16 _ hb hc, Bool.false_eq_true, if_false] using
      C.growth_clause false (fk hk a) (fk hk b) (fk hk c) n1 n2 n3 t
  · simpa only [RowEnc.growthClause, Coupled.growthClause, List.map_cons, List.map_nil, toExpr_neg,
      toExpr_befL hk h16 ha hb, toExpr_befL hk h16 hb hc, toExpr_posL hk h16 ha hb hc,
      toExpr_geL hk h16 _ ha hb, toExpr_geL hk h16 _ hb hc, if_true] using
      C.growth_clause true (fk hk a) (fk hk b) (fk hk c) n1 n2 n3 t

theorem fixed_holds : ∀ cl ∈ fixedPart S, C.clause (cl.map (toExpr hS.2.2.2)) := by
  have hk := hS.2.2.2
  have h16 := hS.2.2.1
  intro cl hcl
  obtain ⟨q, hq, hcl⟩ := List.mem_flatMap.1 hcl
  rcases q with _ | ⟨i, _ | ⟨j, _ | ⟨l, _ | ⟨x, t⟩⟩⟩⟩ <;> simp only [List.not_mem_nil] at hcl
  obtain ⟨hij, hjl, hlk⟩ := triple_facts hq
  have hjk : j < S.length := lt_trans hjl hlk
  have hik : i < S.length := lt_trans hij hjk
  have n1 := fk_ne hk hik hjk (Nat.ne_of_lt hij)
  have n2 := fk_ne hk hjk hlk (Nat.ne_of_lt hjl)
  have n3 := fk_ne hk hik hlk (Nat.ne_of_lt (lt_trans hij hjl))
  unfold fixedClauses at hcl
  split at hcl
  · next h =>
    rw [List.mem_singleton] at hcl; subst hcl
    rw [← states_fk hS hik, ← states_fk hS hjk, ← states_fk hS hlk] at h
    simpa only [List.map_cons, List.map_nil, toExpr_posL hk h16 hik hjk hlk] using
      clause_fixed_pos C _ _ _ n1 n2 n3 h
  · split at hcl
    · next h =>
      rw [List.mem_singleton] at hcl; subst hcl
      rw [← states_fk hS hik, ← states_fk hS hjk, ← states_fk hS hlk] at h
      simpa only [List.map_cons, List.map_nil, toExpr_neg, toExpr_posL hk h16 hik hjk hlk] using
        clause_fixed_neg C _ _ _ n1 n2 n3 h
    · simp at hcl

theorem quad_holds : ∀ cl ∈ quadPart S.length, C.clause (cl.map (toExpr hS.2.2.2)) := by
  have hk := hS.2.2.2
  have h16 := hS.2.2.1
  intro cl hcl
  obtain ⟨q, hq, hcl⟩ := List.mem_flatMap.1 hcl
  rcases q with _ | ⟨a, _ | ⟨b, _ | ⟨c, _ | ⟨d, _ | ⟨x, t⟩⟩⟩⟩⟩ <;> simp only [List.not_mem_nil] at hcl
  obtain ⟨hab, hbc, hcd, hdk⟩ := quad_facts hq
  have hck : c < S.length := lt_trans hcd hdk
  have hbk : b < S.length := lt_trans hbc hck
  have hak : a < S.length := lt_trans hab hbk
  unfold quadClauses at hcl
  rcases List.mem_append.1 hcl with hcl | hcl
  · obtain ⟨⟨q0, q1, q2, q3⟩, hp, hcl⟩ := List.mem_flatMap.1 hcl
    obtain ⟨⟨x, y, z, w⟩, hx, rfl⟩ := List.mem_map.1 hcl
    obtain ⟨d01, d02, d03, d12, d13, d23, l0, l1, l2, l3⟩ := perm4_facts hab hbc hcd hp
    simp only at d01 d02 d03 d12 d13 d23 l0 l1 l2 l3
    have k0 : q0 < S.length := by omega
    have k1 : q1 < S.length := by omega
    have k2 : q2 < S.length := by omega
    have k3 : q3 < S.length := by omega
    simpa only [RowEnc.packetClause, Coupled.packetClause, List.map_cons, List.map_nil, toExpr_neg,
      toExpr_disagreeL, toExpr_befL hk h16 k0 k1, toExpr_befL hk h16 k1 k2, toExpr_befL hk h16 k2 k3,
      toExpr_posL hk h16 k0 k1 k2, toExpr_posL hk h16 k0 k1 k3, toExpr_posL hk h16 k0 k2 k3,
      toExpr_posL hk h16 k1 k2 k3] using
      C.packet_clause (fk hk q0) (fk hk q1) (fk hk q2) (fk hk q3) (fk_ne hk k0 k1 d01) (fk_ne hk k0 k2 d02)
        (fk_ne hk k0 k3 d03) (fk_ne hk k1 k2 d12) (fk_ne hk k1 k3 d13) (fk_ne hk k2 k3 d23) x y z w
        (bad4_invalid _ hx)
  · obtain ⟨⟨x, y, z, w⟩, -, rfl⟩ := List.mem_map.1 hcl
    simpa only [RowEnc.convexClause, Coupled.convexClause, List.map_cons, List.map_nil, toExpr_disagreeL,
      toExpr_posL hk h16 hak hbk hck, toExpr_posL hk h16 hak hbk hdk, toExpr_posL hk h16 hak hck hdk,
      toExpr_posL hk h16 hbk hck hdk, toExpr_cvx hk h16 hak hbk hck hdk] using
      C.convex_clause (fk hk a) (fk hk b) (fk hk c) (fk hk d) (fk_ne hk hak hbk (Nat.ne_of_lt hab))
        (fk_ne hk hak hck (by omega)) (fk_ne hk hak hdk (by omega)) (fk_ne hk hbk hck (Nat.ne_of_lt hbc))
        (fk_ne hk hbk hdk (by omega)) (fk_ne hk hck hdk (Nat.ne_of_lt hcd)) x y z w

theorem oct_holds : ∀ cl ∈ octPart S.length, C.clause (cl.map (toExpr hS.2.2.2)) := by
  classical
  have hk := hS.2.2.2
  have h16 := hS.2.2.1
  intro cl hcl
  obtain ⟨eight, h8, rfl⟩ := List.mem_map.1 hcl
  obtain ⟨hp, hm, hl⟩ := range_facts h8
  have hinj : ∀ x ∈ eight, ∀ y ∈ eight, fk hk x = fk hk y → x = y := fun x hx y hy e => by
    have := congrArg Fin.val e; rwa [fk_val hk (hm x hx), fk_val hk (hm y hy)] at this
  have hnd : (eight.map (fk hk)).Nodup :=
    List.Nodup.map_on hinj (hp.imp fun h => Nat.ne_of_lt h)
  apply C.no_octagon_clause (eight.map (fk hk)).toFinset (by rw [List.toFinset_card_of_nodup hnd]; simp [hl])
  intro i hi j hj l hl' m hm' hij hjl hlm
  simp only [List.mem_toFinset, List.mem_map] at hi hj hl' hm'
  obtain ⟨x, hx, rfl⟩ := hi
  obtain ⟨y, hy, rfl⟩ := hj
  obtain ⟨z, hz, rfl⟩ := hl'
  obtain ⟨w, hw, rfl⟩ := hm'
  rw [fk_lt_iff hk (hm x hx) (hm y hy)] at hij
  rw [fk_lt_iff hk (hm y hy) (hm z hz)] at hjl
  rw [fk_lt_iff hk (hm z hz) (hm w hw)] at hlm
  have hpw : [x, y, z, w].Pairwise (· < ·) := by
    simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq,
      List.Pairwise.nil, and_true, false_implies, implies_true]
    omega
  have hsub : [x, y, z, w] ∈ combs 4 eight :=
    combs_of_sublist (sublist_of_sorted hp hpw (by simp [hx, hy, hz, hw])) rfl
  refine List.mem_map.2 ⟨cvxLit [x, y, z, w], List.mem_map.2 ⟨_, hsub, rfl⟩, ?_⟩
  simp only [cvxLit]
  exact toExpr_cvx hk h16 (hm x hx) (hm y hy) (hm z hz) (hm w hw) false

theorem raw_holds : ∀ cl ∈ rawClauses S, C.clause (cl.map (toExpr hS.2.2.2)) := by
  intro cl hcl
  simp only [rawClauses, List.mem_append] at hcl
  rcases hcl with (((h | h) | h) | h) | h
  · exact pair_holds hS C cl h
  · exact triple_holds hS C cl h
  · exact fixed_holds hS C cl h
  · exact quad_holds hS C cl h
  · exact oct_holds hS C cl h

end raw

/-! ## The soundness theorem -/

theorem statesOf_injective (S : List ℕ) (hS : WF S) : Function.Injective (statesOf S hS.2.1) := by
  intro i j h
  have h' : S[i] = S[j] := congrArg Fin.val h
  exact Fin.ext ((List.Nodup.getElem_inj_iff (hS.1.imp fun h => Nat.ne_of_lt h)).1 h')

/-- **Soundness of the coupled-row CNF.** If `rowCnf S` is unsatisfiable, every actual residual configuration
leaves some state of `S` unoccupied. -/
theorem missing_of_unsat (S : List ℕ) (hS : WF S) (hU : ¬ EncB.DimacsSatisfiable (rowCnf S))
    {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ i : Fin S.length, statesOf S hS.2.1 i ∉ c.residualOccupied noCap noOctagon noJunction := by
  classical
  by_contra! h
  have selected : ∀ i : Fin S.length, ∃ v : Fin n,
      c.residualOwner noCap noOctagon noJunction v = statesOf S hS.2.1 i := by
    intro i
    obtain ⟨v, _, hv⟩ := Finset.mem_image.mp (h i)
    exact ⟨v, hv⟩
  choose owner owner_state using selected
  have owner_injective : Function.Injective owner := by
    intro i j he
    apply statesOf_injective S hS
    rw [← owner_state i, ← owner_state j, he]
  let C : Context S.length n (statesOf S hS.2.1) := {
    config := c, noCap := noCap, noOctagon := noOctagon, noJunction := noJunction,
    owner := owner, injective := owner_injective, owner_state := owner_state,
    nonzero := fun i j l hij hil hjl => c.orient_ne_of_distinct _ _ _
      (owner_injective.ne hij) (owner_injective.ne hil) (owner_injective.ne hjl) }
  exact hU ⟨_, rowCnf_sat S (μ hS.2.2.2 C) fun cl hcl => lsem_of_clause hS.2.2.2 C cl (raw_holds hS C cl hcl)⟩

end RowGeo

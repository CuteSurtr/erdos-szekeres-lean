import ErdosSzekeres.Omission.CoupledSemantics
import ErdosSzekeres.VisibleEdgeInsertion

/-!
A structural geometric proof of the nine-state residual obstruction. The
shared heptagon has two possible extensions. Shared pair-rank growth handles
one chronological case; a four-point orientation packet handles the other.
Only the local finite state-domain and sign tests are computed. The proof
never invokes the literal nine-state CNF/LRAT refutation.
-/

namespace ErdosSzekeres.Omission.StructuralNine111
open Coupled
open VisibleEdgeInsertion
set_option maxHeartbeats 200000
set_option maxRecDepth 10000

def states : Fin 9 → Fin 154 := ![33,43,64,68,75,87,91,99,111]
def qList : List (Fin 9) := [1,2,4,5,6,7,8]
def edgeList : List (Fin 9 × Fin 9) := [(1,2),(2,4),(4,5),(5,7),(7,8),(8,6),(6,1)]
def qIds : Finset (Fin 9) := {1,2,4,5,6,7,8}
def edgeIds : Finset (Fin 9 × Fin 9) := {(1,2),(2,4),(4,5),(5,7),(7,8),(8,6),(6,1)}

variable {n : ℕ} (C : Context 9 n states)

private theorem pos (i j k : Fin 9) (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k)
    (checked : CycleSigns.CheckTriple ResidualDomains.computedTable
      (states i) (states j) (states k) = true) :
    0 < orient (C.point i) (C.point j) (C.point k) := by
  have h := C.fixed_positive i j k hij hjk hik checked
  simpa only [Context.clause_cons, Context.clause_nil, or_false,
    C.holds_positive i j k hij hik hjk] using h

private theorem before (i j : Fin 9) (hij : i ≠ j)
    (checked : emptyCheck states j i = true) : C.owner i < C.owner j := by
  have h := C.empty_clause j i hij.symm checked
  have hnot : ¬ C.owner j < C.owner i := by
    simpa only [Context.clause_cons, Context.clause_nil, or_false,
      Context.holds_neg, C.holds_before j i hij.symm] using h
  have hne := C.injective.ne hij
  exact lt_of_le_of_ne (le_of_not_gt hnot) hne

private def labelCheck (i j : Fin 9) (test : StateInterface.Label → Bool) : Bool :=
  ResidualDomains.grid.all (fun z => !(decide (Allowed states i j z)) || test z)

private theorem label_checked (i j : Fin 9) (hij : i ≠ j) (h : C.owner i < C.owner j)
    (test : StateInterface.Label → Bool) (checked : labelCheck i j test = true) :
    test (C.edge i j) = true := by
  have ht := List.all_eq_true.mp checked (C.edge i j)
    (ResidualDomains.mem_grid _ (C.edge_bounds hij))
  have ha := C.edge_allowed h
  simpa [ha] using ht

private theorem checksBool : (edgeList.all (fun e =>
    decide (e.1 ∈ qIds ∧ e.2 ∈ qIds ∧ e.1 ≠ e.2) &&
    qList.all (fun k => decide (k = e.1 ∨ k = e.2) ||
      CycleSigns.CheckTriple ResidualDomains.computedTable
        (states e.1) (states e.2) (states k)))) = true := by decide +kernel

private theorem checks : ∀ i j : Fin 9, (i,j) ∈ edgeIds →
    i ∈ qIds ∧ j ∈ qIds ∧ i ≠ j ∧
    ∀ k ∈ qIds, k ≠ i → k ≠ j →
      CycleSigns.CheckTriple ResidualDomains.computedTable
        (states i) (states j) (states k) = true := by
  intro i j hij
  have h := List.all_eq_true.mp checksBool (i,j) (by simpa [edgeList,edgeIds] using hij)
  obtain ⟨h1,h2⟩ := Bool.and_eq_true_iff.mp h
  obtain ⟨hi,hj,hne⟩ := of_decide_eq_true h1
  refine ⟨hi,hj,hne,?_⟩
  intro k hk hki hkj
  have h := List.all_eq_true.mp h2 k (by simpa [qList,qIds] using hk)
  simpa [hki,hkj] using h

private theorem coverage : ∀ p ∈ qIds, ∃ e ∈ edgeIds,
    e ≠ (6,1) ∧ (p = e.1 ∨ p = e.2) := by decide +kernel

private theorem original_supports : SupportsOnLeft (qIds.image C.point)
    (edgeIds.image (fun e : Fin 9 × Fin 9 => (C.point e.1, C.point e.2))) := by
  classical
  rintro e he
  obtain ⟨⟨i,j⟩, hij, rfl⟩ := Finset.mem_image.mp he
  obtain ⟨hi, hj, hne, signs⟩ := checks i j hij
  have inj : Function.Injective C.point := C.config.point_injective.comp C.injective
  refine ⟨Finset.mem_image_of_mem _ hi, Finset.mem_image_of_mem _ hj, inj.ne hne, ?_⟩
  intro r hr hri hrj
  obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp hr
  have hki : k ≠ i := fun h => hri (congrArg C.point h)
  have hkj : k ≠ j := fun h => hrj (congrArg C.point h)
  exact pos C i j k hne hki.symm hkj.symm (signs k hk hki hkj)

set_option maxHeartbeats 200000 in
private theorem insert_convex (x : Fin 9)
    (outside : orient (C.point 6) (C.point 1) (C.point x) < 0)
    (inside : ∀ i j : Fin 9, (i,j) ∈ edgeIds → (i,j) ≠ (6,1) →
      0 < orient (C.point i) (C.point j) (C.point x)) :
    ConvexPosition (insert (C.point x) (qIds.image C.point)) := by
  classical
  have inj : Function.Injective C.point := C.config.point_injective.comp C.injective
  have hvisible : (C.point 6, C.point 1) ∈
      edgeIds.image (fun e : Fin 9 × Fin 9 => (C.point e.1, C.point e.2)) := by
    exact Finset.mem_image.mpr ⟨(6,1), by decide, rfl⟩
  refine convexPosition_insert_of_one_visible_edge (qIds.image C.point)
    (edgeIds.image (fun e : Fin 9 × Fin 9 => (C.point e.1, C.point e.2))) (C.point x) (C.point 6) (C.point 1)
    (original_supports C) hvisible outside ?_ ?_
  · intro e he hne
    obtain ⟨⟨i,j⟩, hij, rfl⟩ := Finset.mem_image.mp he
    apply inside i j hij
    intro h
    apply hne
    exact congrArg (fun e : Fin 9 × Fin 9 => (C.point e.1, C.point e.2)) h
  · intro p hp
    obtain ⟨k,hk,rfl⟩ := Finset.mem_image.mp hp
    obtain ⟨⟨i,j⟩,he,hne,hk⟩ := coverage k hk
    refine ⟨(C.point i,C.point j),Finset.mem_image.mpr ⟨(i,j),he,rfl⟩,?_,?_⟩
    · intro h
      apply hne
      exact Prod.ext (inj (congrArg Prod.fst h)) (inj (congrArg Prod.snd h))
    · rcases hk with hk | hk
      · exact Or.inl (congrArg C.point hk)
      · exact Or.inr (congrArg C.point hk)

private def extraTriples : Finset (Fin 9 × Fin 9 × Fin 9) :=
  {(0,1,2),(0,2,4),(0,4,5),(0,5,7),(0,7,8),
   (1,2,3),(2,4,3),(4,5,3),(5,7,3),(7,8,3),(8,6,3),
   (3,7,6),(3,1,7),(6,1,7)}

private def extraList : List (Fin 9 × Fin 9 × Fin 9) :=
  [(0,1,2),(0,2,4),(0,4,5),(0,5,7),(0,7,8),
   (1,2,3),(2,4,3),(4,5,3),(5,7,3),(7,8,3),(8,6,3),
   (3,7,6),(3,1,7),(6,1,7)]

private theorem extraChecksBool : (extraList.all (fun t =>
    decide (t.1 ≠ t.2.1 ∧ t.1 ≠ t.2.2 ∧ t.2.1 ≠ t.2.2) &&
    CycleSigns.CheckTriple ResidualDomains.computedTable
      (states t.1) (states t.2.1) (states t.2.2))) = true := by decide +kernel

private theorem extraChecks : ∀ t ∈ extraTriples,
    t.1 ≠ t.2.1 ∧ t.1 ≠ t.2.2 ∧ t.2.1 ≠ t.2.2 ∧
    CycleSigns.CheckTriple ResidualDomains.computedTable
      (states t.1) (states t.2.1) (states t.2.2) = true := by
  intro t ht
  have h := List.all_eq_true.mp extraChecksBool t (by simpa [extraTriples,extraList] using ht)
  obtain ⟨h1,h2⟩ := Bool.and_eq_true_iff.mp h
  obtain ⟨hi,hj,hk⟩ := of_decide_eq_true h1
  exact ⟨hi,hj,hk,h2⟩

private theorem extra (i j k : Fin 9) (h : (i,j,k) ∈ extraTriples) :
    0 < orient (C.point i) (C.point j) (C.point k) := by
  obtain ⟨hij,hik,hjk,checked⟩ := extraChecks (i,j,k) h
  exact pos C i j k hij hik hjk checked

private theorem first_case (hbg : C.owner 1 < C.owner 6) :
    ConvexPosition (insert (C.point 0) (qIds.image C.point)) := by
  have hab := before C 0 1 (by decide) (by decide +kernel)
  have hgi := before C 6 8 (by decide) (by decide +kernel)
  have hag := hab.trans hbg
  have capEq : (C.edge 0 1).1 = 4 := by
    exact of_decide_eq_true (label_checked C 0 1 (by decide) hab
      (fun z => decide (z.1 = 4)) (by decide +kernel))
  have cupLower : 2 ≤ (C.edge 0 6).2 := by
    exact of_decide_eq_true (label_checked C 0 6 (by decide) hag
      (fun z => decide (2 ≤ z.2)) (by decide +kernel))
  have cupUpper : (C.edge 6 8).2 ≤ 2 := by
    exact of_decide_eq_true (label_checked C 6 8 (by decide) hgi
      (fun z => decide (z.2 ≤ 2)) (by decide +kernel))
  have habg : 0 < orient (C.point 0) (C.point 1) (C.point 6) := by
    have grow := C.growth_clause false 0 1 6 (by decide) (by decide) (by decide) 4
    have upper := C.edge_bounds (i := 1) (j := 6) (by decide)
    have no5 : ¬ 5 ≤ (C.edge 1 6).1 := by omega
    simpa [growthClause, Context.clause_cons, Context.clause_nil,
      Context.holds_neg, C.holds_before 0 1 (by decide),
      C.holds_before 1 6 (by decide), C.holds_positive 0 1 6 (by decide) (by decide) (by decide),
      C.holds_ge false 0 1 (by decide) 4, C.holds_ge false 1 6 (by decide) 5,
      hab, hbg, capEq, no5] using grow
  have hagi : orient (C.point 0) (C.point 6) (C.point 8) < 0 := by
    have grow := C.growth_clause true 0 6 8 (by decide) (by decide) (by decide) 2
    have no3 : ¬ 3 ≤ (C.edge 6 8).2 := by omega
    have hnot : ¬ 0 < orient (C.point 0) (C.point 6) (C.point 8) := by
      simpa [growthClause, Context.clause_cons, Context.clause_nil,
        Context.holds_neg, C.holds_before 0 6 (by decide),
        C.holds_before 6 8 (by decide), C.holds_positive 0 6 8 (by decide) (by decide) (by decide),
        C.holds_ge true 0 6 (by decide) 2, C.holds_ge true 6 8 (by decide) 3,
        hag, hgi, cupLower, no3] using grow
    have nz := C.nonzero 0 6 8 (by decide) (by decide) (by decide)
    exact lt_of_le_of_ne (le_of_not_gt hnot) nz
  apply insert_convex C 0
  · have eq : orient (C.point 6) (C.point 1) (C.point 0) =
        -orient (C.point 0) (C.point 1) (C.point 6) := by simp only [orient]; ring
    rw [eq]; linarith
  · intro i j he hne
    simp only [edgeIds, Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he | he | he | he | he | he
    all_goals have hi := congrArg Prod.fst he; have hj := congrArg Prod.snd he
    all_goals dsimp only at hi hj; subst i; subst j
    · simpa only [orient_cycle] using extra C 0 1 2 (by decide)
    · simpa only [orient_cycle] using extra C 0 2 4 (by decide)
    · simpa only [orient_cycle] using extra C 0 4 5 (by decide)
    · simpa only [orient_cycle] using extra C 0 5 7 (by decide)
    · simpa only [orient_cycle] using extra C 0 7 8 (by decide)
    · have eq : orient (C.point 8) (C.point 6) (C.point 0) =
          -orient (C.point 0) (C.point 6) (C.point 8) := by simp only [orient]; ring
      rw [eq]; linarith
    · exact False.elim (hne rfl)

private theorem second_case (hgb : C.owner 6 < C.owner 1) :
    ConvexPosition (insert (C.point 3) (qIds.image C.point)) := by
  have hdg := before C 3 6 (by decide) (by decide +kernel)
  have hbh := before C 1 7 (by decide) (by decide +kernel)
  have hx1 : (C.point 3) 0 < (C.point 6) 0 := C.config.xOrder hdg
  have hx2 : (C.point 6) 0 < (C.point 1) 0 := C.config.xOrder hgb
  have hx3 : (C.point 1) 0 < (C.point 7) 0 := C.config.xOrder hbh
  have hdgh : orient (C.point 3) (C.point 6) (C.point 7) < 0 := by
    have h := extra C 3 7 6 (by decide)
    rw [orient_swap] at h
    linarith
  have hdbh := extra C 3 1 7 (by decide)
  have hgbh := extra C 6 1 7 (by decide)
  have pack := packetValid_of_xordered (C.point 3) (C.point 6) (C.point 1) (C.point 7)
    hx1 hx2 hx3
  have hnot : ¬0 < orient (C.point 3) (C.point 6) (C.point 1) := by
    intro h
    simp [PacketValid, h, hdbh, hgbh, not_lt.mpr hdgh.le] at pack
  have hdgb : orient (C.point 3) (C.point 6) (C.point 1) < 0 :=
    lt_of_le_of_ne (le_of_not_gt hnot) (C.nonzero 3 6 1 (by decide) (by decide) (by decide))
  apply insert_convex C 3
  · simpa only [orient_cycle] using hdgb
  · intro i j he hne
    simp only [edgeIds, Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he | he | he | he | he | he
    all_goals have hi := congrArg Prod.fst he; have hj := congrArg Prod.snd he
    all_goals dsimp only at hi hj; subst i; subst j
    · exact extra C 1 2 3 (by decide)
    · exact extra C 2 4 3 (by decide)
    · exact extra C 4 5 3 (by decide)
    · exact extra C 5 7 3 (by decide)
    · exact extra C 7 8 3 (by decide)
    · exact extra C 8 6 3 (by decide)
    · exact False.elim (hne rfl)

private theorem octagon_contradiction (x : Fin 9) (hx : x ∉ qIds)
    (convex : ConvexPosition (insert (C.point x) (qIds.image C.point))) : False := by
  classical
  have inj : Function.Injective C.point := C.config.point_injective.comp C.injective
  have hnot : C.point x ∉ qIds.image C.point := by
    intro h
    obtain ⟨y,hy,he⟩ := Finset.mem_image.mp h
    exact hx ((inj he) ▸ hy)
  apply C.noOctagon
  refine ⟨insert (C.point x) (qIds.image C.point), ?_, ?_, convex⟩
  · intro p hp
    rcases Finset.mem_insert.mp hp with hpx | hp
    · rw [hpx]
      exact Finset.mem_image_of_mem _ (Finset.mem_univ (C.owner x))
    · obtain ⟨y,_,rfl⟩ := Finset.mem_image.mp hp
      exact Finset.mem_image_of_mem _ (Finset.mem_univ (C.owner y))
  · rw [Finset.card_insert_of_notMem hnot,Finset.card_image_of_injective _ inj]
    decide

/-- Structural proof for these nine residual states, using shared
pair-rank growth, one four-point packet, and visible-edge insertion. It does
not import the literal CNF/LRAT theorem. The Context assumptions are explicit. -/
theorem context_impossible_structural (C : Context 9 n states) : False := by
  rcases lt_or_gt_of_ne (C.injective.ne (by decide : (1 : Fin 9) ≠ 6)) with h | h
  · exact octagon_contradiction C 0 (by decide) (first_case C h)
  · exact octagon_contradiction C 3 (by decide) (second_case C h)

def support : Finset (Fin 154) := {33,43,64,68,75,87,91,99,111}

theorem states_injective : Function.Injective states := by decide +kernel

private theorem states_mem_support : ∀ i : Fin 9, states i ∈ support := by decide +kernel

/-- The structural proof applies to actual owners in one residual real
configuration. No certificate or further realization premise is required. -/
theorem exists_missing_state {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ s ∈ support, s ∉ c.residualOccupied noCap noOctagon noJunction := by
  classical
  by_contra! h
  have selected : ∀ i : Fin 9, ∃ v : Fin n,
      c.residualOwner noCap noOctagon noJunction v = states i := by
    intro i
    obtain ⟨v, _, hv⟩ := Finset.mem_image.mp (h (states i) (states_mem_support i))
    exact ⟨v, hv⟩
  choose owner owner_state using selected
  have injective : Function.Injective owner := by
    intro i j he
    apply states_injective
    rw [← owner_state i, ← owner_state j, he]
  let C : Context 9 n states := {
    config := c, noCap := noCap, noOctagon := noOctagon, noJunction := noJunction,
    owner := owner, injective := injective, owner_state := owner_state,
    nonzero := fun i j l hij hil hjl => c.orient_ne_of_distinct _ _ _
      (injective.ne hij) (injective.ne hil) (injective.ne hjl) }
  exact context_impossible_structural C

/-- A demand-one omission row proved through the structural geometric route. -/
theorem hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    1 ≤ (support \ c.residualOccupied noCap noOctagon noJunction).card := by
  classical
  obtain ⟨s, hs, hmissing⟩ := exists_missing_state c noCap noOctagon noJunction
  exact Finset.one_le_card.mpr ⟨s, Finset.mem_sdiff.mpr ⟨hs, hmissing⟩⟩

#print axioms context_impossible_structural
#print axioms states_injective
#print axioms exists_missing_state
#print axioms hole_bound

end ErdosSzekeres.Omission.StructuralNine111

/-!
A structural geometric proof of the nine-state residual obstruction. The
shared heptagon has two possible extensions. Shared pair-rank growth handles
one chronological case; a four-point orientation packet handles the other.
Only the local finite state-domain and sign tests are computed. The proof
never invokes the literal nine-state CNF/LRAT refutation.
-/

namespace ErdosSzekeres.Omission.StructuralNineShifted111
open Coupled
open VisibleEdgeInsertion
set_option maxHeartbeats 200000
set_option maxRecDepth 10000

def states : Fin 9 → Fin 154 := ![44,53,64,68,75,87,91,99,111]
def qList : List (Fin 9) := [1,2,4,5,6,7,8]
def edgeList : List (Fin 9 × Fin 9) := [(1,2),(2,4),(4,5),(5,7),(7,8),(8,6),(6,1)]
def qIds : Finset (Fin 9) := {1,2,4,5,6,7,8}
def edgeIds : Finset (Fin 9 × Fin 9) := {(1,2),(2,4),(4,5),(5,7),(7,8),(8,6),(6,1)}

variable {n : ℕ} (C : Context 9 n states)

private theorem pos (i j k : Fin 9) (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k)
    (checked : CycleSigns.CheckTriple ResidualDomains.computedTable
      (states i) (states j) (states k) = true) :
    0 < orient (C.point i) (C.point j) (C.point k) := by
  have h := C.fixed_positive i j k hij hjk hik checked
  simpa only [Context.clause_cons, Context.clause_nil, or_false,
    C.holds_positive i j k hij hik hjk] using h

private theorem before (i j : Fin 9) (hij : i ≠ j)
    (checked : emptyCheck states j i = true) : C.owner i < C.owner j := by
  have h := C.empty_clause j i hij.symm checked
  have hnot : ¬ C.owner j < C.owner i := by
    simpa only [Context.clause_cons, Context.clause_nil, or_false,
      Context.holds_neg, C.holds_before j i hij.symm] using h
  have hne := C.injective.ne hij
  exact lt_of_le_of_ne (le_of_not_gt hnot) hne

private def labelCheck (i j : Fin 9) (test : StateInterface.Label → Bool) : Bool :=
  ResidualDomains.grid.all (fun z => !(decide (Allowed states i j z)) || test z)

private theorem label_checked (i j : Fin 9) (hij : i ≠ j) (h : C.owner i < C.owner j)
    (test : StateInterface.Label → Bool) (checked : labelCheck i j test = true) :
    test (C.edge i j) = true := by
  have ht := List.all_eq_true.mp checked (C.edge i j)
    (ResidualDomains.mem_grid _ (C.edge_bounds hij))
  have ha := C.edge_allowed h
  simpa [ha] using ht

private theorem checksBool : (edgeList.all (fun e =>
    decide (e.1 ∈ qIds ∧ e.2 ∈ qIds ∧ e.1 ≠ e.2) &&
    qList.all (fun k => decide (k = e.1 ∨ k = e.2) ||
      CycleSigns.CheckTriple ResidualDomains.computedTable
        (states e.1) (states e.2) (states k)))) = true := by decide +kernel

private theorem checks : ∀ i j : Fin 9, (i,j) ∈ edgeIds →
    i ∈ qIds ∧ j ∈ qIds ∧ i ≠ j ∧
    ∀ k ∈ qIds, k ≠ i → k ≠ j →
      CycleSigns.CheckTriple ResidualDomains.computedTable
        (states i) (states j) (states k) = true := by
  intro i j hij
  have h := List.all_eq_true.mp checksBool (i,j) (by simpa [edgeList,edgeIds] using hij)
  obtain ⟨h1,h2⟩ := Bool.and_eq_true_iff.mp h
  obtain ⟨hi,hj,hne⟩ := of_decide_eq_true h1
  refine ⟨hi,hj,hne,?_⟩
  intro k hk hki hkj
  have h := List.all_eq_true.mp h2 k (by simpa [qList,qIds] using hk)
  simpa [hki,hkj] using h

private theorem coverage : ∀ p ∈ qIds, ∃ e ∈ edgeIds,
    e ≠ (6,1) ∧ (p = e.1 ∨ p = e.2) := by decide +kernel

private theorem original_supports : SupportsOnLeft (qIds.image C.point)
    (edgeIds.image (fun e : Fin 9 × Fin 9 => (C.point e.1, C.point e.2))) := by
  classical
  rintro e he
  obtain ⟨⟨i,j⟩, hij, rfl⟩ := Finset.mem_image.mp he
  obtain ⟨hi, hj, hne, signs⟩ := checks i j hij
  have inj : Function.Injective C.point := C.config.point_injective.comp C.injective
  refine ⟨Finset.mem_image_of_mem _ hi, Finset.mem_image_of_mem _ hj, inj.ne hne, ?_⟩
  intro r hr hri hrj
  obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp hr
  have hki : k ≠ i := fun h => hri (congrArg C.point h)
  have hkj : k ≠ j := fun h => hrj (congrArg C.point h)
  exact pos C i j k hne hki.symm hkj.symm (signs k hk hki hkj)

set_option maxHeartbeats 200000 in
private theorem insert_convex (x : Fin 9)
    (outside : orient (C.point 6) (C.point 1) (C.point x) < 0)
    (inside : ∀ i j : Fin 9, (i,j) ∈ edgeIds → (i,j) ≠ (6,1) →
      0 < orient (C.point i) (C.point j) (C.point x)) :
    ConvexPosition (insert (C.point x) (qIds.image C.point)) := by
  classical
  have inj : Function.Injective C.point := C.config.point_injective.comp C.injective
  have hvisible : (C.point 6, C.point 1) ∈
      edgeIds.image (fun e : Fin 9 × Fin 9 => (C.point e.1, C.point e.2)) := by
    exact Finset.mem_image.mpr ⟨(6,1), by decide, rfl⟩
  refine convexPosition_insert_of_one_visible_edge (qIds.image C.point)
    (edgeIds.image (fun e : Fin 9 × Fin 9 => (C.point e.1, C.point e.2))) (C.point x) (C.point 6) (C.point 1)
    (original_supports C) hvisible outside ?_ ?_
  · intro e he hne
    obtain ⟨⟨i,j⟩, hij, rfl⟩ := Finset.mem_image.mp he
    apply inside i j hij
    intro h
    apply hne
    exact congrArg (fun e : Fin 9 × Fin 9 => (C.point e.1, C.point e.2)) h
  · intro p hp
    obtain ⟨k,hk,rfl⟩ := Finset.mem_image.mp hp
    obtain ⟨⟨i,j⟩,he,hne,hk⟩ := coverage k hk
    refine ⟨(C.point i,C.point j),Finset.mem_image.mpr ⟨(i,j),he,rfl⟩,?_,?_⟩
    · intro h
      apply hne
      exact Prod.ext (inj (congrArg Prod.fst h)) (inj (congrArg Prod.snd h))
    · rcases hk with hk | hk
      · exact Or.inl (congrArg C.point hk)
      · exact Or.inr (congrArg C.point hk)

private def extraTriples : Finset (Fin 9 × Fin 9 × Fin 9) :=
  {(0,1,2),(0,2,4),(0,4,5),(0,5,7),(0,7,8),
   (1,2,3),(2,4,3),(4,5,3),(5,7,3),(7,8,3),(8,6,3),
   (3,7,6),(3,1,7),(6,1,7)}

private def extraList : List (Fin 9 × Fin 9 × Fin 9) :=
  [(0,1,2),(0,2,4),(0,4,5),(0,5,7),(0,7,8),
   (1,2,3),(2,4,3),(4,5,3),(5,7,3),(7,8,3),(8,6,3),
   (3,7,6),(3,1,7),(6,1,7)]

private theorem extraChecksBool : (extraList.all (fun t =>
    decide (t.1 ≠ t.2.1 ∧ t.1 ≠ t.2.2 ∧ t.2.1 ≠ t.2.2) &&
    CycleSigns.CheckTriple ResidualDomains.computedTable
      (states t.1) (states t.2.1) (states t.2.2))) = true := by decide +kernel

private theorem extraChecks : ∀ t ∈ extraTriples,
    t.1 ≠ t.2.1 ∧ t.1 ≠ t.2.2 ∧ t.2.1 ≠ t.2.2 ∧
    CycleSigns.CheckTriple ResidualDomains.computedTable
      (states t.1) (states t.2.1) (states t.2.2) = true := by
  intro t ht
  have h := List.all_eq_true.mp extraChecksBool t (by simpa [extraTriples,extraList] using ht)
  obtain ⟨h1,h2⟩ := Bool.and_eq_true_iff.mp h
  obtain ⟨hi,hj,hk⟩ := of_decide_eq_true h1
  exact ⟨hi,hj,hk,h2⟩

private theorem extra (i j k : Fin 9) (h : (i,j,k) ∈ extraTriples) :
    0 < orient (C.point i) (C.point j) (C.point k) := by
  obtain ⟨hij,hik,hjk,checked⟩ := extraChecks (i,j,k) h
  exact pos C i j k hij hik hjk checked

private theorem first_case (hbg : C.owner 1 < C.owner 6) :
    ConvexPosition (insert (C.point 0) (qIds.image C.point)) := by
  have hab := before C 0 1 (by decide) (by decide +kernel)
  have hgi := before C 6 8 (by decide) (by decide +kernel)
  have hag := hab.trans hbg
  have capEq : (C.edge 0 1).1 = 4 := by
    exact of_decide_eq_true (label_checked C 0 1 (by decide) hab
      (fun z => decide (z.1 = 4)) (by decide +kernel))
  have cupLower : 2 ≤ (C.edge 0 6).2 := by
    exact of_decide_eq_true (label_checked C 0 6 (by decide) hag
      (fun z => decide (2 ≤ z.2)) (by decide +kernel))
  have cupUpper : (C.edge 6 8).2 ≤ 2 := by
    exact of_decide_eq_true (label_checked C 6 8 (by decide) hgi
      (fun z => decide (z.2 ≤ 2)) (by decide +kernel))
  have habg : 0 < orient (C.point 0) (C.point 1) (C.point 6) := by
    have grow := C.growth_clause false 0 1 6 (by decide) (by decide) (by decide) 4
    have upper := C.edge_bounds (i := 1) (j := 6) (by decide)
    have no5 : ¬ 5 ≤ (C.edge 1 6).1 := by omega
    simpa [growthClause, Context.clause_cons, Context.clause_nil,
      Context.holds_neg, C.holds_before 0 1 (by decide),
      C.holds_before 1 6 (by decide), C.holds_positive 0 1 6 (by decide) (by decide) (by decide),
      C.holds_ge false 0 1 (by decide) 4, C.holds_ge false 1 6 (by decide) 5,
      hab, hbg, capEq, no5] using grow
  have hagi : orient (C.point 0) (C.point 6) (C.point 8) < 0 := by
    have grow := C.growth_clause true 0 6 8 (by decide) (by decide) (by decide) 2
    have no3 : ¬ 3 ≤ (C.edge 6 8).2 := by omega
    have hnot : ¬ 0 < orient (C.point 0) (C.point 6) (C.point 8) := by
      simpa [growthClause, Context.clause_cons, Context.clause_nil,
        Context.holds_neg, C.holds_before 0 6 (by decide),
        C.holds_before 6 8 (by decide), C.holds_positive 0 6 8 (by decide) (by decide) (by decide),
        C.holds_ge true 0 6 (by decide) 2, C.holds_ge true 6 8 (by decide) 3,
        hag, hgi, cupLower, no3] using grow
    have nz := C.nonzero 0 6 8 (by decide) (by decide) (by decide)
    exact lt_of_le_of_ne (le_of_not_gt hnot) nz
  apply insert_convex C 0
  · have eq : orient (C.point 6) (C.point 1) (C.point 0) =
        -orient (C.point 0) (C.point 1) (C.point 6) := by simp only [orient]; ring
    rw [eq]; linarith
  · intro i j he hne
    simp only [edgeIds, Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he | he | he | he | he | he
    all_goals have hi := congrArg Prod.fst he; have hj := congrArg Prod.snd he
    all_goals dsimp only at hi hj; subst i; subst j
    · simpa only [orient_cycle] using extra C 0 1 2 (by decide)
    · simpa only [orient_cycle] using extra C 0 2 4 (by decide)
    · simpa only [orient_cycle] using extra C 0 4 5 (by decide)
    · simpa only [orient_cycle] using extra C 0 5 7 (by decide)
    · simpa only [orient_cycle] using extra C 0 7 8 (by decide)
    · have eq : orient (C.point 8) (C.point 6) (C.point 0) =
          -orient (C.point 0) (C.point 6) (C.point 8) := by simp only [orient]; ring
      rw [eq]; linarith
    · exact False.elim (hne rfl)

private theorem second_case (hgb : C.owner 6 < C.owner 1) :
    ConvexPosition (insert (C.point 3) (qIds.image C.point)) := by
  have hdg := before C 3 6 (by decide) (by decide +kernel)
  have hbh := before C 1 7 (by decide) (by decide +kernel)
  have hx1 : (C.point 3) 0 < (C.point 6) 0 := C.config.xOrder hdg
  have hx2 : (C.point 6) 0 < (C.point 1) 0 := C.config.xOrder hgb
  have hx3 : (C.point 1) 0 < (C.point 7) 0 := C.config.xOrder hbh
  have hdgh : orient (C.point 3) (C.point 6) (C.point 7) < 0 := by
    have h := extra C 3 7 6 (by decide)
    rw [orient_swap] at h
    linarith
  have hdbh := extra C 3 1 7 (by decide)
  have hgbh := extra C 6 1 7 (by decide)
  have pack := packetValid_of_xordered (C.point 3) (C.point 6) (C.point 1) (C.point 7)
    hx1 hx2 hx3
  have hnot : ¬0 < orient (C.point 3) (C.point 6) (C.point 1) := by
    intro h
    simp [PacketValid, h, hdbh, hgbh, not_lt.mpr hdgh.le] at pack
  have hdgb : orient (C.point 3) (C.point 6) (C.point 1) < 0 :=
    lt_of_le_of_ne (le_of_not_gt hnot) (C.nonzero 3 6 1 (by decide) (by decide) (by decide))
  apply insert_convex C 3
  · simpa only [orient_cycle] using hdgb
  · intro i j he hne
    simp only [edgeIds, Finset.mem_insert, Finset.mem_singleton] at he
    rcases he with he | he | he | he | he | he | he
    all_goals have hi := congrArg Prod.fst he; have hj := congrArg Prod.snd he
    all_goals dsimp only at hi hj; subst i; subst j
    · exact extra C 1 2 3 (by decide)
    · exact extra C 2 4 3 (by decide)
    · exact extra C 4 5 3 (by decide)
    · exact extra C 5 7 3 (by decide)
    · exact extra C 7 8 3 (by decide)
    · exact extra C 8 6 3 (by decide)
    · exact False.elim (hne rfl)

private theorem octagon_contradiction (x : Fin 9) (hx : x ∉ qIds)
    (convex : ConvexPosition (insert (C.point x) (qIds.image C.point))) : False := by
  classical
  have inj : Function.Injective C.point := C.config.point_injective.comp C.injective
  have hnot : C.point x ∉ qIds.image C.point := by
    intro h
    obtain ⟨y,hy,he⟩ := Finset.mem_image.mp h
    exact hx ((inj he) ▸ hy)
  apply C.noOctagon
  refine ⟨insert (C.point x) (qIds.image C.point), ?_, ?_, convex⟩
  · intro p hp
    rcases Finset.mem_insert.mp hp with hpx | hp
    · rw [hpx]
      exact Finset.mem_image_of_mem _ (Finset.mem_univ (C.owner x))
    · obtain ⟨y,_,rfl⟩ := Finset.mem_image.mp hp
      exact Finset.mem_image_of_mem _ (Finset.mem_univ (C.owner y))
  · rw [Finset.card_insert_of_notMem hnot,Finset.card_image_of_injective _ inj]
    decide

/-- Structural proof for these nine residual states, using shared
pair-rank growth, one four-point packet, and visible-edge insertion. It does
not import the literal CNF/LRAT theorem. The Context assumptions are explicit. -/
theorem context_impossible_structural (C : Context 9 n states) : False := by
  rcases lt_or_gt_of_ne (C.injective.ne (by decide : (1 : Fin 9) ≠ 6)) with h | h
  · exact octagon_contradiction C 0 (by decide) (first_case C h)
  · exact octagon_contradiction C 3 (by decide) (second_case C h)

def support : Finset (Fin 154) := {44,53,64,68,75,87,91,99,111}

theorem states_injective : Function.Injective states := by decide +kernel

private theorem states_mem_support : ∀ i : Fin 9, states i ∈ support := by decide +kernel

/-- The structural proof applies to actual owners in one residual real
configuration. No certificate or further realization premise is required. -/
theorem exists_missing_state {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ s ∈ support, s ∉ c.residualOccupied noCap noOctagon noJunction := by
  classical
  by_contra! h
  have selected : ∀ i : Fin 9, ∃ v : Fin n,
      c.residualOwner noCap noOctagon noJunction v = states i := by
    intro i
    obtain ⟨v, _, hv⟩ := Finset.mem_image.mp (h (states i) (states_mem_support i))
    exact ⟨v, hv⟩
  choose owner owner_state using selected
  have injective : Function.Injective owner := by
    intro i j he
    apply states_injective
    rw [← owner_state i, ← owner_state j, he]
  let C : Context 9 n states := {
    config := c, noCap := noCap, noOctagon := noOctagon, noJunction := noJunction,
    owner := owner, injective := injective, owner_state := owner_state,
    nonzero := fun i j l hij hil hjl => c.orient_ne_of_distinct _ _ _
      (injective.ne hij) (injective.ne hil) (injective.ne hjl) }
  exact context_impossible_structural C

/-- A demand-one omission row proved through the structural geometric route. -/
theorem hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    1 ≤ (support \ c.residualOccupied noCap noOctagon noJunction).card := by
  classical
  obtain ⟨s, hs, hmissing⟩ := exists_missing_state c noCap noOctagon noJunction
  exact Finset.one_le_card.mpr ⟨s, Finset.mem_sdiff.mpr ⟨hs, hmissing⟩⟩

#print axioms context_impossible_structural
#print axioms states_injective
#print axioms exists_missing_state
#print axioms hole_bound

end ErdosSzekeres.Omission.StructuralNineShifted111

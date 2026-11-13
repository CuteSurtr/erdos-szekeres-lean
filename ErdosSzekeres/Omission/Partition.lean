/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8PartitionComplete.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: real points as Fin 2 → ℝ, local geometry and namespaces, Lean 4.24.
-/
import ErdosSzekeres.Omission.ThreeChain
import ErdosSzekeres.Omission.ProjectiveTransfer

namespace ErdosSzekeres.Omission.Partition
open ActualRanks MinimumSlope Subsets SlopePartition ThreeChain

/-- Extract both actual witnesses and extend the cap using its last upper vertex.
The second cap point stays in U; the new last point need only lie in the ambient set. -/
theorem junction_chains {n} {c : Configuration n} (m : MinNeighbors c) (s : Fin n)
    (hs : s∈junctions m) : ∃ x1 x2 x3 x4 x5 q r3 r4 r5 r6 : Nat,
    (colorConfig c.cup true).Cup [x1,x2,x3,x4,x5,s.val] ∧
    (colorConfig c.cup false).Cup [s.val,q,r3,r4,r5,r6] ∧
    q∈natSet (upper m) ∧ r6<n := by
  classical
  obtain ⟨_,xs,ys,a,b,xlen,ylen,xchain,ychain,xinside,yinside⟩ := Finset.mem_filter.mp hs
  have xl : xs.length=4 := by simp only [List.length_append,List.length_cons,List.length_nil] at xlen; omega
  have yl : ys.length=3 := by simp only [List.length_cons] at ylen; omega
  obtain ⟨x1,x2,x3,x4,rfl⟩ := List.length_eq_four.mp xl
  obtain ⟨r3,r4,r5,rfl⟩ := List.length_eq_three.mp yl
  have order := ychain.1
  simp only [List.isChain_cons_cons] at order
  have r5U := yinside r5 (by simp)
  have r5n := Finset.mem_range.mp (natSet_bounded (upper m) r5U)
  have r4n : r4<n := by omega
  let last : Fin n := ⟨r5,r5n⟩
  have right : last<m.neighbor last := (upper_mem m last).mp ((natSet_member (upper m) last).mp r5U)
  have neg := cap_to_right m ⟨r4,r4n⟩ last (by simpa [last] using order.2.2.2) right
  have color : c.cup r4 r5 (m.neighbor last).val=false := by
    cases h : c.cup r4 r5 (m.neighbor last).val with
    | false => rfl
    | true => have pos := (c.cup_true_iff ⟨r4,r4n⟩ last (m.neighbor last)).mp h; linarith
  refine ⟨x1,x2,x3,x4,a,b,r3,r4,r5,(m.neighbor last).val,?_,?_,yinside b (by simp),(m.neighbor last).isLt⟩
  · simpa using xchain
  · have parts := Config.Cup.append_cons3.mpr
      (show (colorConfig c.cup false).Cup ([s.val,b,r3]++[r4,r5]) ∧
        (colorConfig c.cup false).Cup3 r4 r5 (m.neighbor last).val ∧
        (colorConfig c.cup false).Cup [r5,(m.neighbor last).val] from
        ⟨ychain,color,Config.Cup.pair.mpr right⟩)
    simpa using parts

/-- A seven-cup cannot start in L, even if its other vertices belong to H. -/
theorem seven_cup_start_not_lower {n} {c : Configuration n} (m : MinNeighbors c)
    (s a b d v u t : Nat) (cup : (colorConfig c.cup true).Cup [s,a,b,d,v,u,t])
    (tn : t<n) (noOct : ¬HasConvexNGon 8 (Finset.univ.image c.point)) : s∉natSet (lower m) := by
  intro hs
  have order := cup.1
  simp only [List.isChain_cons_cons] at order
  have sn : s<n := by omega
  have an : a<n := by omega
  let sf : Fin n := ⟨s,sn⟩
  have left := (lower_mem m sf).mp ((natSet_member (lower m) sf).mp hs)
  have positive := cup_from_left m sf ⟨a,an⟩ order.1 left
  have color := (c.cup_true_iff (m.neighbor sf) sf ⟨a,an⟩).mpr positive
  apply noOct
  apply ListGeometry.hasNCup_octagon c
  refine ⟨(m.neighbor sf).val::[s,a,b,d,v,u,t],⟨?_,rfl⟩,?_⟩
  · exact Config.Cup.cons3.mpr ⟨left,color,cup⟩
  · intro z hz; simp at hz; apply Finset.mem_range.mpr
    have := (m.neighbor sf).isLt; omega

/-- A seven-cup cannot end at an actual junction. -/
theorem seven_cup_end_not_junction {n} {c : Configuration n} (m : MinNeighbors c)
    (s a b d v u t : Nat) (cup : (colorConfig c.cup true).Cup [s,a,b,d,v,u,t])
    (tn : t<n) (noCap : ¬(colorConfig c.cup true).HasNCap 7 (Finset.range n))
    (noOct : ¬HasConvexNGon 8 (Finset.univ.image c.point)) : t∉natSet (junctions m) := by
  intro ht
  obtain ⟨x1,x2,x3,x4,x5,q,r3,r4,r5,r6,_,cap,_,rn⟩ :=
    junction_chains m ⟨t,tn⟩ ((natSet_member (junctions m) ⟨t,tn⟩).mp ht)
  have ci := cup
  have cq := cap
  simp only [Config.Cup.cons3,Config.Cup.pair,colorConfig] at ci cq
  obtain ⟨sa,hsab,ab,habd,bd,hbdv,dv,hdvu,vu,hvut,ut⟩ := ci
  obtain ⟨tq,htqr,qr3,hqr,r34,hr345,r45,hr456,r56⟩ := cq
  cases h : c.cup u t q with
  | true =>
    apply noOct
    apply ListGeometry.hasNCup_octagon c
    refine ⟨[s,a,b,d,v,u,t,q],⟨?_,rfl⟩,?_⟩
    · simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
        And.intro sa (And.intro hsab ⟨ab,habd,bd,hbdv,dv,hdvu,vu,hvut,ut,h,tq⟩)
    · intro z hz; simp at hz; apply Finset.mem_range.mpr; omega
  | false =>
    apply noCap
    refine ⟨[u,t,q,r3,r4,r5,r6],⟨(false_cup_iff_cap _ _).mp ?_,rfl⟩,?_⟩
    · simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
        And.intro ut (And.intro h ⟨tq,htqr,qr3,hqr,r34,hr345,r45,hr456,r56⟩)
    · intro z hz; simp at hz; apply Finset.mem_range.mpr; omega

theorem balanced_no_seven_cup {n} {c : Configuration n} (m : MinNeighbors c)
    (noCap : ¬(colorConfig c.cup true).HasNCap 7 (Finset.range n))
    (noOct : ¬HasConvexNGon 8 (Finset.univ.image c.point)) :
    ¬(colorConfig c.cup true).HasNCup 7 (natSet (balancedPart m)) := by
  rintro ⟨xs,⟨cup,len⟩,inside⟩
  obtain ⟨s,xs,rfl⟩ := List.exists_cons_of_length_pos (by omega : 0<xs.length)
  simp only [List.length_cons] at len
  obtain ⟨a,xs,rfl⟩ := List.exists_cons_of_length_pos (by omega : 0<xs.length)
  simp only [List.length_cons] at len
  obtain ⟨b,xs,rfl⟩ := List.exists_cons_of_length_pos (by omega : 0<xs.length)
  simp only [List.length_cons] at len
  obtain ⟨d,xs,rfl⟩ := List.exists_cons_of_length_pos (by omega : 0<xs.length)
  simp only [List.length_cons] at len
  obtain ⟨v,xs,rfl⟩ := List.exists_cons_of_length_pos (by omega : 0<xs.length)
  simp only [List.length_cons] at len
  obtain ⟨u,xs,rfl⟩ := List.exists_cons_of_length_pos (by omega : 0<xs.length)
  simp only [List.length_cons] at len
  obtain ⟨t,xs,rfl⟩ := List.exists_cons_of_length_pos (by omega : 0<xs.length)
  simp only [List.length_cons] at len
  have empty : xs=[] := List.length_eq_zero_iff.mp (by omega)
  subst xs
  have tn := Finset.mem_range.mp (natSet_bounded _ (inside t (by simp)))
  have order := cup.1
  simp only [List.isChain_cons_cons] at order
  have sn : s<n := by omega
  have hs := inside s (by simp)
  have ht := inside t (by simp)
  have union : natSet (balancedPart m)=natSet (lower m)∪natSet (junctions m) :=
    Finset.image_union _ _
  rw [union,Finset.mem_union] at hs ht
  have sG := hs.resolve_left (seven_cup_start_not_lower m s a b d v u t cup tn noOct)
  have tL := ht.resolve_right (seven_cup_end_not_junction m s a b d v u t cup tn noCap noOct)
  obtain ⟨x1,x2,x3,x4,x5,q,r3,r4,r5,r6,incoming,outcap,qU,rn⟩ :=
    junction_chains m ⟨s,sn⟩ ((natSet_member (junctions m) ⟨s,sn⟩).mp sG)
  have exception : q≠t := by
    intro eq
    subst q
    have hU := (natSet_member (upper m) ⟨t,tn⟩).mp qU
    have hL := (natSet_member (lower m) ⟨t,tn⟩).mp tL
    exact Finset.disjoint_left.mp (partition_disjoint m) hU hL
  exact three_chain c x1 x2 x3 x4 x5 s q r3 r4 r5 r6 a b d v u t
    incoming outcap cup sn rn tn exception noCap noOct


/-- The two actual index sets are disjoint; moving junctions does not duplicate
points between the two populations. -/
theorem parts_disjoint {n} {c : Configuration n} (m : MinNeighbors c) :
    Disjoint (balancedPart m) (residualPart m) := by
  classical
  apply Finset.disjoint_left.mpr
  intro u hu hr
  rcases Finset.mem_union.mp hu with hl | hj
  · exact Finset.disjoint_left.mp (partition_disjoint m)
      (residual_subset m hr) hl
  · exact (Finset.mem_sdiff.mp hr).2 hj

/-- An octagon-free ordered real set with no 7-cap splits into a balanced
configuration and a residual configuration. Every avoidance condition and
junction restriction is proved for the actual induced subsets. -/
theorem exists_partition {n} (c : Configuration n) (hn : 2 ≤ n)
    (noCap : ¬ c.HasCap 7)
    (noOct : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    ∃ H R : Finset (Fin n), H ∪ R = Finset.univ ∧ Disjoint H R ∧
      n = H.card + R.card ∧
      ¬ (restrict c H).HasCap 7 ∧ ¬ (restrict c H).HasCup 7 ∧
      ¬ HasConvexNGon 8 (Finset.univ.image (restrict c H).point) ∧
      ¬ (restrict c R).HasCap 6 ∧
      ¬ HasConvexNGon 8 (Finset.univ.image (restrict c R).point) ∧
      NoJunctionOn (restrict c R).cup (Finset.range R.card) := by
  obtain ⟨m⟩ := exists_min_neighbors c hn
  have caps : ¬ (colorConfig c.cup true).HasNCap 7 (Finset.range n) :=
    fun h => noCap (ListGeometry.hasCap_of_list c h)
  refine ⟨balancedPart m, residualPart m, parts_cover m, parts_disjoint m, ?_,
    restrict_no_cap c _ (balanced_no_seven_cap m caps),
    restrict_no_cup c _ (balanced_no_seven_cup m caps noOct),
    restrict_no_octagon c _ noOct,
    restrict_no_cap c _ (residual_no_six_cap m caps),
    restrict_no_octagon c _ noOct,
    no_junction_restrict c _ (residual_no_junction m)⟩
  have card := Finset.card_union_of_disjoint (parts_disjoint m)
  simpa only [parts_cover, Finset.card_univ, Fintype.card_fin] using card

/-- Population bound for the already completed balanced geometric subcase.
Large certificate imports are kept outside the default library. -/
def BalancedBound (B : ℕ) : Prop :=
  ∀ n : ℕ, ∀ c : Configuration n, ¬ c.HasCap 7 → ¬ c.HasCup 7 →
    ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B

/-- The remaining residual population statement. Its no-junction hypothesis
means an actual incoming 6-cup and outgoing 5-cap cannot share their endpoint.
The value 123 is a target, not an assumed axiom or a proved bound. -/
def ResidualBound (B : ℕ) : Prop :=
  ∀ n : ℕ, ∀ c : Configuration n, ¬ c.HasCap 6 →
    ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
    NoJunctionOn c.cup (Finset.range n) → n ≤ B

/-- The partition discharges every geometric splitting hypothesis. Only the
two population estimates remain as explicit parameters. -/
theorem asymmetric_of_population_bounds (balanced : BalancedBound 192)
    (residual : ResidualBound 123) : AsymmetricBound 315 := by
  intro n c noCap noOct
  by_cases hn : 2 ≤ n
  · obtain ⟨H, R, _, _, count, hcap, hcup, hoct, rcap, roct, junction⟩ :=
      exists_partition c hn noCap noOct
    have h := balanced _ (restrict c H) hcap hcup hoct
    have r := residual _ (restrict c R) rcap roct junction
    omega
  · omega

end ErdosSzekeres.Omission.Partition

import EncB.SortLemmas

/-!
# U5: cyclic words of six sorted objects (`wordSpec`, Std-only)

`SortedSix m psiLt a b d S` says that the six code objects `S` of the triple `[a, b, d]`, mapped by `objImg`, are
the six objects of `a, b, d` in strict `objLt` order. `wordSpec` reads rule A's and rule B's patterns off the cyclic
word `S.map (·.kind)` (gen_b2.py:119-130):

* alternating word: the three points sit at positions `{0,2,4}` or `{1,3,5}` and an antipode sits strictly inside
  each of the three arcs between them (wrap-around included); its label is one of the three point labels, because
  the point indices are a permutation of `[0, 1, 2]`;
* three cyclically consecutive points: nothing lies strictly between two cyclically consecutive positions, so the
  arcs `(x, y)` and `(y, z)` hold no antipode.

Everything is reasoned on positions (`ccwIn_getElem_iff` and `omega`); no case tree over the six objects.
-/

namespace EncB
namespace Word

theorem getD_eq {α : Type} {l : List α} {i : Nat} (d : α) (h : i < l.length) : l.getD i d = l[i] := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem h]; rfl

theorem eq6 {α : Type} : ∀ {S : List α}, S.length = 6 → ∃ s0 s1 s2 s3 s4 s5, S = [s0, s1, s2, s3, s4, s5]
  | [_, _, _, _, _, _], _ => ⟨_, _, _, _, _, _, rfl⟩

/-- Cyclic strict betweenness of positions: `j` lies strictly inside the cyclic interval from `i` to `k`. -/
def Cyc (i j k : Nat) : Prop := (i < j ∧ j < k) ∨ (k < i ∧ i < j) ∨ (j < k ∧ k < i)

theorem getD3_mem (a b d : Pt) {i : Nat} (hi : i < 3) : [a, b, d].getD i (0, 0) ∈ [a, b, d] := by
  match i, hi with
  | 0, _ => exact List.mem_cons_self
  | 1, _ => exact List.mem_cons_of_mem _ List.mem_cons_self
  | 2, _ => exact List.mem_cons_of_mem _ (List.mem_cons_of_mem _ List.mem_cons_self)

/-- An index `j < 3` is one of the point indices, so its label is one of the three point labels. -/
theorem getD3_mem_perm (c : List Pt) {p0 p1 p2 j : Nat} (hp : [p0, p1, p2].Perm [0, 1, 2]) (hj : j < 3) :
    c.getD j (0, 0) ∈ [c.getD p0 (0, 0), c.getD p1 (0, 0), c.getD p2 (0, 0)] := by
  have h : j ∈ [p0, p1, p2] := hp.mem_iff.2 (by
    simp only [List.mem_cons, List.not_mem_nil, or_false]; omega)
  simp only [List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl | rfl
  · exact List.mem_cons_self
  · exact List.mem_cons_of_mem _ List.mem_cons_self
  · exact List.mem_cons_of_mem _ (List.mem_cons_of_mem _ List.mem_cons_self)

theorem lt3_of_perm {p0 p1 p2 : Nat} (hp : [p0, p1, p2].Perm [0, 1, 2]) :
    p0 < 3 ∧ p1 < 3 ∧ p2 < 3 := by
  have h : ∀ x ∈ [p0, p1, p2], x < 3 := by
    intro x hx
    have hx' := hp.mem_iff.1 hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx'
    omega
  exact ⟨h p0 List.mem_cons_self, h p1 (List.mem_cons_of_mem _ List.mem_cons_self),
    h p2 (List.mem_cons_of_mem _ (List.mem_cons_of_mem _ List.mem_cons_self))⟩

theorem cmp_of_mem {α : Type} {R : α → α → Prop} {L : List α} (hp : L.Pairwise R) {x y : α}
    (hx : x ∈ L) (hy : y ∈ L) (hne : x ≠ y) : R x y ∨ R y x := by
  obtain ⟨i, hi, rfl⟩ := List.mem_iff_getElem.1 hx
  obtain ⟨j, hj, rfl⟩ := List.mem_iff_getElem.1 hy
  rw [List.pairwise_iff_getElem] at hp
  rcases Nat.lt_trichotomy i j with h | rfl | h
  · exact Or.inl (hp i j hi hj h)
  · exact absurd rfl hne
  · exact Or.inr (hp j i hj hi h)

section
variable {m : Nat} {psiLt : Nat → Nat → Bool} {a b d : Pt} {S : List Obj}

theorem sortedL (hS : SortedSix m psiLt a b d S) : (S.map (objImg [a, b, d])).Pairwise (objLt m psiLt) :=
  List.pairwise_map.2 hS.sorted

theorem mem_L (hS : SortedSix m psiLt a b d S) {w : Pt} (hw : w ∈ [a, b, d]) (bo : Bool) :
    (w, bo) ∈ S.map (objImg [a, b, d]) := by
  apply hS.cover
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hw
  simp only [objs6, List.mem_cons, List.not_mem_nil, or_false]
  rcases hw with rfl | rfl | rfl <;> cases bo <;> simp

theorem keysDistinct_of (hS : SortedSix m psiLt a b d S) {x y z : Pt}
    (hx : x ∈ [a, b, d]) (hy : y ∈ [a, b, d]) (hz : z ∈ [a, b, d]) : KeysDistinct m psiLt x y z := by
  have hmem : ∀ o ∈ objs6 x y z, o ∈ S.map (objImg [a, b, d]) := by
    intro o ho
    simp only [objs6, List.mem_cons, List.not_mem_nil, or_false] at ho
    rcases ho with rfl | rfl | rfl | rfl | rfl | rfl <;>
      first | exact mem_L hS hx _ | exact mem_L hS hy _ | exact mem_L hS hz _
  intro o ho o' ho' hne
  exact cmp_of_mem (sortedL hS) (hmem o ho) (hmem o' ho') hne

theorem ccw_of_pos (hirr : ∀ i, psiLt i i = false)
    (htr : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true)
    {L : List (Pt × Bool)} (hp : L.Pairwise (objLt m psiLt)) {i j k : Nat} {x y z : Pt × Bool}
    (ex : L[i]? = some x) (ey : L[j]? = some y) (ez : L[k]? = some z) (hc : Cyc i j k) :
    ccwIn (objLt m psiLt) x y z := by
  obtain ⟨hi, rfl⟩ := List.getElem?_eq_some_iff.1 ex
  obtain ⟨hj, rfl⟩ := List.getElem?_eq_some_iff.1 ey
  obtain ⟨hk, rfl⟩ := List.getElem?_eq_some_iff.1 ez
  exact (ccwIn_getElem_iff hp (objLt_irrefl hirr) (objLt_asymm hirr htr) hi hj hk).2 hc

theorem not_ccw_of_pos (hirr : ∀ i, psiLt i i = false)
    (htr : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true)
    {L : List (Pt × Bool)} (hp : L.Pairwise (objLt m psiLt)) {i k : Nat} {x y z : Pt × Bool}
    (ex : L[i]? = some x) (ez : L[k]? = some z) (hy : y ∈ L) (hc : ∀ j, j < L.length → ¬ Cyc i j k) :
    ¬ ccwIn (objLt m psiLt) x y z := by
  obtain ⟨hi, rfl⟩ := List.getElem?_eq_some_iff.1 ex
  obtain ⟨hk, rfl⟩ := List.getElem?_eq_some_iff.1 ez
  obtain ⟨j, hj, rfl⟩ := List.mem_iff_getElem.1 hy
  rw [ccwIn_getElem_iff hp (objLt_irrefl hirr) (objLt_asymm hirr htr) hi hj hk]
  exact hc j hj

/-- Rule A from positions: points at `i0, i1, i2` in ccw order, antipodes `z0, z1, z2` of point labels strictly
inside the three arcs. -/
theorem alt_core (hirr : ∀ i, psiLt i i = false)
    (htr : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true)
    (hS : SortedSix m psiLt a b d S) {i0 i1 i2 j0 j1 j2 : Nat} {x0 x1 x2 z0 z1 z2 : Pt}
    (e0 : (S.map (objImg [a, b, d]))[i0]? = some (x0, true))
    (e1 : (S.map (objImg [a, b, d]))[i1]? = some (x1, true))
    (e2 : (S.map (objImg [a, b, d]))[i2]? = some (x2, true))
    (f0 : (S.map (objImg [a, b, d]))[j0]? = some (z0, false))
    (f1 : (S.map (objImg [a, b, d]))[j1]? = some (z1, false))
    (f2 : (S.map (objImg [a, b, d]))[j2]? = some (z2, false))
    (hx0 : x0 ∈ [a, b, d]) (hx1 : x1 ∈ [a, b, d]) (hx2 : x2 ∈ [a, b, d])
    (hz0 : z0 ∈ [x0, x1, x2]) (hz1 : z1 ∈ [x0, x1, x2]) (hz2 : z2 ∈ [x0, x1, x2])
    (c0 : Cyc i0 i1 i2) (c1 : Cyc i0 j0 i1) (c2 : Cyc i1 j1 i2) (c3 : Cyc i2 j2 i0) :
    AltCCW m psiLt x0 x1 x2 :=
  ⟨keysDistinct_of hS hx0 hx1 hx2, ccw_of_pos hirr htr (sortedL hS) e0 e1 e2 c0,
    ⟨z0, hz0, ccw_of_pos hirr htr (sortedL hS) e0 f0 e1 c1⟩,
    ⟨z1, hz1, ccw_of_pos hirr htr (sortedL hS) e1 f1 e2 c2⟩,
    ⟨z2, hz2, ccw_of_pos hirr htr (sortedL hS) e2 f2 e0 c3⟩⟩

/-- The alternating half of `WordSpec`. -/
theorem alt_part (hirr : ∀ i, psiLt i i = false)
    (htr : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true)
    (hS : SortedSix m psiLt a b d S)
    (hk : S.map (·.kind) = [1, 0, 1, 0, 1, 0] ∨ S.map (·.kind) = [0, 1, 0, 1, 0, 1]) :
    AltCCW m psiLt
      ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 0 0) (0, 0))
      ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 1 0) (0, 0))
      ([a, b, d].getD (((S.filter (·.kind == 1)).map (·.idx)).getD 2 0) (0, 0)) := by
  obtain ⟨s0, s1, s2, s3, s4, s5, rfl⟩ := eq6 hS.length
  have hpts := hS.points
  have hidx : ∀ s ∈ [s0, s1, s2, s3, s4, s5], s.idx < 3 := hS.idx_lt
  simp only [List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq] at hidx
  obtain ⟨i0, i1, i2, i3, i4, i5⟩ := hidx
  rcases hk with hk | hk
  · simp only [List.map_cons, List.map_nil, List.cons.injEq, and_true] at hk
    obtain ⟨k0, k1, k2, k3, k4, k5⟩ := hk
    have hf : [s0, s1, s2, s3, s4, s5].filter (·.kind == 1) = [s0, s2, s4] := by
      simp [k0, k1, k2, k3, k4, k5]
    rw [hf] at hpts ⊢
    have hp : [s0.idx, s2.idx, s4.idx].Perm [0, 1, 2] := hpts
    show AltCCW m psiLt ([a, b, d].getD s0.idx (0, 0)) ([a, b, d].getD s2.idx (0, 0))
      ([a, b, d].getD s4.idx (0, 0))
    exact alt_core (i0 := 0) (i1 := 2) (i2 := 4) (j0 := 1) (j1 := 3) (j2 := 5) hirr htr hS
      (by simp [objImg, k0]) (by simp [objImg, k2]) (by simp [objImg, k4])
      (by simp [objImg, k1]) (by simp [objImg, k3]) (by simp [objImg, k5])
      (getD3_mem a b d i0) (getD3_mem a b d i2) (getD3_mem a b d i4)
      (getD3_mem_perm _ hp i1) (getD3_mem_perm _ hp i3) (getD3_mem_perm _ hp i5)
      (by unfold Cyc; omega) (by unfold Cyc; omega) (by unfold Cyc; omega) (by unfold Cyc; omega)
  · simp only [List.map_cons, List.map_nil, List.cons.injEq, and_true] at hk
    obtain ⟨k0, k1, k2, k3, k4, k5⟩ := hk
    have hf : [s0, s1, s2, s3, s4, s5].filter (·.kind == 1) = [s1, s3, s5] := by
      simp [k0, k1, k2, k3, k4, k5]
    rw [hf] at hpts ⊢
    have hp : [s1.idx, s3.idx, s5.idx].Perm [0, 1, 2] := hpts
    show AltCCW m psiLt ([a, b, d].getD s1.idx (0, 0)) ([a, b, d].getD s3.idx (0, 0))
      ([a, b, d].getD s5.idx (0, 0))
    exact alt_core (i0 := 1) (i1 := 3) (i2 := 5) (j0 := 2) (j1 := 4) (j2 := 0) hirr htr hS
      (by simp [objImg, k1]) (by simp [objImg, k3]) (by simp [objImg, k5])
      (by simp [objImg, k2]) (by simp [objImg, k4]) (by simp [objImg, k0])
      (getD3_mem a b d i1) (getD3_mem a b d i3) (getD3_mem a b d i5)
      (getD3_mem_perm _ hp i2) (getD3_mem_perm _ hp i4) (getD3_mem_perm _ hp i0)
      (by unfold Cyc; omega) (by unfold Cyc; omega) (by unfold Cyc; omega) (by unfold Cyc; omega)

/-- A position holding a point: its entry and its label. -/
theorem pt_at (hS : SortedSix m psiLt a b d S) {q : Nat} (hq : q < 6)
    (hk : (S.map (·.kind)).getD q 0 = 1) :
    (S.map (objImg [a, b, d]))[q]? = some ([a, b, d].getD (S.getD q default).idx (0, 0), true) ∧
      [a, b, d].getD (S.getD q default).idx (0, 0) ∈ [a, b, d] := by
  have hq' : q < S.length := by rw [hS.length]; exact hq
  rw [getD_eq _ (by rw [List.length_map]; exact hq'), List.getElem_map] at hk
  rw [getD_eq default hq']
  refine ⟨?_, getD3_mem a b d (hS.idx_lt _ (List.getElem_mem hq'))⟩
  rw [List.getElem?_map, List.getElem?_eq_getElem hq']
  simp [objImg, hk]

/-- The block half of `WordSpec`. -/
theorem block_part (hirr : ∀ i, psiLt i i = false)
    (htr : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true)
    (hS : SortedSix m psiLt a b d S) (st : Nat)
    (h0 : (S.map (·.kind)).getD (st % 6) 0 = 1) (h1 : (S.map (·.kind)).getD ((st + 1) % 6) 0 = 1)
    (h2 : (S.map (·.kind)).getD ((st + 2) % 6) 0 = 1) :
    BlockCCW m psiLt ([a, b, d].getD (S.getD (st % 6) default).idx (0, 0))
      ([a, b, d].getD (S.getD ((st + 1) % 6) default).idx (0, 0))
      ([a, b, d].getD (S.getD ((st + 2) % 6) default).idx (0, 0)) := by
  obtain ⟨e0, m0⟩ := pt_at hS (Nat.mod_lt _ (by decide)) h0
  obtain ⟨e1, m1⟩ := pt_at hS (Nat.mod_lt _ (by decide)) h1
  obtain ⟨e2, m2⟩ := pt_at hS (Nat.mod_lt _ (by decide)) h2
  have hlen : (S.map (objImg [a, b, d])).length = 6 := by rw [List.length_map]; exact hS.length
  have hw : ∀ w, w ∈ [[a, b, d].getD (S.getD (st % 6) default).idx (0, 0),
      [a, b, d].getD (S.getD ((st + 1) % 6) default).idx (0, 0),
      [a, b, d].getD (S.getD ((st + 2) % 6) default).idx (0, 0)] → w ∈ [a, b, d] := by
    intro w hw
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hw
    rcases hw with rfl | rfl | rfl <;> assumption
  refine ⟨keysDistinct_of hS m0 m1 m2,
    ccw_of_pos hirr htr (sortedL hS) e0 e1 e2 (by unfold Cyc; omega), ?_, ?_⟩
  · rintro ⟨w, hwm, hc⟩
    exact not_ccw_of_pos hirr htr (sortedL hS) e0 e1 (mem_L hS (hw w hwm) false)
      (fun j hj => by rw [hlen] at hj; unfold Cyc; omega) hc
  · rintro ⟨w, hwm, hc⟩
    exact not_ccw_of_pos hirr htr (sortedL hS) e1 e2 (mem_L hS (hw w hwm) false)
      (fun j hj => by rw [hlen] at hj; unfold Cyc; omega) hc

end

end Word

/-- **U5.** The cyclic word of six sorted objects gives the `Model`'s rule-A pattern (alternating word) and
rule-B pattern (any three cyclically consecutive points). -/
theorem wordSpec : WordSpec := by
  intro m psiLt a b d S hirr htr _ hS
  exact ⟨Word.alt_part hirr htr hS, fun st _ h0 h1 h2 => Word.block_part hirr htr hS st h0 h1 h2⟩

end EncB

/-- info: 'EncB.wordSpec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.wordSpec

/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8BaekGeometry.lean (list/sign bridge).
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: real points as Fin 2 → ℝ, local geometry and namespaces, Lean 4.24.
-/
import ErdosSzekeres.Omission.PlanarChains
import ErdosSzekeres.ConvexCycleCuts

namespace ErdosSzekeres.Omission.ListGeometry
open ActualRanks PlanarChains

noncomputable def pointAt {n} (c : Configuration n) (i : Nat) : Point :=
  if h : i<n then c.point ⟨i,h⟩ else 0

theorem pointAt_eq {n} (c : Configuration n) (i : Nat) (hi : i<n) :
    pointAt c i=c.point ⟨i,hi⟩ := by simp [pointAt,hi]

theorem cup_sign {n} (c : Configuration n) (a b d : Nat) (ha : a<n) (hb : b<n) (hd : d<n) :
    c.cup a b d=true ↔ 0<orient (pointAt c a) (pointAt c b) (pointAt c d) := by
  simpa only [pointAt_eq c a ha,pointAt_eq c b hb,pointAt_eq c d hd] using
    c.cup_true_iff ⟨a,ha⟩ ⟨b,hb⟩ ⟨d,hd⟩

theorem cap_sign {n} (c : Configuration n) (a b d : Nat) (ha : a<n) (hb : b<n) (hd : d<n)
    (ab : a<b) (bd : b<d) :
    (¬c.cup a b d=true) ↔ orient (pointAt c a) (pointAt c b) (pointAt c d)<0 := by
  rw [cup_sign c a b d ha hb hd]
  have nz : orient (pointAt c a) (pointAt c b) (pointAt c d)≠0 := by
    simpa only [pointAt_eq c a ha,pointAt_eq c b hb,pointAt_eq c d hd] using
      c.generalPosition ⟨a,ha⟩ ⟨b,hb⟩ ⟨d,hd⟩ ab bd
  constructor
  · intro h; exact lt_of_le_of_ne (le_of_not_gt h) nz
  · intro h; linarith

theorem pointAt_order {n} (c : Configuration n) {a b : Nat} (ha : a<n) (hb : b<n) (ab : a<b) :
    pointAt c a 0<pointAt c b 0 := by
  simpa only [pointAt_eq c a ha,pointAt_eq c b hb] using c.xOrder (show (⟨a,ha⟩ : Fin n)<⟨b,hb⟩ from ab)

theorem cup_list_all {n} (c : Configuration n) (xs : List Nat)
    (inside : xs.In (Finset.range n)) (cup : (colorConfig c.cup true).Cup xs) :
    OrderedTriples (fun a b d => 0<orient (pointAt c a) (pointAt c b) (pointAt c d)) xs := by
  have all := chain3_all (fun a b d => c.cup a b d=true) {i | i<n} ?_ xs
    (fun a ha => Finset.mem_range.mp (inside a ha)) cup.1.pairwise cup.2
  · intro a ha b hb d hd ab bd
    exact (cup_sign c a b d (Finset.mem_range.mp (inside a ha))
      (Finset.mem_range.mp (inside b hb)) (Finset.mem_range.mp (inside d hd))).mp (all a ha b hb d hd ab bd)
  · intro a ha b hb d hd e he ab bd de h1 h2
    have result := positive_four (pointAt c a) (pointAt c b) (pointAt c d) (pointAt c e)
      (pointAt_order c ha hb ab) (pointAt_order c hb hd bd) (pointAt_order c hd he de)
      ((cup_sign c a b d ha hb hd).mp h1) ((cup_sign c b d e hb hd he).mp h2)
    exact ⟨(cup_sign c a b e ha hb he).mpr result.1,(cup_sign c a d e ha hd he).mpr result.2⟩

theorem cap_list_all {n} (c : Configuration n) (xs : List Nat)
    (inside : xs.In (Finset.range n)) (cap : (colorConfig c.cup true).Cap xs) :
    OrderedTriples (fun a b d => orient (pointAt c a) (pointAt c b) (pointAt c d)<0) xs := by
  have all := chain3_all (fun a b d => ¬c.cup a b d=true) {i | i<n} ?_ xs
    (fun a ha => Finset.mem_range.mp (inside a ha)) cap.1.pairwise cap.2
  · intro a ha b hb d hd ab bd
    exact (cap_sign c a b d (Finset.mem_range.mp (inside a ha))
      (Finset.mem_range.mp (inside b hb)) (Finset.mem_range.mp (inside d hd)) ab bd).mp (all a ha b hb d hd ab bd)
  · intro a ha b hb d hd e he ab bd de h1 h2
    have result := negative_four (pointAt c a) (pointAt c b) (pointAt c d) (pointAt c e)
      (pointAt_order c ha hb ab) (pointAt_order c hb hd bd) (pointAt_order c hd he de)
      ((cap_sign c a b d ha hb hd ab bd).mp h1) ((cap_sign c b d e hb hd he bd de).mp h2)
    exact ⟨(cap_sign c a b e ha hb he ab (lt_trans bd de)).mpr result.1,
      (cap_sign c a d e ha hd he (lt_trans ab bd) de).mpr result.2⟩

/-- A concrete cup list is an all-triples cup on actual indices. -/
theorem hasCup_of_list {n k} (c : Configuration n)
    (h : (colorConfig c.cup true).HasNCup k (Finset.range n)) : c.HasCup k := by
  obtain ⟨xs, ⟨chain, len⟩, inside⟩ := h
  let f : Fin k → Fin n := fun i => ⟨xs.get ⟨i.val, by omega⟩,
    Finset.mem_range.mp (inside _ (xs.get_mem _))⟩
  have hf : StrictMono f := fun _ _ hij => List.Sorted.rel_get_of_lt chain.1.pairwise hij
  refine ⟨f, hf, ?_⟩
  intro i j l hij hjl
  have h := cup_list_all c xs inside chain _ (xs.get_mem ⟨i.val, by omega⟩)
    _ (xs.get_mem ⟨j.val, by omega⟩) _ (xs.get_mem ⟨l.val, by omega⟩) (hf hij) (hf hjl)
  change 0 < orient (pointAt c (f i).val) (pointAt c (f j).val) (pointAt c (f l).val) at h
  rw [pointAt_eq c _ (f i).isLt, pointAt_eq c _ (f j).isLt,
    pointAt_eq c _ (f l).isLt] at h
  exact h

/-- A concrete cap list is an all-triples cap on actual indices. -/
theorem hasCap_of_list {n k} (c : Configuration n)
    (h : (colorConfig c.cup true).HasNCap k (Finset.range n)) : c.HasCap k := by
  obtain ⟨xs, ⟨chain, len⟩, inside⟩ := h
  let f : Fin k → Fin n := fun i => ⟨xs.get ⟨i.val, by omega⟩,
    Finset.mem_range.mp (inside _ (xs.get_mem _))⟩
  have hf : StrictMono f := fun _ _ hij => List.Sorted.rel_get_of_lt chain.1.pairwise hij
  refine ⟨f, hf, ?_⟩
  intro i j l hij hjl
  have h := cap_list_all c xs inside chain _ (xs.get_mem ⟨i.val, by omega⟩)
    _ (xs.get_mem ⟨j.val, by omega⟩) _ (xs.get_mem ⟨l.val, by omega⟩) (hf hij) (hf hjl)
  change orient (pointAt c (f i).val) (pointAt c (f j).val) (pointAt c (f l).val) < 0 at h
  rw [pointAt_eq c _ (f i).isLt, pointAt_eq c _ (f j).isLt,
    pointAt_eq c _ (f l).isLt] at h
  exact h

/-- Every eight-cup gives an actual convex octagon. -/
theorem hasNCup_octagon {n} (c : Configuration n)
    (h : (colorConfig c.cup true).HasNCup 8 (Finset.range n)) :
    HasConvexNGon 8 (Finset.univ.image c.point) := by
  obtain ⟨f, hf, positive⟩ := hasCup_of_list c h
  have hp : Function.Injective c.point := fun _ _ eq => c.xOrder.injective (congrArg (· 0) eq)
  exact hasConvexNGon_of_positive_cycle (by omega) c.point hp ⟨f, hf.injective⟩
    (fun i => Finset.mem_image_of_mem c.point (Finset.mem_univ (f i))) positive

private theorem chain3_of_all {α : Type*} [LinearOrder α] (R : α → α → α → Prop)
    (xs : List α) (sorted : xs.Pairwise (· < ·)) (all : OrderedTriples R xs) : xs.Chain3' R := by
  cases xs with
  | nil => trivial
  | cons a xs =>
    cases xs with
    | nil => trivial
    | cons b xs =>
      cases xs with
      | nil => exact List.Chain3.nil
      | cons d xs =>
        apply List.chain3'_cons.mpr
        refine ⟨all a (by simp) b (by simp) d (by simp)
          ((List.pairwise_cons.mp sorted).1 b (by simp))
          ((List.pairwise_cons.mp sorted.tail).1 d (by simp)), ?_⟩
        exact chain3_of_all R _ sorted.tail (fun x hx y hy z hz =>
          all x (by simp [hx]) y (by simp [hy]) z (by simp [hz]))

/-- Enumerating an all-triples witness gives the exact consecutive-list predicate. -/
theorem listCup_of_hasCup {n k} (c : Configuration n) (h : c.HasCup k) :
    (colorConfig c.cup true).HasNCup k (Finset.range n) := by
  obtain ⟨f, hf, positive⟩ := h
  let xs := List.ofFn (fun i => (f i).val)
  have sorted : xs.Pairwise (· < ·) := List.pairwise_ofFn.mpr (fun _ _ hij => hf hij)
  refine ⟨xs, ⟨⟨sorted.isChain, ?_⟩, List.length_ofFn⟩, ?_⟩
  · apply chain3_of_all _ xs sorted
    intro a ha b hb d hd ab bd
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp ha
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hb
    obtain ⟨l, rfl⟩ := List.mem_ofFn.mp hd
    exact (c.cup_true_iff _ _ _).mpr (positive i j l
      (hf.lt_iff_lt.mp ab) (hf.lt_iff_lt.mp bd))
  · intro a ha
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp ha
    exact Finset.mem_range.mpr (f i).isLt

theorem listCap_of_hasCap {n k} (c : Configuration n) (h : c.HasCap k) :
    (colorConfig c.cup true).HasNCap k (Finset.range n) := by
  obtain ⟨f, hf, negative⟩ := h
  let xs := List.ofFn (fun i => (f i).val)
  have sorted : xs.Pairwise (· < ·) := List.pairwise_ofFn.mpr (fun _ _ hij => hf hij)
  refine ⟨xs, ⟨(false_cup_iff_cap c.cup xs).mp ⟨sorted.isChain, ?_⟩, List.length_ofFn⟩, ?_⟩
  · apply chain3_of_all _ xs sorted
    intro a ha b hb d hd ab bd
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp ha
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hb
    obtain ⟨l, rfl⟩ := List.mem_ofFn.mp hd
    exact (c.cup_false_iff _ _ _ ab bd).mpr (negative i j l
      (hf.lt_iff_lt.mp ab) (hf.lt_iff_lt.mp bd))
  · intro a ha
    obtain ⟨i, rfl⟩ := List.mem_ofFn.mp ha
    exact Finset.mem_range.mpr (f i).isLt

end ErdosSzekeres.Omission.ListGeometry

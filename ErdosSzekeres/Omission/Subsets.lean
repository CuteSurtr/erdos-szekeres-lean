/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8Subset.lean (reindexing and junctions).
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: real points as Fin 2 → ℝ, local geometry and namespaces, Lean 4.24.
-/
import ErdosSzekeres.Omission.ListGeometry

namespace ErdosSzekeres.Omission.Subsets
open ActualRanks ListGeometry

noncomputable def restrict {n} (c : Configuration n) (S : Finset (Fin n)) : Configuration S.card where
  point := fun i=>c.point (S.orderEmbOfFin rfl i)
  xOrder := c.xOrder.comp (S.orderEmbOfFin rfl).strictMono
  generalPosition := fun _ _ _ uv vw=>c.generalPosition _ _ _
    ((S.orderEmbOfFin rfl).strictMono uv) ((S.orderEmbOfFin rfl).strictMono vw)

noncomputable def enum {n} (S : Finset (Fin n)) (i : Nat) : Nat :=
  if h : i<S.card then (S.orderEmbOfFin rfl ⟨i,h⟩).val else 0

def natSet {n} (S : Finset (Fin n)) : Finset Nat := S.image Fin.val

theorem enum_eq {n} (S : Finset (Fin n)) (i : Nat) (hi : i<S.card) :
    enum S i=(S.orderEmbOfFin rfl ⟨i,hi⟩).val := by simp [enum,hi]

theorem enum_bound {n} (S : Finset (Fin n)) (i : Nat) (hi : i<S.card) : enum S i<n := by
  rw [enum_eq S i hi]; exact (S.orderEmbOfFin rfl ⟨i,hi⟩).isLt

theorem enum_mem {n} (S : Finset (Fin n)) (i : Nat) (hi : i<S.card) : enum S i∈natSet S := by
  rw [enum_eq S i hi]
  exact Finset.mem_image.mpr ⟨_,S.orderEmbOfFin_mem rfl _,rfl⟩

theorem enum_order {n} (S : Finset (Fin n)) (i j : Nat) (ij : i<j) (hj : j<S.card) : enum S i<enum S j := by
  rw [enum_eq S i (by omega),enum_eq S j hj]
  exact (S.orderEmbOfFin rfl).strictMono (show (⟨i,by omega⟩ : Fin S.card)<⟨j,hj⟩ from ij)

theorem cup_eq {n} (c : Configuration n) (S : Finset (Fin n)) (u v w : Nat)
    (hu : u<S.card) (hv : v<S.card) (hw : w<S.card) :
    (restrict c S).cup u v w=c.cup (enum S u) (enum S v) (enum S w) := by
  simp [Configuration.cup,hu,hv,hw,enum,restrict]

/-- Relabel a bounded chain while preserving every actual consecutive witness. -/
theorem chain3_map (R T : Nat→Nat→Nat→Prop) (f : Nat→Nat) (xs : List Nat)
    (same : ∀ a∈xs, ∀ b∈xs, ∀ c∈xs, R a b c → T (f a) (f b) (f c))
    (chain : xs.Chain3' R) : (xs.map f).Chain3' T := by
  induction xs with
  | nil => trivial
  | cons a xs ih =>
    cases xs with
    | nil => trivial
    | cons b xs =>
      cases xs with
      | nil => exact List.Chain3.nil
      | cons c xs =>
        have split := List.chain3'_cons.mp chain
        apply List.chain3'_cons.mpr
        exact ⟨same a (by simp) b (by simp) c (by simp) split.1,
          ih (fun x hx y hy z hz=>same x (by simp [hx]) y (by simp [hy]) z (by simp [hz])) split.2⟩

theorem cup_map {n} (c : Configuration n) (S : Finset (Fin n)) (color : Bool) (xs : List Nat)
    (inside : xs.In (Finset.range S.card)) (chain : (colorConfig (restrict c S).cup color).Cup xs) :
    (colorConfig c.cup color).Cup (xs.map (enum S)) := by
  constructor
  · apply List.Pairwise.isChain
    apply List.pairwise_map.mpr
    exact chain.1.pairwise.imp_of_mem (fun {a b} _ hb ab=>enum_order S a b ab (Finset.mem_range.mp (inside b hb)))
  · apply chain3_map _ _ (enum S) xs _ chain.2
    intro a ha b hb d hd h
    change c.cup (enum S a) (enum S b) (enum S d)=color
    rw [←cup_eq c S a b d (Finset.mem_range.mp (inside a ha))
      (Finset.mem_range.mp (inside b hb)) (Finset.mem_range.mp (inside d hd))]
    exact h

theorem list_map_inside {n} (S : Finset (Fin n)) (xs : List Nat) (inside : xs.In (Finset.range S.card)) :
    (xs.map (enum S)).In (natSet S) := by
  intro a ha
  obtain ⟨i,hi,rfl⟩ := List.mem_map.mp ha
  exact enum_mem S i (Finset.mem_range.mp (inside i hi))

theorem hasCup_map {n} (c : Configuration n) (S : Finset (Fin n)) (k : Nat)
    (h : (colorConfig (restrict c S).cup true).HasNCup k (Finset.range S.card)) :
    (colorConfig c.cup true).HasNCup k (natSet S) := by
  obtain ⟨xs,⟨chain,len⟩,inside⟩ := h
  exact ⟨xs.map (enum S),⟨cup_map c S true xs inside chain,by simpa using len⟩,list_map_inside S xs inside⟩

theorem hasCap_map {n} (c : Configuration n) (S : Finset (Fin n)) (k : Nat)
    (h : (colorConfig (restrict c S).cup true).HasNCap k (Finset.range S.card)) :
    (colorConfig c.cup true).HasNCap k (natSet S) := by
  obtain ⟨xs,⟨chain,len⟩,inside⟩ := h
  have mapped := cup_map c S false xs inside ((false_cup_iff_cap _ _).mpr chain)
  exact ⟨xs.map (enum S),⟨(false_cup_iff_cap _ _).mp mapped,by simpa using len⟩,list_map_inside S xs inside⟩

/-- A junction witnessed wholly inside S. The incoming six-cup and outgoing
five-cap share their actual endpoint u; all other overlaps are permitted. -/
def JunctionOn (cup : Nat→Nat→Nat→Bool) (S : Finset Nat) (u : Nat) : Prop :=
  ∃ xs ys a b, (xs++[a,u]).length=6 ∧ (u::b::ys).length=5 ∧
    (colorConfig cup true).Cup (xs++[a,u]) ∧ (colorConfig cup false).Cup (u::b::ys) ∧
    (xs++[a,u]).In S ∧ (u::b::ys).In S

def NoJunctionOn (cup : Nat→Nat→Nat→Bool) (S : Finset Nat) : Prop := ∀ u, ¬JunctionOn cup S u

/-- The restriction uses exactly the chosen real points. -/
theorem restrict_image {n} (c : Configuration n) (S : Finset (Fin n)) :
    Finset.univ.image (restrict c S).point = S.image c.point := by
  change Finset.univ.image (c.point ∘ S.orderEmbOfFin rfl) = S.image c.point
  rw [← Finset.image_image, Finset.image_orderEmbOfFin_univ]

theorem restrict_no_octagon {n} (c : Configuration n) (S : Finset (Fin n))
    (avoid : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    ¬ HasConvexNGon 8 (Finset.univ.image (restrict c S).point) := by
  rw [restrict_image]
  exact fun h => avoid (h.mono (Finset.image_subset_image (Finset.subset_univ S)))

theorem restrict_no_cup {n k} (c : Configuration n) (S : Finset (Fin n))
    (avoid : ¬ (colorConfig c.cup true).HasNCup k (natSet S)) :
    ¬ (restrict c S).HasCup k :=
  fun h => avoid (hasCup_map c S k (listCup_of_hasCup _ h))

theorem restrict_no_cap {n k} (c : Configuration n) (S : Finset (Fin n))
    (avoid : ¬ (colorConfig c.cup true).HasNCap k (natSet S)) :
    ¬ (restrict c S).HasCap k :=
  fun h => avoid (hasCap_map c S k (listCap_of_hasCap _ h))

/-- Both sides of a junction are transported through the same enumeration. -/
theorem no_junction_restrict {n} (c : Configuration n) (S : Finset (Fin n))
    (avoid : NoJunctionOn c.cup (natSet S)) :
    NoJunctionOn (restrict c S).cup (Finset.range S.card) := by
  intro u h
  obtain ⟨xs, ys, a, b, xl, yl, xc, yc, xi, yi⟩ := h
  have xm := cup_map c S true _ xi xc
  have ym := cup_map c S false _ yi yc
  have xmem := list_map_inside S _ xi
  have ymem := list_map_inside S _ yi
  apply avoid (enum S u)
  refine ⟨xs.map (enum S), ys.map (enum S), enum S a, enum S b, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · simpa using xl
  · simpa using yl
  · simpa using xm
  · simpa using ym
  · simpa using xmem
  · simpa using ymem

end ErdosSzekeres.Omission.Subsets

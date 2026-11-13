import ErdosSzekeres.Suk.AdjacentCaps
import ErdosSzekeres.Suk.ChainEnumeration
import Mathlib.Data.Nat.Choose.Bounds

namespace ErdosSzekeres.Suk

/-- A finite chain in the actual outer-base triangle order of a support spike. -/
structure SpikeChain (F : CapFrame) where
  length : ℕ
  point : Fin length → F.spike
  increasing : StrictMono (fun i => F.toOuter (point i))

def SpikeChain.vertex {F : CapFrame} (C : SpikeChain F) (i : Fin C.length) : Point :=
  (C.point i).val

theorem SpikeChain.vertex_injective {F : CapFrame} (C : SpikeChain F) :
    Function.Injective C.vertex := by
  intro i j h
  exact C.increasing.injective (AboveBase.ext h)

noncomputable def SpikeChain.points {F : CapFrame} (C : SpikeChain F) : Finset Point :=
  Finset.univ.image C.vertex

theorem SpikeChain.card_points {F : CapFrame} (C : SpikeChain F) : C.points.card = C.length := by
  classical
  simp [points, Finset.card_image_of_injective _ C.vertex_injective]

/-- Any finite chain in the geometric outer-base order supplies a SpikeChain,
with exactly the same points and cardinality. -/
theorem SpikeChain.exists_of_finset (F : CapFrame) (s : Finset (AboveBase F.outerBase))
    (hspike : ∀ p ∈ s, p.val ∈ F.spike)
    (hchain : DilworthTheorem.IsChain (s : Set (AboveBase F.outerBase))) :
    ∃ C : SpikeChain F, C.length = s.card ∧ C.points = s.image AboveBase.val := by
  classical
  obtain ⟨f, hf, hmem⟩ := enumerate_finset_chain s hchain
  let p : Fin s.card → F.spike := fun i =>
    ⟨(f i).val, hspike (f i) ((hmem (f i)).mpr ⟨i, rfl⟩)⟩
  have he : (fun i => F.toOuter (p i)) = f := by
    funext i
    exact AboveBase.ext rfl
  let C : SpikeChain F := ⟨s.card, p, by rw [he]; exact hf⟩
  refine ⟨C, rfl, ?_⟩
  ext x
  constructor
  · intro hx
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hx
    exact Finset.mem_image.mpr ⟨f i, (hmem (f i)).mpr ⟨i, rfl⟩, rfl⟩
  · intro hx
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hx
    obtain ⟨i, hi⟩ := (hmem q).mp hq
    apply Finset.mem_image.mpr
    refine ⟨i, Finset.mem_univ _, ?_⟩
    change (f i).val = q.val
    rw [hi]

/-- A cap facing the next spike, anchored at the right endpoint of the edge. -/
def SpikeChain.LeftCap {F : CapFrame} (C : SpikeChain F) (m : ℕ) : Prop :=
  ∃ s : Finset (Fin C.length), s.card = m ∧ ConvexPosition (insert F.c (s.image C.vertex))

/-- A cap facing the preceding spike, anchored at the left endpoint. -/
def SpikeChain.RightCap {F : CapFrame} (C : SpikeChain F) (m : ℕ) : Prop :=
  ∃ s : Finset (Fin C.length), s.card = m ∧ ConvexPosition (insert F.b (s.image C.vertex))

theorem SpikeChain.image_subset_points {F : CapFrame} (C : SpikeChain F)
    (s : Finset (Fin C.length)) : s.image C.vertex ⊆ C.points := by
  classical
  exact Finset.image_subset_image (Finset.subset_univ s)

theorem SpikeChain.leftCap_hasConvexNGon {F : CapFrame} (C : SpikeChain F)
    {m n : ℕ} (h : C.LeftCap m) (hn : n ≤ m) : HasConvexNGon n C.points := by
  classical
  obtain ⟨s, hs, hc⟩ := h
  have hconv := hc.mono (Finset.subset_insert F.c (s.image C.vertex))
  exact (hconv.hasConvexNGon (by simpa [Finset.card_image_of_injective _ C.vertex_injective, hs]
    using hn)).mono (C.image_subset_points s)

theorem SpikeChain.rightCap_hasConvexNGon {F : CapFrame} (C : SpikeChain F)
    {m n : ℕ} (h : C.RightCap m) (hn : n ≤ m) : HasConvexNGon n C.points := by
  classical
  obtain ⟨s, hs, hc⟩ := h
  have hconv := hc.mono (Finset.subset_insert F.b (s.image C.vertex))
  exact (hconv.hasConvexNGon (by simpa [Finset.card_image_of_injective _ C.vertex_injective, hs]
    using hn)).mono (C.image_subset_points s)

/-- A uniform exponential budget gives every cups-caps split used in the
growth induction. This is an unconditional theorem about a given geometric chain. -/
theorem SpikeChain.split_caps {F : CapFrame} (C : SpikeChain F) {n K a b : ℕ}
    (hgp : GeneralPosition (insert F.b (insert F.c C.points)))
    (hsize : 2 ^ (n + K - 4) < C.length)
    (ha : 3 ≤ a) (hb : 3 ≤ b) (hab : a + b ≤ n + K) : C.LeftCap a ∨ C.RightCap b := by
  classical
  have hbin : ((a - 2) + (b - 2)).choose (a - 2) < C.length := by
    calc
      _ ≤ 2 ^ ((a - 2) + (b - 2)) := Nat.choose_le_two_pow _ _
      _ ≤ 2 ^ (n + K - 4) := Nat.pow_le_pow_right (by omega) (by omega)
      _ < C.length := hsize
  rcases F.chain_caps C.point C.increasing Finset.univ hgp (a - 2) (b - 2)
      (by omega) (by omega) (by simpa using hbin) with ⟨s, _, hs, hc⟩ | ⟨s, _, hs, hc⟩
  · left
    exact ⟨s, by omega, hc⟩
  · right
    exact ⟨s, by omega, hc⟩

theorem AdjacentCapFrames.chain_points_disjoint (F : AdjacentCapFrames)
    (C : SpikeChain F.left) (D : SpikeChain F.right) : Disjoint C.points D.points := by
  classical
  apply Finset.disjoint_left.mpr
  intro x hx hy
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hx
  obtain ⟨j, _, hj⟩ := Finset.mem_image.mp hy
  have h₀ := (C.point i).property.2.1
  have h₁ := (D.point j).property.1
  change 0 < orient F.left.b F.left.c (C.vertex i) at h₀
  change orient F.left.b F.left.c (D.vertex j) < 0 at h₁
  rw [hj] at h₁
  linarith

/-- Adjacent cap witnesses give a convex n-gon in the ambient set as soon
as their total cardinality reaches n. The cardinality is proved, not assumed. -/
theorem AdjacentCapFrames.glue_chain_caps (F : AdjacentCapFrames)
    (C : SpikeChain F.left) (D : SpikeChain F.right) {P : Finset Point}
    (hgp : GeneralPosition P) (hanchor : F.left.c ∈ P)
    (hC : C.points ⊆ P) (hD : D.points ⊆ P)
    {a b n : ℕ} (hn : 4 ≤ n) (hsize : n ≤ a + b)
    (hc : C.LeftCap a) (hd : D.RightCap b) : HasConvexNGon n P := by
  classical
  obtain ⟨s, hs, hsc⟩ := hc
  obtain ⟨t, ht, htc⟩ := hd
  have hsub : s.image C.vertex ∪ t.image D.vertex ⊆ P :=
    Finset.union_subset (C.image_subset_points s |>.trans hC) (D.image_subset_points t |>.trans hD)
  have hgen := hgp.mono (Finset.insert_subset_iff.mpr ⟨hanchor, hsub⟩)
  have hconv := F.glue_caps C.point D.point C.increasing D.increasing s t
    (by omega) hgen hsc htc
  have hdis : Disjoint (s.image C.vertex) (t.image D.vertex) :=
    (F.chain_points_disjoint C D).mono (C.image_subset_points s) (D.image_subset_points t)
  have hcard : (s.image C.vertex ∪ t.image D.vertex).card = a + b := by
    rw [Finset.card_union_of_disjoint hdis,
      Finset.card_image_of_injective _ C.vertex_injective,
      Finset.card_image_of_injective _ D.vertex_injective, hs, ht]
  exact (hconv.hasConvexNGon (hsize.trans_eq hcard.symm)).mono hsub

end ErdosSzekeres.Suk

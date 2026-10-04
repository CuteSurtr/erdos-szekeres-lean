import ErdosSzekeres.Suk.AdjacentSpikes
import ErdosSzekeres.Suk.ChainCaps
import ErdosSzekeres.Suk.GlueOrientation
import ErdosSzekeres.Suk.Quadrilateral

namespace ErdosSzekeres.Suk

/-- Suk's adjacent-chain gluing observation, with the support regions and
triangle orders defined geometrically. The two caps face the common anchor c.
Four or more selected vertices suffice; there is no assumed separation lemma. -/
theorem AdjacentCapFrames.glue_caps (F : AdjacentCapFrames)
    {ι κ : Type*} [LinearOrder ι] [LinearOrder κ]
    (p : ι → F.left.spike) (q : κ → F.right.spike)
    (hp : StrictMono (fun i => F.left.toOuter (p i)))
    (hq : StrictMono (fun i => F.right.toOuter (q i)))
    (s : Finset ι) (t : Finset κ) (hcard : 4 ≤ s.card + t.card)
    (hgp : GeneralPosition (insert F.left.c
      (s.image (fun i => (p i).val) ∪ t.image (fun i => (q i).val))))
    (hleft : ConvexPosition (insert F.left.c (s.image (fun i => (p i).val))))
    (hright : ConvexPosition (insert F.left.c (t.image (fun i => (q i).val)))) :
    ConvexPosition (s.image (fun i => (p i).val) ∪ t.image (fun i => (q i).val)) := by
  classical
  let f : ι → Point := fun i => (p i).val
  let g : κ → Point := fun i => (q i).val
  have hf : Function.Injective f := by
    intro i j he
    exact hp.injective (AboveBase.ext he)
  have hg : Function.Injective g := by
    intro i j he
    exact hq.injective (AboveBase.ext he)
  have hne (i : ι) (j : κ) : f i ≠ g j := by
    intro he
    have h₀ := (p i).property.2.1
    have h₁ := (q j).property.1
    change 0 < orient F.left.b F.left.c (f i) at h₀
    change orient F.left.b F.left.c (g j) < 0 at h₁
    rw [he] at h₀
    linarith
  have hfc (i : ι) : f i ≠ F.left.c := by
    intro he
    have h := (p i).property.2.1
    change 0 < orient F.left.b F.left.c (f i) at h
    rw [he] at h
    simp only [orient] at h
    nlinarith
  have hgc (i : κ) : g i ≠ F.left.c := by
    intro he
    have h := (q i).property.2.1
    change 0 < orient F.left.c F.left.d (g i) at h
    rw [he] at h
    simp [orient] at h
  have hfm (i : ι) (hi : i ∈ s) : f i ∈ insert F.left.c (s.image f ∪ t.image g) :=
    Finset.mem_insert_of_mem (Finset.mem_union_left _ (Finset.mem_image_of_mem f hi))
  have hgm (i : κ) (hi : i ∈ t) : g i ∈ insert F.left.c (s.image f ∪ t.image g) :=
    Finset.mem_insert_of_mem (Finset.mem_union_right _ (Finset.mem_image_of_mem g hi))
  have hnonzero := (generalPosition_iff_orient_ne_zero _).mp hgp
  have hfpair (i : ι) (hi : i ∈ s) (j : ι) (hj : j ∈ s) (hij : i < j) :
      0 < orient (f i) (f j) F.left.c := by
    have hle := ((F.left.toEdge (p i)).pair_orientation_sides (F.left.toEdge (p j))
      (F.left.toEdge_lt_of_toOuter_lt _ _ (hp hij)).le).2
    have hn := hnonzero _ (hfm i hi) _ (hfm j hj) _ (by simp) (hf.ne hij.ne) (hfc i) (hfc j)
    exact lt_of_le_of_ne hle hn.symm
  have hgpair (i : κ) (hi : i ∈ t) (j : κ) (hj : j ∈ t) (hij : i < j) :
      orient (g i) (g j) F.left.c < 0 := by
    have hle := ((F.right.toEdge (q i)).pair_orientation_sides (F.right.toEdge (q j))
      (F.right.toEdge_lt_of_toOuter_lt _ _ (hq hij)).le).1
    have hn := hnonzero _ (hgm i hi) _ (hgm j hj) _ (by simp) (hg.ne hij.ne) (hgc i) (hgc j)
    exact lt_of_le_of_ne hle hn
  apply convexPosition_glue_orientation f g hf hg hne s t hcard
  · intro i hi j hj k hk hij hjk
    have hn := hnonzero _ (hfm i hi) _ (hfm j hj) _ (hfm k hk)
      (hf.ne hij.ne) (hf.ne (hij.trans hjk).ne) (hf.ne hjk.ne)
    apply (convexPosition_four_iff_positive_of_anchor _ _ _ _ hn
      (hfpair i hi j hj hij) (hfpair i hi k hk (hij.trans hjk)) (hfpair j hj k hk hjk)).mp
    apply hleft.mono
    simp only [Finset.insert_subset_iff, Finset.singleton_subset_iff]
    exact ⟨Finset.mem_insert_of_mem (Finset.mem_image_of_mem f hi),
      Finset.mem_insert_of_mem (Finset.mem_image_of_mem f hj),
      Finset.mem_insert_of_mem (Finset.mem_image_of_mem f hk), Finset.mem_insert_self _ _⟩
  · intro i hi j hj k hk hij hjk
    have hn := hnonzero _ (hgm i hi) _ (hgm j hj) _ (hgm k hk)
      (hg.ne hij.ne) (hg.ne (hij.trans hjk).ne) (hg.ne hjk.ne)
    apply (convexPosition_four_iff_negative_of_anchor _ _ _ _ hn
      (hgpair i hi j hj hij) (hgpair i hi k hk (hij.trans hjk)) (hgpair j hj k hk hjk)).mp
    apply hright.mono
    simp only [Finset.insert_subset_iff, Finset.singleton_subset_iff]
    exact ⟨Finset.mem_insert_of_mem (Finset.mem_image_of_mem g hi),
      Finset.mem_insert_of_mem (Finset.mem_image_of_mem g hj),
      Finset.mem_insert_of_mem (Finset.mem_image_of_mem g hk), Finset.mem_insert_self _ _⟩
  · intro i hi j hj k hk hij
    have hn := hnonzero _ (hfm i hi) _ (hfm j hj) _ (hgm k hk)
      (hf.ne hij.ne) (hne i k) (hne j k)
    exact lt_of_le_of_ne (F.ordered_pair_right (p i) (p j) (q k) (hp hij).le) hn.symm
  · intro i hi j hj k hk hij
    have hn := hnonzero _ (hgm i hi) _ (hgm j hj) _ (hfm k hk)
      (hg.ne hij.ne) (hne k i).symm (hne k j).symm
    exact lt_of_le_of_ne (F.ordered_pair_left (q i) (q j) (p k) (hq hij).le) hn

end ErdosSzekeres.Suk

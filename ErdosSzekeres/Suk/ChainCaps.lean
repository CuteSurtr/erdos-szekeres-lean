import ErdosSzekeres.Suk.BaseOrientation
import ErdosSzekeres.Suk.OrientationClique
import ErdosSzekeres.Suk.SpikeGeometry

namespace ErdosSzekeres.Suk

/-- Cups-caps extraction along the geometric triangle order, with cap
convexity proved relative to the actual base endpoints. -/
theorem chain_caps {ι : Type*} [LinearOrder ι] (B : BaseSegment)
    (p : ι → AboveBase B) (hp : StrictMono p) (s : Finset ι)
    (hgp : GeneralPosition (insert B.left (insert B.right (s.image (fun i => (p i).val)))))
    (a b : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b) (hcard : (a + b).choose a < s.card) :
    (∃ t ⊆ s, t.card = a + 2 ∧
      ConvexPosition (insert B.right (t.image (fun i => (p i).val)))) ∨
    (∃ t ⊆ s, t.card = b + 2 ∧
      ConvexPosition (insert B.left (t.image (fun i => (p i).val)))) := by
  classical
  let f : ι → Point := fun i => (p i).val
  have hf : Function.Injective f := by
    intro i j he
    exact hp.injective (AboveBase.ext he)
  have hleft (i : ι) : B.left ≠ f i := by
    intro he
    have h := (p i).property
    change 0 < orient B.left B.right (f i) at h
    rw [← he] at h
    simp [orient] at h
  have hright (i : ι) : B.right ≠ f i := by
    intro he
    have h := (p i).property
    change 0 < orient B.left B.right (f i) at h
    rw [← he] at h
    simp only [orient] at h
    nlinarith
  have hg := (generalPosition_iff_orient_ne_zero _).mp hgp
  have hmem (i : ι) (hi : i ∈ s) :
      f i ∈ insert B.left (insert B.right (s.image f)) := by
    exact Finset.mem_insert_of_mem (Finset.mem_insert_of_mem (Finset.mem_image.mpr ⟨i, hi, rfl⟩))
  have htr : TripleTransitive (fun i j k => 0 < orient (f i) (f j) (f k)) := by
    intro i j k l hij hjk hkl
    exact AboveBase.positive_transitive B _ _ _ _ (hp hij) (hp hjk) (hp hkl)
  have hntr : TripleTransitive (fun i j k => ¬ 0 < orient (f i) (f j) (f k)) := by
    intro i j k l hij hjk hkl
    exact AboveBase.nonpositive_transitive B _ _ _ _ (hp hij) (hp hjk) (hp hkl)
  rcases transitive_cups_caps _ htr hntr a b s hcard with ⟨t, hts, ht, hc⟩ | ⟨t, hts, ht, hc⟩
  · left
    refine ⟨t, hts, ht, ?_⟩
    apply convexPosition_insert_of_positive_triples f hf t (by omega) B.right hright hc
    intro i hi j hj hij
    have hne : orient (f i) (f j) B.right ≠ 0 :=
      hg _ (hmem i (hts hi)) _ (hmem j (hts hj)) _ (by simp)
        (hf.ne hij.ne) (hright i).symm (hright j).symm
    exact lt_of_le_of_ne ((p i).pair_orientation_sides (p j) (hp hij).le).2 hne.symm
  · right
    refine ⟨t, hts, ht, ?_⟩
    apply convexPosition_insert_of_negative_triples f hf t (by omega) B.left hleft
    · intro i hi j hj k hk hij hjk
      have hne : orient (f i) (f j) (f k) ≠ 0 :=
        hg _ (hmem i (hts hi)) _ (hmem j (hts hj)) _ (hmem k (hts hk))
          (hf.ne hij.ne) (hf.ne (hij.trans hjk).ne) (hf.ne hjk.ne)
      exact lt_of_le_of_ne (le_of_not_gt (hc i hi j hj k hk hij hjk)) hne
    · intro i hi j hj hij
      have hne : orient (f i) (f j) B.left ≠ 0 :=
        hg _ (hmem i (hts hi)) _ (hmem j (hts hj)) _ (by simp)
          (hf.ne hij.ne) (hleft i).symm (hleft j).symm
      exact lt_of_le_of_ne ((p i).pair_orientation_sides (p j) (hp hij).le).1 hne

/-- Suk's cap extraction inside one support spike. The order is defined
using the outer base a--d, while the caps use the middle edge endpoints b,c,
exactly as in Section 3 of the paper. -/
theorem CapFrame.chain_caps (F : CapFrame) {ι : Type*} [LinearOrder ι]
    (p : ι → F.spike) (hp : StrictMono (fun i => F.toOuter (p i))) (s : Finset ι)
    (hgp : GeneralPosition (insert F.b (insert F.c (s.image (fun i => (p i).val)))))
    (a b : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b) (hcard : (a + b).choose a < s.card) :
    (∃ t ⊆ s, t.card = a + 2 ∧
      ConvexPosition (insert F.c (t.image (fun i => (p i).val)))) ∨
    (∃ t ⊆ s, t.card = b + 2 ∧
      ConvexPosition (insert F.b (t.image (fun i => (p i).val)))) := by
  exact ErdosSzekeres.Suk.chain_caps F.edgeBase (fun i => F.toEdge (p i))
    (fun i j hij => F.toEdge_lt_of_toOuter_lt _ _ (hp hij)) s hgp a b ha hb hcard

end ErdosSzekeres.Suk

import ErdosSzekeres.Suk.SpikeChain

namespace ErdosSzekeres.Suk

/-- Dilworth's alternative for a finite set in a support spike, with actual
geometric output on both sides and exact preservation of cardinality. -/
theorem CapFrame.spike_chain_or_antichain (F : CapFrame) (s : Finset Point)
    (hspike : ∀ p ∈ s, p ∈ F.spike) (a b : ℕ) (hsize : a * b < s.card) :
    (∃ C : SpikeChain F, a < C.length ∧ C.points ⊆ s) ∨
    (∃ t ⊆ s, b < t.card ∧ ∀ p ∈ t, ∀ q ∈ t, p ≠ q →
      q ∉ convexHull ℝ ({F.a, F.d, p} : Set Point)) := by
  classical
  let f : ↥s → AboveBase F.outerBase := fun p => F.toOuter ⟨p.val, hspike p.val p.property⟩
  have hf : Function.Injective f := by
    intro p q he
    apply Subtype.ext
    exact congrArg AboveBase.val he
  let R : Finset (AboveBase F.outerBase) := s.attach.image f
  have hR : R.card = s.card := by simp [R, Finset.card_image_of_injective _ hf]
  have hmem (p : AboveBase F.outerBase) (hp : p ∈ R) : p.val ∈ s ∧ p.val ∈ F.spike := by
    obtain ⟨q, _, rfl⟩ := Finset.mem_image.mp hp
    exact ⟨q.property, hspike q.val q.property⟩
  have hv : Function.Injective (@AboveBase.val F.outerBase) := fun p q he => AboveBase.ext he
  rcases chain_or_antichain R (a + 1) (b + 1) (by omega) (by omega)
      (by simpa [hR] using hsize) with ⟨t, ht, hc, hcard⟩ | ⟨t, ht, ha, hcard⟩
  · obtain ⟨C, hlen, hpoints⟩ := SpikeChain.exists_of_finset F t
      (fun p hp => (hmem p (ht hp)).2) hc
    left
    refine ⟨C, by omega, ?_⟩
    rw [hpoints]
    intro p hp
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hp
    exact (hmem q (ht hq)).1
  · right
    refine ⟨t.image AboveBase.val, ?_, ?_, ?_⟩
    · intro p hp
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hp
      exact (hmem q (ht hq)).1
    · rw [Finset.card_image_of_injective _ hv]
      omega
    · intro p hp q hq hpq
      obtain ⟨p', hp', rfl⟩ := Finset.mem_image.mp hp
      obtain ⟨q', hq', rfl⟩ := Finset.mem_image.mp hq
      have hne : p' ≠ q' := fun he => hpq (congrArg AboveBase.val he)
      exact fun h => (ha p' q' hp' hq' hne).1 ((AboveBase.le_iff p' q').mpr h)

end ErdosSzekeres.Suk

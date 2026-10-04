import ErdosSzekeres.Suk.SupportSequence

namespace ErdosSzekeres.Suk

def evenVertices {α : Type*} {m : ℕ} (p : Fin (2 * m) → α) (i : Fin m) : α :=
  p ⟨2 * i.val, by omega⟩

def oddVertices {α : Type*} {m : ℕ} (p : Fin (2 * m) → α) (i : Fin m) : α :=
  p ⟨2 * i.val + 1, by omega⟩

/-- The two alternating vertex lists determine the entire configuration.
This is the injection used when counting configurations with fixed anchors. -/
theorem alternating_vertices_injective {α : Type*} (m : ℕ) :
    Function.Injective (fun p : Fin (2 * m) → α => (evenVertices p, oddVertices p)) := by
  intro p q he
  have h₀ := congrArg Prod.fst he
  have h₁ := congrArg Prod.snd he
  funext i
  let j : Fin m := ⟨i.val / 2, by omega⟩
  by_cases hmod : i.val % 2 = 0
  · have hij : (⟨2 * j.val, by omega⟩ : Fin (2 * m)) = i := by
      apply Fin.ext
      dsimp [j]
      omega
    have h := congrFun h₀ j
    change p ⟨2 * j.val, by omega⟩ = q ⟨2 * j.val, by omega⟩ at h
    simpa only [hij] using h
  · have hij : (⟨2 * j.val + 1, by omega⟩ : Fin (2 * m)) = i := by
      apply Fin.ext
      dsimp [j]
      omega
    have h := congrFun h₁ j
    change p ⟨2 * j.val + 1, by omega⟩ = q ⟨2 * j.val + 1, by omega⟩ at h
    simpa only [hij] using h

def ClockwiseAnchors.even {m : ℕ} (A : ClockwiseAnchors (2 * m)) : ClockwiseAnchors m where
  point := evenVertices A.point
  clockwise i j k hij hjk := A.clockwise _ _ _
    (by change 2 * i.val < 2 * j.val; omega)
    (by change 2 * j.val < 2 * k.val; omega)

/-- Alternating vertices of a clockwise cap lie in the interior support
spikes of its even-indexed anchor sequence. Three odd endpoint vertices
are outside these interior windows and must be counted separately. -/
theorem ClockwiseAnchors.odd_mem_even_spike {m : ℕ}
    (A : ClockwiseAnchors (2 * (m + 3))) (i : Fin m) :
    oddVertices A.point ⟨i.val + 1, by omega⟩ ∈ (A.even.frame i).spike := by
  refine ⟨?_, ?_, ?_⟩
  · exact A.clockwise _ _ _
      (by change 2 * i.val < 2 * (i.val + 1); omega)
      (by change 2 * (i.val + 1) < 2 * (i.val + 1) + 1; omega)
  · change 0 < orient (A.point _) (A.point _) (A.point _)
    rw [orient_swap]
    apply neg_pos.mpr
    exact A.clockwise _ _ _
      (by change 2 * (i.val + 1) < 2 * (i.val + 1) + 1; omega)
      (by change 2 * (i.val + 1) + 1 < 2 * (i.val + 2); omega)
  · change orient (A.point _) (A.point _) (A.point _) < 0
    rw [orient_cycle]
    exact A.clockwise _ _ _
      (by change 2 * (i.val + 1) + 1 < 2 * (i.val + 2); omega)
      (by change 2 * (i.val + 2) < 2 * (i.val + 3); omega)

end ErdosSzekeres.Suk

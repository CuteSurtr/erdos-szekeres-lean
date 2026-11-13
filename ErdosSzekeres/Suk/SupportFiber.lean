import ErdosSzekeres.Suk.AlternatingAnchors
import Mathlib.Combinatorics.Enumerative.DoubleCounting
import Mathlib.Data.Fintype.BigOperators

namespace ErdosSzekeres.Suk

open scoped BigOperators

/-- Separate the three uncontrolled endpoint entries from the interior ones. -/
def endpointPayload {α : Type*} {m : ℕ} (p : Fin (m + 3) → α) :
    α × α × α × (Fin m → α) :=
  (p ⟨0, by omega⟩, p ⟨m + 1, by omega⟩, p ⟨m + 2, by omega⟩,
    fun i => p ⟨i.val + 1, by omega⟩)

theorem endpointPayload_injective {α : Type*} (m : ℕ) :
    Function.Injective (@endpointPayload α m) := by
  intro p q he
  have h₀ := congrArg (fun x : α × α × α × (Fin m → α) => x.1) he
  have h₁ := congrArg (fun x : α × α × α × (Fin m → α) => x.2.1) he
  have h₂ := congrArg (fun x : α × α × α × (Fin m → α) => x.2.2.1) he
  have hI := congrArg (fun x : α × α × α × (Fin m → α) => x.2.2.2) he
  funext i
  by_cases hi₀ : i.val = 0
  · have hi : i = ⟨0, by omega⟩ := Fin.ext hi₀
    rw [hi]
    exact h₀
  by_cases hi₁ : i.val = m + 1
  · have hi : i = ⟨m + 1, by omega⟩ := Fin.ext hi₁
    rw [hi]
    exact h₁
  by_cases hi₂ : i.val = m + 2
  · have hi : i = ⟨m + 2, by omega⟩ := Fin.ext hi₂
    rw [hi]
    exact h₂
  let j : Fin m := ⟨i.val - 1, by omega⟩
  have hij : (⟨j.val + 1, by omega⟩ : Fin (m + 3)) = i := by
    apply Fin.ext
    dsimp [j]
    omega
  have h := congrFun hI j
  change p ⟨j.val + 1, by omega⟩ = q ⟨j.val + 1, by omega⟩ at h
  simpa only [hij] using h

/-- A fixed alternating anchor sequence supports at most the product of its
interior spike sizes, times |S|^3 for the three uncontrolled endpoint vertices. -/
theorem support_fiber_card_le {m : ℕ} (S : Finset Point)
    (A : ClockwiseAnchors (m + 3)) (F : Finset (Fin (2 * (m + 3)) → Point))
    (hpoints : ∀ p ∈ F, ∀ i, p i ∈ S)
    (hanchors : ∀ p ∈ F, evenVertices p = A.point)
    (hclockwise : ∀ p ∈ F, ∀ i j k, i < j → j < k → orient (p i) (p j) (p k) < 0) :
    F.card ≤ S.card ^ 3 * ∏ i : Fin m, ((A.frame i).region S).card := by
  classical
  let regions : Fin m → Finset Point := fun i => (A.frame i).region S
  let T := S ×ˢ (S ×ˢ (S ×ˢ Fintype.piFinset regions))
  have hcard : F.card ≤ T.card := by
    apply Finset.card_le_card_of_injOn (fun p => endpointPayload (oddVertices p))
    · intro p hp
      have hsp (i : Fin m) : oddVertices p ⟨i.val + 1, by omega⟩ ∈ (A.frame i).spike := by
        let C : ClockwiseAnchors (2 * (m + 3)) := ⟨p, hclockwise p hp⟩
        have hC : C.even = A := ClockwiseAnchors.ext (hanchors p hp)
        have h := C.odd_mem_even_spike i
        rw [hC] at h
        exact h
      refine Finset.mem_product.mpr ⟨hpoints p hp _, Finset.mem_product.mpr
        ⟨hpoints p hp _, Finset.mem_product.mpr ⟨hpoints p hp _, ?_⟩⟩⟩
      apply Fintype.mem_piFinset.mpr
      intro i
      exact ((A.frame i).mem_region S _).mpr ⟨hpoints p hp _, hsp i⟩
    · intro p hp q hq he
      apply alternating_vertices_injective (m + 3)
      exact Prod.ext ((hanchors p hp).trans (hanchors q hq).symm)
        (endpointPayload_injective m he)
  convert hcard using 1
  simp only [T, Finset.card_product, Fintype.card_piFinset]
  ring

/-- Pigeonhole the family by its alternating anchor list. Anchor lists are
counted conservatively by |S|^m; no cyclic-order enumeration is assumed. -/
theorem exists_large_alternating_fiber {α : Type*} [DecidableEq α] {m B : ℕ}
    (S : Finset α) (F : Finset (Fin (2 * m) → α))
    (hpoints : ∀ p ∈ F, ∀ i, p i ∈ S) (hsize : S.card ^ m * B < F.card) :
    ∃ a : Fin m → α, (∀ i, a i ∈ S) ∧ B < (F.filter (fun p => evenVertices p = a)).card := by
  classical
  let U := Fintype.piFinset (fun _ : Fin m => S)
  by_contra! hn
  have hlo : ∀ p ∈ F, 1 ≤ (U.bipartiteAbove (fun p a => evenVertices p = a) p).card := by
    intro p hp
    apply Nat.succ_le_iff.mpr
    apply Finset.card_pos.mpr
    refine ⟨evenVertices p, (Finset.mem_bipartiteAbove _).mpr ⟨?_, rfl⟩⟩
    exact Fintype.mem_piFinset.mpr (fun i => hpoints p hp _)
  have hhi : ∀ a ∈ U, (F.bipartiteBelow (fun p a => evenVertices p = a) a).card ≤ B := by
    intro a ha
    exact hn a (Fintype.mem_piFinset.mp ha)
  have hc := Finset.card_mul_le_card_mul (fun p a => evenVertices p = a) hlo hhi
  have he : U.card = S.card ^ m := by simp [U]
  simp only [mul_one, he] at hc
  omega

end ErdosSzekeres.Suk

import ErdosSzekeres.Suk.FiniteSupport

namespace ErdosSzekeres.Suk

/-- A point outside the original middle edge stays outside any longer edge
with the same left endpoint and a later right endpoint in the cap. -/
theorem ClockwiseAnchors.spike_long_edge_positive {m : ℕ}
    (A : ClockwiseAnchors (m + 3)) (i : Fin m) {p : Point}
    (hp : p ∈ (A.frame i).spike) (c : Fin (m + 3)) (hc : i.val + 2 ≤ c.val) :
    0 < orient (A.frame i).b (A.point c) p := by
  by_cases he : c.val = i.val + 2
  · have hc' : c = ⟨i.val + 2, by omega⟩ := Fin.ext he
    rw [hc']
    exact hp.2.1
  · let a : Fin (m + 3) := ⟨i.val, by omega⟩
    let b : Fin (m + 3) := ⟨i.val + 1, by omega⟩
    let d : Fin (m + 3) := ⟨i.val + 2, by omega⟩
    have hab : a < b := by change i.val < i.val + 1; omega
    have hbd : b < d := by change i.val + 1 < i.val + 2; omega
    have hdc : d < c := by change i.val + 2 < c.val; omega
    let F := A.frameOfIndices a b d c hab hbd hdc
    have hF : p ∈ F.spike :=
      ⟨hp.1, hp.2.1, A.spike_right_boundary i hp c hdc⟩
    exact (F.spike_orientations hF).2.2

/-- Deleting intermediate anchors enlarges the relevant support spike.
The middle left endpoint is retained; the neighboring anchors may move
outward and the middle right endpoint may move to the right. -/
theorem ClockwiseAnchors.spike_subset_coarsened {m : ℕ}
    (A : ClockwiseAnchors (m + 3)) (i : Fin m)
    (a c d : Fin (m + 3))
    (ha : a.val < i.val + 1) (hc : i.val + 2 ≤ c.val) (hcd : c < d) :
    (A.frame i).spike ⊆
      (A.frameOfIndices a ⟨i.val + 1, by omega⟩ c d
        ha (by change i.val + 1 < c.val; omega) hcd).spike := by
  intro p hp
  exact ⟨A.spike_left_boundary i hp a ha,
    A.spike_long_edge_positive i hp c hc,
    A.spike_before_pair i hp c d hcd hc⟩

/-- Select the left endpoints of an increasing list of original support
spikes as a new clockwise anchor sequence. -/
def ClockwiseAnchors.coarsen {m k : ℕ} (A : ClockwiseAnchors (m + 3))
    (e : Fin (k + 3) ↪o Fin m) : ClockwiseAnchors (k + 3) where
  point i := A.point ⟨(e i).val + 1, by have := (e i).isLt; omega⟩
  clockwise i j l hij hjl := A.clockwise _ _ _
    (by have h := e.strictMono hij; change (e i).val + 1 < (e j).val + 1; omega)
    (by have h := e.strictMono hjl; change (e j).val + 1 < (e l).val + 1; omega)

/-- Each interior region of the coarsened sequence contains the original
region indexed by its middle left anchor. -/
theorem ClockwiseAnchors.spike_subset_coarsen {m k : ℕ}
    (A : ClockwiseAnchors (m + 3)) (e : Fin (k + 3) ↪o Fin m) (i : Fin k) :
    (A.frame (e ⟨i.val + 1, by omega⟩)).spike ⊆ ((A.coarsen e).frame i).spike := by
  have h₀ := e.strictMono (show (⟨i.val, by omega⟩ : Fin (k + 3)) <
    ⟨i.val + 1, by omega⟩ from by change i.val < i.val + 1; omega)
  have h₁ := e.strictMono (show (⟨i.val + 1, by omega⟩ : Fin (k + 3)) <
    ⟨i.val + 2, by omega⟩ from by change i.val + 1 < i.val + 2; omega)
  have h₂ := e.strictMono (show (⟨i.val + 2, by omega⟩ : Fin (k + 3)) <
    ⟨i.val + 3, by omega⟩ from by change i.val + 2 < i.val + 3; omega)
  exact A.spike_subset_coarsened (e ⟨i.val + 1, by omega⟩)
    ⟨(e ⟨i.val, by omega⟩).val + 1, by omega⟩
    ⟨(e ⟨i.val + 2, by omega⟩).val + 1, by omega⟩
    ⟨(e ⟨i.val + 3, by omega⟩).val + 1, by omega⟩
    (by change _ + 1 < _ + 1; omega) (by change _ + 2 ≤ _ + 1; omega)
    (by change _ + 1 < _ + 1; omega)

/-- Rich regions need not initially be consecutive. Any k+3 rich spikes
yield a k+3-anchor support configuration with k rich interior spikes. -/
theorem ClockwiseAnchors.extract_rich_spikes {m k B : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (m + 3)) (hx : StrictMono (fun i => A.point i 0))
    (Q : Fin m → Finset Point) (I : Finset (Fin m)) (hI : k + 3 ≤ I.card)
    (hanchors : ∀ i, A.point i ∈ P) (hpoints : ∀ i ∈ I, Q i ⊆ P)
    (hspike : ∀ i ∈ I, ∀ p ∈ Q i, p ∈ (A.frame i).spike)
    (hsize : ∀ i ∈ I, B < (Q i).card) :
    ∃ (C : ClockwiseAnchors (k + 3)) (R : Fin k → Finset Point),
      StrictMono (fun i => C.point i 0) ∧ (∀ i, C.point i ∈ P) ∧
      (∀ i, R i ⊆ P) ∧ (∀ i, ∀ p ∈ R i, p ∈ (C.frame i).spike) ∧
      ∀ i, B < (R i).card := by
  classical
  obtain ⟨J, hJI, hJ⟩ := Finset.exists_subset_card_eq hI
  let e : Fin (k + 3) ↪o Fin m := J.orderEmbOfFin hJ
  have he (i : Fin (k + 3)) : e i ∈ I := hJI (Finset.orderEmbOfFin_mem J hJ i)
  let R : Fin k → Finset Point := fun i => Q (e ⟨i.val + 1, by omega⟩)
  refine ⟨A.coarsen e, R, ?_, ?_, ?_, ?_, ?_⟩
  · intro i j hij
    apply hx
    have h := e.strictMono hij
    change (e i).val + 1 < (e j).val + 1
    omega
  · intro i
    exact hanchors _
  · intro i
    exact hpoints _ (he _)
  · intro i p hp
    exact A.spike_subset_coarsen e i (hspike _ (he _) p hp)
  · intro i
    exact hsize _ (he _)

end ErdosSzekeres.Suk

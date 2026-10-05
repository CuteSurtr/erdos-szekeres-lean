import ErdosSzekeres.IntegerCertificates
import ErdosSzekeres.HMPT.AntichainCapacity

namespace ErdosSzekeres.HMPT.MixedCap

open Suk

def anchorZ (i : Fin 6) : Fin 2 → ℤ := ![10000 * i.val, -100000 * (i.val : ℤ)^2]
def chainZ (i : Fin 8) : Fin 2 → ℤ :=
  ![15000 + 100 * i.val, -200000 - 4900 * i.val + (i.val : ℤ)^2]
def innerZ (i : Fin 8) : Fin 2 → ℤ :=
  ![35000 + 100 * i.val, -1200000 - 7000 * i.val - (i.val : ℤ)^2]

def anchor (i : Fin 6) : Point := integerToReal (anchorZ i)
def chainPoint (i : Fin 8) : Point := integerToReal (chainZ i)
def innerPoint (i : Fin 8) : Point := integerToReal (innerZ i)

noncomputable def anchors : Finset Point := Finset.univ.image anchor
noncomputable def chainPoints : Finset Point := Finset.univ.image chainPoint
noncomputable def innerPoints : Finset Point := Finset.univ.image innerPoint
noncomputable def ambient : Finset Point := anchors ∪ chainPoints ∪ innerPoints

set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

theorem anchors_clockwise : ∀ i j k : Fin 6, i < j → j < k →
    orient (anchorZ i) (anchorZ j) (anchorZ k) < 0 := by decide +kernel

def support : ClockwiseAnchors 6 where
  point := anchor
  clockwise := by
    intro i j k hij hjk
    simp only [anchor, orient_integerToReal]
    exact_mod_cast anchors_clockwise i j k hij hjk

def firstFrame : CapFrame := support.frame (0 : Fin 3)
def lastFrame : CapFrame := support.frame (2 : Fin 3)

/-- These finite interior certificates, checked by kernel reduction, are the
two obstructions that control every convex subset of the 22-point example. -/
theorem three_chain_one_inner : ∀ i j k t : Fin 8, i < j → j < k →
    IntegerInterior (chainZ j) (chainZ i) (chainZ k) (innerZ t) := by decide +kernel

theorem two_chain_anchor_inner : ∀ i j t : Fin 8, i < j →
    IntegerInterior (chainZ j) (chainZ i) (anchorZ 2) (innerZ t) := by decide +kernel

theorem chain_nested : ∀ i j : Fin 8, i < j →
    IntegerInterior (chainZ j) (anchorZ 0) (anchorZ 3) (chainZ i) := by decide +kernel

theorem chain_spike_signs : ∀ i : Fin 8,
    orient (anchorZ 0) (anchorZ 1) (chainZ i) < 0 ∧
    0 < orient (anchorZ 1) (anchorZ 2) (chainZ i) ∧
    orient (anchorZ 2) (anchorZ 3) (chainZ i) < 0 := by decide +kernel

theorem inner_spike_signs : ∀ i : Fin 8,
    orient (anchorZ 2) (anchorZ 3) (innerZ i) < 0 ∧
    0 < orient (anchorZ 3) (anchorZ 4) (innerZ i) ∧
    orient (anchorZ 4) (anchorZ 5) (innerZ i) < 0 := by decide +kernel

theorem chain_injective : Function.Injective chainPoint := by
  intro i j he
  have hx : (15000 : ℝ) + 100 * i.val = 15000 + 100 * j.val := by
    simpa [chainPoint, integerToReal, chainZ] using congrFun he 0
  have hv : (i.val : ℝ) = j.val := by linarith
  exact Fin.ext (by exact_mod_cast hv)

theorem anchor_injective : Function.Injective anchor := by
  intro i j he
  have hx : (10000 : ℝ) * i.val = 10000 * j.val := by
    simpa [anchor, integerToReal, anchorZ] using congrFun he 0
  have hv : (i.val : ℝ) = j.val := by linarith
  exact Fin.ext (by exact_mod_cast hv)

theorem inner_injective : Function.Injective innerPoint := by
  intro i j he
  have hx : (35000 : ℝ) + 100 * i.val = 35000 + 100 * j.val := by
    simpa [innerPoint, integerToReal, innerZ] using congrFun he 0
  have hv : (i.val : ℝ) = j.val := by linarith
  exact Fin.ext (by exact_mod_cast hv)

theorem card_anchors : anchors.card = 6 := by
  classical
  simp [anchors, Finset.card_image_of_injective _ anchor_injective]

theorem card_chainPoints : chainPoints.card = 8 := by
  classical
  simp [chainPoints, Finset.card_image_of_injective _ chain_injective]

theorem card_innerPoints : innerPoints.card = 8 := by
  classical
  simp [innerPoints, Finset.card_image_of_injective _ inner_injective]

def leftZ (i : Fin 9) : Fin 2 → ℤ :=
  if h : i.val < 8 then chainZ ⟨i.val, h⟩ else anchorZ 2

theorem left_support_certificate : ∀ i : Fin 9,
    leftZ i ≠ leftZ (i + 1) ∧ ∀ k : Fin 9,
    leftZ k ≠ leftZ i → leftZ k ≠ leftZ (i + 1) →
    0 < orient (leftZ i) (leftZ (i + 1)) (leftZ k) := by decide +kernel

def innerNeighbor (i : Fin 8) : Fin 8 := if i = 0 then 1 else i - 1

theorem inner_support_certificate : ∀ i : Fin 8,
    innerZ i ≠ innerZ (innerNeighbor i) ∧ ∀ k : Fin 8,
    innerZ k ≠ innerZ i → innerZ k ≠ innerZ (innerNeighbor i) →
    0 < orient (innerZ i) (innerZ (innerNeighbor i)) (anchorZ 2) *
      orient (innerZ i) (innerZ (innerNeighbor i)) (innerZ k) := by decide +kernel

theorem inner_pair_sides : ∀ i j : Fin 8, i ≠ j →
    0 < orient (innerZ i) (innerZ j) (anchorZ 2) *
      orient (innerZ i) (innerZ j) (anchorZ 5) := by decide +kernel

theorem inner_outer_pos : ∀ i : Fin 8,
    0 < orient (anchorZ 2) (anchorZ 5) (innerZ i) := by decide +kernel

def allZ (i : Fin 22) : Fin 2 → ℤ :=
  if h : i.val < 6 then anchorZ ⟨i.val, h⟩
  else if h' : i.val < 14 then chainZ ⟨i.val - 6, by omega⟩
  else innerZ ⟨i.val - 14, by omega⟩

theorem all_general_position : ∀ i j k : Fin 22, i ≠ j → i ≠ k → j ≠ k →
    orient (allZ i) (allZ j) (allZ k) ≠ 0 := by decide +kernel

theorem all_distinct_x : ∀ i j : Fin 22, i ≠ j → allZ i 0 ≠ allZ j 0 := by decide +kernel

def fifteenZ (i : Fin 15) : Fin 2 → ℤ :=
  if h : i.val < 6 then anchorZ ⟨i.val, h⟩
  else if h' : i.val < 14 then innerZ ⟨i.val - 6, by omega⟩
  else chainZ 7

theorem fifteen_support_certificate : ∀ i : Fin 15, ∃ j : Fin 15,
    fifteenZ i ≠ fifteenZ j ∧ ∀ k : Fin 15,
    fifteenZ k ≠ fifteenZ i → fifteenZ k ≠ fifteenZ j →
    0 < orient (fifteenZ i) (fifteenZ j) (fifteenZ k) := by decide +kernel

theorem fifteen_distinct_x : ∀ i j : Fin 15, i ≠ j →
    fifteenZ i 0 ≠ fifteenZ j 0 := by decide +kernel

end ErdosSzekeres.HMPT.MixedCap

import ErdosSzekeres.IntegerCertificates
import ErdosSzekeres.OrientationConvexity
import Mathlib.Data.Finset.Sort
import T12FiniteFacts
import T12IndexHelpers

/-! Auxiliary declarations for the separately checked real-coordinate bridge. -/

noncomputable section

namespace Delta3.Terminal12.RealBridge

def integerPoint (i : Index) : Fin 2 → ℤ := fun j =>
  match j.val with
  | 0 => (point i).1
  | _ => (point i).2

def realPoint (i : Index) : ErdosSzekeres.Point :=
  ErdosSzekeres.integerToReal (integerPoint i)

theorem integer_orient (a b c : Index) :
    ErdosSzekeres.orient (integerPoint a) (integerPoint b) (integerPoint c) = det a b c := rfl

theorem real_orient (a b c : Index) :
    ErdosSzekeres.orient (realPoint a) (realPoint b) (realPoint c) = (det a b c : ℝ) := by
  exact (ErdosSzekeres.orient_integerToReal _ _ _).trans (congrArg Int.cast (integer_orient a b c))

theorem real_x_strict : StrictMono (fun i : Index => realPoint i 0) := by
  intro i j hij
  change ((point i).1 : ℝ) < ((point j).1 : ℝ)
  exact_mod_cast increasing_x i j hij

theorem realPoint_injective : Function.Injective realPoint :=
  fun _ _ h => real_x_strict.injective (congrFun h 0)

theorem real_orient_ne (a b c : Index) (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) :
    ErdosSzekeres.orient (realPoint a) (realPoint b) (realPoint c) ≠ 0 := by
  rw [real_orient]
  exact_mod_cast distinct_det_ne a b c hab hac hbc

def realSet : Finset ErdosSzekeres.Point := by
  classical
  exact Finset.univ.image realPoint

theorem realSet_card : realSet.card = 12 := by
  classical
  rw [realSet, Finset.card_image_of_injective _ realPoint_injective]
  simp

theorem realSet_generalPosition : ErdosSzekeres.GeneralPosition realSet := by
  classical
  rw [ErdosSzekeres.generalPosition_iff_orient_ne_zero]
  intro a ha b hb c hc hab hac hbc
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp ha
  obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hb
  obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp hc
  exact real_orient_ne i j k
    (fun h => hab (congrArg realPoint h))
    (fun h => hac (congrArg realPoint h))
    (fun h => hbc (congrArg realPoint h))

#print axioms integer_orient
#print axioms real_orient
#print axioms real_x_strict
#print axioms realPoint_injective
#print axioms real_orient_ne
#print axioms realSet_card
#print axioms realSet_generalPosition

end Delta3.Terminal12.RealBridge

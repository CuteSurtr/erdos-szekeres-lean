import ErdosSzekeres.Definitions
import ErdosSzekeres.Orientation
import Mathlib.Tactic.Linarith

namespace ErdosSzekeres

/-- The four signs in lexicographic triple order have at most one change. -/
def PacketValid (a b c d : Bool) : Prop :=
  (a = c → a = b) ∧ (a = d → a = b ∧ a = c) ∧ (b = d → b = c)

instance (a b c d : Bool) : Decidable (PacketValid a b c d) := by
  unfold PacketValid
  infer_instance

theorem packetValid_iff_eight_patterns (a b c d : Bool) :
    PacketValid a b c d ↔
      [a, b, c, d] ∈ [[false, false, false, false], [true, false, false, false],
        [true, true, false, false], [true, true, true, false],
        [false, false, false, true], [false, false, true, true],
        [false, true, true, true], [true, true, true, true]] := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

private theorem sign_between {u v w α β γ : ℝ}
    (hα : 0 < α) (hβ : 0 < β) (hγ : 0 < γ)
    (heq : α * v = β * u + γ * w)
    (hsign : (0 < u) ↔ (0 < w)) : (0 < u) ↔ (0 < v) := by
  by_cases hu : 0 < u
  · have hw := hsign.mp hu
    have hv : 0 < v := by nlinarith
    simp [hu, hv]
  · have hw : w ≤ 0 := le_of_not_gt (fun h => hu (hsign.mpr h))
    have hu' : u ≤ 0 := le_of_not_gt hu
    have hv : v ≤ 0 := by nlinarith
    simp [hu, not_lt.mpr hv]

/-- Every x-ordered real quadruple satisfies the packet condition used in the
prefix search. General position is unnecessary for this necessary condition;
zero determinants are treated as nonpositive. -/
theorem packetValid_of_xordered (a b c d : Point)
    (hab : a 0 < b 0) (hbc : b 0 < c 0) (hcd : c 0 < d 0) :
    PacketValid (decide (0 < orient a b c)) (decide (0 < orient a b d))
      (decide (0 < orient a c d)) (decide (0 < orient b c d)) := by
  classical
  have left : (c 0 - a 0) * orient a b d =
      (d 0 - a 0) * orient a b c + (b 0 - a 0) * orient a c d := by
    simp only [orient]; ring
  have right : (d 0 - b 0) * orient a c d =
      (d 0 - c 0) * orient a b d + (d 0 - a 0) * orient b c d := by
    simp only [orient]; ring
  have middle : (c 0 - b 0) * orient a b d =
      (d 0 - b 0) * orient a b c + (b 0 - a 0) * orient b c d := by
    simp only [orient]; ring
  have hl := sign_between (by linarith : 0 < c 0 - a 0)
    (by linarith : 0 < d 0 - a 0) (by linarith : 0 < b 0 - a 0) left
  have hr := sign_between (by linarith : 0 < d 0 - b 0)
    (by linarith : 0 < d 0 - c 0) (by linarith : 0 < d 0 - a 0) right
  have hm := sign_between (by linarith : 0 < c 0 - b 0)
    (by linarith : 0 < d 0 - b 0) (by linarith : 0 < b 0 - a 0) middle
  unfold PacketValid
  simp only [decide_eq_decide]
  refine ⟨hl, ?_, hr⟩
  intro h
  have hb := hm h
  exact ⟨hb, hb.trans (hr (hb.symm.trans h))⟩

end ErdosSzekeres

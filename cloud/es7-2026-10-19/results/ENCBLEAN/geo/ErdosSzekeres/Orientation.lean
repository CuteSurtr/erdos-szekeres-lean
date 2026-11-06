import Mathlib.Data.Rat.Cast.Order
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

namespace ErdosSzekeres

/-- Signed twice-area. Positive means counterclockwise, zero means collinear. -/
def orient {R : Type*} [CommRing R] (a b c : Fin 2 → R) : R :=
  (b 0 - a 0) * (c 1 - a 1) - (b 1 - a 1) * (c 0 - a 0)

theorem orient_swap {R : Type*} [CommRing R] (a b c : Fin 2 → R) :
    orient a c b = -orient a b c := by unfold orient; ring

theorem orient_cycle {R : Type*} [CommRing R] (a b c : Fin 2 → R) :
    orient b c a = orient a b c := by unfold orient; ring

theorem orient_translate {R : Type*} [CommRing R] (a b c v : Fin 2 → R) :
    orient (a + v) (b + v) (c + v) = orient a b c := by
  simp only [orient, Pi.add_apply]
  ring

def rationalToReal (p : Fin 2 → ℚ) : Fin 2 → ℝ := fun i => p i

theorem orient_rationalToReal (a b c : Fin 2 → ℚ) :
    orient (rationalToReal a) (rationalToReal b) (rationalToReal c) =
      (orient a b c : ℚ) := by
  simp [orient, rationalToReal]

/-- Exact rational nondegeneracy survives passage to the real plane. -/
theorem orient_rationalToReal_ne_zero (a b c : Fin 2 → ℚ) :
    orient (rationalToReal a) (rationalToReal b) (rationalToReal c) ≠ 0 ↔
      orient a b c ≠ 0 := by
  rw [orient_rationalToReal]
  exact_mod_cast (Iff.rfl : orient a b c ≠ 0 ↔ orient a b c ≠ 0)

end ErdosSzekeres

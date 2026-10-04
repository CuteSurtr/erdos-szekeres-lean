import Mathlib.Analysis.Convex.Independent
import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional
import Mathlib.Data.Finset.Card
import Mathlib.Data.Real.Basic

/-! The geometric problem uses ordinary convex polygons, with no emptiness requirement. -/
namespace ErdosSzekeres

abbrev Point := Fin 2 → ℝ

/-- No three distinct points are collinear. Finsets already exclude duplicate points. -/
def GeneralPosition (s : Finset Point) : Prop :=
  ∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s,
    a ≠ b → a ≠ c → b ≠ c → ¬ Collinear ℝ ({a, b, c} : Set Point)

/-- All selected points are vertices of their convex hull. -/
def ConvexPosition (s : Finset Point) : Prop :=
  ConvexIndependent ℝ (fun p : (s : Set Point) => (p : Point))

/-- A convex n-gon whose vertices belong to s; other points may lie inside. -/
def HasConvexNGon (n : ℕ) (s : Finset Point) : Prop :=
  ∃ t : Finset Point, t ⊆ s ∧ t.card = n ∧ ConvexPosition t

/-- N is a sufficient number of points to force a convex n-gon. -/
def ForcesConvexNGon (N n : ℕ) : Prop :=
  ∀ s : Finset Point, GeneralPosition s → N ≤ s.card → HasConvexNGon n s

def conjecturedBound (n : ℕ) : ℕ := 2 ^ (n - 2) + 1

/-- An open proposition, deliberately not declared as a theorem or an axiom. -/
def ErdosSzekeresConjecture : Prop :=
  ∀ n : ℕ, 3 ≤ n → ForcesConvexNGon (conjecturedBound n) n

/-- The first currently open case: every 33 points force a convex heptagon. -/
def HeptagonConjecture : Prop := ForcesConvexNGon 33 7

end ErdosSzekeres

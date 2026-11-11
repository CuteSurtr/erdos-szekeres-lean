import ErdosSzekeres.Definitions
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Data.Fin.VecNotation
import LeanLB.Data.C4N52
import LeanLB.Data.C6N60
import LeanLB.Data.C2N64
import LeanLB.Data.MirN46
import LeanLB.Data.C3N61
import LeanLB.Data.C5N56
import LeanLB.Data.C7N64

/-!
# The statements (trusted part, together with `ErdosSzekeres/Definitions.lean` and `LeanLB/Data/*`)

`ErdosSzekeres.Point`, `GeneralPosition`, `ConvexPosition` and `HasConvexNGon` are the repository's
definitions (`ErdosSzekeres/Definitions.lean`, copied verbatim). `Invariant` and `rotAbout` are
copied verbatim from `LAYERLEAN/LayerLemma.lean` (the same text is in
`ENCBLEAN/geo/ES8Geo/OrbitConsistency.lean`, whose `sixfold_es8` uses them for the upper bound), and
`lineRefl` from `SYMLEAN/mirror/ReductionThreeClasses.lean` (used by `mirror_eight_line`).

The point sets are the rows of the repository's files, read as in `ES8SYM/README.md` §2:
* a `.pts` row `w_0 … w_{m-1}` is the point `Σ_j w_j ζ^j`, `ζ = e^{2πi/m}` (`cycPoint m`);
* a row `a b` of `c3_61pts_centre.txt` is `a + bω`, `ω = e^{2πi/3}`, which is again `cycPoint 3`;
* a row `x y` of the other `.txt` files is the integer point `(x, y)` (`intPoint`).
-/

namespace LeanLB

open ErdosSzekeres

/-- `f` maps `S` into itself. (Verbatim from `LAYERLEAN/LayerLemma.lean`.) -/
def Invariant (f : Point → Point) (S : Finset Point) : Prop := ∀ p ∈ S, f p ∈ S

/-- Rotation about `c` by the angle `θ`, in coordinates. (Verbatim from `LAYERLEAN/LayerLemma.lean`.) -/
noncomputable def rotAbout (c : Point) (θ : ℝ) (p : Point) : Point :=
  ![c 0 + Real.cos θ * (p 0 - c 0) - Real.sin θ * (p 1 - c 1),
    c 1 + Real.sin θ * (p 0 - c 0) + Real.cos θ * (p 1 - c 1)]

/-- Reflection in the line `n0 * x + n1 * y = c` (for a unit normal `(n0, n1)`).
(The body is verbatim from `SYMLEAN/mirror/ReductionThreeClasses.lean`.) -/
noncomputable def lineRefl (n0 n1 c : ℝ) (p : Point) : Point :=
  ![p 0 - 2 * (n0 * p 0 + n1 * p 1 - c) * n0, p 1 - 2 * (n0 * p 0 + n1 * p 1 - c) * n1]

/-- `ζ_m^j = e^{2πij/m}` as a point of the plane. -/
noncomputable def unitRoot (m j : ℕ) : Point :=
  ![Real.cos (2 * Real.pi * j / m), Real.sin (2 * Real.pi * j / m)]

/-- The point `Σ_{j < m} w_j ζ_m^j` (missing coefficients count as `0`). -/
noncomputable def cycPoint (m : ℕ) (w : List ℤ) : Point :=
  ∑ j ∈ Finset.range m, ((w.getD j 0 : ℤ) : ℝ) • unitRoot m j

/-- The integer point `(x, y)` of a row `x y`. -/
noncomputable def intPoint (w : List ℤ) : Point :=
  ![((w.getD 0 0 : ℤ) : ℝ), ((w.getD 1 0 : ℤ) : ℝ)]

/-- `ES8SYM/sets/c4_52pts_13layers.pts`: 4-fold, 52 points. -/
noncomputable def setC4N52 : Finset Point := (c4N52Rows.map (cycPoint 4)).toFinset

/-- `SIX60/sets/c6_60pts_D.pts`: 6-fold, 60 points (order type D of `SIX60`). -/
noncomputable def setC6N60 : Finset Point := (c6N60Rows.map (cycPoint 6)).toFinset

/-- `ES8SYM/sets/c2_64points_k8.txt`: half-turn, 64 points. -/
noncomputable def setC2N64 : Finset Point := (c2N64Rows.map intPoint).toFinset

/-- `ES8SYM/sets/mirror_46points_k8.txt`: mirror symmetric in the line `x = 0`, 46 points. -/
noncomputable def setMirN46 : Finset Point := (mirN46Rows.map intPoint).toFinset

/-- `ES8SYM/sets4/c3_61pts_centre.txt`: 3-fold, 61 points (with the centre). -/
noncomputable def setC3N61 : Finset Point := (c3N61Rows.map (cycPoint 3)).toFinset

/-- `ES8SYM/sets3/c5_56pts_11layers_centre.pts`: 5-fold, 56 points (with the centre). -/
noncomputable def setC5N56 : Finset Point := (c5N56Rows.map (cycPoint 5)).toFinset

/-- `ES8SYM/sets/c7_64pts_small.pts`: 7-fold, 64 points (with the centre). -/
noncomputable def setC7N64 : Finset Point := (c7N64Rows.map (cycPoint 7)).toFinset

end LeanLB

import ETVEncoding.Main

/-!
# Targets stated as propositions

These are propositions, not theorems or axioms; nothing in the library assumes them.
Both are proved: `DistinctXReduction` in `ETVEncoding.Shear` (`distinctXReduction`) and
`XsbSound` in `ETVEncoding.Xsb` (`xsbSound`).
-/

namespace ETV

open ErdosSzekeres

/-- Dropping the distinct-x hypothesis; proved as `ETV.distinctXReduction` in
`ETVEncoding.Shear`. A shear `(x, y) ↦ (x + εy, y)` makes the x-coordinates of a finite set
distinct and preserves orientations and convex position. -/
def DistinctXReduction : Prop :=
  ∀ N K : ℕ,
    (∀ S : Finset Point, GeneralPosition S → LowerBound.DistinctX S → S.card = N →
      HasConvexNGon K S) → ForcesConvexNGon N K

/-- Soundness of `--xsb` (`dimacsXsb` is defined in `ETVEncoding.Clauses`); proved as
`ETV.xsbSound` in `ETVEncoding.Xsb`. If `σ` violates the clause, its x-mirror
`σ' i j k = σ (N-1-k) (N-1-j) (N-1-i)` satisfies it and is again a signotope with no `A`-cap,
no `U`-cup and no `K`-gon. -/
def XsbSound : Prop :=
  ∀ (N A U K : ℕ) (σ : Sig), 3 ≤ N → IsSignotope N σ → ¬HasCap σ N A → ¬HasCup σ N U →
    ¬HasGon σ N K → DimacsSatisfiable (dimacsXsb N A U K)

end ETV

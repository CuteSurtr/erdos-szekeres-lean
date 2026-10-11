import ErdosSzekeres.LowerBound.Construction
import ErdosSzekeres.Suk.CupsCaps

/-! The Erdős–Szekeres number as the least forcing size, with the classical
lower bound and the binomial upper bound. -/

namespace ErdosSzekeres

/-- The least number of points in general position that forces a convex `n`-gon. -/
noncomputable def esNumber (n : ℕ) : ℕ := sInf {N : ℕ | ForcesConvexNGon N n}

theorem forcesConvexNGon_esNumber {n : ℕ} (hn : 3 ≤ n) : ForcesConvexNGon (esNumber n) n :=
  Nat.sInf_mem (s := {N : ℕ | ForcesConvexNGon N n}) ⟨_, Suk.classical_upper_bound n hn⟩

theorem esNumber_le_of_forces {N n : ℕ} (h : ForcesConvexNGon N n) : esNumber n ≤ N :=
  Nat.sInf_le h

theorem forcesConvexNGon_iff_esNumber_le {N n : ℕ} (hn : 3 ≤ n) :
    ForcesConvexNGon N n ↔ esNumber n ≤ N :=
  ⟨esNumber_le_of_forces, (forcesConvexNGon_esNumber hn).mono⟩

/-- Erdős–Szekeres (1961): `2 ^ (n - 2) + 1 ≤ ES(n)`. -/
theorem conjecturedBound_le_esNumber {n : ℕ} (hn : 3 ≤ n) : conjecturedBound n ≤ esNumber n :=
  conjecturedBound_le_of_forces hn (forcesConvexNGon_esNumber hn)

/-- Erdős–Szekeres (1935): `ES(n) ≤ choose (2n - 4) (n - 2) + 1`. -/
theorem esNumber_le_choose {n : ℕ} (hn : 3 ≤ n) :
    esNumber n ≤ (2 * n - 4).choose (n - 2) + 1 :=
  esNumber_le_of_forces (Suk.classical_upper_bound n hn)

theorem erdosSzekeresConjecture_iff_esNumber :
    ErdosSzekeresConjecture ↔ ∀ n : ℕ, 3 ≤ n → esNumber n = conjecturedBound n := by
  constructor
  · intro h n hn
    exact le_antisymm (esNumber_le_of_forces (h n hn)) (conjecturedBound_le_esNumber hn)
  · intro h n hn
    rw [← h n hn]
    exact forcesConvexNGon_esNumber hn

theorem esNumber_three : esNumber 3 = 3 :=
  le_antisymm (esNumber_le_of_forces forces_triangle) (conjecturedBound_le_esNumber le_rfl)

/-- `ES(8) ≥ 65`. -/
theorem sixtyFive_le_esNumber_eight : 65 ≤ esNumber 8 :=
  conjecturedBound_le_esNumber (n := 8) (by norm_num)

end ErdosSzekeres

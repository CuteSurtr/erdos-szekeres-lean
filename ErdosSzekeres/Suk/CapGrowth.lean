import Mathlib.Tactic

namespace ErdosSzekeres.Suk

/-- Truncating the desired left cap at n and keeping the right target at
least three resolves the terminal small-cap case without a larger budget. -/
theorem cap_growth_parameters (n K c : ℕ) (hn : 3 ≤ n) (hK : 3 ≤ K) (hc : c ≤ n) :
    3 ≤ min n (c + K) ∧ 3 ≤ max 3 (n - c) ∧
      min n (c + K) + max 3 (n - c) ≤ n + K ∧ n ≤ c + max 3 (n - c) := by
  omega

/-- The finite induction behind Suk's chain case. The hypotheses explicitly
describe extraction and gluing; the geometric instance is proved separately.
Neither color is ever requested at a size below three. -/
theorem iterated_cap_growth (L R : ℕ → ℕ → Prop) (Done : Prop) (n K r : ℕ)
    (hn : 3 ≤ n) (hK : 3 ≤ K) (hreach : n ≤ r * K)
    (hleft : ∀ i < r, ∀ m, n ≤ m → L i m → Done)
    (hright : ∀ i < r, ∀ m, n ≤ m → R i m → Done)
    (hglue : ∀ i, i + 1 < r → ∀ a b, n ≤ a + b → L i a → R (i + 1) b → Done)
    (hsplit : ∀ i < r, ∀ a b, 3 ≤ a → 3 ≤ b → a + b ≤ n + K → L i a ∨ R i b) :
    Done := by
  classical
  by_contra hnot
  have hr : 0 < r := by
    by_contra! h
    have he : r = 0 := by omega
    simp [he] at hreach
    omega
  have grow : ∀ i, i < r → L i (min n ((i + 1) * K)) := by
    intro i
    induction i with
    | zero =>
      intro hi
      have hparams := cap_growth_parameters n K 0 hn hK (Nat.zero_le n)
      have hmax : max 3 n = n := by omega
      rcases hsplit 0 hi (min n K) n (by simpa using hparams.1) hn
          (by simpa [hmax] using hparams.2.2.1) with h | h
      · simpa using h
      · exact (hnot (hright 0 hi n le_rfl h)).elim
    | succ i ih =>
      intro hi
      have hip : i < r := by omega
      have hp := ih hip
      let c := min n ((i + 1) * K)
      have hc : c ≤ n := Nat.min_le_left _ _
      have hparams := cap_growth_parameters n K c hn hK hc
      have he : min n (c + K) = min n ((i + 1 + 1) * K) := by
        dsimp [c]
        simp only [Nat.add_mul, Nat.one_mul]
        omega
      rcases hsplit (i + 1) hi (min n (c + K)) (max 3 (n - c))
          hparams.1 hparams.2.1 hparams.2.2.1 with h | h
      · simpa only [he] using h
      · exact (hnot (hglue i hi c _ hparams.2.2.2 hp h)).elim
  have hlast := grow (r - 1) (by omega)
  have he : min n ((r - 1 + 1) * K) = n := by
    have hr' : r - 1 + 1 = r := by omega
    rw [hr', Nat.min_eq_left hreach]
  rw [he] at hlast
  exact hnot (hleft (r - 1) (by omega) n le_rfl hlast)

end ErdosSzekeres.Suk

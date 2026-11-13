import CompactChecker.Fast

/-! Prop-level composition of separately kernel-checked blocks (no re-evaluation). -/

namespace CompactChecker

open ErdosSzekeres.OmissionCertificates
open scoped BigOperators

theorem split_feas (c : FCat) (m n budget : ℕ) (mask : List ℕ) (v : ℕ)
    (hzero : ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget (mask.set v 2) holes)
    (hone : ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget (mask.set v 1) holes) :
    ¬ ∃ holes : Fin n → ℕ, FFeas c m n budget mask holes := by
  rintro ⟨holes, hbool, hrows, hb, hm, hz⟩
  by_cases hvn : v < n
  · have hcases : holes ⟨v, hvn⟩ = 0 ∨ holes ⟨v, hvn⟩ = 1 := by
      have := hbool ⟨v, hvn⟩
      omega
    rcases hcases with h0 | h1
    · obtain ⟨hm', hz'⟩ := feas_set mask v 2 holes hm hz (fun i hiv => by
        have hi' : i = ⟨v, hvn⟩ := Fin.ext hiv
        subst hi'
        exact ⟨fun h => absurd h (by decide), fun _ => h0⟩)
      exact hzero ⟨holes, hbool, hrows, hb, hm', hz'⟩
    · obtain ⟨hm', hz'⟩ := feas_set mask v 1 holes hm hz (fun i hiv => by
        have hi' : i = ⟨v, hvn⟩ := Fin.ext hiv
        subst hi'
        exact ⟨fun _ => h1, fun h => absurd h (by decide)⟩)
      exact hone ⟨holes, hbool, hrows, hb, hm', hz'⟩
  · obtain ⟨hm', hz'⟩ := feas_set mask v 2 holes hm hz (fun i hiv =>
      absurd (hiv ▸ i.isLt) hvn)
    exact hzero ⟨holes, hbool, hrows, hb, hm', hz'⟩

end CompactChecker

/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891. MIT, copyright (c) 2026 Michael Schroeder.
See docs/SCHROEDER-MIT.txt. Changes: local namespaces and Lean 4.24 APIs.
-/
import ErdosSzekeres.Vendor.ETV.Main.Main

/-! Specialization of Baek's theorem. Config.HasNGon is the upstream
combinatorial boundary definition; the real-plane interpretation is separate. -/
namespace ErdosSzekeres.Omission.Baek

theorem four_cap_or_eight_gon {α : Type*} [LinearOrder α] (C : Config α) (S : Finset α)
    (size : 23 ≤ S.card) : C.HasNCap 4 S ∨ C.HasNGon 8 S := by
  exact main 5 C S (by norm_num; exact size)

theorem capacity22 {α : Type*} [LinearOrder α] (C : Config α) (S : Finset α)
    (noCap : ¬ C.HasNCap 4 S) (noGon : ¬ C.HasNGon 8 S) : S.card ≤ 22 := by
  by_contra h
  have hs : 23 ≤ S.card := by omega
  exact (four_cap_or_eight_gon C S hs).elim noCap noGon

end ErdosSzekeres.Omission.Baek

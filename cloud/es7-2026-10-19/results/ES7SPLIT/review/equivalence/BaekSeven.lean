import ErdosSzekeres.Vendor.ETV.Main.Main

/-! Instantiation of the ported Baek (ETV a = 4) theorem at n = 7:
17 points (in an abstract configuration) contain a 4-cap or a 7-gon. -/

theorem baek_seven {γ : Type} [LinearOrder γ] (C : Config γ) (S : Finset γ)
    (h : 17 ≤ S.card) : C.HasNCap 4 S ∨ C.HasNGon 7 S := by
  have e : Nat.choose (4 + 2) 2 + 2 = 17 := by decide
  exact main 4 C S (e ▸ h)

#check @main
#print axioms baek_seven

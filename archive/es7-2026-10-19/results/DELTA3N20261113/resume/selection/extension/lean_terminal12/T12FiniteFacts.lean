import T12FiniteModel

set_option maxRecDepth 32768

namespace Delta3.Terminal12

theorem ordered_triples_nondegenerate :
    ∀ a b c : Index, a < b → b < c → det a b c ≠ 0 := by decide +kernel

theorem determinant_margin :
    ∀ a b c : Index, a < b → b < c → 45 ≤ (det a b c).natAbs := by decide +kernel

theorem no_five_cap : (choose 5 indices).all (fun s => !cap s) = true := by decide +kernel

#print axioms ordered_triples_nondegenerate
#print axioms determinant_margin
#print axioms no_five_cap

end Delta3.Terminal12

import FiniteModel

namespace Delta3.Balanced15

theorem ordered_triples_nondegenerate :
    ∀ a b c : Index, a < b → b < c → det a b c ≠ 0 := by decide

theorem determinant_margin :
    ∀ a b c : Index, a < b → b < c → 45 ≤ (det a b c).natAbs := by decide

theorem no_five_cap : (choose 5 indices).all (fun s => !cap s) = true := by decide

#print axioms ordered_triples_nondegenerate
#print axioms determinant_margin
#print axioms no_five_cap

end Delta3.Balanced15

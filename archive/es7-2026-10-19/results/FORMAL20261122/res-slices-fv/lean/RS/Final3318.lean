-- res-slices-fv (22 Nov 2026): the budget-33 slice (F, 18), (Lo, 15) of Res118, checked in Lean by the compact checker.
import RS3318.Root
import RS.Bridge3318
open CompactChecker
namespace RS
/-- Res118's hypothesis `s33_18`, exactly as `Res118.residual_bound_118_of_slices` states it. -/
theorem s33_18 : Res118.ResSliceExcludes [] 33 18 :=
  Res118.slice_of_root cat3318_ok RS3318.root
end RS
#print axioms RS.s33_18

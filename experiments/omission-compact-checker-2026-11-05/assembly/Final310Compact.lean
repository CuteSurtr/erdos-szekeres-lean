import BalancedBudgets
import Residual32Bridge2650.Rows
import E310.Final
open ErdosSzekeres
namespace ErdosSzekeres.Omission.Compact310
theorem balanced_population_187 : Partition.BalancedBound 187 :=
  OmissionBalanced.balanced_bound_of_hole_budget (budget := 64) E310.balanced_excludes_64
theorem residual_population_121 : Partition.ResidualBound 121 :=
  OmissionResidual32Bridge2650.residual_bound_121_of_excludes E310.residual_excludes_32
theorem forces_convex_octagon_310 : ForcesConvexNGon 310 8 :=
  Partition.forces_of_population_bounds (by omega) balanced_population_187 residual_population_121
#print axioms forces_convex_octagon_310
end ErdosSzekeres.Omission.Compact310

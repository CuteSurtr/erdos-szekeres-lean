import BalancedGeometry
import ErdosSzekeres.Omission.PopulationBounds

namespace ErdosSzekeres.Omission

theorem balanced_population_192 : Partition.BalancedBound 192 :=
  fun _ c noCap noCup noOct => OmissionBalanced.real_configuration_bound c noCap noCup noOct

#print axioms balanced_population_192

end ErdosSzekeres.Omission

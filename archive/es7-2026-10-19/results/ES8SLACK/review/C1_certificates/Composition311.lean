import ErdosSzekeres.Omission.PopulationBounds
import ErdosSzekeres.Omission.CycleGeometry
import ErdosSzekeres.Omission.CoverCuts

/-!
Re-check, against the prebuilt library, the last composition step of
`Final311/Final.lean` with the two population bounds as explicit hypotheses, print the
definitions the final statement unfolds to, and audit the axioms of the geometric
library theorems that the omission chain uses.
-/

open ErdosSzekeres ErdosSzekeres.Omission

theorem composition_311 (hB : Partition.BalancedBound 188)
    (hR : Partition.ResidualBound 121) : ForcesConvexNGon 311 8 :=
  Partition.forces_of_population_bounds (by omega) hB hR

theorem avoiding_310 (hB : Partition.BalancedBound 188)
    (hR : Partition.ResidualBound 121) (S : Finset Point) (gp : GeneralPosition S)
    (avoid : ¬ HasConvexNGon 8 S) : S.card ≤ 310 :=
  Partition.avoiding_card_le_of_population_bounds (by omega) hB hR S gp avoid

#print ErdosSzekeres.ForcesConvexNGon
#print ErdosSzekeres.HasConvexNGon
#print ErdosSzekeres.ConvexPosition
#print ErdosSzekeres.GeneralPosition
#print ErdosSzekeres.Omission.Partition.BalancedBound
#print ErdosSzekeres.Omission.Partition.ResidualBound
#print axioms composition_311
#print axioms avoiding_310
#print axioms ErdosSzekeres.Omission.Partition.exists_partition
#print axioms ErdosSzekeres.Omission.exists_cap_free_chart
#print axioms ErdosSzekeres.Omission.Configuration.list_cycle_hole_bound
#print axioms ErdosSzekeres.Omission.Configuration.occupied_card
#print axioms ErdosSzekeres.OmissionCertificates.rounded_cover_cut

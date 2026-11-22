/- Negative control (must NOT compile): the (20,15) slice hypothesis weakened to budget 34; same proof script. -/
import Res118.Glue
open ErdosSzekeres ErdosSzekeres.Omission OmissionResidual32Bridge2650 OmissionResidual32Transfer
namespace Res118Ctl
open Res118
theorem bad {P Q U A : List (List ℕ)}
    (n66 : OmissionZRow.N66Bound 55)
    (vP : BlockValid P) (vQ : BlockValid Q) (vU : BlockValid U) (vA : BlockValid A)
    (s33_18 : ResSliceExcludes [] 33 18)
    (s34_18 : ResSliceExcludes (P ++ Q) 34 18)
    (s34_19 : ResSliceExcludes P 34 19)
    (s35_18 : ResSliceExcludes (P ++ Q) 35 18)
    (s35_19 : ResSliceExcludes (P ++ Q ++ U) 35 19)
    (s35_20 : ResSliceExcludes (P ++ Q ++ A) 34 20) :
    Partition.ResidualBound 118 := by
  intro n c noCap noOctagon noJunction
  by_contra hn
  have hsum := holes_sum_add_population c noCap noOctagon noJunction
  have hF := hF18 c noCap noOctagon noJunction
  have hL := hLo n66 c noCap noOctagon noJunction
  have hp := sum_Lo_add_sum_F (holesOf (c.residualOccupied noCap noOctagon noJunction))
  have hpos : 0 < n := by omega
  have vPQ := vP.append vQ
  have vPQU := vPQ.append vU
  have vPQA := vPQ.append vA
  by_cases e33 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i +
      ∑ i ∈ Lo, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 33
  · exact slice_false s33_18 BlockValid.nil c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
  by_cases e34 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i +
      ∑ i ∈ Lo, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 34
  · by_cases f18 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 18
    · exact slice_false s34_18 vPQ c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
    · exact slice_false s34_19 vP c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
  by_cases f18 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 18
  · exact slice_false s35_18 vPQ c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
  by_cases f19 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 19
  · exact slice_false s35_19 vPQU c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
  · exact slice_false s35_20 vPQA c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
end Res118Ctl

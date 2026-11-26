import ResidualGeometry
import ResidualBlock00973
import ResidualBlock01165
import ResidualBlock01166
import ResidualBlock01167
import ResidualBlock01168
import ResidualBlock01169
import ResidualBlock01170
import ResidualBlock01171
import ResidualBlock01172
import ResidualBlock01173
import ResidualBlock01174
import ResidualBlock01175
import ResidualBlock01176
import ResidualBlock01177
import ResidualBlock01178
import ResidualBlock01179
import ResidualBlock01180
import ResidualBlock01181
import ResidualBlock01182
import ResidualBlock01183
import ResidualBlock01184
import ResidualBlock01185
import ResidualBlock01186
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
/-- Every residual row is necessary for an actual residual configuration.
This theorem does not assert an arithmetic population bound. -/
theorem all_geometric_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (r : Fin 1187) : demand r ≤ (support r \ c.residualOccupied noCap noOctagon noJunction).card := by
  by_cases h : r.val = 973
  · have he : r = ResidualBlock00973.row := Fin.ext h
    subst r; exact ResidualBlock00973.row_bound c noCap noOctagon noJunction
  · by_cases hi : r.val < 1165
    · exact all_nonblock_rows c noCap noOctagon noJunction r hi h
    · have lo : 1165 ≤ r.val := by omega
      have high := r.isLt
      generalize he : r.val = j at lo high
      interval_cases j
      · have hr : r = ResidualBlock01165.row := Fin.ext he
        subst r; exact ResidualBlock01165.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01166.row := Fin.ext he
        subst r; exact ResidualBlock01166.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01167.row := Fin.ext he
        subst r; exact ResidualBlock01167.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01168.row := Fin.ext he
        subst r; exact ResidualBlock01168.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01169.row := Fin.ext he
        subst r; exact ResidualBlock01169.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01170.row := Fin.ext he
        subst r; exact ResidualBlock01170.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01171.row := Fin.ext he
        subst r; exact ResidualBlock01171.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01172.row := Fin.ext he
        subst r; exact ResidualBlock01172.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01173.row := Fin.ext he
        subst r; exact ResidualBlock01173.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01174.row := Fin.ext he
        subst r; exact ResidualBlock01174.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01175.row := Fin.ext he
        subst r; exact ResidualBlock01175.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01176.row := Fin.ext he
        subst r; exact ResidualBlock01176.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01177.row := Fin.ext he
        subst r; exact ResidualBlock01177.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01178.row := Fin.ext he
        subst r; exact ResidualBlock01178.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01179.row := Fin.ext he
        subst r; exact ResidualBlock01179.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01180.row := Fin.ext he
        subst r; exact ResidualBlock01180.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01181.row := Fin.ext he
        subst r; exact ResidualBlock01181.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01182.row := Fin.ext he
        subst r; exact ResidualBlock01182.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01183.row := Fin.ext he
        subst r; exact ResidualBlock01183.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01184.row := Fin.ext he
        subst r; exact ResidualBlock01184.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01185.row := Fin.ext he
        subst r; exact ResidualBlock01185.row_bound c noCap noOctagon noJunction
      · have hr : r = ResidualBlock01186.row := Fin.ext he
        subst r; exact ResidualBlock01186.row_bound c noCap noOctagon noJunction
#print axioms all_geometric_rows
end OmissionResidual

import Root
import Occupancy
import Geometry00000
import Geometry00032
import Geometry00064
import Geometry00096
import Geometry00128
import Geometry00160
import Geometry00192
import Geometry00224
import Geometry00256
import Geometry00288
import Geometry00320
import Geometry00352
import Geometry00384
import Geometry00416
import Geometry00448
import Geometry00480
import Geometry00512
import Geometry00544
import Geometry00576
import Geometry00608
import Geometry00640
import Geometry00672
import Geometry00704
import Geometry00736
import Geometry00768
import Geometry00800
import Geometry00832
import Geometry00864
import Geometry00896
import Geometry00928
import Geometry00960
import Geometry00992
import Geometry01024
import Geometry01056
import Geometry01088
import Geometry01120
import Geometry01152
import Geometry01184
import Geometry01216
import Geometry01248
import Geometry01280
import Geometry01312
import Geometry01344
import Geometry01376
import Geometry01408
import Geometry01440
import Geometry01472
import Geometry01504
import Geometry01536
import Geometry01568
import Geometry01600
import Geometry01632
import Geometry01664
import Geometry01696
import Geometry01728
import Geometry01760
import Geometry01792
import Geometry01824
import Geometry01856
import Geometry01888
import Geometry01920
import Geometry01952
import Geometry01984
import Geometry02016
import Geometry02048
import Geometry02080
import Geometry02112
import Geometry02144
import Geometry02176
import Geometry02208
import Geometry02240
import Geometry02272
import Geometry02304
import Geometry02336
import Geometry02368
import Geometry02400
import Geometry02432
import Geometry02464
import Geometry02496
import Geometry02528
import Geometry02560
import Geometry02592
import Geometry02624
import Geometry02656
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
theorem all_geometric_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) : demand r ≤ (support r \ c.occupied noCap noCup).card := by
  have hblocks : r.val / 32 < 84 := by have := r.isLt; omega
  generalize hblock : r.val / 32 = block at hblocks
  interval_cases block
  · exact Geometry00000.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00032.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00064.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00096.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00128.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00160.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00192.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00224.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00256.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00288.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00320.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00352.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00384.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00416.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00448.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00480.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00512.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00544.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00576.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00608.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00640.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00672.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00704.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00736.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00768.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00800.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00832.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00864.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00896.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00928.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00960.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry00992.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01024.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01056.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01088.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01120.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01152.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01184.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01216.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01248.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01280.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01312.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01344.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01376.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01408.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01440.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01472.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01504.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01536.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01568.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01600.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01632.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01664.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01696.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01728.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01760.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01792.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01824.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01856.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01888.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01920.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01952.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry01984.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02016.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02048.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02080.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02112.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02144.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02176.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02208.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02240.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02272.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02304.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02336.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02368.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02400.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02432.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02464.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02496.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02528.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02560.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02592.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02624.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
  · exact Geometry02656.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)
theorem real_configuration_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) : n ≤ 192 := by
  have bound := occupied_card_le (c.occupied noCap noCup)
    (all_geometric_rows c noCap noCup noOctagon)
  simpa only [c.occupied_card noCap noCup] using bound
#print axioms all_geometric_rows
#print axioms real_configuration_bound
end OmissionBalanced

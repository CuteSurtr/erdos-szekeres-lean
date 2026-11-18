import FiniteModel

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem no_seven_part_14 :
    (((choose 7 indices).drop 3584).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_15 :
    (((choose 7 indices).drop 3840).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_16 :
    (((choose 7 indices).drop 4096).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_17 :
    (((choose 7 indices).drop 4352).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_18 :
    (((choose 7 indices).drop 4608).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_19 :
    (((choose 7 indices).drop 4864).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_20 :
    (((choose 7 indices).drop 5120).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

#print axioms no_seven_part_14
#print axioms no_seven_part_15
#print axioms no_seven_part_16
#print axioms no_seven_part_17
#print axioms no_seven_part_18
#print axioms no_seven_part_19
#print axioms no_seven_part_20

end Delta3.Balanced15

import FiniteModel

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem no_seven_part_7 :
    (((choose 7 indices).drop 1792).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_8 :
    (((choose 7 indices).drop 2048).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_9 :
    (((choose 7 indices).drop 2304).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_10 :
    (((choose 7 indices).drop 2560).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_11 :
    (((choose 7 indices).drop 2816).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_12 :
    (((choose 7 indices).drop 3072).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_13 :
    (((choose 7 indices).drop 3328).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

#print axioms no_seven_part_7
#print axioms no_seven_part_8
#print axioms no_seven_part_9
#print axioms no_seven_part_10
#print axioms no_seven_part_11
#print axioms no_seven_part_12
#print axioms no_seven_part_13

end Delta3.Balanced15

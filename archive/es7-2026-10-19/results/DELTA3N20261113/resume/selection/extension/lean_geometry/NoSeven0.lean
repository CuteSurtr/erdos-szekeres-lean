import FiniteModel

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem no_seven_part_0 :
    (((choose 7 indices).drop 0).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_1 :
    (((choose 7 indices).drop 256).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_2 :
    (((choose 7 indices).drop 512).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_3 :
    (((choose 7 indices).drop 768).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_4 :
    (((choose 7 indices).drop 1024).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_5 :
    (((choose 7 indices).drop 1280).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_6 :
    (((choose 7 indices).drop 1536).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

#print axioms no_seven_part_0
#print axioms no_seven_part_1
#print axioms no_seven_part_2
#print axioms no_seven_part_3
#print axioms no_seven_part_4
#print axioms no_seven_part_5
#print axioms no_seven_part_6

end Delta3.Balanced15

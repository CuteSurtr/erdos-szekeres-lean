import FiniteModel

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem no_seven_part_21 :
    (((choose 7 indices).drop 5376).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_22 :
    (((choose 7 indices).drop 5632).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_23 :
    (((choose 7 indices).drop 5888).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_24 :
    (((choose 7 indices).drop 6144).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

theorem no_seven_part_25 :
    (((choose 7 indices).drop 6400).take 256).all (fun s => !signConvex s) = true := by
  decide +kernel

#print axioms no_seven_part_21
#print axioms no_seven_part_22
#print axioms no_seven_part_23
#print axioms no_seven_part_24
#print axioms no_seven_part_25

end Delta3.Balanced15

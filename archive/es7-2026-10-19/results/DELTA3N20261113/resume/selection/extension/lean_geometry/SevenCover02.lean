import SevenBlock02

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_02 :
    ((choose 7 indices).drop 1024).take 512 = sevenBlock02 := by
  decide +kernel

#print axioms seven_cover_02

end Delta3.Balanced15

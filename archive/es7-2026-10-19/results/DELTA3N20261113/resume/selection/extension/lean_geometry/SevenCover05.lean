import SevenBlock05

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_05 :
    ((choose 7 indices).drop 2560).take 512 = sevenBlock05 := by
  decide +kernel

#print axioms seven_cover_05

end Delta3.Balanced15

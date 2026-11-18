import SevenBlock08

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_08 :
    ((choose 7 indices).drop 4096).take 512 = sevenBlock08 := by
  decide +kernel

#print axioms seven_cover_08

end Delta3.Balanced15

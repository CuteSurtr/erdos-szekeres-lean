import SevenBlock12

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_12 :
    ((choose 7 indices).drop 6144).take 512 = sevenBlock12 := by
  decide +kernel

#print axioms seven_cover_12

end Delta3.Balanced15

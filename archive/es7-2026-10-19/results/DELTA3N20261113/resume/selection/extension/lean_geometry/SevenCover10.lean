import SevenBlock10

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_10 :
    ((choose 7 indices).drop 5120).take 512 = sevenBlock10 := by
  decide +kernel

#print axioms seven_cover_10

end Delta3.Balanced15

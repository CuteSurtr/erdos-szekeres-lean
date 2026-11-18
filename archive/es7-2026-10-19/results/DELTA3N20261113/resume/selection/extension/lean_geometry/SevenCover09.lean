import SevenBlock09

set_option maxRecDepth 32768

namespace Delta3.Balanced15

theorem seven_cover_09 :
    ((choose 7 indices).drop 4608).take 512 = sevenBlock09 := by
  decide +kernel

#print axioms seven_cover_09

end Delta3.Balanced15

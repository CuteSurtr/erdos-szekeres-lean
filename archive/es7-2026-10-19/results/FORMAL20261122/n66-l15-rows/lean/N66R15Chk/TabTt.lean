import N66R15Chk.TabTt0
import N66R15Chk.TabTt1
import N66R15Chk.TabTt2
import N66R15Chk.TabTt3
import N66R15Chk.TabTt4
import N66R15Chk.TabTt5
import N66R15Chk.TabTt6
import N66R15Chk.TabTt7
import N66R15Chk.TabTt8
import N66R15Chk.TabTt9
import N66R15Chk.TabTt10
import N66R15Chk.TabTt11
import N66R15Chk.TabTt12
import N66R15Chk.TabTt13

/-! The table `ttChk` agrees on all 70 rows (generated). -/

namespace N66R15Chk

theorem tt_all : (List.range 70).all ttChk = true := by
  have e : List.range 70 = List.range' 0 1 ++ List.range' 1 1 ++ List.range' 2 1 ++ List.range' 3 1 ++ List.range' 4 1 ++ List.range' 5 1 ++ List.range' 6 1 ++ List.range' 7 1 ++ List.range' 8 1 ++ List.range' 9 1 ++ List.range' 10 1 ++ List.range' 11 1 ++ List.range' 12 1 ++ List.range' 13 1 ++ List.range' 14 1 ++ List.range' 15 1 ++ List.range' 16 1 ++ List.range' 17 1 ++ List.range' 18 1 ++ List.range' 19 1 ++ List.range' 20 1 ++ List.range' 21 1 ++ List.range' 22 1 ++ List.range' 23 1 ++ List.range' 24 1 ++ List.range' 25 1 ++ List.range' 26 1 ++ List.range' 27 1 ++ List.range' 28 1 ++ List.range' 29 1 ++ List.range' 30 1 ++ List.range' 31 1 ++ List.range' 32 1 ++ List.range' 33 1 ++ List.range' 34 1 ++ List.range' 35 1 ++ List.range' 36 1 ++ List.range' 37 1 ++ List.range' 38 1 ++ List.range' 39 1 ++ List.range' 40 1 ++ List.range' 41 1 ++ List.range' 42 1 ++ List.range' 43 1 ++ List.range' 44 1 ++ List.range' 45 1 ++ List.range' 46 1 ++ List.range' 47 1 ++ List.range' 48 1 ++ List.range' 49 1 ++ List.range' 50 1 ++ List.range' 51 1 ++ List.range' 52 1 ++ List.range' 53 1 ++ List.range' 54 1 ++ List.range' 55 1 ++ List.range' 56 1 ++ List.range' 57 1 ++ List.range' 58 1 ++ List.range' 59 1 ++ List.range' 60 1 ++ List.range' 61 1 ++ List.range' 62 1 ++ List.range' 63 1 ++ List.range' 64 1 ++ List.range' 65 1 ++ List.range' 66 1 ++ List.range' 67 1 ++ List.range' 68 1 ++ List.range' 69 1 := by decide
  rw [e]; simp only [List.all_append, tt_0, tt_1, tt_2, tt_3, tt_4, tt_5, tt_6, tt_7, tt_8, tt_9, tt_10, tt_11, tt_12, tt_13, tt_14, tt_15, tt_16, tt_17, tt_18, tt_19, tt_20, tt_21, tt_22, tt_23, tt_24, tt_25, tt_26, tt_27, tt_28, tt_29, tt_30, tt_31, tt_32, tt_33, tt_34, tt_35, tt_36, tt_37, tt_38, tt_39, tt_40, tt_41, tt_42, tt_43, tt_44, tt_45, tt_46, tt_47, tt_48, tt_49, tt_50, tt_51, tt_52, tt_53, tt_54, tt_55, tt_56, tt_57, tt_58, tt_59, tt_60, tt_61, tt_62, tt_63, tt_64, tt_65, tt_66, tt_67, tt_68, tt_69, Bool.and_self]

end N66R15Chk

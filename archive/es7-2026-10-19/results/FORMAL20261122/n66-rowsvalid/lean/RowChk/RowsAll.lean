import RowChk.Rows0
import RowChk.Rows1
import RowChk.Rows2
import RowChk.Rows3
import RowChk.Rows4
import RowChk.Rows5
import RowChk.Rows6
import RowChk.Rows7
import RowChk.Rows8
import RowChk.Rows9
import RowChk.Rows10
import RowChk.Rows11
import RowChk.Rows12
import RowChk.Rows13
import RowChk.Rows14
import RowChk.Rows15
import RowChk.Rows16
import RowChk.Rows17
import RowChk.Rows18
import RowChk.Rows19
import RowChk.Rows20
import RowChk.Rows21
import RowChk.Rows22
import RowChk.Rows23
import RowChk.Rows24
import RowChk.Rows25
import RowChk.Rows26
import RowChk.Rows27
import RowChk.Rows28
import RowChk.Rows29

/-! Generated: R1nat and J as concatenations of the chunks. -/

namespace RowChk

def rowChunks : List (List (List Nat) × List RC) := [(rows0, just0), (rows1, just1), (rows2, just2), (rows3, just3), (rows4, just4), (rows5, just5), (rows6, just6), (rows7, just7), (rows8, just8), (rows9, just9), (rows10, just10), (rows11, just11), (rows12, just12), (rows13, just13), (rows14, just14), (rows15, just15), (rows16, just16), (rows17, just17), (rows18, just18), (rows19, just19), (rows20, just20), (rows21, just21), (rows22, just22), (rows23, just23), (rows24, just24), (rows25, just25), (rows26, just26), (rows27, just27), (rows28, just28), (rows29, just29), (rows30, just30), (rows31, just31), (rows32, just32), (rows33, just33), (rows34, just34), (rows35, just35), (rows36, just36), (rows37, just37), (rows38, just38), (rows39, just39), (rows40, just40), (rows41, just41), (rows42, just42), (rows43, just43), (rows44, just44), (rows45, just45), (rows46, just46), (rows47, just47), (rows48, just48), (rows49, just49), (rows50, just50), (rows51, just51), (rows52, just52), (rows53, just53), (rows54, just54), (rows55, just55), (rows56, just56), (rows57, just57), (rows58, just58), (rows59, just59), (rows60, just60), (rows61, just61), (rows62, just62), (rows63, just63), (rows64, just64), (rows65, just65), (rows66, just66), (rows67, just67), (rows68, just68), (rows69, just69), (rows70, just70), (rows71, just71), (rows72, just72), (rows73, just73), (rows74, just74), (rows75, just75), (rows76, just76), (rows77, just77), (rows78, just78), (rows79, just79), (rows80, just80), (rows81, just81), (rows82, just82), (rows83, just83), (rows84, just84), (rows85, just85), (rows86, just86), (rows87, just87), (rows88, just88), (rows89, just89), (rows90, just90), (rows91, just91), (rows92, just92), (rows93, just93), (rows94, just94), (rows95, just95), (rows96, just96), (rows97, just97), (rows98, just98), (rows99, just99), (rows100, just100), (rows101, just101), (rows102, just102), (rows103, just103), (rows104, just104), (rows105, just105), (rows106, just106), (rows107, just107), (rows108, just108), (rows109, just109), (rows110, just110), (rows111, just111), (rows112, just112), (rows113, just113), (rows114, just114), (rows115, just115), (rows116, just116), (rows117, just117), (rows118, just118)]

def R1nat : List (List Nat) := rowChunks.flatMap Prod.fst

theorem chkAll : ∀ p ∈ rowChunks, chkRows p.1 p.2 = true := by
  intro p hp
  simp only [rowChunks, List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact chk0
  · exact chk1
  · exact chk2
  · exact chk3
  · exact chk4
  · exact chk5
  · exact chk6
  · exact chk7
  · exact chk8
  · exact chk9
  · exact chk10
  · exact chk11
  · exact chk12
  · exact chk13
  · exact chk14
  · exact chk15
  · exact chk16
  · exact chk17
  · exact chk18
  · exact chk19
  · exact chk20
  · exact chk21
  · exact chk22
  · exact chk23
  · exact chk24
  · exact chk25
  · exact chk26
  · exact chk27
  · exact chk28
  · exact chk29
  · exact chk30
  · exact chk31
  · exact chk32
  · exact chk33
  · exact chk34
  · exact chk35
  · exact chk36
  · exact chk37
  · exact chk38
  · exact chk39
  · exact chk40
  · exact chk41
  · exact chk42
  · exact chk43
  · exact chk44
  · exact chk45
  · exact chk46
  · exact chk47
  · exact chk48
  · exact chk49
  · exact chk50
  · exact chk51
  · exact chk52
  · exact chk53
  · exact chk54
  · exact chk55
  · exact chk56
  · exact chk57
  · exact chk58
  · exact chk59
  · exact chk60
  · exact chk61
  · exact chk62
  · exact chk63
  · exact chk64
  · exact chk65
  · exact chk66
  · exact chk67
  · exact chk68
  · exact chk69
  · exact chk70
  · exact chk71
  · exact chk72
  · exact chk73
  · exact chk74
  · exact chk75
  · exact chk76
  · exact chk77
  · exact chk78
  · exact chk79
  · exact chk80
  · exact chk81
  · exact chk82
  · exact chk83
  · exact chk84
  · exact chk85
  · exact chk86
  · exact chk87
  · exact chk88
  · exact chk89
  · exact chk90
  · exact chk91
  · exact chk92
  · exact chk93
  · exact chk94
  · exact chk95
  · exact chk96
  · exact chk97
  · exact chk98
  · exact chk99
  · exact chk100
  · exact chk101
  · exact chk102
  · exact chk103
  · exact chk104
  · exact chk105
  · exact chk106
  · exact chk107
  · exact chk108
  · exact chk109
  · exact chk110
  · exact chk111
  · exact chk112
  · exact chk113
  · exact chk114
  · exact chk115
  · exact chk116
  · exact chk117
  · exact chk118

end RowChk

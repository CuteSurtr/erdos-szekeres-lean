import N66R15Enc.RowsD0
import N66R15Enc.RowsD1
import N66R15Enc.RowsD2
import N66R15Enc.RowsD3
import N66R15Enc.RowsD4
import N66R15Enc.RowsD5
import N66R15Enc.RowsD6
import N66R15Enc.RowsD7
import N66R15Enc.RowsD8
import N66R15Enc.RowsD9
import N66R15Enc.RowsD10
import N66R15Enc.RowsD11
import N66R15Enc.RowsD12
import N66R15Enc.RowsD13
import N66R15Enc.RowsD14
import N66R15Enc.RowsD15
import N66R15Enc.RowsD16
import N66R15Enc.RowsD17
import N66R15Enc.RowsD18
import N66R15Enc.RowsD19
import N66R15Enc.RowsD20
import N66R15Enc.RowsD21
import N66R15Enc.RowsD22
import N66R15Enc.RowsD23
import N66R15Enc.RowsD24
import N66R15Enc.RowsD25
import N66R15Enc.RowsD26
import N66R15Enc.RowsD27

/-!
# N66R15Enc.RowList: the level-15 row list from the kernel-checked chunk constants (Std-only; generated)

`R1nat15` is the concatenation of the chunk constants `rows<k>` that `N66R15Chk.Rows*` check with `decide +kernel`,
in the order of n66-level15's `rows_used15.txt` (10,859 rows). `R1_15` is the row list of the cube printer
(`N66R15Enc.Print`) and of the theorem (`CubesUnsat105R`, `RowsValid R1_15`): no parsed text, nothing the kernel
cannot evaluate.
-/

namespace N66R15Enc

def rowsAll : List (List (List Nat)) := [rows0, rows1, rows2, rows3, rows4, rows5, rows6, rows7, rows8, rows9, rows10, rows11, rows12, rows13, rows14, rows15, rows16, rows17, rows18, rows19, rows20, rows21, rows22, rows23, rows24, rows25, rows26, rows27, rows28, rows29, rows30, rows31, rows32, rows33, rows34, rows35, rows36, rows37, rows38, rows39, rows40, rows41, rows42, rows43, rows44, rows45, rows46, rows47, rows48, rows49, rows50, rows51, rows52, rows53, rows54, rows55, rows56, rows57, rows58, rows59, rows60, rows61, rows62, rows63, rows64, rows65, rows66, rows67, rows68, rows69, rows70, rows71, rows72, rows73, rows74, rows75, rows76, rows77, rows78, rows79, rows80, rows81, rows82, rows83, rows84, rows85, rows86, rows87, rows88, rows89, rows90, rows91, rows92, rows93, rows94, rows95, rows96, rows97, rows98, rows99, rows100, rows101, rows102, rows103, rows104, rows105, rows106, rows107, rows108]

def R1nat15 : List (List Nat) := rowsAll.flatten

/-- A state number as a state (`x % 70`; every row entry is below 70, checked by `chkRows`). -/
def toFin70 (x : Nat) : Fin 70 := ⟨x % 70, Nat.mod_lt _ (by decide)⟩

/-- **The level-15 row list** (10,859 supports). -/
def R1_15 : List (List (Fin 70)) := R1nat15.map (·.map toFin70)

end N66R15Enc

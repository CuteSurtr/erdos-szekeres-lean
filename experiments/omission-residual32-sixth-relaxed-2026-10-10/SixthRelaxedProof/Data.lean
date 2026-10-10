import SixthRelaxedTemplateGeometry
import SixthRelaxedTemplateCheck

namespace ErdosSzekeres.Omission.CoupledSixthRelaxedVariants
open CoupledTemplateSixthRelaxed
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def state000 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 12, 26, 23, 17, 36, 64, 33, 34, 54]
def state001 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 12, 36, 23, 17, 49, 64, 33, 34, 54]
def state002 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 26, 36, 23, 17, 49, 64, 33, 34, 54]
def state003 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 12, 26, 23, 17, 49, 64, 33, 34, 54]
def state004 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 12, 26, 23, 17, 36, 49, 33, 34, 54]
def state005 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 12, 18, 23, 17, 27, 39, 33, 34, 44]
def state006 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 12, 18, 23, 17, 39, 53, 33, 34, 44]
def state007 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 12, 27, 23, 17, 39, 53, 33, 34, 44]
def state008 : Fin 13 → Fin 154 := ![1, 4, 8, 14, 12, 18, 23, 17, 27, 53, 33, 34, 44]
def state009 : Fin 13 → Fin 154 := ![2, 4, 8, 14, 12, 26, 23, 25, 36, 64, 33, 34, 54]
def state010 : Fin 13 → Fin 154 := ![2, 4, 8, 14, 12, 36, 23, 25, 49, 64, 33, 34, 54]
def state011 : Fin 13 → Fin 154 := ![2, 4, 8, 14, 12, 26, 23, 25, 49, 64, 33, 34, 54]
def state012 : Fin 13 → Fin 154 := ![2, 4, 8, 14, 12, 26, 23, 25, 36, 49, 33, 34, 54]
def state013 : Fin 13 → Fin 154 := ![2, 4, 8, 14, 12, 18, 23, 25, 27, 39, 33, 34, 44]
def state014 : Fin 13 → Fin 154 := ![2, 4, 8, 14, 12, 18, 23, 25, 39, 53, 33, 34, 44]
def state015 : Fin 13 → Fin 154 := ![2, 4, 8, 14, 12, 27, 23, 25, 39, 53, 33, 34, 44]
def state016 : Fin 13 → Fin 154 := ![2, 4, 8, 14, 12, 18, 23, 25, 27, 53, 33, 34, 44]
def state017 : Fin 13 → Fin 154 := ![25, 43, 53, 65, 39, 49, 77, 68, 60, 72, 89, 90, 99]
def state018 : Fin 13 → Fin 154 := ![33, 43, 53, 65, 39, 49, 77, 79, 60, 72, 89, 90, 99]
def state019 : Fin 13 → Fin 154 := ![25, 43, 53, 65, 39, 59, 77, 68, 70, 82, 89, 90, 107]
def state020 : Fin 13 → Fin 154 := ![33, 43, 53, 65, 39, 59, 77, 79, 70, 82, 89, 90, 107]
def state021 : Fin 13 → Fin 154 := ![34, 53, 64, 75, 49, 59, 87, 68, 81, 93, 99, 100, 115]
def state022 : Fin 13 → Fin 154 := ![44, 53, 64, 75, 49, 59, 87, 79, 81, 93, 99, 100, 115]
def state023 : Fin 13 → Fin 154 := ![25, 43, 53, 65, 74, 85, 77, 91, 96, 107, 110, 111, 125]
def state024 : Fin 13 → Fin 154 := ![25, 43, 53, 77, 74, 85, 89, 91, 96, 107, 110, 111, 125]
def state025 : Fin 13 → Fin 154 := ![34, 53, 65, 77, 85, 95, 89, 91, 105, 115, 110, 119, 131]
def state026 : Fin 13 → Fin 154 := ![3, 8, 13, 21, 18, 26, 31, 17, 47, 60, 44, 45, 66]
def state027 : Fin 13 → Fin 154 := ![3, 8, 13, 21, 18, 26, 31, 17, 60, 75, 44, 45, 66]
def state028 : Fin 13 → Fin 154 := ![3, 8, 13, 21, 18, 47, 31, 17, 60, 75, 44, 45, 66]
def state029 : Fin 13 → Fin 154 := ![3, 8, 13, 21, 26, 47, 31, 17, 60, 75, 44, 45, 66]
def state030 : Fin 13 → Fin 154 := ![3, 8, 13, 21, 18, 26, 31, 17, 47, 75, 44, 45, 66]
def state031 : Fin 13 → Fin 154 := ![5, 8, 13, 21, 18, 26, 31, 25, 47, 60, 44, 45, 66]
def state032 : Fin 13 → Fin 154 := ![5, 8, 13, 21, 18, 26, 31, 25, 60, 75, 44, 45, 66]
def state033 : Fin 13 → Fin 154 := ![5, 8, 13, 21, 18, 47, 31, 25, 60, 75, 44, 45, 66]
def state034 : Fin 13 → Fin 154 := ![5, 8, 13, 21, 18, 26, 31, 25, 47, 75, 44, 45, 66]
def state035 : Fin 13 → Fin 154 := ![34, 53, 64, 75, 74, 95, 87, 91, 105, 115, 118, 119, 131]
def state036 : Fin 13 → Fin 154 := ![34, 53, 64, 75, 74, 95, 99, 91, 105, 115, 118, 119, 131]
def state037 : Fin 13 → Fin 154 := ![34, 53, 64, 87, 74, 95, 99, 91, 105, 115, 118, 119, 131]
def state038 : Fin 13 → Fin 154 := ![34, 53, 75, 87, 85, 95, 99, 91, 105, 115, 118, 119, 131]
def state039 : Fin 13 → Fin 154 := ![34, 64, 75, 87, 85, 95, 99, 91, 105, 115, 118, 119, 131]
def state040 : Fin 13 → Fin 154 := ![53, 64, 75, 87, 85, 95, 99, 91, 105, 115, 118, 119, 131]
def state041 : Fin 13 → Fin 154 := ![45, 65, 75, 87, 85, 95, 99, 91, 105, 115, 118, 119, 131]
def state042 : Fin 13 → Fin 154 := ![53, 64, 75, 87, 85, 95, 99, 101, 105, 115, 118, 119, 131]
def state043 : Fin 13 → Fin 154 := ![44, 64, 75, 87, 85, 95, 99, 101, 105, 115, 118, 119, 131]
def state044 : Fin 13 → Fin 154 := ![34, 64, 75, 87, 85, 104, 99, 91, 113, 122, 118, 119, 136]
def state045 : Fin 13 → Fin 154 := ![53, 64, 75, 87, 85, 104, 99, 91, 113, 122, 118, 119, 136]
def state046 : Fin 13 → Fin 154 := ![53, 64, 75, 87, 85, 104, 99, 101, 113, 122, 118, 119, 136]
def state047 : Fin 13 → Fin 154 := ![44, 64, 75, 87, 85, 104, 99, 101, 113, 122, 118, 119, 136]

def maps : Fin 48 → Fin 13 → Fin 154 := ![state000, state001, state002, state003, state004, state005, state006, state007, state008, state009, state010, state011, state012, state013, state014, state015, state016, state017, state018, state019, state020, state021, state022, state023, state024, state025, state026, state027, state028, state029, state030, state031, state032, state033, state034, state035, state036, state037, state038, state039, state040, state041, state042, state043, state044, state045, state046, state047]

def support (r : Fin 48) : Finset (Fin 154) := Finset.univ.image (maps r)

end ErdosSzekeres.Omission.CoupledSixthRelaxedVariants

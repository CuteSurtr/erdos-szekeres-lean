/- Negative control (must NOT compile): Lo pinned to a wrong index list (120 replaced by 121). -/
import Res118.LemmaA
namespace Res118Ctl
open Res118
def badLo : List ℕ := [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 26,
  27, 28, 29, 30, 31, 32, 35, 36, 37, 38, 39, 40, 41, 42, 46, 47, 48, 49, 50, 51, 52, 57, 58, 59, 60, 61, 62, 63, 69,
  70, 71, 72, 73, 80, 81, 82, 83, 84, 92, 93, 94, 102, 103, 112, 121]
theorem Lo_eq_bad : ∀ i : Fin 154, i ∈ Lo ↔ i.val ∈ badLo := by
  unfold Lo InLo; simp only [Finset.mem_filter, Finset.mem_univ, true_and]; decide +kernel
end Res118Ctl

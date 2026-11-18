import T12FiniteFacts
import T12SixAggregate

namespace Delta3.Terminal12

/-- The enumerator contains every subsequence of the requested length. -/
theorem mem_choose_of_sublist {α : Type} {xs ys : List α} (h : xs.Sublist ys) :
    xs ∈ choose xs.length ys := by
  induction h with
  | slnil => exact .head []
  | @cons xs ys a h ih =>
    cases xs with
    | nil => exact .head []
    | cons b bs => exact List.mem_append_right _ ih
  | cons₂ a h ih => exact List.mem_append_left _ (List.mem_map_of_mem ih)

/-- Every five-point subsequence of the ordered fixture fails the cap test. -/
theorem five_subsequence_not_cap (s : List Index) (hs : s.Sublist indices)
    (hlen : s.length = 5) : cap s = false := by
  have hm : s ∈ choose 5 indices := by
    simpa only [hlen] using mem_choose_of_sublist hs
  have h := List.all_eq_true.mp no_five_cap s hm
  simpa only [Bool.not_eq_true'] using h

/-- Every six-point subsequence fails the all-four-point orientation criterion. -/
theorem six_subsequence_not_signConvex (s : List Index) (hs : s.Sublist indices)
    (hlen : s.length = 6) : signConvex s = false := by
  have hm : s ∈ choose 6 indices := by
    simpa only [hlen] using mem_choose_of_sublist hs
  have h := List.all_eq_true.mp no_six_sign_convex s hm
  simpa only [Bool.not_eq_true'] using h

#print axioms mem_choose_of_sublist
#print axioms five_subsequence_not_cap
#print axioms six_subsequence_not_signConvex

end Delta3.Terminal12

import T12SixCover00
import T12SixCover01
import T12Determinants

namespace Delta3.Terminal12

theorem all_of_take_drop {α : Type} (xs : List α) (p : α → Bool) (start size : Nat)
    (hb : ((xs.drop start).take size).all p = true)
    (ht : (xs.drop (start + size)).all p = true) : (xs.drop start).all p = true := by
  have h := (congrArg (fun ys => ys.all p) (List.take_append_drop size (xs.drop start))).symm
  rw [List.all_append, List.drop_drop, hb, ht] at h
  exact h

theorem no_six_sign_convex : (choose 6 indices).all (fun s => !signConvex s) = true := by
  have he : (choose 6 indices).drop 1024 = [] :=
    List.drop_eq_nil_iff.mpr (by rw [six_count]; decide)
  have h2 : ((choose 6 indices).drop 1024).all (fun s => !signConvex s) = true := by
    rw [he]
    rfl
  have h1 : ((choose 6 indices).drop 512).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 6 indices) (fun s => !signConvex s) 512 512
      (by rw [six_cover_01]; exact no_six_block_01) h2
  have h0 : ((choose 6 indices).drop 0).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 6 indices) (fun s => !signConvex s) 0 512
      (by rw [six_cover_00]; exact no_six_block_00) h1
  exact h0

#print axioms all_of_take_drop
#print axioms no_six_sign_convex

end Delta3.Terminal12

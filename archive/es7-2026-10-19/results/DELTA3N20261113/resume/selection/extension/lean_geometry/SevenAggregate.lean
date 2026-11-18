import SevenCover00
import SevenCover01
import SevenCover02
import SevenCover03
import SevenCover04
import SevenCover05
import SevenCover06
import SevenCover07
import SevenCover08
import SevenCover09
import SevenCover10
import SevenCover11
import SevenCover12
import Determinants

namespace Delta3.Balanced15

theorem all_of_take_drop {α : Type} (xs : List α) (p : α → Bool) (start size : Nat)
    (hb : ((xs.drop start).take size).all p = true)
    (ht : (xs.drop (start + size)).all p = true) : (xs.drop start).all p = true := by
  have h := (congrArg (fun ys => ys.all p) (List.take_append_drop size (xs.drop start))).symm
  rw [List.all_append, List.drop_drop, hb, ht] at h
  exact h

theorem no_seven_sign_convex : (choose 7 indices).all (fun s => !signConvex s) = true := by
  have he : (choose 7 indices).drop 6656 = [] :=
    List.drop_eq_nil_iff.mpr (by rw [seven_count]; decide)
  have h13 : ((choose 7 indices).drop 6656).all (fun s => !signConvex s) = true := by
    rw [he]
    rfl
  have h12 : ((choose 7 indices).drop 6144).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 6144 512
      (by rw [seven_cover_12]; exact no_seven_block_12) h13
  have h11 : ((choose 7 indices).drop 5632).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 5632 512
      (by rw [seven_cover_11]; exact no_seven_block_11) h12
  have h10 : ((choose 7 indices).drop 5120).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 5120 512
      (by rw [seven_cover_10]; exact no_seven_block_10) h11
  have h9 : ((choose 7 indices).drop 4608).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 4608 512
      (by rw [seven_cover_09]; exact no_seven_block_09) h10
  have h8 : ((choose 7 indices).drop 4096).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 4096 512
      (by rw [seven_cover_08]; exact no_seven_block_08) h9
  have h7 : ((choose 7 indices).drop 3584).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 3584 512
      (by rw [seven_cover_07]; exact no_seven_block_07) h8
  have h6 : ((choose 7 indices).drop 3072).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 3072 512
      (by rw [seven_cover_06]; exact no_seven_block_06) h7
  have h5 : ((choose 7 indices).drop 2560).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 2560 512
      (by rw [seven_cover_05]; exact no_seven_block_05) h6
  have h4 : ((choose 7 indices).drop 2048).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 2048 512
      (by rw [seven_cover_04]; exact no_seven_block_04) h5
  have h3 : ((choose 7 indices).drop 1536).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 1536 512
      (by rw [seven_cover_03]; exact no_seven_block_03) h4
  have h2 : ((choose 7 indices).drop 1024).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 1024 512
      (by rw [seven_cover_02]; exact no_seven_block_02) h3
  have h1 : ((choose 7 indices).drop 512).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 512 512
      (by rw [seven_cover_01]; exact no_seven_block_01) h2
  have h0 : ((choose 7 indices).drop 0).all (fun s => !signConvex s) = true :=
    all_of_take_drop (choose 7 indices) (fun s => !signConvex s) 0 512
      (by rw [seven_cover_00]; exact no_seven_block_00) h1
  exact h0

#print axioms all_of_take_drop
#print axioms no_seven_sign_convex

end Delta3.Balanced15

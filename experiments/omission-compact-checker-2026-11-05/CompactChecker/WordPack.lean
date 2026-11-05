import CompactChecker.Fast

/-! Several leaf entries per natural-number word (`k` digits in base `J`).
This is only a data encoding: the leaf of a `PTree` is written
`.leaf cap (expandW J k [w₀, w₁, …])`, and `checkF` evaluates `expandW`;
soundness is unchanged because `checkF_sound` holds for every entry list. -/

namespace CompactChecker

noncomputable section

/-- Prepend the `k` base-`J` digits of `x` (least significant first) to `acc`. -/
def pushDigits (J k x : ℕ) (acc : List ℕ) : List ℕ :=
  Nat.rec (motive := fun _ => ℕ → List ℕ) (fun _ => acc)
    (fun _ ih y => y % J :: ih (y / J)) k x

def expandW (J k : ℕ) (ws : List ℕ) : List ℕ :=
  List.rec (motive := fun _ => List ℕ) [] (fun w _ acc => pushDigits J k w acc) ws

end

end CompactChecker

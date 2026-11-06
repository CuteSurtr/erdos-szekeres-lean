import Start.Rules

/-! Judge check (evidence only, `#eval`): the conclusions of U5's sort lemma (`SortedSix`) and of `WordSpec` on
every ordered triple of distinct labels, for several ψ orders, m ∈ {2,4,6,8}, t = 4. -/

open EncB EncB.Rules

def psiOf (perm : List Nat) (i j : Nat) : Bool := decide (perm.idxOf i < perm.idxOf j)

def sortedSixB (m : Nat) (psiLt : Nat → Nat → Bool) (a b d : Pt) (S : List Obj) : Bool :=
  S.length == 6 &&
  decide (S.Pairwise fun o o' => objLt m psiLt (objImg [a, b, d] o) (objImg [a, b, d] o')) &&
  (objs6 a b d).all (fun x => (S.map (objImg [a, b, d])).contains x) &&
  S.all (fun o => decide (o.idx < 3)) &&
  ((S.filter (·.kind == 1)).map (·.idx)).isPerm [0, 1, 2]

def check (m t : Nat) (perm : List Nat) : Nat × Nat × Nat × Nat :=
  let psiLt := psiOf perm
  let rk : Nat → Nat := fun L => perm.idxOf L
  let labs := labels m t
  let trip := labs.flatMap fun a => labs.flatMap fun b => labs.filterMap fun d =>
    if a != b && a != d && b != d then some (a, b, d) else none
  trip.foldl (fun (acc : Nat × Nat × Nat × Nat) abd =>
    let (a, b, d) := abd
    let objs := objsEven m rk [a, b, d]
    if (pairs (objs.map fun o => (o.J, o.r))).any (fun kk => kk.1 == kk.2) then acc
    else
      let S := insSort Obj.lt objs
      let ss := sortedSixB m psiLt a b d S
      let kinds := S.map (·.kind)
      let seq := (S.filter (·.kind == 1)).map (·.idx)
      let alt := kinds == [1, 0, 1, 0, 1, 0] || kinds == [0, 1, 0, 1, 0, 1]
      let altOk := !alt || decide (AltCCW m psiLt ([a, b, d].getD (seq.getD 0 0) (0, 0))
        ([a, b, d].getD (seq.getD 1 0) (0, 0)) ([a, b, d].getD (seq.getD 2 0) (0, 0)))
      let blkOk := (List.range 6).all fun st =>
        !(kinds.getD (st % 6) 0 == 1 && kinds.getD ((st + 1) % 6) 0 == 1 && kinds.getD ((st + 2) % 6) 0 == 1) ||
        decide (BlockCCW m psiLt ([a, b, d].getD (S.getD (st % 6) default).idx (0, 0))
          ([a, b, d].getD (S.getD ((st + 1) % 6) default).idx (0, 0))
          ([a, b, d].getD (S.getD ((st + 2) % 6) default).idx (0, 0)))
      let nblk := ((List.range 6).filter fun st =>
        kinds.getD (st % 6) 0 == 1 && kinds.getD ((st + 1) % 6) 0 == 1 && kinds.getD ((st + 2) % 6) 0 == 1).length
      (acc.1 + 1, acc.2.1 + (if ss && altOk && blkOk then 0 else 1), acc.2.2.1 + (if alt then 1 else 0),
        acc.2.2.2 + (if nblk > 0 then 1 else 0)))
    (0, 0, 0, 0)

-- (triples with distinct keys, violations, alternating, with a PPP run)
#eval [2, 4, 6, 8].flatMap fun m => [[0, 1, 2, 3], [0, 3, 1, 2], [0, 2, 3, 1], [0, 3, 2, 1]].map fun p =>
  (m, p, check m 4 p)

import V182Chk.WalkDefs

/-!
# V182Ctl.WalkMut: negative control for the six-colouring check (not imported by the theorem modules)

The walk check of `V182Chk.WalkDefs` with the table as a parameter: on `col6Big` it passes at the start masks 14 and
15; with edge 0 (4-set mask 15, bit 0; colour 5) recoloured to 0 (`col6Big ^^^ (5 <<< 360)`) it fails at both, so
the kernel check can detect a non-rainbow colouring.
-/

namespace V182Ctl
open V182Geo

def col6AtT (B m m' : Nat) : Nat :=
  ((B >>> (3 * (8 * (if popT (m ||| m') = 4 then m ||| m' else m &&& m') + popT ((m ^^^ m') - 1)))) % 8) % 6

def rainbow4T (B a b c d : Nat) : Bool := decide ([col6AtT B a b, col6AtT B b c, col6AtT B c d, col6AtT B d a].Nodup)

def walkBodyT (B a : Nat) : Bool :=
  !isV a || (List.range 8).all fun i => (List.range 8).all fun j => (List.range 8).all fun k =>
    !(isV (a ^^^ 1 <<< i) && isV (a ^^^ 1 <<< i ^^^ 1 <<< j) && isV (a ^^^ 1 <<< i ^^^ 1 <<< j ^^^ 1 <<< k) &&
        (a != a ^^^ 1 <<< i ^^^ 1 <<< j) && (a ^^^ 1 <<< i != a ^^^ 1 <<< i ^^^ 1 <<< j ^^^ 1 <<< k) &&
        onebit (a ^^^ 1 <<< i ^^^ 1 <<< j ^^^ 1 <<< k ^^^ a)) ||
      rainbow4T B a (a ^^^ 1 <<< i) (a ^^^ 1 <<< i ^^^ 1 <<< j) (a ^^^ 1 <<< i ^^^ 1 <<< j ^^^ 1 <<< k)

theorem walkBodyT_eq (a : Nat) : walkBodyT col6Big a = walkBody a := rfl

theorem ctl_orig : walkBodyT col6Big 14 = true ∧ walkBodyT col6Big 15 = true := by decide +kernel
theorem ctl_mut : walkBodyT (col6Big ^^^ (5 <<< 360)) 14 = false ∧ walkBodyT (col6Big ^^^ (5 <<< 360)) 15 = false := by
  decide +kernel

end V182Ctl

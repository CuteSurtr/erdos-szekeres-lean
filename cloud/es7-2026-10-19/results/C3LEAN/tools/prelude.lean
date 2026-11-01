namespace C3Cover

/-! ## The split (mirrors `results/C3U2/tools/hullcase.py`) -/

/-- Number of rotation orbits (residues `0 … 10`); the set has `3 m = 33` points. -/
def m : Nat := 11

/-- A layer token `(r, s)`: residue `r < 11` and its σ value `s = 0` or `1`; `s = 2` stands for Python's `None`
(a one-orbit layer below the top carries no σ). -/
abbrev Tok := Nat × Nat

/-- A convex layer: one token (one orbit) or two tokens (two orbits), as in `hullcase.py`. -/
abbrev Layer := List Tok

/-- A node of the case split: its convex layers, top layer first, and its σ cube `C` (pairs `(r, v)`, sorted by
residue; empty for a plain layer node). Name in the records: `hullcase.node_name(layers, C)`. -/
structure Node where
  layers : List Layer
  cube : List (Nat × Nat)
  deriving DecidableEq, Repr

/-- Residues used by the layers of a node. -/
def Node.used (n : Node) : List Nat := n.layers.flatMap fun L => L.map Prod.fst

/-- The two-orbit layers on a list of residues: pairs `b < c` in order, then `σ_b`, then `σ_c`. -/
def pairOptions : List Nat → List Layer
  | [] => []
  | b :: rest =>
    (rest.flatMap fun c => [[(b, 0), (c, 0)], [(b, 0), (c, 1)], [(b, 1), (c, 0)], [(b, 1), (c, 1)]]) ++ pairOptions rest

/-- `hullcase.layer2_options`: every one-orbit layer, then every two-orbit layer with both σ values of both residues,
on the residues not in `used`. -/
def layerOptions (used : List Nat) : List Layer :=
  let rem := (List.range m).filter fun r => !used.contains r
  rem.map (fun r => [(r, 2)]) ++ pairOptions rem

/-- Insert a pair into a list sorted by first component. -/
def insTok (t : Tok) : List Tok → List Tok
  | [] => [t]
  | u :: us => if t.1 ≤ u.1 then t :: u :: us else u :: insTok t us

/-- Sort by residue (Python `sorted` on tokens with distinct residues). -/
def sortTok : List Tok → List Tok
  | [] => []
  | t :: ts => insTok t (sortTok ts)

/-- The 11 top cases (`hullcase.cases`): `H3` = layer `0s0`, then `H6(a, s)` = layer `0s0-a s` for `a = 1 … 5`,
`s = 0, 1`. -/
def topCases : List Layer :=
  [(0, 0)] :: ((List.range 5).flatMap fun i => [[(0, 0), (i + 1, 0)], [(0, 0), (i + 1, 1)]])

/-- `key(O)` of `hullcase.h3_layer2_kept`: tokens sorted by residue, `(r, σ)` with `None` as `-1`, here coded
`3 r + (σ + 1)` (so lexicographic order on the codes is Python's tuple order). -/
def okey (L : Layer) : List Nat := (sortTok L).map fun t => 3 * t.1 + (if t.2 = 2 then 0 else t.2 + 1)

/-- Python's `<=` on tuples. -/
def lexLe : List Nat → List Nat → Bool
  | [], _ => true
  | _ :: _, [] => false
  | a :: as, b :: bs => a < b || (a == b && lexLe as bs)

/-- Lemma 5 (`hullcase.mirror_layer`): `(r, σ) ↦ ((m - r) mod m, 1 - σ)`. -/
def mirror (L : Layer) : Layer := sortTok (L.map fun t => ((m - t.1) % m, if t.2 = 2 then 2 else 1 - t.2))

/-- Lemma H6M (`hullcase.h6_phi`): `(r, σ) ↦ ((a - r) mod m, σ xor [r < a] xor [s = 0])` (σ is flipped exactly
when `[r < a] ≠ [s = 0]`). -/
def phi (a s : Nat) (L : Layer) : Layer :=
  sortTok (L.map fun t => ((a + m - t.1) % m,
    if t.2 = 2 then 2 else if (decide (t.1 < a) != decide (s = 0)) then 1 - t.2 else t.2))

/-- The reflection used below a top case: Lemma 5's `mirror` below `H3` (layer `0s0`), Lemma H6M's `φ_{a,s}` below
`H6(a, s)` (layer `0s0-a s`); the identity otherwise (no such top case exists). -/
def refl (top : Layer) (o : Layer) : Layer :=
  match top with
  | [(0, 0)] => mirror o
  | [(0, 0), (a, s)] => phi a s o
  | _ => o

/-- The kept second layers below a top case (`hullcase.h3_layer2_kept`, `hullcase.h6_layer2_kept`, i.e.
`tree_children` with `mirror = True, mirror_h6 = True`): the options `O` with `key(O) ≤ key(refl O)`. -/
def keptOptions (top : Layer) : List Layer :=
  (layerOptions (top.map Prod.fst)).filter fun o => lexLe (okey o) (okey (refl top o))

/-- The depth-2 roots of the reduced cut, in `hullcase.tree_children` order. -/
def roots : List Node := topCases.flatMap fun t => (keptOptions t).map fun o => ⟨[t, o], []⟩

/-- `hullcase.free_residues`: residues `1 … 10` in no layer and not in the cube, ascending. -/
def Node.free (n : Node) : List Nat :=
  (List.range m).filter fun r => r != 0 && !n.used.contains r && !(n.cube.map Prod.fst).contains r

/-- The `K` bits of `i`, most significant first (Python `[(i >> (K - 1 - j)) & 1 for j in range(K)]`). -/
def bitsOf (K i : Nat) : List Nat := (List.range K).map fun j => i / 2 ^ (K - 1 - j) % 2

/-- Add the pairs `(r, v)` to a cube sorted by residue, keeping it sorted. -/
def addBits (C : List (Nat × Nat)) (new : List (Nat × Nat)) : List (Nat × Nat) := new.foldl (fun c t => insTok t c) C

/-- `hullcase.sigma_children`: the `2 ^ K` cube children on the `K` smallest free residues `b₀ < … < b_{K-1}`;
child `i` (`0 ≤ i < 2 ^ K`) sets `σ_{b_j}` to bit `K - 1 - j` of `i`; the cube stays sorted by residue. -/
def Node.sigmaChildren (n : Node) (K : Nat) : List Node :=
  let bits := n.free.take K
  (List.range (2 ^ K)).map fun i => ⟨n.layers, addBits n.cube (bits.zip (bitsOf K i))⟩

/-- `hullcase.conflicts`: the layer gives a residue of the cube an explicit σ different from the cube's value. -/
def conflicts (L : Layer) (C : List (Nat × Nat)) : Bool :=
  L.any fun t => t.2 != 2 && C.any fun c => c.1 == t.1 && c.2 != t.2

/-- `hullcase.cube_layer_children` (= `tree_children` for a plain node) below depth 1, where nothing is reduced:
every next layer on the unused residues that does not contradict the cube. -/
def Node.layerChildren (n : Node) : List Node :=
  ((layerOptions n.used).filter fun o => !conflicts o n.cube).map fun o => ⟨n.layers ++ [o], n.cube⟩

/-! ## Covered nodes -/

/-- The cover rules of `results/C3U2/tools/compose.py` (`covered2`), for nodes of depth `≥ 2`: `S` is the set of
nodes with a certified, hash-matched record. A node is covered if it is in `S`; or by a layer split (it has at least
one layer child and all of them are covered); or by a σ-split on its `K ≥ 1` smallest free residues (all `2 ^ K`
cube children covered). -/
inductive Covered (S : Node → Prop) : Node → Prop
  | cert {n : Node} : S n → Covered S n
  | layer {n : Node} : 2 ≤ n.layers.length → n.layerChildren ≠ [] →
      (∀ c ∈ n.layerChildren, Covered S c) → Covered S n
  | sigma {n : Node} (K : Nat) : 2 ≤ n.layers.length → 0 < K → K ≤ n.free.length →
      (∀ c ∈ n.sigmaChildren K, Covered S c) → Covered S n

theorem Covered.mono {S T : Node → Prop} (hST : ∀ n, S n → T n) {n : Node} (h : Covered S n) : Covered T n := by
  induction h with
  | cert hs => exact .cert (hST _ hs)
  | layer h2 hne _ ih => exact .layer h2 hne ih
  | sigma K h2 hK hf _ ih => exact .sigma K h2 hK hf ih

/-! ## Node keys

A certified node is named in the data by a key: layer codes in base `2048` (first layer most significant), then the
cube as an 11-bit residue mask and an 11-bit value mask. Token `(r, s)` has code `3 r + s`; a layer has code
`1 + t` (one token `t`) or `34 + 33 t₁ + t₂` (two tokens). -/

def decodeTok (t : Nat) : Tok := (t / 3, t % 3)

def decodeLayer (c : Nat) : Layer :=
  match Nat.ble c 33 with
  | true => [decodeTok (c - 1)]
  | false => [decodeTok ((c - 34) / 33), decodeTok ((c - 34) % 33)]

def decodeLayers : Nat → Nat → List Layer → List Layer
  | 0, _, acc => acc
  | f + 1, lk, acc =>
    match Nat.beq lk 0 with
    | true => acc
    | false => decodeLayers f (lk / 2048) (decodeLayer (lk % 2048) :: acc)

/-- Cube pairs `(r, v)` for the set bits `r` of `cm` (starting at residue `r`), `v` = bit `r` of `cv`. -/
def decodeCube : Nat → Nat → Nat → Nat → List (Nat × Nat)
  | 0, _, _, _ => []
  | f + 1, r, cm, cv =>
    match Nat.beq cm 0 with
    | true => []
    | false =>
      match Nat.beq (cm % 2) 1 with
      | true => (r, cv % 2) :: decodeCube f (r + 1) (cm / 2) (cv / 2)
      | false => decodeCube f (r + 1) (cm / 2) (cv / 2)

/-- The node named by a key. -/
def decodeKey (k : Nat) : Node := ⟨decodeLayers 12 (k / 4194304) [], decodeCube 11 0 (k / 2048 % 2048) (k % 2048)⟩

/-- Boolean equality of lists. -/
def beqList {α : Type} (eq : α → α → Bool) : List α → List α → Bool
  | [], [] => true
  | a :: as, b :: bs => eq a b && beqList eq as bs
  | _, _ => false

def beqTok (a b : Tok) : Bool := Nat.beq a.1 b.1 && Nat.beq a.2 b.2

/-- Boolean equality of nodes. -/
def beqNode (a b : Node) : Bool := beqList (beqList beqTok) a.layers b.layers && beqList beqTok a.cube b.cube

theorem beqList_eq {α : Type} {eq : α → α → Bool} (h : ∀ a b, eq a b = true → a = b) :
    ∀ (l₁ l₂ : List α), beqList eq l₁ l₂ = true → l₁ = l₂
  | [], [], _ => rfl
  | a :: as, b :: bs, hab => by
    simp only [beqList, Bool.and_eq_true] at hab
    rw [h a b hab.1, beqList_eq h as bs hab.2]
  | [], _ :: _, hab => by simp [beqList] at hab
  | _ :: _, [], hab => by simp [beqList] at hab

theorem beqTok_eq : ∀ (a b : Tok), beqTok a b = true → a = b := by
  intro ⟨a1, a2⟩ ⟨b1, b2⟩ h
  simp only [beqTok, Bool.and_eq_true] at h
  rw [Nat.eq_of_beq_eq_true h.1, Nat.eq_of_beq_eq_true h.2]

theorem beqNode_eq {a b : Node} (h : beqNode a b = true) : a = b := by
  cases a; cases b
  simp only [beqNode, Bool.and_eq_true] at h
  rw [beqList_eq (beqList_eq beqTok_eq) _ _ h.1, beqList_eq beqTok_eq _ _ h.2]

def tokCode (t : Tok) : Nat := 3 * t.1 + t.2

/-- The layer code used in keys (`1 + t` or `34 + 33 t₁ + t₂`); below `1123` for valid layers. -/
def layerCode : Layer → Nat
  | [t] => 1 + tokCode t
  | [t, u] => 34 + 33 * tokCode t + tokCode u
  | _ => 0

/-- Code of a depth-2 node: `1123 · code(top layer) + code(second layer)`. -/
def rootCode (n : Node) : Nat :=
  match n.layers with
  | [a, b] => layerCode a * 1123 + layerCode b
  | _ => 0

/-- The depth-2 node (no cube) with a given root code. -/
def decodeRoot (c : Nat) : Node := ⟨[decodeLayer (c / 1123), decodeLayer (c % 1123)], []⟩

/-! ## The checker -/

/-- Cover certificate of one root (`root`: its root code, see `rootCode`): decision digits `ds` (base 16, first decision least significant; in depth-first
order `0` = certified node, `1` = layer split, `1 + K` = σ-split on `K` bits) and the keys of the certified nodes, in
the same order, packed into `ks` (base `2 ^ 64`). -/
structure Cert where
  root : Nat
  ds : Nat
  ks : Nat

/-- Numbers packed in base `2 ^ 64`, least significant first (stops at the first zero remainder; keys are never 0). -/
def unpack : Nat → Nat → List Nat
  | 0, _ => []
  | f + 1, n =>
    match Nat.beq n 0 with
    | true => []
    | false => n % 18446744073709551616 :: unpack f (n / 18446744073709551616)

/-- The keys of the certified nodes named by a certificate, in depth-first order. -/
def Cert.keys (c : Cert) : List Nat := unpack 100000 c.ks

/-- Depth-first check of a cover certificate: `stk` holds the nodes still to cover. -/
def run (fuel : Nat) (stk : List Node) (ds : Nat) (ks : List Nat) : Bool :=
  match fuel, stk with
  | _, [] => ds == 0 && ks.isEmpty
  | 0, _ :: _ => false
  | f + 1, n :: rest =>
    if ds % 16 = 0 then
      match ks with
      | [] => false
      | k :: ks' => beqNode n (decodeKey k) && run f rest (ds / 16) ks'
    else if ds % 16 = 1 then
      decide (2 ≤ n.layers.length) && !n.layerChildren.isEmpty && run f (n.layerChildren ++ rest) (ds / 16) ks
    else
      decide (2 ≤ n.layers.length) && decide (ds % 16 - 1 ≤ n.free.length) &&
        run f (n.sigmaChildren (ds % 16 - 1) ++ rest) (ds / 16) ks

def checkRoot (ρ : Node) (c : Cert) : Bool := run 1000000 [ρ] c.ds c.keys

theorem run_sound (S : Node → Prop) (fuel : Nat) :
    ∀ (stk : List Node) (ds : Nat) (ks : List Nat), run fuel stk ds ks = true →
      (∀ k ∈ ks, S (decodeKey k)) → ∀ n ∈ stk, Covered S n := by
  induction fuel with
  | zero =>
    intro stk ds ks h _ n hn
    cases stk with
    | nil => cases hn
    | cons a rest => simp [run] at h
  | succ f ih =>
    intro stk ds ks h hk n hn
    cases stk with
    | nil => cases hn
    | cons a rest =>
      simp only [run] at h
      have hn' : n = a ∨ n ∈ rest := List.mem_cons.mp hn
      by_cases h0 : ds % 16 = 0
      · rw [if_pos h0] at h
        cases ks with
        | nil => simp at h
        | cons k ks' =>
          simp only [Bool.and_eq_true] at h
          have hk' : ∀ k' ∈ ks', S (decodeKey k') := fun k' h' => hk k' (List.mem_cons_of_mem _ h')
          rcases hn' with rfl | hr
          · exact .cert (beqNode_eq h.1 ▸ hk k (List.mem_cons_self ..))
          · exact ih rest _ ks' h.2 hk' n hr
      · rw [if_neg h0] at h
        by_cases h1 : ds % 16 = 1
        · rw [if_pos h1] at h
          simp only [Bool.and_eq_true, decide_eq_true_eq, Bool.not_eq_true'] at h
          obtain ⟨⟨h2, hne⟩, hr⟩ := h
          have hall := ih _ _ ks hr hk
          rcases hn' with rfl | hr'
          · refine .layer h2 ?_ fun c hc => hall c (List.mem_append_left _ hc)
            intro he; rw [he] at hne; simp at hne
          · exact hall n (List.mem_append_right _ hr')
        · rw [if_neg h1] at h
          simp only [Bool.and_eq_true, decide_eq_true_eq] at h
          obtain ⟨⟨h2, hf⟩, hr⟩ := h
          have hall := ih _ _ ks hr hk
          rcases hn' with rfl | hr'
          · exact .sigma _ h2 (by omega) hf fun c hc => hall c (List.mem_append_left _ hc)
          · exact hall n (List.mem_append_right _ hr')

theorem checkRoot_sound {ρ : Node} {c : Cert} (h : checkRoot ρ c = true) :
    Covered (fun n => ∃ k ∈ c.keys, decodeKey k = n) ρ :=
  run_sound _ _ [ρ] c.ds c.keys h (fun k hk => ⟨k, hk, rfl⟩) ρ (List.mem_singleton_self ρ)

theorem all_append_of {α : Type} {f : α → Bool} {l₁ l₂ : List α} (h₁ : l₁.all f = true) (h₂ : l₂.all f = true) :
    (l₁ ++ l₂).all f = true := by
  simp [List.all_append, h₁, h₂]

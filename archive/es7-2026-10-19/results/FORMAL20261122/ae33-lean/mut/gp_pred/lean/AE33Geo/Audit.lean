import AE33Geo.Radius1
open ErdosSzekeres AE33 AE33Geo

/-! # AE33Geo.Audit: the end theorems, the definitions in their statements, and the axioms, pinned by
`#guard_msgs` (outputs copied from `logs/geo10.log`, the build of `Audit0.lean`). -/

/--
info: ae33_pair : TextsUnsat203 →
  ∀ (i : Fin 203) (P : Fin 31 → Point),
    Realizes (baseOf ↑i) P ∨ RealizesMirror (baseOf ↑i) P →
      ∀ (p q : Point),
        GeneralPosition (insert p (insert q (Finset.image P Finset.univ))) →
          (insert p (insert q (Finset.image P Finset.univ))).card = 33 →
            ConvexNGonThrough 7 (insert p (insert q (Finset.image P Finset.univ))) p ∨
              ConvexNGonThrough 7 (insert p (insert q (Finset.image P Finset.univ))) q
-/
#guard_msgs (whitespace := lax) in #check @AE33Geo.ae33_pair

/--
info: ae33_radius1 : TextsUnsat203 →
  ∀ (S : Finset Point),
    GeneralPosition S →
      S.card = 33 →
        ∀ (u v : ℕ),
          u < 33 →
            v < 33 →
              u ≠ v →
                ∀ (φ : ℕ → Point),
                  (∀ w < 33, w ≠ u → w ≠ v → φ w ∈ S) →
                    (∀ (a b : ℕ), a < 33 → b < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → φ a = φ b → a = b) →
                      OTEmb φ u v ∨ OTEmbMirror φ u v → HasConvexNGon 7 S
-/
#guard_msgs (whitespace := lax) in #check @AE33Geo.ae33_radius1

/--
info: def AE33.TextsUnsat203 : Prop :=
∀ i < 203, ∀ (nv : ℕ) (F : List (List ℤ)), EncB.parseDimacs (cnfText i) = some (nv, F) → ¬EncB.DimacsSatisfiable F
-/
#guard_msgs (whitespace := lax) in #print AE33.TextsUnsat203

/--
info: def AE33.cnfText : ℕ → String :=
fun i => EncB.render (numVars (baseOf i)) (cnf (baseOf i))
-/
#guard_msgs (whitespace := lax) in #print AE33.cnfText

/--
info: def AE33Geo.Realizes : Array Pt → (Fin 31 → Point) → Prop :=
fun B P =>
  ∀ (i j k : Fin 31),
    0 < orient (P i) (P j) (P k) ↔ 0 < iorient (B.getD ↑i (0, 0)) (B.getD ↑j (0, 0)) (B.getD ↑k (0, 0))
-/
#guard_msgs (whitespace := lax) in #print AE33Geo.Realizes

/--
info: def AE33Geo.RealizesMirror : Array Pt → (Fin 31 → Point) → Prop :=
fun B P =>
  ∀ (i j k : Fin 31),
    0 < orient (P i) (P j) (P k) ↔ iorient (B.getD ↑i (0, 0)) (B.getD ↑j (0, 0)) (B.getD ↑k (0, 0)) < 0
-/
#guard_msgs (whitespace := lax) in #print AE33Geo.RealizesMirror

/--
info: def AE33Geo.ConvexNGonThrough : ℕ → Finset Point → Point → Prop :=
fun m S x => ∃ t ⊆ S, t.card = m ∧ ConvexPosition t ∧ x ∈ t
-/
#guard_msgs (whitespace := lax) in #print AE33Geo.ConvexNGonThrough

/--
info: def AE33Geo.OTEmb : (ℕ → Point) → ℕ → ℕ → Prop :=
fun φ u v =>
  ∀ (a b c : ℕ),
    a < 33 →
      b < 33 →
        c < 33 →
          a ≠ u →
            a ≠ v →
              b ≠ u →
                b ≠ v →
                  c ≠ u →
                    c ≠ v →
                      (0 < orient (φ a) (φ b) (φ c) ↔
                        0 < iorient (ae33.getD a (0, 0)) (ae33.getD b (0, 0)) (ae33.getD c (0, 0)))
-/
#guard_msgs (whitespace := lax) in #print AE33Geo.OTEmb

/--
info: def AE33Geo.OTEmbMirror : (ℕ → Point) → ℕ → ℕ → Prop :=
fun φ u v =>
  ∀ (a b c : ℕ),
    a < 33 →
      b < 33 →
        c < 33 →
          a ≠ u →
            a ≠ v →
              b ≠ u →
                b ≠ v →
                  c ≠ u →
                    c ≠ v →
                      (0 < orient (φ a) (φ b) (φ c) ↔
                        iorient (ae33.getD a (0, 0)) (ae33.getD b (0, 0)) (ae33.getD c (0, 0)) < 0)
-/
#guard_msgs (whitespace := lax) in #print AE33Geo.OTEmbMirror

/--
info: 'AE33Geo.ae33_pair' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.ae33_pair

/--
info: 'AE33Geo.ae33_radius1' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.ae33_radius1

/--
info: 'AE33Geo.cnf_sat' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.cnf_sat

/--
info: 'AE33Geo.clauseOf_sound' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.clauseOf_sound

/--
info: 'AE33.texts_iff_cnfs' depends on axioms: [propext, Quot.sound]
-/
#guard_msgs (whitespace := lax) in #print axioms AE33.texts_iff_cnfs

/--
info: 'AE33Geo.hept_ccw' does not depend on any axioms
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.hept_ccw

/--
info: 'AE33Geo.pairs_cover' depends on axioms: [propext, Quot.sound]
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.pairs_cover

/--
info: 'AE33Geo.pvar_spec_all' does not depend on any axioms
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.pvar_spec_all

/--
info: 'AE33Geo.baseOf_size' does not depend on any axioms
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.baseOf_size

/--
info: 'AE33Geo.keepIdx_len' does not depend on any axioms
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.keepIdx_len

/--
info: 'AE33Geo.pairs203_len' does not depend on any axioms
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.pairs203_len
/--
info: 'AE33Geo.ae33_radius0' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs (whitespace := lax) in #print axioms AE33Geo.ae33_radius0

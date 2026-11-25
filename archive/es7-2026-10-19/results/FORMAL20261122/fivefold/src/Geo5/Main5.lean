import ES8Geo.Capstone2
import EncBO.SatisfiableO
import EncB.Compose
import Geo7.ModelOfLab

/-!
# The fivefold heptagon theorem (RESULTS row C4) from the cake_lpr verdict on `twin-base 5 7 7`

Nothing here is new mathematics: every step is a generic lemma of the sevenfold development
(FORMAL20261122/sevenfold, itself built on ENCBLEAN), used at `m = 5, K = 7, t = 7` instead of `m = 7, K = 8, t = 10`.

* `encB_satisfiable_odd` (EncBO/SatisfiableO.lean, odd `m ≥ 2`): a `ModelO m K t` satisfies `encB m K t`.
* `modelO_of_counterexample` (Geo7/ModelOfLab.lean, any `m ≥ 3`, `4 ≤ K ≤ 2m`): a centre-free set of `m·t` points in
  general position, invariant under the rotation by `2π/m`, with no convex `K`-gon, yields a `ModelO m K t`.
* `parseDimacs_cnfText` (ENCBLEAN EncB/Compose.lean, generic in `m K t`): the round trip of the printed text.
* `convexNGon_of_layers` (ES8Geo/Capstone2.lean): the layer reduction for the corollaries, whose proofs are copied
  verbatim from LEANEXT/es7corr/ES7Corollaries.lean (`fivefold_heptagon_of_erase`, `fivefold_heptagon`,
  `fivefold_heptagon_of_centre_not_mem`).

`Fivefold35` has the body of `ErdosSzekeres.SymReduction.Fivefold35` (SYMLEAN/SymmetricReduction.lean:476) and of its
verbatim copy in LEANEXT/es7corr; it is restated here because that file's names clash with Capstone2.

External facts this file does not prove (ENCBLEAN trust items, read for this instance):
* E1: the text `cnfText (encode 5 7 7) []`, printed by the pinned exe `encb_dimacs` (SHA-256 `3d43fa8b…`) as
  `twin-base 5 7 7`, has SHA-256 `326758c67f75aafd80b6e21feae4778da45a983417377211050058ef5b7f8c93`;
* E2: CaDiCaL 2.1.3 gave an LRAT proof of that file and cake_lpr `c14ff498…` printed `s VERIFIED UNSAT`;
* E3: that verdict means `¬ DimacsSatisfiable` of what `parseDimacs` reads from the text.

Every declaration that mentions the instance (`5 7 7`) is a term; the numerals are separate lemmas.
-/

namespace EncB.Geo5
open ErdosSzekeres ErdosSzekeres.LayerLemma

/-- Fivefold symmetric, 35 points, centre not in the set (the body of SYMLEAN's `Fivefold35`). -/
def Fivefold35 : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 35 → c ∉ S →
    Invariant (rotAbout c (2 * Real.pi / 5)) S → HasConvexNGon 7 S

/-- The numeral side conditions of (5,7,7). -/
theorem numerals5 : 3 ≤ 5 ∧ 4 ≤ 7 ∧ 7 ≤ 2 * 5 ∧ (35 : ℕ) = 5 * 7 := by norm_num

/-- The parity side conditions of M3 at `m = 5`. -/
theorem five_odd : 5 % 2 = 1 ∧ 2 ≤ 5 := by decide

/-- `Fivefold35` writes the angle with the real numeral `5`; M6 takes `((5 : ℕ) : ℝ)`. -/
theorem invariant_cast_five {T : Finset Point} {c : Point}
    (h : Invariant (rotAbout c (2 * Real.pi / 5)) T) :
    Invariant (rotAbout c (2 * Real.pi / ((5 : ℕ) : ℝ))) T := by
  exact_mod_cast h

/-- M3 at (5,7,7); no tactic touches `encB 5 7 7`. -/
theorem encB_satisfiable_577 (M : EncB.ModelO 5 7 7) : EncB.DimacsSatisfiable (EncB.encB 5 7 7) :=
  EncB.encB_satisfiable_odd five_odd.1 five_odd.2 M

/-- **The text `twin-base 5 7 7` prints parses to the theorem's clause list.** -/
theorem parseDimacs_base577 :
    EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) =
      some (EncB.numVars 5 7 7, EncB.cubeCnf (EncB.encB 5 7 7) []) :=
  EncB.parseDimacs_cnfText 5 7 7 [] (fun _ hz => absurd hz List.not_mem_nil)

/-- The verdict about the text gives `¬ DimacsSatisfiable (encB 5 7 7)`. -/
theorem encB577_unsat_of_text
    (h : ∀ (nv : Nat) (G : List (List Int)), EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G) :
    ¬EncB.DimacsSatisfiable (EncB.encB 5 7 7) :=
  EncB.cubeCnf_nil (EncB.encB 5 7 7) ▸ h _ _ parseDimacs_base577

/-- The hypothesis is not vacuous: it is equivalent to `¬ DimacsSatisfiable (encB 5 7 7)`. -/
theorem text577_iff :
    (∀ (nv : Nat) (G : List (List Int)), EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G) ↔ ¬EncB.DimacsSatisfiable (EncB.encB 5 7 7) :=
  ⟨encB577_unsat_of_text, fun hu _nv _G hp =>
    (Prod.mk.inj (Option.some.inj (parseDimacs_base577.symm.trans hp))).2 ▸ (EncB.cubeCnf_nil (EncB.encB 5 7 7)).symm ▸ hu⟩

/-- **The geometric half for m = 5**: every centre-free 35-point set in general position, invariant under the
rotation by `2π/5` about `c`, with no convex heptagon, yields a `ModelO 5 7 7`. -/
theorem geo5Bridge :
    ∀ (T : Finset Point) (c : Point), GeneralPosition T → c ∉ T →
      Invariant (rotAbout c (2 * Real.pi / 5)) T → T.card = 35 → ¬ HasConvexNGon 7 T →
        Nonempty (EncB.ModelO 5 7 7) :=
  fun _T _c hgp hc hinv hcard hno =>
    EncB.Geo7.modelO_of_counterexample (m := 5) (K := 7) (t := 7) numerals5.1 numerals5.2.1 numerals5.2.2.1 hgp hc
      (invariant_cast_five hinv) hno (hcard.trans numerals5.2.2.2)

/-- `Fivefold35` from the absence of a `ModelO 5 7 7`. -/
theorem fivefold35_of_no_modelO (h : EncB.ModelO 5 7 7 → False) : Fivefold35 :=
  fun T c hgp hcard hc hinv =>
    Classical.byContradiction fun hno => (geo5Bridge T c hgp hc hinv hcard hno).elim h

/-- **`Fivefold35` from `¬ DimacsSatisfiable (encB 5 7 7)`.** -/
theorem fivefold35_of_unsat (h : ¬ EncB.DimacsSatisfiable (EncB.encB 5 7 7)) : Fivefold35 :=
  fivefold35_of_no_modelO fun M => h (encB_satisfiable_577 M)

/-- **`Fivefold35` from the verdict on the text** printed by `twin-base 5 7 7`. -/
theorem fivefold35_of_text
    (h : ∀ (nv : Nat) (G : List (List Int)), EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G) : Fivefold35 :=
  fivefold35_of_unsat (encB577_unsat_of_text h)

/-! ## Corollaries (proofs verbatim from LEANEXT/es7corr/ES7Corollaries.lean) -/

/-- **Fivefold, layer form.** From `Fivefold35`: every fivefold symmetric set in general position
with more than `30` points other than the centre contains a convex heptagon. -/
theorem fivefold_heptagon_of_erase (H : Fivefold35) (S : Finset Point) (c : Point)
    (hgp : GeneralPosition S) (hinv : Invariant (rotAbout c (2 * Real.pi / 5)) S)
    (hcard : 30 < (S.erase c).card) : HasConvexNGon 7 S := by
  classical
  refine convexNGon_of_layers (m := 5) (K := 7) (t := 7) (by norm_num) (by norm_num) ?_ S c hgp
    (by exact_mod_cast hinv) ?_
  · intro T c' h1 h2 h3 h4
    exact H T c' h1 (by simpa using h4) h2 (by exact_mod_cast h3)
  · omega

/-- **The fivefold case of `ES(7)`, reduced to `Fivefold35`.** Every fivefold symmetric set of at
least `32` points in general position contains a convex heptagon (the centre adds at most one
point). -/
theorem fivefold_heptagon (H : Fivefold35) (S : Finset Point) (c : Point)
    (hgp : GeneralPosition S) (hinv : Invariant (rotAbout c (2 * Real.pi / 5)) S)
    (hcard : 32 ≤ S.card) : HasConvexNGon 7 S := by
  classical
  refine fivefold_heptagon_of_erase H S c hgp hinv ?_
  have h2 := Finset.pred_card_le_card_erase (s := S) (a := c)
  omega

/-- **Fivefold, centre-free form.** From `Fivefold35`: a fivefold symmetric set in general position
that avoids the centre and has at least `31` points contains a convex heptagon. -/
theorem fivefold_heptagon_of_centre_not_mem (H : Fivefold35) (S : Finset Point) (c : Point)
    (hgp : GeneralPosition S) (hinv : Invariant (rotAbout c (2 * Real.pi / 5)) S) (hc : c ∉ S)
    (hcard : 31 ≤ S.card) : HasConvexNGon 7 S := by
  classical
  refine fivefold_heptagon_of_erase H S c hgp hinv ?_
  rw [Finset.erase_eq_of_notMem hc]
  omega

/-- **The fivefold heptagon theorem from the verdict on the text.** Every set of at least 32 points in general
position that is invariant under the rotation by `2π/5` about some point has a convex heptagon, provided the text
printed by `twin-base 5 7 7` parses to an unsatisfiable clause list. -/
theorem fivefold_heptagon_of_text
    (h : ∀ (nv : Nat) (G : List (List Int)), EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 5)) S) (hcard : 32 ≤ S.card) : HasConvexNGon 7 S :=
  fivefold_heptagon (fivefold35_of_text h) S c hgp hinv hcard

/-- The centre-free form from the verdict on the text (at least 31 points). -/
theorem fivefold_heptagon_of_centre_not_mem_of_text
    (h : ∀ (nv : Nat) (G : List (List Int)), EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 5)) S) (hc : c ∉ S) (hcard : 31 ≤ S.card) : HasConvexNGon 7 S :=
  fivefold_heptagon_of_centre_not_mem (fivefold35_of_text h) S c hgp hinv hc hcard

/-! ## Any rotation of order 5 (as `EncB.Geo7`'s order-7 lemmas, with 7 replaced by 5) -/

/-- `rotAbout` is `2π`-periodic in the angle. -/
theorem rotAbout_add_nat_mul_two_pi' (c : Point) (θ : ℝ) (n : ℕ) :
    rotAbout c (θ + n * (2 * Real.pi)) = rotAbout c θ := by
  funext p
  simp only [rotAbout, Real.cos_add_nat_mul_two_pi, Real.sin_add_nat_mul_two_pi]

/-- Invariance under `ρ^j` gives invariance under `ρ` when `j·j' = 1 + 5n` (`ρ` the rotation by `2π/5`). -/
theorem invariant_of_inverse {S : Finset Point} {c : Point} {j j' n : ℕ} (hjj : j * j' = 1 + 5 * n)
    (h : Invariant (rotAbout c (2 * Real.pi * j / 5)) S) : Invariant (rotAbout c (2 * Real.pi / 5)) S := by
  intro p hp
  have hit := iterate_mem h hp j'
  rw [rotAbout_iterate] at hit
  have e : (j' : ℝ) * (2 * Real.pi * j / 5) = 2 * Real.pi / 5 + (n : ℝ) * (2 * Real.pi) := by
    have : (j : ℝ) * j' = 1 + 5 * n := by exact_mod_cast hjj
    linear_combination (2 * Real.pi / 5) * this
  rwa [e, rotAbout_add_nat_mul_two_pi'] at hit

/-- **A rotation of order 5** about `c` (by `2πj/5`, `1 ≤ j ≤ 4`) gives invariance under the rotation by `2π/5`. -/
theorem invariant_fifth_of_order5 {S : Finset Point} {c : Point} {j : ℕ} (hj : 1 ≤ j ∧ j ≤ 4)
    (h : Invariant (rotAbout c (2 * Real.pi * j / 5)) S) : Invariant (rotAbout c (2 * Real.pi / 5)) S := by
  obtain ⟨h1, h4⟩ := hj
  interval_cases j
  · exact invariant_of_inverse (j' := 1) (n := 0) (by norm_num) h
  · exact invariant_of_inverse (j' := 3) (n := 1) (by norm_num) h
  · exact invariant_of_inverse (j' := 2) (n := 1) (by norm_num) h
  · exact invariant_of_inverse (j' := 4) (n := 3) (by norm_num) h

/-- **The fivefold heptagon theorem for any rotation of order 5**, from the verdict on the text. -/
theorem fivefold_heptagon_order5_of_text
    (h : ∀ (nv : Nat) (G : List (List Int)), EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S) (j : ℕ) (hj : 1 ≤ j ∧ j ≤ 4)
    (hinv : Invariant (rotAbout c (2 * Real.pi * j / 5)) S) (hcard : 32 ≤ S.card) : HasConvexNGon 7 S :=
  fivefold_heptagon_of_text h S c hgp (invariant_fifth_of_order5 hj hinv) hcard

end EncB.Geo5

/-! ## Pins: statements and axioms (the build fails if either changes) -/

/--
info: EncB.Geo5.fivefold35_of_text
  (h :
    ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G) :
  EncB.Geo5.Fivefold35
-/
#guard_msgs in #check EncB.Geo5.fivefold35_of_text
/--
info: EncB.Geo5.fivefold_heptagon_of_text
  (h :
    ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G)
  (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point) (hgp : ErdosSzekeres.GeneralPosition S)
  (hinv : ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 5)) S)
  (hcard : 32 ≤ S.card) : ErdosSzekeres.HasConvexNGon 7 S
-/
#guard_msgs in #check EncB.Geo5.fivefold_heptagon_of_text
/--
info: EncB.Geo5.fivefold_heptagon_of_centre_not_mem_of_text
  (h :
    ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G)
  (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point) (hgp : ErdosSzekeres.GeneralPosition S)
  (hinv : ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 5)) S) (hc : c ∉ S)
  (hcard : 31 ≤ S.card) : ErdosSzekeres.HasConvexNGon 7 S
-/
#guard_msgs in #check EncB.Geo5.fivefold_heptagon_of_centre_not_mem_of_text
/--
info: EncB.Geo5.text577_iff :
  (∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G) ↔
    ¬EncB.DimacsSatisfiable (EncB.encB 5 7 7)
-/
#guard_msgs in #check EncB.Geo5.text577_iff
/--
info: EncB.Geo5.fivefold_heptagon_order5_of_text
  (h :
    ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G)
  (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point) (hgp : ErdosSzekeres.GeneralPosition S) (j : ℕ)
  (hj : 1 ≤ j ∧ j ≤ 4)
  (hinv : ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi * ↑j / 5)) S)
  (hcard : 32 ≤ S.card) : ErdosSzekeres.HasConvexNGon 7 S
-/
#guard_msgs in #check EncB.Geo5.fivefold_heptagon_order5_of_text
/--
info: def EncB.Geo5.Fivefold35 : Prop :=
∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
  ErdosSzekeres.GeneralPosition S →
    S.card = 35 →
      c ∉ S →
        ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 5)) S →
          ErdosSzekeres.HasConvexNGon 7 S
-/
#guard_msgs in #print EncB.Geo5.Fivefold35
/--
info: 'EncB.Geo5.geo5Bridge' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms EncB.Geo5.geo5Bridge
/--
info: 'EncB.Geo5.fivefold35_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms EncB.Geo5.fivefold35_of_unsat
/--
info: 'EncB.Geo5.fivefold35_of_text' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms EncB.Geo5.fivefold35_of_text
/--
info: 'EncB.Geo5.fivefold_heptagon_of_text' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms EncB.Geo5.fivefold_heptagon_of_text
/--
info: 'EncB.Geo5.fivefold_heptagon_of_centre_not_mem_of_text' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms EncB.Geo5.fivefold_heptagon_of_centre_not_mem_of_text
/--
info: 'EncB.Geo5.text577_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms EncB.Geo5.text577_iff
/--
info: 'EncB.Geo5.fivefold_heptagon_order5_of_text' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms EncB.Geo5.fivefold_heptagon_order5_of_text

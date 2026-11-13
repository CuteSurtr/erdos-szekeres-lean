# Review of section `oc`, round 1, lens: rigor (referee)

Verdict: **pass**. No blocker and no major finding. 11 minor findings, listed below.

Section file: `sections/oc.tex` (870 lines). Map: `sections/oc.map.tsv` (43 rows).

## What was checked, and how

1. **Compile.** `build/oc_rigorr1_wrapper.tex` (contract wrapper), two `nice -n 15 pdflatex` passes, both exit 0. 0 overfull boxes, no errors.
   The only undefined references are the allowed `fd:` / `ll:` / `lg:` labels (fd:def:point, orient, gp, ngon, inv, rot;
   fd:lem:orient, affine-orient, collinear, cp-hull, mono, separation; ll:def:hv, peel; ll:lem:antitone, inv-peel,
   minperiod; ll:thm:core-rot; lg:def:polar; lg:lem:centre). Every one is in the contract's export lists. Every `oc:` ref
   resolves. All 13 export labels are defined on the right statements.
2. **Map vs. heads.** Script cross-check: 43 statement environments, 43 map rows. Kinds, Lean names and file:line agree
   row by row.
3. **Fidelity against the Lean source, statement by statement.** Every Lean-referenced statement was compared with
   `orbit/OrbitConsistency.lean`, `merged/Merged.lean:1148-1385` and `keys/KeyOrder.lean`. The comparison covered
   hypotheses, implicit and explicit arguments, Set vs. Finset, maps-into, 2π/m with m = 0, `Even`, `m/2 : ℕ`, Euclidean
   `%` and `/`, `toIcoMod Real.two_pi_pos 0`, `toLex`, and conclusions stated as `False` vs. ≠. Every one matches.
   Every cited line number is exact: all heads; LayerLemma 52, 105, 231-308, 298, 364, 465, 932; OrientationGeometry:66;
   gen.py:108; gen_b2.py:56; DESIGN.md:625 and 626; Orbit.lean:13; m4_build.log:3-10; check_literals.log:1-5;
   REPORT.md:22-25.
4. **Provenance claims.** The SHA-256 prefixes of OrbitConsistency, Merged, KeyOrder and LayerLemma match. The ENCBLEAN
   copies are byte-identical. `diff` confirms these claims:
   - Merged 1-1147 equals LayerLemma 1-1147.
   - Merged 1160-1311 vs. OrbitConsistency 273-427 differ in doc comments only.
   - Merged 1148-1383 equals Capstone2 1156-1391.
   - The copied block (OrbitConsistency 39-112) equals LayerLemma up to the type-variable binder, plus one doc comment.

   Other checks:
   - The toolchain is Lean v4.24.0 with Mathlib `f897ebcf…`, in both the repository root and ENCBLEAN/geo, and the pin
     has been unchanged since 2026-10-04 (read-only `git log`).
   - The only `decide` uses are OrbitConsistency:236 and Merged:1125, as claimed.
   - There is no sorry, admit, axiom declaration or native_decide.
   - The axioms logs say what the text claims.
   - `PreservesOrient.iterate` is unused by any printed theorem.
   - The cited Mathlib facts were read in the pinned Mathlib checkout (commit f897ebcf): `toIcoDiv`/`toIcoMod`
     definitions, `toIcoMod_eq_iff`, `swap_induction_on`, `sign_mul`, `sign_swap`, `Int.units_eq_one_or`,
     `Prod.Lex.lt_iff`, `StrictMonoOn`/`.lt_iff_lt`, `Int.emod_nonneg`/`emod_lt_of_pos`/`emod_add_mul_ediv`. All are
     stated correctly.
5. **Every identity checked with sympy.** The script is `build/oc_rigorr1_sympy.py`; run under `nice -n 15` with the
   symvenv Python, it ends with **ALL OK**.

   Trigonometric and rotation facts:
   - Composition of rotations, including both displayed coordinate formulas.
   - R_0 = R_2π = id and R_π(p) = 2c − p.
   - m·(2π/m) = 2π and k·2π/(2k) = π.
   - The rot-inv difference equals orient·(s² + co² − 1) as an exact polynomial identity; det M_θ = 1;
     orient = det(b−a | d−a).

   Orientation and ray facts:
   - The three swap cases and the two cyclic-rule steps used.
   - same-ray (ii), (iii) and (iv): y−x = (l−1)(x−c), q−x = −2(x−c), y−q = (l+1)(x−c), orient(x,y,q) = 0.

   Polar and phase facts:
   - rotAbout_polar and polar_add_int.
   - phase-nat: y − c = (r'/r)(z − c), and the rotation of polar points.
   - phase-int split (j + mq)(2π/m) = j(2π/m) + q·2π.
   - Euclidean division equals floor division for m > 0, checked exhaustively on a small range.

   Key-order facts:
   - cell only-if identity: (J1u+ψ1) − (J2u+ψ2) = (J1−J2−1)u + ψ1 + (u−ψ2).
   - reduce (ii) and (iii) with Nu = 2π.
   - antipode_odd and antipode_even rewrites, and Nu = 2π.
   - Half-open counterexample.
   - toIcoDiv existence via floor (spot checks).

   Parity remark:
   - All six rows of the parity table: τ, the transposition product with (στ)(i) = σ(τ(i)), inv(τ), and sgn.
   - inv(a) = inv(σ⁻¹) for the sorting permutation, all six orders.

   Example of Remark oc:rem:layers(3), in exact rational arithmetic:
   - ρ = rotation by π/2 maps S onto S.
   - All 56 triples have orient ≠ 0.
   - (1/2,1/2) = 3/8(2,0) + 3/8(0,2) + 1/8(−2,0) + 1/8(0,−2).
   - Each outer point is the unique maximiser of ±x, ±y over S, and each inner point is the unique maximiser of ±x±y over
     the inner points.
   - (1/2,1/2) = polar(0, √2/2, π/4).
   - π/4 = 1·π/4 but π/4 = ½·(2π/4).
6. **Proof steps, one by one.** For every proof the following were checked:
   - inequality directions: cell, reduce, literal_sound;
   - exhaustiveness of case splits: S1 sgn = ±1; the three unordered swap pairs; trichotomy in cell, rank only-if and
     disjoint(b); a+1 < m or a = m−1 in Lemma closed;
   - well-foundedness of inductions: on ℕ in iterate, iter-mem, PreservesOrient.iterate, rotComp_iterate and encoder
     Step 1; rule induction for RotComp; Mathlib's swap induction for perm;
   - that each use of an earlier result meets its hypotheses exactly:
     - Theorem literal inside encoder Step 3;
     - Lemma same-ray with x := z (phase-nat) and with x := ρ^[k]x (layers-ray);
     - (L2) and (L3) in Lemma closed, including c ∉ X and K-freeness of X via fd:lem:mono(c);
     - Theorem phase-orbit in layers-phase, including the orbit hypothesis via closed and disjoint(b);
     - Lemma reduce in antipode-cell and key, with N = 2m, u = π/m and N = m, u = 2π/m;
   - that nothing is delegated to Lean. The parentheticals about Lean proofs are informational only, and every written
     proof is complete.

   Remark oc:rem:layers(1), which says that c ∉ S follows from the other hypotheses via `centre_not_mem_of_even`, was
   checked against LayerLemma.lean:582. The cited signature `(0<m) (Even m) (Invariant) (GP) (p ∈ S) (p ≠ c)` is exact,
   and the argument is correct.

## Findings (all minor)

### M1. Remark oc:rem:parity misdescribes the Python evidence (oc.tex:433-435)
The text says: "The agreement of `sortpar` with the permutation sign on all six orders was also tested in Python". But
`LEANEXT/orbit/check_literals.py:25-38` compares `sortpar`'s bubble-sort parity with its own `perm_sign`, which is again
an **inversion count**. It does not compare with an independently computed sign, and nothing like Mathlib's
`Equiv.Perm.sign` appears. The remark's own point is the mismatch "sgn vs. inversion count", so the sentence can be read
as evidence for the very bridge that the six-case argument supplies. There is no effect on correctness, because the
written six-case argument is complete and the remark already says "evidence, not proof".
*Suggested fix:* "The agreement of `sortpar` with an inversion count (`check_literals.py:25-38`) on all six orders was
also tested in Python, …". Optionally add that bubble sort ends with 0 inversions, so the number of exchanges equals
inv(a).

### M2. Section 13 has more verbatim carriers than stated (oc.tex:49-52, 867-868)
`diff` shows that Merged.lean 1148-1383 also reappears verbatim in two more files:
- `LEANEXT/linked/Linked.lean` 1148-1383;
- `LEANEXT/capstone/Capstone.lean` 1156-1391.

The Sources paragraph and Coverage (iv) mention only Capstone2.lean. The inventory records both other copies
(main_results, "same lines in linked/Linked.lean; Capstone.lean/Capstone2.lean:1168-1319").
*Suggested fix:* list Linked.lean and Capstone.lean with Capstone2.lean in both places.

### M3. Axiom records for the LAYERLEAN-located references are not among "the logs above" (oc.tex:80-81; heads at 166, 187)
The Rigor paragraph says every Lean-referenced statement is Lean-checked "in the sense of the logs above". Lemmas
oc:lem:iterate and oc:lem:iter-mem also cite `ErdosSzekeres.LayerLemma.rotAbout_iterate` (LAYERLEAN:465) and
`ErdosSzekeres.LayerLemma.iterate_mem` (LAYERLEAN:52). Their axiom records are in `LEANEXT/review/axioms.log`, at line 33
and line 1; iterate_mem has only `[propext, Quot.sound]`. They are also covered transitively by `merged/axioms.log` for
the Merged copies. Neither log is cited for them.
*Suggested fix:* one clause in the Axioms paragraph, e.g. "the two LayerLemma helpers cited in Lemmas oc:lem:iterate and
oc:lem:iter-mem are recorded in LEANEXT/review/axioms.log (iterate_mem: [propext, Quot.sound])".

### M4. The Dependencies paragraph is incomplete (oc.tex:88-97)
The section also uses four more labels:
- fd:lem:affine-orient (proof of Lemma oc:lem:rot-inv);
- fd:lem:cp-hull and fd:lem:separation (Remark oc:rem:layers(3));
- ll:lem:minperiod (parenthetical in the proof of Lemma oc:lem:closed).

All are allowed refs; the list omits them.
*Suggested fix:* add them, with "in a remark/parenthetical only" where that applies.

### M5. The informal overview drops 0 < m and writes orient for orient₃ (oc.tex:13-19)
Item (B) says: "For even m, a finite set … mapped into itself by the rotation ρ by 2π/m … contains the antipode
2c − x of each of its points". But m = 0 is even, and then ρ = R_{c,0} = id, so the sentence is false for m = 0. Every
formal statement assumes 0 < m. Item (A) writes orient(t) and orient(C) for triples where orient₃ is meant.
*Suggested fix:* "For even m > 0", and orient₃ in (A).

### M6. Remark oc:rem:layers(3) leaves two elementary steps implicit (oc.tex:664-669)
The example itself is correct; I checked it exactly. Two steps are left implicit:
- (a) The general-position argument lists only the lines through two outer points or through two inner points. It
  should say why this suffices: any three points of S include two of the same kind (pigeonhole).
- (b) "the convex hull {|x|+|y| ≤ 2} of the outer points" is asserted without proof. Only "inner points lie in
  conv(outer)" is needed, and an explicit convex combination would do, e.g. (1/2,1/2) = 3/8(2,0) + 3/8(0,2) +
  1/8(−2,0) + 1/8(0,−2), and its images under ρ.

This is a remark that illustrates sharpness, not part of any Lean statement's proof. I rate it minor, but a strict
reading of "true but unproved claim used" could put (b) at major. The fix is one sentence.

### M7. Literal "--" inside `\dirn{…}` (oc.tex:66, 824, 863, 866)
`\dirn` uses `\nolinkurl`, so `151--158`, `22--25` and `231--308` print as a double hyphen. Elsewhere the en-dash is
used. The rendered text shows "KeyOrder.lean:151--158" and "REPORT.md:22--25".
*Suggested fix:* write `\dirn{KeyOrder.lean}:151--158` with the line range outside `\dirn`, or use a single hyphen.

### M8. "Same text" in Remark oc:rem:copies (oc.tex:128-130)
Besides the type-variable binder of `iterate_mem`, the doc comment of `polar` also differs. OrbitConsistency.lean:111
reads "The point `c + r (cos θ, sin θ)`" and LayerLemma.lean:931 reads "The point at distance `r` from `c` …". The
claim concerns definitions, so this is cosmetic.
*Suggested fix:* "(up to the declaration of a type variable and one doc comment)".

### M9. Overloaded slash in Definition oc:def:keys(b) (oc.tex:694-697)
"J/N = ⌊J/N⌋" uses the same symbol for Lean's `Int.ediv` and for the rational quotient.
*Suggested fix:* "Lean's `J / N` (Int.ediv) equals ⌊J/N⌋, the floor of the rational quotient, …".

### M10. Slight overstatement in Remark oc:rem:keys-outside (oc.tex:825-826)
"For even m, the distinctness of the phases of distinct layers … is Theorem oc:thm:layers-phase." The theorem gives
incongruence mod 2π/m of the directions of points given in polar form. Turning that into ψ_i ≠ ψ_j needs the
decomposition θ = J·u + ψ, which the same remark lists as outside Lean.
*Suggested fix:* "follows from Theorem oc:thm:layers-phase once the phases are defined from polar forms".

### M11. Multiplicativity of the real image of sgn is used implicitly (oc.tex:289-290, 320-322)
Lemma oc:lem:perm passes from sgn(swap·f) = −sgn(f) in ℤˣ to the same identity for the real numbers. That needs the map
ℤˣ → ℤ → ℝ to be multiplicative, which is trivial: it is a composite of monoid homomorphisms. Fact oc:fact:sign states
only that the map is injective.
*Suggested fix:* add "and multiplicative" to the last sentence of Fact oc:fact:sign.

## Notes (no finding)
- Remark oc:rem:ray: the l ≠ 0 counterexample needs some admissible S with a point x ≠ c. Such S trivially exist, e.g.
  m = 2 and S = {x, 2c−x}, where general position holds vacuously. Acceptable as written.
- All Lean-faithfulness items requested by the task notes are handled correctly:
  - inversion parity not modelled in Lean (Remark oc:rem:parity, with a correct six-case bridge);
  - `toIcoMod` and half-open [a, a+p) exact (Definition oc:def:keys(a), Lemma oc:lem:toico, Remark oc:rem:halfopen);
  - 2π/0 = 0 for RotComp and encoder_literal_sound;
  - `m/2 : ℕ` in antipode_even.

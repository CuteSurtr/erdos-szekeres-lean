# Review of section `oc` (Orbit literals, rays and phases, key order), round 1, lens: adversarial

Verdict: **pass**. There is no blocker and no major finding; there are eight minor findings.

Files reviewed: `sections/oc.tex` (870 lines) and `sections/oc.map.tsv` (43 rows). I checked them against these files:
- `LEANEXT/orbit/OrbitConsistency.lean` (all 429 lines);
- `LEANEXT/merged/Merged.lean` (lines 1100-1385, and the copy claim for lines 1-1147);
- `LEANEXT/keys/KeyOrder.lean` (all 158 lines);
- the LAYERLEAN lines that the section cites (`LAYERLEAN/LayerLemma.lean:36-60, 105, 111, 231-308, 336, 364, 374-388, 460, 465, 582, 932`);
- `LEANEXT/README.md`, `LEANEXT/{orbit,merged,keys}/REPORT.md`, `LEANEXT/orbit/logs/{axioms,build,check_literals}.log`,
  `LEANEXT/orbit/check_literals.py`, `LEANEXT/merged/axioms.log`;
- `ENCBLEAN/logs/m4_build.log`, `ENCBLEAN/geo/ES8Geo/Orbit.lean`, `ENCBLEAN/DESIGN.md:618-630`, `C7UPPER/gen.py:60-125`,
  `C6UPPER/encb/gen_b2.py:40-110`;
- `ErdosSzekeres/{Definitions,Orientation,OrientationGeometry}.lean`;
- `inventory/LEANEXT.json`, and the `fd:`, `ll:` and `lg:` statements that the section cites (`sections/fd.tex`,
  `sections/ll.tex`, `sections/lg.tex`).

Paths are relative to the results root RES, except paths starting with `ErdosSzekeres/` (repository root) or with
`sections/`, `build/` or `inventory/` (staging area).

## Method

1. **Attack on every statement.** For each statement I looked for counterexamples among degenerate inputs:
   - m = 0 (where 2π/0 = 0 and `Even 0` holds), m = 1 and m = 2;
   - K ≤ 3 (the hypotheses are then vacuous), the empty set, coincident points and repeated labels;
   - c ∈ S, negative cell indices J and k;
   - ψ = 0 and ψ → u, J a multiple of N, and the right end of `toIcoMod`'s interval;
   - natural-number subtraction (`a = m-1`, `N-1-R`).

   I also checked each proof for hidden hypotheses (general position, distinctness, c ∉ S, injectivity, nonemptiness),
   for circularity, and for forward uses.
2. **Fidelity.** I compared every \leanref statement with the Lean source binder by binder: hypotheses, explicit and
   implicit order, `Finset` vs `Set`, strict vs weak inequalities, casts, `(m / 2 : ℕ)`, Euclidean `%` and `/`,
   `toIcoMod` argument order, and the direction of `t' = g ∘ t ∘ σ` and `C = r^[s] ∘ T₀ ∘ σ₂`. All of them match.
3. **Symbolic and exact checks.** `build/oc_r1adv_sympy.py` (sympy 1.13.3) ran 17,679 checks, and all passed:
   - rot-add (a), (b);
   - `orient_rotAbout_inv` as a *polynomial* identity in independent symbols C, S: LHS − RHS = orient·(S² + C² − 1);
   - `rotAbout_polar` and `polar_add_int`;
   - the same-ray identities (iv), y − x = (l−1)(x−c) and y − q = (l+1)(x−c);
   - the phase-nat ratio and the phase-int split;
   - all 6 ordered swaps and all 6 permutations of `orient3`, with the sign computed by cycle count (independent of
     inversions);
   - every row of the table in Remark `oc:rem:parity` (product convention (στ)(i) = σ(τ(i)), inversion count, sign);
   - `sortpar` (gen.py logic) and `perm_sign(order)` (gen_b2 logic) against the sign of the sorting permutation, on all
     orders;
   - the counterexample of Remark `oc:rem:layers` (3), in exact rationals:
     - invariance under the quarter-turn and c ∉ S;
     - general position over all 56 triples;
     - hv(S) = the outer points, peel(S,1) = hv(peel(S,1)) = the inner points, and S not in convex position;
     - polar(0, √2/2, π/4) = (½, ½);
   - 4,000 random exact-rational instances of `cell_lt_iff`, `cell_eq_iff`, `reduce_mod_two_pi` (with
     `toIcoMod` implemented exactly from its Mathlib definition) and `reduced_lt_iff_key`, including negative J;
   - `antipode_odd` for m = 1..8 and `antipode_even` for even m ≤ 8, for J ∈ [−20, 20], in exact units of π;
   - `encoder_literal_sound` on 300 exact instances with m ∈ {2, 4}, non-injective P, and repeated labels allowed.
4. **Negative controls.** `build/oc_r1adv_negctl.py` checks that these checks can fail:
   - a truncated (C-style) remainder in place of the Euclidean one fails `reduce` for negative J (1,547 failures);
   - using only sgn σ₁ in the encoder literal fails (241 failures);
   - the π/m variant fails on the Remark (3) instance.
5. **Records.** I re-checked the following, and all are correct:
   - the four SHA-256 prefixes and the line counts;
   - "Merged 1-1147 = LayerLemma 1-1147" (diff);
   - "Merged 1160-1311 vs OrbitConsistency 273-427 differ only in doc comments" (diff);
   - "Merged 1148-1383 = Capstone2 1156-1391" (diff);
   - the ENCBLEAN byte-identical copies (same digests);
   - the toolchain (`lean-toolchain` v4.24.0, Mathlib `f897ebcf…`, unchanged since 2026-10-04);
   - the 15 axiom lines and `exit=0` in `orbit/logs/axioms.log`, and the 6 lines of `merged/axioms.log`;
   - `ENCBLEAN/logs/m4_build.log:3-10`;
   - no `sorry`, `admit`, `axiom` or `native_decide`, and `decide` only at OrbitConsistency:236 and Merged:1125
     (`Even 6`, matching the argument order of `centre_not_mem_of_even`);
   - all cited LayerLemma lines, and `gen.py:108` and `gen_b2.py:56`;
   - 42,840 + 39,270 + 12,144 + 274,560 = 368,814 in `check_literals.log:1-5`;
   - `DESIGN.md:625, 626` and `keys/REPORT.md:22-25`;
   - `EncB.Geo.rotAbout_eq_orbitConsistency` at `ENCBLEAN/geo/ES8Geo/Orbit.lean:13`.
6. **Build and map.**
   - A private wrapper (`build/oc_r1adv_wrapper.tex`) compiles with `pdflatex`, two passes, exit 0. There are no
     errors and no overfull boxes; the only undefined references are to `fd:`, `ll:` and `lg:` export labels.
   - Every `\ref` is permitted, and there are no duplicate labels.
   - The map has one row per statement environment (43 of 43), with matching kinds.
   - There are no machine paths and no tool names.

## Main statements: why each survives

- **`oc:lem:rot-inv`.** This is a polynomial identity with no hypotheses. The determinant argument is correct, and so is
  the description of the Lean `linear_combination`.
- **`oc:lem:perm` (with `oc:lem:swap`).**
  - The three-case reduction for the swaps is complete.
  - The induction step t∘(swap·f) = (t∘swap)∘f uses Mathlib's product convention, which the section states correctly.
  - (S1)-(S4) are stated exactly as used.
- **`oc:thm:literal`.** The proof splits on sgn σ ∈ {±1}. The hypothesis `orient3 t ≠ 0` is used exactly in the
  converse of the case −1. For m = 0, RotComp(c,0) = {id} and the statement still holds; the section says so.
- **`oc:thm:encoder`.**
  - The semiconjugacy iterates correctly.
  - P∘C = ρ^[s]∘(P∘T)∘(σ₁σ₂) holds, and the order σ₁σ₂ (not σ₂σ₁) matches the Lean term `σ₁ * σ₂`.
  - For m = 0, ρ = id.
  - Exact tests found no failure, and the negative control fails.
- **`oc:lem:antipode`.** The lemma keeps the hypothesis `0 < m`. This matters: `Even 0` holds, and for m = 0 the
  conclusion is false (S = {p}, p ≠ c).
- **`oc:lem:same-ray`.**
  - c ∈ S is allowed, and the proof does not need c ∉ S: x = c forces y = x.
  - The proof uses only l + 1 ≠ 0.
  - Remark `oc:rem:ray`: the weakening to l ≠ 0 really fails (a regular m-gon about c, with y = 2c − x).
- **`oc:lem:phase-nat`, `oc:lem:phase-int`, `oc:thm:phase-orbit`.**
  - The identities are verified.
  - The Euclidean remainder is necessary for negative k (shown by the negative control).
  - r > 0 gives r'/r, and r' > 0 gives l > 0.
- **`oc:lem:disjoint` and `oc:lem:closed`.**
  - `oc:lem:disjoint` holds with no hypotheses.
  - `oc:lem:closed` uses ρ^[m] = id, which is valid for 0 < m, and a = m − 1 does not underflow.
  - (L1)-(L3) match `ll:lem:antitone`, `ll:lem:inv-peel` and `ll:thm:core-rot` (and their Lean sources) hypothesis by
    hypothesis.
  - The K-freeness of peel(S,i) follows from `fd:lem:mono`(c).
- **`oc:thm:layers-ray` and `oc:thm:layers-phase`.**
  - Every hypothesis of the lemmas used is discharged, including x' ≠ y via disjointness.
  - Remark `oc:rem:layers` (1) is correct and not circular: two distinct points of S give a point p ≠ c, and then
    `centre_not_mem_of_even` applies.
  - The example of Remark (3) is valid (verified exactly), so the modulus cannot be π/m.
- **`oc:lem:cell`, `oc:lem:rank`, `oc:lem:reduce`, `oc:lem:antipode-cell` and `oc:thm:key`.**
  - These hold at all boundary cases.
  - With ψ = u the statement fails, as Remark `oc:rem:halfopen` (1) says.
  - toIcoMod(0, 2π) = 0, as Remark (2) says.
  - (m/2 : ℕ) is used correctly in `antipode_even`.
  - In `antipode_odd`, J + m and 2m are formed in ℤ.

## Findings (all minor)

**m1 (minor). Intro item (B) is false for m = 0.** Location: `sections/oc.tex:16-19`.
- The text reads: "For even m, a finite set in general position that is mapped into itself by the rotation ρ by 2π/m
  about c contains the antipode 2c−x of each of its points, and no two of its points lie on one open ray from c".
- The section itself (line 108) uses Mathlib's `Even`, under which m = 0 is even and ρ = R_{c,0} = id. Then
  S = {p} with p ≠ c violates the antipode claim, and S = {c+v, c+2v} (general position holds vacuously) violates
  the ray claim.
- The formal statements (Lemmas `oc:lem:antipode` and `oc:lem:same-ray`) correctly carry 0 < m; only the summary
  omits it.
- Fix: write "For even m > 0" (or "even m ≥ 2").

**m2 (minor). "The labels need not be distinct" suggests a generality that does not exist.** Location: Theorem
`oc:thm:encoder`, `sections/oc.tex:386-387`.
- The hypothesis `orient3 (P∘T) ≠ 0` forces P(T 0), P(T 1), P(T 2) to be pairwise distinct (`fd:lem:orient`(e)), and
  hence the labels to be distinct.
- The sentence is true of the hypothesis list, but a reader may think the theorem says something about repeated
  labels.
- Fix: "Distinctness of the labels is not a separate hypothesis; it follows from `orient3(P∘T) ≠ 0`. P need not be
  injective".

**m3 (minor). The Python parity test is not independent evidence for agreement with Mathlib's sgn.** Location: Remark
`oc:rem:parity`, `sections/oc.tex:433-434`.
- `check_literals.py:25-39` compares `sortpar`'s bubble-sort parity with its own `perm_sign`, which is another
  inversion count. It never compares with a sign computed independently, so "agreement of sortpar with the
  permutation sign" overstates what was tested.
- The written six-case table is the real argument, and it is correct (verified).
- Fix: say "with an inversion count of the permutation (check_literals.py)".

**m4 (minor). The remark does not say which list each encoder counts inversions of.** Location: Remark
`oc:rem:parity`, `sections/oc.tex:405-414`.
- `gen.py` applies `sortpar` to the label triple, so the derivation inv(a) = inv(σ⁻¹) fits.
- `gen_b2.py:72-73` applies `perm_sign` to `order`, which is the sorting permutation itself
  (`order = sorted(range(3), key=...)`), not to the label list.
- The conclusion still holds: perm_sign(order) = (−1)^{inv(σ)} = sgn σ, directly from the table (checked). But the
  remark should state the argument for each encoder.
- Also, `\lean{sortpar}` and `\lean{perm_sign}` typeset Python functions with the Lean-name macro. This is a style
  issue, and it may suggest that they are Lean declarations.

**m5 (minor). Verbatim copies of section 13 are listed incompletely.** Location: Sources and Coverage (iv),
`sections/oc.tex:49-52, 867-868`.
- Section 13 of `Merged.lean` (lines 1148-1383) also appears verbatim as `LEANEXT/linked/Linked.lean:1148-1383` and
  `LEANEXT/capstone/Capstone.lean:1156-1391`; both checked with diff.
- Only `LEANEXT/capstone/Capstone2.lean` and `ENCBLEAN/geo/ES8Geo` are named.
- These files are outside the stated scope, so this is minor, but the list of verbatim duplicates should be
  complete.

**m6 (minor). The Dependencies paragraph is incomplete.** Location: `sections/oc.tex:88-97`. The section also
uses these labels, which the paragraph does not list:
- `fd:lem:affine-orient` (proof of Lemma `oc:lem:rot-inv`);
- `fd:lem:cp-hull` and `fd:lem:separation` (Remark `oc:rem:layers` (3));
- `ll:lem:minperiod` (proof of Lemma `oc:lem:closed`, in a parenthesis).

**m7 (minor). The evidence chain for two references to LAYERLEAN-located Lean names is not named.** Location: the
Rigor paragraph, `sections/oc.tex:80-81`.
- The paragraph reads: "Every statement below that carries a Lean reference is Lean-checked in the sense of the logs
  above."
- The references `ErdosSzekeres.LayerLemma.rotAbout_iterate` (`LAYERLEAN/LayerLemma.lean:465`) and
  `ErdosSzekeres.LayerLemma.iterate_mem` (`:52`) point into LAYERLEAN.
- Their axiom records are LAYERLEAN's own logs, or `LEANEXT/review/axioms.log`, none of which the paragraph names.
  (The Merged.lean copies of the same names are covered transitively by `merged/axioms.log`.)
- Fix: name the LAYERLEAN log, or refer to the `ll` section for these two.

**m8 (minor). Overloaded notation.** Location: Definition `oc:def:keys` (b), `sections/oc.tex:695`.
- "J/N = ⌊J/N⌋" uses "/" for integer division on the left and real division on the right.
- Fix: write `J / N` (Lean) $=\lfloor J/N\rfloor$ with the real quotient made explicit, or use $\operatorname{div}$.

## Not findings (checked, correct)

- Intro (C): N·u = 2π with u > 0 forces N > 0, so the summary is correct as written.
- Remark `oc:rem:copies`: the copied block has the same text as LayerLemma's declarations. LayerLemma has extra
  declarations (`crot_eq_self_iff`, `crot_injective`, `rotAff`), but the corresponding ones agree.
  `iterate_mem` differs only in the type-variable declaration (`omit [DecidableEq α] in`).
- "The new content starts at line 114" is accurate. Line 112 is the copied `polar`, and line 114 is the section
  header (a).
- The axioms reasoning for helpers that no theorem prints is sound: `#print axioms` collects the axioms of all
  dependencies. `PreservesOrient.iterate` is correctly reported as unused by every printed theorem.
- `DESIGN.md:625` does say that `encoder_literal_sound` is not used because of the sign versus inversion-count
  mismatch ("A 6-case bridge would be needed").
- `gen_b2.py:107` does compute `J = (2 * k + h[i]) % (2 * m)` (encoder B, J = 2k + h_i), as Remark
  `oc:rem:keys-outside` says.

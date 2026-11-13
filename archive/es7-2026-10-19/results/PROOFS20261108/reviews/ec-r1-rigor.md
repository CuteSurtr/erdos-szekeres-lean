# Review of section `ec` (Small corollaries for k = 7 and k = 8), round 1, lens: rigor

**Verdict: pass.** No blocker or major findings. Seven minor findings, listed below with their evidence.

Paths: `sections/`, `build/` and `reviews/` are relative to the staging area. Research files are relative to
`cloud/es7-2026-10-19/results` (RES). Nothing under the repository was modified, and Lean was not run.

## What was checked

1. **Statement fidelity.** I compared all 41 statement environments with their Lean declarations, hypothesis by
   hypothesis: `ES7Corollaries.lean` 1148-1233, `C6check.lean`, `PolarOrient.lean`, `PCompatCore.lean` and
   `L0Check.lean`, read in full. Every statement matches. Points checked:
   - quantifier order;
   - `Finset` vs `Set`: `part_a` is over an arbitrary `Set ℂ`, with no finiteness and no general position;
   - forward invariance (maps-into);
   - `S.erase c` and natural subtraction `m*(t-1)`;
   - the real numerals `2π/5` and `2π/4` against the ℕ-cast `2π/m` of `convexNGon_of_layers`; the bridge is stated in the
     Conventions paragraph;
   - `u ≠ 0` in `det_mul_eq` but `u > 0` in `orient_polar`;
   - `r o > 0` as the only hypothesis of `nested_regular_orient`;
   - the hypotheses (O), (R0) and (RD) of `exists_card0/1` and `exists_iff`;
   - `1 % m` in `Compat`; `1 ≤ m` in `classification`; `2 ≤ m` in `arith`, `L0` and `L0_rot`;
   - `Nat.FermatPsp` with natural subtraction;
   - `e`/`c` naming in `thr_m5` and `thr_m7`, and the absence of `e` in `thr_m4` and `thr_m6`.

   The case statements `Fivefold35` and `Fourfold32` are stated exactly as in the Lean file (RES
   `LEANEXT/es7corr/ES7Corollaries.lean:1157`, `:1164`). They appear as explicit hypotheses in all five theorems, and the
   statement heads say so.
2. **Lean references.** A script compared every `\leanref` with the source line. All 49 name/line pairs are exact: the
   named declaration starts on the cited line. All 41 environments appear in `sections/ec.map.tsv` with the same kind,
   names and lines.
3. **Proofs, step by step.** Every proof was checked as a referee would. Specific checks:
   - inequality directions: the strict-convexity contradiction in Lemma `ec:lem:sphere`, the thresholds, and
     `|S∖{c}| ≥ |S|-1`;
   - exhaustive case splits:
     - extreme-point Step 1 (`b=0`, `a=0`, `a,b>0`);
     - `pc-basic(b)` (`i<j`, `i=j`, `j<i`);
     - the orbit-removal step (`j=0` or `j≥1`);
     - parity (residues 0 and 1, plus the converse);
     - `classification` (even, odd with `m=1`, odd with `m≥3`);
     - `arith` (even, odd with `e≠1 ⇒ e=0`);
     - `L0` (`0∈S` or not);
     - `exists_iff (⇐)` (`N mod m = 0` or `= 1 mod m`, which forces `m>1`);
   - well-founded inductions: strong induction on `|T|`, and induction on `k` and `j` for the orbit membership;
   - hypotheses of every cited result:
     - (R) with `0<m`, `K≤2m`, `m(t-1)=30` or `28`;
     - (C) with `m=4` and a point `p≠c` from `|S|≥29>1`;
     - `Fact ec:fact:prim`, which needs `m≥1` at every use;
     - `Lemma ec:lem:zeta`, which needs `m≠0`;
     - `Lemma ec:lem:orbit8`, which needs `8≤m` and `p≠0`;
     - `Prop ec:prop:layered` applied to `λu` and `1/r`, both positive;
     - `Theorem ec:thm:compat(a)` for ℂ via Fact (iv).

   Nothing is delegated to Lean: each parenthetical about a Lean proof is extra to a complete written proof. The
   finite computation `ex341` is labelled computer-assisted, the kernel `decide` check is described correctly, and a
   hand computation is also given.
4. **Identities (sympy).** The script `build/ec_rigor_r1/check_identities.py` runs 34 checks, and all pass. They cover:
   - `|ax₁+bx₂|² = a|x₁|²+b|x₂|²-ab|x₁-x₂|²` when `a+b=1`, with `a-ab=a²` and `b-ab=b²`;
   - the 3×3 determinant expanded along the third column into the three-term form;
   - `x_a y_b - x_b y_a = sin(φ_b-φ_a)/(u_a u_b)`;
   - `D·u₁u₂u₃ = Σ` and each of its three terms;
   - `cross` expanded into the same three-term form, and `cross(pt,pt,pt)·u₁u₂u₃ = Σ`;
   - `cross(p,q,0) = x₁y₂-x₂y₁`, and `orient_centre`;
   - `pt(φ,λu) = pt(φ,u)/λ`, and `cross` homogeneous of degree 2;
   - `cos φ/(1/r) = r cos φ`, and the same for `sin`;
   - the coefficient sums of `coef` for all 8 coincidence patterns of `L(i)`, `L(j)`, `L(k)` with `t=2`;
   - Remark `ec:rem:polar`(ii): the LAYERLEAN radius form with `r=1/u`, multiplied by `u₁u₂u₃`, equals `Σ`;
   - the LAYERLEAN `orient_polar` formula itself;
   - `cross = orient`;
   - the complex form of `rotAbout`;
   - the half-turn `rotAbout(c,π)p = 2c-p`;
   - `(m/2)(2π/m) = π`.
5. **Arithmetic (exact integers).** The script `build/ec_rigor_r1/check_arith.py` checks the following, and all pass:
   - `thr_m4`-`thr_m7` for `t<200` and `e∈{0,1}`;
   - `m4_with_centre_counter`;
   - `1024 = 93·11+1 = 33·31+1 = 3·341+1` and `2^340 mod 341 = 1`;
   - `classification`, `compat_even` and `compat_odd` for all `m ≤ 20000`;
   - `arith` for `2 ≤ m ≤ 59`;
   - `64 = 7·9+1`;
   - five random numeric checks of the complex form of `rotAbout`.
6. **Records cited in the text.** Every item matches the record:
   - **Hashes.** The SHA-256 prefixes of the five files match the table. The prefixes in
     `LEANEXT/es7corr/REPORT.md` (`5883c8eb…`) and `PRIMEFOLD/README.md` (`ebc6aace…`, `05a67c3b…`) match.
     `ES8SYM/README.md:258-260` records `8c090168…` and `4d42e2fb…` and the four-comment-line statement; the section
     reports this mismatch honestly.
   - **Toolchain.** The repository pins are `leanprover/lean4:v4.24.0` and Mathlib `f897ebcf…` (lake manifest).
   - **Axiom logs.** All of them were read: es7corr `axioms.log`, `C6check.out`, `PolarOrient.out`, `PCompatCore.out`
     (where `ex341` uses only `propext`) and `L0Check.out`. `m4_with_centre_counter` has no axiom line.
   - **Forbidden tactics.** A grep of all five files finds no `sorry`, `native_decide`, `axiom` or `admit`, including
     lines 1-1147 of `ES7Corollaries.lean`.
   - **Duplicated prefix.** `diff` confirms that lines 1-1147 of `ES7Corollaries.lean` equal `LAYERLEAN/LayerLemma.lean`
     1-1147. The latter has 1148 lines, the last being `end`. `Invariant`, `rotAbout`, `centre_not_mem_of_even` and
     `convexNGon_of_layers` sit at 105, 298, 582 and 1066 in both files.
   - **SYMLEAN copies.** `SYMLEAN/SymmetricReduction.lean` has `Fivefold35` at 477 and `Fourfold32` at 496, in namespace
     `ErdosSzekeres.SymReduction`, with its own `Invariant` (271) and `rotAbout` (400).
   - **Mutant logs.** The failing `omega` calls are at the final steps (1189 and 1231).
   - **SYMMAX examples.** `c5_31points.txt` and `c4_28points.txt` exist.
   - **SYM5 and C4CUT.** The READMEs agree with Remark `ec:rem:cases`: proofs accepted by `cake_lpr`, six cuts with
     exact rational certificates.
   - **ES8SYM layers.md.** Lemma 1 is at lines 15-29, Lemma 2 at lines 31-43, and the general-position counterexample at
     lines 41-42.
   - **LAYERLEAN `orient_polar`.** It is at 935, in radius form, as Remark `ec:rem:polar`(ii) says. `p1.tex:380` and
     `k8_soundness.tex:449,480` use the radius form.
   - **PRIMEFOLD and the note.** `PRIMEFOLD/cluster/PROOFS.md` Lemma 0 excludes the centre by general position.
     `symmetric_es7.tex` `prop:C` and `lem:sizes`, and `symmetric_extremal.tex` `prop:compat`, read as the section says.
   - **ES8SLACK.** All four Lean files named in Coverage exist, and so does `ES8SLACK/proofs.md`.
7. **Mathlib definitions at the pinned commit** (`f897ebcf`, read with grep):
   - `Set.extremePoints` concludes only `x₁ = x`, exactly as the section defines it; the two-sided form is
     `mem_extremePoints`;
   - `openSegment` uses `0<a`, `0<b`, `a+b=1`;
   - `ConvexIndependent` and `convexIndependent_iff_notMem_convexHull_diff`;
   - `IsPrimitiveRoot`, with the fields `pow_eq_one` and `dvd_of_pow_eq_one`;
   - `IsPrimitiveRoot.ne_zero`, `.pow_inj`, `.pow_ne_one_of_pos_of_lt`, and `.norm'_eq_one` (in `RootsOfUnity/Complex`);
   - `Complex.isPrimitiveRoot_exp`;
   - `Nat.FermatPsp` (`ProbablePrime n b ∧ ¬n.Prime ∧ 1 < n`) and `Nat.ProbablePrime` (`n ∣ b^(n-1) - 1`);
   - `Nat.not_prime_mul`, which takes `a ≠ 1` and `b ≠ 1`, as the section says;
   - `Nat.dvd_prime_pow`;
   - `GroupWithZero`, which is Nontrivial, with `mul_inv_cancel` and `inv_zero`; the section's description is
     correct.
8. **LaTeX.** I compiled the section twice in `build/ec_rigor_r1/` with my own wrapper. Results:
   - pdflatex exits 0 both times;
   - the only undefined references are the allowed cross-section labels (`fd:`, `ll:`, `lg:`, `sr:`);
   - there are no duplicate labels, and all seven export labels are defined on the named statements;
   - there is no `\newcommand`, `\usepackage`, machine path or tool name.

## Findings (all minor)

**F1 (minor). The overview states the threshold arithmetic inaccurately** (`sections/ec.tex` line 13). The text reads
"Also the threshold arithmetic $65\le mt+e\iff t\ge17,13,11,10$ for $m=4,5,6,7$." The variable `e` is not defined
there. The natural reading, as elsewhere in the section, is `e = [c∈S] ≤ 1`, and under that reading the `m=4` instance
is false: `t=16`, `e=1` gives `65 ≤ 65` but `16 < 17`. This is the section's own Prop `ec:prop:thr`(v), the Lean
`m4_with_centre_counter`. Lean's `thr_m4` and `thr_m6` have no `e`. The formal statement (Prop `ec:prop:thr`) is
correct, so I rate this minor. I am unsure whether the orchestrator would treat it as an "ambiguous statement" (major);
it is an informal overview sentence, not a statement environment.

*Fix:* "$65\le4t\iff t\ge17$, $65\le5t+e\iff t\ge13$ $(e\le1)$, $65\le6t\iff t\ge11$, $65\le7t+e\iff t\ge10$ $(e\le1)$".

**F2 (minor). The overview drops finiteness** (lines 8-9). Item (1) reads "every set in general position that is invariant
under a rotation by 2π/5 and has at least 32 points". The Lean theorems are about finite sets (`Finset Point`), and an
infinite set also "has at least 32 points".

*Fix:* write "every finite set".

**F3 (minor). Remark `ec:rem:thr` omits a hypothesis of Lemma `lg:lem:centre`** (lines 396-398). It says the layer
results give "$c\notin S$ for even $m$ (Lemma `lg:lem:centre`)". That lemma (`centre_not_mem_of_even`) needs a point
`p∈S` with `p≠c`, and the claim is false for `S={c}`, which is invariant, in general position and 8-free. The remark
then applies the claim to `|S|≥65`, where the hypothesis holds, so the conclusion is unaffected.

*Fix:* add "(when $S\not\subseteq\{c\}$, e.g. $|S|\ge2$)".

**F4 (minor). Remark `ec:rem:cases` describes the trust base of SYM5 incompletely** (lines 105-106). The remark says
"Both results also rest on the written soundness argument for the encoder". `SYM5/README.md` §1 also relies on a
perturbation lemma: the centre may be assumed in general position with respect to S′, and the written proof of this is
in `C2ENC/perturbation.md`, recorded as refereed. The step from `Fivefold35`, whose `S` may have two points collinear
with `c`, to the CNF needs this lemma. The records label both written arguments "refereed".

*Fix:* name the perturbation lemma alongside the encoder soundness and give the records' label.

**F5 (minor). Remark `ec:rem:es7-sharp` skips the bridging step to the note's notion** (lines 193-198). The remark
identifies the Lean bounds with "$N(C_5)\le31$ and $N(C_4)\le28$" of `symmetric_es7.tex` `prop:C`. There, "symmetry
$C_s$" means invariance under some rotation of order $s$ about $c$; the Lean theorems use `rotAbout(c,2π/5)` and
`rotAbout(c,2π/4)` specifically. The bridge is easy: a rotation of order 5, resp. 4, has `rotAbout(c,2π/5)`, resp.
`rotAbout(c,2π/4)`, among its powers, and forward invariance passes to powers. It is not stated, and a one-line
remark would close it.

**F6 (minor). Remark `ec:rem:big-order` calls Lemma 2(a) the corollary itself** (lines 341-343). The remark says the
planar statement of `ES8SYM/proofs/layers.md` Lemma 2(a) "is the following corollary". layers.md assumes general
position (Notation, line 6), while Corollary `ec:cor:planar` does not. So the corollary implies Lemma 2(a) and is
slightly more general; "implies" or "is a strengthening of" would be exact.

**F7 (minor, style). Five overfull hboxes** appear in long statement heads: lines 602-603 (4-5 pt), 640-642, 645-646
(10.6 pt), 668-669 and 780-781 (30.8 pt, the head of Theorem `ec:thm:l0`). The output is readable; the last one is
visible in the PDF.

## Checked and found correct (inventory risks)

- `RefuteC6.part_a` is stated over ℂ for an arbitrary forward-invariant `Set`, with no finiteness and no general
  position. The planar link is a separate written step (Corollary `ec:cor:planar`) with a complete proof: the affine
  identification φ, `conv` commuting with affine maps, the convex-position transfer, and `φ(p)=0 ⇔ p=c`.
- `m4_with_centre_counter` is described correctly as arithmetic with no axiom line.
- C7 `orient_polar` is distinguished from the LAYERLEAN radius-form `orient_polar` (Lemma `lg:lem:polar`), and the two
  agree in substance; the identity was checked with sympy. `nested_regular_orient` is stated with `r>0` only (no
  nesting), as in Lean.
- `exists_iff` is stated with (R0) and (RD) as hypotheses, and the section says these are not discharged in Lean. The
  example `r_i = i+1` is a correct written step. Fermat's little theorem and existence in general position are
  explicitly marked as not formalized.
- `L0` excludes the centre for even `m` by parity, not by general position (Lemma `ec:lem:arith` and Remark
  `ec:rem:l0`). `Nat.FermatPsp` is defined correctly with natural subtraction.
- The wrong copied docstring of `Fourfold32` is flagged. The theorems of `ec:ssec:es7` are presented as conditional on
  `Fivefold35` and `Fourfold32`, and those propositions are distinguished from the SYMLEAN constants.
- Coverage lists every declaration in scope. It explains the omissions (the LayerLemma copy and the `#print axioms`
  lines) and names ES8SLACK as out of scope.

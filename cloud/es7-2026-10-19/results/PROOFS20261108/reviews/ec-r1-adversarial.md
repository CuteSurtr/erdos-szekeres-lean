# Review of section `ec` (Small corollaries for k = 7 and k = 8), round 1, lens: adversarial

**Verdict: pass.** No blocker or major finding. 9 minor findings are listed below.

Files reviewed: `sections/ec.tex` (851 lines) and `sections/ec.map.tsv` (41 rows). Paths below are relative to
`RES = cloud/es7-2026-10-19/results` unless they start with `sections/` or `build/`, which are relative to the staging area.

## What was checked

- **Statements against Lean.** Every statement with a `\leanref` was compared with its Lean source:
  - `LEANEXT/es7corr/ES7Corollaries.lean:1148-1233`;
  - `ES8SYM/lean/C6check.lean`;
  - `ES8SYM/lean/PolarOrient.lean`;
  - `PRIMEFOLD/compat/lean/PCompatCore.lean`;
  - `PRIMEFOLD/compat/lean/L0Check.lean`.

  The comparison covered hypotheses, conclusion, quantifier order, casts, `Finset` vs `Set`, and natural subtraction.
  All 41 statements match.
- **Cited results.** (R) = `convexNGon_of_layers` (`LAYERLEAN/LayerLemma.lean:1066`) and (C) = `centre_not_mem_of_even`
  (`:582`) are restated exactly as in Lean and as in `ll:thm:reduction` and `lg:lem:centre`.
- **The copy.** `diff` of lines 1-1147 of `ES7Corollaries.lean` against `LAYERLEAN/LayerLemma.lean` shows them
  identical; LayerLemma has 1148 lines. The line numbers 105, 298, 582, 1066 and 935 are right.
- **Mathlib definitions**, read from a local Mathlib source checkout at the pinned commit `f897ebcf`:
  - `Set.extremePoints` is `{x ∈ A | ∀ x₁ ∈ A, ∀ x₂ ∈ A, x ∈ openSegment x₁ x₂ → x₁ = x}`, exactly the section's
    definition. The Lean proof uses the equivalent `mem_extremePoints`, with the conjunction.
  - `ConvexIndependent`, `IsPrimitiveRoot` (`pow_eq_one`, `dvd_of_pow_eq_one`), and
    `Nat.FermatPsp n b = ProbablePrime n b ∧ ¬ n.Prime ∧ 1 < n` with `ProbablePrime n b = n ∣ b^(n-1) - 1`.
  - `Nat.not_prime_mul` takes `a ≠ 1`, `b ≠ 1`, as the section says.
  - `GroupWithZero` extends `Nontrivial`.
  - `Complex.isPrimitiveRoot_exp n (h0 : n ≠ 0)`.
  - `IsPrimitiveRoot.ne_zero`, `.norm'_eq_one`, `.pow_inj` and `.pow_ne_one_of_pos_of_lt` all exist.
- **Hashes.** SHA-256 of the five files: `5883c8ebac55…`, `92f15b5cc907…`, `6e54f5f83a19…`, `ebc6aacefadb…`,
  `05a67c3b8b16…`. All match the section's table. The README prefixes match where the section says they do
  (`LEANEXT/es7corr/REPORT.md:3`, `PRIMEFOLD/README.md:35,38`). `ES8SYM/README.md:258-260` records the compiled-file
  prefixes `8c090168`/`4d42e2fb`, and the section honestly says this could not be checked.
- **Axiom logs.** `LEANEXT/es7corr/axioms.log`, `ES8SYM/lean/C6check.out`, `ES8SYM/lean/PolarOrient.out`,
  `PRIMEFOLD/compat/lean/PCompatCore.out` (`ex341`: `[propext]` only) and `PRIMEFOLD/compat/lean/L0Check.out` agree with
  the Axioms paragraph.
  - Every covered declaration not in a log occurs in the statement or proof of a logged one. I checked each:
    - `sphere…` → `convexIndependent_of_norm_eq` → `orbit_convexIndependent` → `part_a`;
    - `det_mul_eq` → `orient_polar`;
    - `ngonPt_eq_pt` → `nested_regular_orient`;
    - `ne_zero_of_order`, `pow_inj_of_order`, `pow_mul_mem` → `dvd_card`;
    - `exists_card0/1` → `exists_iff`;
    - `arith`, `orbit_dvd`, `L0` → `L0_rot`.
  - The only exception is `m4_with_centre_counter`, as stated.
  - A text scan finds no `sorry`, `admit`, `axiom` or `native_decide` in the five files.
- **Record claims.** All of these were checked against their sources:
  - `mutant31.log` fails at line 1189 and `mutant28.log` at line 1231; both are the final `omega` lines.
  - `SYMLEAN/SymmetricReduction.lean:477,496`, namespace `ErdosSzekeres.SymReduction`.
  - `ES8SYM/proofs/layers.md` lines 15-29 (Lemma 1) and 41-42 (the general-position remark).
  - `PRIMEFOLD/cluster/PROOFS.md` Lemma 0, which excludes the centre by general position.
  - The `SYM5` and `C4CUT` READMEs (cake_lpr acceptance).
  - `SYMMAX/c5_31points.txt` and `c4_28points.txt` exist.
  - `WRITEUP/note/symmetric_es7.tex` `prop:C` (`:326`).
  - `WRITEUP/note/symmetric_extremal.tex` `prop:compat` (`:355`) and the "order ≥8" row (`:550`).
  - The radius-form `orient_polar` cited at `p1.tex:380` and `k8_soundness.tex:449`.
  - The four `ES8SLACK` Lean files and `ES8SLACK/proofs.md` exist.
- **Identities.** A short sympy script confirmed all of the following:
  - $D\,u_1u_2u_3=\Sigma$;
  - the third-column expansion;
  - cross = the three-term expression;
  - the centre identity;
  - the radius-form identity times $u_1u_2u_3$ equals $\Sigma$;
  - the norm identity $|ax_1+bx_2|^2=a|x_1|^2+b|x_2|^2-ab|x_1-x_2|^2$ for $a+b=1$;
  - $2^{340}\bmod 341=1$ and $1024=93\cdot11+1=33\cdot31+1=3\cdot341+1$.

  A brute-force check over $t<30$ confirmed `thr_m4`–`thr_m7`.
- **Map.** The map's 41 rows match the 41 statement environments in order, label and kind. Every `file_line` in the map
  is exact.
- **Compile.** The section compiles twice from `build/ec_adv_r1/` with exit 0. The only undefined references are the
  `fd:`, `ll:`, `lg:` and `sr:` export labels, and each of them is defined in its own section file. There are no other
  errors or warnings apart from 5 overfull boxes.
- **Forbidden content.** No machine paths or tool names appear. The section never uses the words
  "verified", "certified" or "proved".

## Attack log (main statements)

1. **The five ES(7) corollaries (`ec:thm:fivefold-erase`–`ec:thm:fourfold`).** They survive.
   - **Hypotheses.** Each states `Fivefold35`/`Fourfold32` as a hypothesis, and `ec:rem:cases` names `SYM5` and
     `C4CUT` with the computer-assisted label.
   - **Natural subtraction.** It is harmless: $5(7-1)=30$, $4(8-1)=28$, and $|S|-1\ge31$ needs no truncation since
     $|S|\ge32$.
   - **Casts.** Real-numeral $5$/$4$ versus $(m:\mathbb R)$ is addressed.
   - **Hypothesis order.** The order in the case classes differs from (R)'s premise (H), and the proof notes this.
   - **Fourfold centre.** The `fourfold_heptagon` proof obtains $p\ne c$ from $|S|\ge29>1$ before applying (C); without
     $p$, (C) would not apply.
   - **Degenerate inputs.** $c\in S$, $|S|$ not $\equiv0,1$ and $S\subseteq\{c\}$ are either excluded by the size
     hypotheses or make the statements vacuous.
   - **Orbit-counting remark (`ec:rem:orbits`).** Checked: $\rho$ is injective and fixes $c$, so $\rho(S')\subseteq S'$;
     orbits have size $m$ by `minimalPeriod_rotAbout`; and $m(t-1)<m\cdot\#\text{orbits}$ gives $\#\text{orbits}\ge t$.
2. **`ec:lem:sphere`, `ec:lem:ci-circle`.** They survive.
   - $r<0$ makes the hypothesis vacuous, and $r=0$ gives $x_1=x_2=0$.
   - An empty $\iota$ or a one-element $\iota$ is fine: $\operatorname{conv}\emptyset=\emptyset$.
   - In Step 1, the cases $a=0$ and $b=0$ are handled.
   - The extreme-point definition matches pinned Mathlib exactly.
3. **`ec:thm:big-order` (`part_a`).** It survives.
   - Over $\mathbb C$, `Set`, forward invariance only, no finiteness and no general position, as in Lean.
   - $S=\emptyset$ and $S=\{0\}$ satisfy the hypotheses and the conclusion.
   - $m=8$ exactly is fine: indices $j,k<8\le m$.
   - **`ec:cor:planar` (written step).**
     - $\varphi\circ\mathrm{rotAbout}(c,\theta)=e^{i\theta}\varphi$ matches the complex form of `fd:def:rot`.
     - The angles agree: the real $2\pi/m$ cast to $\mathbb C$ equals $2\pi i/(m:\mathbb C)$ after multiplication by $i$.
     - The passage between an injective convex-independent family and convex position of its image uses `fd:def:cp`'s
       "$T\subseteq S$, $x\in\operatorname{conv}T\Rightarrow x\in T$" form, and both directions are correct.
4. **`ec:prop:thr`.** The arithmetic is correct. The $m=4$ statement has no $e$, as in Lean. Item (v) is the
   counterexample to adding $e=1$; see finding 1 for the intro's inconsistency with this.
5. **PolarOrient (`ec:lem:det-mul`–`ec:lem:centre-u`, `ec:thm:nested`).** They survive.
   - The degenerate triples $i=j=k$ give 0 on both sides.
   - $L(i)=L(j)$ is handled: the coefficients add.
   - $t=0$ or $m=0$ (`Fin 0`) makes the statements vacuous.
   - $u_k<0$ is allowed in `det_mul_eq` (only $\ne0$), and the identity still holds.
   - `nested_regular_orient` is stated with only $r_o>0$. The section claims no nesting, radius order, distinctness or
     general position, and does not overclaim the arrangement statement of `layers.md:26`.
6. **PCompat (`ec:lem:pc-basic`, `ec:lem:pc-exist`, `ec:prop:parity`, `ec:thm:compat`, `ec:prop:ex341`).** They survive.
   - $m=1$ forces $\zeta=1$. Then (a) and (b) are trivial and (c) holds with injective $r$; the converse direction's
     "$N\bmod m=1\bmod m\Rightarrow m>1$" uses $N\bmod m\ne0$.
   - $t=0$ gives $S=\emptyset$, and $N=0$ is fine.
   - $m=0$ is excluded everywhere.
   - In the strong induction, the $j=0$ case $\zeta^{m-1}z=w$ uses $0<m$.
   - The `classification` cases are exhaustive: even $m\ge2$, $m=1$, odd $m\ge3$.
   - In `ex341`, the five `decide` claims plus `Nat.not_prime_mul` are described correctly, and the hand arithmetic is
     right.
   - (R0)/(RD) are discharged for $r_i=i+1$ in a written step.
   - Finite $K$ would make (RD) unsatisfiable, so `exists_iff` is vacuous there. That is not an error.
7. **L0Check (`ec:lem:arith`, `ec:lem:orbit-dvd`, `ec:thm:l0`).** They survive.
   - $m=2$ gives $0\notin S$ and $m=2^1$.
   - $m=3$ gives $0\in S$ and $m$ prime.
   - $m=9$ is vacuous, since no $t,e$ exist.
   - The phrase "$m$ is odd, $e=1$, and $m$ is prime or FermatPsp$(m,2)$" could be parsed as $(A\wedge B\wedge C)\vee D$,
     but under the hypotheses both parses are equivalent. FermatPsp$(m,2)$ with $mt+e=2^{m-1}$ forces $m$ odd, $e=1$
     and $0\in S$. So there is no real ambiguity.
   - Lemma `orbit-dvd` is derived from `ec:thm:compat`(a), which comes earlier in the section, so the argument is not
     circular.
   - Parity, not general position, excludes the centre for even $m$, as the Lean statement requires.

## Findings (all minor)

1. **minor — Intro, item (2), line 13.** The sentence reads "Also the threshold arithmetic $65\le mt+e\iff t\ge17,13,11,10$
   for $m=4,5,6,7$."
   - **Issue.** $e$ is undefined at this point. Read with $e\le1$ for every $m$, as in Prop. `ec:prop:thr`(ii),(iv),
     the $m=4$ case is false.
   - **Evidence.** For $t=16$, $e=1$: $65\le4\cdot16+1$ but $\neg(17\le16)$. This is exactly
     `m4_with_centre_counter`, which the section itself proves in item (v). The precise statements (`thr_m4` and
     `thr_m6` have no $e$) appear only in the proposition.
   - **Fix.** Write "$65\le mt+e\iff t\ge17,13,11,10$ for $m=4,5,6,7$, with $e=0$ for $m=4,6$ and $e\le1$ for $m=5,7$",
     or drop $e$ from the overview.
2. **minor — Remark `ec:rem:thr`, line 398.** The text says "and $e=0$ for $m=4,6$".
   - **Issue.** Lemma `lg:lem:centre` needs a point $p\in S$ with $p\ne c$. For $S=\{c\}$, $e=1$ with $m=4$.
   - **Context.** This is harmless where it is used ($|S|\ge65$), but stated unconditionally it is slightly imprecise.
   - **Fix.** Add "(when $S\not\subseteq\{c\}$, e.g. when $|S|\ge2$)".
3. **minor — Line 438.** The text says "For the next two lemmas let $D=\dots$, $\Sigma=\dots$".
   - **Issue.** $\Sigma$ is used in the next three lemmas (`det-mul`, `polar-u`, `polar-cross`) and in the proof of
     Prop. `ec:prop:layered`.
   - **Fix.** Write "For the rest of this subsection let …".
4. **minor — Coverage, lines 848-849.** The text calls "Fact `ec:fact:prim`, Corollary `ec:cor:planar` and the example
   in Remark `ec:rem:compat`(ii)" "written steps that are not in Lean".
   - **Issue.** Items (i)-(iv) of the Fact are Mathlib lemmas, which the Fact's own proof names. They are in Lean, just
     not project declarations.
   - **Fix.** Write "not project Lean declarations (the Fact restates Mathlib lemmas)".
5. **minor — Remark `ec:rem:cases`, lines 100-106.** The support chain of the case classes is described as SAT/LRAT
   plus "the written soundness argument for the encoder". It omits two further written or unwritten steps:
   - **`SYM5` §1 (`SYM5/README.md:40-44`).** The reduction to 35 points relies on a perturbation lemma (centre in
     general position with respect to $S'$), with its written proof in `C2ENC/perturbation.md`.
   - **`C4CUT` §1 (`C4CUT/README.md:29-32`).** The sector-unit step is one that "AUDIT3, A4-1, noted … was not written
     down".

   This does not affect any statement, since the theorems are correctly conditional, but the rigor description of the
   hypotheses is incomplete.
   - **Fix.** Add one clause naming these two steps.
6. **minor — Intro, item (1), line 9.** The text says "every set in general position …". The Lean objects are finite
   sets (`Finset`).
   - **Fix.** Write "every finite set …".
7. **minor — Line 587.** The gloss of Mathlib `CommGroupWithZero` ("a commutative monoid with zero in which $0\ne1$ and
   every $a\ne0$ has an inverse") omits the axiom $0^{-1}=0$. This is harmless.
   - **Fix.** Optionally add "(and $0^{-1}=0$ by convention)".
8. **minor (informational) — `\ref{sr:def:classes}`, lines 66 and 108.** This label is a forward reference: `sr`
   follows `ec` in `proofs.tex`.
   - **Allowed?** The contract allows it, since it is listed as an export label of section `sr`, and it is defined in
     `sections/sr.tex`.
   - **Uncertainty.** The task note for this section mentions only `ll:`, `lg:` and `fd:` export labels. I am not sure
     whether that note was meant as exhaustive, so I report it.
   - **Fix.** None needed if the contract governs; otherwise refer to `SYMLEAN/SymmetricReduction.lean:477,496` without
     a `\ref`.
9. **minor — Layout.** There are 5 overfull `\hbox` warnings, in the statement heads at source lines 602-603, 640-642,
   645-646, 668-669 and 780-781. The largest is 30.8pt, in the head of `ec:thm:l0`.
   - **Fix.** Optional: break the `\leanref` lists or shorten the heads.

## Not findings (checked and correct)

- Remark `ec:rem:es7-sharp` describes the mutant logs exactly. Both failures are at the final `omega`: lines 1189 and
  1231.
- The docstring correction for `Fourfold32` in `ec:rem:cases` is accurate. The docstring copied from SYMLEAN is wrong
  in this file, and the inventory flags this.
- `ec:rem:polar`(ii) correctly separates `C7.orient_polar` from the radius-form `orient_polar` (`LAYERLEAN:935`). The
  identity linking them is correct, as the sympy check confirms.
- `ec:rem:compat`(ii)-(iii) keeps the "core" qualifier: (R0)/(RD) are not discharged in Lean, Fermat's little theorem is
  not formalized, and existence in general position is not formalized.
- `ec:rem:l0` correctly records that the Lean statement excludes the centre by parity, while `PROOFS.md` Lemma 0 uses
  general position.

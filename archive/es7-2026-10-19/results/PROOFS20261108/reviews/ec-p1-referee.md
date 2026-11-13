# Section `ec`: polish round 1, independent referee report

Files read in full: `sections/ec.tex` (891 lines), `sections/ec.map.tsv` (41 rows). Lean sources read in full (paths
relative to `RES = cloud/es7-2026-10-19/results`): `LEANEXT/es7corr/ES7Corollaries.lean` lines 1148-1233 (and the
header), `ES8SYM/lean/C6check.lean`, `ES8SYM/lean/PolarOrient.lean`, `PRIMEFOLD/compat/lean/PCompatCore.lean`,
`PRIMEFOLD/compat/lean/L0Check.lean`, with their logs; the cited LAYERLEAN declarations (`Invariant` :105, `rotAbout`
:298, `minimalPeriod_rotAbout` :336, `centre_not_mem_of_even` :582, `orient_polar` :935, `convexNGon_of_layers` :1066);
`SYMLEAN/SymmetricReduction.lean` :271, :400, :477, :496; `ErdosSzekeres/Definitions.lean`. The earlier reports were read
only after this review had been formed.

## Verdict

**pass.** No blocker or major finding. Three minor findings (below).

## What was checked independently

- **Fidelity, all 49 `\leanref` pairs.** Every name and line matches the source (mechanical check of the map against
  the 41 statement environments: kinds, names and file:line columns identical). Every statement was compared with its
  Lean declaration by hand: hypotheses, conclusions, quantifier order, `Finset` vs `Set` (`part_a` is over an arbitrary
  `Set ℂ`), maps-into invariance, natural subtraction in `m * (t - 1)`, the casts `2π/m` (ℕ cast) vs `2π/5` (real
  numeral), `exp(2πi/m)` with `m` cast to ℂ and `m = 0` giving `ζ_0 = 1`, `Compat` with `1 % m`, `card_mod` with
  `[0 ∈ S] % m`, `Nat.FermatPsp` with natural subtraction, `thr_m5`/`thr_m7` with `c ≤ 1`. No discrepancy.
- **Mathlib definitions at the pinned revision `f897ebcf`** (the pinned copy in the project's main working copy):
  `Set.extremePoints` is defined with the single conclusion `x₁ = x` (as in the section; the two-sided form is the lemma
  `mem_extremePoints`); `ConvexIndependent`, `IsPrimitiveRoot`, `Nat.ProbablePrime`/`Nat.FermatPsp` as stated;
  `Nat.not_prime_mul` takes `a ≠ 1`, `b ≠ 1` (as the section says); `IsPrimitiveRoot.ne_zero`, `norm'_eq_one`,
  `pow_inj`, `pow_ne_one_of_pos_of_lt` exist (the last with `l ≠ 0`).
- **Identities (sympy 1.13.3, all pass):** the norm identity `|a x₁+b x₂|² = a|x₁|²+b|x₂|²−ab|x₁−x₂|²` for `a+b=1`;
  `det_mul_eq` (`D·u₁u₂u₃ = Σ`); the third-column expansion of `D`; the expansion of `cross`; `cross(p,q,r) =
  orient(p̂,q̂,r̂)`; the pair terms `x_a y_b − x_b y_a = sin(φ_b−φ_a)/(u_a u_b)`; the centre case; homogeneity of
  `cross`; the radius form of LAYERLEAN `orient_polar` and its relation to `Σ` with `r = 1/u` (Remark ec:rem:polar(ii));
  the complex form of `rotAbout` and the half-turn `rotAbout(c,π)p = 2c−p`; coinciding layers in Prop. ec:prop:layered.
- **Arithmetic (exhaustive):** the four threshold equivalences for `t < 200`, `e ≤ 1`; `m4_with_centre_counter`; all
  `ex341` numerals including `2^340 mod 341 = 1` and `1024 = 93·11+1 = 33·31+1 = 3·341+1`; the classification for
  `1 ≤ m < 3000`; `arith` for `2 ≤ m < 40`.
- **Proofs.** Every proof step was re-derived: strict convexity (Lemma ec:lem:sphere), extreme point ⇒ `A∖{x}` convex,
  orbit injectivity, `part_a`, the planar Corollary ec:cor:planar (affine bijection `φ`, `conv` commutes with affine
  maps, `U = g(s)`), the polar lemmas, the orbit induction of `dvd_card` (both cases `j = 0` and `j ≥ 1`), `card_mod`,
  `exists_card0/1`, `exists_iff` (including `m = 1`), `compat_even/odd`, `classification` (including `m = 1`), `arith`
  (parity for even `m`), `L0`, `L0_rot`. No gap, no circularity, no use of a cited fact beyond its statement.
- **Cross-section references.** `ll:thm:reduction`, `ll:thm:layers`, `ll:thm:card-peel`, `ll:lem:minperiod`,
  `lg:lem:centre`, `lg:lem:polar`, `sr:def:classes` and the `fd:def:*` labels say what ec uses them for (statements
  (R) and (C) match `ll.tex` and `lg.tex` and the Lean declarations exactly). All targets are allowed export labels.
- **Records.** Hash prefixes (all five recomputed), the `diff` of lines 1-1147 against `LAYERLEAN/LayerLemma.lean`, the
  axioms logs, `mutant31.log`/`mutant28.log` (errors at the final `omega`, lines 1189 and 1231), `ES8SYM/README.md`
  258-260, `ES8SYM/proofs/layers.md` lines 15-23, 25-29, 26-27, 37-43, `WRITEUP/note/symmetric_es7.tex` (`lem:sizes`,
  `prop:C`, `thm:E`), `WRITEUP/note/symmetric_extremal.tex` (`prop:compat`, the `order ≥ 8` row, line 550),
  `WRITEUP/P1/p1.tex:380` and `WRITEUP/note/k8_soundness.tex:449` (radius-form `orient_polar`), `SYM5/README.md`,
  `C4CUT/README.md` §0-§1, `C2ENC/perturbation.md` status line, `C2ENC/class_table.md`, `AUDIT3/findings.tsv`
  (A4-1, A4-3), `PRIMEFOLD/README.md`, `PRIMEFOLD/cluster/PROOFS.md` Lemma 0, `ES8SLACK/README.md` 153 and 402-404.
  All claims attributed to the records are accurate. The two SYMLEAN case classes are textually identical to the
  ES7Corollaries ones (checked with `diff`, together with `Invariant` and `rotAbout`).
- **Rigor vocabulary and hygiene.** No "verified/certified/proved"; hypotheses `Fivefold35`, `Fourfold32`, `hr0`,
  `hdisj` are presented as hypotheses everywhere; `ex341` is labelled computer-assisted with the kernel `decide`
  described; the records' word "refereed" is always attributed. No machine paths, no tool names, no macro definitions.
- **Compile.** `build/ec_p1ref_wrapper.tex`, two `nice -n 15 pdflatex` passes: exit 0, 0 overfull boxes, no errors;
  the only undefined references are `fd:`, `ll:`, `lg:`, `sr:` export labels.

## Findings

### F1 (minor). Remark ec:rem:cases cites lrat-check acceptance without the records' caveat on that checker

*Location.* `sections/ec.tex` lines 112-113 (Fivefold35: "both LRAT proofs were accepted by the checkers lrat-check and
cake\_lpr") and line 121 (Fourfold32: "its LRAT proof was accepted by lrat-check and cake\_lpr").

*Evidence.* The repository records that upstream lrat-check (drat-trim `2e3b2dc`) is unsound on the empty clause and
that only the patched build, or cake\_lpr, counts: `E2/README.md` §"lrat-check is unsound on the empty clause",
`LRATCHECK20261105/README.md` (title and lines 1-20), `ENCBLEAN/DESIGN.md:256` ("Only that line [cake\_lpr's `s VERIFIED
UNSAT`] certifies"). For Fourfold32 specifically, `AUDIT3` finding A4-5 (`AUDIT3/reports/A4_fivefold_layers.md`
lines 320-345) records that C4CUT does not say which lrat-check build produced its verdict and concludes that "the claim
is still carried by cake\_lpr". The remark lists the two checkers side by side, so a reader can count lrat-check as a
second, independent confirmation, which the records do not support. The statements themselves remain correctly
labelled as hypotheses; this is a completeness issue of the status remark only.

*Fix.* After "accepted by the checkers lrat-check and cake\_lpr" (line 113) add: "(the records rely on cake\_lpr's
verdict: upstream lrat-check is unsound on the empty clause, \dirn{E2} and \dirn{LRATCHECK20261105})"; after line 121
add: "\dirn{C4CUT} does not record which lrat-check build was used (\dirn{AUDIT3}, A4-5); the records rely on
cake\_lpr's verdict".

### F2 (minor). The gloss of Definition ec:def:compat is inaccurate

*Location.* `sections/ec.tex` lines 678-679: "(The form $1\bmod m$ makes the case $m=1$ work; ...)".

*Evidence.* The form `N % m = 1 % m` defines the same proposition as `N % m = 1` for every `m`: for `m = 1` the first
alternative `N % 1 = 0` always holds, for `m ≥ 2` we have `1 % m = 1`, and for `m = 0` Lean gives `1 % 0 = 1`
(exhaustive check for `0 ≤ m < 60`, `0 ≤ N < 400`: no difference). So the case `m = 1` "works" with either form, and
the sentence suggests a role the form does not have. Its actual role is that it matches the right side of
Theorem ec:thm:compat(b) (`card_mod`), so the forward direction of (c) reads off directly. No effect on correctness.

*Fix.* Replace the parenthetical by: "(Since $N\bmod1=0$, this is the same condition as $N\bmod m\in\{0,1\}$ for every
$m\ge1$; the form $1\bmod m$ matches the right side of Theorem~\ref{ec:thm:compat}(b). For $m=0$, Lean's convention
$N\bmod0=N$ applies, but $m=0$ is not used.)"

### F3 (minor). Remark ec:rem:big-order: the step from "rotation of order m" to rotAbout(c, 2π/m) is missing

*Location.* `sections/ec.tex` lines 370-373: the planar statement "(... the row ``order $\ge8$'', labelled
Lean-checked, of the $k=8$ tables in ES8SYM/README.md and WRITEUP/note/symmetric\_extremal.tex) follows from the
following corollary".

*Evidence.* Corollary ec:cor:planar is stated for invariance under $\mathrm{rotAbout}(c,2\pi/m)$. The table row of
`WRITEUP/note/symmetric_extremal.tex` (line 550) and its Proposition `prop:k8sizes`(a) (line 521) concern "$m$-fold
symmetric" sets, where `symmetric_extremal.tex:338` defines the setting as "Let $\rho$ be a rotation of order $m$ about
$O$", i.e. $\rho=\mathrm{rotAbout}(O,2\pi k/m)$ with $\gcd(k,m)=1$, not necessarily $k=1$. The corollary applies only
after replacing $\rho$ by the power $\rho^j=\mathrm{rotAbout}(O,2\pi/m)$ with $jk\equiv1\pmod m$. Round 1 added exactly
this step to Remark ec:rem:es7-sharp (lines 220-226) for $C_5$ and $C_4$, but not here. (For `ES8SYM/proofs/layers.md`
Lemma 2(a), whose setting is the rotation by $2\pi/m$, line 7, the corollary applies directly.) A competent reader can
fill the step from Remark ec:rem:es7-sharp.

*Fix.* At line 372 replace "follows from the following corollary" by "follows from the following corollary (for a
rotation of order $m$ that is not the rotation by $2\pi/m$, first pass to the power that is, as in
Remark~\ref{ec:rem:es7-sharp})".

## Notes (no change needed)

1. **The ES8SYM "four comment lines" claim is true.** Copies of the two compiled files with exactly the recorded
   hashes exist outside the repository checkout, in the project's main working copy under
   `.cache/es7/night-2026-11-01/mirror/scout/S1_es8_layers/` (`refute_C6/C6check.lean`, SHA-256 `8c0901681427…`;
   `refute_C7/PolarOrient.lean`, `4d42e2fbfca6…`). `diff` against the present copies shows exactly four changed lines,
   all inside comments or docstrings: `C6check.lean` line 7 (module docstring), `PolarOrient.lean` lines 9 and 13
   (module docstring) and 44 (docstring of `cross`). The original logs (`refute_C6/C6check.out`,
   `refute_C7/PolarOrient.log`) have the same axiom lines as `ES8SYM/lean/*.out`. Since these copies are not part of
   the repository, the section's hedge "we could not check this" (lines 45-47) is still the right wording for a reader
   of the repository; it is not a defect.
2. `LEANEXT/es7corr/ES7Corollaries.lean` has two sections headed "11" (line 929, the copied "angular rules", and line
   1148, the ES(7) corollaries). The section disambiguates by the line range at line 79; the Coverage item at line 853
   ("Section~11") does not repeat it, but lists the declarations, so there is no real ambiguity.
3. For the coordinator, not a defect of `ec`: the two compiled `ES8SLACK` Lean files (`review/C6_early_vertex/
   EarlyVertex.lean`, `review/C2_identity/Identity.lean`), which the inventory unit `ES8-small` lists, are not in the
   scope of any Stage-1 section (`ec` says so in its Coverage; no other section mentions them).
4. Remark ec:rem:thr (lines 427-429) derives $\card{S\setminus\{c\}}=mt$ from Theorems ll:thm:layers and
   ll:thm:card-peel in one sentence; at remark level this is adequate (each nonempty peel removes exactly one orbit of
   $m$ points), and the remark says this input is not part of the Lean file.

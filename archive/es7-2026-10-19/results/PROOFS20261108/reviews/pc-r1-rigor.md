# Review pc, round 1, lens: rigor (referee)

Section: `sections/pc.tex` (951 lines), map `sections/pc.map.tsv` (32 rows).
Lean sources: `LEANEXT/phase/PhaseClassification.lean`, `LEANEXT/linked/Linked.lean` 1385-1416,
`LEANEXT/capstone/Capstone.lean` 1966-2004, `LEANEXT/capstone/Capstone2.lean` 2004-2132 (paths relative to the
results directory).

**Verdict: PASS.** No blocker and no major finding. Seven minor findings are listed below.

## What was checked

1. **Every statement against its Lean declaration.** I compared hypotheses, conclusions and quantifier order
   for all 32 statement environments: Definitions pc:def:polar and pc:def:arc; Lemmas polar-facts (a)-(e),
   periodic, exists-polar, helpers (a)-(f), inarc, empty (a)-(f) and arc12; Theorems alternating, runB,
   trichotomy, rule-alt, rule-run (B, D, A), phase, sign, word and layers (a)-(e3); Propositions exactly-one,
   gaps, centre and halfplane; Corollary alt-polar.
   - All match exactly, including the hypotheses that are easy to get wrong:
     - the gap conditions (`α+2π−δ≠π` for B, `β−α≠π` for D, `δ−β≠π` for A);
     - which radii must be positive in each rule;
     - the order `¬H3 ∧ ¬H1` in RunMidA;
     - the `0<α−δ+2π` form in rule A;
     - `0 < r_b` in `orient_pos_of_layers`;
     - (P√) in the intrinsic versions;
     - the two implication blocks of `orient_sign_of_phase`;
     - for each statement, whether `LayerLemma.polar` or `PhaseClassification.polar` is the constant meant.
   - The integers `m` given in the proof of Lemma pc:lem:empty are the ones the Lean proofs use.
2. **Line numbers.** All 55 `\leanref` file:line pairs point exactly to the declaration line (script check).
   - The extra `\dirn{...:N}` citations are also exact: LayerLemma 932, 999 and 1012, Linked 932, 999 and 1012,
     Capstone2 940, 1007 and 1020.
   - The map has one row per environment, and every kind matches.
3. **Provenance claims in "Sources" and "Rigor and axioms".**
   - **Hashes and lengths.** All SHA-256 prefixes and line counts are correct.
   - **Copies.** I re-ran every copy relation with `diff`:
     - PhaseClassification 40-102 against LayerLemma 931-996: only docstrings differ;
     - Linked 1-1147 against LayerLemma 1-1147;
     - Linked 1-1384 against Merged 1-1384;
     - Capstone 19-1424 against Linked 11-1416; Capstone line 1425 is blank;
     - Capstone 1426-1965 against PhaseClassification 6-545;
     - Capstone2 1-2003 against Capstone 1-2003;
     - Capstone2 is byte-identical to `ENCBLEAN/geo/ES8Geo/Capstone2.lean` and listed in `SOURCES.sha256`.
   - **Axiom log.** `phase/logs/axioms.log` has exactly the 16 listed theorems, each with
     [propext, Classical.choice, Quot.sound].
   - **Transitive coverage.** The claim that every other declaration of the file is used by one of the 16 is
     true. I checked each declaration.
   - **Mutant log.** M7 in `phase/logs/mutants.log` says that `decide` proved the mutated proposition false.
   - **Build log.** `ENCBLEAN/logs/m4_build.log` shows only KeyOrder axiom messages.
   - **Text search.** The four files contain no `sorry`, `admit`, `axiom` declaration or `native_decide`. Among
     this section's declarations, `decide` occurs only in `word_dichotomy`.
   - **Toolchain pins.** Lean 4.24.0 and Mathlib f897ebcf.
   - **ENCBLEAN dependency chain** (checked by grep):
     - `exists_layer_polar` uses `exists_angle`, `sqrt_dist2_pos` and `ne_of_mem`; `labelling_of_counterexample`
       calls it, and `sixfold66_of_no_model` calls that;
     - `labelling_ruleA` and `labelling_ruleB` use `orient_pos_of_alternating` and `orient_pos_of_runMidB`;
       `modelOfLabelling` calls them;
     - the axioms are pinned in `Audit.lean` 30-70.
   - **REPORT citations.** The quotes from `phase/REPORT.md` ("Not in Lean", item 2) and `capstone/REPORT.md`
     (open issues) are accurate.
4. **Identities (sympy 1.13.3, script `build/pc_r1rigor_sympy.py`, Part 1).** All pass:
   - **Polar formula (a)** and its pieces:
     - the bracket expansion `[v−u,w−u]=[u,v]+[v,w]+[w,u]` and `orient(u,v,w)=[v−u,w−u]`;
     - translation invariance;
     - `[u,v]=r_a r_b sin(β−α)` and its two cyclic analogues.
   - **Part (b)**, both directly and as (a) at `r_d=0`.
   - **Parts (c) and (d):** `sin(α−δ)=sin(α−δ+2π)` and `sin x+sin y−sin(x+y)=sin x(1−cos y)+sin y(1−cos x)`.
   - **Part (e):** the decomposition `O = r_a(r_b−r_d)sin x + r_d(r_b−r_a)sin y + r_a r_d(sin x+sin y−sin(x+y))`.
   - **Orientation symmetries:** the cyclic and swap identities used in rule-run (D), (A) and sign (ii).
   - **Polar forms:**
     - 2π-periodicity for integer k;
     - the arccos construction of `exists_polar` (both sign cases, 300 exact-rational samples);
     - `dist2(c,polar(c,r,θ))=r²`;
     - the half-plane identity `r cosθ cosφ + r sinθ sinφ = r cos(θ−φ)`;
     - `r²−r'²=(r−r')(r+r')`.
5. **All linear-inequality steps.** I checked 42 implications by exact Fourier-Motzkin elimination over ℚ,
   with strictness tracked. All inequalities are homogeneous in (α,β,δ,π), so π is scaled to 1. Script
   `build/pc_r1rigor_fm.py`. All pass:
   - every inequality, with the stated `m`, in Lemma empty (a)-(f), and its intermediate claims;
   - the three cases of Lemma arc12 with the stated witnesses `k`;
   - both directions of Theorem alternating;
   - all non-memberships of Proposition exactly-one;
   - Theorem runB (⇒);
   - all 8 sign patterns of Proposition gaps, plus "two gaps > π is impossible";
   - pairwise exclusivity of the gap disjuncts (Remark gaps (2));
   - the five cases of Remark runs;
   - the relabelled orderings in rule-run (D) and (A);
   - `|θ−φ|<π/2` in Proposition halfplane.

   Four negative controls are correctly rejected: a non-implied inequality, the boundary `≤` versus `<`, a
   wrong `m`, and a wrong `k`.
6. **Exact randomized tests of the written statements as transcribed** (`build/pc_r1rigor_exact.py`).
   - **Exact predicates.** I implemented `inArc` exactly over ℚ (cross-checked against brute force over k).
     On 6000 sorted triples with 1633 boundary cases (some gap = π), the following hold:
     - Lemma shift (a)-(d), including for unordered triples;
     - Lemma empty and Lemma arc12;
     - Theorem alternating (including at gap = π) and Remark alt-boundary;
     - Proposition exactly-one;
     - Theorem runB under the gap hypothesis, and its failure at δ−α=π (Remark runB-example);
     - Proposition gaps;
     - the counterexample (0,π,3π/2) of Remark gaps (1), and Remark gaps (2);
     - Theorem trichotomy (i) and (ii);
     - Remark runs: H1∨H2∨H3 always, and exactly one pattern under genericity.
   - **Float tests** of rules A, B, D and A, of phase, and of sign (i) and (ii) as transcribed (about 15,000
     qualifying samples) show no violation.
   - **Words.** Of the 64 words, exactly 8 satisfy the premise. The 8-row table (words and run positions) is
     correct. PPAPPA violates the premise and is neither alternating nor has a run.
7. **Proof-by-proof referee pass.** Every case split is exhaustive:
   - `k≥m` / `k≤m−1`;
   - `u1≥0` / `u1<0`;
   - β−α against π (three cases);
   - the number of gaps above π (0, 1, or at least 2);
   - the four disjuncts of the trichotomy;
   - the five positions of α+π;
   - the 8 words.

   Further checks:
   - **Induction.** The one induction (`peel(S,n)⊆S`) is well founded.
   - **Uses of earlier results.** Every use meets its hypotheses exactly, including the cross-section uses of
     lg:thm:radius (stated in `lg.tex` with the same hypotheses) and lg:lem:ruleB.
   - **No circularity.** helpers (d) needs exists-polar, and (e) needs (d) and (b).
   - **Standard facts** are stated correctly: arccos/sin, monotonicity of cos, toIcoMod (T1)/(T2) and
     `⌊(θ−α)/2π⌋`.
   - **Nothing is delegated to Lean.** Remarks of the form "the Lean proof does ..." are commentary only.
8. **Contract checks.**
   - It compiles twice with exit 0 (wrapper `build/pc_r1rigor_wrapper.tex`). The only undefined references are
     the expected fd:/ll:/lg: labels.
   - Every `\ref` target is an allowed label, and all 10 export labels are defined on the right statements.
   - There are no `\newcommand`, no machine paths and no tool names.
   - The Coverage paragraph is present and complete: every declaration of PhaseClassification.lean and all new
     declarations of Linked, Capstone and Capstone2 are covered.
   - The NOTES are respected:
     - phase_trichotomy is stated exactly as the conjunction of the disjunction and "Alternating ⇒ no run";
     - mutual exclusion of runs is proved separately and labelled as not Lean-checked;
     - the gap = π boundary is treated in Remarks alt-boundary, runB-example and gaps (1).

Tooling note for later rounds: in this sympy version, `sympy.solvers.simplex.lpmax` returned points that violate
its own constraints on two 4-variable systems (for example, the arc12 case-1 system; its reported optimum broke
`a−b+1≤0`). I therefore used exact Fourier-Motzkin for all linear checks. Do not rely on `lpmax` verdicts here.

## Findings

### F1 (minor): "How Lean checks it" describes the evaluation inaccurately
- Location: `sections/pc.tex:742-748`.
- The text says the evaluation "runs through all 64 functions s and, for each, evaluates the premise (six
  equalities ...), the alternation condition (six equalities ...) and the existence of a cyclic run (six
  triples)".
- The decidability instance of an implication is lazy: if the premise evaluates to false, the conclusion is not
  evaluated. The `∀ i : Fin 6` and `∃ i` checks also stop early.
- So the conclusion is evaluated only for the 8 words that satisfy the premise, not for all 64. What is decided
  (premise ⇒ (i) ∧ (ii) for each of the 64 functions) is stated correctly. Only the account of the evaluation
  is off.
- Suggested fix: "the kernel evaluates, for each of the 64 functions, the Boolean value of 'premise ⇒ (i) ∧
  (ii)'; the conclusion is evaluated only when the premise holds (8 functions)".

### F2 (minor): unrecorded computer cross-check inside the hand proof
- Location: `sections/pc.tex:778-779`.
- The proof headed "Written proof (by hand)" ends with "As a cross-check, the table was also confirmed by a
  computer enumeration of all 64 functions while this text was prepared."
- No record of this enumeration is cited, and a reader cannot check it. The table is correct (I re-verified
  it), so this is about documentation only.
- Suggested fix: delete the sentence, or move it out of the proof with a pointer to a recorded check.

### F3 (minor): "proved by hand here" wording
- Location: `sections/pc.tex:19-20` (intro bullet for Theorem pc:thm:word).
- Contract rule 8 asks not to call anything "proved" beyond "Lean-checked" and "written proofs (not
  refereed)".
- Suggested fix: "computer-assisted in Lean; a written proof by hand is given here".

### F4 (minor): the PPAPPA example reads as if it came from the mutant log
- Location: `sections/pc.tex:748-751`.
- "The mutation log ... (mutant M7) records that `decide` refutes the statement when the premise is dropped;
  for example, the word PPAPPA ... is neither alternating nor contains a cyclic PPP."
- The log records only that `decide` proved the mutated proposition false. It gives no witness. PPAPPA is the
  writer's own (correct) example.
- Suggested fix: "... records that `decide` reports the mutated statement false; indeed the word PPAPPA ...".

### F5 (minor): "by shifting the witness k by ±1" is incomplete
- Location: `sections/pc.tex:334-336`, the closing paragraph of Lemma pc:lem:shift.
- The Lean `hrun'` proofs also keep the witness unchanged for several disjuncts:
  - `LEANEXT/phase/PhaseClassification.lean` lines 327-328 and 332-333 (D);
  - lines 351, 360 and 362 (A).
- In (d), the second conjunct combines the antipode shift (k+1) with the start shift (k−1), which nets 0.
- Suggested fix: "by shifting the witness k by −1, 0 or +1, as above".

### F6 (minor): overfull boxes in the statement heads
- The compile log reports:
  - 11.7pt at source lines 131-132;
  - 5.8pt at 419-420;
  - up to 59pt at 816-818 (the head of Theorem pc:thm:layers with seven `\leanref`s visibly runs into the
    right margin on page 10 of the standalone PDF);
  - 42pt at 893-898.
- These are cosmetic.
- Suggested fix: allow breaks inside long Lean names (needs a preamble-level change; ask the coordinator), or
  move some references into the text after the head.

### F7 (minor, wording): the "final theorems" parenthetical is ambiguous
- Location: `sections/pc.tex:72-75`.
- "... in the proofs of the final theorems of the ENCBLEAN geometric package (`ENCBLEAN/geo/ES8Geo/Labelling.lean`
  and `ENCBLEAN/geo/ES8Geo/ArcBridge.lean`)" reads as if the final theorems were in those two files.
- They are in `Main.lean` (e.g. `sixfold66_of_no_model`, `sixfold_es8`). The two files are where the lemmas are
  used, inside `exists_layer_polar`, `labelling_ruleA/B` and `P_eq_polar`.
- I verified that the claim itself is correct.
- Suggested fix: "used in `Labelling.lean` and `ArcBridge.lean`, in the proofs of the final theorems (in
  `Main.lean`), whose axioms are pinned ...".

## Evidence files (staging area)
- `build/pc_r1rigor_sympy.py`: identity checks (Part 1). Its LP part uses `lpmax`, which is unreliable (see the
  tooling note).
- `build/pc_r1rigor_fm.py`: the same checks, with exact Fourier-Motzkin for every linear step. All OK.
- `build/pc_r1rigor_exact.py` and `build/pc_r1rigor_exact.out`: exact randomized tests, negative controls, the
  word table and float tests of the rules. 97 lines OK, no FAIL.
- `build/pc_r1rigor_wrapper.tex` and `.log`: compile check, two passes, exit 0.

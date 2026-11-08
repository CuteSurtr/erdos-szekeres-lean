# Review of section `pc` (Phase patterns and angular rules), round 1, lens: adversarial

Verdict: **PASS**. There are no blocker or major findings, and 7 minor ones (listed below).

## What was attacked and how

1. **Fidelity, every statement against its Lean declaration.** I read every declaration of
   `LEANEXT/phase/PhaseClassification.lean` (all 545 lines), `LEANEXT/linked/Linked.lean:1385-1416`,
   `LEANEXT/capstone/Capstone.lean:1966-2004` and `LEANEXT/capstone/Capstone2.lean:2004-2132`. I compared each one
   with its statement in `sections/pc.tex`. That covers 39 PhaseClassification declarations (7 definitions and 32
   theorems), 2 Linked declarations, 3 Capstone declarations and 9 Capstone2 declarations. For each I checked:
   - every hypothesis, including strict vs weak inequalities and the gap conditions `≠ π`;
   - which point is the hull vertex and the direction of the layer-index inequalities;
   - which radius is not assumed positive;
   - the relabelled radius implications in `orient_sign_of_phase` (ii) (Lean lines 510-520);
   - the conjunction structure of `phase_trichotomy`;
   - `Set` vs `Finset` (the `halfplane_of_runMidB` point set and the `S : Finset` of the layer theorems);
   - `polar` vs `LayerLemma.polar`, and the `dist2` constant used.

   I found no mismatch. All file:line citations are exact, and every one is the first occurrence.
2. **Proofs, step by step.** I re-derived every inequality chain:
   - the 18 lift checks in the arc-emptiness lemmas (the integers m agree with Lean's `not_inArc 0/1/-1`);
   - the 3 cases of `arc12_nonempty`;
   - both directions of `alternating_iff_gaps_lt_pi` and of `runMidB_iff`;
   - the relabellings (β, δ, α+2π) and (δ, α+2π, β+2π) used for rules D and A, including the new gap
     `α'+2π−δ' = β−α` (resp. `δ−β`), the radius permutation and `orient_cycle`;
   - the bilinear identity in (a) and the rule-B decomposition in (e) of Lemma `pc:lem:polar-facts`;
   - the arccos construction in `exists_polar`;
   - the case analyses in the written-only remarks (`pc:rem:gaps` (1),(2) and `pc:rem:runs`).

   I found no gap, no circularity and no forward use. The forward references (Prop. `pc:prop:halfplane` in
   `pc:rem:runB-example`, Lemma `pc:lem:helpers`(a) before the lemma) are comparisons only, not proof steps.
3. **Exact brute force with boundary values.** I used a short exact-arithmetic script of my own, which is not a
   deliverable. Angles are rational
   multiples of π. α ranges over {0, 1/7, −5/3}·π, and β, δ over α + (j/24)·π for j = 0..47, which includes every
   case where a gap equals π. On the 3243 ordered triples I tested:
   - Thm `pc:thm:alternating`, Thm `pc:thm:runB` (given g₃ ≠ π), and Lemmas `pc:lem:empty` (a)-(f) and
     `pc:lem:arc12`;
   - the remark that `RunMidB` together with δ−α ≥ π forces δ−α = π;
   - `pc:rem:runs` (H₁∨H₂∨H₃ under the ordering alone);
   - exactly one pattern holds under genericity, and never more than one without it;
   - `gap_classification` and the mutual exclusivity of its disjuncts;
   - `alternating_exactly_one`.

   On all 6912 triples, ordered or not, I also tested Lemma `pc:lem:shift` (c),(d), both directions. The
   counterexample (0, π, 3π/2) of `pc:rem:gaps`(1) and the example (0, π/2, π) of `pc:rem:runB-example` were
   confirmed. Result: **0 failures**.
4. **Random float test of the orientation statements as transcribed.** This used a second short script of my own.
   I used 200000 random
   configurations with arbitrary real angles in [−20, 20]. The results:

   | Statement | Instances | Violations |
   |---|---|---|
   | polar formula | 200000 | 0 |
   | `orient_sign_of_phase` (i) | 49954 | 0 |
   | `orient_sign_of_phase` (ii), with the section's relabelled radius implications | 49385 | 0 |
   | rules B (middle radius not assumed positive) | 8299 | 0 |
   | rules D | 8436 | 0 |
   | rules A | 8337 | 0 |
5. **Degenerate inputs.**
   - m = 0 is excluded by (L), so 2π/m never occurs with m = 0.
   - K = 0 makes (L) unsatisfiable, since `HasConvexNGon 0 S` always holds. The theorem is then vacuous, not false.
   - c ∈ S is excluded by (L).
   - Coincident points a = b or a = d contradict 0 < β−α, 0 < δ−β, δ−α < π (resp. the ordering
     α < β < δ < α+2π). This was checked for each layer theorem.
   - β′ = δ′ is disclosed as not covered (`pc:rem:sign-scope`).
   - A gap equal to π is handled correctly in every statement. In particular `runMidB_iff` (⇒) needs g₃ ≠ π, and
     the section's example shows this. The trichotomy is stated with genericity, as in Lean, and the section does
     not claim that genericity is needed for it.
6. **Records and claims about Lean.**
   - The line counts and SHA-256 prefixes of all 10 cited files match `shasum`.
   - The `diff` relations stated in the Sources paragraph hold:
     - PC 40-102 = LayerLemma 931-996 up to docstrings;
     - Linked 1-1147 = LayerLemma;
     - Linked 1-1384 = Merged;
     - Capstone 19-1424 = Linked 11-1416;
     - Capstone 1426-1965 = PC 6-545;
     - Capstone2 1-2003 = Capstone;
     - Capstone2 = ENCBLEAN copy (`cmp`).
   - The offsets +1420 and +8 are right.
   - `phase/logs/axioms.log` has the 16 named theorems with the 3 standard axioms. I checked that every other
     PhaseClassification declaration is used by one of them.
   - `mutants.log` M7 is the decide refutation with the premise replaced by `True`.
   - The ENCBLEAN uses are at Labelling.lean:63-65, :133 and ArcBridge.lean:155-156, :464, :481. They are reachable
     from `labelling_of_counterexample` and `modelOfLabelling`, which are pinned at Audit.lean:46, :49.
   - In `m4_build.log` only the KeyOrder messages appear.
   - The toolchain is v4.24.0 and Mathlib is f897ebcf, as in the repository's `lake-manifest`.
   - A grep finds no `sorry`, `admit`, `axiom` or `native_decide`. `decide` occurs only in `word_dichotomy` and in
     an unrelated `Even 6` side goal of a test in the LayerLemma copy.
7. **Form.**
   - The compile check (`build/pc_r1adv_wrapper.tex`, two passes) exits 0. The only undefined refs are to allowed
     `fd:`/`ll:`/`lg:` export labels.
   - All 10 export labels are defined on the right statements.
   - The map has 32 rows for 32 statement environments, and its Lean names and file:line entries agree with the
     heads.
   - No machine path or tool name appears in the tex or the map.

## Findings (all minor)

### F1 (minor): the description of what `decide` evaluates is slightly inaccurate
- **Location:** pc.tex:745-748 ("How Lean checks it").
- **Issue:** The text says the evaluation runs through all 64 functions and, for each, "evaluates the premise (six
  equalities), the alternation condition (six equalities) and the existence of a cyclic run (six triples)". That is
  not quite what happens:
  - The `Decidable (p → q)` instance evaluates q only when p holds, that is, for the 8 words satisfying the
    premise.
  - The bounded ∀ and ∃ over `Fin 6` stop at the first index that decides them.
  - `decide` first evaluates in the elaborator. The kernel then re-checks `of_decide_eq_true (Eq.refl true)`.
- **Severity note:** The logical content is correct. I'm unsure whether the contract's "state precisely what is
  checked" requires this level of detail, so I report it as minor.
- **Suggested fix:** "The decision procedure enumerates the 64 functions; for each it evaluates the premise and, for
  the 8 functions satisfying it, the two parts of the conclusion; the kernel re-checks this evaluation when it
  type-checks the proof term."

### F2 (minor): a process claim the reader cannot check
- **Location:** pc.tex:778-779.
- **Issue:** "As a cross-check, the table was also confirmed by a computer enumeration of all 64 functions while
  this text was prepared." No artifact in the repository records such an enumeration.
- **Suggested fix:** Delete the sentence, or replace it with a pointer to the Lean `decide` check, which is exactly
  such an enumeration.

### F3 (minor): the scope remark misdescribes part (a)
- **Location:** pc.tex:906-909 (Remark `pc:rem:layers-scope`).
- **Issue:** The remark says that in Theorem `pc:thm:layers` "the strict order α<β<δ<α+2π ..., the gap condition
  ≠π and the pattern are hypotheses". For part (a) (`orient_pos_of_layers`) this is wrong:
  - its angular hypotheses are 0<β−α, 0<δ−β and δ−α<π;
  - it has no bound δ<α+2π, no gap condition and no pattern.
- **Suggested fix:** "in (b)–(e) ...; in (a) the hypotheses are 0<β−α, 0<δ−β, δ−α<π."

### F4 (minor): the reading remark assumes six distinct points
- **Location:** pc.tex:271-274 (Remark `pc:rem:reading`).
- **Issue:** The reading "RunMidB is a cyclic run PPP whose middle point is β" assumes the six points are distinct,
  that is, no gap equals π. Without genericity there is no six-letter word. For example, (0, π/2, π) satisfies
  `RunMidB`, but δ = π coincides with the antipode α+π. The section does treat the boundary correctly elsewhere
  (`pc:rem:alt-boundary`, `pc:rem:runB-example`).
- **Suggested fix:** Add "when no gap equals π (so the six points are distinct)" to the PAPAPA/PPP reading.

### F5 (minor): the polar constant is left implicit in three statements
- **Location:** pc.tex:184-212 (Lemmas `pc:lem:periodic`, `pc:lem:exists-polar`) and pc.tex:690-704 (Thm
  `pc:thm:sign`).
- **Issue:** These statements don't name the constant behind `polar` (it is `PhaseClassification.polar`). The
  default from Definition `pc:def:polar` and Lemma `pc:lem:helpers`(a) make this harmless. However, the inventory
  asks that each theorem be stated with the constant its Lean statement uses.
- **Severity note:** I'm unsure whether the section-wide convention is enough. I report it only as minor.

### F6 (minor): imprecise wording about where the ENCBLEAN final theorems are
- **Location:** pc.tex:72-74.
- **Issue:** The text says "the final theorems of the ENCBLEAN geometric package (`Labelling.lean` and
  `ArcBridge.lean`)", but the pinned final theorems are mostly in `Main.lean` and `ModelOfLabelling.lean`. The
  listed helpers are *used in* `Labelling.lean` and `ArcBridge.lean`, inside declarations reachable from the pinned
  `labelling_of_counterexample` and `modelOfLabelling` (Audit.lean:46, :49). The transitive-coverage claim itself
  is correct.
- **Suggested fix:** "... are used in `Labelling.lean` and `ArcBridge.lean`, in proofs that feed the final theorems
  whose axioms are pinned ...".

### F7 (minor): overfull lines in statement heads
- **Location:**

  | Statement | pc.tex line | Overflow |
  |---|---|---|
  | Theorem `pc:thm:layers` | 815-818 | up to 59 pt |
  | Corollary `pc:cor:alt-polar` | 892-898 | 42 pt |
  | Lemma `pc:lem:polar-facts` | 130-131 | 11.7 pt |
  | Theorem `pc:thm:alternating` | 418-420 | 5.8 pt |
- **Issue:** Overfull hboxes in the statement heads. The rendered page 10 stays inside the paper margin, so this is
  layout only.

## Statements that survived (summary)

Every main statement survives:
- `inArc`/`not_inArc` and the six emptiness lemmas, with the right lift integers m;
- `arc12_nonempty`;
- `alternating_iff_gaps_lt_pi`, which holds with no genericity hypothesis; a gap equal to π gives non-alternation;
- `alternating_exactly_one`;
- `runMidB_iff`, with its example (0, π/2, π);
- `gap_classification`, stated as only a disjunction; exclusivity is proved separately, and the counterexample
  without genericity is (0, π, 3π/2);
- `phase_trichotomy`, stated exactly as the conjunction of the disjunction and Alternating ⇒ no run; the mutual
  exclusion of runs is a separate, correct written observation;
- rules A, B, D and A-middle, with the middle radius not assumed positive;
- `orient_pos_of_phase`, `centre_inside_of_alternating` and `halfplane_of_runMidB`;
- `exists_polar` and the periodicity lemmas;
- `orient_sign_of_phase`, including the relabelled radius conditions in (ii);
- `word_dichotomy`, which is labelled computer-assisted and has a genuine 8-word hand proof;
- the seven layer theorems, with the hull vertex and index inequalities exactly as in Lean, and positivity of the
  intrinsic radii from c ∉ S;
- the helper lemmas.

# pc, round 1, lens: claims, labels and LaTeX

Verdict: **pass** (no blocker, no major finding; 8 minor findings below).

Paths: Lean sources and records are relative to the results directory `cloud/es7-2026-10-19/results` (RES);
section, map and build files are relative to the staging directory (STAGE).

## Compile check

- `build/claims-pc-r1/`: `pc_wrapper.tex` compiled twice with `nice -n 15 pdflatex -interaction=nonstopmode
  -halt-on-error -output-directory=claims-pc-r1`. Both passes exit 0, 12 pages, no `!` errors, no "Missing $".
- Undefined references (unique): `fd:def:inv`, `fd:def:ngon`, `fd:def:orient`, `fd:def:point`, `fd:def:rot`,
  `fd:lem:orient`, `ll:def:hv`, `ll:def:peel`, `lg:def:polar`, `lg:lem:polar`, `lg:lem:ruleA`, `lg:lem:ruleB`,
  `lg:lem:sinadd`, `lg:thm:radius`. All 14 are fd: labels or export labels of `ll`/`lg` listed in the contract. Each is
  defined in `sections/fd.tex`, `ll.tex` or `lg.tex`, on a statement of the kind the text names (Definition, Lemma or
  Theorem). The PDF text has 30 `??`, matching the 30 `\ref`s to fd/ll/lg; all own references resolve.
- Overfull boxes: see finding 6.

## What was checked (all OK unless a finding is listed)

1. **Machine paths and tool names.** I searched `pc.tex` and `pc.map.tsv` for `/private`, `/Users`, `/home`,
   `/tmp`, `~/` and for tool names (case-insensitive). No hits. There are no `\usepackage`,
   `\newcommand` or `\def` lines, and no `\begin{document}`. The first line is `\section{...}\label{pc:sec}`.
2. **Paths.** Every `\dirn{...}` path exists relative to RES, or relative to the repository root for
   `cloud/es7-2026-10-19/results`. Bare file names (`Capstone.lean` etc.) are used only after their full path has been
   given.
3. **SHA-256 prefixes, recomputed with `shasum -a 256`:** PhaseClassification.lean `490efcd0a7e4`, Linked.lean
   `f1e18c119276`, Capstone.lean `dc382395ca55`, Capstone2.lean `f8c3930c2427`, LayerLemma.lean `afb8542dceb0`,
   Merged.lean `245b7d65407a`, Audit.lean `39f214bbf30b`, Labelling.lean `489ba89f8d6f`, ArcBridge.lean
   `46966b48a101`. All match. `ENCBLEAN/geo/ES8Geo/Capstone2.lean` has the same full hash as
   `LEANEXT/capstone/Capstone2.lean`, and `ENCBLEAN/geo/SOURCES.sha256` lists it.
   Line counts (545, 1416, 2004, 2132) match `wc -l`.
4. **Copy relations, checked with diff.**
   - Phase 40–102 vs LayerLemma 931–996: only the 5 docstrings differ.
   - Linked 1–1147 = LayerLemma 1–1147. Linked 1–1384 = Merged 1–1384; Merged 1385 is `end ErdosSzekeres.LayerLemma`.
   - Capstone 19–1424 = Linked 11–1416. Capstone 1425 is blank. Capstone 1426–1965 = Phase 6–545.
   - Capstone2 1–2003 = Capstone 1–2003. Capstone 2004 is `end ErdosSzekeres.Capstone`; Capstone2 2004 is blank.
   - The 18-line header and the offsets +1420 and +8 are correct.
5. **Every `\leanref` line number** (54 references) points at the declaration line of the named constant. The
   namespaces are correct: `PhaseClassification` is top level (Phase:36), `ErdosSzekeres.LayerLemma` (Linked
   1385–1416, section `Link`), `ErdosSzekeres.Capstone` (Capstone:1969, Capstone2 to 2132). Cited repeats are
   correct: polar at Linked:932 and Capstone2:940, dist2 at :999 and :1007, dist2_le_of_later at :1012 and :1020.
6. **Axioms log.** `LEANEXT/phase/logs/axioms.log` has exactly the 16 theorems listed in pc.tex:59–63, each with
   `[propext, Classical.choice, Quot.sound]`, including `word_dichotomy`. Each of the other PhaseClassification
   declarations is used in the statement or proof of one of the 16, so the transitivity argument (pc.tex:64–66)
   holds.
   - There is no axiom output for the new Linked/Capstone/Capstone2 declarations anywhere in RES (grep). The two
     REPORTs state the three axioms and clean builds (linked/REPORT.md:14–15; capstone/REPORT.md:5–7, 28–29).
   - The ENCBLEAN uses claimed at pc.tex:69–75 all exist:
     - Labelling.lean:63–65: `Capstone.ne_of_mem`, `Capstone.exists_angle`, `Capstone.sqrt_dist2_pos`;
     - Labelling.lean:133: `dist2_polar`;
     - ArcBridge.lean:155–156: `PhaseClassification.polar_add_int_two_pi`, `Capstone.polar_eq`;
     - ArcBridge.lean:464, 481: `orient_pos_of_alternating`, `orient_pos_of_runMidB`.
   - `polar_zero` is used in the proof of `sqrt_dist2_pos` (Capstone2:2070).
   - The dependency chain reaches the pinned theorems: P_eq_polar → arcFrame → labelling_ruleA/B → modelOfLabelling;
     exists_layer_polar → labelling_of_counterexample.
   - Audit.lean:31–70 has the 14 `#guard_msgs in #print axioms` lines, and `logs/m8_build.log` and
     `logs/m8_fix_build.log` show `Built ES8Geo.Audit` and "Build completed successfully".
   - `ENCBLEAN/logs/m4_build.log` has exactly one module with messages (KeyOrder, 8 axiom lines), then "Build
     completed successfully". DESIGN.md (M4 row) confirms that this build includes the Capstone2 copy.
7. **Text search** of the four Lean files: no `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`,
   `implemented_by`, `extern`, `unsafe` or `opaque`. `decide` occurs in `word_dichotomy` and at Linked:1125 (=
   Capstone:1133), which is outside this section's declarations. The claim at pc.tex:79–81 is correct.
8. **Pins.** The repository `lean-toolchain` is `v4.24.0` and the lake-manifest has Mathlib rev `f897ebcf…`; ENCBLEAN
   geo pins the same. LEANEXT/README.md:6 says the files compile with `lake env lean` from the repository root.
9. **Cited records.**
   - `LEANEXT/phase/REPORT.md` "Not in Lean" item 2 is the sorted-word item, as cited.
   - `LEANEXT/capstone/REPORT.md` "Open issues" says orient_sign_of_phase is not wired in, as cited.
   - `mutants.log` line 7 is M7. `mutants.py` replaces the premise by `True`, and the log reads "Tactic `decide`
     proved that the proposition" (see finding 8).
10. **Computer-assisted labelling.**
    - Theorem pc:thm:word is labelled computer-assisted in its head, in the intro bullet and in the map row.
    - The text says the check is `decide` with kernel evaluation, that no `native_decide` and no `Lean.ofReduceBool`
      enter, and that the three standard axioms appear in the log. All correct.
    - A full hand proof is given. I re-enumerated the 64 words: 8 satisfy the premise, the dichotomy holds for all of
      them, and the table rows and run positions are correct. PPAPPA is neither alternating nor has a cyclic PPP.
11. **Hypotheses as hypotheses.**
    - No SAT verdict, Sixfold66/Sevenfold70 or case class appears in this section.
    - In the layer theorems, the polar forms, sorted directions, gap ≠ π and the pattern are stated as hypotheses
      (Remark pc:rem:layers-scope).
    - The task notes are met: phase_trichotomy is stated as disjunction (i) plus implication (ii). Remark pc:rem:runs
      says that mutual exclusion of the runs is not in Lean. The boundary gap = π is handled in pc:rem:alt-boundary,
      pc:rem:runB-example and pc:rem:gaps(1). I checked those examples, (0,π/2,π) and (0,π,3π/2).
12. **Labels.**
    - All 34 labels start with `pc:` and are unique.
    - All 10 export labels are defined on the named statements: pc:def:arc, pc:thm:alternating, pc:thm:runB,
      pc:thm:trichotomy, pc:thm:rule-alt, pc:thm:rule-run (B, D, A), pc:thm:phase, pc:thm:sign, pc:thm:word,
      pc:thm:layers (orient_pos_of_layers plus the six Capstone layer rules).
13. **Map TSV.**
    - The header is correct and there are 32 rows for 32 statement environments, in the same order.
    - Labels and kinds match. Lean names and file:line lists match the `\leanref`s exactly (scripted comparison).
    - Written step and remarks have `-`.
14. **Coverage.**
    - All 39 declarations of PhaseClassification.lean are listed.
    - Linked's new declarations are dist2_polar and orient_pos_of_layers.
    - Capstone's are orient_pos_of_layers_runMidB, orient_pos_of_alternating_polar and polar_eq.
    - Capstone2's are runMidD, runMidA, polar_zero, exists_angle, sqrt_dist2_pos, ne_of_mem and the three
      `_intrinsic` theorems.
    - The statements of the Linked/Capstone theorems match the Lean text, including the `{α β δ}` placement, the
      `LayerLemma.polar` vs `PhaseClassification.polar` usage and the hull-vertex/layer-index hypotheses.

## Findings (all minor)

1. **minor. pc.tex:745–747 ("How Lean checks it").** The sentence "The evaluation runs through all 64 functions s
   and, for each, evaluates the premise (six equalities), the alternation condition (six equalities) and the
   existence of a cyclic run (six triples)" over-describes the evaluation.
   - The `Decidable` instance of an implication tests the premise first. So the conclusion (both conjuncts) is
     evaluated only for the 8 functions that satisfy the premise.
   - The ∀/∃ instances over `Fin 6` stop at the first failure or witness.
   - What is enumerated (64 functions), what is checked (premise → conclusion) and how (kernel evaluation of
     `decide`) are stated correctly.
   - Suggested fix: "for each s it evaluates the premise; for the 8 functions satisfying it, it evaluates the
     conclusion."
   - I am confident of the premise-first behaviour of the implication instance. The exact short-circuiting inside the
     list-based ∀/∃ instances is my reading of the instances and was not checked here, since Lean may not be run.
2. **minor. pc.tex:778–779.** "As a cross-check, the table was also confirmed by a computer enumeration of all 64
   functions while this text was prepared." This is an unrecorded process claim that a reader cannot check, and it
   is not needed because the hand proof is complete. (I re-enumerated, and the table is correct.) Suggest deleting
   the sentence or citing a record.
3. **minor. pc.tex:785–788 (Remark pc:rem:word-scope).** The remark says that "a cyclic PPP in it is RunMidA, RunMidB
   or RunMidD of the middle point, is not proved in Lean". That is true inside LEANEXT, which is what the cited
   phase/REPORT.md, dated 4 Nov, covers. It is out of date for encoder B:
   - `ENCBLEAN/geo/ES8Geo/ArcBridge.lean`, `arcFrame` (line 393), proves in Lean that encoder B's three
     `EncB.ArcHasAntipode` tests on sorted keys are the `PhaseClassification.arcHasAntipode` tests of the arcs of the
     true directions α<β<δ<α+2π.
   - `labelling_ruleB` (lines 473–487) turns the encoder's run test (`BlockCCW`) into `RunMidB` and applies
     `orient_pos_of_runMidB`. ENCBLEAN/DESIGN.md row 9 says G9 "turns 'sorted word' into inArc facts".
   - The first half of the sentence (the sorted word, as a `Fin 6 → Bool` word, satisfies s(i+3)=¬s(i)) is still not
     in Lean anywhere.
   - Suggested fix: scope it ("is not proved in LEANEXT") and add that, for encoder B, ENCBLEAN's arc bridge
     (ArcBridge.lean, `arcFrame`) proves the corresponding link without `word_dichotomy`.
   - I am unsure whether the writer meant "in LEANEXT". It understates Lean coverage rather than overclaiming, hence
     minor.
4. **minor. pc.tex:72–75.** "in the proofs of the final theorems of the ENCBLEAN geometric package (Labelling.lean
   and ArcBridge.lean)" reads as if the final theorems were in those two files.
   - The pinned theorems are mostly in `Main.lean` and `ModelOfLabelling.lean`; only `labelling_of_counterexample` is
     in Labelling.lean. The two named files are where the uses occur.
   - Suggested fix: "are used in Labelling.lean (exists_layer_polar, labelling_of_counterexample) and ArcBridge.lean
     (P_eq_polar, arcFrame, labelling_ruleA/B), on which the final theorems pinned in Audit.lean:31–70 depend."
5. **minor. Map TSV notes: paths not relative to RES.**
   - Row `pc:def:polar`: "linked/Linked.lean:999 and capstone/Capstone2.lean:1007".
   - Rows `pc:lem:polar-facts`, `pc:lem:periodic` and `pc:lem:exists-polar`: "phase/logs/axioms.log".
   - Row `pc:rem:word-scope`: "phase/REPORT.md".
   - Prefix each with `LEANEXT/`, as in the file_line column and in pc.tex.
6. **minor. LaTeX layout: overfull boxes.**
   - 58.97pt three times and 6.5pt and 1.2pt once each, in the head of Theorem pc:thm:layers (source lines 815–818,
     the long `_intrinsic` names).
   - 42.1pt in the head of Corollary pc:cor:alt-polar (892).
   - 11.7pt in the head of Lemma pc:lem:polar-facts (130).
   - 5.8pt in the head of Theorem pc:thm:alternating (418).
   - Rendered pages 10–11 show the theorem-head lines running into the right margin.
   - Suggested fix: shorten the head (for example keep one `\leanref` in the optional argument and move the other
     references into the first sentence of the statement), so that the long names can wrap.
7. **minor (wording). pc.tex:20.** The phrase "proved by hand here" uses "proved" for the written proof. The contract
   prefers the label "written proof (not refereed)". Suggested wording: "with a written proof here".
8. **minor. pc.tex:749–751.**
   - The mutation-log line for M7 is truncated by `mutants.py` (`[:110]`) after "Tactic `decide` proved that the
     proposition". So "records that decide refutes the statement" relies on the standard continuation "… is false"
     of this Lean message. That is a reasonable reading.
   - The example PPAPPA is the writer's own; the log does not contain it, but the sentence reads as if it did.
   - Suggested fix: "(for example, PPAPPA, checked by hand, is …)".

No other discrepancies were found between the claims of the section and the Lean sources, logs and records.

# Section `oc`, whole-document review round 1 (docfix-r1): re-check

Lens: recheck. Verdict: **pass**. No blocker, major or minor finding remains, and the fix introduces none.

Inputs: the fix log `reviews/docfix-oc-r1-fix.md`; the pre-edit snapshot `snapshots/docfix-r1-pre/oc.tex` (SHA-256
`4be86aff99b9`, 938 lines) and `snapshots/docfix-r1-pre/oc.map.tsv` (`5278bd649da2`, 44 lines); the current
`sections/oc.tex` (`093dc95716f6`, 944 lines) and `sections/oc.map.tsv` (`5278bd649da2`, byte-identical to the
snapshot). Paths are relative to the stage directory or, for Lean files, to the results directory. The hashes were taken
again at the end of the re-check and had not changed.

## 1. The two findings

| # | finding | severity | fixer's action | re-check |
|---|---|---|---|---|
| 1 | [xref-ocpcec F1] oc writes the map R_{c,θ} and the matrix M_θ, citing Definition `fd:def:rot` (which writes ρ_{c,θ}). fd writes R_θ for the matrix, so the pointer to Lemma `fd:lem:affine-orient` in the proof of Lemma `oc:lem:rot-inv` meets "the linear part R_θ of ρ_{o,θ}" | minor | note added to Definition `oc:def:basic`(b) (oc.tex:144-148); pointer annotated (oc.tex:242-244) | **resolved correctly** |
| 2 | [consistency m6] R_{c,θ} (map) in oc vs R_θ (matrix) in fd and lg; oc's matrix is M_θ | minor | same note, with the sentence "In this section R_{c,θ} always denotes the map, never a matrix" (the reviewer's second option) | **resolved correctly** |

Each claim in the new text was checked against the current sources:
- "Definition `fd:def:rot` ... write[s] ρ_{c,θ} for the map": fd.tex:381-385 defines the map
  ρ_{c,θ} = rotAbout c θ with the same coordinate formula as oc.tex:140-141. True.
- "the layer-lemma section write[s] ρ_{c,θ} for the map": ll.tex:397-401 (Definition `ll:def:rot`) does, and ll
  writes ρ = ρ_{c,2π/m} throughout (e.g. ll.tex:451, 473, 518). So "our ρ is their ρ_{c,2π/m}" is exact, since oc
  sets ρ = R_{c,2π/m} (oc.tex:144). True.
- "the foundations and layer-geometry sections write R_θ for the matrix M_θ, for instance in Lemma
  `fd:lem:affine-orient`": fd.tex:405 (Lemma `fd:lem:rot`) and fd.tex:546-548 and 568-569 (Lemma
  `fd:lem:affine-orient`(i) and its proof) write R_θ for the matrix with rows (cos θ, −sin θ) and (sin θ, cos θ).
  lg.tex:144-148 writes the same matrix as R_θ. Both equal oc's M_θ (oc.tex:142-143). The note correctly says nothing
  about ll's matrix name A_θ. True.
- "In this section R_{c,θ} always denotes the map, never a matrix": all 64 occurrences of R_{c,·} in oc.tex (forms
  R_{c,θ}, R_{c,2π/m}, R_{c,α}, R_{c,π}, R_{c,0}, R_{c,ku}, ...) are values or iterates of the map of Definition
  `oc:def:basic`(b). R_{o,θ} (once, oc.tex:243) is the same map with centre o. R_θ occurs only twice (oc.tex:146 and
  244), both times inside the new notes and attributed to the other sections. True. (A bare R also appears, at
  oc.tex:824-828, as a natural-number remainder local to a proof. It has no subscript and is not covered by the claim.)
- Proof of Lemma `oc:lem:rot-inv`: "the case det = 1 of Lemma `fd:lem:affine-orient`, item (i), which writes the map
  R_{o,θ} as ρ_{o,θ} and the matrix M_θ as R_θ". fd's items use `label=(\roman*)` (fd.tex:545), so "item (i)"
  exists. It is headed "(rotations have determinant 1)", has centre o and uses ρ_{o,θ} and R_θ (fd.tex:546-548). Its
  head cites the same Lean theorem `ErdosSzekeres.OrbitConsistency.orient_rotAbout_inv` (fd.tex:534). True. The
  pointer is a comparison only: oc proves the lemma directly, and fd proves (i) from `fd:lem:rot`(b) without using
  oc, so there is no circularity.

The decision not to rename (R_{c,θ} to ρ_{c,θ} and M_θ to R_θ) is right. Both reviewers accepted a note: finding 1
proposes exactly this clause, and finding 2 offers it as its second option. The fd-side fix that the round still has
to apply (doc-r1-xref-fdlllg F1 and consistency m5) proposes naming oc's variant, "R_{c,θ} with matrix M_θ", in fd's
notation paragraph, and a rename here would contradict that text. No other section uses R_{c,·}: counts over all 12
section files show R_{c,·} only in oc, R_θ in fd and lg, ρ_{c,·} in fd, ll, oc (inside the note) and sa, and A_θ in ll.
So keeping oc's symbols affects no cross-reference. fd.tex is byte-identical to its round snapshot (`5b710c687001`).
The round's edits to ll.tex and lg.tex do not touch any rotation notation (a grep of their diff lines for ρ, R_θ, A_θ,
M_θ, R_{c and rotAbout(c finds nothing), so every claim of the note still holds now.

## 2. Diff review (`diff -u` snapshot vs current)

`oc.map.tsv`: no difference (diff exit 0). This is correct: no statement environment, Lean name, file:line or note
changed, so the appendix map needs no regeneration for oc.

`oc.tex`: three hunks.
1. **@@ -108,8 +108,9 @@ (Dependencies paragraph).** The new text says that Lemma `fd:lem:affine-orient` "is cited
   only in a note on notation in Definition `oc:def:basic`(b) and in a parenthetical comparison in the proof of
   Lemma `oc:lem:rot-inv`". The label occurs exactly three times in oc.tex: line 111 (this sentence), 147 (the note)
   and 242 (the proof). True. The sentence parses and renders correctly ("... Definition 1.1(b) ... Lemma 1.7, and the
   example in Remark 1.34 uses ...").
2. **@@ -140,7 +141,11 @@ (Definition `oc:def:basic`(b)).** A parenthetical note on notation only. The definition
   text (the display, the matrix form, "it turns counterclockwise", ρ = R_{c,2π/m}) is unchanged and still matches
   Lean (see section 3). All claims are checked in section 1. The note refers to ll and lg in words. That is right:
   `ll:sec` and `lg:sec` are not export labels, and the wording matches oc's existing Dependencies paragraph ("the
   layer-lemma section", "the layer-geometry section", "the foundations section").
3. **@@ -234,8 +239,9 @@ (proof of Lemma `oc:lem:rot-inv`).** The parenthetical gains "item (i), which writes the
   map R_{o,θ} as ρ_{o,θ} and the matrix M_θ as R_θ". It is checked in section 1. The proof itself is unchanged.
   The computation was re-checked with sympy (`build/oc_recheck_r1_rotinv.py`): R_{c,θ}(p) = c + M_θ(p − c) as
   polynomials; det M_θ = cos²θ + sin²θ; and orient(R a, R b, R d) − orient(a,b,d) − orient(a,b,d)(sin²θ + cos²θ − 1) = 0
   identically, which is the Lean `linear_combination` certificate described in the text.

No hunk adds or changes a statement, hypothesis, conclusion, rigor label or record claim. Labels: identical lists
(51, same order). Referenced labels: identical sets (63 distinct). Every `\ref` is an oc label, a foundations label or
an export label of ll or lg. The kind words of the new references fit the targets: `fd:def:rot` is a definition,
`fd:lem:affine-orient` a lemma, `oc:def:basic` a definition with items (a)-(c), and `oc:lem:rot-inv` a lemma.

## 3. Lean source re-read (touched statements)

`LEANEXT/orbit/OrbitConsistency.lean` (SHA-256 `9b843180ac38`, 429 lines):
- line 47 `def Invariant (f : Point → Point) (S : Finset Point) : Prop := ∀ p ∈ S, f p ∈ S`: Definition
  `oc:def:basic`(a), maps-into, Finset. Matches.
- line 93 `noncomputable def rotAbout (c : Point) (θ : ℝ) (p : Point) : Point := ![c 0 + Real.cos θ * (p 0 - c 0) -
  Real.sin θ * (p 1 - c 1), c 1 + Real.sin θ * (p 0 - c 0) + Real.cos θ * (p 1 - c 1)]`: matches the display in (b).
- line 112 `noncomputable def polar (c : Point) (r θ : ℝ) : Point := ![c 0 + r * Real.cos θ, c 1 + r * Real.sin θ]`:
  matches (c).
- line 117 `theorem orient_rotAbout_inv (c : Point) (θ : ℝ) (a b d : Point) : orient (rotAbout c θ a) (rotAbout c θ b)
  (rotAbout c θ d) = orient a b d`, no hypotheses. Proof: `simp only [orient, rotAbout, ...]` then
  `linear_combination (orient-expression) * Real.sin_sq_add_cos_sq θ`. Matches Lemma `oc:lem:rot-inv` and its
  comparison with the Lean proof.
- Map-row record claims for these two statements still hold: `LAYERLEAN/LayerLemma.lean` lines 105 (`Invariant`),
  298 (`rotAbout`) and 932 (`polar`) have identical text, and `LEANEXT/orbit/logs/axioms.log` line 1 prints
  `orient_rotAbout_inv` with [propext, Classical.choice, Quot.sound].

The `\leanref` line numbers (47, 93, 112, 117) are correct.

## 4. Compile

`build/oc_recheck_r1_wrapper.tex` (identical to the contract wrapper `build/oc_wrapper.tex`) was compiled twice from
`build/` with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`. Both runs exited 0 (logs
`build/oc_recheck_r1_run1.txt`, `build/oc_recheck_r1_run2.txt`). Results: 0 error lines, 0 overfull boxes, 13 pages,
no "Missing", no multiply defined labels. The 44 undefined references are all `fd:` (27), `ll:` (12) or `lg:` (5), as
expected in the standalone check. The pre-fix snapshot was compiled with the same commands for comparison
(`build/oc_recheck_r1_pre_wrapper.tex`): 13 pages, 0 overfull boxes, and the same 68 underfull warnings at the same
places once the line shift of the three hunks is accounted for. So the fix adds no box warning. pdftotext
(`build/oc_recheck_r1.txt`) shows the three new passages typeset correctly.

## 5. Hygiene (contract rules)

oc.tex and oc.map.tsv contain no machine path, no tool name (contract rule 3), no "verified", "certified" or
"proved", and no `\newcommand`, `\renewcommand`, `\def`, `\usepackage` or `\providecommand`. The new text uses only
`\ref` and math mode, with no `\lean`/`\dirn` around spaced expressions.

## Observations (not findings; they concern the fix log, not the document)

- The log says the snapshot "wrote R_{c,θ} 42 times and M_θ twice". These are line counts (42 lines; lines 141 and
  230). The occurrence counts are 62 for R_{c,·} and 3 for M_θ. This does not affect the document.
- The log's line references into ll.tex and lg.tex (ll.tex:390-396 and 405, lg.tex:140-143) predate those sections'
  own edits in this round. They are now ll.tex:395-401 and 411, and lg.tex:144-148. The note in oc.tex cites no line
  numbers, so it is unaffected.
- The note describes the notation of fd, ll and lg. If a later round renames rotation symbols there, it must update
  this note too (the fixer's log says the same about a rename in oc).

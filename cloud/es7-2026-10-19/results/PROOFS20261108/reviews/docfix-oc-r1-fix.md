# Section `oc`, whole-document review round 1 (docfix-r1): fix log

Inputs: two minor findings for `oc` from the whole-document review, round 1:
`reviews/doc-r1-xref-ocpcec.md` F1 (finding 1 below) and `reviews/doc-r1-consistency.md` m6 (finding 2 below).
Both concern the same notation clash. Pre-edit snapshot: `snapshots/docfix-r1-pre/oc.tex` (SHA-256 `4be86aff99b9`,
938 lines) and `snapshots/docfix-r1-pre/oc.map.tsv` (SHA-256 `5278bd649da2`, 44 lines). Paths are relative to STAGE
(`sections/`, `build/`, `reviews/`, `snapshots/`) or, for Lean sources, to the results directory. `oc.tex:N` refers to
the file after the fix (SHA-256 `093dc95716f6`, 944 lines).

Both findings resolved: 2 fixed, 0 declined.

## Summary

| # | finding | severity | action | location after the fix |
|---|---|---|---|---|
| 1 | [xref-ocpcec F1] oc writes the rotation map as R_{c,θ} and its matrix as M_θ, citing Definition `fd:def:rot`, which writes the map as ρ_{c,θ}; fd writes R_θ for the matrix (Lemmas `fd:lem:rot`, `fd:lem:affine-orient`). The pointer in the proof of `oc:lem:rot-inv` leads to "the linear part R_θ of ρ_{o,θ}", where R is a matrix | minor | fixed: a note on notation added to Definition `oc:def:basic`(b), and the pointer in the proof of Lemma `oc:lem:rot-inv` now gives the correspondence | `oc.tex:144-148` (Definition `oc:def:basic`(b)); `oc.tex:242-244` (proof of Lemma `oc:lem:rot-inv`) |
| 2 | [consistency m6] oc uses R_{c,θ} for the map while fd and lg use R_θ for the matrix; oc calls the matrix M_θ | minor | fixed by the same note (the reviewer's second option, "add a sentence noting that oc's R_{c,θ} is the map, not fd's matrix R_θ"). The note also covers lg | `oc.tex:144-148` |

Also updated to stay accurate: the Dependencies paragraph (`oc.tex:111-113`). It now says that Lemma
`fd:lem:affine-orient` is cited in the new note as well as in the proof of Lemma `oc:lem:rot-inv`.

## Check against the sources

The findings are correct:
- `sections/fd.tex:381-385` (Definition `fd:def:rot`) writes the map as ρ_{c,θ} = rotAbout c θ. `fd.tex:404-405`
  (Lemma `fd:lem:rot`) writes ρ_θ = ρ_{c,θ} and calls the matrix R_θ. `fd.tex:546-548` (Lemma
  `fd:lem:affine-orient`(i)) says "the linear part R_θ of ρ_{o,θ}".
- `sections/lg.tex:140-143` lets R_θ be the matrix and writes the map as rotAbout(c,θ).
- `sections/ll.tex:390-396` (Definition `ll:def:rot`) writes the map as ρ_{c,θ} and uses ρ = ρ_{c,2π/m} (e.g. ll.tex:445,
  467, 512). ll calls the matrix A_θ (ll.tex:405).
- Before the fix, oc wrote R_{c,θ} 42 times and M_θ twice (oc.tex:141 and 230 in the snapshot) and gave no
  correspondence. No other section uses R_{c,θ}.

## What was changed

1. Definition `oc:def:basic`(b), after "we write ρ = R_{c,2π/m} when c and m are clear", adds:
   "(Notation: Definition `fd:def:rot` and the layer-lemma section write ρ_{c,θ} for the map R_{c,θ}, so that our ρ is
   their ρ_{c,2π/m}; the foundations and layer-geometry sections write R_θ for the matrix M_θ, for instance in Lemma
   `fd:lem:affine-orient`. In this section R_{c,θ} always denotes the map, never a matrix.)"
2. Proof of Lemma `oc:lem:rot-inv`: "(This is the case det = 1 of Lemma `fd:lem:affine-orient`.)" now reads
   "(This is the case det = 1 of Lemma `fd:lem:affine-orient`, item (i), which writes the map R_{o,θ} as ρ_{o,θ} and the
   matrix M_θ as R_θ.)". fd's item (i) is the rotation case, headed by the same Lean theorem
   `ErdosSzekeres.OrbitConsistency.orient_rotAbout_inv`; its centre is called o.
3. Dependencies: "a parenthetical comparison in the proof of Lemma `oc:lem:rot-inv` cites Lemma
   `fd:lem:affine-orient`" now reads "Lemma `fd:lem:affine-orient` is cited only in a note on notation in Definition
   `oc:def:basic`(b) and in a parenthetical comparison in the proof of Lemma `oc:lem:rot-inv`".

## Choice of fix (note rather than rename)

A full rename (R_{c,θ} to ρ_{c,θ} in 42 places, M_θ to R_θ) was considered and not done, for three reasons.
- The fd fixer of this round handles fd F1 (`doc-r1-xref-fdlllg.md`) and consistency m5. Their suggested fix names
  oc's variant ("R_{c,θ} with matrix M_θ") in fd's notation paragraph. Renaming oc at the same time would make that
  sentence false.
- Both findings accept a note as the fix: finding 1 proposes exactly this clause, and finding 2 offers it as its
  second option.
- The rename would touch about 20 statements and change no mathematics.
If a later round prefers the rename, it should be done together with fd's notation paragraph.

The note refers to fd's matrix only through the export labels `fd:def:rot` and `fd:lem:affine-orient`. Lemma
`fd:lem:rot` is not in CONTRACT.md's list of foundations export labels, and the ocpcec reviewer treats it as "not an
export label" (`doc-r1-xref-ocpcec.md:119`). No other section references it, so it is named in this log only and not
referenced in `oc.tex`. The note mentions the layer-lemma and layer-geometry sections in words, without `\ref`.
`lg:sec` and `ll:sec` are not export labels either.

## Lean declarations re-read (statements touched)

The statement text of the two touched statements is unchanged; only a notational sentence (in the definition) and
a proof comment were added. Re-read in `LEANEXT/orbit/OrbitConsistency.lean` (SHA-256 `9b843180ac38`, 429 lines):
- line 47 `def Invariant (f : Point → Point) (S : Finset Point) : Prop := ∀ p ∈ S, f p ∈ S`: matches (a);
- line 93 `noncomputable def rotAbout (c : Point) (θ : ℝ) (p : Point) : Point := ![c 0 + Real.cos θ * (p 0 - c 0) -
  Real.sin θ * (p 1 - c 1), c 1 + Real.sin θ * (p 0 - c 0) + Real.cos θ * (p 1 - c 1)]`: matches the display in (b);
- line 112 `noncomputable def polar (c : Point) (r θ : ℝ) : Point := ![c 0 + r * Real.cos θ, c 1 + r * Real.sin θ]`:
  matches (c);
- line 117 `theorem orient_rotAbout_inv (c : Point) (θ : ℝ) (a b d : Point) : orient (rotAbout c θ a) (rotAbout c θ b)
  (rotAbout c θ d) = orient a b d`, with no hypotheses, proved by `linear_combination` with `Real.sin_sq_add_cos_sq θ`.
  This matches Lemma `oc:lem:rot-inv` and the comparison with the Lean proof.
The line numbers in the `\leanref` heads (47, 93, 112, 117) are unchanged and correct.

## Other checks

- Labels: identical to the snapshot (51 labels, same order). Every label referenced after the fix was already
  referenced before it, and no new label prefix appears.
- `sections/oc.map.tsv`: no change is needed. No statement environment, Lean name or line number changed, and no
  map note mentions the notation. The file is byte-identical to the snapshot, so `appendix_map.tex` does not need to
  be regenerated for oc.
- No machine paths, no forbidden names (contract rule 3), no "verified"/"certified", and no `\newcommand`/`\usepackage` in
  `oc.tex` (grep).
- Compile: `build/oc_wrapper.tex` compiled twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode
  -halt-on-error`. Both runs exited 0, with 0 errors (`!` lines), 0 overfull boxes (none at all, so 0 above 1pt) and
  13 pages. The only undefined references are `fd:`, `ll:` and `lg:` labels, as expected in the standalone check.
  The new passages render correctly (checked with pdftotext).

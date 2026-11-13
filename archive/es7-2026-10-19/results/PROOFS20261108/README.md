# PROOFS20261108: written proofs of the Lean-checked results on symmetric point sets (Stage 1)

8 November 2026 (KST). **Written proofs (not refereed)** of Lean-checked theorems. Every theorem restated here keeps
its own label, **Lean-checked** or, where only a project record documents the Lean check, **Lean-checked according to
the record**. The written proofs are a second route to the same statements; they raise no label and claim no new
result.

- **The document.** `proofs.pdf` (188 pages, source `proofs.tex`) has a scope section and twelve sections. Each
  section restates the Lean-checked theorems of one part of the project's work on symmetric point sets, faithfully to
  the Lean declarations, and gives each a complete proof that a mathematician can check without Lean.
- **Statement map.** Appendix A of the PDF and `MAP.tsv` list all 470 labelled statements (theorems, lemmas, facts,
  definitions, remarks) with their Lean names and `file:line`.
- **Faithful statements.** A statement that corresponds to a Lean declaration has the same hypotheses, side conditions
  included (casts, `Finset` or `Set`, natural-number subtraction), the same conclusion and the same quantifier order.
  A more convenient form is labelled a variant and derived from the faithful one.
- **Hypotheses stay hypotheses.** Theorems that take unproved propositions as hypotheses (`Sixfold66`, `Sevenfold70`,
  and the case classes `HalfTurn34`, `Threefold33`, `Fivefold35`, `MirrorOneAxis33`, `MirrorNoAxis34`, `Fourfold32`)
  are stated with them. A remark names, for each hypothesis, the records that support it and their labels. The two
  mirror classes are themselves Lean-checked theorems (Section 10).
- **Computer-assisted statements.** Where the Lean proof is a finite computation (`decide`, `decide +kernel` on
  explicit data), the statement is marked computer-assisted, and the document gives the reduction and describes
  exactly what is evaluated; where a complete hand proof is also given, the mark is "computer-assisted in Lean". No
  Lean file under the directories of the table below or under `ErdosSzekeres/` uses `native_decide`,
  `decide +native`, `Lean.ofReduceBool`, `Lean.ofReduceNat` or `debug.skipKernelTC` (text search; the only occurrence
  is in a comment).
- **Axioms.** Each section names the build and axioms logs that its labels rest on. Where no saved `#print axioms`
  output covers a declaration, the section says so and names the evidence used instead; the rules are in Section 1
  ("Rigor labels"). For `C2FINAL/Central34Orbits.lean` no Lean output is committed, so its declarations, among them
  three theorems, are labelled Lean-checked according to the record (`C2FINAL/README.md`, §6).
- **Line basis.** All `file:line` references are to commit `7e32ee259`, the parent of the commit that adds this
  directory. Paths that begin with `ErdosSzekeres/`, `docs/`, `experiments/` or `scripts/` are relative to the
  repository root; all others are relative to `cloud/es7-2026-10-19/results/`.

## Sections

| § | key | title | Lean files restated | rows |
|---|---|---|---|---|
| 1 | `fd` | Conventions and foundations | `ErdosSzekeres/{Definitions,Basic,Orientation,OrientationGeometry,ConvexCycleCuts}.lean`, `ErdosSzekeres/Suk/{FourPoint,OrientationClique,Reflection,SupportingLines}.lean`; definitions shared by `LAYERLEAN`, `LEANEXT/orbit`, `SYMLEAN` and `MIRRORETV/lean` | 40 |
| 2 | `ll` | The layer lemma and the reduction to exactly *mt* points | `LAYERLEAN/LayerLemma.lean` | 31 |
| 3 | `lg` | Geometry of the layers: nesting, chains and polar rules | `LAYERLEAN/LayerLemma.lean` | 31 |
| 4 | `oc` | Orbit literals, rays and phases, key order | `LEANEXT/orbit/OrbitConsistency.lean`, `LEANEXT/merged/Merged.lean`, `LEANEXT/keys/KeyOrder.lean` | 43 |
| 5 | `pc` | Phase patterns and angular rules | `LEANEXT/phase/PhaseClassification.lean`, `LEANEXT/capstone/{Capstone,Capstone2}.lean`, `LEANEXT/linked/Linked.lean` | 32 |
| 6 | `ec` | Small corollaries for *k* = 7 and *k* = 8 | `LEANEXT/es7corr/ES7Corollaries.lean`, `ES8SYM/lean/{PolarOrient,C6check}.lean`, `PRIMEFOLD/compat/lean/{PCompatCore,L0Check}.lean` | 41 |
| 7 | `sr` | Reduction of symmetric sets to case classes | `SYMLEAN/SymmetricReduction.lean` | 46 |
| 8 | `ar` | Affine symmetries | `SYMLEAN/AffineReduction.lean` | 30 |
| 9 | `mm` | The mirror lemma and the mirror reduction (Theorem A of `MIRRORETV`) | `MIRRORETV/lean/MirrorMain.lean`; two definitions of `ErdosSzekeres/Omission/Realization.lean` | 21 |
| 10 | `mb` | Mirror bounds via Baek's theorem and the three-class reduction | `MIRRORETV/lean/{MirrorMain,MirrorNine_append}.lean`, `SYMLEAN/mirror/ReductionThreeClasses.lean`, bridge files under `ErdosSzekeres/Omission/`; Baek's theorem and the cups–caps theorem (`ErdosSzekeres/Vendor/`) are cited, not reproved | 42 |
| 11 | `cb` | Case-split bookkeeping: the threefold cover and the central 34-point split | `C3LEAN/C3Cover.lean`, `C2FINAL/Central34Orbits.lean` | 100 |
| 12 | `sa` | Size arithmetic of the symmetric *k* = 7 reduction | `AUDIT3/A1_reduction/SizeArith.lean`, `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean`, `ES7SPLIT/review/equivalence/BaekSeven.lean` | 13 |

Each section ends with a Coverage paragraph that lists the declarations of its files that it restates and those it
leaves out, with the reason.

## What the written proofs use

- Standard facts of convexity, compactness, plane isometries and roots of unity, each stated precisely where it
  is used; the References name textbooks (Rockafellar, *Convex Analysis*; Rudin, *Principles of Mathematical
  Analysis*).
- Baek's theorem and the Erdős–Szekeres cups–caps theorem, stated exactly as the vendored Lean code uses them; cited,
  not reproved.
- The hypotheses named above. The evidence for them outside Lean (SAT certificates, exact computations, written
  soundness proofs) is described in remarks but not checked in this document. For SAT certificates the project counts
  only the verdicts of cake_lpr (`LRATCHECK20261105`).

## How the proofs were checked

All checks were internal to the project. The document has not been refereed.

- **Rules.** `reviews/CONTRACT.md` fixed the rules that every section and review followed: faithfulness to Lean,
  complete proofs, computations, hypotheses, labels and coverage, and a severity scale. *Blocker*: a false or
  unfaithful statement, an invalid step or real gap, circularity, an overclaimed label. *Major*: a gap a reader could
  fill but that is not filled, an ambiguity, an unexplained omission, a wrong file or line. *Minor*: style and small
  imprecision. A section passed when no review reported a blocker or major finding.
- **First reviews** (Sections 1–11). Each section was reviewed separately under four briefs: fidelity to the Lean
  statements, rigor of the proofs, claims and labels, and an adversarial reading. 48 reports; 2 major findings, both
  in Section 1 and fixed before a second round of all four reviews; 364 minor findings.
- **Polish** (Sections 1–11). Each minor finding was fixed, marked as a duplicate, or left unchanged with a reason
  (`reviews/<key>-polish-r1-fix.md`). Each change was then audited against its diff, and a fresh referee read each
  section: 22 reports, no blocker or major finding, 48 minor ones.
- **Section 12** was written later and reviewed under two briefs (mathematics; claims) in two rounds: 4 reports, no
  blocker or major finding.
- **Whole document.** The 48 open minor findings were fixed and every change was audited (16 audit reports). Eight
  reviews then read the assembled document: cross-references (in four groups of sections), consistency of notation
  and conventions, claims and front matter, completeness against the Lean files of the Stage 1 directories, and
  typesetting of the PDF. They reported 80 findings, 16 of them major, none a blocker. Every fix was re-checked by a
  separate reader (14 re-check reports). One fix cited a label outside the agreed list of shared labels; its re-check
  caught this and a second round corrected it.
- **Final pass.** The 24 findings still open (four of them, on the label of the `C2FINAL` theorems, treated as major)
  were fixed section by section, and each fix was re-checked by a separate reader (10 fix and 10 re-check reports; no
  blocker or major finding remained). A sweep then read the whole document for the consistency of the changed labels;
  its one major finding was that the generated appendix was older than the last map edits, and the final build
  regenerates it. The main change: the three theorems of `C2FINAL/Central34Orbits.lean`, for which no Lean output is
  saved, now carry the label Lean-checked according to the record wherever they are named (Sections 7, 8, 10 and 11,
  and the scope section). Nineteen further small wording edits were then made by hand in three batches of 10, 7 and 2
  (`reviews/final-inline-edits-1.diff` to `-3.diff`), and each batch was read by independent checks
  (`reviews/final-inline-accuracy.md`, `final-inline-rules.md`, `final-inline2-check.md`, `final-inline3-check.md`).
- **Mechanical checks of the final text.**
  - All 663 `\leanref` heads cite a line that declares the named Lean constant at commit `7e32ee259`.
  - All 677 locations in the statement maps declare a name of their row.
  - The dependency graph of the proofs (`tools/depgraph.py`, output in `logs/depgraph.txt`) has 470 statements and
    523 dependencies. Its three cycles are references between different parts of a statement, not circular
    reasoning: the proof of `fd:lem:mono`(d) mentions `fd:lem:ngon-basic`(b) only to describe the Lean proof;
    `sr:lem:supports` names `sr:lem:concyclic` only as a user; `mb:prop:cap113` uses part (a) of `mb:thm:nine`, whose
    parts (b) and (c) use it.

## What is not covered

- **Stage 2** (the SAT encodings): `ENCBLEAN` (encoder B of the sixfold *k* = 8 case as a Lean program, its soundness,
  and `ENCBLEAN/geo`), `H` and `H2` (clause generators and their soundness), and `H3`, `V1-L`, `V2-L`, `V2-L2` (the
  mirror statement `Mir.MirrorExclusionLine` from named CNF-unsatisfiability hypotheses).
- **Stage 3**: the compact checker of omission certificates with its Lean check of ES(8) ≤ 311
  (`experiments/omission-compact-checker-2026-11-05`), and the main library beyond the declarations restated here.
- **`ES8SLACK`**: its Lean files are not treated; written proofs of its lemmas are in `ES8SLACK/proofs.md`.
- **Stage 1 declarations left out on purpose** (reasons in each section's Coverage paragraph):
  - verbatim copies, checked byte-identical;
  - the complex-coordinate helper copies in `LEANEXT/orbit/OrbitConsistency.lean`, and `mirror_seven'`, `mirror_eight'`
    (same statements as `mirror_seven`, `mirror_eight`);
  - tests, negative controls and review files: the controls of `C3LEAN/C3Cover.lean`, the review files under
    `SYMLEAN/review` (among them `VariantChecks.group_form` and the converse mirror bridge), `LEANEXT/review`
    (non-vacuity tests), and `MIRRORETV/review` (`MirrorA.lean` and `MirrorCap.lean`, independent formalizations;
    `FarFlatExtra.lean`, estimates for the far-flat lower bound; `ReplayRepo.lean`, a kernel replay);
  - `MIRRORETV/lean/FarFlat.lean` (estimates for the far-flat lower-bound construction);
  - `C3L` (a CNF generator; definitions only) and `AUDIT2` (audit scripts);
  - `#print`, `#check` and `#eval` commands.

## Files

| path | what |
|---|---|
| `proofs.pdf` | the document |
| `proofs.tex`, `preamble.tex`, `bibliography.tex` | LaTeX sources; `proofs.tex` contains the scope section |
| `appendix_map.tex` | Appendix A, generated by `tools/make_appendix.py` from the section maps |
| `sections/<key>.tex` | the twelve sections |
| `sections/<key>.map.tsv` | statement map of each section: label, kind, Lean names, `file:line`, note |
| `MAP.tsv` | the twelve maps in one table, with a first column `section` |
| `tools/make_appendix.py` | generates `appendix_map.tex` |
| `tools/depgraph.py` | dependency graph of the proofs; reports cycles |
| `logs/build.log` | `pdflatex` log of the third pass |
| `logs/depgraph.txt` | output of `tools/depgraph.py` |
| `reviews/` | the review and fix reports (see below) |
| `SHA256SUMS` | SHA-256 of every other file in this directory |

**The reports.** `reviews/<key>-r<n>-<brief>.md` are the first reviews, `<key>-polish-r1-fix.md`, `<key>-p1-diff.md`
and `<key>-p1-referee.md` the polish, `<key>-doc-r<n>-{fix,audit}.md` the fixes of the open minor findings,
`doc-r1-<brief>.md` the eight reviews of the whole document, `docfix-<key>-r<n>-{fix,recheck}.md` their fixes and
re-checks, and `final-*.md` and `final-inline-edits-*.diff` the final pass. `<key>-writer-concerns.md` are the
writers' own notes from the first draft. `reviews/checks/` holds the check scripts written during the reviews. In the
reports, `STAGE` is the directory in which the document was written (its files correspond to this directory), `REPO` a
checkout of the branch at `7e32ee259`, `RES` = `REPO/cloud/es7-2026-10-19/results`, and `STAGE/../symvenv` a Python
environment with sympy 1.13.3. Of `STAGE/build/` only the check scripts were kept, not the compile wrappers, logs and
page images; the pre-edit snapshots, the inventories of the Lean units (`STAGE/snapshots/`, `STAGE/inventory/`) and
the reviewers' own scratch files were working files and were not kept either. Line numbers in a report refer to the
files as they were when it was written. The copies differ from the working files only in that machine paths are
replaced by `STAGE` and `REPO`, in the script paths (`reviews/checks/`), and in the wording of the sentences that
report hygiene checks (`reviews/scrub_changes.tsv` counts the changes per file).

## Rebuild

From this directory, with TeX Live 2026 and Python 3:

```sh
shasum -a 256 -c SHA256SUMS                                 # check the files; sha256sum -c SHA256SUMS on Linux
python3 tools/make_appendix.py                              # regenerates appendix_map.tex (identical)
pdflatex -interaction=nonstopmode -halt-on-error proofs     # three times
python3 tools/depgraph.py                                   # prints the report kept in logs/depgraph.txt
```

A rebuilt `proofs.pdf` has the same text as the committed one; its embedded date and ID differ, and so does its hash.

Build of this directory on 8 November 2026 (TeX Live 2026): 188 pages; no errors, no warnings, no undefined references
and no overfull boxes; 203 underfull boxes (loose lines, mostly in statement heads that cite many Lean names).

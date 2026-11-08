# Section `ar` (Affine symmetries), polish round 1, lens: referee

**Verdict: pass.** No blocker and no major finding. There are three minor findings (R1–R3). None of them affects a
statement, a proof step or a rigor label.

Inputs: `sections/ar.tex` (797 lines), `sections/ar.map.tsv` (31 lines), `RES/SYMLEAN/AffineReduction.lean`, and
every file or record the section cites. I read the earlier reports (`reviews/ar-r1-*.md`, `ar-polish-r1-fix.md`,
`ar-writer-concerns.md`) only after forming my own view. Line numbers refer to `sections/ar.tex` as it is now.

## Findings

### R1 (minor): the axioms inference does not cover the two rfl lemmas
- **Location.** `ar.tex:60-61`, Rigor and axioms: "Every other declaration of this section is used, directly or through
  other declarations, in the proof of one of these nine theorems. So it depends on no further axiom."
- **Evidence.**
  - `lin2_fst` and `lin2_snd` (`SYMLEAN/AffineReduction.lean:1174-1175`) are `@[simp]` theorems proved by `rfl`.
  - They are used only inside `simp only [...]` (lines 1180, 1187, 1193, 1197).
  - `simp` applies an rfl lemma by definitional unfolding and puts no proof step for it into the proof term. So these
    two constants need not lie in the dependency closure that `#print axioms` follows from the nine printed theorems.
  - "Used in the proof" is true of the source text. The step from it to "depends on no further axiom" is a step about
    proof terms, and for these two lemmas it is not justified as written.
  - The earlier reports checked this claim only through a *textual* dependency closure (`ar-r1-claims.md:87-88`,
    `ar-r1-rigor.md:47-48`).
  - The conclusion is still true. The proof of each lemma is `rfl` about `lin2`, and `lin2` is in the closure: it is
    the map T of `hasConvexNGon_of_affine_symmetry`.
- **Fix.** Add one clause after line 61, for example: "(The rfl lemmas `lin2_fst` and `lin2_snd` are applied by `simp`
  through unfolding and need not occur in these proof terms; their proofs are `rfl` and mention only `lin2`, which
  does occur.)"

### R2 (minor): "the five case classes of Definition sr:def:classes", which defines six
- **Location.** `ar.tex:14`, introduction: "these five theorems take the five case classes of
  Definition~\ref{sr:def:classes} as hypotheses".
- **Evidence.** `sections/sr.tex:209` opens Definition sr:def:classes with "The following six propositions are
  defined". The sixth is `Fourfold32`, which Theorem ar:thm:main does not assume. The sentence reads as if the
  definition had exactly five classes. The statement of Theorem ar:thm:main (`ar.tex:648-649`) names the five
  correctly, so only the introduction is affected.
- **Fix.** "take five of the six case classes of Definition~\ref{sr:def:classes} (all except \lean{Fourfold32}) as
  hypotheses", or name the five.

### R3 (minor): the Coverage paragraph overstates the duplicate
- **Location.** `ar.tex:787-788`: "Lines 1--1058 of SYMLEAN/AffineReduction.lean. They are a verbatim duplicate of
  SYMLEAN/SymmetricReduction.lean".
- **Evidence.**
  - `SymmetricReduction.lean` has 1,059 lines. Its line 1059, `end ErdosSzekeres.SymReduction`, is not among lines
    1–1058 of `AffineReduction.lean`; there it is line 1533.
  - What holds (checked with `cmp`) is that lines 1–1058 of the two files are byte-identical. The Sources paragraph
    (`ar.tex:29-30`) says exactly this.
- **Fix.** "They are a verbatim duplicate of lines 1--1058 of SYMLEAN/SymmetricReduction.lean".

## What I checked independently (all correct)

1. **Fidelity of every statement.** I compared all 45 declarations of lines 1059–1533 with the written statements and
   checked:
   - hypotheses, implicit and explicit arguments, the order of quantifiers, and conclusions;
   - `0 < n` for `avgQ_ge`, `qA_pos` and `qdisc_pos`; only `L ^ n = 1` for `avgQ_mulVec`;
   - `s ≠ 0`, and `t ≠ 0` where needed, for the three Cholesky lemmas, with the `x/0 = 0` remark;
   - `D ≠ 0` without injectivity for `generalPosition_image_of_orient`; `det L ≠ 0`;
   - Mathlib `AffineMap` versus `AffineEquiv`, `⇑f ≠ id` versus `≠ AffineEquiv.refl`;
   - `g '' ↑S ⊆ ↑S` (set image) versus `Invariant` (maps into);
   - the natural-number subtraction `j - i` with `i < j` in `exists_periodic_of_injective`, and `-β / (s^2 t)`.

   No discrepancy.
2. **Map and heads.**
   - Every `\leanref` and every row of `ar.map.tsv` names a declaration that starts exactly at the cited line (45 of
     45, checked by script).
   - The 30 map rows match the 30 statement environments in label, kind and order. Every row has 5 fields.
   - The Coverage list contains all 45 declarations.
3. **Algebra (sympy 1.13.3, 27 checks, all true).**
   - `nsq_mulVec`; qA at (1,0); the evaluation at (−β, α), including the displayed middle expression;
   - `orient_lin2`, in core form and with points; `orient_affine` with translation;
   - `nsq_lin2_chol`, both inverse identities and the intermediate steps written in (b) and (c); the stated formula
     for T'x;
   - β²/α + (αγ − β²)/α = γ; TᵀT equals the Gram matrix (Cholesky factor);
   - the four identities of `matrix_eq_one_of_fix` and the two of `injective_of_affine`;
   - orient(p0,p1,p2) = u0 w1 − u1 w0; the coordinate form and `det_fin_two_of`; the Gram entries.

   End to end, I took the non-orthogonal order-3 matrix L = P R P⁻¹, with R the rotation by 2π/3 and P = [[1,1],[0,2]].
   This gives (α, β, γ) = (9, −9/2, 9/2), T T' = T' T = 1, (T L T⁻¹)ᵀ(T L T⁻¹) = 1 and det T = st = 9/2 > 0.
4. **Proof steps.** I checked every written proof line by line. Three were the main concerns:
   - the common period and g^m = id in Proposition ar:prop:averaging(a);
   - the hull identity in both directions (Step 1 of Lemma ar:lem:cp-affine);
   - h^k = T g^k T' and the equal orders in (d).

   I found no gap and no circularity: fd:lem:affine-orient and fd:lem:affine-cp are only identified, never used, and
   no fd proof cites an ar label.
5. **Cross-references.**
   - Every foreign `\ref` is an allowed export label and is defined in its section: fd ×10, sr:def:iso,
     sr:def:classes, sr:thm:main, sr:thm:variant, mb:thm:baek, mb:thm:classes, mb:thm:main3, cb:thm:c3, cb:thm:c2.
   - I opened each target and it says what ar attributes to it. Two examples:
     - sr:thm:main has exactly the premises of E(33,7);
     - cb:thm:c3 and cb:thm:c2 are the Lean-checked bookkeeping of the 910 roots and of the parallelogram orbit
       closure.
6. **Sources and evidence.**
   - SHA-256 prefixes of all eight cited files.
   - Byte-identity: lines 1–1058 against `SymmetricReduction.lean`; the 1533-line prefix of the axioms file; the
     mirror copy, whose lines 38–1559 equal lines 12–1533 (offset +26).
   - Logs and records: `AffineReduction.out` is empty; `runs.tsv` records exit 0 on 2026-11-01 with matching hash
     prefixes; the axioms log lists the nine theorems with the three standard axioms and the `#check` output.
   - The source contains no `decide`, `native_decide`, `sorry`, `admit` or `axiom`.
   - Lines 4274, 4282 and 4303 of `SYMLEAN/mirror/ReductionThreeClasses.lean` and `SYMLEAN/mirror/axioms.out` are as
     cited.
   - `WRITEUP/P1/p1.tex:173-183` (Remark rem:affine) needs an order-preserving form and says that it is not
     formalized.
   - No Lean file in the checkout has an affine version of the variant.
7. **Remark ar:rem:classes against the records.** I checked each claim against its source:
   - SYMMETRIC.md §§0–4: the cake_lpr-only trust base since 6 November; "both checkers" means the cake_lpr verdict;
     the deleted proofs; the 116,883 threefold pieces; the 910 roots.
   - SYMLEAN/README.md §§5, 6, 9: the latest date in the file is 2 November, so §9 predates the revision.
   - C3FINAL: every record carries `s VERIFIED UNSAT`.
   - C2FINAL §§2, 4, 5, 9, and C2RECHECK §6: the 65 Mac-only units were re-solved, 65 of 65.
   - SYM5: P1 and L1 accepted by both checkers.

   All cited record paths exist. No rigor label is rounded up: the unconditional form is called computer-assisted
   and not Lean-checked as a whole.
8. **Contract rules.**
   - No `\newcommand`, `\def`, `\usepackage` or other macro definition.
   - No machine path and no tool name in `ar.tex` or `ar.map.tsv`.
   - Rigor vocabulary is clean: "verified", "certified" and "proved" occur only in Lean names.
   - Standalone compile (`build/ar_p1ref_wrapper.tex`, two runs of `nice -n 15 pdflatex`): exit 0, no error, no
     overfull box, 68 underfull warnings, and undefined references only to the export labels of fd, sr, mb and cb.
   - The section-local sloppy group causes no problem and can stay.

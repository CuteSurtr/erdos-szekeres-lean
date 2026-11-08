# Fix log of section `mm` (The mirror lemma and Theorem A), round doc-r1

Paths: `sections/`, `snapshots/`, `reviews/`, `build/` and `bibliography.tex` are relative to STAGE. `MIRRORETV/...`
is relative to RES. `ErdosSzekeres/...` is relative to the repository root.

## 0. Inputs

- **Snapshot before editing:** `snapshots/doc-r1-pre/mm.tex` (964 lines) and `snapshots/doc-r1-pre/mm.map.tsv`.
- **Notes addressed:** `reviews/mm-doc-r0-audit.md`. Its verdict is pass, with no blocker or major finding and one
  optional minor finding (its section 7, item 1).
- **After:** `sections/mm.tex` (966 lines). `sections/mm.map.tsv` is unchanged (byte-identical to the snapshot,
  SHA-256 `82cee6db7c02...`).

## 1. Disposition

| note | disposition | where |
|---|---|---|
| audit minor 1: the cups–caps bound in Remark `mm:rem:hm`(2) is cited only through a project note | fixed | `sections/mm.tex:681-684` |

### Minor 1: reference for the cups–caps bound, and the range of the parameters

**Old text** (snapshot l. 681-682):

> These numbers are finite: by the cups--caps theorem, every set in the class that defines $N(n,a,b)$ has at most
> $\binom{a+b-4}{a-2}$ points (\dirn{MIRRORETV/PROOFS.md}, \S1).

**New text** (l. 681-684):

> These numbers are finite: by the cups--caps theorem of Erd\H{o}s and Szekeres (1935), for $a,b\ge2$ every set in
> the class that defines $N(n,a,b)$ has at most $\binom{a+b-4}{a-2}$ points (\dirn{MIRRORETV/PROOFS.md}, \S1), and
> the two numbers above have $a,b\ge j\ge2$.

The three changes:

1. **The reference.** "of Erd\H{o}s and Szekeres (1935)" names the original paper. The document bibliography has it
   as `ES35` (`bibliography.tex:6`: P. Erdős and G. Szekeres, A combinatorial problem in geometry, Compositio
   Math. 2 (1935), 463–470). It is the only Erdős–Szekeres entry, so the author–year form identifies it.
   - No section uses `\cite`; all sections give their references inline (for example `sections/mb.tex:221-222` for
     this paper, `sections/ll.tex:81` for Rockafellar, `sections/sr.tex:294` for Subercaseaux et al.).
   - A `\cite{ES35}` would also be an undefined citation in the standalone compile check, because the wrapper does
     not load the bibliography. So I wrote the reference inline, in the form the audit suggested.
   - The project note stays as the second source: `MIRRORETV/PROOFS.md` l. 25-28 states "It is finite by the
     cups–caps theorem, N(n,a,b) <= C(a+b-4, a-2) (Erdős–Szekeres 1935)".
2. **The range.** "for $a,b\ge2$" is the range in which `MIRRORETV/PROOFS.md` §1 (l. 25) defines $N(n,a,b)$
   ("for n >= 3 and a,b >= 2"). In this range the binomial $\binom{a+b-4}{a-2}$ has natural-number entries.
3. **The two numbers are in the range.** The numbers of the preceding sentence are $N(2j+1,j+1,2j+1)$ and
   $N(2j,j,2j)$. They have $a\in\{j+1,j\}$ and $b\in\{2j+1,2j\}$, so $a,b\ge j$.
   - $j\ge2$ is the hypothesis `hj : 2 ≤ j` of both theorems (re-read below).
   - The section states it as "$2\le j$" in Theorem `mm:thm:odd` (l. 602) and Theorem `mm:thm:even` (l. 633).
   - The remark speaks of the $j$ of those theorems.

**The mathematics of the cited bound.**

- The cups–caps theorem says: an $x$-distinct set in general position with no $a$-cap and no $b$-cup has at most
  $\binom{a+b-4}{a-2}$ points ($a,b\ge2$).
- The bound is symmetric, since $\binom{a+b-4}{a-2}=\binom{a+b-4}{b-2}$, so it does not matter which letter bounds the
  caps.
- The class that defines $N(n,a,b)$ adds the condition "no $n$ points in convex position". This only shrinks the
  class, so the bound holds for it.
- It agrees with the vendored statement cited in `sections/mb.tex` (Theorem `mb:thm:capcup`,
  `ErdosSzekeres/Vendor/ETV/Main/CapCup.lean:46`): $\binom{a'+b'}{a'}<\card S$ gives an $(a'+2)$-cap or a
  $(b'+2)$-cup. Put $a'=a-2$ and $b'=b-2$.

**Consistency check** (small arithmetic check of $\binom{a+b-4}{a-2}$ against the instances of item (1) of the remark;
for each, $a,b\ge j\ge2$ holds and the bound is at least $M$):

| case | $j$ | number | bound | $M$ in item (1) |
|---|---|---|---|---|
| odd | 2 | $N(5,3,5)$ | $\binom41=4$ | 4 |
| even | 3 | $N(6,3,6)$ | $\binom51=5$ | 5 |
| even | 2 | $N(4,2,4)$ | $\binom20=1$ | 1 |
| odd | 3 | $N(7,4,7)$ | $\binom72=21$ | 16 |
| even | 4 | $N(8,4,8)$ | $\binom82=28$ | 22 |
| odd | 4 | $N(9,5,9)$ | $\binom{10}3=120$ | 113 |

For the three small instances the bound equals the $M$ of item (1). For the three Lean-checked instances the bound is
weaker than the $M$ that Baek's theorem gives, as it should be.

## 2. Lean re-read

No statement environment, head, label, `\leanref` or Lean name changed. The edited text is in a remark with no Lean
declaration. It concerns the hypothesis (hM), so I re-read the declarations involved:

- **`MirrorOdd.mirror_odd_general`** (`MIRRORETV/lean/MirrorMain.lean:2498`):
  - `(j M : ℕ) (hj : 2 ≤ j)`;
  - `hM : ∀ (n : ℕ) (c : Configuration n), ¬ c.HasCap (j + 1) → ¬ HasConvexNGon (2 * j + 1)
    (Finset.univ.image c.point) → n ≤ M`;
  - conclusion `S.card ≤ 2 * M`.
- **`MirrorOdd.mirror_even_general`** (`:2599`): the same with `c.HasCap j`, `2 * j` and `S.card ≤ 2 * M + 2`.
- **`Configuration`** (`ErdosSzekeres/Omission/Realization.lean:9`) and **`HasCap`** (`:64`):
  - `xOrder : StrictMono`;
  - nonzero orientation for `i < j → j < k`;
  - caps are negative on all increasing triples.

All of these agree with the remark's derivation and with the statements of Theorems `mm:thm:odd` and `mm:thm:even`.
The added clause uses only `hj`.

## 3. Map

- `sections/mm.map.tsv` is unchanged.
- The `mm:rem:hm` row ("... relation to N(n,a,b) ...") is still accurate.
- The export labels and the 21 statement rows are untouched, so `tools/make_appendix.py` does not need to be re-run
  for this section.

## 4. Compile check

- **Setup.** `build/mm_wrapper.tex` (the contract's wrapper). I ran
  `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error mm_wrapper.tex` twice from `build/`. The console
  output is in `build/mm_docr1_pass1.txt` and `build/mm_docr1_pass2.txt`.
- **Result.**
  - Both runs exited 0, with 13 pages.
  - The log has 0 `!` lines and no "Missing".
  - There are no undefined citations, no multiply defined labels, and no other LaTeX or package warnings.
- **Boxes.**
  - Overfull boxes: 0, so 0 over 1pt.
  - Underfull boxes: 76, the same count as in the doc-r0 audit. They come from the section's local
    `\emergencystretch`.
- **Undefined references.** There are 17: the 13 contract `fd:` labels and the 4 `mb` export labels (`mb:thm:baek`,
  `mb:thm:seven`, `mb:thm:eight`, `mb:thm:nine`). This is expected in a standalone build, and there are no others.
- **Rendering.** I rendered page 9 (`build/mmdocr1/page-09.png`). Remark 1.19(2) typesets cleanly. The new text fills
  two lines of the item, and the inline binomial is set in text style.

## 5. Other checks

- **Machine paths and tool names.** `sections/mm.tex` and `sections/mm.map.tsv` contain none.
- **Macros.** There is no `\newcommand`, `\def`, `\let` or `\usepackage`.
- **Rigor words.** "verified" and "certified" do not occur. The edit adds no rigor word.
  - The cups–caps bound is attributed to the 1935 paper and to the project note. No Lean check is claimed for it.
  - The remark still says that this relation "is not used in this section".
- **The diff.** `diff -u` against the snapshot gives exactly one hunk, l. 681-684.

## 6. Files written

- `sections/mm.tex` (edited);
- `snapshots/doc-r1-pre/mm.tex` and `snapshots/doc-r1-pre/mm.map.tsv` (snapshot);
- `build/mm_wrapper.{aux,log,out,pdf}`, `build/mm_docr1_pass1.txt`, `build/mm_docr1_pass2.txt`,
  `build/mmdocr1/page-09.png`;
- this log.

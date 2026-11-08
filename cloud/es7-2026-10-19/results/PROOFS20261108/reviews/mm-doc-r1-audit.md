# Diff audit of section `mm` (The mirror lemma and Theorem A), round doc-r1

**Verdict: pass.** There is no blocker, no major and no minor finding (section 7).

Paths: `sections/`, `snapshots/`, `reviews/` and `build/` are relative to STAGE. `MIRRORETV/...` is relative to RES.
`ErdosSzekeres/...` is relative to the repository root.

## 0. Inputs

- **Before:** `snapshots/doc-r1-pre/mm.tex` (964 lines) and `snapshots/doc-r1-pre/mm.map.tsv`.
- **After:** `sections/mm.tex` (966 lines) and `sections/mm.map.tsv`.
- **Fix log:** `reviews/mm-doc-r1-fix.md`.
- **Notes addressed:** `reviews/mm-doc-r0-audit.md` §7, minor 1 (the only open note of the predecessor audit). The
  three earlier notes (`reviews/mm-p1-diff.md` minors 1 and 2, `reviews/mm-p1-referee.md` R1, the `mm` entries of
  `build/open_minors.json`) were fixed in doc-r0. I re-checked that they are still fixed (section 2).
- **The diff:**
  - `diff -u` on `mm.tex` gives exactly one hunk (snapshot l. 681-682, current l. 681-684).
  - `diff -u` on `mm.map.tsv` is empty. Both map files have SHA-256 `82cee6db7c02...`, as the log says.
  - A word-level diff shows exactly two replacements and nothing else:
    - "theorem," becomes "theorem of Erd\H{o}s and Szekeres (1935), for $a,b\ge2$";
    - "\S1)." becomes "\S1), and the two numbers above have $a,b\ge j\ge2$.".

## 1. The hunk: Remark `mm:rem:hm`(2), l. 681-684

New text:

> These numbers are finite: by the cups--caps theorem of Erd\H{o}s and Szekeres (1935), for $a,b\ge2$ every set in
> the class that defines $N(n,a,b)$ has at most $\binom{a+b-4}{a-2}$ points (\dirn{MIRRORETV/PROOFS.md}, \S1), and
> the two numbers above have $a,b\ge j\ge2$.

**Mathematics.**

- **The bound.** The cups–caps theorem says that an x-distinct set in general position with no $a$-cap and no
  $b$-cup has at most $\binom{a+b-4}{a-2}$ points ($a,b\ge2$). Caps and cups are defined by consecutive triples,
  which is the slope definition of the classical theorem (PROOFS Lemma 2.1, Consequences (a)).
  - The bound is symmetric, since $\binom{a+b-4}{a-2}=\binom{a+b-4}{b-2}$. So it does not matter which letter bounds
    the caps.
  - The class that defines $N(n,a,b)$ adds "no $n$ points in convex position". This only shrinks the class, so every
    set in it obeys the bound.
  - Edge case $a=2$: two x-distinct points always form a 2-cap (PROOFS §1: "Sequences with m <= 2 count as both"), so
    the class has at most one point, and $\binom{b-2}{0}=1$. The case $b=2$ is the same.
- **The range.** "for $a,b\ge2$" is the range in which PROOFS §1 defines $N(n,a,b)$. In that range the binomial
  has natural-number entries.
- **The two numbers are in range.** "The two numbers above" are $N(2j+1,j+1,2j+1)$ and $N(2j,j,2j)$, in the indexing
  of Theorems `mm:thm:odd` and `mm:thm:even`. Their parameters are:
  - odd case: $(a,b)=(j+1,2j+1)$;
  - even case: $(a,b)=(j,2j)$.

  So $a,b\ge j$ in both cases. $j\ge2$ is the hypothesis `hj : 2 ≤ j` of the theorems the remark comments on, so the
  bound applies. The even case needs it ($a=j$), and the odd case would need only $j\ge1$.
- **The attribution.** The cups–caps theorem is the theorem of P. Erdős and G. Szekeres, *A combinatorial problem in
  geometry*, Compositio Math. 2 (1935). It gives exactly this threshold: $\binom{k+l-4}{k-2}+1$ points force a
  $k$-cup or an $l$-cap.
  - The document bibliography has this paper as `ES35` (`bibliography.tex:6-7`), and it is the only Erdős–Szekeres
    entry. So the author–year form identifies it.
  - `sections/mb.tex:221-222` (Remark `mb:rem:capcup`) cites the same paper inline for the same theorem.
  - No section uses `\cite` (grep), so the inline form matches the document's convention.
- **The vendored form.** The bound agrees with the vendored statement `Config.cap_cup`
  (`ErdosSzekeres/Vendor/ETV/Main/CapCup.lean:46`, re-read): `Nat.choose (a + b) a < S.card → C.HasNCap (a + 2) S ∨
  C.HasNCup (b + 2) S`. Put $a'=a-2$ and $b'=b-2$. The section does not claim this agreement, so it is a consistency
  check only.

**Records.** `MIRRORETV/PROOFS.md` §1, l. 25-28 (re-read) says:

> N(n,a,b), for n >= 3 and a,b >= 2: the maximum size of an x-distinct set in general position with no n points in
> convex position, no a-cap and no b-cup. [...] It is finite by the cups–caps theorem, N(n,a,b) <= C(a+b-4, a-2)
> (Erdős–Szekeres 1935).

So the source supports the bound, the range $a,b\ge2$, the attribution and the section reference "§1". The
condition $n\ge3$ in the definition of $N$ is not repeated in the new text, but the bound does not depend on $n$.
Both numbers have $n\ge4$ anyway.

**Consistency with item (1).** I recomputed the fix log's table. The bound equals the $M$ of item (1) for the three
small instances:
- odd $(j,M)=(2,4)$: $\binom41=4$;
- even $(3,5)$: $\binom51=5$;
- even $(2,1)$: $\binom20=1$.

It is weaker than Baek's value for the three Lean-checked instances:
- $(3,16)$: bound 21;
- $(4,22)$: bound 28;
- $(4,113)$: bound 120.

In all six instances, $a,b\ge j\ge2$. Nothing in the section depends on this table.

**Rigor vocabulary.** The hunk adds no rigor word.
- The bound is attributed to the 1935 paper and to the project note, and no Lean check is claimed for it.
- This is a cited classical theorem with a precise statement and a reference, as contract rule 5 allows.
- The remark still says that the relation to $N$ "is not used in this section" and that no declaration of `MirrorOdd`
  states it.
- (hM) is still presented as an unproved hypothesis.

**LaTeX.**
- `Erd\H{o}s` and the inline `\binom` are standard.
- `\dirn{MIRRORETV/PROOFS.md}` contains no space, so `\nolinkurl` is safe.
- The new lines are pure ASCII.
- No macro is defined and no package is loaded.

## 2. The fixer's dispositions

| note | source | disposition | audit |
|---|---|---|---|
| cups–caps bound cited only through a project note | `mm-doc-r0-audit.md` §7, minor 1 | fixed | fixed as suggested: the original paper is named, and the optional range "for $a,b\ge2$" was added. The extra clause "$a,b\ge j\ge2$" is correct (section 1) and closes the small gap of whether the bound applies to the two numbers |

No note was declined.

The earlier notes are still fixed in the current file:
- `mm-p1-diff.md` minor 1 (citation order): "(Lemma~2.1(b))" follows the all-triples fact and "(\S1; see also
  Lemma~2.3)" follows the cup fact (l. 687-689).
- `mm-p1-diff.md` minor 2 ("moreover"):
  - Definition `mm:def:config`(c) reads "From now on let $T$ also be $x$-injective" (l. 148-149);
  - (d) reads "If, in addition, $T$ is in general position" (l. 157).
- `mm-p1-referee.md` R1 (finiteness of $N$): the finiteness sentence precedes the derivation of (hM) for $M=N$, and
  it is now sharper.

**Claims in the fix log, checked.**
- **Files.** Line counts are 964 and 966. The map hash is identical.
- **Bibliography.** `ES35` is at `bibliography.tex:6`.
- **Inline references in other sections.** `sections/mb.tex:221-222` cites ES 1935, `sections/ll.tex:81` cites
  Rockafellar and `sections/sr.tex:294` cites Subercaseaux et al. All three are inline.
- **PROOFS.md.** The quotation of l. 25-28 is accurate.
- **Section lines.** "$2\le j$" is at l. 602 (Theorem `mm:thm:odd`) and l. 633 (Theorem `mm:thm:even`).
- **Lean.** `Configuration` is at `Realization.lean:9` and `HasCap` at `:64`.
- **Compile.** Counts: 13 pages, 0 overfull, 76 underfull, 17 undefined references. `build/mm_docr1_pass{1,2}.txt`
  and `build/mmdocr1/page-09.png` exist.

All of these are accurate.

## 3. Touched statements re-read against Lean

No statement environment, head, label or `\leanref` changed. The hunk is inside Remark `mm:rem:hm`, which has no Lean
declaration. Its new clause uses the hypothesis $2\le j$, so I re-read every declaration the remark comments on
(`MIRRORETV/lean/MirrorMain.lean`):

- **`mirror_odd_general`** (`:2498`): `(j M : ℕ) (hj : 2 ≤ j)`, then
  `hM : ∀ (n : ℕ) (c : Configuration n), ¬ c.HasCap (j + 1) → ¬ HasConvexNGon (2 * j + 1) (Finset.univ.image c.point) → n ≤ M`,
  with conclusion `S.card ≤ 2 * M`.
- **`mirror_even_general`** (`:2599`): the same with `¬ c.HasCap j`, `2 * j` and `S.card ≤ 2 * M + 2`.
- **`mirror_odd_general_line`** (`:2641`) and **`mirror_even_general_line`** (`:2650`) (parts (b), (c) of
  Theorem `mm:thm:line`, also named in the remark's first sentence): `(hj : 2 ≤ j)` and the same `hM`, followed by
  `{n0 n1 c : ℝ}`.
- **`Configuration`** (`ErdosSzekeres/Omission/Realization.lean:9`):
  - `xOrder : StrictMono`;
  - `generalPosition` for `i < j → j < k`.
- **`HasCap`** (`:64`): `orient < 0` on all increasing triples of a `StrictMono` index map.

So $j\ge2$ holds for every theorem whose (hM) the remark discusses. The statements of Theorems `mm:thm:odd` and
`mm:thm:even` (l. 601-610 and 632-641) still state "Let $j,M\in\N$ with $2\le j$" and the (hM) above, unchanged.

## 4. Map

- `sections/mm.map.tsv` is byte-identical to the snapshot.
- A script check confirms the following:
  - The header is the contract's.
  - All 21 rows have 5 fields.
  - The 21 labelled statement environments match the rows in order, label and kind.
  - There are 22 labels, unique and all `mm:`-prefixed.
  - All 38 distinct `\ref` targets are own labels, contract `fd:` labels or `mb` export labels (`mb:thm:baek`,
    `mb:thm:seven`, `mb:thm:eight`, `mb:thm:nine`).
  - The 8 export labels of `mm` are all defined.
- The `mm:rem:hm` row ("... relation to N(n,a,b) ...") is still accurate. No re-run of `tools/make_appendix.py` is
  needed for this section.

## 5. Compile check

- **Setup.**
  - Wrapper: `build/mm_docr1audit_wrapper.tex`. Its content is the contract's wrapper; `diff` against
    `build/mm_wrapper.tex` is empty.
  - Ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error mm_docr1audit_wrapper.tex` twice from `build/`.
- **Result.**
  - Both runs exited 0 and produced 13 pages.
  - The log has 0 `!` lines, no error, no "Missing", no undefined citation and no multiply defined label.
  - The only other warning is the summary "There were undefined references".
- **Boxes.** There are **0 overfull boxes**, so there is no minor finding from this item. There are 76 underfull
  boxes, the same count as in the doc-r0 audit; they come from the section's local `\emergencystretch` and are
  cosmetic.
- **Undefined references.** These are only the 13 contract `fd:` labels and the 4 `mb` export labels above, as
  expected in a standalone build.
- **Rendering.**
  - I rendered page 9 (`build/mmdocr1audit/page-09.png`). Remark 1.19(2) typesets cleanly.
  - The new text adds about one line to the item, and the inline binomial is set in text style without disturbing the
    line spacing.
  - The text extraction (`build/mm_docr1audit_wrapper.txt`) reads "by the cups–caps theorem of Erdős and Szekeres
    (1935), for a, b ≥ 2 every set in the class ...".
- **Files left in `build/`:**
  - `mm_docr1audit_wrapper.{tex,aux,log,out,pdf,txt}`;
  - `mm_docr1audit_pass1.out`, `mm_docr1audit_pass2.out`;
  - `mmdocr1audit/page-09.png`.

## 6. Other checks

- **Machine paths and tool names.** `sections/mm.tex` and `sections/mm.map.tsv` contain none. The only grep hit was
  the substring in `psmallmatrix`, a false positive.
- **Macros.** There is no `\newcommand`, `\def`, `\let`, `\usepackage` or `\makeatletter`.
- **Rigor words.**
  - "verified" and "certified" do not occur.
  - "certificate(s)" refers only to the `linarith` certificates.
  - "proved" occurs only in "not proved here" and for Lean proofs.
  - The added words contain no rigor term.
- **Hypotheses.** (hM) is still a stated, unproved hypothesis in Theorems `mm:thm:odd`, `mm:thm:even` and
  `mm:thm:line`(b), (c). The remark's discussion of $N$ is marked as not used.

## 7. Findings

None.

- **Observation (no action needed).** "the two numbers above have $a,b\ge j\ge2$" is shorthand for "the parameters
  $a,b$ of the two numbers above satisfy $a,b\ge j\ge2$". In context (the preceding sentence displays both numbers) it
  is clear, and it is correct.

No blocker and no major finding:
- the hunk is mathematically correct;
- no Lean statement changed, and the hypothesis $2\le j$ the new clause relies on is in all four declarations;
- every new claim about the records checks out (PROOFS.md §1, the bibliography);
- no rigor label is rounded up;
- no machine path or tool name appears;
- the LaTeX compiles with exit 0 and no overfull box.

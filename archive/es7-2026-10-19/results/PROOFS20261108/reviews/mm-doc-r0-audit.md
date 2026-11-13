# Diff audit of section `mm` (The mirror lemma and Theorem A), round doc-r0

**Verdict: pass.** There is no blocker and no major finding. There is 1 minor finding (section 7). It is optional.

Paths: `sections/`, `snapshots/`, `reviews/` and `build/` are relative to STAGE. `MIRRORETV/...` is relative to RES.
`ErdosSzekeres/...` is relative to the repository root.

## 0. Inputs

- **Before:** `snapshots/doc-r0-pre/mm.tex` (961 lines) and `snapshots/doc-r0-pre/mm.map.tsv`.
- **After:** `sections/mm.tex` (964 lines) and `sections/mm.map.tsv`.
- **Fix log:** `reviews/mm-doc-r0-fix.md`.
- **Notes addressed:** `reviews/mm-p1-diff.md` (minors 1 and 2) and `reviews/mm-p1-referee.md` (R1). These are exactly
  the three entries under `mm` in `build/open_minors.json`.
- **The diff:**
  - `diff -u` on `mm.tex` gives three hunks.
  - `diff -u` on `mm.map.tsv` is empty.
  - A word-level diff confirms that the only changes are the intended ones. The re-wrapped lines of Remark (2) change
    whitespace only.

## 1. Hunk-by-hunk check of `mm.tex`

Line numbers refer to the current `sections/mm.tex`.

| # | location | change | check | result |
|---|---|---|---|---|
| 1 | Definition `mm:def:config`(c), l. 148-149 | "Now let $T$ be moreover $x$-injective" becomes "From now on let $T$ also be $x$-injective" | `xset` (`MirrorMain.lean:1549`) takes only `T`. `emb` (`:1553`) and `sortPt` (`:1558`) take `hx : Set.InjOn (fun p => p 0) T`. The definition still defines `xset` for every finite T and assumes x-injectivity from `emb` on. Later statements restate their own hypotheses (Lemma `mm:lem:sort`: "finite and x-injective"; Lemma `mm:lem:upper-caps` proves x-injectivity), so "From now on" does not leak | correct; matches Lean |
| 2 | Definition `mm:def:config`(d), l. 157 | "If $T$ is moreover in general position" becomes "If, in addition, $T$ is in general position" | `cfg` (`:1584`) takes `hx` and `hgp : GeneralPosition T`, and its `point` is `sortPt T hx` | correct; matches Lean |
| 3 | Remark `mm:rem:hm`(2), l. 681-687 | (i) new sentence: the numbers are finite, since by the cups–caps theorem every set in the class that defines $N(n,a,b)$ has at most $\binom{a+b-4}{a-2}$ points (PROOFS.md, §1); (ii) "the point set of a configuration of $n$ points is an $x$-distinct set of $n$ points in general position"; (iii) each source now sits next to its own fact: Lemma 2.1(b) for consecutive ⇒ all triples, and §1 (see also Lemma 2.3) for "a cup is in convex position" | see the mathematics and records checks below | correct |

**Mathematics of hunk 3.**

- **The bound.** The cups–caps theorem says that an x-distinct set in general position with no $a$-cap and no
  $b$-cup has at most $\binom{a+b-4}{a-2}$ points. The bound is symmetric, since $\binom{a+b-4}{a-2}=\binom{a+b-4}{b-2}$,
  so it does not matter which letter bounds caps and which bounds cups. The extra condition "no $n$ points in convex
  position" only shrinks the class, so the bound holds for it.
- **Parameter range.** PROOFS §1 defines $N(n,a,b)$ for $n\ge3$ and $a,b\ge2$. The numbers used are:
  - $N(2j+1,j+1,2j+1)$ (odd case): $a=j+1\ge3$;
  - $N(2j,j,2j)$ (even case): $a=j\ge2$, $b=2j\ge4$, $n\ge4$.

  Both have $j\ge2$ (the hypothesis $2\le j$ of `mirror_odd_general` and `mirror_even_general`), so they lie in that
  range.
- **Consistency with item (1).** The bound reproduces the small-$j$ instances that item (1) states:
  - $\binom{4}{1}=4$ for $(j,M)=(2,4)$, odd;
  - $\binom{5}{1}=5$ for $(3,5)$, even;
  - $\binom{2}{0}=1$ for $(2,1)$, even.
- **The derivation of (hM) for $M=N$.** Let $C$ be a configuration of $n$ points with no $(j+1)$-cap (all-triples,
  `Realization.lean:64`) such that $\mathrm{pts}(C)$ has no convex $(2j+1)$-gon.
  1. `xOrder` is `StrictMono`, so $C$ is injective and $\mathrm{pts}(C)$ is x-distinct with $n$ points.
  2. `generalPosition`, together with the permutation rule and `fd:lem:collinear`, gives no three collinear points.
  3. A consecutive $(j+1)$-cap of $\mathrm{pts}(C)$ would be an all-triples cap (PROOFS Lemma 2.1(b)). Its index map
     is increasing because $C$ is sorted, so `c.HasCap (j+1)` would hold, a contradiction.
  4. A $(2j+1)$-cup would be a convex $(2j+1)$-gon (PROOFS §1 and Lemma 2.3).
  5. So $\mathrm{pts}(C)$ is in the class. That class is bounded, so $n\le N$.

  The even case is the same with $j$-caps and $2j$-gons. Referee note R1 asked for the finiteness step, and it is now
  stated with its source.
- **The scope sentence.** "No declaration of `MirrorOdd` states this" stays true even if "this" is read to include
  the finiteness:
  - `MirrorMain.lean` contains no cups–caps statement;
  - its only `Nat.choose` is Baek's threshold in `capacity16` (`:1532`, via `main 4`);
  - `Config.cap_cup` is used only in `C12Check` (`MirrorNine_append.lean`), not in `MirrorOdd`.

  "It is not used in this section" is still true. No rigor word was added: the claim is attributed to the classical
  theorem and to PROOFS.md, and no Lean check is claimed for it.

## 2. The fixer's dispositions

| note | source | disposition | audit |
|---|---|---|---|
| 1. citation order in Remark (2) | `mm-p1-diff.md` minor 1 | fixed | fixed: "(Lemma 2.1(b))" now follows the all-triples fact, and "(§1; see also Lemma 2.3)" follows the cup fact |
| 2. "moreover" wording in Definition (c), (d) | `mm-p1-diff.md` minor 2 | fixed | fixed as suggested in (c), and the repetition in (d) is removed. Content unchanged and still Lean-faithful |
| 3. (hM) for $M=N$ also needs $N$ finite | `mm-p1-referee.md` R1 | fixed | fixed: the finiteness sentence with the cups–caps bound and its source precedes the derivation, and "then follows" links them |

No note was declined.

**Claims in the fix log, checked.**
- **PROOFS.md §1** (l. 25-30):
  - "It is finite by the cups–caps theorem, N(n,a,b) <= C(a+b-4, a-2) (Erdős–Szekeres 1935)";
  - "A 2j-cup is a convex 2j-gon … and likewise for r'_j";
  - the range "n >= 3 and a,b >= 2".
- **Lemma 2.1, Consequences (b)** (l. 53-57): "every 3-subset of a cap is a cap triple".
- **Self-citation.** PROOFS cites itself as "Lemma 2.1(b)" in the proof of Lemma 2.3 (l. 85). Remark 1.4 of the
  section already uses this form (l. 166).
- **Lemma 2.3** (l. 79-91), direction (<=) with $U=\{a,b\}$, gives "a cup is in convex position".
- **Compile and labels.** The log's compile and label claims agree with this audit (sections 4 and 5).

## 3. Touched statements re-read against Lean

- **Definition `mm:def:config`.** I re-read:
  - `Configuration` (`ErdosSzekeres/Omission/Realization.lean:9`: fields `point`, `xOrder : StrictMono`,
    `generalPosition` for `i < j → j < k`);
  - `HasCap` (`:64`: `∃ f, StrictMono f ∧ ∀ i j l, i < j → j < l → orient … < 0`);
  - `xset`, `emb`, `sortPt`, `cfg` (`MIRRORETV/lean/MirrorMain.lean:1549, 1553, 1558, 1584`).

  All six head line numbers are exact. The definition matches Lean exactly.
- **Remark `mm:rem:hm`.** It has no Lean declaration. Its item (2) concerns the hypothesis (hM). I re-read
  `mirror_odd_general` (`:2498`) and `mirror_even_general` (`:2599`). Their hypothesis `hM` has the form
  `∀ n (c : Configuration n), ¬ c.HasCap (j+1) [resp. j] → ¬ HasConvexNGon (2*j+1) [resp. 2*j]
  (Finset.univ.image c.point) → n ≤ M`, with `hj : 2 ≤ j`. This is the (hM) of Theorems `mm:thm:odd` and
  `mm:thm:even`, and the remark's derivation targets exactly this form.
- **Unchanged statements.** No other statement, head, label or `\leanref` changed.

## 4. Map

- `sections/mm.map.tsv` is byte-identical to the snapshot.
- A script check confirms the following:
  - The 21 labelled statement environments correspond one-to-one, in order, with the 21 rows. Kind, Lean names and
    file:line agree with each head.
  - Every row has 5 fields.
  - There are 22 labels, all `mm:`-prefixed (including `mm:sec`).
  - Every `\ref` points to an own label, a contract `fd:` label (13 of them) or an `mb` export label (`mb:thm:baek`,
    `mb:thm:seven`, `mb:thm:eight`, `mb:thm:nine`).
- The `mm:rem:hm` row ("… relation to N(n,a,b) …") is still accurate.

## 5. Compile check

- **Setup.**
  - Wrapper: `build/mm_docr0audit_wrapper.tex`. Its content is identical to the contract's wrapper (`diff` against
    `build/mm_wrapper.tex` is empty).
  - Ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error mm_docr0audit_wrapper.tex` twice from `build/`.
- **Result.**
  - Both runs exited 0 and produced 13 pages.
  - The log has 0 `!` lines, 0 errors, no "Missing $", no undefined citation and no multiply defined label.
  - It has no other LaTeX or package warning.
- **Boxes.** 0 overfull boxes, so there is no minor finding from this item. There are 76 underfull boxes, from the
  section's local `\emergencystretch`, as in the previous audits; they are cosmetic.
- **Undefined references.** Only the 13 contract `fd:` labels and the 4 `mb` export labels, as expected for a
  standalone build.
- **Rendering.**
  - I rendered pages 3 and 9 (`build/mmdocr0audit/page-03.png`, `page-09.png`).
  - Definition 1.3(c), (d) and Remark 1.19(2) typeset cleanly.
  - The inline $\binom{a+b-4}{a-2}$ is set in text style and does not disturb the line spacing.
- **Files left in `build/`.**
  - `mm_docr0audit_wrapper.{tex,aux,log,out,pdf,txt}`;
  - `mm_docr0audit_pass1.out`, `mm_docr0audit_pass2.out`;
  - `mmdocr0audit/page-{03,09,10}.png`.

## 6. Other checks

- **Machine paths and tool names.** `sections/mm.tex` and `sections/mm.map.tsv` contain none.
- **Macros.** No `\newcommand`, `\usepackage` or other macro definition. The only local setting is the existing
  `\emergencystretch` group.
- **Rigor words.**
  - "verified" and "certified" do not occur.
  - "certificate(s)" refers only to the `linarith` certificates.
  - "proved" occurs only in "not proved here" and for Lean proofs.
  - The diff adds no rigor word and rounds up no label.
- **Hypotheses.** (hM) is still presented as an unproved hypothesis. The new finiteness sentence is a cited
  classical fact inside a remark that is marked as not used.
- **Export labels.** The 8 export labels are unchanged and sit on the same statements.

## 7. Findings

1. **minor (optional): Remark `mm:rem:hm`(2) cites the classical cups–caps theorem only through a project note**
   (`sections/mm.tex:681-682`).
   - **Issue:** The new sentence states a quantitative classical theorem, the bound $\binom{a+b-4}{a-2}$. Its only
     source is `MIRRORETV/PROOFS.md` §1, which in turn names "Erdős–Szekeres 1935". The document's bibliography has
     the original paper (`ES35`), and `sections/mb.tex:221-222` cites it inline for the same theorem. Contract rule 5
     asks that a cited standard fact come with a reference.
   - **Impact:** None on correctness. The statement is right, the parameters used are in range, and the remark is not
     used.
   - **Fix (optional):** "by the cups--caps theorem of Erd\H{o}s and Szekeres (1935)". Optionally also add "for
     $a,b\ge2$", the range in which PROOFS §1 defines $N$.

No blocker and no major finding:
- the diff introduces no false statement;
- every touched statement still matches its Lean declaration;
- every new claim about the records checks out in PROOFS.md;
- no rigor label is rounded up;
- no machine path or tool name appears;
- the LaTeX compiles cleanly.

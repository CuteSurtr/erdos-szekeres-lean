# Section `mm`, round doc-r0: fix log

Input: the three open minor notes under key `mm` in `build/open_minors.json`, from `reviews/mm-p1-diff.md` (2 notes)
and `reviews/mm-p1-referee.md` (1 note). Snapshot taken before editing: `snapshots/doc-r0-pre/mm.tex` and
`snapshots/doc-r0-pre/mm.map.tsv`.

Sources checked:
- `MIRRORETV/PROOFS.md` §1, lines 10-41. Caps and cups are defined there by consecutive triples. It says of N(n,a,b):
  "It is finite by the cups–caps theorem, N(n,a,b) <= C(a+b-4, a-2) (Erdős–Szekeres 1935)". It also says: "A 2j-cup
  is a convex 2j-gon, so r_j is also the largest ... and likewise for r'_j".
- `MIRRORETV/PROOFS.md` §2. Lemma 2.1, Consequences (b), lines 53-57, says "every 3-subset of a cap is a cap triple".
  Lemma 2.3 (convex position = cap + cup) proves the cup fact: it is the case U = {a,b}.
- `MIRRORETV/lean/MirrorMain.lean:1549-1594`: `xset`, `xset_card`, `emb`, `emb_mem`, `sortPt`, `sortPt_*`, `cfg`.
- `ErdosSzekeres/Omission/Realization.lean:9` (`Configuration`) and `:64` (`HasCap`).

## The notes

| # | lens | note (summary) | action | location (final file) | reason if declined |
|---|---|---|---|---|---|
| 1 | diff | Remark `mm:rem:hm`(2): "(§1 and Lemma 2.1(b))" lists the sources in reverse order. The all-triples fact is PROOFS Lemma 2.1, Consequences (b). The cup fact is in §1 (and Lemma 2.3). | fixed | `sections/mm.tex:681-689` | - |
| 2 | diff | Definition `mm:def:config`(c): "Now let $T$ be moreover $x$-injective" is awkward, and (d) repeats "moreover". | fixed | `sections/mm.tex:148-149, 157` | - |
| 3 | referee | Remark `mm:rem:hm`(2): (hM) for M = N also needs N to be finite. PROOFS §1 gets this from the cups–caps theorem, but the remark lists only two facts. | fixed | `sections/mm.tex:681-689` | - |

### Notes 1 and 3 (same sentence, fixed together)

All three claims check out against PROOFS.md as quoted above. The sentence now reads:

> These numbers are finite: by the cups--caps theorem, every set in the class that defines $N(n,a,b)$ has at most
> $\binom{a+b-4}{a-2}$ points (PROOFS.md, §1). That (hM) holds for $M$ equal to the corresponding number then
> follows, since the point set of a configuration of $n$ points is an $x$-distinct set of $n$ points in general
> position, from two facts stated in writing in PROOFS.md: consecutive clockwise triples imply that all increasing
> triples are clockwise (Lemma 2.1(b)), and a cup is in convex position (§1; see also Lemma 2.3).

- **Finiteness (note 3).** It is stated with its source and with the bound PROOFS §1 gives.
- **Parameter range.** The parameters used, N(2j+1, j+1, 2j+1) and N(2j, j, 2j) with j >= 2, lie in the range of
  PROOFS (n >= 3 and a, b >= 2), so the bound applies.
- **Citation order (note 1).** Each source now sits next to its own fact.
- **Form of the citation.** "Lemma 2.1(b)" is how PROOFS.md cites itself (in the proof of Lemma 2.3), and it is how
  the Remark after Definition `mm:def:config` already cites it.
- **Lemma 2.3.** I added it as the place where PROOFS.md proves the cup fact, which the diff reviewer pointed out.
- **One precision added while rewriting.** "The point set of a configuration is $x$-distinct" became "the point set
  of a configuration of $n$ points is an $x$-distinct set of $n$ points". This names the step n = |pts(C)| that the
  conclusion n <= M needs. C is injective because its abscissae increase strictly.
- **Unchanged.** The remark still says that the claim is not used in this section, and no rigor word was added.

### Note 2

- (c) now reads "From now on let $T$ also be $x$-injective." This is the suggested wording.
- (d) now reads "If, in addition, $T$ is in general position, ...".
- I re-read the Lean before and after the edit:
  - `xset` (`:1549`) takes only `T`.
  - `emb` (`:1553`) and `sortPt` (`:1558`) take `hx : Set.InjOn (fun p => p 0) T`.
  - `cfg` (`:1584`) takes `hx` and `hgp : GeneralPosition T`.
- The definition still matches Lean: `xset` is defined for every finite T, x-injectivity is assumed from (c) on, and
  `cfg` also needs general position. The head, the label and the `\leanref`s did not change.

## Other changes

- **Text.** None beyond the three notes. Two source lines in Remark (2) were re-wrapped; this changes only
  whitespace and does not affect the output.
- **Map.** `sections/mm.map.tsv` is unchanged and still in sync. There are 21 labelled statement environments and 21
  rows, and the kind, the Lean names and the file:line entries of every head agree with the map. No row needed a
  change because no head, label or `\leanref` changed.

## Checks

- **Diff and labels.** `diff` against the snapshot shows only the three hunks above. The labels are identical (22,
  including `mm:sec`).
- **Forbidden content.** `sections/mm.tex` and `sections/mm.map.tsv` contain no machine path and no tool name, and the section has no `\newcommand` or `\usepackage`.
- **Rigor words.** "verified" and "certified" do not occur. "proved" occurs only in the existing "not proved here"
  passages and in statements about the Lean proofs.
- **Compile.** I compiled `build/mm_wrapper.tex` twice from `build/` with `nice -n 15 pdflatex`. Both passes exit
  with 0, and the log shows:
  - 0 errors;
  - 0 overfull boxes (so none over 1pt);
  - undefined references only to `fd:` (13) and `mb:` (4) labels;
  - no undefined citation, no "Missing $" and no multiply defined label.
- **Rendering.** I looked at the rendered page 9: Remark (2) typesets cleanly, including the inline binomial.

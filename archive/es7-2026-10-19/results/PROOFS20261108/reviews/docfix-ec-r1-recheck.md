# Re-check of section ec after the whole-document review, round 1

Inputs: `reviews/docfix-ec-r1-fix.md` (fixer's log); `snapshots/docfix-r1-pre/ec.tex` and `ec.map.tsv` (before);
`sections/ec.tex` and `sections/ec.map.tsv` (after); the Lean sources and records under RES. Paths below are relative
to STAGE (sections, build, reviews) or to RES (Lean files and records).

**Verdict: pass.** The fixer addressed all six findings; none was declined. All six are resolved correctly, and the
edits introduce no blocker or major problem. This re-check adds one minor finding: the generated appendix is stale
until it is regenerated.

## 1. The six findings

| # | finding | fixer | re-check | evidence |
|---|---|---|---|---|
| 1 | xref-ocpcec, minor: the cast-angle side condition was stated only for ll:thm:reduction | fixed (both suggested fixes) | **resolved** | The Conventions (ec.tex:92-95) now name Theorem ll:thm:reduction and Lemma lg:lem:centre, items (R) and (C), with angle 2pi/m and m in N cast to R. Item (C) (ec.tex:168-172) now begins "Let m in N". This matches `centre_not_mem_of_even {S : Finset Point} {c : Point} {m : ℕ} (hm : 0 < m) (heven : Even m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S) {p} (hp : p ∈ S) (hpc : p ≠ c) : c ∉ S` (LAYERLEAN/LayerLemma.lean:582; the copy at ES7Corollaries.lean:582 is identical, lines 1-1147 of the two files coincide). The proof of ec:thm:fourfold (ec.tex:232-236) identifies rotAbout(c,2pi/4) with the m = 4 instance of (C), as Lean does with `centre_not_mem_of_even (m := 4) ... (by exact_mod_cast hinv)` (ES7Corollaries.lean:1227-1228). |
| 2 | consistency, minor: (R) wrote m(t-1) "(natural subtraction)" | fixed | **resolved** | (R) (ec.tex:161-167) now writes m·(t∸1) and defines t∸1 = max(t-1,0). This is ll's notation (ll.tex:113, 627) and meets fd's convention (fd.tex:89-90). Lean has `hcard : m * (t - 1) < (S.erase c).card` with `t : ℕ` (LayerLemma.lean:1066-1070). The two applications are right: 5·(7∸1) = 30 (ec.tex:189) and 4·(8∸1) = 28 (ec.tex:223); Lean closes both by `omega`. Remark ec:rem:orbits keeps m(t-1) with t in {7,8}, where the difference is ordinary; that is acceptable. |
| 3 | consistency, minor: "case statements" vs "case classes" | fixed | **resolved** | No section file contains "case statement" any more. ec says "case class(es)" at ec.tex:7, 97, 107, 175 and 267, as sr does (sr.tex:211) and as ar, mb and sa do. The map notes of ec:def:cases and ec:rem:cases use the same term. |
| 4 | consistency, minor: \dirn{E2} collided with trust item (E2) of the k8 note | fixed | **resolved** | ec.tex:113 now cites `E2/logs/lrat_check_soundness.md`. The file exists. It records that the unpatched build (drat-trim git 2e3b2dc) accepts the empty clause with any non-conflicting hint list, including none, which supports "unsound on the empty clause". LRATCHECK20261105/README.md:14 names this file as "the record". |
| 5 | consistency, minor: "refereed" next to the document's "(not refereed)" | fixed | **resolved** | Both occurrences now say "refereed within the project" (ec.tex:121, 130). A new sentence (ec.tex:137-138) says that all the reviews, audits and refereeing in the list were internal and that none is an external peer review. This is compatible with ar.tex:737 ("reviewed or audited within the project"). |
| 6 | claims, minor: the records' "refereed" was reported without saying that the review was internal and same-day | fixed (with 5) | **resolved** | C2ENC/perturbation.md:3-5: "Written 1 November 2026 (UTC) ... and refereed with proof.md the same day (referee/NOTES.md §4: correct)". C2ENC/referee/NOTES.md: "Refereed 1 November 2026 (UTC)", and its §4 says "perturbation.md: correct." The text "refereed within the project on the day it was written: C2ENC/referee/NOTES.md, Section 4" is therefore accurate. C4CUT/README.md:16-19: "Encoder soundness: written proof, refereed ... The independent review of 1 November (review/)". C4CUT/review/README.md is titled "Independent review of C4CUT (1 November 2026)" and checks SYM5/symcnf_layers.py with m = 4 clause family by clause family, so "the review of 1 November 2026, C4CUT/review/README.md" is accurate. That the reviews are internal is supported by three records. AUDIT3/README.md describes a project-run audit (local runs against the project repository). WRITEUP/note/symmetric_extremal.tex:116-117 defines the project's label "Written proof (not refereed)" as "checked by at least one independent internal review, not refereed by a journal". WRITEUP/SYMMETRIC.md:214-219 lists these proofs under "Written proofs, refereed or audited (not Lean-checked)". The new sentence is therefore true, and it lowers the claim rather than raising it. |

## 2. Each hunk checked as a referee

`diff -u snapshots/docfix-r1-pre/ec.tex sections/ec.tex` has 10 hunks; `ec.map.tsv` has 1 (two rows).

- **ec.tex:7, 97, 107, 175, 267.** "case statement(s)" became "case class(es)". This is wording only. The definition
  text of ec:def:cases is unchanged and still matches `Fivefold35` and `Fourfold32` (ES7Corollaries.lean:1157,
  1164: GeneralPosition, card = 35/32, c ∉ S, Invariant under rotAbout c (2 * Real.pi / 5)/(… / 4), conclusion
  HasConvexNGon 7 S).
- **ec.tex:92-95 (Conventions).** The statement is true. Both cited statements have angle `2 * Real.pi / m` with
  `m : ℕ`. The Lean proofs use `exact_mod_cast` at ES7Corollaries.lean:1175, 1177, 1208, 1210 and 1228.
- **ec.tex:113.** The record citation is correct (see finding 4).
- **ec.tex:118-140.** Apart from the two "refereed within the project" phrases and the new sentence, the old content
  is unchanged (compared word by word). The claims about the records are true (see finding 6).
- **ec.tex:161-167, item (R).** It matches `convexNGon_of_layers` (LayerLemma.lean:1066) exactly: the order of
  `{m K t : ℕ}`, `0 < m`, `K ≤ 2 * m`, the premise H (∀ T c, GeneralPosition T → c ∉ T → Invariant … T → T.card =
  m * t → HasConvexNGon K T), and then S, c, GeneralPosition S, Invariant, `m * (t - 1) < (S.erase c).card` ⊢
  HasConvexNGon K S. The truncated subtraction is now explicit.
- **ec.tex:168-172, item (C).** It matches `centre_not_mem_of_even` (see finding 1). The text quantifies m before S and
  c, while Lean has {S} {c} {m}; these universal quantifiers are independent, so the statements are equivalent.
  "Some p ∈ S with p ≠ c" is equivalent to Lean's ∀ {p}, p ∈ S → p ≠ c → c ∉ S. The parenthetical half-turn argument
  is unchanged and correct.
- **ec.tex:189 and 223.** The arithmetic 5·6 = 30 and 4·7 = 28 is correct.
- **ec.tex:232-237, proof of ec:thm:fourfold.** Every hypothesis of (C) is discharged: 0 < 4, 4 is even, general
  position, invariance (with the cast identification), and p ∈ S with p ≠ c from the previous sentence. The rest is
  unchanged and correct.
- **ec.map.tsv, rows ec:def:cases and ec:rem:cases.** Only the notes changed. The file is ASCII, every row has 5
  fields, and its 41 rows match the 41 statement environments with the same kinds. No label was added, removed or
  renamed (47 ec: labels).

Rigor labels: nothing is rounded up. The hunks contain no "verified", "certified" or "proved". "Refereed within the
project" together with "none of them is an external peer review" is weaker than the old wording.
Machine paths and tool names: none in ec.tex or ec.map.tsv (grep for /private, /Users, /home, /tmp and the usual
tool names).
LaTeX: no new macro or package. `\mathbin{\dot{-}}` is used as in ll. No new `\lean`/`\dirn` argument contains
spaces. The only new `\ref`s are ll:thm:reduction and lg:lem:centre, both export labels.

## 3. Compile

The wrapper `build/ec_recheck_r1_wrapper.tex` has the contract content. It was run twice from `build/` with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`:
- both runs exited 0, with 0 errors and 0 "Missing" messages;
- **0 overfull boxes**, and 21 underfull boxes, all in statement heads with long Lean names (the fixer reports the same
  count for the snapshot);
- the 18 undefined references are all fd: labels or export labels of ll, lg, oc and sr, as expected for a standalone
  build;
- the PDF has 12 pages. I looked at page 3, which holds (R), (C) and Theorems 1.3-1.7: the truncated minus renders as
  in ll, and `E2/logs/lrat_check_soundness.md` renders with its underscores.

## 4. Finding of this re-check

- **minor (pipeline): `appendix_map.tex:210-211` is stale.** The appendix was generated at 20:03, before the map edit
  at 20:40. Its rows for ec:def:cases and ec:rem:cases still carry the old notes. These are not wrong: they contain no
  "case statement" wording; they only lack "case classes" and the clause saying the reviews were internal. Fix:
  regenerate with `python3 tools/make_appendix.py` after the section fixes of this round, as the fixer's log notes.

## 5. Observations (not findings)

- C2ENC/perturbation.md was revised after the refereeing, in answer to referee note R3 (its header says so, and
  C2ENC/README.md says that the referee's hashes are those of the refereed versions). ec reports the record's own
  status ("recorded there as …"), so the sentence is accurate; no change is needed.
- These items were not assigned to this fixer and were left open: consistency M1 (the "computer-assisted" label of
  ec:prop:ex341), consistency m7 and claims F11 ("conditional" in theorem heads and in Coverage).

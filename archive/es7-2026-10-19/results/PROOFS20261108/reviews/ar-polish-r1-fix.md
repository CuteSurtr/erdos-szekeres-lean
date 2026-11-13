# Section ar, polish round 1: fix log

Inputs: `reviews/ar-r1-fidelity.md`, `reviews/ar-r1-rigor.md`, `reviews/ar-r1-adversarial.md`, `reviews/ar-r1-claims.md`,
`reviews/ar-writer-concerns.md`. Snapshot before editing: `snapshots/polish-r1-pre/ar.tex`, `snapshots/polish-r1-pre/ar.map.tsv`.
Line numbers below refer to `sections/ar.tex` after this round (797 lines). Paths are relative to STAGE; record paths
are relative to RES.

## Findings

| report, id | summary | action | location after the fix | reason (declined only) |
|---|---|---|---|---|
| fidelity F1 | The axioms file was said to be the 1533 lines plus nine `#print axioms` lines and one `#check` line; line 1534 is blank. | fixed | ar.tex:47-49 ("followed by a blank line, nine ... and one ..."); same wording in Coverage, ar.tex:791-792 | |
| fidelity F2 | "The Lean proofs ... pass heptagon_of_nontrivial_isometry ... as hE" is wrong for (b), whose Lean proof applies (a); also "one-line" (they are two-line terms). | fixed | ar.tex:688-691: (a), (c), (d), (e) pass the isometry theorem as hE and prove 3 <= 33 by norm_num; (b) passes no hE and applies (a) after turning the inclusion into maps-into; "each a two-line term" | |
| fidelity F3 | "Relation to Lean" of Proposition ar:prop:averaging omits hgp' (orientation factor), hTinj, hTiinj. | fixed | ar.tex:552-557: lists the inverse identities, hTinj and hTiinj, hnT, the factor st-(beta/s)*0 used only inside hgp' (via generalPosition_image_of_orient and orient_lin2), hiso, hinv' | |
| fidelity F4 | "word for word" overstates Definition ar:def:E (variables renamed, IsEucIsometry and Invariant unfolded). | fixed | ar.tex:471-475: "up to two changes of notation" (bound variables S, g renamed S', h; the two predicates unfolded); quantifiers, premises, their order and conclusion are Lean's | |
| fidelity F5 | f is an affine map in Theorem ar:thm:main(c) and a real in (e); b is a vector in (d) and a real in (e). | fixed | ar.tex:665: "(in this part b and f are real numbers)" | |
| fidelity F6 | References to mb: labels, in case the task note restricts refs to sr: and fd:. | declined (no change needed) | ar.tex:708, 711, 713, 795 (unchanged refs) | The contract allows \ref to every export label of another section; mb:thm:baek, mb:thm:classes and mb:thm:main3 are export labels in the contract table and are defined in sections/mb.tex. |
| rigor m1 | Lean-proof summary of ar:thm:main wrong for (b). | duplicate of fidelity F2 | ar.tex:688-691 | |
| rigor m2 | Letter reuse: b as lin2 parameter in the proofs of ar:lem:orient-affine and ar:prop:averaging(b), where b is the translation; matrix N in "M(Nz)=(MN)z" vs the threshold N; s as finite set in ar:lem:cp-affine vs s = sqrt(alpha); g_A, g_B, g_C vs the map g. | fixed (first three); declined (g_A part) | ar.tex:363-366 ("the entries L00, L01, L10, L11 in place of the four parameters of lin2"); ar.tex:521-523 ("applied to T = lin2(s, beta/s, 0, t)"); ar.tex:89-90 ("M(M'z) = (MM')z for matrices M, M'"); ar.tex:427-453 (finite set renamed S in statement and proof) | g_A(A), g_B(A), g_C(A) follow the Lean names gA, gB, gC, always carry a subscript and a matrix argument, and occur only in Definitions ar:def:gram, ar:def:avgq and Lemmas ar:lem:nsq-mulvec, ar:lem:avgq-eq, where no map g appears; renaming would break the correspondence with Lean without removing any ambiguity. |
| rigor m3 | "Relation to Lean" omits hgp'. | duplicate of fidelity F3 | ar.tex:552-557 | |
| rigor m4 | "Two affine equivalences with the same map are equal" justified only by the Mathlib name. | fixed | ar.tex:129-131: the linear part is determined by the map, f_lin(v) = f(v) - f(0) (defining property with p = 0) | |
| rigor m5 | Overview: "permutes the finite set, so L^m = 1" omits the three non-collinear points. | fixed | ar.tex:17-19: S contains three non-collinear points (general position, at least N >= 3 points), so a power g^m fixes them, and then L^m = 1 | |
| rigor m6 | Remark ar:rem:classes lists only part of what supplies HalfTurn34 and Threefold33. | fixed | ar.tex:694-742: chain records (C2FINAL with C2C34 and C2P-C2P5; C3FINAL; SYM5) and four kinds of evidence: SAT certificates (cake_lpr verdicts, deleted proofs, re-solves); written proofs reviewed or audited within the project (encoders, reductions A and B, the C3-S normal form, Lemma 5 and Lemma H6M, perturbation argument; full list in WRITEUP/SYMMETRIC.md §3); exact compositions with the Lean-checked bookkeeping (Theorems cb:thm:c3, cb:thm:c2) and the record matching outside Lean; the class-to-formula match checked by reading (SYMLEAN/README.md §6); pointer to WRITEUP/SYMMETRIC.md §4 for the remaining caveats | |
| rigor m7 | "word for word" overstates. | duplicate of fidelity F4 | ar.tex:471-475 | |
| rigor m8 | Blank line 1534 of the axioms file not mentioned. | duplicate of fidelity F1 | ar.tex:47-49 | |
| adversarial F1 | Overview sentence omits the spanning hypothesis (counterexample S = {0}, g(p) = 2p). | duplicate of rigor m5 | ar.tex:17-19 | |
| adversarial F2 | Closing sentence of the proof of ar:thm:main over-generalises. | duplicate of fidelity F2 | ar.tex:688-691 | |
| adversarial F3 | Axioms file description omits the blank line. | duplicate of fidelity F1 | ar.tex:47-49 | |
| adversarial F4 | "word for word" overstates. | duplicate of fidelity F4 | ar.tex:471-475 | |
| claims F1 | Lean-proof summary wrong for (b). | duplicate of fidelity F2 | ar.tex:688-691 | |
| claims F2 | Introduction: "a hypothesis ... (a parameter), not a claim of the project" can be misread (for N = 33, n = 7 it is Theorem sr:thm:main). | fixed | ar.tex:8-12: "a hypothesis of the transfer (a parameter of the theorem), so the transfer is an implication and asserts neither statement on its own"; "the Euclidean statement supplied by Theorem sr:thm:main" | |
| claims F3 | "word for word" overstates. | duplicate of fidelity F4 | ar.tex:471-475 | |
| claims F4 | Run date and exit codes come from SYMLEAN/logs/runs.tsv, not from the .out files (plus the blank-line note). | fixed (blank-line note: duplicate of fidelity F1) | ar.tex:50-51 (new bullet: runs.tsv records that AffineReduction.lean and AffineReductionAxioms.lean were each compiled on 1 November 2026 with exit code 0); ar.tex:52-53 and 62-63 (date and exit code removed from the .out bullets) | |
| claims F5 | "written soundness proofs of the encoders (not refereed)" does not match the records ("reviewed"; C2ENC "refereed" by an internal referee). | fixed | ar.tex:725-729: "Written proofs, reviewed or audited within the project (listed in WRITEUP/SYMMETRIC.md, §3)", the records' own level; no label rounded up | |
| claims F6 | Remark names only C2FINAL, C3FINAL, SYM5; the certificate chains are in SYMLEAN/README.md §5. | fixed (same action as rigor m6) | ar.tex:714-716 ("C2FINAL (with C2C34 and C2P-C2P5), C3FINAL and SYM5"), ar.tex:725-734 | |
| claims F7 | Map rows with several names use ", "; most maps (fd, ll, mb, mm, oc, pc, sr) use "; ". | fixed | sections/ar.map.tsv: columns 3 and 4 of the 10 multi-name rows now use "; "; notes unchanged; 31 lines, 5 fields each | |
| claims F8 | `\begingroup\sloppy\emergencystretch=\linewidth` gives 68 underfull warnings and stretched lines (Sources paragraph; heads with several \leanref). | partly fixed, partly declined | Sources paragraph split into a list (ar.tex:25-41) and its last sentence rephrased; mirror bullet of Remark ar:rem:classes reordered (ar.tex:706-708). Group kept at ar.tex:2 and 797. | Group kept: the preamble's new statement tolerance does not suffice here. Tested on scratch copies: without the group 14 overfull boxes (up to 75pt, statement heads and one Coverage item); `\sloppy` alone 13 overfull; `\emergencystretch` of 0.3, 0.5 or 1 linewidth without `\sloppy` 0 overfull but 80, 78, 77 underfull; the current group 0 overfull and the fewest underfull (68 now). The stretched multi-reference heads follow from the contract's head format (several full Lean names) and from amsthm setting the head in a box, where the url break points are lost; changing that needs a preamble-level change (see the note at the end), which a section may not make. |
| claims F9 | f is a real number in ar:thm:main(e) but an affine map in (c). | duplicate of fidelity F5 | ar.tex:665 | |
| writer concerns, item 1 | amsthm boxes the heads; the section needs its own sloppy group. | addressed under claims F8 | ar.tex:2 | |
| writer concerns, item 2 | `\lean{}` drops spaces and breaks on non-ASCII. | no change needed | | Followed throughout (Greek letters kept out of `\lean{}`, also in the new "Relation to Lean" text). |
| writer concerns, item 3 and contract discrepancy 1 | mb: refs vs the narrower task text. | duplicate of fidelity F6 | | |
| writer concerns, item 4 | Proposition ar:prop:averaging goes beyond Lean. | no change needed | ar.tex:552-557, Remark ar:rem:hE(2) | Already stated in the proof and in Remark ar:rem:hE(2); the "Relation to Lean" list is now complete (fidelity F3). |
| writer concerns, item 5 | Rigor evidence relies on recorded logs of 1 November 2026. | no change needed | ar.tex:44-68 | The text says "recorded output" and now cites runs.tsv for the run (claims F4). |
| writer concerns, item 6 | Class-status remark used neutral wording because later notes question lrat-check. | fixed | ar.tex:718-724 | The remark now says that every certificate used carries a recorded cake_lpr acceptance, that cake_lpr is the only checker in the trust base since the revision of 6 November 2026 (WRITEUP/SYMMETRIC.md §3; before it both checkers were trusted, checked in the history of that file), lrat-check a secondary check, and that SYMLEAN/README.md §9 (last changed 2 November) predates the revision. |
| writer concerns, contract discrepancy 2 | fd:lem:affine-cp is phrased for injective maps; the hull identity holds for all affine maps. | no change needed | | No effect on correctness; Step 1 of ar:lem:cp-affine proves the identity without injectivity. |
| writer concerns, overfull list | None in the full build. | confirmed | | Standalone build: 0 overfull boxes. Full document built in a private output directory: 0 overfull boxes in the ar part, 0 undefined references. |

## Other changes

1. Layout rule (statement body must not begin with a list): lead sentences added to Remark ar:rem:hE (ar.tex:597-598)
   and Remark ar:rem:scope (ar.tex:745).
2. Introduction, last sentence of the overview (ar.tex:22-23): "T preserves general position, cardinality and convex
   position" replaced by "T preserves general position and cardinality, and T^{-1} carries n points of T(S) in convex
   position back to n points of S in convex position", which is what the proof uses.
3. Conventions (ar.tex:93-96): a note that Nat.iterate is defined by g^{k+1} = g^k o g, while the text uses
   g^{k+1}(p) = g(g^k(p)), the lemma Function.iterate_succ_apply' used by the Lean proof of iterate_sub_of_affine
   (the file opens Function, line 56). Prompted by the fidelity review's remark in §1.1 (no finding).
4. Proposition ar:prop:averaging(a) (ar.tex:507-509): the base case r = 0 of the common-period induction is stated
   (the rigor review, check 7, noted it was implicit).
5. Lemma ar:lem:cp-affine, Step 2 (ar.tex:449-450): "By this identity and Step 1" names both facts used for the
   equality of the two hulls.
6. Rigor and axioms (ar.tex:64-66): "the #check line of the log" corrected to "the output of the #check line, in the
   same log as the axioms" (the #check line is in the .lean file).
7. Remark ar:rem:classes: sources extended to SYMLEAN/README.md §§5, 6, 9 and WRITEUP/SYMMETRIC.md §§1, 3, 4
   (ar.tex:703-704); the mirror bullet now says the mirror classes come from Baek's theorem "and the mirror reduction"
   (SYMLEAN/README.md, Status); new references to Theorems cb:thm:c3 and cb:thm:c2 (export labels of section cb).
   Checked and deliberately not added: the caveat that 60 orbit facts and five covers of HalfTurn34 rested on local
   records without tool provenance, because C2RECHECK §4 and §6 report all 65 re-solved and accepted by both checkers.
8. Coverage (ar.tex:791-792): the description of SYMLEAN/AffineReductionAxioms.lean matches the corrected one.

No statement environment was added, removed or retitled; all 31 labels are unchanged; the two edited statements
(ar:lem:cp-affine: bound variable renamed; ar:thm:main(e): a parenthesis added) still match their Lean declarations
(SYMLEAN/AffineReduction.lean:1263 and :1521). The map was re-checked against the 30 statement heads (labels, kinds,
names, file:line, order): no mismatch.

## Compile check

- `build/ar_wrapper.tex`, two runs of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` from `build/`:
  exit 0 both times, 11 pages, no errors, 0 overfull boxes, 68 underfull boxes (68 before this round).
- Undefined references, all export labels of other sections: fd:def:{cp,gp,inv,ngon,orient,point},
  fd:lem:{affine-cp,affine-orient,collinear,cp-hull}, sr:def:classes, sr:def:iso, sr:thm:main, sr:thm:variant,
  mb:thm:baek, mb:thm:classes, mb:thm:main3, cb:thm:c2, cb:thm:c3 (each defined in its section file).
- Full document (`proofs.tex`, output directory `build/ar_full`): exit 0 twice, 143 pages, no errors, no undefined
  references, 0 overfull boxes in the ar part.

## Note for the preamble maintainer (macro request, not acted on)

Statement heads with several `\leanref`s are visibly stretched (for example Corollary ar:cor:transfer-forms and
Theorem ar:thm:main), because amsthm builds the head in a box where the url break points of `\nolinkurl` are lost, so
each full Lean name is one unbreakable chunk. A preamble-level `\leanref` that inserts explicit break points (for
example after the dots of the namespace) would let these heads break normally and would make the section-local sloppy
group unnecessary.

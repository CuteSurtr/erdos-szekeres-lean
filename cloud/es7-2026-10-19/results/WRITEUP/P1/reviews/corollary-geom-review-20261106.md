> Archived 6 November 2026 from the session in which it was written. It records one check, by a reviewer within the
> same session, of a draft of the corrected proof of Corollary k8s:cor:geom (written with τ for the translation and A
> for its linear part); its wording remarks were then applied in commit f2a462b67, whose final text was not re-checked.
> It is not an independent or external review. The paper still lists that proof as having had no internal review (G4);
> see README.md, open item 5. The scratch path cited below (`/tmp/claude-1000/.../rev-noty12/conj.py`) is a temporary
> session directory that is not kept. Line numbers refer to the files as they were before the audit edits of the same
> day; the P1 copy has since gained 9 lines before the corollary (now about lines 807-820). The text below is
> unchanged.

**Review of the corollary edit: k8_soundness_p1.tex:798-811 (same text in note/k8_soundness.tex:785-798)**

The new argument for part (a) is correct and complete. I found no mathematical defect, and part (b) also holds. There are three small wording issues, all low severity, listed below.

**Checks against the definitions**
- **Rotation direction and angle match.** `rotAbout c θ p = c + [[cos θ, −sin θ],[sin θ, cos θ]](p − c)` (LAYERLEAN/LayerLemma.lean:298-300). Sixfold66 uses `rotAbout c (2π/6)` (LayerLemma.lean:1102-1104). k8_soundness_p1.tex:63-64 defines ρ as the counterclockwise rotation `rotAbout O (2π/m)`.
  - So `τR_cτ⁻¹(y) = R_c(y+c) − c = rotAbout O (2π/6) y = ρ(y)` holds exactly, coordinate by coordinate.
  - A small numeric check agrees to 3.6e-15 for m = 6 and 7, and orient(O, e1, ρe1) > 0 confirms the counterclockwise direction (/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/rev-noty12/conj.py).
  - The step would hold even with the opposite direction: invariance under ρ⁻¹ of a finite set gives invariance under ρ.
- **"R_c maps T into itself" is the right hypothesis.** It is exactly `Invariant` (LayerLemma.lean:105, `∀ p ∈ S, f p ∈ S`). Upgrading it to R_cT = T needs only injectivity (`rotAbout_injective`, LayerLemma.lean:316), which the text cites. Then ρ(τT) = τR_cT = τT.
- **Each condition of Definition k8s:def:adm (lines 102-105) holds:**
  - m = 6 ≥ 3, 4 ≤ K = 8 ≤ 12, t = 11, |τT| = 66 = 6·11 (τ is injective).
  - O ∉ τT because O = τ(c) and c ∉ T.
  - General position and 8-free follow from the first part of Lemma k8s:lem:affine (lines 113-115), which is stated for every affine bijection.
  - "8-free" is the paper's ¬HasConvexNGon 8, which is exactly the negated conclusion of Sixfold66 (`t.card = n`, ErdosSzekeres/Definitions.lean:21-22).
  - The parenthetical saying the last clause (g(O) = O) is not used is accurate.
- **Rest of the chain:** Theorem k8s:thm:sound needs t ≥ 3 (11 is fine) and m ∈ {6,7} for encoder A (6 is fine). Lemma k8s:lem:cube is applied with F = base + Y(1,2) and five literals, which is right.
- **Part (b) "by the same" holds.** Sevenfold70 (LayerLemma.lean:1107-1109) has the same shape with 2π/7. The same conjugation gives ρ₇, and 70 = 7·10 with K = 8 ≤ 14. The hypothesis "F_A + H(1) unsat" contradicts Theorem (b). "F_B unsat" contradicts Theorem (a), because a model of F_B + H(1) is a model of F_B.
- **The PDF was rebuilt after the edit** (tex 12:48:25, pdf/log 12:48:38). p1.log has no undefined or multiply-defined references.

**Wording issues, ranked**
1. **Notation clashes.** In the edit, τ is the translation and A is its linear part. Elsewhere in the paper:
   - τ is the reflection in Lemma k8s:lem:refl (lines 612, 620).
   - The proof of Theorem k8s:thm:sound, which this proof invokes, writes "replacing S by τS" (line 667).
   - p1.tex:309 uses τ = π/m.
   - A clashes with encoder A / F_A in the same corollary (lines 787, 806).

   Fix: rename the translation (e.g. σ(x) = x − c). Replace A by writing `R_c(x) = c + ρ(x − c)`, which is immediate from the definition of `rotAbout` (LayerLemma.lean:298-300). Then σR_cσ⁻¹ = ρ needs no separate "linear part" step.
2. **Part (b) says "is the same", but the cube step does not carry over.** Lemma k8s:lem:cube and the "32 cube formulas" do not apply, because the hypothesis of (b) is unsatisfiability of the whole formula. Fix (line 807-809): "(b) Replace 2π/6, 66, (6,8,11), Y(1,2) by 2π/7, 70, (7,8,10), H(1). No cube step is needed: F_A + H(1) unsat contradicts Theorem (b); F_B unsat contradicts Theorem (a), since a model of F_B + H(1) is a model of F_B."
3. **Cosmetic (optional).** In the proof, name R_c explicitly as "`rotAbout c (2π/6)`, the rotation in \lean{Sixfold66}" so the direction is tied to the Lean statement. Line 169 (note:156), "after translating the centre to O, Sixfold66 says…", could add "(Corollary~\ref{k8s:cor:geom})". It is correct as it stands.

**Other uses of Lemma k8s:lem:affine with a g that does not fix O: none remain**
- k8_soundness_p1.tex:278 and :666 use a rotation about O, which fixes O and commutes with ρ.
- :620 uses the reflection (x,y)↦(x,−y), which is linear, fixes O, and satisfies τρτ⁻¹ = ρ⁻¹.
- :832 and :871 are only listings in the trust table and gap list.
- p1.tex never cites k8s:lem:affine. p1.tex:257 ("after translating its centre to O") is a definition, and Remark rem:affine (p1.tex:144-153) has its own argument with T linear.
- In the note, the same uses are at note/k8_soundness.tex:265, 607, 653, all fine. The note's corollary and proof (770-799) match the P1 version word for word.

I did not touch the c6upper-noty12 job or its directory.
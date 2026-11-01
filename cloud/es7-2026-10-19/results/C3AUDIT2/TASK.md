# C3AUDIT2 task: adversarial check of the H6 mirror reduction (Lemma H6M)

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} by those values; follow everything else exactly.

General rules: as in `results/C3AUDIT/TASK.md` (paths under `cloud/es7-2026-10-19/`), with `results/C3AUDIT2/` as your only directory and the fallback branch `es7-fallback-c3audit2`. In particular: commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com> (check `git var GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`), `env.txt` pushed at once, plain commit messages with no AI co-author or attribution trailers, `git pull --rebase --autostash` before every push, notes pushed at least every 30 minutes, the last 10 minutes for `REPORT.md`, do not end your turn while work is running, do not modify anything outside your directory, and never write `sorry` or `admit` in any Lean file.

## The claim under review

`results/C3PLAN/PLAN.md` §3a states Lemma H6M: for a top case H6(a, s) of the 3-fold class (m = 11), the map φ(r, σ) = ((a − r) mod m, σ ⊕ [r < a] ⊕ [s = 0]) on residues r ∉ {0, a} sends the layer path of a set S to the layer path of its mirror image M(S), canonically relabelled, in the same case H6(a, s). Its corollary keeps only the layer-2 options O with key(O) ≤ key(φ(O)) below every H6 case (81 of 153), which would cut the 1,530 H6 roots to 810. The canonical labelling, the layers and the mirror lemma for H3 are in `results/C3-S/soundness.md` (Lemmas 1 to 5) and `results/C3-S/tools/hullcase.py`. P1's validation: `results/C3PLAN/scripts/validate_mirror_h6.py`, `logs/validate_mirror_h6.jsonl`.

## What to do

Default to suspicion; the reduction must not be used unless it is right.
1. Re-derive the proof line by line: the relabelling after the reflection, the sweep of the line l to the new label 0, which σ values flip, the case a' = m − a ≥ 6 and the return to a ≤ 5, the point reflection p ↦ −p when s = 0, the claim that every deeper layer maps by the same φ, one-orbit layers, and that φ is an involution on the options. Check the corollary: why keeping one option of each φ-pair covers the class (as Lemma 5 does for H3), including self-mirror options, and that the key comparison picks exactly one of each pair.
2. Write your own independent test (not P1's code, not the repository's canonicalizer): random exact-coordinate 3-fold-symmetric sets with a hexagonal hull (two orbits on the hull), m = 7, 9 and 11, at least 3,000 sets covering all 10 H6 cases, canonicalized from scratch by your code; for each, compute the layer path of S and of M(S) and check the prediction of φ. Include mutations that must fail (no σ flip, wrong residue map, no [s = 0] term).
3. Check that the column `h6m_kept` of `results/C3W3/lists/A_s0.tsv` and `C_s1two.tsv` equals the corollary's rule.

`results/C3AUDIT2/REPORT.md` and final message: a clear verdict (accept / reject / accept with conditions), the findings with file and line, the test counts, and what you could not check.

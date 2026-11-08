# Writer report for section `sr` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- Preamble/layout, affects every section: amsthm builds each statement head in an \sbox, which is restricted horizontal mode. There TeX does not insert the math penalties that url.sty uses as break points, so \lean and \dirn names inside a \leanref head cannot break. In sr all 39 remaining overfull boxes (up to about 190pt) are in statement heads, and the PDF cuts head text at the right margin. Body text breaks normally. Tested: adding `\tolerance=10000 \emergencystretch=6em` to the preamble (via a test wrapper outside STAGE) gives 0 overfull boxes for sr. The preamble was not changed.
- Two further formatting traps for every writer. (1) \lean uses \nolinkurl, which drops spaces: \lean{HasConvexNGon 7 S} prints as HasConvexNGon7S. In sr every expression containing spaces uses \texttt instead. (2) A statement body that starts directly with \begin{enumerate} turns the whole head into one unbreakable box, overflowing by more than 600pt. Every sr statement now starts with a sentence.
- isometry_complex_cases (sr:thm:structure(a)) is proved by an elementary argument: inner products are preserved, giving an orthonormal frame H(1), H(i) = +-i H(1). It does not follow the Lean route (Mathlib Isometry.affineIsometryOfStrictConvexSpace and linear_isometry_complex), and the text says so. orbit_select and orbit_select_minimalPeriod share one written induction (sr:lem:orbit-core) instead of repeating it as Lean does.
- IsEucIsometry.injective is outside the dependency cone of every printed theorem, so its evidence is the empty compile log plus a source scan (no axiom declarations, no decide or native_decide in the file or the imported modules). mirrorOneAxis33_of_exclusionLine is covered through the axioms print of the review theorem mirrorOneAxis33_iff_exclusionLine (logs/ReviewSanity.out).
- Remark sr:rem:records names the records and rigor labels behind each class (C2FINAL/C2C34/C2P*/C2ENC; C3FINAL/C3-S/C3a/C3SPOT/perturbation; SYM5; SYMLEAN/mirror and SYMZ; C4CUT). It is based on SYMLEAN/README.md section 5 and C2ENC/class_table.md; I did not re-verify these records.
- Only \ref targets outside sr: the fd: labels, plus mb:thm:classes, mb:thm:main3 and ar:thm:main. The mb and ar targets appear only in remarks and the dependencies paragraph. The contract allows them; the task text mentioned only fd: labels.

## contract_discrepancies
- The contract's mandated head format (one or more \leanref{...}{...} in the optional argument of an amsthm environment) does not typeset well with the mandated preamble. The heads cannot break inside names, so long \leanref lists overflow the margin (see concerns). The format was followed exactly; the fix belongs in the preamble.
- The task text says 'You may \ref fd: labels', while the contract also allows other sections' export labels. sr uses mb:thm:classes, mb:thm:main3 and ar:thm:main, all listed export labels, in remarks only.

## not_covered
- None of the 72 declarations of SYMLEAN/SymmetricReduction.lean is omitted.
- Deliberately out of scope and named in the Coverage paragraph: SYMLEAN/SymmetricReductionAxioms.lean (verbatim copy plus two #print axioms lines); lines 1-1058 of SYMLEAN/AffineReduction.lean (verbatim copy; the affine part belongs to section ar); the audit files SYMLEAN/review/ReviewSanity.lean, VariantChecks.lean and SupMetric.lean (only mentioned in remarks); SYMLEAN/mirror (section mb).

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/sr.tex as of the snapshot)
- 19.9pt in paragraph at lines 482--483
- 22.2pt in paragraph at lines 319--320
- 45.1pt in paragraph at lines 972--973
- 48.5pt in paragraph at lines 894--898
- 61.4pt in paragraph at lines 602--604
- 75.3pt in paragraph at lines 929--935

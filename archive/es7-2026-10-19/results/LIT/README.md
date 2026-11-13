# LIT: literature check (task at 3d83517, H = 1.25 h, run 2026-10-21)

- `RELATED.md`: known values and bounds of ES(n) for n ≤ 8, prior computer-assisted and formal
  work, prior work on symmetric configurations, answers to questions (a) to (c), and what to cite.
  §6 records a second search, on 6 November 2026: what was read in full and what only at abstract level, and its
  findings (no symmetric k = 8 work found; upper bounds unchanged; the GLitchfield Lean repository; drat-trim
  issue #42 and pull request #43; classical antecedents of the chord lemma and the certificate methods).
- `references.bib`: BibTeX for every source cited in `RELATED.md` §§1–5. Of the sources added in §6 (6 November),
  Mackey's thesis, Georgiev et al. and Miyata–Moriyama–Imai have entries; the others are cited inline there.
- `searches.tsv`: every search run on 21 October (the 6 November searches are recorded in that check's session
  journal, not here).

Limitation (21 October search; on 6 November direct fetches worked): direct page fetches to arXiv,
Semantic Scholar, DBLP, Zenodo, MathOverflow, Google Scholar and alphaXiv were refused by the session's network
proxy (HTTP 403). Sources were read through the abstracts and snippets that WebSearch returned. Section-level
details come from the repository survey `docs/RELATED_WORK_2026-10-14.md` and are marked as such.

Short answers (details and wording in `RELATED.md` §4; the 6 November search in §6 does not change them):
- (a) We did not find prior work stating that reflection-invariant 33-point sets in general
  position contain a convex 7-gon. The closest is 4-fold rotational symmetry at 32 points
  (Subercaseaux–Mackey–Qian–Heule 2025).
- (b) We did not find prior work restricting the symmetries of 33-point 7-gon-free sets, or
  excluding the D3 case.
- (c) The best peer-reviewed bound is ES(8) ≤ 408 (Mojarrad–Vlachos 2016, our arithmetic). The
  best earlier public, unreviewed bound known to us is ES(8) ≤ 319 (Schroeder, Zenodo, Sept 2026).
  We did not find prior work stating ES(8) ≤ 311.

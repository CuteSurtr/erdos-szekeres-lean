# LIT: literature check (task at 3d83517, H = 1.25 h, run 2026-10-21)

- `RELATED.md`: known values and bounds of ES(n) for n ≤ 8, prior computer-assisted and formal
  work, prior work on symmetric configurations, answers to questions (a) to (c), and what to cite.
- `references.bib`: BibTeX for every source cited in `RELATED.md`.
- `searches.tsv`: every search run (date, engine, query, useful results).

Limitation: direct page fetches to arXiv, Semantic Scholar, DBLP, Zenodo, MathOverflow, Google
Scholar and alphaXiv were refused by the session's network proxy (HTTP 403). Sources were read
through the abstracts and snippets that WebSearch returned. Section-level details come from the
repository survey `docs/RELATED_WORK_2026-10-14.md` and are marked as such.

Short answers (details and wording in `RELATED.md` §4):
- (a) We did not find prior work stating that reflection-invariant 33-point sets in general
  position contain a convex 7-gon. The closest is 4-fold rotational symmetry at 32 points
  (Subercaseaux–Mackey–Qian–Heule 2025).
- (b) We did not find prior work restricting the symmetries of 33-point 7-gon-free sets, or
  excluding the D3 case.
- (c) The best peer-reviewed bound is ES(8) ≤ 408 (Mojarrad–Vlachos 2016, our arithmetic). The
  best earlier public, unreviewed bound known to us is ES(8) ≤ 319 (Schroeder, Zenodo, Sept 2026).
  We did not find prior work stating ES(8) ≤ 311.

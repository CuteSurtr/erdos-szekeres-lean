# SCRUB20261107: commit trailers removed from the branch history (7 November 2026)

**What changed.** Of the 46 commits of `es7-night-2026-11-01` after `28e2c0bde` (4 to 7 November 2026), 42 were rewritten.
Each of those 42 ended with an automatically added `Co-Authored-By` trailer line; that line was removed. Nothing else
changed: every commit keeps its tree, author, committer, dates and parent structure (the merge of the review branch
is still a merge). The 4 commits of the review branch had no such line and keep their hashes, so
`origin/es8-c6c7-review-2026-11-04` (`d3cbcbe94`) is unaffected.

The new hashes start at the merge `1bc033d57`, now `ef8b788c6`; the old tip `94aee3ead` is now `8c2e907b2`.
Commits up to `28e2c0bde`, and every other branch, are unchanged.

**Files in this directory.**
- `commit_map.tsv`: for each of the 46 commits, the old and new full hash, whether its message changed, and its
  subject. To resolve a commit hash quoted in a log, an email or a note from before this rewrite, look it up in the
  `old_commit` column.

**Hash citations updated.** One rewritten commit was cited in the tree: `b583d89ab` (the correction of the proof of
Corollary k8s:cor:geom), now `f2a462b67`. It was replaced in `WRITEUP/P1/p1.tex`, `WRITEUP/P1/k8_soundness_p1.tex`,
`WRITEUP/P1/README.md` and `WRITEUP/P1/reviews/corollary-geom-review-20261106.md`, and `p1.pdf` was rebuilt (see
the `p1.pdf` row of `WRITEUP/P1/README.md`). No other file in the tree cites a rewritten commit (checked against
every hexadecimal token of 7 or more characters in the tree).

**Unaffected.** No file content changed in the rewrite, so every SHA-256 record, CNF, LRAT proof, certificate and
Lean file is byte-identical, and every check stands.

**Other working copies.** A clone that has the old commits should run `git fetch origin` and then
`git reset --hard origin/es7-night-2026-11-01` (after committing or saving any local work, which can then be
re-applied with `git rebase --onto origin/es7-night-2026-11-01 94aee3ead`).

# WRITEUP review task: referee `MIRROR.md` against its sources

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} below by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>`.
- Time budget: {H} hours of wall time. Commit and push at least every 30 minutes. Use the last 10 minutes to finish `REVIEW.md`, push, and report. Do not end your turn while work is running.
- Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/WRITEUP/`, with plain commit messages and no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push and retry until it succeeds (about 50 machines push to this branch); after 10 failures push to branch `es7-fallback-writeup-review` and say so.

## Task

`results/WRITEUP/MIRROR.md`, `NUMBERS.tsv` and `README.md` (paths under `cloud/es7-2026-10-19/`) were written in one quick pass (commit 3c829b65) as a self-contained account, for a mathematician, of the result: every 33-point set in general position in the plane that is invariant under a reflection contains 7 points in convex position. Referee them as a careful co-author would before they go to an outside reader:
1. Check every number, file path, commit hash (new hashes; old ones translated with `results/FINAL/COMMIT_MAP.tsv`) and Lean name against the file it cites. Re-derive totals yourself from the data files where the text sums them.
2. Check every mathematical argument for completeness, especially §2 (which symmetries a 33-point set with no convex 7-gon can have: every rotation order, the point reflection, the dihedral groups, and why exactly one point lies on a mirror axis), the encoding and normalization (§3) and the case split (§4). Compare with `results/H3`, `results/Mii-S/soundness.md`, `results/C3-S/soundness.md`, `results/E`, `results/E2`.
3. Check that the statement matches the Lean theorem (`results/V2-L/V2L/FinalTree.lean`, `MirrorExclusionLine` in `results/H3`) and that the trust base is described completely and without overstatement. Check that the related-work wording says "we did not find prior work" and claims no priority (`results/LIT/RELATED.md` has the search).
4. Check readability for an outside mathematician: undefined notation, repository jargon (wave, V3, Zf, shard) used without explanation, and missing definitions.

Write `REVIEW.md`: every problem found, with location, what the text says, what the source says (path), and severity (wrong / incomplete / unclear / cosmetic). Then apply to `MIRROR.md`, `NUMBERS.tsv` and `README.md` the corrections you verified against a source file, and list each applied change in `REVIEW.md`. Do not add claims that are not in the sources. Final message: the number of problems by severity, the most serious ones, and the commit.

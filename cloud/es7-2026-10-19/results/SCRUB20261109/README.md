# SCRUB20261109: tool identity removed from nine commits; all branches combined into `main` (9 November 2026)

**What changed.** Nine commits of 31 October 2026, lane logs of the `ES8SAT` runs E01 and E03, had the identity of
an automated tool, not the author, in their committer field. That field now names the author, as in every other
commit. Every commit that descends from them had to be rewritten too: 1,735 commits in all (the nine and 1,726
descendants) have new hashes. Nothing else changed. Every rewritten commit keeps its tree, author, author and
committer dates, message and parent structure; the 5,741 other commits of the history keep their hashes.
- **Signatures.** A rewritten commit cannot keep a valid signature, so signatures were dropped. 1,613 of the 1,735
  carried an SSH signature, all made with one key. That key is registered for the tool's account, not the author's:
  GitHub showed the nine commits as verified for the tool's account and the other 1,604 as unverified. The rewritten
  commits carry none. 3,228 older commits that keep their hashes (21 to 31 October, all committed under the author's
  name) still carry signatures by the same key, which GitHub shows as unverified; removing those would need another
  rewrite and was not done.
- **Checks.** A separate script compared every old and new commit: same tree, author, message and number of
  parents; parents mapped; the committer changed only in the nine, in name and e-mail, with the date kept; no
  signature left. Result: 1,735 pairs, 0 mismatches; the old and new tips have the same tree; the new history is the
  5,741 kept commits plus the 1,735 rewritten ones; no commit of it has the tool identity as author or committer.

**Branches combined.** Before the rewrite, two merges were made on the research line:
- `main`'s two commits of 22 October (the twelve-point obstruction, `docs/MINIMAL12_OBSTRUCTION.md` and its
  certificates) were merged in, without conflicts (`d0f950046`, now `e9d2a1f50`);
- the nine `es7-fallback-*` branches were recorded by a merge that changes no file (`a2803fb51`, now `8e9a98f55`).
  Their files were already on the research line, identical or in a later version.

After the rewrite, `main` points to the combined tip; this is a fast-forward, since `main`'s own commits keep their
hashes. `es7-night-2026-11-01` points to the same commit, so existing checkouts of it keep working after a reset.
`es7-cloud`, `es8-c6c7-review-2026-11-04` and the nine `es7-fallback-*` branches are deleted; every commit of theirs
is in the new history, rewritten where it descends from the nine. Pull request #1 (`es7-cloud` into `main`) is
contained in `main`. GitHub may keep the old commit objects for a while (for example in the history of that pull
request), but no branch refers to them.

**Files in this directory.**
- `commit_map.tsv`: for each of the 1,735 commits, the old and new full hash, whether its committer changed, whether
  a signature was dropped, and its subject. To resolve a commit hash quoted in a log, a record or a note from before
  this rewrite, look it up in the `old_commit` column. For a hash from before 7 November, first look it up in
  `SCRUB20261107/commit_map.tsv`, then here.
- `commit_citations.tsv`: every citation of a rewritten commit in the text files of the tree, with its status.

| old | new | commit |
|---|---|---|
| `bb8c5b1be` | `f9f268dd2` | written proofs, Stage 1 (`PROOFS20261108`) |
| `7e32ee259` | `38e0af1ec` | start of the Mac share of the budget-64 search; the line basis of `PROOFS20261108` |
| `5aa5b31f2` | `e49379023` | `SCRUB20261107`, part 2 |
| `9cf4949a5` | `471d5f63a` | tip of `es7-cloud` (pull request #1); the audited commit of `AUDIT3` and `REPLAY` |
| `d3cbcbe94` | `3a5408fcc` | tip of `es8-c6c7-review-2026-11-04` |
| `6a4e5c3c1249` | `536800bfe8a3` | ENCBLEAN M9, the commit pinned in `ENCBLEAN/geo/VENDOR.sha256` |

**Hash citations.** A word-bounded search of every text file of the tree (in Python; `git grep -E` has no `\b`)
found 1,977 citations of rewritten commits, each listed in `commit_citations.tsv`:
- **98 updated.** 97 are in 24 hand-written files: the `AUDIT3` README and reports, the READMEs of `C2RECHECK`,
  `C3LEAN`, `C6C7REVIEW`, `ENCBLEAN` (with `DESIGN.md`), `ES8SLACK`, `ES8UPPER20261105`, `REPLAY` and `SYMLEAN`,
  `LRATCHECK20261105/AUDIT.md`, the P1 README, `p1.tex` and `k8_soundness_p1.tex`, the compact-checker README,
  two comments of `ENCBLEAN/geo/scripts/audit_geo.sh` and a docstring in `ES8SLACK/review`. Each hash was replaced
  by the new one, abbreviated to the same length; every new abbreviation resolves to exactly one commit. The 98th
  is functional: the header of `ENCBLEAN/geo/VENDOR.sha256` names the M9 commit, and check 2 of `audit_geo.sh`
  looks it up. The header now names `536800bfe8a3`, and the PINNED SHA-256 of `VENDOR.sha256` in `audit_geo.sh`
  changed from `8060ed40…` to `c192e808…`. Check 2 was redone by hand against the new commit: the 10 vendored
  modules and the 24 pinned `../` files match.
- **1,878 kept.**
  - 967 are in logs and run outputs;
  - 489 are in run records that state the repository at run time: the lane records under `C2P3`–`C2P5` and the
    replay's `REPLAY/build_manifest.py`;
  - 170 are in the replay manifest `REPLAY/manifest.tsv`;
  - 135 are in files whose SHA-256 another record pins. Among them are all files of `PROOFS20261108`, whose line
    basis `7e32ee259` is now `38e0af1ec` with the same tree, and `WRITEUP/note/k8_soundness.tex`;
  - 110 are in the earlier rewrite records;
  - 1 names what an earlier draft printed (`WRITEUP/note/symmetric_extremal.tex`);
  - 6 are in hand-written lines that must keep the old hash: the reproduction command in `C3LEAN/README.md`, whose
    argument is written into the hash-pinned `C3Cover.lean`; the description of the manifest entries in
    `REPLAY/README.md`; a quotation of the kept `status.log` in `AUDIT3/reports/A1_reduction.md`; and two sentences of
    the P1 README about what the rewrite of 7 November produced. Four of them now name the new hash as well.

  To resolve any of them, use `commit_map.tsv`. The search covered text files only. Three committed PDFs print
  rewritten hashes from their sources: `PROOFS20261108/proofs.pdf`, `WRITEUP/note/k8_soundness_wrapper.pdf` and
  `WRITEUP/note/symmetric_extremal.pdf`. They match their kept or pinned sources and were not rebuilt.
- **1 is not a citation**: a decimal number in `inputs/distinct_K7.txt`.

**Rebuilt.** `WRITEUP/P1/p1.pdf`: 38 pages, as before; its text differs from the previous build only in the three
printed hashes (P1 README, last section). `WRITEUP/P1/p1.log` is now the log of this build. No other file content
changed. Every CNF, proof, certificate, point set
and Lean file is byte-identical; of the hash records only the header line of `VENDOR.sha256` and the pin in
`audit_geo.sh` changed.

**Not changed here.** Absolute paths of the October cloud runs' home directory remain in 426 files (484 lines). They
are file content, not history, and a separate cleanup can replace them without a rewrite.

**Other working copies.** A clone that has the old commits should save any local work, then run `git fetch origin`
and `git reset --hard origin/main` (or `origin/es7-night-2026-11-01`, which points to the same commit). Local work can
then be re-applied with `git rebase --onto origin/main <old tip>`. On the Mac, the refs from before the rewrite are
kept locally under `refs/backup/pre-scrub-20261109/`.

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

**Hash citations updated.** At first only `b583d89ab` (the correction of the proof of Corollary k8s:cor:geom), now
`f2a462b67`, was found and replaced in `WRITEUP/P1/p1.tex`, `WRITEUP/P1/k8_soundness_p1.tex`, `WRITEUP/P1/README.md`
and `WRITEUP/P1/reviews/corollary-geom-review-20261106.md`, and `p1.pdf` was rebuilt.
- *Correction (same evening).* The first version of this paragraph said no other file cites a rewritten commit. That
  was wrong. The search used `\b` in a `git grep -E` pattern, which git reads as a literal `b`, so it saw only
  hashes that begin and end with `b`.
- A word-bounded search of every text file now lists 52 citations of rewritten commits, each in `commit_citations.tsv`
  with its status:
  - **29 updated to the new hash.** These are in ENCBLEAN's README, DESIGN and M3PLAN, LRATCHECK's AUDIT, the
    compact-checker README, P1's README, `k8_soundness_p1.tex` and `p1.tex`. `p1.pdf` was rebuilt (38 pages,
    0 errors); its text changed only in "committed in 862d95ed5".
  - **One functional citation fixed.** `ENCBLEAN/geo/VENDOR.sha256` names the M9 commit, and `geo/scripts/audit_geo.sh`
    (check 2) requires that commit to exist. In a fresh clone the old `115ccda3dd34` no longer does. The header now
    names `6a4e5c3c1249`, which has the same tree. The PINNED hash of `VENDOR.sha256` in `audit_geo.sh` changed from
    `f1fffe4e…` to `8060ed40…`, and check 2 passes against the new commit (34 files equal it).
  - **23 kept.** 19 are logs that recorded `git HEAD` when they ran. 3 are in hash-pinned files (`assemble_final310.sh`
    and `assemble_final311.sh`, which have them in comments, and `WRITEUP/note/k8_soundness.tex`, the source of a
    recorded copy). 1 names the old hash on purpose. To resolve any of them, use `commit_map.tsv`.

**Unaffected.** No file content changed in the rewrite, so every SHA-256 record, CNF, LRAT proof, certificate and
Lean file is byte-identical, and every check stands.

**Other working copies.** A clone that has the old commits should run `git fetch origin` and then
`git reset --hard origin/es7-night-2026-11-01` (after committing or saving any local work, which can then be
re-applied with `git rebase --onto origin/es7-night-2026-11-01 94aee3ead`).

## Part 2: sandbox and machine paths in files (7 November 2026, evening)

**What changed.** 91 text files that came from the Linux machine between 4 and 7 November had absolute paths
of that machine. Only those strings changed (in `ENCBLEAN/docs/M3PLAN.md` also a commit citation, see above), and line counts are the same. Every edited Python file parses, every
edited shell script passes `bash -n`, and every edited JSON or JSONL file loads.

| Count | Old string | New string |
|---|---|---|
| 99 | sandbox path prefixes of the Linux sessions, under `/tmp/`, including the per-session project directory and scratchpad | `/sandbox` |
| 223 | the repository root on the Linux machine | `/path/to/repo` |
| 77 | its data directory (campaign and replay work directories) | `/path/to/data` |
| 15 | its SAT tools directory (`cake_lpr`) | `/path/to/tools` |
| 2 | its home directory, elsewhere | `/path/to/home` |

The placeholders are plain paths with no shell metacharacters, so no edited script gains a redirection (compare
`SCRUB20261104`). The edited scripts are records of completed runs (the replay of 6 November, the ¬Y(1,2) run, the P1
and LAYERLEAN re-runs). They no longer run as they are; replace the placeholders to rerun them.

**Left unchanged: 16 files, 24 lines** (`left_unchanged.tsv`, with the reason for each). None of them contains a tool
name; what remains is the Linux home path.
- 13 are hash-pinned: their SHA-256 is cited in another record, such as the frozen ES(8) ≤ 310 pipeline
  (`assemble_final310.sh`, `frozen-shas.txt`), the ENCBLEAN audit (`audit_geo.sh` pins `EncB/Render.lean`), the
  311 chain records and the replay manifests. Editing them would break those checks.
- 2 are deletion manifests (`deleted-cnf-2026-11-06.sha256`). Records are not edited.
- 1 is operational: `experiments/omission-compact-checker-2026-11-05/incr_es310.sh`, which the paused hourly
  ES(8) ≤ 310 loop runs on the Linux machine.

**Hash records.** No record was edited in this part. The only record changes are the `VENDOR.sha256` header and
its pin in `audit_geo.sh`, described under "Hash citations updated" above. One record cites the pre-scrub hash of an
edited file: the M3 snapshot
`ENCBLEAN/logs/env.txt` lists `docs/M3PLAN.md` (`hash_citations.tsv`). That value describes the original bytes, which
remain in git history. For every edited file, `path_scrub_map.tsv` gives the SHA-256 before and after and the number of
replacements of each kind.

**Unaffected.** No CNF, LRAT proof, certificate, point set or Lean file was edited. The Linux host name and the file
owner still appear in a few ENCBLEAN logs (`host:` lines, `ls -l` output); they are not paths and were left.

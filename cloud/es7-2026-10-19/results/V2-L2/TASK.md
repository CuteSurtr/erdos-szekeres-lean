# V2-L2 task: state the mirror theorem on the exact leaf files that cake_lpr checked

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} below by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>` (if not, unset GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL for your git commands). Record the environment (`uname -a; nproc; free -g || true; date -u`) into `cloud/es7-2026-10-19/results/V2-L2/env.txt`, then commit and push it at once.
- Time budget: {H} hours of wall time. Commit and push at least every 30 minutes. Use the last 10 minutes to finish `results/V2-L2/README.md`, push, and report. Do not end your turn while work is running: ScheduleWakeup does not fire here, so wait in the foreground with bounded until-loops (at most 10 minutes per tool call).
- Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/V2-L2/`, with plain commit messages and no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push and retry until it succeeds (about 50 machines push to this branch); after 10 failures push to branch `es7-fallback-v2l2` and say so. Never commit build outputs (`.lake/`), files over 50 MB, CNF or proof files.
- **Never write `sorry` or `admit` in any Lean file, not even temporarily.** No new `axiom` declarations. Do not modify any file outside your directory.
- Commit hashes cited in files written before 2026-10-21 are pre-rewrite hashes; translate them with `results/FINAL/COMMIT_MAP.tsv`.

## Background

Paths are under `cloud/es7-2026-10-19/`. `V2L.mirrorExclusionLine_final` (`results/V2-L/V2L/FinalTree.lean`, README §9) proves `MirrorExclusionLine` from cake_lpr facts. Its sub-case (ii) hypothesis is

```lean
hleaves : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves,
  ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)
```

The files that cake_lpr actually checked for these leaves were written by `verify/v3/v3_check.py` (at commit 92746ac, formerly bdf319c): F's clause body unchanged, then one unit clause per literal of the case cube sorted by absolute value, then one unit clause per leaf literal that is not already in the case cube, sorted by absolute value; header `p cnf NV NC+k`. So the Lean term and the checked file have the same clauses but are not the same list. Also, a leaf that contains the negation of a case-cube literal is recorded as VERIFIED by V3 without a solver call. `results/WRITEUP/MIRROR.md` (trust base section) lists both points.

## Goal

A new Lean package `V2L2` in `results/V2-L2`, depending on `results/V2-L` by path (as V2-L depends on H3; build instructions: `results/V2-L/README.md` §1, Mathlib from source takes about 30 minutes), with:
1. A definition `v3LeafCnf F c l` that is exactly the clause list `v3_check.py` writes (same order, same deduplication rule, same sorting), and a lemma that `DimacsSatisfiable` depends only on the set of clauses (if every clause of A is in B and every clause of B is in A, then A is satisfiable iff B is), hence `DimacsSatisfiable (v3LeafCnf F c l) ↔ DimacsSatisfiable (cubeCnf (cubeCnf F c) l)`.
2. A lemma that a CNF containing the unit clauses `[z]` and `[-z]` (z ≠ 0) is not satisfiable, hence every leaf containing the negation of a case-cube literal needs no hypothesis.
3. A theorem `V2L2.mirrorExclusionLine_v3` with the same conclusion as `V2L.mirrorExclusionLine_final`, the same `h1`, `hroot` and `hup`, and instead of `hleaves` the hypothesis: for every case and every tree leaf `l` that contains no negation of a case-cube literal, `¬DimacsSatisfiable (v3LeafCnf (interiorCnf 33 7) p.2 l)`. `#print axioms` must show only propext, Classical.choice and Quot.sound; put it in an `Audit.lean` with `#guard_msgs` as V2-L does.
4. Count the tree leaves that the hypothesis no longer needs (contradicting the case cube), and check, for at least 50 leaves of different cases, that the DIMACS text of `v3LeafCnf` emitted from Lean (reuse the DIMACS emission of `results/H3` if it fits; otherwise write the bytes with a small Lean exe) has the sha256 recorded for that leaf in the V3 records (`results/V3Z`, `results/V3A` to `results/V3E`). If you cannot, say what is missing.

`README.md` and final message: the new theorem statement exactly as in the file, the axioms, the build log lines, the counts from 4, and what is still trusted.

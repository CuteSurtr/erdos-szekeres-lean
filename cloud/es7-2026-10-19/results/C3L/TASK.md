# C3L task: a Lean generator for the 3-fold base CNF, byte-identical to the one the solvers use

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} below by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>` (if not, unset GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL for your git commands). Record the environment (`uname -a; nproc; free -g || true; date -u`) into `cloud/es7-2026-10-19/results/C3L/env.txt`, then commit and push it at once.
- Time budget: {H} hours of wall time. Commit and push at least every 30 minutes. Use the last 10 minutes to finish `results/C3L/README.md`, push, and report. Do not end your turn while work is running: ScheduleWakeup does not fire here, so wait in the foreground with bounded until-loops (at most 10 minutes per tool call).
- Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/C3L/`, with plain commit messages and no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push and retry until it succeeds (about 50 machines push to this branch); after 10 failures push to branch `es7-fallback-c3l` and say so. Never commit build outputs (`.lake/`), files over 50 MB or CNF files.
- **Never write `sorry` or `admit` in any Lean file, not even temporarily.** No new `axiom` declarations. Do not modify any file outside your directory.

## Background

Paths are under `cloud/es7-2026-10-19/`. For the mirror class, `results/H3` (`MirrorEncoding`, on top of `results/H`, `ETVEncoding`) has a Lean generator that writes the solver's CNFs byte for byte, and soundness proofs; `results/V2-L` then states the result in Lean modulo cake_lpr verdicts. The 3-fold (C3) class has no Lean side yet. Its base CNF is `python3 results/C3-S/tools/gen_case.py 11 7 none -o base.cnf` (the C3a chain encoding, `results/C3a/c3cnf.py`; header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`); case CNFs add the unit clauses of `results/C3-S/tools/hullcase.py`.

## Goal, in this order

1. Read `c3cnf.py`, `gen_case.py` and `hullcase.py`, and `results/H3` (`Gen.lean`, `Emit.lean`) to see how the mirror generator is written. Write `PLAN.md`: the variables and clause families of the C3 base CNF, and how each maps to a Lean definition.
2. A Lean 4 package `C3Encoding` in `results/C3L` (same Lean version as `results/H3`; keep the generator free of Mathlib so it builds fast, as `results/V2-L/V2L/Defs.lean` does) with a generator for the base CNF and a `lake exe` that writes its DIMACS text. Check that the output is byte-identical to `gen_case.py 11 7 none` (header and sha256 above); also compare at small parameters (for example m = 3, 4 and k = 5, 6, 7) against `gen_case.py m k none`.
3. If time remains: the case and layer unit clauses of `hullcase.py` for named nodes, checked by sha256 against `results/C3-S/manifest_depth2.tsv` (column `cnf_sha256`) for at least 20 nodes; then, in `PLAN.md`, the soundness statement to prove next (every 3-fold-symmetric 33-point set in general position without a convex 7-gon, labelled as in `results/C3-S/soundness.md`, satisfies the base CNF), with the lemmas from `results/H` and `results/H3` that can be reused.

`README.md` and final message: what builds, the byte comparisons (with sha256 values), what is planned next.

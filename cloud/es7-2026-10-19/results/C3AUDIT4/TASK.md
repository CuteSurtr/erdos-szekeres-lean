# C3AUDIT4 task: independent check of the composer fix (C3U2)

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} by those values; follow everything else exactly.

General rules: as in `results/C3AUDIT/TASK.md` (paths under `cloud/es7-2026-10-19/`), with `results/C3AUDIT4/` as your only directory and the fallback branch `es7-fallback-c3audit4`. In particular: commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com> (check `git var GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`), `env.txt` pushed at once, plain commit messages with no AI co-author or attribution trailers, `git pull --rebase --autostash` before every push, notes pushed at least every 30 minutes, the last 10 minutes for `REPORT.md`, do not end your turn while work is running, do not modify anything outside your directory, never commit CNF or proof files, and never write `sorry` or `admit` in any Lean file.

## What is under review

`results/C3AUDIT3/REPORT.md` found that `results/C3U/tools/compose.py` (95cafa93) can cover a childless plain node vacuously (finding 1), plus smaller findings 2 to 4. Another agent is fixing this right now in `results/C3U2/tools` (task `results/C3U2/TASK.md`) and will write `results/C3U2/README.md` when done (expected within about 1.5 hours of your start; poll the branch every 10 minutes). The fixed composer will judge whether the 3-fold class is covered, so default to suspicion.

## What to do

1. **Before the fix lands:** read C3AUDIT3's report, its fixed `results/C3AUDIT3/tools/mycompose.py` and the specification `results/C3U/TASK.md`. Write your own new adversarial inputs that a correct composer must reject (at m = 5 to 7, k = 5 or 6; known answers in `results/C3-S/tools/controls.py`): childless plain and cube nodes reached through rule-3 splits, a σ-split with a missing or wrong cube, mixed layer and σ routes where neither route is complete, `sigma_cubes.py` records mixed into a `close_tree.py` OUT file, forged sha values, and a σ-split at depth 1. Check C3AUDIT3's composer on them too.
2. **When `results/C3U2/README.md` appears:** review `git diff` of `results/C3U2/tools` against `results/C3U/tools` at 95cafa93 line by line. Run C3U2's composer and C3AUDIT3's fixed composer on all your inputs, on C3AUDIT3's tests (`forge.py`, `logs/childless_real_m5k6.jsonl`, `logs/natural/`) and on every 3-fold record listed in step 3 of `results/C3U2/TASK.md` at the commit you use (both with and without `--mirror-h6`). They must agree on covered or not, the frontier and the set of open depth-2 roots, and every forged input must be rejected or left uncovered.
3. If C3U2 has not finished 30 minutes before your end, report on your inputs and on C3AUDIT3's composer, and say so.

`REPORT.md` and final message: a clear verdict (accept / reject / accept with conditions) on `results/C3U2/tools/compose.py` and `close_tree.py`, every finding with file and line, the test counts, the composer comparison, and what you could not check.

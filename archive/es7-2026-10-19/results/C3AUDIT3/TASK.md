# C3AUDIT3 task: independent check of the σ-cube splitting (C3U)

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} by those values; follow everything else exactly.

General rules: as in `results/C3AUDIT/TASK.md` (paths under `cloud/es7-2026-10-19/`), with `results/C3AUDIT3/` as your only directory and the fallback branch `es7-fallback-c3audit3`. In particular: commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com> (check `git var GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`), `env.txt` pushed at once, plain commit messages with no AI co-author or attribution trailers, `git pull --rebase --autostash` before every push, notes pushed at least every 30 minutes, the last 10 minutes for `REPORT.md`, do not end your turn while work is running, do not modify anything outside your directory, never commit CNF or proof files, and never write `sorry` or `admit` in any Lean file.

## What is under review

`results/C3U/TASK.md` specifies σ-cube splitting for the 3-fold tools (names `L__C`, their CNF, the σ-split and its `sigma_bits`, the layer split of a cube node, caps, and `compose.py`). Another agent is implementing it right now in `results/C3U/tools` and will write `results/C3U/README.md` when done (expected within about 2 hours of your start; poll the branch every 10 minutes). Default to suspicion: the split must not be used in a wave unless it is right.

## What to do

1. **Before the code lands:** read the specification and the prototype `results/C3PLAN/scripts/sigma_cubes.py`, and decide whether the specification is sound (cover of rule 2, cover and dropped options of rule 3, CNF construction, interaction with the H3 mirror reduction, `--mirror-h6` and `--split-singles` (rule 2 forbids σ-splits at depth 1 because the mirror arguments map S to M(S), which changes σ values: check that this restriction is sufficient and enforced in the code and in `compose.py`), and with records of earlier waves that split the same nodes by layers). Then write **your own composer** with σ-cube support from the specification only: start from `results/C3AUDIT/tools/mycompose.py` (copy it into your directory), not from any C3U or C3T code. Test it on small instances you generate yourself (m = 5..7, k = 5..6; known answers in `results/C3-S/tools/controls.py`), including forged inputs that must be rejected.
2. **When `results/C3U/README.md` appears:** review the changed files of `results/C3U/tools` line by line against the specification (the README cites the commits). Run both composers on C3U's test records, on all records of `results/C3SIG/*/out.jsonl`, and on all 3-fold wave records (`results/C3WAVE1`, `C3WAVE2`, `C3S0`, `C3W3`, out and recheck files, at the commit you start from); they must agree. Re-solve at least 3 cube nodes from C3U's records yourself (CaDiCaL c6073042 `--sat --lrat --binary=false`, both checkers as in `results/C3WAVE2/TASK.md` step 1) and compare `cnf_sha256` and the verdict.
3. If C3U has not finished 30 minutes before your end, report on the specification and your composer, and say so.

`REPORT.md` and final message: a clear verdict (accept / reject / accept with conditions) for the specification and for the implementation, every finding with file and line, the test counts, the composer comparison, and what you could not check.

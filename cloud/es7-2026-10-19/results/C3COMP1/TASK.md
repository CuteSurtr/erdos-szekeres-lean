# C3COMP1 task: composition after wave 4, and a cap experiment on timed-out 6-bit cubes

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} by those values; follow everything else exactly.

General rules: as in `results/C3U2/TASK.md` (paths under `cloud/es7-2026-10-19/`), with `results/C3COMP1/` as your only directory and the fallback branch `es7-fallback-c3comp1`: commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com> (check `git var GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`), `env.txt` pushed at once, plain commit messages with no AI co-author or attribution trailers, `git pull --rebase --autostash` before every push, progress pushed at least every 30 minutes, the last 10 minutes for the README, do not end your turn while work is running, do not edit anything outside your directory, never commit CNF or proof files. Any SAT answer: stop, commit the model and the solver output, report it first.

## Part 1: composition (do this first)

Run `results/C3U2/tools/compose.py` at commit cad4e050 with `--mirror-h6` and sha checks on, and `results/C3AUDIT3/tools/mycompose.py` (its fixed version) in the matching mode, on every 3-fold record at the head you start from: the 127 files listed in `results/C3U2/compose_m11/files.txt`, plus `results/C3W4/*/out.jsonl` and `recheck*.jsonl`, plus `results/C3W5/*/out.jsonl` and `recheck*.jsonl` (whatever exists; list the files and the commit). Base CNF as step 1 of `results/C3WAVE2/TASK.md`. The two composers must agree on covered or not and on the set of open depth-2 roots (if they disagree, report it first). Write `results/C3COMP1/open_roots.tsv` (every root of the reduced cut: root, stratum, status, frontier size) and a table of open roots per stratum.

## Part 2: what the remaining roots need

From the records of `results/C3W4` and `results/C3SIG2`, for the open H3 and one-orbit roots: how many of each root's 64 six-bit cubes are certified, timed out at 300 s, or never ran; the distribution of solve times of certified six-bit cubes; and how large the layer subtrees under timed-out cubes grew. Then run an experiment in parallel with Part 1 (3 jobs): pick at least 15 six-bit cubes that timed out at 300 s in C3W4 (spread over at least 6 different roots), and solve each alone with `results/C3U2/tools/close_tree.py` at cad4e050 as the root (`--caps 1800 --jobs 3`, no σ-split, `--cadopts=--sat`), with both checkers. Record how many close and how long they take.

README.md and final message: the composition table (both composers), the number of open roots per stratum and their total frontier, the Part 2 statistics, the cap experiment, and a recommendation for the remaining roots (caps per depth, σ levels, expected core-hours), with the evidence for it.

# C3W5 task: mop-up of the 3-fold class with the fixed σ-cube tools, one machine

Your prompt gives these values: V (your machine name, for example M03), LIST (a file in `results/C3W5/lists/`), j (your shard), N (the number of shards of LIST), SLICE (hours per root), H (your time budget in hours) and Z (the commit of this file). Replace {V}, {LIST}, {j}, {N}, {SLICE}, {H} and {Z} by those values. Everything else in this file is to be followed exactly.

This is part of the search for a counterexample to ES(7) = 33 (a 3-fold-symmetric 33-point set in general position with no 7 points in convex position); the 3-fold class is the last symmetry class that could hold one. Every SAT answer is a candidate counterexample.

General rules: exactly as in `results/C3W4/TASK.md`, with `results/C3W5/{V}/` as your only directory and the fallback branch `es7-fallback-c3w5-{V}` (lower case): commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com> (check `git var GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`), `env.txt` committed at once, commits only inside your directory with plain messages and no AI co-author or attribution trailers, `git pull --rebase --autostash` before every push, progress pushed at least every 25 minutes, the last 12 minutes for the README, no CNF or proof files, no file over 50 MB, and do not end your turn while work is running.

## Differences from C3W4

1. Tools: `git worktree add /opt/c3u2 cad4e050`; TOOLS = `/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools` (the fixed tools: `results/C3U2/README.md`, accepted by `results/C3AUDIT4/REPORT.md`), used unmodified. Build CaDiCaL, cake_lpr, lrat-check and the base CNF exactly as step 1 of `results/C3W4/TASK.md` (same commits, same checks). Do not run `compose.py`; the final composition is done separately.
2. Seeding (partial roots continue where they stopped): for each of your roots R, copy into `/opt/work/out.jsonl`, before the runner starts, every record of `results/C3W4/*/out.jsonl` and `results/C3W4/*/recheck*.jsonl` whose `node` is R or starts with `R_` or `R__` and that is certified (both checkers) or a split record with at least one child. Do not seed records of any other directory. Count the seeded lines; the out file you commit contains only the new records (the lines after the seeded ones).
3. Options by list: `W5_two.tsv`: `--sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles`; `W5_rest.tsv` (if your prompt names it): the stratum column decides — H3 and one-orbit roots `--sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat` (no `--split-singles`), two-orbit roots as `W5_two.tsv`.
4. close_tree.py at cad4e050 reports timed-out nodes without children as `unsplittable` and keeps them in `open_frontier`; list them in the README (they are open).

Everything else (runner with `setsid nohup`, `--jobs 3`, `--hours S` with S = min({SLICE}, hours left before END), END = start + {H} hours − 15 minutes, SAT and PROOF NOT ACCEPTED handling, commits every 25 minutes, README content) is as in `results/C3W4/TASK.md` steps 4 and 5.

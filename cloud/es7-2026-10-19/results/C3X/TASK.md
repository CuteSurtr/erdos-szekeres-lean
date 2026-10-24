# C3X task: which method closes the hard nodes of the 3-fold class fastest

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} below by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>` (if not, unset GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL for your git commands). Record the environment (`uname -a; nproc; free -g || true; date -u`) into `cloud/es7-2026-10-19/results/C3X/env.txt`, then commit and push it at once.
- Time budget: {H} hours of wall time. Commit and push at least every 25 minutes. Use the last 10 minutes to finish `results/C3X/RESULTS.md`, push, and report. Do not end your turn while work is running: ScheduleWakeup does not fire here, so run long jobs with `setsid nohup` and wait in the foreground with bounded until-loops (at most 10 minutes per tool call).
- Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/C3X/`, with plain commit messages and no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push and retry until it succeeds (about 50 machines push to this branch); after 10 failures push to branch `es7-fallback-c3x` and say so. Never commit files over 50 MB, CNF or proof files.
- An UNSAT counts only if cake_lpr prints the exact line `s VERIFIED UNSAT` on its LRAT proof. If any run reports SAT, stop at once, commit the model and the solver output, and report it first.
- Commit hashes cited in files written before 2026-10-21 are pre-rewrite hashes; translate them with `results/FINAL/COMMIT_MAP.tsv`.

## Background

Paths are under `cloud/es7-2026-10-19/`. The 3-fold (C3) class is split into a layer tree (`results/C3-S/README.md`, `soundness.md`; 1,630 depth-2 roots). The current method, `results/C3-S/tools/close_tree.py` with caps 300/300/600 s and `--split-singles`, closes most two-orbit roots in minutes but stalls on some: for example `0s0-1s1_4` in `results/C3WAVE1/C00` (one-orbit layer 2; 23,826 s of solving and still open), and the roots left open in `results/C3WAVE1/C*/out.jsonl` and `results/C3WAVE2/K*/out.jsonl` (pull again during the run). `results/C3-S/README.md` ("Measurements") reports that march_cu cubes on whole top cases did not help, that σ cubes alone did not help, and that `--sat` was about 1.4× faster.

## Task

Build the tools exactly as `results/C3WAVE1/C00/README.md` describes (C3-S tools from commit 132398c, CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch; base CNF `gen_case.py 11 7 none` with sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`), plus march_cu (CnC 705b60c, as `results/C3a/shard_plan.md` builds it) if you use it. Pick 4 to 8 hard nodes (open nodes at depth 3 or 4 below open roots, and some one-orbit layer-2 roots), and for each compare, at a fixed budget per method:
1. the current `close_tree.py` recursion (reference);
2. march_cu cubes of the node CNF (the base CNF plus the node's units), at a few depths, each cube solved by CaDiCaL;
3. splitting on σ bits or on the next layer's orbit choice before solving;
4. CaDiCaL options that `results/C3-S/logs/cadical_options.jsonl` did not try.

Record per node and method: closed or not, wall time, total solve and check seconds, number of subproblems, the largest subproblem time. Write `records.jsonl` (one line per run), `RESULTS.md` (a table, and the method you recommend for the next wave, with the evidence), `scripts/` and `README.md`. Say which results are certified (both checkers accepted every proof) and which are only measured.

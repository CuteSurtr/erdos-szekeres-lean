# LBS task: heuristic search for 33 points with no convex heptagon

Your prompt gives these values: V (your machine name, L1 to L3), STRATEGY (one of `random`, `extend32`, `c3coords`), H (your time budget in hours) and Z (the commit of this file). Replace {V}, {STRATEGY}, {H} and {Z} by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check `git var GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`. Record the environment into `cloud/es7-2026-10-19/results/LBS/{V}/env.txt` and push it at once.
- Time budget {H} hours; commit and push at least every 30 minutes; the last 10 minutes for the README. Do not end your turn while work is running: run the search with `setsid nohup` and wait in the foreground with bounded until-loops (at most 10 minutes per tool call).
- Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/LBS/{V}/`, with plain commit messages and no AI co-author or attribution trailers; `git pull --rebase --autostash` before every push (fallback branch `es7-fallback-lbs-{V}`, lower case). No file over 50 MB.

## Goal

ES(7) = 33 is conjectured. A set of 33 points in general position (no three collinear) with no 7 points in convex position would disprove it. The mirror-symmetric class is excluded (`results/WRITEUP/MIRROR.md`); the 3-fold class is being searched by SAT (`results/C3W3`). This task tries heuristic search, which nobody expects to succeed easily, but which is cheap and finds near-misses that tell us something.

Write a fast C or C++ program (with `-O2`, using all 4 cores) that keeps 33 points with integer coordinates, counts the 7-point subsets in convex position (incrementally when one point moves), and minimizes that count by simulated annealing or tabu search, rejecting any move that creates three collinear points. Strategy {STRATEGY}:
- `random`: many restarts from random sets, varied temperature schedules;
- `extend32`: start from 32-point sets with no convex 7-gon (the classical Erdős–Szekeres construction as formalized in `ErdosSzekeres/LowerBound` on branch main, and perturbed versions of it), add a 33rd point at many positions, then anneal all points;
- `c3coords`: search 3-fold-symmetric sets (11 orbit representatives, rotation by 120° about the origin, exact rational or large-integer coordinates), minimizing the count, then also allow breaking the symmetry.

Verify every reported count with an independent exact check (integer orientation tests over all 7-subsets, and a general-position check). If you ever reach 0, stop the search at once, verify it twice with two independent exact programs, commit the coordinates, and report it first: it would be a counterexample.

README.md and final message: the program, the runs, the best count found (with the coordinates of the best set in `best.txt`), the distribution of final counts, and what the near-misses look like (for example how many 6-gons-plus-one the best sets have).

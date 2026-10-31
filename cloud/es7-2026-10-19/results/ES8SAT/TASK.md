# ES8SAT task: one-point extensions of 64-point sets with no convex octagon, one machine

Your prompt gives V (your machine name, for example E03), H (your time budget in hours) and Z (the commit of this
file). Everything else in this file is to be followed exactly.

**Background.** ES(8) ≥ 65: `witness8.txt` is a 64-point set in general position with no 8 points in convex position.
A 65-point set with no convex octagon would disprove the Erdős–Szekeres conjecture for k = 8. Every 64-point subset of
such a set is a 64-point octagon-free set to which one point can be added. `sat.c` (copied unchanged from
`experiments/es8-lower-bound-search-2026-10-11/saturation/sat.c` on the main branch) decides exactly, for a given set S
and K, whether some point p can be added to S in general position without creating K points in convex position. It
tests every face of the arrangement of the lines through pairs of S and prints a JSON line in which
`bad_candidates > 0` means such a point exists. `walk.py` walks through octagon-free 64-point sets: it moves one
point at a time, accepting only positions where the moved point lies in no convex octagon (checked with `sat test`), and
runs the full `sat sat` test after every 10 accepted moves.

General rules: commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>; commits only inside
`cloud/es7-2026-10-19/results/ES8SAT/{V}/`, with plain messages and no AI co-author or attribution trailers;
`git pull --rebase --autostash` before every push (branch es7-cloud; if a push keeps failing, push to
`es7-fallback-es8sat-{V}` lower case and say so); no file over 50 MB; do not end your turn while work is running (wait in
the foreground with bounded until-loops of at most 10 minutes per tool call; ScheduleWakeup does not fire here).

## Steps

1. `cd cloud/es7-2026-10-19/results/ES8SAT && mkdir -p /opt/work && cc -O2 -o /opt/work/sat sat.c`. Check
   `sha256sum sat.c witness8.txt` against `MANIFEST.sha256`. Run the control
   `/opt/work/sat sat witness8.txt 8` (about 20–40 s): it must print `"bad_candidates": 0` and equal
   `faces_euler` and `faces_hit_by_valid_candidates` (1,909,613). Write `uname -a; nproc; free -g; date -u`, the
   control's JSON line and the build command to `results/ES8SAT/{V}/env.txt`; commit and push. If the control fails,
   stop and report.
2. Let n be your machine number (E03: n = 3). Start four walkers, seeds 100n+1 … 100n+4, each until
   DEADLINE = your start time + {H} hours − 12 minutes (epoch seconds):
   `SAT_BIN=/opt/work/sat setsid nohup python3 <repo>/cloud/es7-2026-10-19/results/ES8SAT/walk.py SEED /opt/work/wSEED DEADLINE > /opt/work/wSEED.stdout 2>&1 &`
   (`<repo>` is the absolute path of your checkout). Copy the four commands to `results/ES8SAT/{V}/run.sh`.
3. Every 20 minutes and at the end, copy each `/opt/work/wSEED/walk.log` to `results/ES8SAT/{V}/wSEED.log`, commit and
   push. If any walk.log contains `ALARM` or a line with `"bad": ` followed by a positive number, copy
   `/opt/work/wSEED/FOUND_*.txt` and `/opt/work/wSEED/bad.txt` into your directory at once, push, and report it first:
   that set plus one point of a bad face would be a 65-point set with no convex octagon (to be verified independently).
4. In the last 12 minutes write `results/ES8SAT/{V}/README.md`: the control result, the number of saturation tests per
   walker (lines of walk.log), the largest and smallest face counts seen, and every line with `bad` > 0 or
   `hit` ≠ `faces` (there should be none). Push, and end with the same summary.

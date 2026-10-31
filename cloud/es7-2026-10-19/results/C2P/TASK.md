# C2P task: the parallelogram cases of the central 34-point formula, one machine

Your prompt gives these values: V (your machine name, for example M07), LIST (a file in `results/C2P/lists/`), j (your shard), N (the number of shards of LIST), H (your time budget in hours) and Z (the commit of this file). Replace {V}, {LIST}, {j}, {N}, {H} and {Z} by those values. Everything else in this file is to be followed exactly.

This is part of the search for a counterexample to ES(7) = 33: a centrally symmetric set of 34 points in general position with no 7 points in convex position. Every other symmetry class is excluded (`results/WRITEUP/SYMMETRIC.md`). By `results/C2C34`, such a set would have a parallelogram as its convex hull, and the 8 canonical parallelogram cases P1..P8 are open. Each case is split at the second convex layer into 560 subcases (`results/C2C34/l2cubes.py`). A reflection pairs these subcases up, so 287 representatives per case are solved (`results/C2C34/README.md` §6; `results/C2P/tools/mklist.py`). For P8, 64 representatives and the cover of the split are already certified there.

General rules: exactly as in `results/C3W4/TASK.md` (paths under `cloud/es7-2026-10-19/`), with `results/C2P/{V}/` as your only directory and the fallback branch `es7-fallback-c2p-{V}` (lower case):
- commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com> (check `git var GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`);
- `env.txt` (the output of `uname -a; nproc; free -g; df -h /; date -u`) committed at once;
- commits only inside your directory, with plain messages and no AI co-author or attribution trailers;
- `git pull --rebase --autostash` before every push; progress pushed at least every 25 minutes;
- the last 12 minutes for the README;
- no CNF or proof files and no file over 50 MB;
- do not end your turn while work is running. Wait in the foreground with bounded until-loops of at most 10 minutes per tool call; ScheduleWakeup does not fire here.

## Steps

1. **Tools.**
   - Build CaDiCaL 3.0.1 (commit c6073042), cake_lpr (a36874a8, `make cake_lpr`) and drat-trim lrat-check (2e3b2dc, with `results/E2/tools/lrat-check-E2.patch` applied) exactly as step 1 of `results/C3WAVE2/TASK.md` describes. That includes its sanity checks: the cake_lpr example prints `s VERIFIED UNSAT`, lrat-check rejects the LRAT `3 0 0` on {1},{-1} and accepts `3 0 1 2 0`.
   - Put the three binaries (or links to them) in `/opt/work/bin/` as `cadical`, `cake_lpr` and `lrat-check`.
   - Base CNF: from `cloud/es7-2026-10-19/results`, run `python3 SYMZ/zcnf.py rot 17 7 --m 2 --hull -o /opt/work/base.cnf --map /opt/work/base.json` (under a minute). The header must be `p cnf 838032 16653336`. The sha256 must be `b0061e908bff80e6a597f31a6fec1d91e8504aebc09b0bcf41c2ff21604d8ff1` for base.cnf and `2476fafff493a763fd7f2883380d359629191912a15a69bcbdfbf49bbf472b48` for base.json.
   - Cubes: for a = 1..8, `python3 C2C34/l2cubes.py /opt/work/base.json a /opt/work/P{a}.txt` must be byte-identical to `C2P/cubes/P{a}_cubes.txt`.
   - Record everything in `results/C2P/{V}/tools.txt`. If any check fails, stop and report.
2. **Units.** Your units are the rows of `results/C2P/lists/{LIST}` with idx ≡ {j} (mod {N}), in file order.
   - Write them, with the header line, to `/opt/work/units.tsv`, and copy that to `results/C2P/{V}/units.tsv`.
   - Each unit is a subcase of a case `P<a>`, or the cover `P<a>_cover` of its 560-way split. Its kind is cover, Q (quadrilateral second layer) or H (hexagonal), and its cap is in seconds.
3. **One lane.**
   - Start it with `setsid nohup python3 <repo>/cloud/es7-2026-10-19/results/C2P/tools/lane.py /opt/work <repo>/cloud/es7-2026-10-19/results /opt/work/units.tsv /opt/work/out.jsonl END > /opt/work/lane.stdout 2>&1 &`.
     - `<repo>` is the absolute path of your checkout.
     - END = your start time + {H} hours − 15 minutes, in epoch seconds.
     - Copy the command to `results/C2P/{V}/run.sh`.
   - Run only this one lane and nothing else heavy. CaDiCaL needs up to about 12 GB on these formulas, and the machine has 15 GB.
   - **What lane.py does.**
     - It solves your units one at a time, each with CaDiCaL --lrat.
     - It checks every UNSAT proof with lrat-check and then cake_lpr, and deletes the proof.
     - It appends one JSON record per unit to `/opt/work/out.jsonl`. `"certified": true` means both checkers accepted the proof.
     - It starts no unit when less than 15 minutes remain before END, and it caps each solve so that 10 minutes remain for the checks.
   - **If `/opt/work/SAT_FOUND` appears:**
     - Commit `/opt/work/SAT_<unit>.out` into your directory at once (gzip it first if it is over 50 MB), push, and report it first.
     - The lane goes on by itself.
     - A SAT answer is an abstract configuration that may not be realizable. It is not yet a counterexample, but it is the most important possible outcome.
   - A record with `"certified": false` or a status starting with `ERROR`: list it in the README, and do not re-run it.
4. **Progress.** Every 25 minutes and at the end, copy `/opt/work/out.jsonl` to `results/C2P/{V}/out.jsonl` and the last 200 lines of `/opt/work/lane.log` to `results/C2P/{V}/lane.log.tail`. Then commit and push.

**README.md and final message.**
- The tool commits and the base and cube checks.
- The units: certified, timed out (status UNKNOWN), not reached, and errors.
  - Break the counts down by case and kind.
  - For certified units, give solve, lrat-check and cake_lpr seconds and proof sizes (minimum, median, maximum).
- The largest solver RSS.
- Any SAT, proof rejection or memory problem.
